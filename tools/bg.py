"""Real-footage background, one clip per story. Run in the work dir after search.py.
plan.json: {"picks": {"s0": ["query", index], ...}, "segments": [["s0", 0.0, 11.6], ["s1a", 11.6, 19.6], ...]}
segment times are seconds on the voice timeline (cover 0 to the end). Downloads clips, builds bg/00001.jpg... (frame f -> file f+1)
and writes bgFrames into news.json. Times inside a clip start at its beginning; add a 4th value to start later in the clip."""
import json, subprocess, os, urllib.request, glob
from concurrent.futures import ThreadPoolExecutor
plan = json.load(open("plan.json")); res = json.load(open("px/res.json")); os.makedirs("clips", exist_ok=True); os.makedirs("bg", exist_ok=True)
info = {}
def dl(k):
    q, i = plan["picks"][k]; c = res[q][i]; url = c["large"] if max(c["lw"], c["lh"]) <= 2730 else c["url"]; p = f"clips/{k}.mp4"
    if not os.path.exists(p): open(p, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read())
    return k, c["dur"]
with ThreadPoolExecutor(4) as ex:
    for k, d in ex.map(dl, plan["picks"]): info[k] = d
lst = []
for n, seg in enumerate(plan["segments"]):
    name, a, b = seg[:3]; off = seg[3] if len(seg) > 3 else 0
    cnt = round(b * 30) - round(a * 30); f = max(1.0, (cnt / 30) / max(.5, info[name] - off) * 1.03)
    out = f"clips/seg{n:03d}.mp4"
    vf = f"setpts={f:.3f}*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=saturation=0.92,tpad=stop_mode=clone:stop_duration=3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(off), "-i", f"clips/{name}.mp4", "-vf", vf, "-frames:v", str(cnt), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
    lst.append(f"file '{os.path.basename(out)}'")
open("clips/segs.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "clips/segs.txt", "-c", "copy", "clips/bg.mp4"], check=True)
for f in glob.glob("bg/*.jpg"): os.remove(f)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "clips/bg.mp4", "-q:v", "4", "bg/%05d.jpg"], check=True)
for f in glob.glob("clips/seg*.mp4"): os.remove(f)
n = len(glob.glob("bg/*.jpg")); d = json.load(open("news.json")); d["bgFrames"] = n; json.dump(d, open("news.json", "w"))
print("bg frames", n, "clips", {k: plan["picks"][k] for k in plan["picks"]})
