import json, re
T = json.load(open("tts_timing.json"))
paras = open("el_script.txt").read().strip().split("\n\n")
fix = []
sents = []
for p, st in zip(paras, T["para_starts"]):
    for s, t0 in zip(re.split(r'(?<=[.!?])\s+', p), st): sents.append([t0, s])
for i, sn in enumerate(sents):
    sn.append((sents[i + 1][0] - 0.2) if i + 1 < len(sents) else T["end"])
def ts(x): h, r = divmod(x, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
def wrap(s, n=42):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur); return lines
cues = []
for t0, s, t1 in sents:
    for a_, b_ in fix: s = s.replace(a_, b_)
    lines = wrap(s)
    chunks = ["\n".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
    tot = sum(len(c) for c in chunks); t = t0
    for c in chunks:
        d = (t1 - t0) * len(c) / tot
        cues.append((t, t + d - 0.02, c)); t += d
with open(__import__("sys").argv[1], "w") as f:
    for i, (a_, b_, c) in enumerate(cues, 1): f.write(f"{i}\n{ts(a_)} --> {ts(b_)}\n{c}\n\n")
print(len(cues))
