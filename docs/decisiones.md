**🇦🇷 Español · 🇬🇧 [English](#-english)**

# Decisiones de diseño

## 1. El brief de marca lo completa el cliente antes de generar nada

- **Qué se hizo:** un cuestionario estructurado que el cliente llena una vez —
  tono, jerga, palabras prohibidas, ejemplos reales de sus propios captions.
- **Alternativa descartada:** que el modelo infiera la voz de la marca mirando
  el feed de Instagram.
- **Por qué:** sin brief, el output suena a IA genérica y el cliente no lo
  publica. El brief es lo que hace que el copy suene a la marca.
- **Qué costó:** fricción en el onboarding. Hay que perseguir al cliente para
  que lo complete, y hasta que no lo hace el sistema no genera bien.

## 2. La identidad visual se aplica con Pillow, no se le pide al modelo

- **Qué se hizo:** el generador de imágenes produce la base; el logo, la paleta
  y la tipografía se superponen por código con Pillow.
- **Alternativa descartada:** pedirle al modelo que incluya el logo en la imagen.
- **Por qué:** los modelos de imagen no reproducen un logo de forma consistente
  — lo deforman, le cambian el color o lo reinventan. Un logo mal puesto es peor
  que no ponerlo.
- **Qué costó:** menos libertad de composición. El overlay ocupa posiciones
  fijas y no se adapta a cada imagen.

## 3. Nada se publica solo

- **Qué se hizo:** toda pieza pasa por aprobación del cliente antes de publicarse.
- **Por qué:** la voz de la marca es del cliente; la última palabra también.

---

<a name="english"></a>
# 🇬🇧 English — Design decisions

## 1. The brand brief is filled in by the client before generating anything

- **What:** a structured questionnaire the client fills in once — tone, slang,
  forbidden words, real examples of their own captions.
- **Rejected alternative:** have the model infer the brand voice from the
  Instagram feed.
- **Why:** without a brief, the output sounds like generic AI and the client
  won't publish it. The brief is what makes the copy sound like the brand.
- **Cost:** onboarding friction. You have to chase the client to complete it,
  and until they do the system doesn't generate well.

## 2. Visual identity is applied with Pillow, not asked of the model

- **What:** the image generator produces the base; logo, palette and typography
  are overlaid by code with Pillow.
- **Rejected alternative:** ask the model to include the logo in the image.
- **Why:** image models don't reproduce a logo consistently — they warp it,
  change its color or reinvent it. A wrong logo is worse than no logo.
- **Cost:** less compositional freedom. The overlay uses fixed positions and
  doesn't adapt to each image.

## 3. Nothing publishes on its own

- **What:** every piece goes through client approval before publishing.
- **Why:** the brand voice is the client's; so is the last word.
