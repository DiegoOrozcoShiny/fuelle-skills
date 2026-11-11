# Flujo detallado y plantillas

## Estructura de carpetas de cada video

```
videos/AAAA-MM-DD_nombre/
├── guion.txt                 # guion original del usuario
├── frases.txt                # una frase de subtítulo por línea (Fase 1)
├── voz/voz.mp3               # audio de ElevenLabs (Fase 2, lo trae el usuario)
├── remotion/                 # copia de templates/remotion-fuelle
│   ├── public/audio/mix.wav
│   ├── public/illus/*.png    # ilustraciones generadas con illus.py
│   └── src/timeline.json     # escenas + subtítulos + SFX + música
├── storyboard/               # stills, storyboard.json, PDF
└── entregables/              # MP4 final, stems, tiempos_VO.txt, copys.md
```

## Fase 1 · Tabla de desglose (entregar así)

| # | Tiempo aprox. | VO | Palabra gigante | Metáfora / ilustración | Efecto | Fondo | SFX |
|---|---|---|---|---|---|---|---|
| 01 | 0–3 s | "Por más que lo intentas…" | NO / SUBEN. | Cohete que intenta despegar 3 veces | chart-grow | Carbón | riser + caída |

Reglas: arco problema (Carbón) → giro (Marfil) → solución (Marfil) → cierre/CTA (Carbón). Máximo 1 palabra gigante por escena. Varía los efectos (no repitas el mismo efecto en escenas seguidas). Usa al menos un "momento de pago visual" (cruce de líneas, cohete que despega, marco que se rompe).

## Fase 2 · Entrega de voz

Ver `elevenlabs.md`. Entrega en bloques de código: prompt EN, prompt ES, texto de prueba, texto final con pausas, tabla de ajustes. Cierra pidiendo el MP3.

## Fase 3 · timeline.json

```json
{
  "title": "Reel IMPULSO", "fps": 30, "duration": 35.0,
  "voice": "audio/voz.mp3", "mix": "audio/mix.wav",
  "subtitles": [ {"start":0.11,"end":1.50,"text":"Por más que lo intentas,"} ],
  "scenes": [ {"id":"s1","start":0,"end":3.0,"bg":"dark","effect":"chart-grow"} ],
  "music": { "preset":"urgencia", "bpm":120,
             "sections":[{"start":0,"end":16.6,"mood":"problema"},{"start":16.6,"end":28.4,"mood":"solucion"},
                         {"start":28.4,"end":31.9,"mood":"climax"},{"start":31.9,"end":35,"mood":"cierre"}],
             "silences":[[12.3,12.9]] },
  "sfx": [ {"t":3.08,"type":"tock"}, {"t":26.42,"type":"ding"} ]
}
```
- `mix` se llena con `audio/mix.wav` después de correr `audio_engine.py` (vacío = sin audio en storyboard).
- `duration` = fin de la última palabra + 1.3–2 s para sostener el CTA.
- Cada evento visual clave (golpe, ✓, cruce) se ancla al inicio de su palabra según `subtitles_words.json`.
- Cada escena es un componente en `src/scenes/` registrado en `src/scenes/index.ts` con su `id`.

## Fase 4 · Storyboard

Ver `storyboard.md`. Mensaje al usuario: qué cambió, decisiones que necesita confirmar (máx. 4, numeradas) y la pregunta "¿Lo apruebas para renderizar o ajustamos algo?".

## Fase 5 · Comandos de producción

```bash
cd remotion
npx remotion still src/index.ts FuelleReelSafe ../storyboard/s1_safe.png --frame=60
python ../../scripts/audio_engine.py --timeline src/timeline.json --voice ../voz/voz.mp3 --out public/audio/mix.wav --stems ../entregables/stems
npx remotion render src/index.ts FuelleReel ../entregables/video.mp4 --codec=h264 --crf=17
ffmpeg -i ../entregables/video.mp4 -vf "fps=2,scale=150:-1,tile=10x7" -frames:v 1 ../storyboard/hoja_contacto.png   # QA
```
QA antes de entregar: hoja de contacto a 2 fps, loudness (−14 a −13 LUFS), duración, que ningún texto salga del área segura, que el subtítulo coincida con la voz.

## Fase 6 · Entregables

1. `video.mp4` (H.264, 1080×1920, 30 fps, AAC 192 kbps)
2. `stems/musica_sfx.wav`
3. `tiempos_VO.txt` (inicio – fin | frase)
4. `copys.md` con:

### Copys
- **Instagram**: gancho (1 línea) → problema → giro → beneficios con ↗ → CTA "Comenta PALABRA" → 8–10 hashtags.
- **TikTok**: 2 líneas + CTA + 3–5 hashtags (el video manda).
- **Threads**: texto que funcione sin video, lista corta de "no funcionó", insight, cierre con pregunta abierta; sin hashtags.
Usa la misma palabra clave del CTA del video (permite automatizar respuestas por DM).
