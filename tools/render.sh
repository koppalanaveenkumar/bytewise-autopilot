#!/bin/bash
# Full render in two parallel halves + voice. Usage: bash render.sh WORKDIR OUT.mp4
set -e
BW=$(cd "$(dirname "$0")/.." && pwd); W=$1; OUT=$2
N=$(python3 -c "import json;print(round(json.load(open('$W/news.json'))['end']*30))"); H=$((N/2))
python3 "$BW/tools/rec.py" "$W" 8801 video 0 $H "$W/pA.mp4" > "$W/recA.log" 2>&1 &
python3 "$BW/tools/rec.py" "$W" 8802 video $H $N "$W/pB.mp4" > "$W/recB.log" 2>&1 &
wait
grep -i "error" "$W"/rec?.log && exit 1 || true
printf "file 'pA.mp4'\nfile 'pB.mp4'\n" > "$W/parts.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$W/parts.txt" -c copy "$W/v.mp4"
ffmpeg -v error -y -i "$W/v.mp4" -i "$W/voice.wav" -map 0:v -map 1:a -c:v copy -af "apad,loudnorm=I=-14:TP=-1.5:LRA=7" -ar 48000 -c:a aac -b:a 192k -shortest "$OUT"
rm -f "$W/v.mp4" "$W/pA.mp4" "$W/pB.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
