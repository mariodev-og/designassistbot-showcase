**🇦🇷 Español · 🇬🇧 [English](#-english)**

# Arquitectura

## Flujo de datos

```
1. El cliente completa el brief de marca una vez (docs/brief_de_marca.md):
   tono, jerga, palabras que la marca nunca usaría, ejemplos reales de captions.

2. Al generar, Claude recibe ese brief como contexto y escribe el copy de cada
   slide en la voz de la marca. Devuelve JSON estructurado.

3. El JSON se parsea a la defensiva: el modelo a veces manda texto alrededor del
   JSON, así que hay que aislarlo antes de construir la pieza.

4. Para cada slide se genera una imagen (Gemini) y se le aplica la identidad de
   marca con Pillow: logo en su posición, paleta, tipografía. El modelo no toca
   el logo — lo pone el código.

5. La pieza queda pendiente de aprobación. El cliente revisa antes de publicar.
```

## Por qué el brief primero

La diferencia entre "contenido de IA" y "contenido de la marca" no está en el
modelo, está en el contexto. El brief es ese contexto, y por eso es lo primero
que se completa y lo que condiciona cada generación.

---

<a name="english"></a>
# 🇬🇧 English — Architecture

## Data flow

1. The client fills in the brand brief once (docs/brief_de_marca.md): tone,
   slang, words the brand would never use, real caption examples.
2. When generating, Claude receives that brief as context and writes each
   slide's copy in the brand's voice. It returns structured JSON.
3. The JSON is parsed defensively: the model sometimes wraps it in extra text,
   so it has to be isolated before building the piece.
4. For each slide an image is generated (Gemini) and the brand identity is
   applied with Pillow: logo in place, palette, typography. The model doesn't
   touch the logo — the code places it.
5. The piece is left pending approval. The client reviews before publishing.

## Why the brief first

The difference between "AI content" and "brand content" isn't in the model, it's
in the context. The brief is that context, and that's why it's the first thing
filled in and what conditions every generation.
