// Identidad Fuelle Studio — fuente única de verdad para colores, tipografía y área segura.
export const W = 1080;
export const H = 1920;
export const FPS = 30;

export const C = {
  carbon: "#0F0F0F",   // fondo de escenas de problema
  marfil: "#F7F3EA",   // fondo de escenas de giro/solución
  taupe: "#C9B7A7",    // inactivos, retículas, sombras en fondo oscuro
  naranja: "#FF6A00",  // acento: SOLO momentos clave
  azul: "#2A5BFF",     // SOLO datos de saturación/costos
  grayOnDark: "#8A8A8A",
  grayOnLight: "#6B6B6B",
  shadowDark: "#3C3630",
} as const;

// Área segura de Reels/TikTok (px en lienzo 1080×1920)
export const SAFE = { x0: 80, x1: 920, y0: 270, y1: 1440 } as const;
export const SAFE_W = SAFE.x1 - SAFE.x0;

export const FONT = {
  display: "Sora",  // titulares, contadores, palabras gigantes (peso 800)
  text: "Inter",    // etiquetas, subtítulos (400–600), MAYÚSCULAS con tracking
} as const;

// Compresión horizontal de Sora para el efecto póster brutalista
export const POSTER_COMPRESS = 0.8;

export const BORDER = 6;       // bordes brutalistas
export const HARD_SHADOW = 14; // sombra dura desplazada, sin desenfoque
