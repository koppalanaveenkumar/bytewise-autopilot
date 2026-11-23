"""Assemble the page: python3 build_page.py WORKDIR scenes.js [episode]  -> WORKDIR/index.html (+ links to fonts, badge, three.js).
Add "episode" as a third argument for the 1920x1080 Python episode engine (then film with BW_SIZE=1920x1080)."""
import sys, os
BW = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); W, scenes = sys.argv[1], sys.argv[2]
HEAD = "episode_head.html" if len(sys.argv) > 3 and sys.argv[3] == "episode" else "head.html"
open(f"{W}/index.html", "w").write(open(f"{BW}/engine/{HEAD}").read() + open(f"{BW}/engine/motion.js").read() + "\n" + open(scenes).read() + "\n</script>\n</body></html>\n")
for f in ["node_modules", "anton.ttf", "inter.otf", "mono.ttf", "badge.png"]:
    src, dst = f"{BW}/engine/{f}" if f == "node_modules" else f"{BW}/assets/{f}", f"{W}/{f}"
    if not os.path.exists(dst): os.symlink(src, dst)
print("built", f"{W}/index.html")
