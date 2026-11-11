# Identidad Fuelle Studio para video

Fuente: `assets/brand/manual-identidad-fuelle.jpeg` (dirección "Editorial + Vibrante") y logo `assets/brand/fuelle-logo-*.png`.
En video se aplica en clave **brutalista tipo póster** (referencias arquitectónicas: concreto, tipografía gigante, un solo acento de color).

## Paleta y uso

| Color | Hex | Uso en video |
|---|---|---|
| Carbón | #0F0F0F | Fondo de escenas de problema/tensión; texto sobre Marfil; bordes |
| Marfil | #F7F3EA | Fondo de escenas de giro/solución; texto sobre Carbón; bloques de titular |
| Taupe | #C9B7A7 | Elementos inactivos, retículas, sombras duras sobre fondo oscuro, piel de ilustraciones |
| Naranja Impulso | #FF6A00 | **Escaso**: segunda línea de la palabra gigante, ✓, tachados, cruce de gráficas, palabra clave del CTA, flecha ↗, transición de semitono. Nunca fondo de escena completa (solo en la transición) |
| Azul Dinámico | #2A5BFF | Solo datos de saturación o costo (contador "Costo por cliente") y detalles mínimos de ilustración |
| Grises texto | #8A8A8A sobre Carbón · #6B6B6B sobre Marfil | Etiquetas pequeñas |

## Tipografía

- **Sora 800 (ExtraBold)** — palabras gigantes, contadores, números. Sora no tiene peso Black: 800 es el máximo.
  En palabras gigantes se **comprime horizontalmente al 80 %** (`POSTER_COMPRESS`) para el efecto póster condensado.
- **Inter 400–600** — subtítulos (SemiBold 30 px), etiquetas en MAYÚSCULAS con tracking 3–6 px (24 px).
- Nada menor a 24 px. Fuentes locales OFL en `assets/fonts/` (no dependas de Google Fonts al renderizar).

## Logo

- Usa siempre el archivo, nunca lo redibujes: `fuelle-logo-marfil.png` sobre Carbón, `fuelle-logo-carbon.png` sobre Marfil, `fuelle-logo-naranja.png` solo en piezas de acento.
- Recurso de marca: flecha diagonal ↗ en naranja.

## Sistema visual brutalista (lo que define "estilo Fuelle")

1. **Palabra gigante por escena** (1–2 líneas, palabras partidas con guion cuando ayuda: "INFRAES-/TRUCTURA."). Última línea en naranja.
2. **Regla técnica** bajo la palabra: línea de 3 px + etiqueta pequeña izquierda + "0X / 0N" derecha.
3. **Retícula visible** de 60 px y **textura de concreto** sutil en todos los fondos.
4. **Bordes 6 px, sombras duras** desplazadas 12–14 px (Carbón sobre Marfil; Taupe o sombra oscura sobre Carbón), sin desenfoque, sin radios.
5. **Capas**: la ilustración pisa parcialmente las letras gigantes (como edificio frente al título de un póster).
6. **Concreto** en volúmenes (barras, escalones, torres): textura con marcas de cimbra horizontales.
7. **Cortes secos**: apariciones en 2–3 cuadros; movimiento por pasos (stop-motion) en flechas y crecimientos. Fundidos solo en la transición de semitono.
8. **Marcas de corte** (crop marks) en las 4 esquinas, todo el video.
9. **Contadores** grandes arriba a la izquierda con etiqueta gris, cuando hay datos que cuentan la historia.
10. **Subtítulo** en bloque Carbón con borde (Marfil en escenas oscuras) y sombra dura (Taupe en oscuro, Naranja en claro), centrado al fondo del área segura.

## Ilustraciones

- Complejas y con volumen: personaje emprendedor (cabello, camisa con botones, pantalón, zapatos), manos, objetos con hoyuelos/texturas, billetes con guilloché, tiendas con toldo, escenarios con reflectores.
- Estilo: contorno Carbón 5–7 px, rellenos planos de la paleta (+ verde billete, piel #D9B79A), sombreado con **semitono de puntos**, sombra dura.
- Librería base: `scripts/illus.py` (golf, canasta, persona en poses, mano, billete, cohete, bolsa de dinero, anuncio genérico, 7 canales, íconos de barras). Amplíala con el mismo estilo; nunca íconos planos de 2 formas.

## Área segura (1080×1920)

```
y 0–270     ← barra superior de la app (sin texto)
x 80–920 · y 270–1440   ← ZONA SEGURA para todo lo importante
x 920–1080  ← columna de botones (like, comentar, compartir)
y 1440–1920 ← caption, usuario, audio (sin texto)
```
Verifica cada fotograma del storyboard con la composición `FuelleReelSafe` o `SafeOverlay`.
