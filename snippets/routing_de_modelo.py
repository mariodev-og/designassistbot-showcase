# Español primero · English below
# Origen: app/llm.py del sistema en produccion (fragmento: TASK_TIERS,
# get_model y _estimate_cost).
# Ilustra: el tier de cada tarea (fast/smart) se declara en un solo lugar y
# cada llamada estima su costo por tokens. Es la base del presupuesto y del
# kill-switch de gasto — el mismo patron que en los otros sistemas.
#
# --- English ---
# Source: app/llm.py from the production system (fragment: TASK_TIERS, get_model
# and _estimate_cost).
# Shows: each task's tier (fast/smart) is declared in one place and every call
# estimates its token cost. It's the basis of the budget and the spend kill-switch
# — the same pattern as in the other systems.

TASK_TIERS: dict[str, str] = {
    # fast: output corto, estructura predecible, latencia importa
    "hashtags":          "fast",
    "caption_short":     "fast",
    "clasificacion":     "fast",
    "formato_post":      "fast",
    "start_greeting":    "fast",
    "brief_diario":      "fast",

    # smart: calidad importa, contexto largo, razonamiento
    "guion_carrusel":    "smart",
    "guion_historia":    "smart",
    "estrategia":        "smart",
    "analisis_semanal":  "smart",
    "descripcion_larga": "smart",
    "ayuda_archivo":     "smart",
    "comparar_piezas":   "smart",
}

# Dict final task -> model string, construido desde env vars
TASK_MODEL: dict[str, str] = {
    task: (DEFAULT_MODEL if tier == "smart" else FAST_MODEL)
    for task, tier in TASK_TIERS.items()
}


def register_task(task: str, tier: str = "smart") -> None:
    """Registra una nueva tarea en el routing. Llamar al definir tareas nuevas."""
    TASK_TIERS[task] = tier
    TASK_MODEL[task] = DEFAULT_MODEL if tier == "smart" else FAST_MODEL


# Precios por millon de tokens (actualizar si Anthropic cambia pricing)
_COST_PER_MTOK: dict[str, dict[str, float]] = {
    "claude-sonnet-4-6":         {"input": 3.0,  "output": 15.0},
    "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.0},
    # Agregar nuevos modelos aca si se cambian las env vars
}

_anthropic_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.getenv("DAB_ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError("[LLM] DAB_ANTHROPIC_API_KEY no configurada")
        _anthropic_client = anthropic.AsyncAnthropic(api_key=api_key)
    return _anthropic_client


def get_model(task: str) -> str:
    return TASK_MODEL.get(task, DEFAULT_MODEL)


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    prices = _COST_PER_MTOK.get(model, _COST_PER_MTOK[DEFAULT_MODEL])
    return (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000


async def call_llm(
    messages: list[dict],
    task: str = "guion_carrusel",
    max_tokens: int = 1024,
    system: str | None = None,
    account_id: str | None = None,
    piece_id: str | None = None,
) -> tuple[str, dict[str, Any]]:
    """
    Llama a Claude con retry y tracking de budget.

    Returns:
        (texto_respuesta, usage_dict)
        usage_dict tiene: model, task, input_tokens, output_tokens, cost_usd, duration_ms
    """
    from app.monitoring import registrar_uso, check_budget

    if not check_budget():
        raise RuntimeError("[LLM] Budget agotado. Revisa /stats.")

    # Routing por proveedor: gemini (gratis, testing) o anthropic (produccion)
    if LLM_PROVIDER == "gemini":
        return await _call_gemini(messages, task, max_tokens, system, account_id, piece_id)

    model   = get_model(task)
    client  = _get_client()
    start   = time.time()
