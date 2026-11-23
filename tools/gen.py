"""Kokoro narration (voice am_puck). Run inside a work dir with el_script.txt (paragraphs split by blank lines)
and optional say.json ({"written": "spoken"} pronunciation fixes). Writes voice_raw.wav, tts_timing.json, voice.wav."""
import re, json, subprocess, os, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
BW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
k = Kokoro(f"{BW}/kokoro/kokoro-v1.0.onnx", f"{BW}/kokoro/voices-v1.0.bin")
VOICE, SPEED, GAP, PGAP = "am_puck", 1.0, 0.22, 0.35
paras = [p for p in open("el_script.txt").read().strip().split("\n\n")]
SAY = json.load(open("say.json")) if os.path.exists("say.json") else {}
def say(s):
    for a, b in SAY.items(): s = s.replace(a, b)
    return s
def trim(x, sr):
    nz = np.where(np.abs(x) > 0.01)[0]
    return x[max(0, nz[0] - int(0.02 * sr)): nz[-1] + int(0.06 * sr)]
audio, t, sr = [], 0.25, 24000
audio.append(np.zeros(int(0.25 * sr))); para_sent_starts = []
for pi, p in enumerate(paras):
    sents = re.split(r'(?<=[.!?])\s+', p); singles = []
    for s in sents:
        x, sr = k.create(say(s), voice=VOICE, speed=SPEED, lang="en-us"); singles.append(len(trim(x, sr)) / sr)
    full, sr = k.create(say(p), voice=VOICE, speed=SPEED, lang="en-us"); full = trim(full, sr)
    sf.write("/tmp/p.wav", full, sr); tot = len(full) / sr
    err = subprocess.run(["ffmpeg", "-i", "/tmp/p.wav", "-af", "silencedetect=noise=-35dB:d=0.06", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", err)]; en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", err)]
    sil = [(a + b) / 2 for a, b in zip(st, en) if a > 0.15 and b < tot - 0.1]
    cum = np.cumsum(singles)[:-1] * tot / sum(singles); pieces, prev, shift, rel = [], 0, 0.0, [0.0]
    for c in cum:
        near = min(sil, key=lambda v: abs(v - c)) if sil else None; real = near is not None and abs(near - c) < 0.45
        cut = near if real else float(c); i = int(cut * sr); pieces.append(full[prev:i])
        if real: pieces.append(np.zeros(int(GAP * sr), dtype=full.dtype)); shift += GAP
        rel.append(round(cut + shift, 3)); prev = i
    pieces.append(full[prev:]); seg = np.concatenate(pieces)
    para_sent_starts.append([t + r for r in rel]); audio.append(seg); t += len(seg) / sr
    audio.append(np.zeros(int(PGAP * sr))); t += PGAP; print(pi + 1, round(t, 1), flush=True)
sf.write("voice_raw.wav", np.concatenate(audio), sr)
json.dump({"para_starts": para_sent_starts, "end": t - PGAP}, open("tts_timing.json", "w"))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "voice_raw.wav", "-af", "highpass=f=70,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.5:g=2,deesser=i=0.3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2", "-ar", "48000", "-ac", "1", "voice.wav"], check=True)
