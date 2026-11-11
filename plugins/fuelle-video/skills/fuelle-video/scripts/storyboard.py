#!/usr/bin/env python3
"""
Arma el storyboard de aprobación (PDF + PNG) con la marca Fuelle.

Uso:
  python storyboard.py --spec storyboard.json --out-dir entregables/ --name Fuelle_Storyboard
storyboard.json:
{
  "title": "VIDEO 35 s · 1080×1920 · 30 fps",
  "main":  [ {"n":"01","tc":"0:00–0:03","image":"stills/s1.png","vo":"…","desc":"…","safe":"stills/s1_safe.png"} ],
  "extra": [ {"n":"04a","tc":"0:10.9","image":"stills/s4a.png","vo":"…","desc":"…"} ]
}
Páginas: 1) un fotograma por escena · 2) momentos intermedios · 3) verificación de área segura (si hay "safe").
Las fuentes se buscan en ../assets/fonts (Sora/Inter variables).
"""
import argparse, json, os, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'assets', 'fonts')
CAR = (15, 15, 15); MAR = (247, 243, 234); NAR = (255, 106, 0); GR = (107, 107, 107)
def sora(s):
    f = ImageFont.truetype(os.path.join(FONTS, 'Sora-Variable.ttf'), s)
    try: f.set_variation_by_name('ExtraBold')
    except Exception: pass
    return f
def inter(s, w='Regular'):
    f = ImageFont.truetype(os.path.join(FONTS, 'Inter-Variable.ttf'), s)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def page(items, title, sub, base):
    TW, TH = 360, 640; cols = 4; PW = cols * (TW + 40) + 80
    rows = (len(items) + cols - 1) // cols; PH = 220 + rows * (TH + 330) + 40
    p = Image.new('RGB', (PW, PH), MAR); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, PW, 140], fill=CAR)
    d.text((60, 70), 'FUELLE STUDIO', font=sora(46), fill=MAR, anchor='lm')
    d.text((460, 70), title, font=inter(24, 'Medium'), fill=MAR, anchor='lm')
    d.text((PW - 60, 70), sub, font=inter(20), fill=(170, 170, 170), anchor='rm')
    for i, it in enumerate(items):
        x = 60 + (i % cols) * (TW + 40); y = 180 + (i // cols) * (TH + 330)
        im = Image.open(os.path.join(base, it['image'])).convert('RGB').resize((TW, TH), Image.LANCZOS); p.paste(im, (x, y))
        d.rectangle([x, y, x + TW - 1, y + TH - 1], outline=CAR, width=3)
        yy = y + TH + 18
        d.text((x, yy), it['n'], font=sora(34), fill=NAR); d.text((x + TW, yy + 8), it['tc'], font=inter(20, 'Medium'), fill=GR, anchor='ra')
        yy += 52
        for l in textwrap.wrap('VO: “' + it.get('vo', '') + '”', 34)[:5]: d.text((x, yy), l, font=inter(19, 'SemiBold'), fill=CAR); yy += 26
        yy += 8
        for l in textwrap.wrap(it.get('desc', ''), 38)[:6]: d.text((x, yy), l, font=inter(18), fill=(60, 60, 60)); yy += 24
    return p
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--spec', required=True); ap.add_argument('--out-dir', default='.'); ap.add_argument('--name', default='Fuelle_Storyboard')
    a = ap.parse_args(); spec = json.load(open(a.spec, encoding='utf-8')); base = os.path.dirname(os.path.abspath(a.spec))
    pages = [page(spec['main'], 'STORYBOARD · ' + spec.get('title', ''), 'Fotogramas clave · 1 por escena', base)]
    if spec.get('extra'): pages.append(page(spec['extra'], 'STORYBOARD · MOMENTOS INTERMEDIOS', 'Transiciones y beats', base))
    safe = [dict(it, image=it['safe'], desc='Zona rosa = interfaz de la app. Todo lo importante queda dentro.') for it in spec['main'] if it.get('safe')]
    if safe: pages.append(page(safe, 'STORYBOARD · ÁREA SEGURA', 'arriba 270 · abajo 480 · izq 80 · der 160 px', base))
    os.makedirs(a.out_dir, exist_ok=True)
    png = os.path.join(a.out_dir, a.name + '_escenas.png'); pdf = os.path.join(a.out_dir, a.name + '.pdf')
    pages[0].save(png); pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=150)
    print('Storyboard listo:', pdf, png)
if __name__ == '__main__':
    main()
