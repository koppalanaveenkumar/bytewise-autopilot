import sys, os, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG1, BG2 = (10, 14, 32), (22, 30, 66)
WHITE = (255, 255, 255)
MUTED = (170, 180, 210)
ACC = (74, 222, 128)
CARD = (30, 40, 84)
KEY = (52, 64, 118)
FD = "/usr/share/fonts/opentype/inter/"


def font(size, weight="ExtraBold", display=True):
    return ImageFont.truetype(f"{FD}{'InterDisplay' if display else 'Inter'}-{weight}.otf", size)


def make_bg():
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        k = y / H
        c = tuple(int(BG1[i] + (BG2[i] - BG1[i]) * k) for i in range(3))
        for x in range(W):
            px[x, y] = c
    from PIL import ImageFilter
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([W - 560, -210, W + 160, 510], fill=70)
    g = g.filter(ImageFilter.GaussianBlur(170))
    im.paste(Image.new("RGB", (W, H), ACC), (0, 0), g)
    return im


BG = make_bg()


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def a(t, start, dur=0.5):
    return ease((t - start) / dur)


def col(c, alpha):
    return (c[0], c[1], c[2], int(255 * max(0, min(1, alpha))))


def text_c(d, lines, y, f, fill, alpha=1.0, dy=0, gap=1.18):
    for i, ln in enumerate(lines):
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y + dy + i * f.size * gap), ln, font=f, fill=col(fill, alpha))


def badge(d, label, y, alpha, dy=0):
    f = font(40, "Bold", False)
    w = d.textlength(label, font=f) + 72
    x = (W - w) / 2
    d.rounded_rectangle([x, y + dy, x + w, y + dy + 80], 40, fill=col(ACC, alpha))
    d.text((x + 36, y + dy + 16), label, font=f, fill=col((8, 30, 16), alpha))


def caption(d, lines, t, start):
    p = a(t, start)
    f = font(46, "SemiBold", False)
    text_c(d, lines, 1380, f, MUTED, p, dy=(1 - p) * 40, gap=1.35)


def lock(d, cx, cy, s, fill, alpha=1.0):
    d.arc([cx - 0.36 * s, cy - 0.85 * s, cx + 0.36 * s, cy - 0.05 * s], 180, 360, fill=col(fill, alpha), width=int(0.13 * s))
    d.line([cx - 0.36 * s + 0.06 * s, cy - 0.45 * s, cx - 0.36 * s + 0.06 * s, cy - 0.1 * s], fill=col(fill, alpha), width=int(0.13 * s))
    d.line([cx + 0.36 * s - 0.06 * s, cy - 0.45 * s, cx + 0.36 * s - 0.06 * s, cy - 0.1 * s], fill=col(fill, alpha), width=int(0.13 * s))
    d.rounded_rectangle([cx - 0.55 * s, cy - 0.15 * s, cx + 0.55 * s, cy + 0.7 * s], int(0.14 * s), fill=col(fill, alpha))
    d.ellipse([cx - 0.1 * s, cy + 0.12 * s, cx + 0.1 * s, cy + 0.32 * s], fill=col(BG1, alpha))


# ---------- scenes ----------
def intro(d, t):
    p = a(t, 0.1, 0.6)
    f = font(330)
    text_c(d, ["3"], 430, f, ACC, p, dy=(1 - p) * 80)
    p2 = a(t, 0.45, 0.6)
    text_c(d, ["PHONE", "TRICKS"], 830, font(170), WHITE, p2, dy=(1 - p2) * 60, gap=1.05)
    p3 = a(t, 1.0, 0.6)
    text_c(d, ["you'll use every day"], 1250, font(64, "SemiBold", False), MUTED, p3, dy=(1 - p3) * 40)


def head(d, t, n, lines):
    p = a(t, 0.05)
    badge(d, f"TRICK {n} OF 3", 250, p, dy=(1 - p) * -30)
    p2 = a(t, 0.25)
    text_c(d, lines, 380, font(86), WHITE, p2, dy=(1 - p2) * 50, gap=1.12)


def tip1(d, t):
    head(d, t, 1, ["Move the cursor", "with your spacebar"])
    p = a(t, 0.7)
    if p <= 0:
        return
    oy = (1 - p) * 60
    # message box
    d.rounded_rectangle([110, 700 + oy, 970, 830 + oy], 30, fill=col(CARD, p))
    f = font(56, "SemiBold", False)
    msg = "See you at 5 pm today"
    d.text((150, 730 + oy), msg, font=f, fill=col(WHITE, p))
    # slide progress: loops back and forth
    s = 0.0
    if t > 1.8:
        s = 0.5 - 0.5 * math.cos(min(t - 1.8, 4.4) / 4.4 * 2 * math.pi)
    full = d.textlength(msg, font=f)
    mid = d.textlength("See you at ", font=f)
    cx = 150 + full + 6 - (full - mid + 6) * s
    if int(t * 2.5) % 2 == 0 or 0.02 < s:
        d.rectangle([cx, 728 + oy, cx + 6, 800 + oy], fill=col(ACC, p))
    # keyboard
    ky = 900 + oy
    d.rounded_rectangle([90, ky, 990, ky + 400], 36, fill=col(CARD, p))
    for r, n in enumerate([10, 9, 7]):
        kw, g = 72, 14
        tot = n * kw + (n - 1) * g
        x0 = (W - tot) / 2
        for i in range(n):
            x = x0 + i * (kw + g)
            y = ky + 28 + r * 88
            d.rounded_rectangle([x, y, x + kw, y + 72], 14, fill=col(KEY, p))
    sy = ky + 28 + 3 * 88
    d.rounded_rectangle([280, sy, 800, sy + 76], 16, fill=col(ACC, p))
    d.rounded_rectangle([130, sy, 262, sy + 76], 16, fill=col(KEY, p))
    d.rounded_rectangle([818, sy, 950, sy + 76], 16, fill=col(KEY, p))
    # finger
    fp = a(t, 1.3)
    if fp > 0:
        fx = 720 - 360 * s
        fy = sy + 38
        d.ellipse([fx - 62, fy - 62, fx + 62, fy + 62], fill=(255, 255, 255, int(70 * fp)))
        d.ellipse([fx - 40, fy - 40, fx + 40, fy + 40], fill=(255, 255, 255, int(235 * fp)))
    caption(d, ["Slide your finger along the spacebar.", "On iPhone, press and hold it first."], t, 1.6)


def qr_cells():
    rnd = random.Random(7)
    n = 21
    g = [[rnd.random() < 0.5 for _ in range(n)] for _ in range(n)]
    for (ox, oy) in [(0, 0), (n - 7, 0), (0, n - 7)]:
        for y in range(-1, 8):
            for x in range(-1, 8):
                xx, yy = ox + x, oy + y
                if 0 <= xx < n and 0 <= yy < n:
                    edge = x in (0, 6) or y in (0, 6)
                    core = 2 <= x <= 4 and 2 <= y <= 4
                    inside = 0 <= x <= 6 and 0 <= y <= 6
                    g[yy][xx] = inside and (edge or core)
    return g


QR = qr_cells()


def tip2(d, t):
    head(d, t, 2, ["Share Wi-Fi without", "saying the password"])
    p = a(t, 0.7)
    if p <= 0:
        return
    oy = (1 - p) * 60
    size = 560
    x0, y0 = (W - size) / 2, 690 + oy
    d.rounded_rectangle([x0 - 50, y0 - 50, x0 + size + 50, y0 + size + 50], 44, fill=col(WHITE, p))
    n = 21
    c = size / n
    for y in range(n):
        for x in range(n):
            if QR[y][x]:
                # reveal diagonally
                rp = a(t, 0.9 + (x + y) * 0.025, 0.3)
                if rp > 0:
                    d.rectangle([x0 + x * c, y0 + y * c, x0 + (x + 1) * c - 1, y0 + (y + 1) * c - 1], fill=col((12, 18, 40), p * rp))
    # scan line
    if 2.6 < t < 6.2:
        k = ((t - 2.6) % 1.8) / 1.8
        yy = y0 + size * (0.5 - 0.5 * math.cos(k * 2 * math.pi))
        d.rounded_rectangle([x0 - 30, yy - 5, x0 + size + 30, yy + 5], 5, fill=col(ACC, 0.95))
    caption(d, ["On Android: open Wi-Fi settings, tap", "your network, then Share. They scan it."], t, 1.6)


def tip3(d, t):
    head(d, t, 3, ["Lock your phone", "to just one app"])
    p = a(t, 0.7)
    if p <= 0:
        return
    oy = (1 - p) * 60
    px0, py0, pw, ph = 330, 660 + oy, 420, 660
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], 60, fill=col((6, 9, 22), p), outline=col(MUTED, p), width=6)
    d.rounded_rectangle([px0 + 150, py0 + 22, px0 + pw - 150, py0 + 44], 11, fill=col(KEY, p))
    # app screen: photo-style tiles
    tiles = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
    cols = [(96, 165, 250), (244, 114, 182), (250, 204, 21), (129, 140, 248), (45, 212, 191), (251, 146, 60)]
    for i, (cx, cy) in enumerate(tiles):
        tp = a(t, 0.9 + i * 0.08, 0.4)
        x = px0 + 36 + cx * 178
        y = py0 + 80 + cy * 178
        d.rounded_rectangle([x, y, x + 164, y + 164], 22, fill=col(cols[i], p * tp))
    # lock badge pops in
    lp = a(t, 2.2, 0.5)
    if lp > 0:
        r = 130 * (0.6 + 0.4 * lp)
        cx, cy = px0 + pw - 10, py0 + ph - 120
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col(ACC, lp))
        lock(d, cx, cy + 4, 0.8 * r, (8, 30, 16), lp)
    caption(d, ["Turn on App pinning in Settings >", "Security, then pin the app you hand over."], t, 1.6)


def outro(d, t):
    p = a(t, 0.1, 0.6)
    text_c(d, ["Which trick", "was new to you?"], 620, font(118), WHITE, p, dy=(1 - p) * 60, gap=1.12)
    p2 = a(t, 0.7, 0.6)
    f = font(54, "Bold", False)
    label = "Follow for more tech tips"
    w = d.textlength(label, font=f) + 110
    x = (W - w) / 2
    y = 1010 + (1 - p2) * 40
    d.rounded_rectangle([x, y, x + w, y + 120], 60, fill=col(ACC, p2))
    d.text((x + 55, y + 28), label, font=f, fill=col((8, 30, 16), p2))


SCENES = [("intro", intro, 3.5), ("tip1", tip1, 7.5), ("tip2", tip2, 7.5), ("tip3", tip3, 7.5), ("outro", outro, 3.5)]


def frame(fn, t, dur):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer), t)
    im = BG.copy()
    im.paste(layer, (0, 0), layer)
    # short fade in/out per scene (inside each file)
    f = min(1.0, t / 0.25, (dur - t) / 0.25)
    if f < 1.0:
        im = Image.blend(Image.new("RGB", (W, H), BG1), im, max(0.0, f))
    return im


def stills(out):
    for name, fn, dur in SCENES:
        frame(fn, dur * 0.72, dur).save(f"{out}/{name}.png")


def render(out):
    files = []
    for name, fn, dur in SCENES:
        tmp, final = f"{out}/{name}.tmp.mp4", f"{out}/{name}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                              "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            p.stdin.write(frame(fn, i / FPS, dur).tobytes())
        p.stdin.close()
        if p.wait() != 0:
            sys.exit(f"ffmpeg failed on {name}")
        os.rename(tmp, final)
        files.append(final)
    with open(f"{out}/list.txt", "w") as fh:
        fh.writelines(f"file '{f}'\n" for f in files)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt",
                           "-c", "copy", "-movflags", "+faststart", f"{out}/3-phone-tricks-short.mp4"])


if __name__ == "__main__":
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    stills(out) if sys.argv[1] == "stills" else render(out)
