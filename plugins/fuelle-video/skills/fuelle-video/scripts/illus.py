"""Ilustraciones vectoriales brutalistas para Fuelle (contorno grueso, rellenos planos, sombreado en semitono)."""
import math, io
import cairosvg
from PIL import Image

C = '#0F0F0F'; M = '#F7F3EA'; T = '#C9B7A7'; N = '#FF6A00'; A = '#2A5BFF'
TD = '#8E7D6E'; TL = '#E4DACB'; G2 = '#2B2B2B'; G3 = '#3A3A3A'; G5 = '#5A5A5A'; SK = '#D9B79A'

def defs(extra=''):
    return f'''<defs>
<pattern id="ht" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.4" fill="{TD}"/></pattern>
<pattern id="htc" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="2.1" fill="{C}"/></pattern>
<pattern id="htm" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="2.0" fill="{M}"/></pattern>
<pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="12" fill="{C}"/></pattern>
{extra}</defs>'''

def svg(w, h, body, extra_defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{defs(extra_defs)}{body}</svg>'

_cache = {}
def render(name, width, *args, **kw):
    key = (name, int(width), args, tuple(sorted(kw.items())))
    if key in _cache: return _cache[key]
    s = ASSETS[name](*args, **kw)
    png = cairosvg.svg2png(bytestring=s.encode(), output_width=int(width))
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    _cache[key] = im
    return im

def P(pts): return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)

def gear_path(cx, cy, r, teeth=10, depth=0.22, rot=0):
    pts = []
    for i in range(teeth * 4):
        a = rot + i / (teeth * 4) * 2 * math.pi
        rr = r if (i % 4) in (0, 1) else r * (1 - depth)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return P(pts)

# ------------------------------------------------------------------ PELOTA DE GOLF
def golf(icon='agencias'):
    dim = []
    for gy in range(-9, 10):
        for gx in range(-9, 10):
            x = 120 + gx * 17 + (8.5 if gy % 2 else 0); y = 120 + gy * 15
            d = math.hypot(x - 120, y - 120)
            if d > 100 or d < 66: continue
            s = 1 - (d / 112) ** 2 * 0.5
            dim.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6.2*s:.1f}" fill="{TL}"/><circle cx="{x+1.6:.1f}" cy="{y+1.6:.1f}" r="{4*s:.1f}" fill="{M}"/>')
    ic = BALL_ICONS[icon]()
    return svg(240, 240, f'''
<clipPath id="ball"><circle cx="120" cy="120" r="112"/></clipPath>
<circle cx="120" cy="120" r="112" fill="{M}"/>
{''.join(dim)}
<g clip-path="url(#ball)"><path fill-rule="evenodd" fill="url(#ht)" d="M0,0H240V240H0Z M-16,94 a112,112 0 1,0 224,0 a112,112 0 1,0 -224,0Z"/></g>
<circle cx="120" cy="120" r="112" fill="none" stroke="{C}" stroke-width="7"/>
<path d="M58,62 A84,84 0 0 1 104,38" fill="none" stroke="{M}" stroke-width="8"/>
<circle cx="120" cy="120" r="60" fill="{M}" stroke="{C}" stroke-width="6"/>
<circle cx="120" cy="120" r="51" fill="none" stroke="{C}" stroke-width="2" stroke-dasharray="4 5"/>
{ic}''')

def ic_agencias():
    return f'''<g stroke="{C}" stroke-width="4" stroke-linejoin="miter">
<path d="M104,92 V82 H136 V92" fill="none" stroke-width="6"/>
<rect x="86" y="92" width="68" height="50" fill="{C}"/>
<rect x="86" y="92" width="68" height="16" fill="{G3}"/>
<rect x="113" y="102" width="14" height="12" fill="{T}"/>
<line x1="92" y1="132" x2="148" y2="132" stroke="{T}" stroke-width="2" stroke-dasharray="4 3"/>
<rect x="98" y="142" width="8" height="5" fill="{C}"/><rect x="134" y="142" width="8" height="5" fill="{C}"/>
</g>'''

def ic_influencers():
    return f'''<g stroke="{C}" stroke-width="4">
<circle cx="120" cy="116" r="40" fill="none" stroke="{T}" stroke-width="7" stroke-dasharray="7 4"/>
<rect x="100" y="82" width="40" height="72" fill="{C}"/>
<rect x="105" y="92" width="30" height="50" fill="{M}" stroke="none"/>
<rect x="115" y="86" width="10" height="3" fill="{M}" stroke="none"/>
<circle cx="120" cy="108" r="7" fill="{C}" stroke="none"/>
<path d="M108,128 Q120,112 132,128 Z" fill="{C}" stroke="none"/>
<path d="M131,99 l3,-3 3,3 -3,4 z" fill="{C}" stroke="none"/>
<path d="M140,96 c4,-6 12,-2 8,4 l-7,7 -7,-7 c-4,-6 4,-10 6,-4z" fill="{C}" stroke="{M}" stroke-width="2"/>
<rect x="105" y="136" width="30" height="4" fill="{T}" stroke="none"/>
</g>'''

def ic_cursos():
    return f'''<g stroke="{C}" stroke-width="4" stroke-linejoin="miter">
<rect x="88" y="100" width="64" height="40" fill="{C}"/>
<rect x="94" y="105" width="52" height="30" fill="{M}" stroke="none"/>
<polygon points="114,112 114,128 128,120" fill="{C}" stroke="none"/>
<polygon points="80,140 160,140 166,150 74,150" fill="{G3}"/>
<polygon points="120,72 154,84 120,96 86,84" fill="{C}"/>
<rect x="104" y="88" width="32" height="12" fill="{C}"/>
<line x1="150" y1="85" x2="150" y2="104" stroke="{T}" stroke-width="3"/><rect x="146" y="102" width="8" height="8" fill="{T}" stroke="none"/>
</g>'''

def ic_ads():
    return f'''<g stroke="{C}" stroke-width="4" stroke-linejoin="miter">
<polygon points="92,108 128,88 128,140 92,122" fill="{C}"/>
<rect x="80" y="104" width="14" height="22" fill="{G3}"/>
<rect x="128" y="84" width="8" height="60" fill="{C}"/>
<polygon points="96,124 108,128 104,148 94,148" fill="{G3}"/>
<path d="M144,100 q8,14 0,28" fill="none" stroke-width="5"/>
<path d="M152,92 q14,22 0,44" fill="none" stroke-width="5"/>
<circle cx="104" cy="84" r="11" fill="{T}"/><text x="104" y="89" font-family="Sora" font-weight="800" font-size="15" text-anchor="middle" fill="{C}" stroke="none">$</text>
</g>'''

BALL_ICONS = {'agencias': ic_agencias, 'influencers': ic_influencers, 'cursos': ic_cursos, 'ads': ic_ads}

# ------------------------------------------------------------------ CANASTA
def canasta():
    w, h = 760, 330
    rows = []
    for r in range(5):
        y = 62 + r * 50
        inset = 30 + (y - 40) * 40 / 290
        x0, x1 = inset, w - inset
        n = 12
        cw = (x1 - x0) / n
        for k in range(n):
            col = T if (k + r) % 2 == 0 else '#B19D8A'
            rows.append(f'<rect x="{x0+k*cw:.1f}" y="{y}" width="{cw:.1f}" height="40" fill="{col}" stroke="{C}" stroke-width="3"/>')
            rows.append(f'<line x1="{x0+k*cw+6:.1f}" y1="{y+12}" x2="{x0+(k+1)*cw-6:.1f}" y2="{y+12}" stroke="{TD}" stroke-width="2"/>')
    rope = ''.join(f'<line x1="{x}" y1="14" x2="{x+18}" y2="44" stroke="{TD}" stroke-width="4"/>' for x in range(16, w - 16, 16))
    return svg(w, h, f'''
<polygon points="30,40 730,40 690,322 70,322" fill="{TD}" stroke="{C}" stroke-width="7"/>
{''.join(rows)}
<polygon points="520,44 730,44 690,320 480,320" fill="url(#htc)" opacity="0.55"/>
<polygon points="30,40 730,40 690,322 70,322" fill="none" stroke="{C}" stroke-width="7"/>
<rect x="6" y="8" width="748" height="42" fill="{T}" stroke="{C}" stroke-width="7"/>{rope}
<rect x="6" y="8" width="748" height="42" fill="none" stroke="{C}" stroke-width="7"/>
<rect x="-2" y="70" width="34" height="70" fill="none" stroke="{C}" stroke-width="10"/>
<rect x="728" y="70" width="34" height="70" fill="none" stroke="{C}" stroke-width="10"/>''')

# ------------------------------------------------------------------ PERSONAJE
def persona(pose='stand', shirt=M, pants=G3, hair=C, skin=SK, la=0, ra=0, ll=0, rl=0, look=0):
    """Emprendedor brutalista. la/ra = ángulo brazos, ll/rl = ángulo piernas (grados)."""
    S = f'stroke="{C}" stroke-width="6" stroke-linejoin="miter"'
    if pose == 'walk': la, ra, ll, rl = 28, -28, -22, 22
    if pose == 'walk2': la, ra, ll, rl = -24, 24, 20, -20
    if pose == 'sad': la, ra = 6, -6
    if pose == 'climb': la, ra, ll, rl = 30, -20, -30, 5
    leg = lambda ang, x: f'''<g transform="rotate({ang} {x} 268)">
<polygon points="{x-26},262 {x+26},262 {x+22},420 {x-20},420" fill="{pants}" {S}/>
<line x1="{x}" y1="280" x2="{x}" y2="410" stroke="{G5}" stroke-width="2"/>
<polygon points="{x-26},418 {x+30},418 {x+40},446 {x-26},446" fill="{C}" {S}/>
<rect x="{x-26}" y="440" width="66" height="6" fill="{M}"/></g>'''
    arm = lambda ang, x, side: f'''<g transform="rotate({ang} {x} 150)">
<polygon points="{x-20},140 {x+20},140 {x+18},226 {x-16},226" fill="{shirt}" {S}/>
<rect x="{x-19}" y="200" width="38" height="16" fill="{TL if shirt==M else C}" {S}/>
<polygon points="{x-15},226 {x+15},226 {x+14},260 {x-12},262" fill="{skin}" {S}/>
<line x1="{x-8}" y1="246" x2="{x+8}" y2="246" stroke="{C}" stroke-width="2"/></g>'''
    head_dy = 6 if pose == 'sad' else 0
    return svg(240, 460, f'''
{leg(ll, 96)}{leg(rl, 144)}
<polygon points="70,256 170,256 168,284 72,284" fill="{pants}" {S}/>
<rect x="108" y="258" width="24" height="12" fill="{T}" stroke="{C}" stroke-width="3"/>
{arm(la, 62, 'l')}{arm(ra, 178, 'r')}
<polygon points="66,132 174,132 168,262 72,262" fill="{shirt}" {S}/>
<polygon points="66,132 174,132 168,262 72,262" fill="url(#ht)" opacity="0.35"/>
<line x1="120" y1="148" x2="120" y2="256" stroke="{C}" stroke-width="3"/>
{''.join(f'<rect x="124" y="{y}" width="6" height="6" fill="{C}"/>' for y in (166, 196, 226))}
<rect x="134" y="158" width="26" height="22" fill="none" stroke="{C}" stroke-width="3"/>
<rect x="108" y="116" width="24" height="22" fill="{skin}" {S}/>
<polygon points="94,132 120,154 146,132 132,124 120,140 108,124" fill="{shirt if shirt!=M else TL}" {S}/>
<g transform="translate({look},{head_dy})">
<polygon points="86,44 154,44 156,104 140,124 100,124 84,104" fill="{skin}" {S}/>
<rect x="76" y="72" width="12" height="24" fill="{skin}" {S}/><rect x="152" y="72" width="12" height="24" fill="{skin}" {S}/>
<polygon points="80,20 160,20 164,62 150,56 146,44 112,46 96,60 82,62" fill="{hair}" {S}/>
<polygon points="96,20 150,8 160,22" fill="{hair}" {S}/>
<rect x="100" y="{76+ (6 if pose=='sad' else 0)}" width="12" height="7" fill="{C}"/><rect x="128" y="{76+(6 if pose=='sad' else 0)}" width="12" height="7" fill="{C}"/>
<rect x="98" y="66" width="18" height="4" fill="{C}"/><rect x="124" y="66" width="18" height="4" fill="{C}"/>
<rect x="112" y="102" width="{16 if pose!='sad' else 12}" height="4" fill="{C}"/>
</g>''')

# ------------------------------------------------------------------ MANO QUE SEÑALA
def mano():
    S = f'stroke="{C}" stroke-width="6" stroke-linejoin="miter"'
    return svg(380, 200, f'''
<rect x="0" y="54" width="120" height="100" fill="{G3}" {S}/>
<rect x="0" y="54" width="120" height="100" fill="url(#htm)" opacity="0.25"/>
<rect x="110" y="48" width="34" height="112" fill="{M}" {S}/>
<rect x="120" y="64" width="12" height="12" fill="{C}"/><rect x="120" y="128" width="12" height="12" fill="{C}"/>
<polygon points="144,58 230,50 240,150 150,154" fill="{SK}" {S}/>
<polygon points="226,52 366,58 372,84 228,92" fill="{SK}" {S}/>
<rect x="344" y="62" width="18" height="16" fill="{M}" stroke="{C}" stroke-width="3"/>
<line x1="300" y1="64" x2="300" y2="86" stroke="{C}" stroke-width="3"/>
{''.join(f'<polygon points="{x},{y} {x+44},{y-2} {x+46},{y+24} {x},{y+26}" fill="{SK}" {S}/>' for x,y in ((206,94),(204,120)))}
<polygon points="202,146 244,144 244,166 204,168" fill="{SK}" {S}/>
<polygon points="160,40 200,24 222,40 200,58 168,62" fill="{SK}" {S}/>
<polygon points="150,90 196,96 194,150 150,154" fill="url(#ht)" opacity="0.6"/>
''')

# ------------------------------------------------------------------ BILLETE
def billete():
    S = f'stroke="{C}" stroke-width="6"'
    g = ''.join(f'<ellipse cx="150" cy="75" rx="{90-i*9}" ry="{44-i*4}" fill="none" stroke="{TD}" stroke-width="1.6"/>' for i in range(6))
    return svg(300, 150, f'''
<rect x="3" y="3" width="294" height="144" fill="#BFD0A8" {S}/>
<rect x="16" y="16" width="268" height="118" fill="none" stroke="{C}" stroke-width="2" stroke-dasharray="6 4"/>
{g.replace(TD, '#6F8460')}
<circle cx="150" cy="75" r="36" fill="#DDE6CF" stroke="{C}" stroke-width="4"/>
<circle cx="150" cy="64" r="12" fill="#6F8460"/><path d="M128,104 q22,-30 44,0 z" fill="#6F8460"/>
<text x="38" y="52" font-family="Sora" font-weight="800" font-size="30" fill="{C}">$</text>
<text x="262" y="124" font-family="Sora" font-weight="800" font-size="30" fill="{C}" text-anchor="end">100</text>
<text x="262" y="52" font-family="Sora" font-weight="800" font-size="22" fill="{C}" text-anchor="end">100</text>
<rect x="30" y="100" width="60" height="10" fill="#6F8460"/>
<rect x="3" y="3" width="294" height="144" fill="none" {S}/>''')

# ------------------------------------------------------------------ COHETE
def cohete(flame=True):
    S = f'stroke="{C}" stroke-width="6" stroke-linejoin="miter"'
    fl = f'''<polygon points="40,196 60,262 80,196" fill="{N}" {S}/><polygon points="50,196 60,232 70,196" fill="{M}"/>''' if flame else ''
    return svg(120, 270, f'''{fl}
<polygon points="60,6 92,60 92,190 28,190 28,60" fill="{M}" {S}/>
<polygon points="60,6 92,60 28,60" fill="{T}" {S}/>
<polygon points="60,64 92,64 92,190 60,190" fill="url(#ht)" opacity="0.6"/>
<circle cx="60" cy="96" r="16" fill="{A}" stroke="{C}" stroke-width="6"/><rect x="52" y="88" width="6" height="6" fill="{M}"/>
<rect x="28" y="140" width="64" height="12" fill="{C}"/>
<polygon points="28,150 4,200 28,190" fill="{T}" {S}/><polygon points="92,150 116,200 92,190" fill="{T}" {S}/>
<rect x="44" y="186" width="32" height="14" fill="{G3}" {S}/>''')

# ------------------------------------------------------------------ BOLSA DE DINERO
def bolsa():
    S = f'stroke="{C}" stroke-width="6" stroke-linejoin="miter"'
    return svg(180, 200, f'''
<polygon points="64,14 116,14 104,46 76,46" fill="{T}" {S}/>
<polygon points="70,46 110,46 168,120 160,190 20,190 12,120" fill="{T}" {S}/>
<polygon points="110,46 168,120 160,190 104,190" fill="url(#ht)"/>
<polygon points="70,46 110,46 168,120 160,190 20,190 12,120" fill="none" {S}/>
<rect x="62" y="42" width="56" height="12" fill="{N}" {S}/>
<text x="90" y="152" font-family="Sora" font-weight="800" font-size="64" text-anchor="middle" fill="{C}">$</text>''')

# ------------------------------------------------------------------ TARJETA DE ANUNCIO GENÉRICA
def anuncio(v=0):
    prods = [
        # tenis
        f'<polygon points="50,150 120,150 160,176 196,180 196,200 46,200" fill="{T}" stroke="{G5}" stroke-width="4"/><rect x="46" y="194" width="150" height="8" fill="{M}"/>',
        # botella
        f'<rect x="108" y="96" width="24" height="22" fill="{T}" stroke="{G5}" stroke-width="4"/><polygon points="96,118 144,118 150,206 90,206" fill="{T}" stroke="{G5}" stroke-width="4"/><rect x="96" y="150" width="48" height="26" fill="{G5}"/>',
        # lentes
        f'<rect x="56" y="140" width="56" height="36" fill="{T}" stroke="{G5}" stroke-width="5"/><rect x="128" y="140" width="56" height="36" fill="{T}" stroke="{G5}" stroke-width="5"/><rect x="110" y="148" width="20" height="6" fill="{G5}"/>',
        # taza
        f'<rect x="80" y="126" width="64" height="76" fill="{T}" stroke="{G5}" stroke-width="5"/><rect x="144" y="142" width="22" height="36" fill="none" stroke="{G5}" stroke-width="7"/><path d="M96,112 q6,-10 0,-20 M116,112 q6,-10 0,-20" stroke="{G5}" stroke-width="4" fill="none"/>',
    ]
    return svg(240, 320, f'''
<rect x="2" y="2" width="236" height="316" fill="#1A1A1A" stroke="#3E3E3E" stroke-width="4"/>
<circle cx="28" cy="28" r="14" fill="{G5}"/><rect x="50" y="18" width="90" height="9" fill="#4A4A4A"/><rect x="50" y="32" width="60" height="7" fill="{G3}"/>
<rect x="200" y="24" width="6" height="6" fill="{G5}"/><rect x="210" y="24" width="6" height="6" fill="{G5}"/><rect x="220" y="24" width="6" height="6" fill="{G5}"/>
<rect x="12" y="52" width="216" height="168" fill="#2E2A26"/>
<rect x="12" y="52" width="216" height="168" fill="url(#ht)" opacity="0.18"/>
{prods[v % 4]}
<path d="M24,242 c4,-7 14,-3 10,4 l-9,9 -9,-9 c-4,-7 4,-11 8,-4z" fill="none" stroke="{G5}" stroke-width="3"/>
<rect x="46" y="236" width="18" height="14" fill="none" stroke="{G5}" stroke-width="3"/>
<polygon points="76,236 96,242 76,250" fill="none" stroke="{G5}" stroke-width="3"/>
<rect x="206" y="234" width="14" height="18" fill="none" stroke="{G5}" stroke-width="3"/>
<rect x="16" y="264" width="170" height="8" fill="{G3}"/><rect x="16" y="278" width="120" height="8" fill="#303030"/>
<rect x="150" y="290" width="76" height="20" fill="{G3}"/>''')

# ------------------------------------------------------------------ CANALES (escena 5)
def canal(kind):
    S = f'stroke="{C}" stroke-width="5" stroke-linejoin="miter"'
    if kind == 'referidos':
        b = f'''
<polygon points="20,190 90,190 86,140 24,140" fill="{T}" {S}/><polygon points="38,92 76,92 78,134 36,134" fill="{SK}" {S}/><polygon points="34,78 80,78 82,98 72,92 40,94 32,98" fill="{C}" {S}/>
<polygon points="150,190 220,190 216,140 154,140" fill="{G3}" {S}/><polygon points="166,92 204,92 206,134 164,134" fill="{SK}" {S}/><polygon points="160,78 210,78 212,100 200,90 170,92 160,100" fill="{T}" {S}/>
<polygon points="88,24 168,24 168,72 136,72 120,88 120,72 88,72" fill="{M}" {S}/>
<path d="M120,38 c5,-9 18,-4 13,5 l-13,13 -13,-13 c-5,-9 8,-14 13,-5z" fill="{N}" stroke="{C}" stroke-width="3"/>
<rect x="20" y="186" width="200" height="6" fill="{C}"/>'''
    elif kind == 'alianzas':
        b = f'''
<rect x="6" y="96" width="70" height="56" fill="{G3}" {S}/><rect x="164" y="96" width="70" height="56" fill="{T}" {S}/>
<rect x="64" y="90" width="18" height="68" fill="{M}" {S}/><rect x="158" y="90" width="18" height="68" fill="{M}" {S}/>
<polygon points="82,98 138,86 170,104 166,148 110,158 82,150" fill="{SK}" {S}/>
{''.join(f'<polygon points="{x},{y} {x+30},{y-4} {x+34},{y+12} {x+2},{y+16}" fill="{SK}" {S}/>' for x,y in ((96,112),(98,128),(102,144)))}
<polygon points="120,90 160,100 150,116 112,108" fill="{SK}" {S}/>
<polygon points="110,108 170,104 166,148 136,150" fill="url(#ht)" opacity="0.7"/>
<line x1="34" y1="40" x2="54" y2="62" stroke="{C}" stroke-width="5"/><line x1="120" y1="24" x2="120" y2="54" stroke="{C}" stroke-width="5"/><line x1="206" y1="40" x2="186" y2="62" stroke="{C}" stroke-width="5"/>'''
    elif kind == 'eventos':
        flags = ''.join(f'<polygon points="{x},22 {x+26},22 {x+13},44" fill="{T if i%2 else C}" stroke="{C}" stroke-width="3"/>' for i, x in enumerate(range(14, 220, 30)))
        b = f'''
<line x1="8" y1="22" x2="232" y2="22" stroke="{C}" stroke-width="4"/>{flags}
<polygon points="30,60 70,60 110,170 -10,170" fill="url(#htc)" opacity="0.35"/>
<polygon points="170,60 210,60 250,170 130,170" fill="url(#htc)" opacity="0.35"/>
<rect x="34" y="50" width="32" height="16" fill="{C}"/><rect x="174" y="50" width="32" height="16" fill="{C}"/>
<rect x="111" y="80" width="18" height="34" fill="{C}"/><rect x="108" y="76" width="24" height="12" fill="{G5}" stroke="{C}" stroke-width="3"/>
<rect x="117" y="114" width="6" height="56" fill="{C}"/><rect x="100" y="166" width="40" height="8" fill="{C}"/>
<rect x="4" y="172" width="232" height="26" fill="{T}" {S}/><rect x="4" y="198" width="232" height="10" fill="{C}"/>'''
    elif kind == 'email':
        b = f'''
<polygon points="30,96 210,96 210,196 30,196" fill="{T}" {S}/>
<polygon points="44,40 196,40 196,150 44,150" fill="{M}" {S}/>
{''.join(f'<rect x="62" y="{y}" width="{w}" height="8" fill="{C}"/>' for y,w in ((60,70),(76,90),(92,60)))}
<text x="168" y="94" font-family="Sora" font-weight="800" font-size="40" text-anchor="middle" fill="{N}">@</text>
<polygon points="30,112 120,160 210,112 210,196 30,196" fill="{T}" {S}/>
<polygon points="30,196 120,140 210,196" fill="#B19D8A" {S}/>
<polygon points="120,140 210,196 210,112" fill="url(#ht)" opacity="0.8"/>'''
    elif kind == 'tienda':
        stripes = ''.join(f'<rect x="{12+i*24}" y="36" width="24" height="40" fill="{C if i%2==0 else M}"/>' for i in range(9))
        teeth = ''.join(f'<polygon points="{12+i*24},76 {36+i*24},76 {24+i*24},90" fill="{C if i%2==0 else M}" stroke="{C}" stroke-width="3"/>' for i in range(9))
        b = f'''
<rect x="20" y="70" width="200" height="130" fill="{M}" {S}/>
<rect x="20" y="70" width="200" height="130" fill="url(#ht)" opacity="0.3"/>
{stripes}<rect x="12" y="36" width="216" height="40" fill="none" {S}/>{teeth}
<rect x="60" y="8" width="120" height="26" fill="{T}" {S}/><rect x="74" y="17" width="92" height="7" fill="{C}"/>
<rect x="34" y="104" width="100" height="70" fill="{A}" {S}/>
<rect x="44" y="140" width="16" height="30" fill="{M}" stroke="{C}" stroke-width="3"/><rect x="68" y="128" width="16" height="42" fill="{T}" stroke="{C}" stroke-width="3"/><rect x="92" y="146" width="30" height="24" fill="{M}" stroke="{C}" stroke-width="3"/>
<rect x="150" y="104" width="54" height="96" fill="{G3}" {S}/><rect x="190" y="150" width="8" height="8" fill="{M}"/>
<rect x="26" y="196" width="190" height="8" fill="{C}"/>'''
    elif kind == 'b2b':
        win = lambda x0, y0, nx, ny: ''.join(f'<rect x="{x0+i*20}" y="{y0+j*22}" width="12" height="14" fill="{M}"/>' for i in range(nx) for j in range(ny))
        b = f'''
<rect x="14" y="60" width="78" height="140" fill="{C}" {S}/>{win(24,72,3,5)}
<rect x="150" y="24" width="78" height="176" fill="{G3}" {S}/>{win(160,36,3,7)}
<rect x="150" y="24" width="78" height="176" fill="url(#htm)" opacity="0.15"/>
<rect x="100" y="96" width="44" height="8" fill="{N}"/><polygon points="136,86 152,100 136,114" fill="{N}"/>
<rect x="100" y="130" width="44" height="8" fill="{C}"/><polygon points="108,120 92,134 108,148" fill="{C}"/>
<rect x="6" y="198" width="228" height="8" fill="{C}"/>'''
    elif kind == 'redes':
        cells = ''.join(f'<rect x="{84+i*26}" y="{60+j*26}" width="22" height="22" fill="{G5 if (i+j)%2 else T}"/>' for i in range(3) for j in range(4))
        b = f'''
<rect x="72" y="20" width="96" height="180" fill="{G2}" stroke="{M}" stroke-width="5"/>
<rect x="80" y="34" width="80" height="150" fill="{C}"/>
<circle cx="90" cy="45" r="6" fill="{T}"/><rect x="100" y="42" width="40" height="6" fill="{G5}"/>
{cells}
<rect x="104" y="188" width="32" height="5" fill="{M}"/>
<rect x="150" y="10" width="60" height="34" fill="{N}" stroke="{M}" stroke-width="4"/>
<path d="M164,24 c3,-6 11,-3 8,3 l-8,8 -8,-8 c-3,-6 5,-9 8,-3z" fill="{M}"/><rect x="180" y="21" width="20" height="8" fill="{M}"/>'''
    return svg(240, 210, b)

# ------------------------------------------------------------------ ÍCONOS DE BARRAS (línea marfil sobre negro)
def barra_icon(kind):
    S = f'stroke="{M}" stroke-width="6" stroke-linejoin="miter"'
    if kind == 'auto':
        b = f'''<polygon points="{gear_path(62,70,44,10,0.24)}" fill="{M}"/><rect x="48" y="56" width="28" height="28" fill="{C}"/>
<polygon points="{gear_path(116,112,30,8,0.28,0.2)}" fill="{T}"/><rect x="107" y="103" width="18" height="18" fill="{C}"/>
<rect x="18" y="122" width="54" height="30" fill="none" {S}/><rect x="26" y="130" width="12" height="14" fill="{M}"/><rect x="44" y="130" width="20" height="5" fill="{M}"/><rect x="44" y="139" width="14" height="5" fill="{M}"/>'''
    elif kind == 'aprende':
        b = f'''<rect x="14" y="96" width="18" height="50" fill="{T}"/><rect x="40" y="70" width="18" height="76" fill="{T}"/><rect x="66" y="84" width="18" height="62" fill="{T}"/>
<rect x="8" y="146" width="96" height="6" fill="{M}"/>
<circle cx="96" cy="64" r="36" fill="{C}" {S}/><circle cx="96" cy="64" r="36" fill="url(#htm)" opacity="0.35"/>
<polyline points="76,78 90,62 102,70 116,50" fill="none" stroke="{N}" stroke-width="6"/>
<line x1="122" y1="92" x2="150" y2="122" stroke="{M}" stroke-width="14"/>'''
    elif kind == 'ahorro':
        b = f'''<polygon points="30,70 120,70 140,96 140,130 120,140 120,154 102,154 102,140 54,140 54,154 36,154 36,138 20,126 20,90" fill="{T}" stroke="{M}" stroke-width="5"/>
<polygon points="30,70 50,46 62,70" fill="{T}" stroke="{M}" stroke-width="5"/>
<rect x="140" y="98" width="14" height="20" fill="{T}" stroke="{M}" stroke-width="5"/>
<rect x="60" y="78" width="40" height="7" fill="{C}"/><rect x="118" y="90" width="7" height="7" fill="{C}"/>
<polygon points="90,70 120,70 140,96 140,130 120,140 90,140" fill="url(#htc)" opacity="0.4"/>
<rect x="66" y="8" width="30" height="30" fill="{N}" stroke="{M}" stroke-width="4"/><text x="81" y="31" font-family="Sora" font-weight="800" font-size="22" text-anchor="middle" fill="{C}">$</text>
<rect x="76" y="44" width="10" height="16" fill="{M}"/>'''
    else:  # roi
        b = f'''<rect x="14" y="110" width="24" height="40" fill="{G5}"/><rect x="46" y="88" width="24" height="62" fill="{T}"/><rect x="78" y="62" width="24" height="88" fill="{M}"/>
<rect x="8" y="150" width="140" height="6" fill="{M}"/>
<polyline points="14,96 50,70 80,82 132,26" fill="none" stroke="{N}" stroke-width="10"/>
<polygon points="110,22 140,18 136,48" fill="{N}"/>
<circle cx="126" cy="112" r="22" fill="{C}" {S}/><text x="126" y="122" font-family="Sora" font-weight="800" font-size="28" text-anchor="middle" fill="{M}">$</text>'''
    return svg(160, 160, b)

ASSETS = {'golf': golf, 'canasta': canasta, 'persona': persona, 'mano': mano, 'billete': billete,
          'cohete': cohete, 'bolsa': bolsa, 'anuncio': anuncio, 'canal': canal, 'barra_icon': barra_icon}
