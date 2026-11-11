#!/usr/bin/env python3
"""
Alinea el guion (una frase de subtítulo por línea) con la voz generada en ElevenLabs y escribe subtitles.json.

Modos (de más a menos preciso):
  --mode elevenlabs  Forced Alignment de ElevenLabs (requiere ELEVENLABS_API_KEY). Tiempos por palabra.
  --mode whisper     faster-whisper local con marcas por palabra (pip install faster-whisper; descarga el modelo 1 vez).
  --mode pauses      Solo FFmpeg: reparte por pausas y sílabas. Aproximado: SIEMPRE revisar a oído.
  --mode auto        (default) elevenlabs si hay API key → whisper si está instalado → pauses.

Uso:
  python align_voice.py --audio voz.mp3 --script frases.txt --out subtitles.json [--mode auto]
Salida: [{"start":0.11,"end":1.5,"text":"..."}, ...] + reporte en consola + words.json (tiempos por palabra si hay).
"""
import argparse, json, os, re, subprocess, unicodedata, difflib

def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)

def phrase_tokens(lines):
    return [[norm(w) for w in l.split() if norm(w)] for l in lines]

def words_to_subs(lines, words, pad=0.12):
    """words: [{'text','start','end'}] en orden. Empata tokens del guion con palabras alineadas (difflib)."""
    toks = phrase_tokens(lines)
    flat = [(i, t) for i, ph in enumerate(toks) for t in ph]
    wn = [norm(w["text"]) for w in words]
    sm = difflib.SequenceMatcher(a=[t for _, t in flat], b=wn, autojunk=False)
    idx = [None] * len(flat)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): idx[blk.a + k] = blk.b + k
    subs = []
    for i, l in enumerate(lines):
        js = [idx[k] for k, (pi, _) in enumerate(flat) if pi == i and idx[k] is not None]
        if js: subs.append({"start": round(words[min(js)]["start"], 2), "end": round(words[max(js)]["end"] + pad, 2), "text": l})
        else: subs.append({"start": None, "end": None, "text": l})
    for i, s in enumerate(subs):  # interpolar huecos
        if s["start"] is None:
            prev = subs[i - 1]["end"] if i else 0.0
            nxt = next((x["start"] for x in subs[i + 1:] if x["start"] is not None), prev + 1.0)
            s["start"], s["end"] = round(prev, 2), round(nxt, 2)
    for i in range(len(subs) - 1):
        if subs[i]["end"] > subs[i + 1]["start"]: subs[i]["end"] = subs[i + 1]["start"]
    return subs

def align_elevenlabs(audio, text):
    import urllib.request, uuid
    key = os.environ["ELEVENLABS_API_KEY"]; b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{text}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(audio)}\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode()
    body += open(audio, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment", data=body, method="POST",
                                 headers={"xi-api-key": key, "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.load(urllib.request.urlopen(req))["words"]

def align_whisper(audio, model="small"):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, compute_type="int8")
    segs, _ = m.transcribe(audio, language="es", word_timestamps=True)
    return [{"text": w.word, "start": w.start, "end": w.end} for s in segs for w in s.words]

def silences(audio, noise="-32", dur="0.06"):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", f"silencedetect=noise={noise}dB:d={dur}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    h, m, s = re.findall(r"Duration: (\d+):(\d+):([\d.]+)", out)[0]
    return list(zip(st, en)), int(h) * 3600 + int(m) * 60 + float(s)

def syllables(t):
    t = re.sub(r"[^a-záéíóúüñ ]", " ", t.lower()); return max(1, len(re.findall(r"[aeiouáéíóúü]+", t)))

def align_pauses(audio, lines):
    """Aproximación: pseudo-palabras repartidas por sílabas dentro del tiempo de habla."""
    sil, total = silences(audio)
    segs, cur = [], 0.0
    for s, e in sil:
        if s - cur > 0.05: segs.append((cur, s))
        cur = e
    if total - cur > 0.05: segs.append((cur, total))
    talk = sum(e - s for s, e in segs)
    toks = [w for l in lines for w in l.split()]
    syl = [syllables(w) for w in toks]; tot = sum(syl)
    def at(x):
        acc = 0.0
        for s, e in segs:
            if acc + (e - s) >= x: return s + (x - acc)
            acc += e - s
        return segs[-1][1]
    words, acc = [], 0
    for w, n in zip(toks, syl):
        a0 = at(talk * acc / tot); acc += n; words.append({"text": w, "start": a0, "end": at(talk * acc / tot)})
    return words

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True); ap.add_argument("--script", required=True)
    ap.add_argument("--out", default="subtitles.json"); ap.add_argument("--mode", default="auto"); ap.add_argument("--whisper-model", default="small")
    a = ap.parse_args()
    lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
    mode = a.mode
    if mode == "auto":
        if os.environ.get("ELEVENLABS_API_KEY"): mode = "elevenlabs"
        else:
            try: import faster_whisper  # noqa
            except ImportError: mode = "pauses"
            else: mode = "whisper"
    if mode == "elevenlabs": words = align_elevenlabs(a.audio, " ".join(lines))
    elif mode == "whisper": words = align_whisper(a.audio, a.whisper_model)
    else: words = align_pauses(a.audio, lines)
    subs = words_to_subs(lines, words)
    json.dump(subs, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(words, open(os.path.splitext(a.out)[0] + "_words.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sil, total = silences(a.audio)
    print(f"Modo: {mode} · audio {total:.2f} s")
    if mode == "pauses": print("AVISO: modo aproximado. Verifica cada frase a oído y corrige el JSON antes del storyboard.")
    for s in subs: print(f"{s['start']:6.2f} – {s['end']:6.2f} | {s['text']}")
    print("Pausas largas (>0.4 s):", ", ".join(f"{s:.2f}–{e:.2f}" for s, e in sil if e - s > 0.4))

if __name__ == "__main__":
    main()
