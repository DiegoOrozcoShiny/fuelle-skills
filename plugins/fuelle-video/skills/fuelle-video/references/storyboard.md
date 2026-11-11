# Storyboard de aprobación

## Qué incluir
- **Página 1**: 1 fotograma clave por escena (el momento más representativo, con la ilustración y la palabra gigante completas).
- **Página 2**: momentos intermedios importantes: transiciones (semitono, zoom-through), beats (✓, golpes), el "momento de pago".
- **Página 3**: los mismos fotogramas de la página 1 con la superposición de área segura.
Cada tarjeta: número, timecode, VO entre comillas, descripción de 1–2 líneas de lo que se mueve.

## Cómo generarlo
```bash
# stills limpios (escala 1) y con área segura
npx remotion still src/index.ts FuelleReel     ../storyboard/s1.png      --frame=66
npx remotion still src/index.ts FuelleReelSafe ../storyboard/s1_safe.png --frame=66
python scripts/storyboard.py --spec ../storyboard/storyboard.json --out-dir ../storyboard --name Fuelle_Storyboard_v1
```
`storyboard.json`: ver docstring de `scripts/storyboard.py`. Versiona (v1, v2…) cada iteración; nunca sobrescribas.

## Al presentarlo
- Resume cambios vs la versión anterior.
- Lista numerada (máx. 4) de decisiones que el usuario debe confirmar (ej. compresión tipográfica, sombras, duración).
- Termina con: "¿Lo apruebas para renderizar o ajustamos algo?" y **no renderices** hasta un sí explícito.
