"""Film the page. stills: python3 rec.py WORKDIR PORT stills 0 2.5 10 ... -> /tmp/nw_<t>.jpg
video: python3 rec.py WORKDIR PORT video F0 F1 OUT.mp4 (frames F0..F1-1 at 30 fps). Run two halves in parallel on 2 CPUs."""
import sys, subprocess, http.server, threading, functools, shutil, os
from playwright.sync_api import sync_playwright
W, port, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=W))
threading.Thread(target=srv.serve_forever, daemon=True).start()
CH = shutil.which("google-chrome") or shutil.which("chromium")
with sync_playwright() as p:
    kw = {"executable_path": CH} if CH else {}
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"], **kw)
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.on("pageerror", lambda e: print("pageerror:", e, flush=True))
    pg.goto(f"http://127.0.0.1:{port}/index.html"); pg.wait_for_function("window.READY === true", timeout=180000)
    if mode == "stills":
        for t in sys.argv[4:]:
            pg.evaluate(f"renderAt({t})"); pg.screenshot(path=f"/tmp/nw_{t}.jpg", type="jpeg", quality=80)
    elif mode == "cover":
        pg.evaluate("renderCover()"); pg.screenshot(path=sys.argv[4])
    else:
        f0, f1, out = int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(f0, f1):
            pg.evaluate(f"renderAt({i / 30})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
            if i % 150 == 0: print(i, f1, flush=True)
        ff.stdin.close(); ff.wait(); os.replace(out + ".tmp.mp4", out)
    b.close()
