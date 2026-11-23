"""Word timings for the page. Run in the work dir after gen.py. Writes news.json (words, chunks, P, end) next to it."""
import re, json
TM = json.load(open("tts_timing.json")); paras = open("el_script.txt").read().strip().split("\n\n")
WORDS, starts = [], TM["para_starts"]
flat = [(pi, si, s) for pi, p in enumerate(starts) for si, s in enumerate(p)]
for k, (pi, si, s0) in enumerate(flat):
    sent = re.split(r'(?<=[.!?])\s+', paras[pi])[si]
    nxt = flat[k + 1][2] if k + 1 < len(flat) else TM["end"]
    gap = 0.22 if (k + 1 < len(flat) and flat[k + 1][0] == pi) else 0.35
    e0 = nxt - gap if k + 1 < len(flat) else TM["end"]
    ws = sent.split(); wt = [len(w) + 2 + (3 if w[-1] in ",.!?" else 0) for w in ws]; tot = sum(wt); t = s0
    for w, x in zip(ws, wt):
        d = (e0 - s0) * x / tot; WORDS.append((round(t, 3), round(t + d, 3), w, pi)); t += d
CHUNKS, cur = [], []
for wd in WORDS:
    cur.append(wd)
    if len(cur) == 3 or wd[2][-1] in ",.!?": CHUNKS.append(cur); cur = []
if cur: CHUNKS.append(cur)
json.dump({"words": WORDS, "chunks": CHUNKS, "P": starts, "end": TM["end"] + 1.0, "EV": {}}, open("news.json", "w"))
print("words", len(WORDS), "end", round(TM["end"] + 1.0, 2), "frames", round((TM["end"] + 1.0) * 30))
