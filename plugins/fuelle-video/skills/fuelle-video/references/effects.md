# Catálogo de efectos

Todos los componentes están en `templates/remotion-fuelle/src/effects/` (exportados en `effects/index.ts`) y se ven funcionando en la composición `EffectsShowcase` (3 s por efecto). Usan el tiempo local de su `<Sequence>`: los parámetros `at`, `breakAt`, `durationInFrames` están en cuadros desde el inicio de la escena.

## Cómo elegir
| Si la escena dice… | Usa |
|---|---|
| "intentaste muchas cosas", lista de opciones | couch-wall, orbit, paper-cut |
| saturación, ruido, demasiado | couch-wall, headline-wall, vertigo |
| datos, crecimiento, retorno | chart-grow, pull-back-reveal |
| sistema, tecnología, automatización | ui-world, phone-mockup, orbit |
| beneficios o pasos | checklist, chart-grow |
| giro / revelación | zoom-through-cut, frame-break, pull-back-reveal |
| ansiedad, presión | vertigo, digital-zoom, headline-wall |
| autoridad, marca, cierre | cover-story, glass-type |
| cercanía, hecho a mano, proceso | doodle-boil, paper-cut |
| persona real hablando | green-screen |

Máximo 2 efectos "grandes" por escena. No repitas el mismo efecto en escenas consecutivas.

---

### 1. Orbit — `<Orbit center items cx cy rx ry turnsPerSecond itemSize />`
Elementos que giran en elipse 3D alrededor de un centro; los de atrás se achican y pasan detrás. **Comunica:** ecosistema, todo gira alrededor de tu negocio. **SFX:** riser suave. **Tip:** 4–6 ítems ilustrados; centro = palabra gigante o logo.

### 2. Couch Wall (muro de tarjetas) — `<CouchWall tiles cols tileW tileH fillFrames panY />`
Un muro de piezas que se llena a golpes hasta saturar la pantalla y se desplaza lento. **Comunica:** saturación, volumen, "todos hacen lo mismo"; o portafolio/testimonios. **SFX:** `tick` por pieza. Pon la palabra gigante en un bloque brutalista encima.
> Interpretación: "couch wall" se tomó como *muro de tarjetas*. Si Diego se refería a otro efecto, actualiza esta sección.

### 3. UI World — `<UIWorld panels travel durationInFrames perspective />`
La cámara vuela dentro de un espacio 3D lleno de paneles de interfaz (métricas, chats, dashboards). **Comunica:** sistema, infraestructura, tecnología. **Tip:** paneles con ilustración/datos reales del guion; alterna `rotY` ±14°. Alternativa: escena HTML en HyperFrames.

### 4. Frame Break — `<FrameBreak x y w h background subject breakAt popScale />`
El sujeto empieza dentro de un marco y en `breakAt` se sale con un golpe y sacudida. **Comunica:** romper el molde, salir de lo de siempre. **SFX:** `glass` + `hit`.

### 5. Digital Zoom — `<DigitalZoom punches=[{at, scale, fx, fy, hold}]>…</DigitalZoom>`
Punch-in seco de 2 cuadros hacia un punto con destello de scanlines y desfase naranja/azul. **Comunica:** "mira esto", énfasis en un dato. **SFX:** `hit` corto. Úsalo sobre una palabra o número clave, máximo 2 por escena.

### 6. Phone Mockup — `<PhoneMockup x y width scrollPx durationInFrames tiltDeg>…</PhoneMockup>`
Teléfono genérico brutalista (sin marca) con contenido que hace scroll y giro 3D leve. **Comunica:** redes, app, contenido. **Regla:** nada de interfaces reconocibles de Instagram/TikTok; feed genérico.

### 7. Checklist — `<Checklist items=[{text, at, icon}] y dark rowH />`
Lista que se marca a golpes con ✓ naranja estampado, sincronizado con la voz. **Comunica:** beneficios, pasos, entregables. **SFX:** `stamp` + `pop`.

### 8. Headline Wall — `<HeadlineWall words highlightRow rows size speed dark top />`
Filas de titulares repetidos que corren en direcciones alternas; una fila en naranja. **Comunica:** ruido, presión, mensaje repetido; o fondo de impacto para el CTA. Bueno como fondo de Vertigo.

### 9. Zoom-Through Cut — `<ZoomThroughCut from to fx fy durationInFrames maxScale />`
La cámara entra por un hueco (la "O" de una palabra, una ventana, la pantalla del teléfono) y aparece la escena siguiente. **Comunica:** transición problema → solución. **SFX:** `whoosh_up` + `hit` al llegar. Calcula `fx, fy` en el centro del hueco.

### 10. Chart Grow — `<ChartGrow bars=[{label, value, at, color, icon}] x y w h max prefix suffix dark />`
Barras que suben por golpes con el valor contando, retícula visible. **Comunica:** resultados, crecimiento, comparación. Para líneas que se cruzan (momento de pago) ver el ejemplo del reel IMPULSO (escena 6b).

### 11. Pull-Back Reveal — `<PullBackReveal fx fy startScale durationInFrames stepped>…</PullBackReveal>`
Empieza en un detalle y se aleja por saltos hasta revelar todo. **Comunica:** contexto, "el panorama completo". **SFX:** `whoosh_down`.

### 12. Green Screen — `<GreenScreen src x y width outline shadow />`
Persona u objeto grabado en verde, recortado con contorno marfil tipo recorte y sombra dura, sobre la escena de marca.
Pre-proceso:
```bash
ffmpeg -i grabacion.mp4 -vf "chromakey=0x00FF00:0.13:0.06,despill=green,scale=1080:-2" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 4M public/footage/sujeto.webm
```
Ajusta `similarity` (0.10–0.18) y `blend` si quedan bordes verdes. Requiere que el usuario entregue el video.

### 13. Paper Cut — `<PaperCut layers=[{node, color, x, y, w, h, from, delay, seed}] />`
Capas de papel con borde rasgado que entran en stop-motion (12 fps) con sombra dura. **Comunica:** artesanal, construir paso a paso, "hecho contigo". **SFX:** `paper`.

### 14. Doodle Boil — `<DoodleBoil width height strength every><DrawPath d length progress color width /></DoodleBoil>`
Trazos a mano que "hierven" (line boil) y se dibujan. **Comunica:** idea, boceto, anotación sobre una gráfica (círculo, flecha, subrayado). Úsalo como capa de anotación encima de otras escenas.

### 15. Vertigo — `<Vertigo background subject durationInFrames bgScale subjectScale fx fy />`
Dolly zoom: el fondo crece mientras el sujeto se mantiene o achica. **Comunica:** ansiedad, abrumo, revelación incómoda. **SFX:** riser grave + latido (música en mood problema).

### 16. Cover Story — `<CoverStory masthead subject coverLines issue dark />`
Portada de revista brutalista: cabecera gigante, sujeto encima de las letras, titulares de portada a golpes y código de barras. **Comunica:** autoridad, caso de éxito, lanzamiento. Ideal para testimonios o anuncios.

### 17. Glass Type — `<GlassType text y size dark durationInFrames glassW glassH label />`
Tipografía gigante detrás de un bloque de vidrio esmerilado (backdrop-filter) que se desliza; sombra dura naranja. **Comunica:** claridad, transparencia, premium. **SFX:** `glass` suave.

---

## Recursos de marca (siempre disponibles)
| Recurso | Componente | Uso |
|---|---|---|
| Palabra gigante póster | `GiantType` + `PosterRule` | 1 por escena |
| Contador grande | `Counter` | datos que cuentan la historia (intentos, ventas, costo) |
| Transición de semitono | `HalftoneWipe` | cambio Carbón ↔ Marfil (problema → giro) |
| Bloque brutalista | `BrutBlock` | titulares sobre fondos cargados, CTA |
| Ilustraciones | `Illustration` + `scripts/illus.py` | metáforas visuales |
| Subtítulos | `Subtitle` | siempre |
| Crop marks / retícula / concreto | `CropMarks`, `Background` | siempre |
| Área segura (QA) | `SafeOverlay` | storyboard |
