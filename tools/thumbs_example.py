from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os; A = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/assets/"; W, H = 1080, 1920
def cover(p, fx=.5, fy=.5):
    im = Image.open(p).convert("RGB"); s = max(W / im.width, H / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy); return im.crop((x, y, x + W, y + H))
def grade(im, c=1.25, b=.85, sat=1.1): return ImageEnhance.Color(ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(c)).enhance(b)).enhance(sat)
def grad(im, top=1050, a=235, bottom=True):
    g = Image.new("L", (1, H)); 
    for y in range(H): g.putpixel((0, y), int(a * max(0, 1 - y / top) ** 1.2) if y < top else (int(200 * ((y - 1550) / 370) ** 1.5) if bottom and y > 1550 else 0))
    g = g.resize((W, H)); dark = Image.new("RGB", (W, H), (7, 10, 20)); return Image.composite(dark, im, g)
def glowtext(im, xy, s, size, fill, glow, font="anton.ttf", spread=26):
    f = ImageFont.truetype(A + font, size); lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=f, fill=glow); lay = lay.filter(ImageFilter.GaussianBlur(spread)); im.paste(lay, (0, 0), lay)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 8, xy[1] + 10), s, font=f, fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(6)); im.paste(sh, (0, 0), sh)
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill)
def pill(im, xy, s, bg, fg, size=46):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(A + "inter.otf", size); w = d.textlength(s, font=f); x, y = xy
    d.rounded_rectangle((x, y, x + w + 64, y + size + 40), radius=(size + 40) // 2, fill=bg); d.text((x + 32, y + 16), s, font=f, fill=fg)
def badge(im): b = Image.open(A + "badge.png").convert("RGBA"); im.paste(b, (34, 34), b)

# A: real chalkboard + AI CRACKED 1859
im = grade(cover("/tmp/th_s1a.jpg", .5, .62), 1.2, .9); im = grad(im, 1000, 245).convert("RGB")
d = ImageDraw.Draw(im, "RGBA")
# chalk-style glowing formula on the board
lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); f = ImageFont.truetype(A + "mono.ttf", 96)
ld.text((520, 1200), "ζ(s) = 0", font=f, fill=(255, 210, 58, 255)); lay2 = lay.filter(ImageFilter.GaussianBlur(14)); im.paste(lay2, (0, 0), lay2); im.paste(lay, (0, 0), lay)
d = ImageDraw.Draw(im, "RGBA"); d.ellipse((470, 1140, 1010, 1360), outline=(255, 74, 28, 255), width=12)
badge(im); pill(im, (60, 170), "AI + MATH", (255, 74, 28), "white")
glowtext(im, (50, 270), "AI", 330, "white", (255, 255, 255, 90))
glowtext(im, (50, 600), "CRACKED", 230, (255, 74, 28), (255, 74, 28, 200))
glowtext(im, (50, 850), "1859?", 230, (255, 210, 58), (255, 210, 58, 150))
im.save("out/cover-A-ai-cracked-1859.png")

# B: cyber attack map + PASSWORDS STOLEN
im = grade(cover("/tmp/th_s3b.jpg", .5, .5), 1.35, .8, 1.25); im = grad(im, 1000, 240).convert("RGB")
badge(im); pill(im, (60, 170), "CYBER SECURITY", (229, 56, 59), "white")
glowtext(im, (50, 290), "PASSWORDS", 215, "white", (255, 255, 255, 80))
glowtext(im, (50, 540), "STOLEN", 300, (229, 56, 59), (229, 56, 59, 210))
glowtext(im, (50, 880), "IN HOURS", 170, (255, 210, 58), (255, 210, 58, 140))
im.save("out/cover-B-passwords-stolen.png")
s = Image.new("RGB", (1080, 960)); s.paste(Image.open("out/cover-A-ai-cracked-1859.png").resize((540, 960)), (0, 0)); s.paste(Image.open("out/cover-B-passwords-stolen.png").resize((540, 960)), (540, 0)); s.save("/tmp/thAB.jpg")
