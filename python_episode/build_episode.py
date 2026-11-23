"""Build Python for Beginners Episode 11 at 1440p from the Kokoro narration timings."""
import sys, os, json, re, subprocess
from multiprocessing import Pool
HERE = os.getcwd()  # work dir: el_script.txt, tts_timing.json, voice.wav, scenes_epN.py
KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, KIT)
os.makedirs(f"{HERE}/out", exist_ok=True)
import look2x as L
import importlib
SC = importlib.import_module(os.environ.get("SCENES", "scenes_ep11"))
from PIL import Image

OUT = f"{HERE}/out"
TM = json.load(open(f"{HERE}/tts_timing.json"))
GROUPS = SC.GROUPS
TAIL = 4.0
PALS = [(L.YELLOW, L.BLUE, L.ACC), (L.ORANGE, L.RED, L.PURPLE), (L.YELLOW, L.PURPLE, L.ACC), (L.BLUE, L.PURPLE, L.ACC), (L.YELLOW, L.RED, L.PURPLE),
        (L.ACC, L.BLUE, L.PURPLE), (L.PURPLE, L.ACC, L.BLUE), (L.YELLOW, L.BLUE, L.PURPLE), (L.ORANGE, L.BLUE, L.ACC), (L.ORANGE, L.PURPLE, L.RED),
        (L.BLUE, L.ACC, L.PURPLE), (L.ACC, L.YELLOW, L.BLUE), (L.ACC, L.ORANGE, L.BLUE), (L.ACC, L.YELLOW, L.PURPLE), (L.YELLOW, L.ORANGE, L.BLUE),
        (L.BLUE, L.ACC, L.PURPLE), (L.ORANGE, L.ACC, L.BLUE), (L.YELLOW, L.BLUE, L.ACC)]
starts, beats = [], []
for gi, g in enumerate(GROUPS):
    ss = [s for pi in g for s in TM["para_starts"][pi]]
    st = 0.0 if gi == 0 else ss[0] - 0.275
    starts.append(st)
    beats.append([round(s - st, 3) for s in ss])
fr = [round(s * 30) for s in starts] + [round((TM["end"] + TAIL) * 30)]
TOTAL = fr[-1] / 30
plan = [(f"k{i + 1:02d}", SC.CHAPTERS[i], PALS[i], (fr[i + 1] - fr[i]) / 30, beats[i], fr[i] / 30) for i in range(len(GROUPS))]


def scene(i):
    sid, chap, pal, D, B, st = plan[i]
    return L.Scene(sid, chap, getattr(SC, sid), pal, D, B, st, TOTAL)


def render(i):
    sc = scene(i)
    tmp, final = f"{OUT}/{sc.sid}.tmp.mp4", f"{OUT}/{sc.sid}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L.PW}x{L.PH}",
                          "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-tune", "animation",
                          "-pix_fmt", "yuv420p", "-threads", "1", tmp], stdin=subprocess.PIPE)
    for f in range(round(sc.D * 30)):
        p.stdin.write(L.frame(sc, f / 30).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f"ffmpeg failed {sc.sid}")
    os.rename(tmp, final)
    return sc.sid


def chapters():
    seen, outl = set(), []
    for sid, chap, pal, D, B, st in plan:
        if chap not in seen:
            seen.add(chap); outl.append(f"{int(st // 60)}:{int(st % 60):02d} {chap}")
    return outl


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1]
    if mode == "frames":  # frames sid:t ...
        tiles = []
        for arg in sys.argv[2:]:
            sid, tt = arg.split(":")
            i = [p[0] for p in plan].index(sid)
            tiles.append(L.frame(scene(i), float(tt)))
        tiles[0].save(f"{OUT}/frame_full.png")
        cols = 3
        sh = Image.new("RGB", (640 * cols, 360 * ((len(tiles) + cols - 1) // cols)))
        for k, tl in enumerate(tiles): sh.paste(tl.resize((640, 360)), (640 * (k % cols), 360 * (k // cols)))
        sh.save(f"{OUT}/sheet.png")
    elif mode == "render":
        ids = sys.argv[2:]
        todo = [i for i, pl in enumerate(plan) if (not ids or pl[0] in ids) and not os.path.exists(f"{OUT}/{pl[0]}.mp4")]
        todo.sort(key=lambda i: -plan[i][3])
        with Pool(2) as pool:
            for sid in pool.imap_unordered(render, todo): print("done", sid, flush=True)
    elif mode == "join":
        with open(f"{OUT}/list.txt", "w") as fh:
            for pl in plan: fh.write(f"file '{OUT}/{pl[0]}.mp4'\n")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt", "-c", "copy", f"{OUT}/video.mp4"])
        final = os.environ.get("OUTNAME", f"{OUT}/episode.mp4")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/video.mp4", "-i", f"{HERE}/voice.wav",
                               "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                               "-af", "loudnorm=I=-15:TP=-1.5:LRA=9,apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                               "-shortest", "-movflags", "+faststart", final + ".tmp.mp4"])
        os.rename(final + ".tmp.mp4", final)
        print("\n".join(chapters())); print("total", round(TOTAL, 2))
    elif mode == "plan":
        for sid, chap, pal, D, B, st in plan: print(sid, chap, round(st, 2), round(D, 2), B)
        print("\n".join(chapters())); print("total", TOTAL)
