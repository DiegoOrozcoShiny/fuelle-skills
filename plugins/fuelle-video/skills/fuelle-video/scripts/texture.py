import numpy as np
from PIL import Image, ImageFilter
_cache = {}
def noise(w, h, seed=1):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for k, amp in ((8, 0.5), (32, 0.3), (128, 0.15), (512, 0.05)):
        sw, sh = max(2, w * k // 1080), max(2, h * k // 1080)
        n = rng.standard_normal((sh, sw)).astype(np.float32)
        im = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += (np.asarray(im, np.float32) / 127.5 - 1) * amp
    fine = rng.standard_normal((h, w)).astype(np.float32) * 0.25
    acc += fine
    # poros (speckles)
    sp = rng.random((h, w)) > 0.9985
    acc[sp] -= 2.5
    return acc
def background(kind, S):
    key = (kind, S)
    if key in _cache: return _cache[key]
    W, H = 1080 * S, 1920 * S
    n = noise(W, H, 3 if kind == 'dark' else 5)
    if kind == 'dark':
        base = np.array([15, 15, 15], np.float32); amp = 7
    else:
        base = np.array([247, 243, 234], np.float32); amp = 9
    arr = base[None, None, :] + n[..., None] * amp
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    _cache[key] = im
    return im
def concrete(w, h, S, tone=(122, 117, 112), seed=9):
    key = ('conc', w, h, S, tone, seed)
    if key in _cache: return _cache[key]
    W, H = int(w * S), int(h * S)
    n = noise(max(W, 64), max(H, 64), seed)[:H, :W]
    arr = np.array(tone, np.float32)[None, None, :] + n[..., None] * 16
    # encofrado: líneas horizontales cada 34 px
    for y in range(0, H, int(34 * S)):
        arr[y:y + max(1, int(2 * S))] -= 22
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    _cache[key] = im
    return im
