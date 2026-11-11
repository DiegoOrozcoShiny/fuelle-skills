# HyperFrames (HeyGen) junto a Remotion

HyperFrames renderiza HTML/CSS/JS (incluido GSAP) a MP4 con Chrome headless + FFmpeg. Es ideal para escenas que el agente escribe más rápido en HTML: UI World con CSS 3D, interfaces/dashboards falsos, tipografía con efectos CSS (glass, backdrop-filter), animaciones GSAP.

## Instalación (versión fijada)
```bash
npx skills add heygen-com/hyperframes          # skills oficiales: síguelas para la sintaxis exacta
npm i -D hyperframes@0.8.209                    # versión con ≥ 2 semanas de publicada
npx hyperframes init escena-ui && npx hyperframes preview && npx hyperframes render
```
Lee y obedece las skills oficiales de HyperFrames para la sintaxis de composición (atributos `data-*`, linting).

## Integración con el pipeline Fuelle
1. Renderiza la escena HTML a 1080×1920, 30 fps, con la duración exacta de la escena (`timeline.json`).
2. Usa `templates/hyperframes-fuelle/brand.css` (colores, fuentes locales, área segura, bordes y sombras).
3. Copia el MP4 a `remotion/public/clips/` y móntalo en su escena con `<OffthreadVideo src={staticFile('clips/escena.mp4')} />`.
4. Subtítulos, crop marks y audio se ponen siempre en Remotion (una sola fuente de verdad).

Regla: si una escena se puede hacer bien con los componentes de `templates/remotion-fuelle/src/effects`, prefiere Remotion.
