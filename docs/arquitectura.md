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
