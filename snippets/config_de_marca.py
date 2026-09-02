# Español primero · English below
# Origen: app/brand_config.py del sistema en produccion (fragmento: la
# dataclass BrandConfig y su carga; se recorto el armado de descripciones).
# Ilustra: cada cuenta tiene su identidad (paleta, logo, tono, jerga) como
# dato estructurado. El generador lee de aca, no de valores hardcodeados,
# y por eso agregar una marca nueva es cargar config, no tocar codigo.
#
# --- English ---
# Source: app/brand_config.py from the production system (fragment: the BrandConfig
# dataclass and its loading; the description builder was trimmed).
# Shows: each account has its identity (palette, logo, tone, slang) as structured
# data. The generator reads from here, not from hardcoded values, so adding a new
# brand means loading config, not touching code.

@dataclass
class BrandConfig:
    account_id: str
    # Voz / tono
    tone:              str = "profesional y directo"
    voice:             str = ""
    emojis:            str = ""
    pillars:           list[str] = field(default_factory=list)
    signature_phrases: list[str] = field(default_factory=list)
    forbidden_words:   list[str] = field(default_factory=list)
    # CTAs
    cta_keywords:      dict[str, str] = field(default_factory=dict)
    cta_formula:       str = ""
    content_structure: str = ""
    # Formato
    hashtags:          list[str] = field(default_factory=list)
    hashtags_count:    str = ""
    funnel_desc:       dict[str, str] = field(default_factory=lambda: dict(_DEFAULT_FUNNEL_DESC))
    # Audiencia
    audience:          dict = field(default_factory=dict)
    avatar_phrases:    list[str] = field(default_factory=list)
    objections:        dict = field(default_factory=dict)
    legal_limits:      list[str] = field(default_factory=list)
    # Visual / programa
    visual_style:      dict = field(default_factory=dict)
    program:           dict = field(default_factory=dict)
    palette:           dict = field(default_factory=dict)
    fonts:             dict = field(default_factory=dict)
    logo_storage_path: str | None = None
    voice_examples:    list[str] = field(default_factory=list)
    custom_stages:     list[dict] = field(default_factory=list)

    def get_funnel_label(self, stage_id: str) -> str:
        """Label legible para cualquier etapa, incluyendo las personalizadas."""
        if stage_id.startswith("custom_"):
            for cs in self.custom_stages:
                if cs.get("id") == stage_id and cs.get("nombre"):
                    return cs["nombre"]
        return {
            "tofu": "TOFU — Atraccion",
            "mofu": "MOFU — Consideracion",
            "bofu": "BOFU — Conversion",
            "generico": "Personalizada",
        }.get(stage_id, stage_id.upper())

    def to_system_prompt_section(self) -> str:
        """Construye la seccion del system prompt con todo el contexto de marca."""
        lines = []
        if self.tone:
            lines.append(f"TONO: {self.tone}")
        if self.voice:
            lines.append(f"VOZ: {self.voice}")
        if self.emojis:
            lines.append(f"USO DE EMOJIS: {self.emojis}")
        if self.pillars:
            lines.append(f"PILARES DE CONTENIDO (rotar entre estos):\n- " + "\n- ".join(self.pillars))
        if self.signature_phrases:
            lines.append(f"FRASES TIPICAS DE LA MARCA (usar como referencia, no copiar literal):\n- " + "\n- ".join(self.signature_phrases))
        if self.forbidden_words:
            lines.append(f"PALABRAS PROHIBIDAS (NUNCA usar): {', '.join(self.forbidden_words)}")
        if self.avatar_phrases:
            lines.append(f"FRASES TEXTUALES DEL AVATAR (usar para hooks de identificacion):\n- " + "\n- ".join(self.avatar_phrases))
        if self.objections:
            obj_str = "\n".join(f"- '{k}' → {v}" for k, v in self.objections.items())
            lines.append(f"OBJECIONES TIPICAS Y SUS RESPUESTAS:\n{obj_str}")
        if self.cta_keywords:
            cta_str = "\n".join(f"- {k}: {v}" for k, v in self.cta_keywords.items())
            lines.append(f"PALABRAS CLAVE DE CTA (elegir UNA segun el tema):\n{cta_str}")
        if self.cta_formula:
            lines.append(f"FORMULA DEL CTA: {self.cta_formula}")
        if self.content_structure:
            lines.append(f"ESTRUCTURA DE CADA PIEZA: {self.content_structure}")
        if self.hashtags:
            lines.append(f"HASHTAGS OBLIGATORIOS: {', '.join(self.hashtags)}")
        if self.hashtags_count:
            lines.append(f"CANTIDAD DE HASHTAGS: {self.hashtags_count}")
        if self.legal_limits:
            lines.append(f"LIMITES LEGALES:\n- " + "\n- ".join(self.legal_limits))
        if self.program:
            prog_str = ", ".join(f"{k}: {v}" for k, v in self.program.items() if not isinstance(v, (list, dict)))
            if prog_str:
                lines.append(f"PROGRAMA QUE SE VENDE: {prog_str}")
        return "\n\n".join(lines)
