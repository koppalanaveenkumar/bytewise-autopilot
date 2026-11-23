#!/bin/bash
# One-time setup in a fresh workspace. Usage: bash setup.sh   (run from the pipeline folder)
set -e
BW=$(cd "$(dirname "$0")" && pwd)
pip install --break-system-packages -q kokoro-onnx soundfile playwright pillow numpy 2>&1 | tail -1
mkdir -p "$BW/kokoro"
[ -f "$BW/kokoro/kokoro-v1.0.onnx" ] || curl -sL -o "$BW/kokoro/kokoro-v1.0.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f "$BW/kokoro/voices-v1.0.bin" ] || curl -sL -o "$BW/kokoro/voices-v1.0.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd "$BW/engine" && [ -d node_modules/three ] || npm install --silent three@0.170.0 >/dev/null
cp -n "$BW"/assets/* "$BW/engine/" 2>/dev/null || true
CH=$(which google-chrome || which chromium || true)
if [ -z "$CH" ]; then python3 -m playwright install chromium >/dev/null 2>&1 || echo "WARN: no chrome; install one"; fi
echo "setup done. chrome: ${CH:-playwright-chromium}"
