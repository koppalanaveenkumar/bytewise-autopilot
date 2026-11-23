#!/bin/bash
# High-quality encode that fits GitHub's 100 MB limit, then put it (and the thumbnail) on a public media branch.
# Usage: bash publish_prep.sh VIDEO.mp4 THUMB.png SLOT   (SLOT = news | short | epA | epB)
# Prints the public video and thumbnail URLs for vidiq_video_upload / vidiq_upload_image.
# Needs push access in this session first: call add_repo(owner="koppalanaveenkumar", repo="bytewise-autopilot", access="push").
set -e
IN=$1; TH=$2; SLOT=$3; REPO=https://github.com/koppalanaveenkumar/bytewise-autopilot
D=$(mktemp -d); DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$IN")
CAP=12000; [ "$H" -ge 1400 ] && CAP=16000          # kbps ceiling: 12 Mbps vertical 1080p, 16 Mbps 1440p
VB=$(python3 -c "print(min($CAP, int((92*8*1024)/$DUR - 192)))")
cd "$D"
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -b:v ${VB}k -pass 1 -an -f mp4 /dev/null
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -b:v ${VB}k -pass 2 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart video.mp4
cp "$TH" thumb.png 2>/dev/null || true
SZ=$(stat -c %s video.mp4); [ "$SZ" -lt 99000000 ] || { echo "too big: $SZ"; exit 1; }
git init -q && git checkout -q --orphan media-$SLOT && git add video.mp4 thumb.png 2>/dev/null; git add video.mp4
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $SLOT $(date -u +%F)"
git remote add origin $REPO && git push -q -f origin media-$SLOT
echo "bitrate ${VB}k size $SZ"
echo "VIDEO_URL=https://raw.githubusercontent.com/koppalanaveenkumar/bytewise-autopilot/media-$SLOT/video.mp4"
echo "THUMB_URL=https://raw.githubusercontent.com/koppalanaveenkumar/bytewise-autopilot/media-$SLOT/thumb.png"
