# Fuelle Studio · Skills para Claude

Marketplace privado de plugins de Fuelle Studio para **Claude Code** (y Claude Cowork).

| Plugin | Qué hace |
|---|---|
| `fuelle-video` | Agente + skill que convierte un guion en un video vertical brutalista con la identidad de Fuelle: voz con ElevenLabs, storyboard para aprobación y render con Remotion, HyperFrames, Python y Node. Incluye 17 efectos (orbit, couch wall, UI world, frame break, digital zoom, phone mockup, checklist, headline wall, zoom-through cut, chart grow, pull-back reveal, green screen, paper cut, doodle boil, vertigo, cover story, glass type). |

## Requisitos en tu computadora
- Claude Code actualizado
- Node.js ≥ 22, Python ≥ 3.10, FFmpeg en el PATH
- (Opcional) `ELEVENLABS_API_KEY` para alineación exacta de la voz, o `pip install faster-whisper`

## Instalar
```bash
# dentro de Claude Code
/plugin marketplace add <tu-usuario>/fuelle-skills
/plugin install fuelle-video@fuelle-studio
```

## Usar
```
/fuelle-video  <pega aquí tu guion>
```
El agente: 1) desglosa escenas y te da el prompt de voz para ElevenLabs → 2) con tu MP3 alinea y arma el storyboard (PDF) → 3) cuando escribes "aprobado", renderiza el video, mezcla el audio y te entrega MP4 + stems + tiempos + copys.

## Probar los efectos
```bash
cd plugins/fuelle-video/skills/fuelle-video/templates/remotion-fuelle
npm install
npx remotion studio        # abre EffectsShowcase y FuelleReel en el navegador
```

## Actualizar
Haz cambios, sube la versión en `plugins/fuelle-video/.claude-plugin/plugin.json` y `git push`. En Claude Code: `/plugin marketplace update fuelle-studio`.

## Licencias
Sora e Inter: SIL Open Font License (ver `assets/fonts/OFL-*.txt`). Remotion requiere licencia de empresa para compañías de más de 3 personas (ver remotion.dev/license). HyperFrames: Apache-2.0.
