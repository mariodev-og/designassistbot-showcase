# DesignAssistBot

> Asistente que genera carruseles, historias y posts de Instagram con la voz de cada marca, no con la voz genérica de una IA.

**Este repositorio es una vitrina técnica, no el sistema.** El sistema en
producción es privado. Acá están la arquitectura, las decisiones de diseño y
algunos fragmentos de código elegidos para mostrar cómo está resuelto.

---

## El problema

Un community manager necesita publicar seguido y con una voz consistente. Las
herramientas de IA generan texto correcto pero plano: suena a IA, no a la marca,
y el cliente no lo publica. Y la imagen que devuelven no respeta el logo ni la
paleta de la cuenta.

DesignAssistBot arma la pieza completa desde un brief de marca que completa el
cliente: el modelo escribe el copy condicionado por ese brief, se genera la
imagen, y la identidad visual (logo, paleta, tipografía) se aplica por código
por encima — no se le pide al modelo, porque no reproduce un logo de forma
consistente.

## Arquitectura

![Arquitectura de DesignAssistBot](docs/img/arquitectura.svg)

```
Brief de marca (lo completa el cliente: tono, jerga, ejemplos reales)
      │
      ▼
Claude escribe el copy condicionado por el brief  ──►  JSON de slides
      │                                                     │ parseo defensivo
      ▼                                                     ▼
Generación de imagen (Gemini)  ──►  overlay de marca (Pillow: logo, paleta, fuente)
      │
      ▼
Pieza (carrusel / historia / post)  ──►  aprobación humana  ──►  publicación
```

Detalle en [`docs/arquitectura.md`](docs/arquitectura.md).

## Stack

| Capa | Tecnología | Por qué esta y no otra |
|---|---|---|
| Backend | Python · FastAPI | Async para la cola de generación |
| Base de datos | PostgreSQL sobre Supabase | Config por cuenta + Storage de imágenes |
| Interfaz | Jinja2 · Tailwind · Chart.js | Panel de 20 vistas con métricas de Instagram |
| Texto | Claude | Copy en la voz de la marca, routing por tarea |
| Imagen | Gemini + Pillow | El modelo genera; Pillow aplica la identidad |
| Despliegue | Render | — |

## Decisiones de diseño

Detalle en [`docs/decisiones.md`](docs/decisiones.md).

### El brief de marca lo completa el cliente antes de generar nada

- **Qué se hizo:** un cuestionario estructurado (tono, jerga, palabras prohibidas, ejemplos reales de captions propios). Ver [`docs/brief_de_marca.md`](docs/brief_de_marca.md).
- **Alternativa descartada:** que el modelo infiera la voz de la marca desde el feed.
- **Por qué:** sin brief, el output suena a IA genérica y el cliente no lo publica.
- **Qué costó:** fricción en el onboarding — hay que perseguir al cliente para que lo llene.

### La identidad visual se aplica con Pillow, no se le pide al modelo

- **Qué se hizo:** logo, paleta y tipografía se superponen por código sobre la imagen generada.
- **Alternativa descartada:** pedirle al generador de imágenes que incluya el logo.
- **Por qué:** el modelo no reproduce un logo de forma consistente — lo deforma o lo reinventa.
- **Qué costó:** menos libertad de composición; el overlay es más rígido.

## Decisiones sobre este repositorio

- **Es una vitrina, no un espejo.** El sistema en producción tiene material de
  clientes: nombres de marca, cuentas de Instagram, captions reales. No es publicable entero.
- **Se publica lo que se lee.** Tres fragmentos elegidos, uno por decisión, más
  el brief de marca en blanco como artefacto de producto.
- **Este proyecto no tiene suite de tests.** Se dice acá en vez de improvisar
  una para la vitrina. La calidad se apoya en la documentación del pipeline.
- **Los nombres de cliente están reemplazados** por ficticios, no ofuscados.

## Qué hay en este repositorio

| Carpeta | Qué contiene |
|---|---|
| [`docs/`](docs/) | Arquitectura, decisiones, el brief de marca y capturas |
| [`snippets/`](snippets/) | Tres fragmentos comentados, uno por decisión |

Los fragmentos de `snippets/` no forman un programa ejecutable: están para leerse.

## Escala del proyecto

Panel propio de 20 vistas con análisis semanal de métricas de Instagram.
Entregado a un cliente entre mayo y junio de 2026.

## Estado

Entregado. Repositorio de producción privado.

---

## Código completo

El repositorio de producción es privado porque contiene material de clientes.
Puedo dar acceso de lectura durante un proceso de selección: escribime a
**mario1804.dev@gmail.com**.

## Licencia

Todos los derechos reservados. Ver [`LICENSE`](LICENSE).
