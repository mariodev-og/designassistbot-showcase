# Español primero · English below
# Origen: app/carrusel_generator.py del sistema en produccion (fragmento:
# _parse_json_response y _build_piece; se recorto la generacion de imagenes).
# Ilustra: el modelo devuelve JSON con los slides, que hay que parsear a la
# defensiva (el LLM a veces manda texto de mas alrededor del JSON) y recien
# ahi construir la Piece. El copy lo escribe el modelo; la estructura la
# valida el codigo.
#
# --- English ---
# Source: app/carrusel_generator.py from the production system (fragment:
# _parse_json_response and _build_piece; image generation was trimmed).
# Shows: the model returns JSON with the slides, which has to be parsed defensively
# (the LLM sometimes wraps the JSON in extra text) before building the Piece. The
# model writes the copy; the code validates the structure.

def _sanitize_json_string(s: str) -> str:
    """
    Reemplaza comillas tipograficas que Claude suele meter por imitar
    el estilo de la marca (las frases con "..."). El JSON solo acepta " rectas.
    Solo toca el contenido DENTRO del JSON, no las comillas estructurales.
    """
    # Comillas dobles tipograficas -> comilla simple recta (para no romper la estructura JSON)
    # Asi 'el "miedo"' dentro de un string se vuelve "el 'miedo'"
    s = s.replace("“", "'").replace("”", "'")  # " " -> ' '
    s = s.replace("‘", "'").replace("’", "'")  # ' ' -> ' '
    # Guion largo y otros caracteres comunes
    s = s.replace("–", "-").replace("—", "-")  # – — -> -
    return s


def _parse_json_response(raw: str) -> list[dict]:
    """
    Intenta parsear la respuesta de Claude como JSON.
    Si falla, intenta recuperar las variantes completas truncando al ultimo ']' o '}' valido.
    """
    # Limpiar markdown fences si vinieran
    txt = raw.strip()
    if txt.startswith("```"):
        txt = re.sub(r"^```(?:json)?\s*", "", txt)
        txt = re.sub(r"\s*```\s*$", "", txt)

    # Intento 1: parseo directo
    try:
        data = json.loads(txt)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "variantes" in data:
            return data["variantes"]
        return [data]
    except json.JSONDecodeError:
        pass

    # Intento 2: extraer variantes individuales con decoder incremental
    variantes = []
    start = txt.find("[")
    if start < 0:
        raise ValueError("No se encontró array de variantes en la respuesta")

    dec = json.JSONDecoder()
    pos = start + 1
    while pos < len(txt):
        while pos < len(txt) and txt[pos] in " \n\r\t,":
            pos += 1
        if pos >= len(txt) or txt[pos] == "]":
            break
        try:
            obj, end = dec.raw_decode(txt, pos)
            if isinstance(obj, dict):
                variantes.append(obj)
            pos = end
        except json.JSONDecodeError:
            break

    if not variantes:
        raise ValueError(f"No se pudo recuperar ninguna variante. Raw[:200]: {raw[:200]}")
    return variantes


def _build_piece(data: dict, account_id: str, brief: str, funnel_stage: str) -> Piece:
    """Convierte el dict de Claude en un Piece con sus Slides."""
    slides = [
        Slide(
            position=s.get("position", i + 1),
            title=s.get("title"),
            body=s.get("body"),
            image_prompt=s.get("image_prompt"),
        )
        for i, s in enumerate(data.get("slides", []))
    ]

    try:
        fs = FunnelStage(funnel_stage)
    except ValueError:
        fs = FunnelStage.GENERICO

    return Piece(
        account_id=account_id,
        kind=PieceKind.CARRUSEL,
        status=PieceStatus.GENERADO,
        brief=brief,
        funnel_stage=fs,
        caption=data.get("caption"),
        hashtags=data.get("hashtags", []),
        slides=slides,
        generation_log={
            "variante": data.get("variante"),
            "angulo":   data.get("angulo"),
            "titulo":   data.get("titulo"),
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# Funcion principal
# ─────────────────────────────────────────────────────────────────────────────
