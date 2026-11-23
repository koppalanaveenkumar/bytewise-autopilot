# Pixabay video search. Run in work dir: PIXABAY_KEY=... python3 search.py "query one" "query two". Makes px/sheet_*.jpg contact sheets + px/res.json
import json, sys, urllib.request, urllib.parse, os
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["PIXABAY_KEY"]
os.makedirs("px/thumbs", exist_ok=True)
Q = sys.argv[1:]
res = json.load(open("px/res.json")) if os.path.exists("px/res.json") else {}
def get(q):
    u = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": KEY, "q": q, "per_page": 30, "safesearch": "true"})
    hits = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))["hits"]
    out = []
    for h in hits:
        v = h["videos"]
        m = v.get("medium") or v.get("large")
        vert = m["height"] > m["width"]
        out.append(dict(id=h["id"], vert=vert, dur=h["duration"], tags=h["tags"], user=h["user"], page=h["pageURL"],
                        url=m["url"], w=m["width"], h=m["height"], large=v["large"]["url"], lw=v["large"]["width"], lh=v["large"]["height"], thumb=m["thumbnail"]))
    out.sort(key=lambda x: (not x["vert"]))
    return q, out[:8]
with ThreadPoolExecutor(3) as ex:
    for q, out in ex.map(get, Q): res[q] = out
json.dump(res, open("px/res.json", "w"), indent=1)
def th(c):
    p = f"px/thumbs/{c['id']}.jpg"
    if not os.path.exists(p): open(p, "wb").write(urllib.request.urlopen(urllib.request.Request(c["thumb"], headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())
    return p
for q in Q:
    cs = res[q]
    with ThreadPoolExecutor(8) as ex: paths = list(ex.map(th, cs))
    sheet = Image.new("RGB", (8 * 240, 300), (20, 20, 20)); d = ImageDraw.Draw(sheet)
    for i, (c, p) in enumerate(zip(cs, paths)):
        im = Image.open(p).convert("RGB"); im.thumbnail((236, 260)); sheet.paste(im, (i * 240 + 2, 0))
        d.text((i * 240 + 4, 268), f"{i}:{'V' if c['vert'] else 'H'} {c['w']}x{c['h']} {c['dur']}s", fill=(255, 255, 0))
    sheet.save(f"px/sheet_{q.replace(' ', '_')}.jpg")
    print(q, len(cs), sum(c["vert"] for c in cs))
