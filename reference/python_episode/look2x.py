"""Widescreen (1920x1080) lesson style: moving colour background, code editor, output panel, chapters."""
import math, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, "/home/claude/video")
import make as m

W, H, FPS = 1920, 1080, 30  # logical layout units
SC = 4 / 3  # physical scale: 2560x1440
PW, PH = round(W * SC), round(H * SC)
font = m.font
WHITE, MUTED, ACC, DARK = (255, 255, 255), (176, 186, 214), (74, 222, 128), (8, 30, 16)
RED, BLUE, PURPLE, YELLOW, ORANGE = (248, 86, 86), (80, 150, 255), (168, 110, 255), (250, 204, 21), (251, 146, 60)
INK, PANEL, CODEBG = (7, 9, 20), (26, 32, 66), (10, 13, 30)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
EMO = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
_b = Image.open("/home/claude/logo/brand.png").convert("RGBA")
BRAND = _b.resize((round(_b.width * SC), round(_b.height * SC)), Image.LANCZOS)
_mf = {}


def mono(size, bold=False):
    if (size, bold) not in _mf:
        _mf[(size, bold)] = ImageFont.truetype(MONOB if bold else MONO, size)
    return _mf[(size, bold)]


def clamp(x): return max(0.0, min(1.0, x))
def a(t, start, dur=0.3): return 1 - (1 - clamp((t - start) / dur)) ** 3
def out(t, start, dur=0.2): return 1 - clamp((t - start) / dur)
def col(c, al): return (c[0], c[1], c[2], int(255 * clamp(al)))


def pop(t, start, dur=0.38):
    x = clamp((t - start) / dur)
    if x <= 0: return 0.0
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


# ---------- background ----------
_y = np.linspace(0, 1, PH)[:, None]
_base = np.zeros((PH, PW, 3), np.float32)
_base[..., 0] = 7 + 10 * _y; _base[..., 1] = 9 + 10 * _y; _base[..., 2] = 20 + 26 * _y
BASE = Image.fromarray(_base.astype(np.uint8))
_gd = ImageDraw.Draw(BASE, "RGBA")
for x in range(0, PW, 128): _gd.line([x, 0, x, PH], fill=(255, 255, 255, 7), width=3)
for y in range(0, PH, 128): _gd.line([0, y, PW, y], fill=(255, 255, 255, 7), width=3)
S = 1330
_mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(_mask).ellipse([265, 265, S - 265, S - 265], fill=100)
BLOB = _mask.filter(ImageFilter.GaussianBlur(186))
_solid = {}


def bg(T, pal):
    im = BASE.copy()
    spots = [(1580, 200), (260, 820), (1100, 1000)]
    for i, c in enumerate(pal[:3]):
        if c not in _solid: _solid[c] = Image.new("RGB", (S, S), c)
        x = (spots[i][0] + math.sin(T * 0.5 + i * 2.1) * 200) * SC - S // 2
        y = (spots[i][1] + math.cos(T * 0.4 + i * 1.3) * 120) * SC - S // 2
        im.paste(_solid[c], (int(x), int(y)), BLOB)
    return im


# ---------- text pieces ----------
_ec = {}


def emoji(layer, ch, cx, cy, size, p=1.0):
    if p <= 0.02: return
    cx, cy, size = cx * SC, cy * SC, size * SC
    s = max(16, int(size * p / 8) * 8)
    if (ch, s) not in _ec:
        im = Image.new("RGBA", (170, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((14, 12), ch, font=EMO, embedded_color=True)
        im = im.crop(im.getbbox())
        _ec[(ch, s)] = im.resize((max(1, int(im.width * s / im.height)), s), Image.LANCZOS)
    im = _ec[(ch, s)]
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    if x >= 0 and y >= 0 and x + im.width <= PW and y + im.height <= PH:
        layer.alpha_composite(im, (x, y))


def text(d, s, x, y, size, fill, p=1.0, weight="ExtraBold", display=True, anchor="mm", slide=28):
    if p <= 0: return
    d.text((x, y + (1 - min(p, 1)) * slide), s, font=font(size, weight, display), fill=col(fill, p), anchor=anchor)


def body(d, s, x, y, size, fill, p=1.0, anchor="mm"):
    text(d, s, x, y, size, fill, p, "SemiBold", False, anchor)


def kw(d, words, cx, y, size, t, t0, step, hi=None, fill=WHITE, maxw=1720):
    """One-line headline that appears word by word; words in hi get a coloured box."""
    hi = hi or {}
    while True:
        f = font(size); sp = size * 0.27
        ws = [d.textlength(w, font=f) for w in words]
        if sum(ws) + sp * (len(words) - 1) + 50 <= maxw or size < 30: break
        size -= 4
    x = cx - (sum(ws) + sp * (len(words) - 1)) / 2
    for i, (w, wd) in enumerate(zip(words, ws)):
        p = a(t, t0 + i * step, 0.16)
        if p > 0:
            yy = y - size * 0.6 + (1 - p) * 30
            if w in hi:
                d.rounded_rectangle([x - 18, yy - 2, x + wd + 18, yy + size * 1.2], 18, fill=col(hi[w], p))
                d.text((x, yy), w, font=f, fill=col(INK, p))
            else:
                d.text((x, yy), w, font=f, fill=col(fill, p))
        x += wd + sp


def panel(d, x0, y0, x1, y1, p, outline=None, fill=PANEL, r=36):
    if p <= 0: return 0
    oy = (1 - min(p, 1)) * 50
    d.rounded_rectangle([x0 + 8, y0 + oy + 10, x1 + 8, y1 + oy + 10], r, fill=(0, 0, 0, int(80 * clamp(p))))
    d.rounded_rectangle([x0, y0 + oy, x1, y1 + oy], r, fill=col(fill, p), outline=col(outline, p) if outline else None, width=5)
    return oy


def pill(d, label, cx, cy, p, size=46, fill=ACC, fg=DARK):
    if p <= 0: return
    k = 0.7 + 0.3 * min(p, 1.08)
    f = font(int(size * k), "Bold", False)
    w = d.textlength(label, font=f) + 90 * k
    h = size * 2.1 * k
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], h / 2, fill=col(fill, p))
    d.text((cx, cy), label, font=f, fill=col(fg, p), anchor="mm")


# ---------- code ----------
KEYWORDS = {"public", "class", "static", "void", "True", "False", "None", "if", "else"}
BUILTINS = {"print", "input", "int", "type", "float", "str"}
C_STR, C_NUM, C_KW, C_FN, C_OP, C_TXT = (152, 224, 130), (251, 166, 90), (198, 140, 255), (110, 180, 255), (137, 221, 255), (220, 226, 245)
TOK = re.compile(r'f?"[^"]*"?|\d+(?:\.\d+)?|[A-Za-z_]\w*|\s+|.')


def draw_code_line(d, x, y, s, f):
    for tok in TOK.findall(s):
        if tok.startswith(('"', 'f"')):
            if tok.startswith('f"'):
                parts = re.split(r'(\{[^}]*\}?)', tok)
                for part in parts:
                    c = C_TXT if part.startswith("{") else C_STR
                    d.text((x, y), part, font=f, fill=c + (255,))
                    x += d.textlength(part, font=f)
                continue
            c = C_STR
        elif tok[0].isdigit(): c = C_NUM
        elif tok in KEYWORDS: c = C_KW
        elif tok in BUILTINS: c = C_FN
        elif tok.strip() and not tok[0].isalnum() and tok[0] != "_": c = C_OP
        else: c = C_TXT
        d.text((x, y), tok, font=f, fill=c + (255,))
        x += d.textlength(tok, font=f)
    return x


def code_win(d, x0, y0, x1, lines, t, ts, te, p, size=44, label="code", run_t=None, outline=None):
    """Code editor that types its lines between ts and te. Returns the window's bottom edge."""
    lh = size * 1.45
    h = 78 + len(lines) * lh + 34
    if p <= 0: return y0 + h
    oy = panel(d, x0, y0, x1, y0 + h, p, outline=outline, fill=CODEBG, r=26)
    for i, c in enumerate([(248, 113, 113), (250, 204, 21), (74, 222, 128)]):
        d.ellipse([x0 + 28 + i * 34, y0 + oy + 26, x0 + 48 + i * 34, y0 + oy + 46], fill=col(c, p))
    d.text((x0 + 150, y0 + oy + 36), label, font=font(30, "SemiBold", False), fill=col(MUTED, p), anchor="lm")
    if run_t is not None:
        rx, ry = x1 - 60, y0 + oy + 36
        rp = clamp((t - run_t) / 0.5)
        if 0 < rp < 1:
            r = 24 + 40 * rp
            d.ellipse([rx - r, ry - r, rx + r, ry + r], outline=col(ACC, 1 - rp), width=5)
        on = t >= run_t
        d.ellipse([rx - 24, ry - 24, rx + 24, ry + 24], fill=col(ACC if on else (60, 72, 120), p))
        d.polygon([(rx - 8, ry - 12), (rx - 8, ry + 12), (rx + 13, ry)], fill=col(INK if on else MUTED, p))
    f = mono(size)
    total = sum(len(s) for s in lines)
    n = int(clamp((t - ts) / max(0.01, te - ts)) * total)
    cx, cy = None, None
    for i, s in enumerate(lines):
        vis = s[:max(0, n)]
        n -= len(s)
        y = y0 + oy + 78 + 12 + i * lh
        if vis:
            ex = draw_code_line(d, x0 + 44, y, vis, f)
            cx, cy = ex, y
        if 0 < len(vis) < len(s) or (vis == s and n <= 0 and n > -1):
            cx, cy = (ex if vis else x0 + 44), y
    if cx is not None and t < te + 0.6 and int(t * 3) % 2 == 0:
        d.rectangle([cx + 2, cy + 2, cx + size * 0.55, cy + size * 1.08], fill=col(ACC, p))
    return y0 + h


def out_win(d, x0, y0, x1, items, t, p, size=40, label="Output", outline=None):
    """items: list of (segments, appear_time); segments: list of (text, colour, bold)."""
    lh = size * 1.45
    h = 70 + max(1, len(items)) * lh + 28
    if p <= 0: return y0 + h
    oy = panel(d, x0, y0, x1, y0 + h, p, outline=outline, fill=(14, 18, 40), r=26)
    d.text((x0 + 40, y0 + oy + 36), label, font=font(30, "Bold", False), fill=col(MUTED, p), anchor="lm")
    for i, (segs, at) in enumerate(items):
        q = a(t, at, 0.18) * p
        if q <= 0: continue
        x = x0 + 44
        y = y0 + oy + 70 + 8 + i * lh
        for s, c, b in segs:
            f = mono(size, b)
            d.text((x, y), s, font=f, fill=col(c, q))
            x += d.textlength(s, font=f)
    return y0 + h


def stamp(layer, label, cx, cy, p, colr=RED, size=110, angle=-6):
    if p <= 0: return
    f = font(round(size * SC))
    cx, cy = cx * SC, cy * SC
    tmp = Image.new("RGBA", (1500, 400), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    w = td.textlength(label, font=f)
    td.rounded_rectangle([750 - w / 2 - 58, 66, 750 + w / 2 + 58, 334], 34, outline=col(colr, 1), width=17)
    td.text((750, 200), label, font=f, fill=col(colr, 1), anchor="mm")
    k = 1 + 0.7 * (1 - clamp(p))
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, expand=True)
    tmp = tmp.resize((int(tmp.width * k), int(tmp.height * k)), Image.BILINEAR)
    if clamp(p) < 1: tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * clamp(p))))
    x, y = int(cx - tmp.width / 2), int(cy - tmp.height / 2)
    crop = tmp.crop((max(0, -x), max(0, -y), min(tmp.width, PW - x), min(tmp.height, PH - y)))
    layer.alpha_composite(crop, (max(0, x), max(0, y)))


# ---------- scaled drawing ----------
class SD:
    """Draws in logical 1920x1080 units onto a physical 2560x1440 image."""
    _fc = {}

    def __init__(self, d): self.d = d

    def f(self, fo):
        k = (fo.path, fo.size)
        if k not in SD._fc: SD._fc[k] = fo.font_variant(size=max(1, round(fo.size * SC)))
        return SD._fc[k]

    @staticmethod
    def xy(v):
        if isinstance(v, (int, float)): return v * SC
        return [SD.xy(e) for e in v]

    def text(self, xy, txt, font=None, fill=None, anchor=None, **kw):
        self.d.text(tuple(self.xy(list(xy))), txt, font=self.f(font), fill=fill, anchor=anchor, **kw)

    def textlength(self, txt, font=None): return self.d.textlength(txt, font=self.f(font)) / SC
    def rounded_rectangle(self, xy, radius=0, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(self.xy(list(xy)), radius * SC, fill=fill, outline=outline, width=max(1, round(width * SC)))
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self.d.rectangle(self.xy(list(xy)), fill=fill, outline=outline, width=max(1, round(width * SC)))
    def ellipse(self, xy, fill=None, outline=None, width=1):
        self.d.ellipse(self.xy(list(xy)), fill=fill, outline=outline, width=max(1, round(width * SC)))
    def polygon(self, xy, fill=None, outline=None):
        self.d.polygon([tuple(p) for p in self.xy([list(p) for p in xy])], fill=fill, outline=outline)
    def line(self, xy, fill=None, width=1, joint=None):
        self.d.line(self.xy(list(xy)), fill=fill, width=max(1, round(width * SC)), joint=joint)
    def arc(self, xy, start, end, fill=None, width=1):
        self.d.arc(self.xy(list(xy)), start, end, fill=fill, width=max(1, round(width * SC)))


# ---------- frame ----------
class Scene:
    def __init__(self, sid, chapter, fn, pal, D, B, t0, total):
        self.sid, self.chapter, self.fn, self.pal, self.D, self.B, self.t0, self.total = sid, chapter, fn, pal, D, B, t0, total


def frame(sc, t):
    T = sc.t0 + t
    im = bg(T, sc.pal)
    layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    d = SD(ImageDraw.Draw(layer))
    sc.fn(layer, d, t, sc.D, sc.B)
    layer.alpha_composite(BRAND, (round(44 * SC), round(30 * SC)))
    f = font(34, "ExtraBold", False)
    tw = d.textlength("LEARN", font=f)
    x1 = W - 48
    d.rounded_rectangle([x1 - tw - 64, 52, x1, 120], 34, fill=col(ACC, 1))
    d.text((x1 - 32, 86), "LEARN", font=f, fill=col(INK, 1), anchor="rm")
    cf = font(32, "Bold", False)
    cw = d.textlength(sc.chapter, font=cf)
    cx1 = x1 - tw - 84
    d.rounded_rectangle([cx1 - cw - 60, 52, cx1, 120], 34, fill=col((20, 26, 56), 0.9), outline=col((70, 84, 140), 1), width=3)
    d.text((cx1 - 30, 86), sc.chapter, font=cf, fill=col(WHITE, 1), anchor="rm")
    d.rectangle([0, H - 10, W * T / sc.total, H], fill=col(sc.pal[0], 1))
    im.paste(layer, (0, 0), layer)
    return im
