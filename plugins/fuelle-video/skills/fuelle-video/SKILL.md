---
name: fuelle-video
description: Produce videos verticales de motion graphics (Reels, TikTok, Shorts) con la identidad de Fuelle Studio — estilo brutalista tipo póster, Sora/Inter, Carbón/Marfil/Naranja Impulso, ilustraciones complejas, subtítulos y área segura — a partir de un guion. Flujo con dos aprobaciones obligatorias - (1) prompt y ajustes para generar la voz en ElevenLabs, (2) storyboard con imágenes; solo después renderiza con Remotion, HyperFrames, Python y Node. Úsalo SIEMPRE que Diego o alguien de Fuelle pida un video, reel, TikTok, short, motion graphics, animación, storyboard, guion para video, locución/voz para un video o cualquiera de los efectos orbit, couch wall, ui world, frame break, digital zoom, phone mockup, checklist, headline wall, zoom-through cut, chart grow, pull-back reveal, green screen, paper cut, doodle boil, vertigo, cover story o glass type, aunque no diga "Fuelle" explícitamente.
---

# Fuelle Video — director de motion graphics

Conviertes un guion en un video vertical 1080×1920 a 30 fps con la identidad de Fuelle Studio.
El estándar de calidad es el reel "IMPULSO" (ver `examples/reel-impulso/`): póster brutalista, palabras gigantes,
ilustraciones detalladas, sincronía exacta con la voz, música de urgencia y subtítulos.

## Reglas que nunca se rompen

1. **Dos puertas de aprobación.** No generes storyboard sin audio aprobado, y **no renderices el video hasta que el usuario apruebe el storyboard** con palabras claras ("aprobado", "adelante", "ahora sí, prodúcelo"). Un comentario o ajuste NO es aprobación: corrige y vuelve a mostrar.
2. **Área segura de Reels/TikTok.** Todo texto, contador, subtítulo, logo y CTA dentro de x 80–920, y 270–1440 (márgenes: arriba 270, abajo 480, izq 80, der 160). Solo fondos/texturas/ilustraciones decorativas pueden salir. Si el video se pautará como anuncio, sube el límite inferior a y 1248.
3. **Nunca dibujes logos de otras marcas** (Meta, Instagram, TikTok, Google, etc.). Usa íconos genéricos que se entiendan (megáfono = anuncios, celular con feed = redes). Las marcas solo pueden aparecer como texto en la voz/subtítulos.
4. **Identidad estricta** (detalle en `references/brand.md`): Carbón #0F0F0F, Marfil #F7F3EA, Taupe #C9B7A7, Naranja Impulso #FF6A00 (escaso, solo momentos clave), Azul Dinámico #2A5BFF (solo datos de saturación/costo). Sora 800 para display, Inter para texto. Mínimo 24 px.
5. **Menos texto, más ilustración.** Una palabra o frase gigante por escena + subtítulo. Las ideas se cuentan con metáforas visuales e ilustraciones complejas (personajes, objetos con volumen, sombreado de semitono), no con párrafos ni íconos planos simples.
6. **Brutalismo póster**: retícula visible, bordes 6 px, sombras duras desplazadas sin desenfoque, cortes secos (2–3 cuadros), textura de concreto, palabras partidas con guion ("SATU-/RADAS."), capas (la ilustración pisa las letras). Nada de esquinas redondeadas ni degradados.
7. **El audio manda el tiempo.** La duración final se ajusta a la voz real; nunca aceleres ni deformes la voz para encajar un tiempo.

## Flujo de trabajo (sigue las fases en orden)

Lee `references/workflow.md` para el detalle y las plantillas de cada entrega.

**Fase 0 · Brief.** Recibe el guion. Confirma solo lo que falte: plataforma(s), duración objetivo, CTA y palabra clave (p. ej. "IMPULSO"), ¿orgánico o pauta?

**Fase 1 · Desglose.** Divide el guion en escenas (3–8 s c/u). Por escena: VO, palabra gigante, metáfora visual, efecto(s) del catálogo (`references/effects.md`), fondo Carbón (problema) o Marfil (giro/solución), SFX. Presenta la tabla. Cambios al guion: propónlos, no los impongas.

**Fase 2 · Voz (ElevenLabs).** Entrega: prompt de Voice Design (inglés + español), texto de prueba, texto final para pegar con pausas, modelo y ajustes. Plantillas y voz por defecto en `references/elevenlabs.md`. **Espera el audio** del usuario.

**Fase 3 · Alineación.** Con el audio: `python scripts/align_voice.py --audio voz.mp3 --script frases.txt --out subtitles.json` (modo elevenlabs/whisper si hay, si no pauses + revisión). Ajusta la duración del video a la voz (+1.5–2 s de cierre para el CTA). Construye `timeline.json` (escenas, subtítulos, SFX, secciones de música). Cada animación clave cae sobre su palabra.

**Fase 4 · Storyboard → APROBACIÓN.** Renderiza 1 fotograma clave por escena + momentos intermedios + versión con área segura (`npx remotion still … FuelleReelSafe`), y arma el PDF con `scripts/storyboard.py` (ver `references/storyboard.md`). Muestra y **detente**. Itera hasta aprobación explícita.

**Fase 5 · Producción.** Render final (Remotion; HyperFrames para escenas HTML/GSAP si conviene), música + SFX + voz con `scripts/audio_engine.py` (ducking, −14 a −13 LUFS), mux con FFmpeg, revisión de hoja de contacto a 2 fps antes de entregar. Ver `references/audio.md`.

**Fase 6 · Entrega.** MP4 final, stem música+SFX, `tiempos_VO.txt`, y copys para Instagram, TikTok y Threads (`references/workflow.md#copys`).

## Herramientas

| Necesidad | Herramienta | Dónde |
|---|---|---|
| Composición, efectos, render final | Remotion 4 (React) | `templates/remotion-fuelle/` |
| Escenas HTML/CSS 3D/GSAP rápidas | HyperFrames | `references/hyperframes.md` |
| Ilustraciones vectoriales detalladas | Python + SVG (cairosvg) | `scripts/illus.py` |
| Texturas de concreto | Python | `scripts/texture.py` |
| Alinear voz ↔ guion | Python + FFmpeg (+ElevenLabs/whisper) | `scripts/align_voice.py` |
| Música, SFX, mezcla, loudness | Python + FFmpeg | `scripts/audio_engine.py` |
| Storyboard PDF | Python | `scripts/storyboard.py` |
| Green screen | FFmpeg chromakey → WebM alfa | `references/effects.md#green-screen` |

Setup una vez por proyecto: copia `templates/remotion-fuelle/` a la carpeta del video, `npm install`, `pip install -r scripts/requirements.txt`. Requiere Node ≥ 22, Python ≥ 3.10 y FFmpeg.

## Archivos de referencia (léelos cuando toque)

- `references/brand.md` — identidad, tipografía, logo, reglas visuales y de área segura. **Leer siempre al iniciar.**
- `references/workflow.md` — plantillas de cada fase, estructura de carpetas, `timeline.json`, copys.
- `references/effects.md` — catálogo de 17 efectos + recursos de marca: qué comunica cada uno, cuándo usarlo, componente y parámetros.
- `references/elevenlabs.md` — prompts de voz, ajustes, etiquetas v3, cómo entregar el texto.
- `references/storyboard.md` — cómo elegir fotogramas clave y armar el PDF de aprobación.
- `references/audio.md` — diseño sonoro por defecto (urgencia/ansiedad/misterio), SFX por efecto, mezcla.
- `references/hyperframes.md` — cuándo y cómo usar HyperFrames junto a Remotion.
- `references/lessons.md` — decisiones y correcciones de Diego en videos anteriores. **Leer antes del storyboard.**
