import numpy as np
from PIL import Image
import fuelle as F, fuelle4 as V, fuelle5 as X, texture
from fuelle import Ctx, CARBON, MARFIL, NARANJA, GRAY_D, GRAY_L, halftone, cropmarks

DUR = 35.0
# anclas: (tiempo nuevo, tiempo del storyboard)  -> sincroniza animación con la voz real
ANCH = [(0,0),(3.0,3.0),(3.08,3.10),(3.96,3.85),(5.00,4.75),(5.78,5.85),(7.3,7.0),(7.6,7.15),(9.05,8.4),
        (10.15,9.45),(10.6,10.0),(11.6,10.55),(12.9,11.5),(14.56,13.2),(16.6,15.0),(17.7,16.2),(18.0,16.6),
        (20.1,19.0),(20.5,19.5),(21.65,20.6),(22.8,22.05),(23.4,22.65),(24.7,23.25),(25.15,23.75),(25.7,24.2),
        (25.75,24.25),(27.2,25.25),(28.4,26.0),(28.5,26.05),(29.55,27.0),(30.0,27.4),(30.1,27.5),(31.9,28.9),
        (32.3,29.3),(33.0,30.2),(35.0,32.0)]
_n = np.array([a for a, b in ANCH]); _o = np.array([b for a, b in ANCH])
def to_old(tn): return float(np.interp(tn, _n, _o))
def to_new(to): return float(np.interp(to, _o, _n))

VO = [(0.11,1.50,"Por más que lo intentas,"),(1.50,2.95,"tus ventas no suben."),
 (3.15,4.95,"Agencias, influencers,"),(4.95,7.20,"cursos... hasta Meta Ads."),
 (7.65,8.90,"El gasto sube."),(9.00,10.45,"Tus ventas, no."),
 (10.85,12.30,"El problema no eres tú:"),
 (12.95,14.50,"las redes están saturadas"),(14.50,16.50,"y destacar es cada vez más caro."),
 (16.95,18.40,"Y el marketing es mucho más"),(18.40,20.00,"que un Instagram bonito."),
 (20.25,21.60,"En Fuelle construimos contigo"),(21.60,22.75,"una infraestructura"),
 (22.75,24.60,"que automatiza tus redes,"),(24.60,25.70,"ahorra gastos"),
 (25.70,28.20,"y te muestra el retorno de cada decisión."),
 (28.45,29.95,"Deja de regalar tu dinero"),(29.95,31.75,"y atrévete a dar ese paso."),
 (31.95,34.20,"Nosotros te acompañamos.")]

def frame(tn, S=2):
    t = to_old(tn)
    if t < 3: bg, fn = CARBON, X.s1
    elif t < 7: bg, fn = CARBON, X.s2
    elif t < 10: bg, fn = CARBON, X.s3
    elif t < 11.5: bg, fn = MARFIL, X.s4a
    elif t < 15: bg, fn = CARBON, X.s4b
    elif t < 19: bg, fn = MARFIL, X.s5
    elif t < 26: bg, fn = MARFIL, X.s6
    else: bg, fn = CARBON, X.s7
    dark = bg == CARBON
    c = Ctx(S, bg)
    c.img.paste(texture.background('dark' if dark else 'light', S), (0, 0))
    V.grid_bg(c, dark)
    fn(c, t)
    if 9.45 <= t < 10.0: halftone(c, (t - 9.45) / 0.55, NARANJA)
    if 10.0 <= t < 10.3: halftone(c, 1 - (t - 10.0) / 0.3, NARANJA)
    cropmarks(c, GRAY_D if dark else GRAY_L)
    V.VO = VO
    V.subtitle(c, tn, dark)
    return c.out()
