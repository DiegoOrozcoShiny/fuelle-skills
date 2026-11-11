#!/usr/bin/env python3
"""
Motor de audio Fuelle: música generativa + efectos + mezcla con la voz (ducking) + loudness para redes.

Uso:
  python audio_engine.py --timeline timeline.json --voice voz.mp3 --out public/audio/mix.wav [--stems carpeta/]

timeline.json (campos usados):
{
  "duration": 35.0,
  "music": {
    "preset": "urgencia",                    # urgencia (reloj, latido, ostinato disonante) | energia (más luminoso)
    "bpm": 120,
    "sections": [ {"start":0,"end":16.6,"mood":"problema"}, {"start":16.6,"end":28.4,"mood":"solucion"},
                  {"start":28.4,"end":31.9,"mood":"climax"}, {"start":31.9,"end":35,"mood":"cierre"} ],
    "silences": [[12.3,12.9]]                # silencio total de música (golpes dramáticos)
  },
  "sfx": [ {"t":3.08,"type":"hit"}, {"t":3.3,"type":"tock"}, {"t":26.4,"type":"ding"} ... ]
}
Tipos de SFX: hit, tock, thump, tick, ding, whoosh_down, whoosh_up, riser(dur,f0,f1), stamp, swish, glass, paper, pop, boom
Requiere ffmpeg en PATH (para leer la voz y medir loudness).
"""
import argparse, json, subprocess, os, tempfile
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
from scipy.ndimage import maximum_filter1d, uniform_filter1d

SR = 48000
rng = np.random.default_rng(3)

def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR; e = np.exp(-t / d); na = int(a * SR)
    if na > 0: e[:na] *= np.linspace(0, 1, na)
    return e
def tone(f0, f1, d, decay, shape='sine'):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(ph) if shape == 'sine' else (2 * ((ph / (2 * np.pi)) % 1) - 1)
    return w * env(n, 0.002, decay)
def saw(f, d):
    t = np.arange(int(d * SR)) / SR; return 2 * ((f * t) % 1) - 1

class Bus:
    def __init__(self, dur): self.N = int(dur * SR); self.x = np.zeros(self.N)
    def add(self, t, sig, g=1.0):
        i = int(t * SR); j = min(self.N, i + len(sig))
        if 0 <= i < self.N: self.x[i:j] += sig[:j - i] * g

# ------------------------------------------------------------------ SFX
def sfx_hit(b, t, g=1): b.add(t, tone(90, 38, 0.5, 0.18), 0.9 * g); b.add(t, lp(noise(0.12), 2500) * env(int(0.12 * SR), 0, 0.03), 0.5 * g)
def sfx_tock(b, t, g=1): b.add(t, bp(noise(0.05), 1800, 4500) * env(int(0.05 * SR), 0, 0.006), 1.2 * g); b.add(t, tone(1150, 950, 0.08, 0.02), 0.45 * g)
def sfx_thump(b, t, g=1): b.add(t, tone(110, 55, 0.3, 0.08), 0.9 * g); b.add(t, lp(noise(0.05), 1200) * env(int(0.05 * SR), 0, 0.01), 0.4 * g)
def sfx_tick(b, t, g=1, f=2400): b.add(t, tone(f, f * 0.8, 0.03, 0.008), 0.35 * g)
def sfx_ding(b, t, g=1):
    n = int(1.8 * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for fr, a, d in [(1318.5, 1, 0.9), (2637, 0.35, 0.5), (3950, 0.15, 0.3), (1975.5, 0.2, 0.6)]: x += a * np.sin(2 * np.pi * fr * tt) * np.exp(-tt / d)
    b.add(t, x, 0.35 * g)
def sfx_whoosh(b, t, g=1, d=0.3, up=False):
    n = int(d * SR); x = noise(d); out = np.zeros(n); seg = int(SR * 0.01)
    for i in range(0, n, seg):
        u = i / n; fc = (300 + 5000 * u) if up else (5000 - 4700 * u)
        out[i:i + seg] = bp(x[max(0, i - 2000):i + seg], fc * 0.7, fc * 1.3)[-len(out[i:i + seg]):]
    b.add(t, out * np.sin(np.linspace(0, np.pi, n)) ** 1.5, 0.6 * g)
def sfx_riser(b, t, g=1, d=1.0, f0=200, f1=900): b.add(t, lp(tone(f0, f1, d, 10, 'saw'), 3000) * np.linspace(0.2, 1, int(d * SR)), 0.22 * g)
def sfx_stamp(b, t, g=1): sfx_thump(b, t, 0.8 * g); b.add(t, hp(noise(0.08), 1500) * env(int(0.08 * SR), 0, 0.02), 0.4 * g)
def sfx_pop(b, t, g=1): b.add(t, tone(880, 1320, 0.08, 0.03), 0.35 * g)
def sfx_glass(b, t, g=1):
    for k in range(10): b.add(t + k * 0.012, bp(noise(0.06), 3000 + 400 * k, 6000 + 400 * k) * env(int(0.06 * SR), 0, 0.02), 0.25 * g)
def sfx_paper(b, t, g=1): b.add(t, bp(noise(0.18), 800, 6000) * env(int(0.18 * SR), 0.01, 0.06), 0.45 * g)
def sfx_boom(b, t, g=1): b.add(t, tone(55, 30, 2.5, 0.9), 1.0 * g)
SFX = {'hit': sfx_hit, 'tock': sfx_tock, 'thump': sfx_thump, 'tick': sfx_tick, 'ding': sfx_ding, 'whoosh_down': sfx_whoosh,
       'whoosh_up': lambda b, t, g=1, **k: sfx_whoosh(b, t, g, up=True, **k), 'riser': sfx_riser, 'stamp': sfx_stamp, 'pop': sfx_pop,
       'glass': sfx_glass, 'paper': sfx_paper, 'boom': sfx_boom, 'swish': lambda b, t, g=1, **k: sfx_whoosh(b, t, g, d=0.18)}

# ------------------------------------------------------------------ MÚSICA (preset urgencia)
D, Eb, F, G, A, C3 = 73.42, 77.78, 87.31, 98.0, 110.0, 65.41
PAT = {'problema': [D, D, Eb, D, F, D, Eb, C3], 'solucion': [D, F, A, D * 2, A, F, G, A], 'climax': [D, Eb, D, Eb, F, Eb, G, F], 'cierre': [], 'pausa': []}
DRONE = {'problema': [36.71, 55.0, 38.89], 'solucion': [36.71, 55.0, 73.42], 'climax': [36.71, 55.0, 38.89, 51.91], 'cierre': [36.71, 55.0, 73.42], 'pausa': [36.71, 38.89]}
PAD = {'problema': [587.3, 622.3], 'solucion': [587.3, 880.0], 'climax': [587.3, 622.3, 415.3], 'cierre': [587.3, 880.0, 440.0], 'pausa': [587.3, 622.3]}

def music(dur, cfg):
    b = Bus(dur); spb = 60 / cfg.get('bpm', 120); s16 = spb / 4
    sections = cfg['sections']; sil = cfg.get('silences', [])
    def mood_at(t):
        for s in sections:
            if s['start'] <= t < s['end']: return s['mood']
        return sections[-1]['mood']
    for s in sections:  # drones y pads
        d = s['end'] - s['start']; n = int(d * SR); x = np.zeros(n); tt = np.arange(n) / SR
        fr = DRONE[s['mood']]
        for f in fr:
            for det in (-0.6, 0.6): x += saw(f + det, d)[:n]
        cut = {'problema': 600, 'solucion': 800, 'climax': 1500, 'cierre': 500, 'pausa': 220}[s['mood']]
        x = lp(x, cut) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.5 * tt)) / len(fr)
        fade = np.minimum(1, np.minimum(tt / 0.3, (d - tt) / 0.3)); b.add(s['start'], x * fade, 0.55)
        p = np.zeros(n)
        for f in PAD[s['mood']]: p += np.sin(2 * np.pi * f * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * 5.5 * tt + f))
        b.add(s['start'], p * fade / len(PAD[s['mood']]), 0.1)
    t, k = 0.0, 0
    while t < dur - 0.4:
        m = mood_at(t); in_sil = any(a - 0.05 <= t < c for a, c in sil)
        if not in_sil:
            if m == 'pausa':
                if k % 4 == 0: sfx_tock(b, t, 0.35)
            else:
                if k % 2 == 0: b.add(t, bp(noise(0.03), 2800 if (k // 2) % 2 == 0 else 1900, 5200) * env(int(0.03 * SR), 0.0005, 0.006), 0.55)  # reloj
                if k % 4 == 0 and m in ('problema', 'solucion', 'climax'):
                    g = 0.8 if m == 'problema' else 0.6
                    b.add(t, tone(70, 40, 0.25, 0.07), 0.95 * g); b.add(t + 0.16, tone(62, 38, 0.22, 0.06), 0.6 * g)  # latido
                pat = PAT[m]
                if pat:
                    b.add(t, lp(saw(pat[k % 8] * 2, 0.11) * env(int(0.11 * SR), 0.002, 0.035), 1800), 0.32 * (1.0 if m == 'climax' else 0.8))
        t = round(t + s16, 5); k += 1
    for s in sections:
        if s['mood'] == 'climax':  # redoble que acelera
            tt = s['start']
            while tt < s['end'] - 0.05:
                u = (tt - s['start']) / (s['end'] - s['start'])
                b.add(tt, bp(noise(0.12), 1200, 5000) * env(int(0.12 * SR), 0.001, 0.04), 0.5 * (0.25 + 0.75 * u)); tt += 0.25 * (1 - u) + 0.04
        if s['mood'] == 'cierre': sfx_boom(b, s['start'])
        if s['start'] > 0.5:  # ruido en reversa hacia cada cambio de sección
            n = int(0.9 * SR); b.add(s['start'] - 0.9, hp(noise(0.9), 600) * np.linspace(0, 1, n) ** 3, 0.45)
    x = b.x
    for a, c in sil: x[int(a * SR):int(c * SR)] = 0
    tail = int((dur - 0.8) * SR); x[tail:] *= np.linspace(1, 0, len(x) - tail) ** 2
    return x

def load_voice(path, dur):
    tmp = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ar', str(SR), '-ac', '1', tmp], check=True)
    _, v = wavfile.read(tmp); os.remove(tmp)
    v = v.astype(np.float32) / 32768; out = np.zeros(int(dur * SR)); out[:min(len(out), len(v))] = v[:len(out)]
    return out / (np.max(np.abs(out)) + 1e-9) * 0.9

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeline', required=True); ap.add_argument('--voice'); ap.add_argument('--out', required=True); ap.add_argument('--stems')
    a = ap.parse_args()
    tl = json.load(open(a.timeline, encoding='utf-8')); dur = float(tl['duration'])
    mus = music(dur, tl['music']); fx = Bus(dur)
    for e in tl.get('sfx', []):
        e = dict(e); t = e.pop('t'); typ = e.pop('type'); SFX[typ](fx, t, **e)
    mus /= np.max(np.abs(mus)) + 1e-9; fxs = fx.x / (np.max(np.abs(fx.x)) + 1e-9)
    if a.voice:
        v = load_voice(a.voice, dur)
        e = uniform_filter1d(maximum_filter1d(np.abs(v), int(0.08 * SR)), int(0.25 * SR)); e = np.clip(e / (np.percentile(e, 95) + 1e-9), 0, 1)
        mix = v + mus * 0.34 * (1 - 0.6 * e) + fxs * 0.42 * (1 - 0.35 * e)
    else:
        v = None; mix = mus * 0.6 + fxs * 0.5
    mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / np.max(np.abs(mix)) * 0.93
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    wavfile.write(a.out, SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    if a.stems:
        os.makedirs(a.stems, exist_ok=True)
        for name, sig in (('musica', mus * 0.6), ('sfx', fxs * 0.6), ('musica_sfx', (mus * 0.34 + fxs * 0.42) / 0.8)):
            sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.9
            wavfile.write(os.path.join(a.stems, f'{name}.wav'), SR, (np.stack([sig, sig], 1) * 32767).astype(np.int16))
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.out, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    il = [l for l in r.splitlines() if l.strip().startswith('I:')]
    print('Mezcla lista:', a.out, '| loudness integrado:', il[-1].strip() if il else 'n/d', '(objetivo −14 a −13 LUFS)')

if __name__ == '__main__':
    main()
