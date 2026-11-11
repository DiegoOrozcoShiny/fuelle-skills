import math, random
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1080, 1920
CARBON = (15, 15, 15); MARFIL = (247, 243, 234); TAUPE = (201, 183, 167)
NARANJA = (255, 106, 0); AZUL = (42, 91, 255); WHITE = (247, 243, 234)
GRAY_D = (138, 138, 138); GRAY_L = (107, 107, 107)
FPS = 30
ML = 80  # margen izquierdo

SORA = '/home/claude/fonts/Sora.ttf'
INTER = {'Regular': '/usr/share/fonts/opentype/inter/Inter-Regular.otf',
         'Medium': '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
         'SemiBold': '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',
         'Bold': '/usr/share/fonts/opentype/inter/Inter-Bold.otf'}
_fc = {}

def font(kind, weight, size, S):
    key = (kind, weight, size, S)
    if key not in _fc:
        if kind == 'sora':
            f = ImageFont.truetype(SORA, int(size * S)); f.set_variation_by_name(weight)
        else:
            f = ImageFont.truetype(INTER[weight], int(size * S))
        _fc[key] = f
    return _fc[key]

# ---------- VO / subtítulos ----------
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

# ---------- helpers ----------
def snap(t, t0, frames=3):
    """0->1 en 'frames' cuadros (aparición casi instantánea)."""
    d = frames / FPS
    if t < t0: return 0.0
    if t >= t0 + d: return 1.0
    return (t - t0) / d

def ease_out(x): return 1 - (1 - x) ** 3
def clamp(x, a=0, b=1): return max(a, min(b, x))

class Ctx:
    def __init__(self, S, bg):
        self.S = S; self.bg = bg
        self.img = Image.new('RGB', (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.img)
    def p(self, v): return v * self.S
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=0):
        S = self.S
        self.d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=fill, outline=outline, width=int(width * S))
    def line(self, pts, fill, width):
        S = self.S
        self.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S), joint='curve')
    def poly(self, pts, fill):
        S = self.S
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)
    def ellipse(self, x0, y0, x1, y1, fill=None, outline=None, width=0):
        S = self.S
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline, width=int(width * S))
    def text(self, x, y, s, f, fill, anchor='la', tracking=0):
        S = self.S
        if tracking == 0:
            self.d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor); return
        # tracking manual
        total = self.tw(s, f, tracking)
        if anchor[0] == 'm': x -= total / 2
        elif anchor[0] == 'r': x -= total
        cx = x
        for ch in s:
            self.d.text((cx * S, y * S), ch, font=f, fill=fill, anchor='l' + anchor[1])
            cx += f.getlength(ch) / S + tracking
    def tw(self, s, f, tracking=0):
        return f.getlength(s) / self.S + tracking * max(0, len(s) - 1)
    def out(self):
        if self.S == 1: return self.img
        return self.img.resize((W, H), Image.LANCZOS)

def cropmarks(c, col):
    L, m, w = 30, 40, 2
    for (x, y, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        c.rect(min(x, x + dx * L), y if dy > 0 else y - w, max(x, x + dx * L), y + w if dy > 0 else y, fill=col)
        c.rect(x if dx > 0 else x - w, min(y, y + dy * L), x + w if dx > 0 else x, max(y, y + dy * L), fill=col)

def counter(c, x, y, label, value, col, dark=True):
    c.text(x, y, label, font('inter', 'Medium', 26, c.S), GRAY_D if dark else GRAY_L)
    c.text(x, y + 36, value, font('sora', 'Bold', 110, c.S), col)

def headline(c, lines, y=360, size=72, align='l'):
    """lines: lista de (texto, color). Ajusta tamaño para caber en 920 px."""
    f = font('sora', 'ExtraBold', size, c.S)
    mx = max(c.tw(s, f) for s, _ in lines if s)
    while mx > W - 2 * ML and size > 48:
        size -= 2; f = font('sora', 'ExtraBold', size, c.S); mx = max(c.tw(s, f) for s, _ in lines if s)
    lh = size * 1.12
    for i, (s, col) in enumerate(lines):
        if s is None: continue
        if align == 'l': c.text(ML, y + i * lh, s, f, col)
        else: c.text(W / 2, y + i * lh, s, f, col, anchor='ma')
    return y + len(lines) * lh

def subtitle(c, t, dark=True):
    cur = None
    for a, b, s in VO:
        if a <= t < b: cur = s
    if not cur: return
    f = font('inter', 'Medium', 30, c.S)
    tw = c.tw(cur, f)
    maxw = W - 2 * ML - 48
    lines = [cur]
    if tw > maxw:  # partir en 2 líneas
        words = cur.split(); best = None
        for i in range(1, len(words)):
            a, b = ' '.join(words[:i]), ' '.join(words[i:])
            m = max(c.tw(a, f), c.tw(b, f))
            if best is None or m < best[0]: best = (m, [a, b])
        lines = best[1]
    w = max(c.tw(l, f) for l in lines) + 48
    lh = 40; h = lh * len(lines) + 28
    yb = H - 160; y0 = yb - h
    fill = (0, 0, 0) if dark else CARBON
    c.rect(W / 2 - w / 2, y0, W / 2 + w / 2, yb, fill=fill, outline=(48, 48, 48) if dark else None, width=2 if dark else 0)
    for i, l in enumerate(lines):
        c.text(W / 2, y0 + 14 + i * lh + lh / 2, l, f, WHITE, anchor='mm')

def halftone(c, prog, col, reverse=False):
    """Barrido de semitono diagonal (abajo-izq -> arriba-der). prog 0..1 cubre la pantalla."""
    step = 54
    for gy in range(-1, H // step + 2):
        for gx in range(-1, W // step + 2):
            x = gx * step + (step / 2 if gy % 2 else 0); y = gy * step
            pos = (x + (H - y)) / (W + H)  # 0 en abajo-izq
            local = clamp((prog * 1.6 - pos * 0.6) / 1.0 * 1.0)
            if reverse: local = 1 - clamp(((1 - prog) * 1.6 - (1 - pos) * 0.6))
            r = local * step * 0.82
            if r > 0.5: c.ellipse(x - r, y - r, x + r, y + r, fill=col)

def checkmark(c, x, y, s, col, w=10):
    c.line([(x, y + s * 0.5), (x + s * 0.38, y + s * 0.88), (x + s, y)], col, w)

def arrow(c, x0, y0, x1, y1, col, w, head=70):
    ang = math.atan2(y1 - y0, x1 - x0)
    c.line([(x0, y0), (x1 - math.cos(ang) * w * 0.5, y1 - math.sin(ang) * w * 0.5)], col, w)
    # cabeza en L (dos brazos rectos)
    for da in (math.pi * 0.75, -math.pi * 0.75):
        hx = x1 + math.cos(ang + da) * head; hy = y1 + math.sin(ang + da) * head
        c.line([(x1, y1), (hx, hy)], col, w)
    c.rect(x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2, fill=col)

_logo = None
def logo(c, cx, cy, width, col):
    global _logo
    if _logo is None:
        im = Image.open('/mnt/project/FUELLE_PNG.png').convert('L')
        _logo = ImageChops.invert(im)  # alpha: negro->opaco
    lw = int(width * c.S); lh = int(_logo.height * lw / _logo.width)
    a = _logo.resize((lw, lh), Image.LANCZOS)
    solid = Image.new('RGB', (lw, lh), col)
    c.img.paste(solid, (int(cx * c.S - lw / 2), int(cy * c.S - lh / 2)), a)
    return lh / c.S

# ================= ESCENAS =================
def scene1(c, t):
    # Ventas: la línea intenta subir 3 veces y cae
    attempts = [(0.35, 230), (1.15, 340), (1.95, 450)]
    x0, x1, yb = ML, W - ML, 1380
    xk = 560
    h = 0; done = []
    for (ta, peak) in attempts:
        up, hold, fall = 0.20, 0.12, 0.10
        if t >= ta:
            dt = t - ta
            if dt < up: h = peak * ease_out(dt / up)
            elif dt < up + hold: h = peak
            elif dt < up + hold + fall: h = peak * (1 - ((dt - up - hold) / fall) ** 2)
            elif dt < up + hold + fall + 0.08: h = -18 * math.sin((dt - up - hold - fall) / 0.08 * math.pi)  # rebote seco
            else: h = 0; done.append(peak)
    ventas = 120 + int(h / 450 * 28)
    counter(c, ML, 150, 'Ventas', f'{ventas}', WHITE)
    if t >= 0.1: headline(c, [('Por más que', WHITE), ('lo intentas...', NARANJA)], y=380)
    # eje
    c.rect(x0, yb + 40, x1, yb + 42, fill=(60, 60, 60))
    # marcas de intentos fallidos
    for i, pk in enumerate(done):
        c.rect(x1 - 8, yb - pk, x1, yb - pk + 4, fill=TAUPE)
        c.text(x1 - 16, yb - pk, f'INTENTO {i+1}', font('inter', 'Medium', 24, c.S), GRAY_D, anchor='rm', tracking=2)
    c.line([(x0, yb), (xk, yb), (x1, yb - h)], WHITE, 6)

def basket(c):
    bx0, bx1, by0, by1 = 220, 940, 1200, 1460
    # tiras horizontales de tejido
    for i in range(5):
        y = by0 + 20 + i * 48
        c.rect(bx0 + 6, y, bx1 - 6, y + 26, fill=(70, 64, 58))
    c.rect(bx0, by0, bx1, by1, outline=TAUPE, width=6)
    c.rect(bx0 - 24, by0 - 6, bx1 + 24, by0 + 18, fill=TAUPE)  # borde superior
    c.rect(ML, by1, W - ML, by1 + 3, fill=(60, 60, 60))

EGGS = [(3.10, 'AGENCIAS', 350), (3.85, 'INFLUENCERS', 580), (4.75, 'CURSOS', 810), (5.85, 'META ADS', 580)]
def egg(c, cx, cy, label, sq=0):
    """Pelota de golf: círculo marfil, hoyuelos taupe en retícula hexagonal, etiqueta al centro."""
    r = 112
    rx, ry = r * (1 + sq), r * (1 - sq)
    c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, fill=WHITE, outline=CARBON, width=6)
    # hoyuelos (solo dentro del círculo, dejando libre la franja de la etiqueta)
    step = 26
    for gy in range(-5, 6):
        for gx in range(-5, 6):
            dx = gx * step + (step / 2 if gy % 2 else 0); dy = gy * step * 0.88
            if (dx / rx) ** 2 + (dy / ry) ** 2 > 0.78: continue
            if abs(dy) < 26: continue
            k = 1 - 0.45 * ((dx * dx + dy * dy) / (r * r))  # más chicos hacia el borde
            d = 5.5 * k
            c.ellipse(cx + dx - d, cy + dy - d * (1 - sq), cx + dx + d, cy + dy + d * (1 - sq), fill=TAUPE)
    f = font('inter', 'Bold', 24, c.S)
    c.text(cx, cy, label, f, CARBON, anchor='mm', tracking=0)

def scene2(c, t):
    land = [(ta + 0.22) for ta, _, _ in EGGS]
    n = sum(1 for l in land if t >= l)
    counter(c, ML, 150, 'Intentos', str(n), WHITE)
    counter(c, 560, 150, 'Ventas nuevas', '0', NARANJA)
    headline(c, [('Lo intentaste todo.', WHITE)], y=380)
    rest = {350: 1150, 580: 1150, 810: 1150}
    for i, (ta, lab, cx) in enumerate(EGGS):
        if t < ta: continue
        ty = rest[cx] if i < 3 else 950
        dt = t - ta
        if dt < 0.22:
            y = 560 + (ty - 560) * (dt / 0.22) ** 2; sq = 0
        elif dt < 0.22 + 0.16:  # rebote corto y seco
            u = (dt - 0.22) / 0.16
            y = ty - 55 * math.sin(u * math.pi); sq = 0.10 if dt < 0.22 + 2 / FPS else 0
        else:
            y = ty; sq = 0
        # los huevos quedan detrás del frente de la canasta
        egg(c, cx, y, lab, sq)
    basket(c)

def chart_axes(c, x0, y0, x1, y1, col):
    c.rect(x0, y1, x1, y1 + 3, fill=col)
    for i in range(1, 5):
        yy = y1 - (y1 - y0) * i / 4
        c.rect(x0, yy, x1, yy + 1, fill=col)

def hatch(c, poly_top, poly_bot, col, step=22, w=3):
    # rayado diagonal entre dos curvas (muestreado por columnas)
    mask = Image.new('L', c.img.size, 0); md = ImageDraw.Draw(mask)
    S = c.S
    pts = [(x * S, y * S) for x, y in poly_top] + [(x * S, y * S) for x, y in reversed(poly_bot)]
    if len(pts) >= 3: md.polygon(pts, fill=255)
    lay = Image.new('RGB', c.img.size, col)
    hm = Image.new('L', c.img.size, 0); hd = ImageDraw.Draw(hm)
    for k in range(-H, W + H, step):
        hd.line([(k * S, H * S), ((k + H) * S, 0)], fill=255, width=w * S)
    c.img.paste(lay, (0, 0), ImageChops.multiply(mask, hm))

def gasto_curve(u):  # exponencial creciente 0..1
    return (math.exp(3.2 * u) - 1) / (math.exp(3.2) - 1)

def scene3(c, t):
    headline(c, [('El gasto sube.', WHITE), ('Tus ventas, no.' if t >= 8.4 else None, NARANJA)], y=200)
    x0, x1, y0, y1 = ML, W - ML - 10, 560, 1420
    chart_axes(c, x0, y0, x1, y1, (45, 45, 45))
    prog = clamp((t - 7.15) / 1.4)
    N = 60; n = max(2, int(N * prog))
    gp = [(x0 + (x1 - x0) * i / N, y1 - 30 - (y1 - y0 - 80) * gasto_curve(i / N)) for i in range(n + 1)]
    vp = [(x0 + (x1 - x0) * i / N, y1 - 120 + 3 * math.sin(i * 0.9)) for i in range(n + 1)]
    if prog > 0.05:
        hatch(c, gp, vp, (110, 54, 14))
        c.line(vp, TAUPE, 6); c.line(gp, NARANJA, 8)
        f = font('inter', 'SemiBold', 24, c.S)
        ex, ey = gp[-1]
        c.text(min(ex, x1) - 10, ey - 30, 'GASTO EN MARKETING', f, NARANJA, anchor='rb', tracking=3)
        vx, vy = vp[-1]
        c.text(vx - 10, vy + 24, 'VENTAS', f, TAUPE, anchor='rt', tracking=3)

def scene4a(c, t):
    f = font('sora', 'ExtraBold', 76, c.S)
    c.text(W / 2, H / 2 - 50, 'El problema', f, CARBON, anchor='mm')
    c.text(W / 2, H / 2 + 40, 'no eres tú.', f, CARBON, anchor='mm')

def ad_card(c, x, y, w, h, seed):
    r = random.Random(seed)
    c.rect(x, y, x + w, y + h, fill=(28, 28, 28), outline=(55, 55, 55), width=4)
    c.rect(x + 14, y + 14, x + w - 14, y + h * 0.56, fill=(58, 53, 48))
    c.rect(x + 14, y + h * 0.56 + 16, x + 14 + (w - 28) * r.uniform(0.6, 0.95), y + h * 0.56 + 30, fill=(80, 80, 80))
    c.rect(x + 14, y + h * 0.56 + 40, x + 14 + (w - 28) * r.uniform(0.3, 0.6), y + h * 0.56 + 52, fill=(65, 65, 65))
    c.rect(x + w - 14 - 70, y + h - 40, x + w - 14, y + h - 16, fill=(90, 90, 90))

def scene4b(c, t):
    cols, rows = 4, 9
    gx, gy = 30, 20; cw = (W - 2 * gx - (cols - 1) * 14) / cols; ch = (H - 2 * gy - (rows - 1) * 14) / rows
    order = list(range(cols * rows)); random.Random(7).shuffle(order)
    prog = clamp((t - 11.6) / 2.2)
    shown = int(len(order) * prog ** 0.8)
    for k in order[:shown]:
        i, j = k % cols, k // cols
        ad_card(c, gx + i * (cw + 14), gy + j * (ch + 14), cw, ch, k)
    # contador azul sobre bloque carbón
    cost = int(48 + 264 * prog ** 1.5)
    c.rect(ML - 30, 120, 640, 320, fill=CARBON)
    counter(c, ML, 150, 'Costo por cliente', f'${cost}', AZUL)
    # titular sobre bloque carbón
    c.rect(ML - 30, 340, ML + 820, 340 + 72 * 1.12 * 2 + 40, fill=CARBON)
    headline(c, [('Saturadas.', WHITE), ('Y cada vez más caras.' if t >= 13.2 else None, NARANJA)], y=360)

def scene5(c, t):
    headline(c, [('Las redes son', CARBON), ('solo un canal.', NARANJA)], y=200)
    bw, bh, g = 280, 220, 20
    cy = 1080
    shrink = clamp((t - 16.2) / (3 / FPS))
    # posición del bloque REDES (centro de la fila media)
    rx0, ry0 = W / 2 - bw / 2, cy - bh / 2
    if shrink < 1:
        # feed 3x3 que se encoge
        big = 820; s = big + (bw - big) * shrink
        fx0, fy0 = W / 2 - s / 2, cy - s / 2 * (1 if shrink == 0 else bh / bw)
        cell = (s - 2 * 10) / 3
        for i in range(3):
            for j in range(3):
                c.rect(fx0 + i * (cell + 10), cy - s / 2 + j * (cell + 10), fx0 + i * (cell + 10) + cell, cy - s / 2 + j * (cell + 10) + cell, fill=CARBON)
        return
    c.rect(rx0, ry0, rx0 + bw, ry0 + bh, fill=CARBON)
    cell = 34
    for i in range(3):
        for j in range(3):
            c.rect(rx0 + 30 + i * 40, ry0 + 30 + j * 40, rx0 + 30 + i * 40 + cell, ry0 + 30 + j * 40 + cell, fill=(70, 70, 70))
    c.text(rx0 + 24, ry0 + bh - 26, 'REDES', font('inter', 'SemiBold', 26, c.S), WHITE, anchor='ls', tracking=3)
    others = [('REFERIDOS', -0.5, -1), ('ALIANZAS', 0.5, -1), ('EVENTOS', -1, 0), ('EMAIL', 1, 0),
              ('PUNTO DE\nVENTA', -0.5, 1), ('B2B', 0.5, 1)]
    for k, (lab, dx, dy) in enumerate(others):
        ta = 16.6 + k * 0.33
        if t < ta: continue
        sc = 0.85 + 0.15 * snap(t, ta, 2)
        x = W / 2 + dx * (bw + g) - bw / 2 * sc; y = cy + dy * (bh + g) - bh / 2 * sc
        c.rect(x, y, x + bw * sc, y + bh * sc, fill=MARFIL, outline=CARBON, width=5)
        f = font('inter', 'SemiBold', 26, c.S)
        ls = lab.split('\n')
        for li, l in enumerate(ls):
            c.text(x + 24, y + bh * sc - 26 - (len(ls) - 1 - li) * 34, l, f, CARBON, anchor='ls', tracking=3)
        c.rect(x + 24, y + 24, x + 60, y + 30, fill=CARBON)

BARS = [(22.05, 'AUTOMATIZA\nTUS REDES', 360), (22.65, 'APRENDE DE\nTU NEGOCIO', 470), (23.25, 'AHORRA\nGASTOS', 580), (23.75, 'MIDE\nTU ROI', 690)]
def scene6(c, t):
    headline(c, [('En Fuelle construimos contigo', CARBON), ('tu infraestructura.' if t >= 20.6 else None, NARANJA)], y=200)
    if t < 24.2:
        x0, yb = ML, 1500; bw, g = 200, 40
        c.rect(ML, yb, W - ML, yb + 3, fill=TAUPE)
        for i, (ta, lab, hgt) in enumerate(BARS):
            # andamiaje taupe (inactivo) que aparece por golpe y luego se rellena
            tg = 19.5 + i * 0.5
            if tg <= t < ta:
                x = x0 + i * (bw + g)
                c.rect(x, yb - hgt, x + bw, yb, outline=TAUPE, width=5)
            if t < ta: continue
            s = snap(t, ta, 2)
            hh = hgt * (0.7 + 0.3 * s)
            x = x0 + i * (bw + g)
            c.rect(x, yb - hh, x + bw, yb, fill=CARBON)
            f = font('inter', 'SemiBold', 24, c.S)
            for li, l in enumerate(lab.split('\n')):
                c.text(x + 18, yb - hh + 26 + li * 32, l, f, WHITE, tracking=1)
            if t >= ta + 0.17:
                checkmark(c, x + bw / 2 - 30, yb - hh - 80, 60, NARANJA, 11)
        return
    # (b) gráfica invertida con cruce
    x0, x1, y0, y1 = ML, W - ML - 10, 560, 1420
    chart_axes(c, x0, y0, x1, y1, (222, 214, 200))
    prog = clamp((t - 24.25) / 1.0)
    N = 60; n = max(2, int(N * prog))
    gasto = lambda u: y1 - 120 - (y1 - y0 - 220) * (1 - u) ** 1.6
    ventas = lambda u: y1 - 140 - (y1 - y0 - 220) * u ** 1.4
    gp = [(x0 + (x1 - x0) * i / N, gasto(i / N)) for i in range(n + 1)]
    vp = [(x0 + (x1 - x0) * i / N, ventas(i / N)) for i in range(n + 1)]
    c.line(gp, NARANJA, 8); c.line(vp, CARBON, 8)
    f = font('inter', 'SemiBold', 24, c.S)
    c.text(x0 + 6, gasto(0) - 22, 'GASTO EN MARKETING', f, NARANJA, tracking=3, anchor='ls')
    if prog > 0.8:
        c.text(vp[-1][0] - 8, vp[-1][1] - 26, 'VENTAS', f, CARBON, anchor='rs', tracking=3)
    # cruce
    us = [i / 400 for i in range(401)]
    uc = min(us, key=lambda u: abs(gasto(u) - ventas(u)))
    xc, yc = x0 + (x1 - x0) * uc, gasto(uc)
    tc = 24.25 + 1.0 * uc
    if t >= tc:
        dt = t - tc
        for k in range(2):
            ph = ((dt + k * 0.45) % 0.9) / 0.9
            r = 18 + 70 * ph
            col = tuple(int(NARANJA[i] * (1 - ph) + MARFIL[i] * ph) for i in range(3))
            c.rect(xc - r, yc - r, xc + r, yc + r, outline=col, width=4)
        c.rect(xc - 16, yc - 16, xc + 16, yc + 16, fill=NARANJA)
        # etiqueta tipo "Meta" de la referencia
        lf = font('inter', 'SemiBold', 26, c.S)
        lab = 'RETORNO ↗'
        tw = c.tw(lab, lf, 3)
        c.rect(xc - tw / 2 - 18, yc - 150, xc + tw / 2 + 18, yc - 98, fill=CARBON)
        c.text(xc, yc - 124, lab, lf, WHITE, anchor='mm', tracking=3)
        c.rect(xc - 2, yc - 98, xc + 2, yc - 20, fill=CARBON)

def scene7(c, t):
    big = font('sora', 'ExtraBold', 104, c.S)
    if t < 27.4:
        c.text(ML, 720, 'DEJA DE', big, WHITE)
        c.text(ML, 836, 'REGALAR', big, WHITE)
        c.text(ML, 952, 'TU DINERO.', big, WHITE)
        return
    if t < 28.9:
        c.text(ML, 420, 'ATRÉVETE', big, WHITE)
        c.text(ML, 536, 'A DAR ESE', big, WHITE)
        c.text(ML, 652, 'PASO.', big, NARANJA if False else WHITE)
        g = clamp((t - 27.5) / 0.6)
        g = math.floor(g * 6) / 6  # crecimiento por pasos (brutalista)
        if g > 0:
            sx, sy = 70, 1650; ex, ey = sx + 760 * g, sy - 760 * g
            arrow(c, sx, sy, ex, ey, NARANJA, 44, head=90 + 60 * g)
        return
    lh = logo(c, W / 2, 760, 820, WHITE)
    c.text(W / 2, 760 + lh / 2 + 70, 'NOSOTROS TE ACOMPAÑAMOS.', font('inter', 'Medium', 30, c.S), WHITE, anchor='mm', tracking=6)
    if t >= 29.6:
        c.text(W / 2, 1090, '1 PAGO · SI NO HAY RESULTADOS,', font('inter', 'Regular', 24, c.S), GRAY_D, anchor='mm', tracking=3)
        c.text(W / 2, 1126, 'TE DEVOLVEMOS TU DINERO', font('inter', 'Regular', 24, c.S), GRAY_D, anchor='mm', tracking=3)
    if t >= 30.2:
        fr = font('inter', 'Regular', 32, c.S); fb = font('inter', 'Bold', 32, c.S)
        parts = [('Escríbenos ', fr, WHITE), ('IMPULSO', fb, NARANJA), (' en los comentarios', fr, WHITE)]
        tw = sum(c.tw(s, f) for s, f, _ in parts)
        bx0 = W / 2 - tw / 2 - 34; by0 = 1230
        c.rect(bx0, by0, W / 2 + tw / 2 + 34, by0 + 90, outline=WHITE, width=2)
        x = W / 2 - tw / 2
        for s, f, col in parts:
            c.text(x, by0 + 45, s, f, col, anchor='lm'); x += c.tw(s, f)
        ax = W / 2 + tw / 2 + 34 + 30

# ================= MASTER =================
def frame(t, S=1):
    if t < 3: bg, fn = CARBON, scene1
    elif t < 7: bg, fn = CARBON, scene2
    elif t < 10: bg, fn = CARBON, scene3
    elif t < 11.5: bg, fn = MARFIL, scene4a
    elif t < 15: bg, fn = CARBON, scene4b
    elif t < 19: bg, fn = MARFIL, scene5
    elif t < 26: bg, fn = MARFIL, scene6
    else: bg, fn = CARBON, scene7
    c = Ctx(S, bg)
    fn(c, t)
    dark = bg == CARBON
    # transición semitono 9.45-10.0 (entrada) y 10.0-10.3 (salida sobre Marfil)
    if 9.45 <= t < 10.0: halftone(c, (t - 9.45) / 0.55, NARANJA)
    if 10.0 <= t < 10.3: halftone(c, 1 - (t - 10.0) / 0.3, NARANJA)
    cropmarks(c, GRAY_D if dark else GRAY_L)
    subtitle(c, t, dark)
    return c.out()

if __name__ == '__main__':
    import sys
    for t in map(float, sys.argv[1:]):
        frame(t, 2).save(f'/home/claude/kf_{t:05.2f}.png')
