"""Assemble the page: python3 build_page.py WORKDIR scenes.js  -> WORKDIR/index.html (+ links to fonts, badge, three.js)."""
import sys, os
BW = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); W, scenes = sys.argv[1], sys.argv[2]
open(f"{W}/index.html", "w").write(open(f"{BW}/engine/head.html").read() + open(scenes).read() + "\n</script>\n</body></html>\n")
for f in ["node_modules", "anton.ttf", "inter.otf", "mono.ttf", "badge.png"]:
    src, dst = f"{BW}/engine/{f}" if f == "node_modules" else f"{BW}/assets/{f}", f"{W}/{f}"
    if not os.path.exists(dst): os.symlink(src, dst)
print("built", f"{W}/index.html")
