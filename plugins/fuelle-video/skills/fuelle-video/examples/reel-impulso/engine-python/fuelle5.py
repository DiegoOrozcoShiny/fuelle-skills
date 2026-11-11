import math, random
from PIL import Image, ImageDraw
import fuelle as F
import fuelle4 as V
from fuelle import (W, H, CARBON, MARFIL, TAUPE, NARANJA, AZUL, WHITE, GRAY_D, GRAY_L, FPS,
                    Ctx, font, snap, clamp, ease_out, cropmarks, halftone, checkmark, arrow, logo, gasto_curve)
from fuelle4 import (SX0, SX1, SY0, SY1, SHADOW_D, sprite, R, brut_rect, counter, subtitle, panel, BALLS)
import texture

COMPRESS = 0.80          # Sora comprimida horizontalmente para el efecto póster
CONCRETE = (118, 113, 108)

# ---------------- tipografía gigante ----------------
def giant(c, lines, y, dark, align='l', accent=None, maxsize=330, lh=0.86, fit=SX1 - SX0):
    """Palabras gigantes tipo póster brutalista. accent = índice de línea en naranja (por defecto la última)."""
    if accent is None: accent = len(lines) - 1
    S = c.S
    size = maxsize
    probe = font('sora', 'ExtraBold', 100, S)
    for s in lines:
        size = min(size, fit / (probe.getlength(s) / S * COMPRESS) * 100 * 0.995)
    size = int(size)
    f = font('sora', 'ExtraBold', size, S)
    col = MARFIL if dark else CARBON
    yy = y
    for i, s in enumerate(lines):
        tw = int(f.getlength(s)) + 4 * S
        asc, desc = f.getmetrics()
        layer = Image.new('L', (tw, asc + desc), 0)
        ImageDraw.Draw(layer).text((0, 0), s, font=f, fill=255)
        bbox = layer.getbbox()
        layer = layer.crop((0, bbox[1], tw, bbox[3]))
        nw = int(layer.width * COMPRESS)
        layer = layer.resize((nw, layer.height), Image.LANCZOS)
        x = SX0 if align == 'l' else (W * S - nw) / S / 2
        if align == 'm': x = (W - nw / S) / 2
        solid = Image.new('RGB', layer.size, NARANJA if i == accent else col)
        c.img.paste(solid, (int(x * S), int(yy * S)), layer)
        yy += size * lh
    return yy - size * lh + (layer.height / S)

def rule(c, y, left, right, dark):
    col = GRAY_D if dark else CARBON
    c.rect(SX0, y, SX1, y + 3, fill=col)
    f = font('inter', 'SemiBold', 24, c.S)
    c.text(SX0, y + 14, left, f, col, tracking=3)
    c.text(SX1, y + 14, right, f, col, anchor='ra', tracking=3)

def concrete_block(c, x0, y0, x1, y1, shcol=CARBON, sh=12, border=CARBON, seed=9, tone=CONCRETE):
    if sh: c.rect(x0 + sh, y0 + sh, x1 + sh, y1 + sh, fill=shcol)
    tex = texture.concrete(max(1, x1 - x0), max(1, y1 - y0), c.S, tone, seed)
    c.img.paste(tex, (int(x0 * c.S), int(y0 * c.S)))
    c.rect(x0, y0, x1, y1, outline=border, width=6)

# ================= ESCENAS =================
def s1(c, t):
    attempts = [(0.35, 170), (1.15, 240), (1.95, 300)]
    x0, xk, x1, yb = 110, 430, 770, 1280
    h = 0; done = []; rising = False
    for (ta, peak) in attempts:
        if t >= ta:
            dt = t - ta; up, hold, fall = 0.22, 0.12, 0.12
            if dt < up: h = peak * ease_out(dt / up); rising = True
            elif dt < up + hold: h = peak; rising = True
            elif dt < up + hold + fall: h = peak * (1 - ((dt - up - hold) / fall) ** 2); rising = False
            elif dt < up + hold + fall + 0.08: h = -14 * math.sin((dt - up - hold - fall) / 0.08 * math.pi); rising = False
            else: h = 0; done.append(peak); rising = False
    counter(c, SX0, SY0 + 10, 'Ventas', f'{120 + int(h / 300 * 28)}', WHITE)
    yb_g = giant(c, ['NO', 'SUBEN.'], 470, True, maxsize=230)
    rule(c, yb_g + 24, 'FUELLE STUDIO', '01 / 07', True)
    panel(c, SX0, 930, SX1, 1330, True)
    for pk in done:
        y = yb - pk
        c.line([(x1 + 76, y - 14), (x1 + 104, y + 14)], TAUPE, 6); c.line([(x1 + 76, y + 14), (x1 + 104, y - 14)], TAUPE, 6)
    c.line([(x0, yb), (xk, yb), (x1, yb - h)], WHITE, 8)
    ang = math.degrees(math.atan2(h, x1 - xk)); a = math.radians(ang)
    sprite(c, R('cohete', 70, c, h > 0 and rising), x1 + math.cos(a) * 72, yb - h - math.sin(a) * 72, 'mm', (8, 8, SHADOW_D), ang - 90)

def basket(c, y_top=1040):
    sprite(c, R('canasta', 720, c), (SX0 + SX1) / 2, y_top, 'mt', (14, 14, SHADOW_D))

def s2(c, t):
    n = sum(1 for ta, _, _ in BALLS if t >= ta + 0.22)
    counter(c, SX0, SY0 + 10, 'Intentos', str(n), WHITE)
    counter(c, 470, SY0 + 10, 'Ventas nuevas', '0', NARANJA)
    yb_g = giant(c, ['TODO.'], 470, True, accent=-1, maxsize=330)
    rule(c, yb_g + 20, 'LO INTENTASTE', '02 / 07', True)
    for i, (ta, ic, cx) in enumerate(BALLS):
        if t < ta: continue
        ty = 985 if i < 3 else 830
        dt = t - ta; sq = 0; rot = 0
        if dt < 0.22: y = 560 + (ty - 560) * (dt / 0.22) ** 2; rot = -dt * 400
        elif dt < 0.38: u = (dt - 0.22) / 0.16; y = ty - 50 * math.sin(u * math.pi); sq = 0.1 if dt < 0.22 + 2 / FPS else 0
        else: y = ty
        sprite(c, R('golf', 200, c, ic), cx, y, 'mm', (10, 10, SHADOW_D), rot, 1 + sq, 1 - sq)
    basket(c)

def s3(c, t):
    yb_g = giant(c, ['EL GASTO', 'SUBE.'], SY0 + 20, True, maxsize=230)
    rule(c, yb_g + 22, 'TUS VENTAS, NO.' if t >= 8.4 else '', '03 / 07', True)
    x0, x1, y0, y1 = SX0, SX1, 790, 1330
    panel(c, x0, y0, x1, y1, True)
    prog = clamp((t - 7.15) / 1.4); N = 60; n = max(2, int(N * prog))
    xa, xb = x0 + 20, x1 - 80
    gp = [(xa + (xb - xa) * i / N, y1 - 40 - (y1 - y0 - 170) * gasto_curve(i / N)) for i in range(n + 1)]
    vp = [(xa + (xb - xa) * i / N, y1 - 100 + 3 * math.sin(i * 0.9)) for i in range(n + 1)]
    if prog > 0.05:
        F.hatch(c, gp, vp, (110, 54, 14))
        c.line(vp, TAUPE, 8); c.line(gp, NARANJA, 10)
        ex, ey = gp[-1]
        sprite(c, R('bolsa', 100 + 30 * prog, c), ex, ey - 16, 'mb', (8, 8, SHADOW_D))

def s4a(c, t):
    giant(c, ['NO ERES', 'TÚ.'], SY0 + 20, False, maxsize=260)
    gy = 1330
    c.rect(SX0, gy, SX1, gy + 6, fill=CARBON)
    flipped = t >= 10.55
    # el personaje se para delante de las letras (capas, como edificio frente al título)
    sprite(c, R('persona', 340, c, 'stand' if flipped else 'sad'), 300, gy + 4, 'mb', (14, 0, TAUPE))
    hand = R('mano', 300, c)
    if not flipped:
        sprite(c, hand.transpose(Image.FLIP_LEFT_RIGHT), 700, 1000, 'mm', (12, 12, CARBON))
    else:
        k = snap(t, 10.55, 3)
        sprite(c, hand, 600 + 20 * (1 - k), 1000, 'mm', (12, 12, CARBON))
        brut_rect(c, 770, 900, 920, 1100, CARBON, CARBON, 0, 10, NARANJA)
        sprite(c, R('canal', 190, c, 'redes'), 845, 1000, 'mm')

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
    # bloque de concreto oscuro detrás de la palabra gigante
    brut_rect(c, SX0, 500, SX1, 900, CARBON, MARFIL, 4, 14, TAUPE)
    giant(c, ['SATU-', 'RADAS.'] if t >= 13.2 else ['SATU-', 'RADAS.'], 530, True, maxsize=200, fit=SX1 - SX0 - 60, accent=1 if t >= 13.2 else 5)

CH = V.CH
def s5(c, t):
    yb_g = giant(c, ['UN', 'CANAL.'], SY0 + 20, False, maxsize=165)
    rule(c, yb_g + 18, 'LAS REDES SON SOLO', '05 / 07', False)
    tw_, th_, g = 236, 206, 14
    cx0, cy0 = (SX0 + SX1) / 2, 992
    shrink = clamp((t - 16.2) / (3 / FPS))
    if shrink < 1:
        s = 660 + (tw_ - 660) * shrink; cell = (s - 24) / 3; fx0 = cx0 - s / 2; fy0 = cy0 - s / 2
        for i in range(3):
            for j in range(3):
                brut_rect(c, fx0 + i * (cell + 12), fy0 + j * (cell + 12), fx0 + i * (cell + 12) + cell, fy0 + j * (cell + 12) + cell, CARBON, CARBON, 0, 10, TAUPE)
        return
    lf = font('inter', 'SemiBold', 24, c.S)
    def tile(cx, cy, kind, lab, dark, sc=1.0):
        w, h = tw_ * sc, th_ * sc; x0, y0 = cx - w / 2, cy - h / 2
        brut_rect(c, x0, y0, x0 + w, y0 + h, CARBON if dark else MARFIL, CARBON, 6, 12, NARANJA if dark else CARBON)
        sprite(c, R('canal', int(176 * sc), c, kind), cx, y0 + 8 * sc, 'mt')
        c.rect(x0, y0 + h - 44 * sc, x0 + w, y0 + h, fill=CARBON if not dark else MARFIL)
        c.text(cx, y0 + h - 22 * sc, lab, lf, MARFIL if not dark else CARBON, anchor='mm', tracking=4)
    tile(cx0, cy0, 'redes', 'REDES', True)
    for k, (lab, kind, dx, dy) in enumerate(CH):
        ta = 16.6 + k * 0.33
        if t < ta: continue
        sc = 0.85 + 0.15 * snap(t, ta, 2)
        tile(cx0 + dx * (tw_ + g), cy0 + dy * (th_ + g), kind, lab, False, sc)

BARS = [(22.05, 'REDES', 'auto', 300, 11), (22.65, 'APRENDE', 'aprende', 380, 12), (23.25, 'AHORRO', 'ahorro', 460, 13), (23.75, 'ROI', 'roi', 540, 14)]
def s6(c, t):
    if t < 24.2:
        yb_g = giant(c, ['INFRAES-', 'TRUCTURA.'], SY0 + 20, False, maxsize=200, accent=1 if t >= 20.6 else 5)
        rule(c, yb_g + 18, 'EN FUELLE CONSTRUIMOS CONTIGO', '06 / 07', False)
        yb = 1290; bw, g = 180, 40
        c.rect(SX0, yb, SX1, yb + 6, fill=CARBON)
        lf = font('inter', 'SemiBold', 24, c.S)
        for i, (ta, lab, ic, hgt, seed) in enumerate(BARS):
            x = SX0 + i * (bw + g)
            if 19.5 + i * 0.5 <= t < ta:
                for k in range(0, int(hgt), 24):
                    c.rect(x, yb - k - 12, x + 5, yb - k, fill=TAUPE); c.rect(x + bw - 5, yb - k - 12, x + bw, yb - k, fill=TAUPE)
                c.rect(x, yb - hgt, x + bw, yb - hgt + 5, fill=TAUPE)
            if t < ta: continue
            s = snap(t, ta, 2); hh = int(hgt * (0.7 + 0.3 * s))
            concrete_block(c, x, yb - hh, x + bw, yb, CARBON, 12, CARBON, seed)
            brut_rect(c, x + 14, yb - hh + 14, x + bw - 14, yb - hh + 166, CARBON, CARBON, 0, 0)
            sprite(c, R('barra_icon', 140, c, ic), x + bw / 2, yb - hh + 20, 'mt')
            c.text(x + bw / 2, yb + 30, lab, lf, CARBON, anchor='mm', tracking=3)
            if t >= ta + 0.17:
                cs = 60
                brut_rect(c, x + bw / 2 - cs / 2, yb - hh - cs - 20, x + bw / 2 + cs / 2, yb - hh - 20, NARANJA, CARBON, 5, 6, CARBON)
                checkmark(c, x + bw / 2 - 17, yb - hh - cs - 3, 34, CARBON, 8)
        return
    yb_g = giant(c, ['RETORNO.'], SY0 + 20, False, maxsize=200, accent=0)
    rule(c, yb_g + 18, 'DE CADA DECISIÓN', '06 / 07', False)
    x0, x1, y0, y1 = SX0, SX1, 560, 1330
    panel(c, x0, y0, x1, y1, False)
    prog = clamp((t - 24.25) / 1.0); N = 60; n = max(2, int(N * prog))
    xa, xb = x0 + 20, x1 - 60
    gasto = lambda u: y1 - 110 - (y1 - y0 - 240) * (1 - u) ** 1.6
    ventas = lambda u: y1 - 130 - (y1 - y0 - 240) * u ** 1.4
    gp = [(xa + (xb - xa) * i / N, gasto(i / N)) for i in range(n + 1)]
    vp = [(xa + (xb - xa) * i / N, ventas(i / N)) for i in range(n + 1)]
    c.line(gp, NARANJA, 10); c.line(vp, CARBON, 10)
    f = font('inter', 'SemiBold', 24, c.S)
    c.text(xa + 6, gasto(0) - 26, 'GASTO', f, NARANJA, tracking=3, anchor='ls')
    vx, vy = vp[-1]; px, py = vp[-2]
    sprite(c, R('cohete', 70, c, True), vx, vy - 30, 'mm', (8, 8, TAUPE), math.degrees(math.atan2(py - vy, vx - px)) - 90)
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

BILLS = V.BILLS
def s7(c, t):
    if t < 27.4:
        yb_g = giant(c, ['DEJA DE', 'REGALAR.'], SY0 + 20, True, maxsize=230)
        rule(c, yb_g + 18, 'TU DINERO', '07 / 07', True)
        for (ta, cx, r0) in BILLS:
            if t < ta: continue
            dt = min(t, 27.0) - ta
            y = 760 + min(1, dt / 0.35) ** 2 * (1010 - 760)
            sprite(c, R('billete', 210, c), cx, y, 'mm', (10, 10, SHADOW_D), r0 + dt * 60 * (1 if r0 > 0 else -1))
        basket(c)
        if t >= 27.0:
            k = snap(t, 27.0, 3)
            c.line([(SX0 + 10, 1340), (SX0 + 10 + (SX1 - SX0 - 20) * k, 1340 - 560 * k)], CARBON, 52)
            c.line([(SX0 + 10, 1340), (SX0 + 10 + (SX1 - SX0 - 20) * k, 1340 - 560 * k)], NARANJA, 34)
        return
    if t < 28.9:
        yb_g = giant(c, ['ATRÉVE-', 'TE.'], SY0 + 20, True, maxsize=240)
        rule(c, yb_g + 18, 'A DAR ESE PASO', '07 / 07', True)
        n = 4; sw = 190; sh = 110; bx = SX0 + 20; by = 1330
        g = clamp((t - 27.5) / 1.0); g = math.floor(g * 6) / 6
        if g > 0:
            arrow(c, SX0, 1320, SX0 + 760 * g, 1320 - 600 * g, NARANJA, 34, head=60 + 40 * g)
        for i in range(n):
            concrete_block(c, bx + i * sw, by - (i + 1) * sh, bx + (i + 1) * sw, by, SHADOW_D, 12, CARBON, 20 + i, (96, 92, 88))
        k = min(n - 1, int(max(0, t - 27.45) / 0.33))
        pose = 'walk' if int((t - 27.45) / 0.165) % 2 == 0 else 'walk2'
        sprite(c, R('persona', 140, c, pose), bx + k * sw + sw / 2, by - (k + 1) * sh + 4, 'mb', (8, 0, SHADOW_D))
        return
    # cierre
    yb_g = giant(c, ['ATRÉVETE A', 'DAR ESE PASO.'], SY0 + 20, True, align='m', maxsize=200)
    lh = logo(c, W / 2, yb_g + 160, 560, WHITE)
    ly = yb_g + 160 + lh / 2 + 52
    c.text(W / 2, ly, 'NOSOTROS TE ACOMPAÑAMOS.', font('inter', 'SemiBold', 30, c.S), WHITE, anchor='mm', tracking=6)
    if t >= 29.3:
        ph = int((t - 29.3) / 0.25) % 2
        sprite(c, R('persona', 110, c, 'walk' if ph else 'walk2'), W / 2 - 55, ly + 230, 'mb', (8, 0, SHADOW_D))
        sprite(c, R('persona', 110, c, 'walk2' if ph else 'walk', shirt='#FF6A00'), W / 2 + 55, ly + 230, 'mb', (8, 0, SHADOW_D))
    if t >= 30.2:
        fr = font('inter', 'Regular', 32, c.S); fb = font('inter', 'Bold', 32, c.S)
        parts = [('Escríbenos ', fr, CARBON), ('IMPULSO', fb, NARANJA), (' en los comentarios', fr, CARBON)]
        tw = sum(c.tw(s, ff) for s, ff, _ in parts)
        by0 = ly + 260
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
    dark = bg == CARBON
    c = Ctx(S, bg)
    c.img.paste(texture.background('dark' if dark else 'light', S), (0, 0))
    V.grid_bg(c, dark)
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
        im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    return im

if __name__ == '__main__':
    import sys
    ov = '--safe' in sys.argv
    for a in sys.argv[1:]:
        if a.startswith('--'): continue
        t = float(a)
        frame(t, 2, ov).save(f'/home/claude/kf5_{t:05.2f}{"_safe" if ov else ""}.png')
