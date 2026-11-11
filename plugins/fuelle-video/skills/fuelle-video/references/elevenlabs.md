# Voz con ElevenLabs

## Voz por defecto de Fuelle (aprobada por Diego)
Femenina, seductora pero **enérgica y ágil** (no lenta ni susurrada), español de México neutro, ~30 años.

### Prompt de Voice Design (pegar en inglés)
```
A confident, seductive and energetic female voice in her early 30s, native Mexican Spanish speaker with a neutral Mexico City accent. Warm, smooth and slightly low-pitched, with a magnetic, self-assured tone and a playful smile in her voice. Upbeat, dynamic delivery with a quick, punchy pace — she speaks with drive and conviction, landing key words with emphasis, like a bold brand commercial for social media. Charismatic and persuasive, never slow, sleepy or whispery. Studio-quality recording, clean and crisp, no background noise, no reverb.
```
Si la voz ya existe en la cuenta del usuario, pide su nombre y salta el diseño.

### Ajustes (Eleven Multilingual v2)
| Ajuste | Valor |
|---|---|
| Stability | 35 % |
| Similarity | 80 % |
| Style exaggeration | 35 % (25 % si suena teatral) |
| Speaker boost | ON |
| Speed | 1.10 (máx. 1.15) |

### Eleven v3 (alternativa con más actuación)
Etiquetas al inicio de frase: `[energetic]`, `[confident]`, `[excited]`, `[serious]`, `[softly]`. Pausas con "..." o saltos de línea.

## Qué entregar en la Fase 2
1. Prompt de voz (EN + ES) — solo si hay que diseñarla.
2. Texto de prueba (≥100 caracteres, del propio guion).
3. **Texto final** para pegar, con pausas `<break time="0.3s" />` (v2) en los cambios de escena y `0.5s` antes de giros dramáticos.
4. Tabla de ajustes.
5. Recomendación: generar en una sola toma; si una frase sale mal, regenerar solo esa y pegarla en su lugar.

## Alineación posterior
- Con API key: `ELEVENLABS_API_KEY=… python scripts/align_voice.py --mode elevenlabs` (Forced Alignment, tiempos por palabra).
- Sin API: `--mode whisper` (faster-whisper local) o `--mode pauses` (aproximado, verificar a oído).
