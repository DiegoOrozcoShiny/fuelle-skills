# Diseño sonoro

## Música por defecto: urgencia · ansiedad · misterio (aprobada)
- Reloj (tic-tac en corcheas) todo el video → urgencia.
- Latido grave "lub-dub" en escenas de problema → ansiedad.
- Ostinato en semicorcheas en re menor con segunda menor (re–mi♭) → inquietud; en la solución se resuelve (re–fa–la) pero sigue el pulso.
- Drone grave que se abre + pad agudo disonante → misterio.
- Clímax antes del logo: redoble que acelera; golpe grave en el logo; el reloj se detiene antes del final.
- Medio segundo de **silencio total** después de la frase de giro ("El problema no eres tú:").
Secciones en `timeline.json → music.sections` con moods `problema | pausa | solucion | climax | cierre`.

## SFX por recurso visual
| Visual | SFX |
|---|---|
| Corte duro / palabra gigante que golpea | `hit` |
| Pelota/objeto que cae y rebota | `tock` (+ rebotes con g 0.45 y 0.15) |
| Bloque/barra que aparece | `thump` / `stamp` |
| ✓ en checklist | `pop` o tono corto ascendente |
| Muro que se llena | `tick` por pieza |
| Línea/gasto que sube | `riser` |
| Transición semitono / zoom-through | `whoosh_up` |
| Cruce de gráficas / momento de pago | `ding` |
| Frame break / glass type | `glass` |
| Paper cut | `paper` |
| Logo | `boom` (incluido en mood cierre) |

## Mezcla
`scripts/audio_engine.py` hace ducking automático (la música baja ~60 % cuando habla la voz), normaliza y mide loudness. Objetivo: **−14 a −13 LUFS** integrados para Instagram/TikTok. Entrega siempre el stem música+SFX por separado.
Si el usuario prefiere música licenciada, usa el stem de SFX y respeta los mismos tiempos.
