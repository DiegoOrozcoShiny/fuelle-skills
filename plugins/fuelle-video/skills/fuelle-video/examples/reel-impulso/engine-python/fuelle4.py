import math, random
from PIL import Image, ImageDraw
import fuelle as F
from fuelle import (W, H, CARBON, MARFIL, TAUPE, NARANJA, AZUL, WHITE, GRAY_D, GRAY_L, FPS,
                    Ctx, font, snap, clamp, ease_out, cropmarks, halftone, checkmark, arrow, logo, gasto_curve)
from illus import render

# ---------------- ÁREA SEGURA REELS ----------------
SX0, SX1, SY0, SY1 = 80, 920, 270, 1440      # izq 80 · der 160 (botonera) · arriba 270 · abajo 480
SHADOW_D = (60, 54, 48)                      # sombra dura en escenas oscuras (taupe oscurecido)
TAUPE_D = (142, 125, 110)

VO = [
    (0.00, 3.00, "Por más que lo intentas, tus ventas no suben."),
    (3.00, 4.70, "Agencias, influencers,"),
    (4.70, 7.00, "cursos... hasta Meta Ads."),
    (7.00, 8.40, "El gasto sube."),
    (8.40, 10.00, "Tus ventas, no."),
    (10.00, 11.00, "El problema no eres tú:"),
    (11.50, 13.20, "las redes están saturadas"),
    (13.20, 15.00, "y destacar es cada vez más caro."),
    (15.00, 17.00, "Y el marketing es mucho más"),
    (17.00, 19.00, "que un Instagram bonito."),
    (19.00, 20.60, "En Fuelle construimos contigo"),
    (20.60, 21.80, "una infraestructura"),
    (21.80, 23.20, "que automatiza tus redes,"),
    (23.20, 24.20, "ahorra gastos"),
    (24.20, 26.00, "y te muestra el retorno de cada decisión."),
    (26.00, 27.40, "Deja de regalar tu dinero"),
    (27.40, 28.80, "y atrévete a dar ese paso."),
    (28.90, 30.30, "Nosotros te acompañamos."),
]

# ---------------- utilidades ----------------
def sprite(c, im, x, y, anchor='mm', shadow=None, rot=0, sx=1.0, sy=1.0):
    """im ya viene a escala S. x,y en px de 1080. shadow=(dx,dy,color) sombra dura sin desenfoque."""
    if sx != 1 or sy != 1:
        im = im.resize((max(1, int(im.width * sx)), max(1, int(im.height * sy))), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    w, h = im.size
    S = c.S
    ox = {'l': 0, 'm': w / 2, 'r': w}[anchor[0]]; oy = {'t': 0, 'm': h / 2, 'b': h}[anchor[1]]
    px, py = int(x * S - ox), int(y * S - oy)
    if shadow:
        dx, dy, col = shadow
        sil = Image.new('RGB', im.size, col)
        c.img.paste(sil, (px + int(dx * S), py + int(dy * S)), im.split()[3])
    c.img.paste(im, (px, py), im)

def R(name, w, c, *a, **k): return render(name, w * c.S, *a, **k)

def grid_bg(c, dark):
    col = (26, 26, 26) if dark else (233, 226, 213)
    for x in range(0, W + 1, 60): c.rect(x, 0, x + 1, H, fill=col)
    for y in range(0, H + 1, 60): c.rect(0, y, W, y + 1, fill=col)

def brut_rect(c, x0, y0, x1, y1, fill, border=CARBON, bw=6, sh=12, shcol=CARBON):
    if sh: c.rect(x0 + sh, y0 + sh, x1 + sh, y1 + sh, fill=shcol)
    c.rect(x0, y0, x1, y1, fill=fill)
    if bw: c.rect(x0, y0, x1, y1, outline=border, width=bw)

def hblock(c, lines, y, dark, align='l', size=64, show=None):
    """Titular en bloque brutalista: marfil, borde carbón 6 px, sombra dura. 2.ª línea naranja."""
    f = font('sora', 'ExtraBold', size, c.S)
    maxw = (SX1 - SX0) - 56
    while max(c.tw(s, f) for s in lines) > maxw and size > 44:
        size -= 2; f = font('sora', 'ExtraBold', size, c.S)
    lh = size * 1.14
    bw = max(c.tw(s, f) for s in lines) + 56
    bh = lh * len(lines) + 36
    x0 = SX0 if align == 'l' else (W - bw) / 2
    brut_rect(c, x0, y, x0 + bw, y + bh, MARFIL, CARBON, 6, 14, TAUPE if dark else CARBON)
    n = len(lines) if show is None else show
    for i, s in enumerate(lines[:n]):
        c.text(x0 + 28, y + 18 + i * lh + size * 0.02, s, f, NARANJA if i == 1 else CARBON)
    return y + bh

def counter(c, x, y, label, value, col, dark=True):
    c.text(x, y, label.upper(), font('inter', 'SemiBold', 24, c.S), GRAY_D if dark else GRAY_L, tracking=3)
    c.text(x, y + 30, value, font('sora', 'ExtraBold', 110, c.S), col)

def scene_tag(c, n, dark):
    f = font('inter', 'SemiBold', 24, c.S)
    s = f'{n:02d}/07'; tw = c.tw(s, f, 2)
    x1 = SX1; x0 = x1 - tw - 28
    col = GRAY_D if dark else CARBON
    c.rect(x0, SY0 + 6, x1, SY0 + 50, outline=col, width=3)
    c.text((x0 + x1) / 2, SY0 + 28, s, f, col, anchor='mm', tracking=2)

def subtitle(c, t, dark=True):
    cur = None
    for a, b, s in VO:
        if a <= t < b: cur = s
    if not cur: return
    f = font('inter', 'SemiBold', 30, c.S)
    maxw = (SX1 - SX0) - 60
    lines = [cur]
    if c.tw(cur, f) > maxw:
        words = cur.split(); best = None
        for i in range(1, len(words)):
            a, b = ' '.join(words[:i]), ' '.join(words[i:])
            m = max(c.tw(a, f), c.tw(b, f))
            if best is None or m < best[0]: best = (m, [a, b])
        lines = best[1]
    w = max(c.tw(l, f) for l in lines) + 48; lh = 40; h = lh * len(lines) + 28
    cx = (SX0 + SX1) / 2
    y1 = SY1 - 8; y0 = y1 - h
    brut_rect(c, cx - w / 2, y0, cx + w / 2, y1, CARBON, MARFIL if dark else CARBON, 3, 8, TAUPE if dark else NARANJA)
    for i, l in enumerate(lines):
        c.text(cx, y0 + 14 + i * lh + lh / 2, l, f, MARFIL, anchor='mm')

def panel(c, x0, y0, x1, y1, dark):
    bc = (70, 70, 70) if dark else CARBON
    gc = (34, 34, 34) if dark else (226, 218, 204)
    for i in range(1, 6):
        yy = y0 + (y1 - y0) * i / 6; c.rect(x0, yy, x1, yy + 1, fill=gc)
    for i in range(1, 7):
        xx = x0 + (x1 - x0) * i / 7; c.rect(xx, y0, xx + 1, y1, fill=gc)
    c.rect(x0, y0, x1, y1, outline=bc, width=4)

# ================= ESCENAS =================
def s1(c, t):
    attempts = [(0.35, 220), (1.15, 320), (1.95, 420)]
    x0, xk, x1, yb = 110, 440, 780, 1240
    h = 0; done = []; rising = False
    for (ta, peak) in attempts:
        if t >= ta:
            dt = t - ta; up, hold, fall = 0.22, 0.12, 0.12
            if dt < up: h = peak * ease_out(dt / up); rising = True
            elif dt < up + hold: h = peak; rising = True
            elif dt < up + hold + fall: h = peak * (1 - ((dt - up - hold) / fall) ** 2); rising = False
            elif dt < up + hold + fall + 0.08: h = -16 * math.sin((dt - up - hold - fall) / 0.08 * math.pi); rising = False
            else: h = 0; done.append(peak); rising = False
    counter(c, SX0, SY0 + 10, 'Ventas', f'{120 + int(h / 420 * 28)}', WHITE)
    scene_tag(c, 1, True)
    hblock(c, ['Por más que', 'lo intentas...'], 470, True)
    panel(c, SX0, 720, SX1, 1320, True)
    for pk in done:  # marcas de intentos fallidos
        y = yb - pk
        c.line([(x1 + 90 - 14, y - 14), (x1 + 90 + 14, y + 14)], TAUPE, 6); c.line([(x1 + 90 - 14, y + 14), (x1 + 90 + 14, y - 14)], TAUPE, 6)
    c.line([(x0, yb), (xk, yb), (x1, yb - h)], WHITE, 8)
    ang = math.degrees(math.atan2(h, x1 - xk))
    tipx, tipy = x1, yb - h
    rk = R('cohete', 76, c, h > 0 and rising)
    # el cohete se apoya en la punta de la línea; rot positiva = antihoraria (PIL)
    rot = ang - 90
    a = math.radians(ang)
    sprite(c, rk, tipx + math.cos(a) * 78, tipy - math.sin(a) * 78, 'mm', (8, 8, SHADOW_D), rot)

BALLS = [(3.10, 'agencias', 300), (3.85, 'influencers', 500), (4.75, 'cursos', 700), (5.85, 'ads', 500)]
def basket(c, y_top=1010):
    sprite(c, R('canasta', 720, c), (SX0 + SX1) / 2, y_top, 'mt', (14, 14, SHADOW_D))

def s2(c, t):
    n = sum(1 for ta, _, _ in BALLS if t >= ta + 0.22)
    counter(c, SX0, SY0 + 10, 'Intentos', str(n), WHITE)
    counter(c, 470, SY0 + 10, 'Ventas nuevas', '0', NARANJA)
    scene_tag(c, 2, True)
    hblock(c, ['Lo intentaste todo.'], 470, True)
    for i, (ta, ic, cx) in enumerate(BALLS):
        if t < ta: continue
        ty = 955 if i < 3 else 775
        dt = t - ta; sq = 0; rot = 0
        if dt < 0.22: y = 600 + (ty - 600) * (dt / 0.22) ** 2; rot = -dt * 400
        elif dt < 0.38: u = (dt - 0.22) / 0.16; y = ty - 50 * math.sin(u * math.pi); sq = 0.1 if dt < 0.22 + 2 / FPS else 0
        else: y = ty
        sprite(c, R('golf', 200, c, ic), cx, y, 'mm', (10, 10, SHADOW_D), rot, 1 + sq, 1 - sq)
    basket(c)

def s3(c, t):
    scene_tag(c, 3, True)
    hblock(c, ['El gasto sube.', 'Tus ventas, no.'], SY0 + 20, True, show=2 if t >= 8.4 else 1)
    x0, x1, y0, y1 = SX0, SX1, 560, 1320
    panel(c, x0, y0, x1, y1, True)
    prog = clamp((t - 7.15) / 1.4); N = 60; n = max(2, int(N * prog))
    xa, xb = x0 + 20, x1 - 70
    gp = [(xa + (xb - xa) * i / N, y1 - 40 - (y1 - y0 - 200) * gasto_curve(i / N)) for i in range(n + 1)]
    vp = [(xa + (xb - xa) * i / N, y1 - 120 + 3 * math.sin(i * 0.9)) for i in range(n + 1)]
    if prog > 0.05:
        F.hatch(c, gp, vp, (110, 54, 14))
        c.line(vp, TAUPE, 8); c.line(gp, NARANJA, 10)
        ex, ey = gp[-1]
        sprite(c, R('bolsa', 110 + 40 * prog, c), ex, ey - 20, 'mb', (8, 8, SHADOW_D))
        f = font('inter', 'SemiBold', 24, c.S)
        c.text(x0 + 24, y1 - 150, 'VENTAS', f, TAUPE, tracking=3)
        c.text(x0 + 24, y0 + 24, 'GASTO EN MARKETING', f, NARANJA, tracking=3)

def s4a(c, t):
    scene_tag(c, 4, False)
    hblock(c, ['El problema', 'no eres tú.'], SY0 + 20, False)
    gy = 1330
    c.rect(SX0, gy, SX1, gy + 6, fill=CARBON)
    flipped = t >= 10.55
    sprite(c, R('persona', 300, c, 'stand' if flipped else 'sad'), 250, gy + 4, 'mb', (12, 0, TAUPE))
    hand = R('mano', 330, c)
    if not flipped:
        sprite(c, hand.transpose(Image.FLIP_LEFT_RIGHT), 680, 860, 'mm', (12, 12, CARBON))
    else:
        k = snap(t, 10.55, 3)
        sprite(c, hand, 540 + 20 * (1 - k), 860, 'mm', (12, 12, CARBON))
        brut_rect(c, 760, 760, 920, 960, CARBON, CARBON, 0, 10, NARANJA)
        sprite(c, R('canal', 200, c, 'redes'), 840, 860, 'mm')

def s4b(c, t):
    cols, rows = 4, 6
    cw, ch, g = 252, 336, 12
    gx0 = (W - (cols * cw + (cols - 1) * g)) / 2; gy0 = -40
    order = list(range(cols * rows)); random.Random(7).shuffle(order)
    prog = clamp((t - 11.6) / 2.2)
    shown = int(len(order) * prog ** 0.8)
    for k in order[:shown]:
        i, j = k % cols, k // cols
        sprite(c, R('anuncio', cw, c, (k + k // 4) % 4), gx0 + i * (cw + g), gy0 + j * (ch + g), 'lt')
    cost = int(48 + 264 * prog ** 1.5)
    brut_rect(c, SX0, SY0 + 4, SX0 + 470, SY0 + 190, CARBON, MARFIL, 4, 12, AZUL)
    counter(c, SX0 + 26, SY0 + 26, 'Costo por cliente', f'${cost}', AZUL)
    hblock(c, ['Saturadas.', 'Y cada vez más caras.'], SY0 + 240, True, show=2 if t >= 13.2 else 1)

CH = [('REFERIDOS', 'referidos', -0.5, -1), ('ALIANZAS', 'alianzas', 0.5, -1), ('EVENTOS', 'eventos', -1, 0),
      ('EMAIL', 'email', 1, 0), ('TIENDA', 'tienda', -0.5, 1), ('B2B', 'b2b', 0.5, 1)]
def s5(c, t):
    scene_tag(c, 5, False)
    hblock(c, ['Las redes son', 'solo un canal.'], SY0 + 20, False)
    tw_, th_, g = 260, 250, 18
    cx0, cy0 = (SX0 + SX1) / 2, 520 + th_ * 1.5 + g
    shrink = clamp((t - 16.2) / (3 / FPS))
    if shrink < 1:
        s = 780 + (tw_ - 780) * shrink; cell = (s - 24) / 3; fx0 = cx0 - s / 2; fy0 = cy0 - s / 2
        for i in range(3):
            for j in range(3):
                brut_rect(c, fx0 + i * (cell + 12), fy0 + j * (cell + 12), fx0 + i * (cell + 12) + cell, fy0 + j * (cell + 12) + cell,
                          CARBON, CARBON, 0, 10, TAUPE)
        return
    lf = font('inter', 'SemiBold', 24, c.S)
    def tile(cx, cy, kind, lab, dark, sc=1.0):
        w, h = tw_ * sc, th_ * sc
        x0, y0 = cx - w / 2, cy - h / 2
        brut_rect(c, x0, y0, x0 + w, y0 + h, CARBON if dark else MARFIL, CARBON, 6, 12, NARANJA if dark else CARBON)
        sprite(c, R('canal', int(220 * sc), c, kind), cx, y0 + 10 * sc, 'mt')
        c.rect(x0, y0 + h - 46 * sc, x0 + w, y0 + h, fill=CARBON if not dark else MARFIL)
        c.text(cx, y0 + h - 23 * sc, lab, lf, MARFIL if not dark else CARBON, anchor='mm', tracking=4)
    tile(cx0, cy0, 'redes', 'REDES', True)
    for k, (lab, kind, dx, dy) in enumerate(CH):
        ta = 16.6 + k * 0.33
        if t < ta: continue
        sc = 0.85 + 0.15 * snap(t, ta, 2)
        tile(cx0 + dx * (tw_ + g), cy0 + dy * (th_ + g), kind, lab, False, sc)

BARS = [(22.05, 'REDES', 'auto', 330), (22.65, 'APRENDE', 'aprende', 420), (23.25, 'AHORRO', 'ahorro', 510), (23.75, 'ROI', 'roi', 600)]
def s6(c, t):
    scene_tag(c, 6, False)
    hblock(c, ['En Fuelle construimos contigo', 'tu infraestructura.'], SY0 + 20, False, show=2 if t >= 20.6 else 1)
    if t < 24.2:
        yb = 1270; bw, g = 180, 40
        c.rect(SX0, yb, SX1, yb + 6, fill=CARBON)
        lf = font('inter', 'SemiBold', 24, c.S)
        for i, (ta, lab, ic, hgt) in enumerate(BARS):
            x = SX0 + i * (bw + g)
            if 19.5 + i * 0.5 <= t < ta:
                for k in range(0, int(hgt), 24):
                    c.rect(x, yb - k - 12, x + 5, yb - k, fill=TAUPE); c.rect(x + bw - 5, yb - k - 12, x + bw, yb - k, fill=TAUPE)
                c.rect(x, yb - hgt, x + bw, yb - hgt + 5, fill=TAUPE)
            if t < ta: continue
            s = snap(t, ta, 2); hh = hgt * (0.7 + 0.3 * s)
            brut_rect(c, x, yb - hh, x + bw, yb, CARBON, CARBON, 0, 12, TAUPE)
            sprite(c, R('barra_icon', 150, c, ic), x + bw / 2, yb - hh + 18, 'mt')
            c.text(x + bw / 2, yb + 34, lab, lf, CARBON, anchor='mm', tracking=3)
            if t >= ta + 0.17:
                cs = 64
                brut_rect(c, x + bw / 2 - cs / 2, yb - hh - cs - 22, x + bw / 2 + cs / 2, yb - hh - 22, NARANJA, CARBON, 5, 6, CARBON)
                checkmark(c, x + bw / 2 - 18, yb - hh - cs - 4, 36, CARBON, 8)
        return
    x0, x1, y0, y1 = SX0, SX1, 540, 1320
    panel(c, x0, y0, x1, y1, False)
    prog = clamp((t - 24.25) / 1.0); N = 60; n = max(2, int(N * prog))
    xa, xb = x0 + 20, x1 - 60
    gasto = lambda u: y1 - 120 - (y1 - y0 - 240) * (1 - u) ** 1.6
    ventas = lambda u: y1 - 140 - (y1 - y0 - 240) * u ** 1.4
    gp = [(xa + (xb - xa) * i / N, gasto(i / N)) for i in range(n + 1)]
    vp = [(xa + (xb - xa) * i / N, ventas(i / N)) for i in range(n + 1)]
    c.line(gp, NARANJA, 10); c.line(vp, CARBON, 10)
    f = font('inter', 'SemiBold', 24, c.S)
    c.text(xa + 6, gasto(0) - 26, 'GASTO', f, NARANJA, tracking=3, anchor='ls')
    # cohete sobre la línea de ventas (regresa, ahora sí despega)
    vx, vy = vp[-1]
    if n >= 2:
        px, py = vp[-2]
        ang = math.degrees(math.atan2(py - vy, vx - px))
        sprite(c, R('cohete', 70, c, True), vx, vy - 30, 'mm', (8, 8, TAUPE), ang - 90)
    us = [i / 400 for i in range(401)]
    uc = min(us, key=lambda u: abs(gasto(u) - ventas(u)))
    xc, yc = xa + (xb - xa) * uc, gasto(uc); tc = 24.25 + 1.0 * uc
    if t >= tc:
        dt = t - tc
        for k in range(2):
            ph = ((dt + k * 0.45) % 0.9) / 0.9; r = 20 + 80 * ph
            col = tuple(int(NARANJA[i] * (1 - ph) + MARFIL[i] * ph) for i in range(3))
            c.rect(xc - r, yc - r, xc + r, yc + r, outline=col, width=5)
        brut_rect(c, xc - 18, yc - 18, xc + 18, yc + 18, NARANJA, CARBON, 4, 0)
        lf = font('inter', 'Bold', 26, c.S); lab = 'RETORNO ↗'; tw = c.tw(lab, lf, 3)
        brut_rect(c, xc - tw / 2 - 20, yc + 70, xc + tw / 2 + 20, yc + 124, CARBON, CARBON, 0, 8, NARANJA)
        c.text(xc, yc + 97, lab, lf, MARFIL, anchor='mm', tracking=3)
        c.rect(xc - 3, yc + 20, xc + 3, yc + 70, fill=CARBON)

BILLS = [(26.05, 330, -14), (26.25, 600, 18), (26.45, 460, -6), (26.65, 700, 10), (26.85, 380, 24)]
def s7(c, t):
    if t < 27.4:
        scene_tag(c, 7, True)
        hblock(c, ['Deja de regalar', 'tu dinero.'], SY0 + 20, True)
        for (ta, cx, r0) in BILLS:
            if t < ta: continue
            dt = min(t, 27.0) - ta
            y = 560 + min(1, dt / 0.35) ** 2 * (980 - 560)
            sprite(c, R('billete', 230, c), cx, y, 'mm', (10, 10, SHADOW_D), r0 + dt * 60 * (1 if r0 > 0 else -1))
        basket(c)
        if t >= 27.0:
            k = snap(t, 27.0, 3)
            c.line([(SX0 + 10, 1320), (SX0 + 10 + (SX1 - SX0 - 20) * k, 1320 - 620 * k)], CARBON, 52)
            c.line([(SX0 + 10, 1320), (SX0 + 10 + (SX1 - SX0 - 20) * k, 1320 - 620 * k)], NARANJA, 34)
        return
    if t < 28.9:
        scene_tag(c, 7, True)
        hblock(c, ['Atrévete a', 'dar ese paso.'], SY0 + 20, True)
        n = 4; sw = 190; sh = 130; bx = SX0 + 20; by = 1320
        g = clamp((t - 27.5) / 1.0); g = math.floor(g * 6) / 6
        if g > 0:
            arrow(c, SX0, 1300, SX0 + 780 * g, 1300 - 760 * g, NARANJA, 34, head=60 + 40 * g)
        for i in range(n):
            brut_rect(c, bx + i * sw, by - (i + 1) * sh, bx + (i + 1) * sw, by, (34, 34, 34), MARFIL, 5, 12, TAUPE)
            c.rect(bx + i * sw, by - (i + 1) * sh, bx + (i + 1) * sw, by - (i + 1) * sh + 10, fill=TAUPE)
        k = min(n - 1, int(max(0, t - 27.45) / 0.33))
        pose = 'walk' if int((t - 27.45) / 0.165) % 2 == 0 else 'walk2'
        sprite(c, R('persona', 160, c, pose), bx + k * sw + sw / 2, by - (k + 1) * sh + 4, 'mb', (8, 0, SHADOW_D))
        return
    # cierre
    hblock(c, ['Atrévete a', 'dar ese paso.'], SY0 + 20, True, align='m')
    lh = logo(c, W / 2, 690, 620, WHITE)
    c.text(W / 2, 690 + lh / 2 + 56, 'NOSOTROS TE ACOMPAÑAMOS.', font('inter', 'SemiBold', 30, c.S), WHITE, anchor='mm', tracking=6)
    if t >= 29.3:
        ph = int((t - 29.3) / 0.25) % 2
        sprite(c, R('persona', 120, c, 'walk' if ph else 'walk2'), W / 2 - 60, 1150, 'mb', (8, 0, SHADOW_D))
        sprite(c, R('persona', 120, c, 'walk2' if ph else 'walk', shirt='#FF6A00'), W / 2 + 60, 1150, 'mb', (8, 0, SHADOW_D))
    if t >= 30.2:
        fr = font('inter', 'Regular', 32, c.S); fb = font('inter', 'Bold', 32, c.S)
        parts = [('Escríbenos ', fr, CARBON), ('IMPULSO', fb, NARANJA), (' en los comentarios', fr, CARBON)]
        tw = sum(c.tw(s, ff) for s, ff, _ in parts)
        by0 = 1200
        brut_rect(c, W / 2 - tw / 2 - 30, by0, W / 2 + tw / 2 + 30, by0 + 86, MARFIL, CARBON, 6, 12, NARANJA)
        x = W / 2 - tw / 2
        for s, ff, col in parts:
            c.text(x, by0 + 43, s, ff, col, anchor='lm'); x += c.tw(s, ff)

# ================= MASTER =================
def frame(t, S=1, safe_overlay=False):
    if t < 3: bg, fn = CARBON, s1
    elif t < 7: bg, fn = CARBON, s2
    elif t < 10: bg, fn = CARBON, s3
    elif t < 11.5: bg, fn = MARFIL, s4a
    elif t < 15: bg, fn = CARBON, s4b
    elif t < 19: bg, fn = MARFIL, s5
    elif t < 26: bg, fn = MARFIL, s6
    else: bg, fn = CARBON, s7
    c = Ctx(S, bg)
    dark = bg == CARBON
    grid_bg(c, dark)
    fn(c, t)
    if 9.45 <= t < 10.0: halftone(c, (t - 9.45) / 0.55, NARANJA)
    if 10.0 <= t < 10.3: halftone(c, 1 - (t - 10.0) / 0.3, NARANJA)
    cropmarks(c, GRAY_D if dark else GRAY_L)
    subtitle(c, t, dark)
    im = c.out()
    if safe_overlay:
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        sh = (255, 0, 80, 70)
        d.rectangle([0, 0, W, SY0], fill=sh); d.rectangle([0, SY1, W, H], fill=sh)
        d.rectangle([0, SY0, SX0, SY1], fill=sh); d.rectangle([SX1, SY0, W, SY1], fill=sh)
        for k in range(0, W, 24): d.line([(k, SY0), (k + 12, SY0)], fill=(255, 0, 80, 255), width=3); d.line([(k, SY1), (k + 12, SY1)], fill=(255, 0, 80, 255), width=3)
        for k in range(SY0, SY1, 24): d.line([(SX0, k), (SX0, k + 12)], fill=(255, 0, 80, 255), width=3); d.line([(SX1, k), (SX1, k + 12)], fill=(255, 0, 80, 255), width=3)
        im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    return im

if __name__ == '__main__':
    import sys
    ov = '--safe' in sys.argv
    for a in sys.argv[1:]:
        if a.startswith('--'): continue
        t = float(a)
        frame(t, 2, ov).save(f'/home/claude/kf4_{t:05.2f}{"_safe" if ov else ""}.png')
