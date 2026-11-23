// ---------------- scenes (Nov 23) ----------------
const RED = "#e5383b", BLU = "#4f7bff";
function icon3(kind, x, y, s, color, alpha = 1) {
  c.save(); c.globalAlpha *= alpha; c.translate(x, y); c.strokeStyle = color; c.fillStyle = color; c.lineWidth = s * .08; c.lineJoin = "round"; c.lineCap = "round";
  if (kind === "key") { c.beginPath(); c.arc(-s * .22, 0, s * .2, 0, 7); c.stroke(); c.beginPath(); c.moveTo(-s * .02, 0); c.lineTo(s * .46, 0); c.moveTo(s * .3, 0); c.lineTo(s * .3, s * .16); c.moveTo(s * .42, 0); c.lineTo(s * .42, s * .13); c.stroke(); }
  if (kind === "plane") { c.rotate(-.2); c.beginPath(); c.moveTo(-s * .5, 0); c.lineTo(s * .5, 0); c.moveTo(-s * .05, 0); c.lineTo(-s * .25, -s * .4); c.moveTo(-s * .05, 0); c.lineTo(-s * .25, s * .4); c.moveTo(-s * .42, 0); c.lineTo(-s * .5, -s * .16); c.moveTo(-s * .42, 0); c.lineTo(-s * .5, s * .16); c.stroke(); }
  if (kind === "bank") { c.beginPath(); c.moveTo(-s * .48, -s * .18); c.lineTo(0, -s * .46); c.lineTo(s * .48, -s * .18); c.closePath(); c.stroke(); for (let k = -2; k <= 2; k++) c.fillRect(k * s * .19 - s * .04, -s * .1, s * .08, s * .42); c.fillRect(-s * .5, s * .36, s, s * .08); }
  if (kind === "mail") { rr(-s * .45, -s * .3, s * .9, s * .6, s * .06, null, color, s * .08); c.beginPath(); c.moveTo(-s * .43, -s * .27); c.lineTo(0, s * .05); c.lineTo(s * .43, -s * .27); c.stroke(); }
  if (kind === "patch") { c.rotate(-.6); rr(-s * .5, -s * .17, s, s * .34, s * .17, null, color, s * .07); for (let a = -1; a <= 1; a += 2) for (let b = -1; b <= 1; b += 2) { c.beginPath(); c.arc(a * s * .06, b * s * .06, s * .025, 0, 7); c.fill(); } }
  if (kind === "brain") { c.beginPath(); c.arc(-s * .15, -s * .08, s * .25, Math.PI * .6, Math.PI * 1.9); c.arc(s * .15, -s * .08, s * .25, Math.PI * 1.1, Math.PI * 2.4); c.stroke(); c.beginPath(); c.moveTo(0, -s * .3); c.lineTo(0, s * .25); c.stroke(); }
  if (kind === "check") { c.beginPath(); c.moveTo(-s * .3, 0); c.lineTo(-s * .08, s * .22); c.lineTo(s * .34, -s * .24); c.stroke(); }
  c.restore();
}
function counterS(s, x, y, size, t, t0, color = ORG, align = "left") { if (t < t0) return; const k = .6 + .4 * back(prog(t, t0, .35)); c.save(); c.translate(x, y); c.scale(k, k); c.shadowColor = "rgba(255,74,28,.55)"; c.shadowBlur = 50; c.font = `${size}px Anton`; c.fillStyle = color; c.textAlign = align; c.fillText(s, 0, 0); c.restore(); }

const TILES = [["1", "AI SOLVES MATH"], ["2", "TESLA AI VIEW"], ["3", "PASSWORD TRAP"], ["4", "US OUTAGES"], ["5", "AMAZON $7B"], ["6", "UBISOFT AI"], ["7", "TO DO SHUTS"]];
const S = [];
const SHOTS = [];  // optional camera shots per scene, e.g. SHOTS[3] = [[0, 1, 540, 960], [2.0, 1.6, 540, 1100], [4.5, 1, 540, 960]]
S[0] = t => {
  const t2 = P[0][1];
  if (t < t2 - .15) {
    // motion from frame 0: real road + AI scan grid, two short lines only
    slam("TESLA'S ROAD", 56, 420, 150, "#fff", t, -1); slam("MADE BY AI.", 56, 580, 150, ORG, t, -1);
    const vx = 540, vy = 900; c.save(); c.strokeStyle = "#5ee7ff"; c.lineWidth = 3; c.shadowColor = "#5ee7ff"; c.shadowBlur = 14; c.globalAlpha = .45;
    for (let k = -6; k <= 6; k++) { c.beginPath(); c.moveTo(vx + k * 8, vy); c.lineTo(vx + k * 260, 1920); c.stroke(); }
    for (let k = 0; k < 10; k++) { const z = ((k / 10) + t * .7) % 1, y = vy + (1920 - vy) * z * z, hw = 60 + 1600 * z * z; c.globalAlpha = .45 * clamp(z * 4); c.beginPath(); c.moveTo(vx - hw, y); c.lineTo(vx + hw, y); c.stroke(); }
    c.restore();
    const sw = (t * .9) % 1, sy = 760 + 760 * sw; c.save(); c.globalAlpha = .5; c.fillStyle = "#5ee7ff"; c.fillRect(120, sy, 840, 4); c.restore();
    const bx = 120, by = 760, bw = 840, bh = 760, L = 70; c.save(); c.strokeStyle = YEL; c.lineWidth = 8;
    [[bx, by, 1, 1], [bx + bw, by, -1, 1], [bx, by + bh, 1, -1], [bx + bw, by + bh, -1, -1]].forEach(([x, y, sx, sy2]) => { c.beginPath(); c.moveTo(x + sx * L, y); c.lineTo(x, y); c.lineTo(x, y + sy2 * L); c.stroke(); });
    c.restore(); txt("● AI VIEW", bx + 20, by + 60, "36px Mono", YEL);
  } else {
    // bridge: one title card, headlines flash over their footage
    slam("TODAY'S TOP", 540, 520, 170, "#fff", t, t2 - .15, "center"); slam("TECH NEWS", 540, 700, 170, ORG, t, t2, "center");
    const tm = t2 - .2, sl = (PS[1] - tm) / 7, k = Math.min(6, Math.max(0, Math.floor((t - tm) / sl))), lt = (t - tm) - k * sl, a = back(clamp(lt / .16));
    c.save(); c.translate(540, 1150); c.scale(a, a); rr(-440, -90, 880, 180, 40, "rgba(7,10,20,.75)", ORG, 5); c.font = "100px Anton"; c.textAlign = "center"; c.fillStyle = "#fff"; c.fillText(TILES[k][1], 0, 36); c.restore();
  }
};
S[1] = t => {
  const t0 = PS[1]; headline("AI HELPS SOLVE", "AN 1859 PUZZLE.", t, t0 + .3, t0 + .6, 135);
  const tNov = W("November", 1), t17 = W("17", 1), tCert = W("certified", 1);
  // panel: critical line with zeros dropping onto it
  const a0 = ease(prog(t, t0 + .2, .5)), cx = 540, top = 600, bot = 1120;
  if (t < t17 - .3) {
    c.save(); c.globalAlpha = a0; rr(80, top - 20, 920, bot - top + 40, 30, "rgba(255,255,255,.04)", "rgba(255,255,255,.15)", 3);
    c.strokeStyle = "rgba(255,255,255,.15)"; c.lineWidth = 2; for (let k = 1; k < 8; k++) { c.beginPath(); c.moveTo(80 + k * 115, top); c.lineTo(80 + k * 115, bot); c.stroke(); }
    c.shadowColor = ORG; c.shadowBlur = 30; c.strokeStyle = ORG; c.lineWidth = 6; c.beginPath(); c.moveTo(cx, top); c.lineTo(cx, top + (bot - top) * ease(prog(t, t0 + .4, .8))); c.stroke(); c.shadowBlur = 0;
    txt("ζ(s) = 0", 120, top + 60, "52px Mono", CREAM); txt("all zeros on ONE line?", 120, bot - 30, "34px Mono", GREY);
    for (let k = 0; k < 14; k++) { const st = t0 + 1 + k * .28, u = ease(prog(t, st, .5)); if (t < st) continue; const yy = top + 40 + k * 32, sx = cx + (k % 2 ? 1 : -1) * 260 * (1 - u);
      c.fillStyle = YEL; c.shadowColor = YEL; c.shadowBlur = 20; c.beginPath(); c.arc(sx, yy, 11, 0, 7); c.fill(); c.shadowBlur = 0; }
    c.restore();
    if (t > tNov - .2) pill("found with help from Claude AI", 540, 1180, t, tNov - .2, "rgba(255,255,255,.1)", CREAM, 38);
  } else {
    // scrolling code wall + 17M counter
    const a = ease(prog(t, t17 - .3, .4)), rc = rand(17); c.save(); c.globalAlpha = a; rr(80, 580, 920, 560, 26, "#0d1222", "rgba(255,255,255,.18)", 3);
    c.beginPath(); c.roundRect(80, 580, 920, 560, 26); c.clip(); c.font = "26px Mono";
    const words = ["theorem", "lemma", "zeta", "have", "exact", "simp", "intro", "apply", "ring", "norm_num", "∀ s,", "→", ":=", "by"];
    for (let r = 0; r < 26; r++) { const yy = 620 + r * 34 - ((t - t17) * 220) % 34; let line = ""; const n = 3 + Math.floor(rc() * 5); for (let k = 0; k < n; k++) line += words[Math.floor(rc() * words.length)] + " "; c.fillStyle = r % 5 === 0 ? ORG : "rgba(243,239,230,.55)"; c.fillText(line, 110 + (r % 3) * 30, yy); }
    c.restore();
    c.save(); c.globalAlpha = a; rr(80, 1180, 920, 0, 0); c.restore();
    counter(17000000, 60, 1300, 150, t, t17 - .1, 1.4); txt("LINES OF CHECKED CODE", 70, 1360, "40px Mono", CREAM, "left", prog(t, t17 + .3, .3));
    if (t > tCert - .3) stamp("CERTIFIED ✓", 540, 860, 130, t, tCert - .2, GRN, -.1);
  }
};
S[2] = t => {
  const t0 = PS[2]; headline("TESLA'S ROAD", "MADE BY AI.", t, t0 + .3, t0 + .6, 150);
  const tRV = W("Reality", 2), tMusk = W("Musk", 2), tDec = W("December", 2);
  const x0 = 90, y0 = 600, w = 900, h = 560, a = ease(prog(t, t0 + .2, .5));
  c.save(); c.globalAlpha = a; rr(x0 - 16, y0 - 16, w + 32, h + 32, 40, "#05070d", "rgba(255,255,255,.25)", 4); c.beginPath(); c.roundRect(x0, y0, w, h, 28); c.clip();
  const real = t > tRV - .2 ? ease(prog(t, tRV - .2, .9)) : 0;
  const g = c.createLinearGradient(0, y0, 0, y0 + h); g.addColorStop(0, real ? `rgba(120,160,220,${.6 * real})` : "#10141f"); g.addColorStop(.45, real ? `rgba(255,190,140,${.35 * real})` : "#10141f"); g.addColorStop(.46, "#1b1f29"); g.addColorStop(1, "#2a2f3a"); c.fillStyle = g; c.fillRect(x0, y0, w, h);
  const hz = y0 + h * .45, vx = x0 + w / 2;
  // buildings
  if (real > 0) for (let k = 0; k < 12; k++) { const side = k % 2 ? 1 : -1, z = ((k * .37 + t * .5) % 1), sc = .2 + z * 1.6, bx = vx + side * (90 + 380 * z * z) , bh = 60 + 160 * sc;
    c.globalAlpha = a * real * clamp(z * 3); c.fillStyle = ["#3b4a66", "#56617a", "#6d5f57"][k % 3]; c.fillRect(bx - 40 * sc, hz - bh, 80 * sc, bh); c.fillStyle = "rgba(255,220,150,.5)"; for (let q = 0; q < 3; q++) c.fillRect(bx - 25 * sc, hz - bh + 20 * sc + q * 30 * sc, 14 * sc, 10 * sc); }
  c.globalAlpha = a;
  // road
  c.fillStyle = real ? "#3a3d45" : "#1f2330"; c.beginPath(); c.moveTo(vx - 30, hz); c.lineTo(vx + 30, hz); c.lineTo(x0 + w + 200, y0 + h); c.lineTo(x0 - 200, y0 + h); c.closePath(); c.fill();
  for (let k = 0; k < 10; k++) { const z = ((k / 10) + t * .9) % 1, yy = hz + (y0 + h - hz) * z * z, ww = 4 + 18 * z * z, hh = 10 + 60 * z * z; c.fillStyle = real ? "#f3efe6" : "rgba(143,176,255,.6)"; c.fillRect(vx - ww / 2, yy, ww, hh); }
  c.strokeStyle = real ? "#f3efe6" : "rgba(143,176,255,.6)"; c.lineWidth = 4; [-1, 1].forEach(sd => { c.beginPath(); c.moveTo(vx + sd * 30, hz); c.lineTo(vx + sd * (w / 2 + 200), y0 + h); c.stroke(); });
  // other cars
  [[-.5, .3], [.45, .62]].forEach(([lx, ph]) => { const z = ((ph + t * .25) % 1), yy = hz + (y0 + h - hz) * z * z, sc = .2 + 1.2 * z * z, xx = vx + lx * 520 * z * z;
    if (real) { rr(xx - 70 * sc, yy - 50 * sc, 140 * sc, 60 * sc, 14 * sc, lx < 0 ? "#c43c3c" : "#d8d8e0"); rr(xx - 50 * sc, yy - 80 * sc, 100 * sc, 36 * sc, 10 * sc, "#222833"); }
    else { c.strokeStyle = "rgba(143,176,255,.8)"; c.lineWidth = 3; c.strokeRect(xx - 70 * sc, yy - 60 * sc, 140 * sc, 70 * sc); } });
  // own car
  const by = y0 + h - 120 + 4 * Math.sin(t * 6); rr(vx - 110, by, 220, 100, 30, real ? "#e8e8ee" : "rgba(143,176,255,.25)", real ? null : "rgba(143,176,255,.9)", 3); rr(vx - 80, by - 40, 160, 60, 20, real ? "#2a3140" : "rgba(143,176,255,.15)", real ? null : "rgba(143,176,255,.9)", 3);
  c.restore();
  txt(real ? "REALITY VIEW" : "OLD VIEW", x0 + 30, y0 + 50, "34px Mono", real ? YEL : GREY, "left", a);
  if (t > tMusk - .2) pill("AI VIDEO · NOT A GAME ENGINE", 540, 1215, t, tMusk - .2, ORG, "#fff", 40);
  if (t > tDec - .2) pill("WIDER RELEASE: DECEMBER", 540, 1345, t, tDec - .2, "rgba(255,255,255,.1)", CREAM, 40);
};
S[3] = t => {
  const t0 = PS[3]; headline("FAKE PASSWORDS", "STOLEN IN HOURS.", t, t0 + .3, W("stolen", 3) - .1, 135);
  const t2m = W("two", 3), tSt = W("stolen", 3), tNext = W("next", 3), tNever = W("Never", 3);
  if (t < tNever - .3) {
    // stream of prompt bubbles with keys
    const rb = rand(31); for (let k = 0; k < 16; k++) { const lane = k % 4, sp = 160 + rb() * 120, ph = rb(); const y = 640 + lane * 140, x = -200 + ((t - t0) * sp + ph * 1400) % 1400;
      const stolen = t > tSt && k % 5 === 2; c.save(); c.translate(x, y + (stolen ? -Math.min(300, (t - tSt) * 400) * (k % 2 ? 1 : -.3) : 0)); rr(0, -38, 220, 76, 24, stolen ? "rgba(229,56,59,.25)" : "rgba(255,255,255,.08)", stolen ? RED : "rgba(255,255,255,.25)", 3);
      icon3("key", 50, 0, 60, stolen ? RED : YEL); c.fillStyle = "rgba(243,239,230,.6)"; c.fillRect(100, -12, 90, 8); c.fillRect(100, 6, 60, 8); c.restore(); }
    if (t > t2m - .2) { c.save(); rr(60, 1190, 960, 150, 30, "rgba(7,10,20,.85)"); c.restore(); counter(2000000, 90, 1285, 110, t, t2m - .1, 1.2); txt("AI PROMPTS WITH FAKE KEYS", 96, 1325, "30px Mono", CREAM, "left", prog(t, t2m + .3, .3)); }
    if (t > tNext - .3) { const a = back(prog(t, tNext - .3, .35)); c.save(); c.translate(540, 1470); c.scale(a, a); rr(-330, -70, 660, 140, 30, RED); txt("USED THE NEXT DAY", 0, 22, "64px Anton", "#fff", "center"); c.restore(); }
  } else {
    const a = back(prog(t, tNever - .3, .4)); c.save(); c.translate(540, 950); c.scale(a, a); rr(-430, -330, 860, 660, 44, "rgba(229,56,59,.1)", RED, 6);
    icon3("key", -10, -110, 260, YEL); c.strokeStyle = RED; c.lineWidth = 22; c.beginPath(); c.arc(0, -110, 170, 0, 7); c.stroke(); c.beginPath(); c.moveTo(-120, -230); c.lineTo(120, 10); c.stroke();
    txt("NEVER PASTE", 0, 160, "96px Anton", "#fff", "center"); txt("PASSWORDS INTO AI", 0, 260, "80px Anton", RED, "center"); c.restore();
  }
};
S[4] = t => {
  const t0 = PS[4]; headline("OUTAGE WEEK.", "NOT A HACK.", t, t0 + .3, W("not", 4) - .1, 150);
  const tGr = W("grounded", 4), tNot = W("not", 4), tSys = W("systems", 4);
  const items = [["mail", "MICROSOFT", W("Microsoft", 4)], ["plane", "FAA FLIGHTS", W("FAA", 4)], ["bank", "BIG BANKS", W("banks", 4)]];
  items.forEach(([ic, lab, st], i) => { const y = 650 + i * 200, a = ease(prog(t, t0 + .3 + i * .1, .4)), down = t > st + .1, bl = down && Math.sin(t * 10) > 0;
    c.save(); c.globalAlpha = a; c.translate((1 - a) * -200 + (down && t < st + .5 ? Math.sin(t * 80) * 8 : 0), 0); rr(80, y - 80, 920, 160, 30, down ? "rgba(229,56,59,.14)" : "rgba(255,255,255,.06)", down ? RED : "rgba(255,255,255,.2)", 4);
    icon3(ic, 180, y, 100, down ? RED : CREAM); txt(lab, 270, y + 22, "60px Anton", "#fff");
    if (down) { rr(760, y - 36, 200, 72, 36, bl ? RED : "#7a1214"); txt("DOWN", 860, y + 14, "700 36px Inter", "#fff", "center"); } c.restore(); });
  if (t > tGr - .2 && t < tNot) pill("FLIGHTS GROUNDED NATIONWIDE", 540, 1290, t, tGr - .2, RED, "#fff", 38);
  if (t > tNot - .1) { stamp("NOT A CYBERATTACK", 540, 860, 96, t, tNot - .1, GRN, -.08); }
  if (t > tSys - .2) { const a = ease(prog(t, tSys - .2, .4)); c.save(); c.globalAlpha = a; rr(80, 1250, 920, 200, 30, "rgba(255,210,58,.1)", YEL, 4);
    c.save(); c.translate(200, 1350); c.rotate(t * 4); c.strokeStyle = YEL; c.lineWidth = 12; c.lineCap = "round"; c.beginPath(); c.arc(0, 0, 50, 0, 4.7); c.stroke(); c.restore();
    txt("RESTARTS FAILED AFTER", 290, 1335, "44px Anton", "#fff"); txt("SECURITY FIXES + UPGRADES", 290, 1395, "44px Anton", YEL); c.restore(); }
};
S[5] = t => {
  const t0 = PS[5]; headline("AMAZON'S", "$7B AI DEAL?", t, t0 + .3, t0 + .6, 160);
  const t7 = W("7", 5), tLive = W("edits", 5), tNov = W("November", 5);
  // two blocks merging
  const m = io(prog(t, t0 + .8, 1.2)); const ax = 200 + 145 * m, dx = 880 - 145 * m;
  [["AMAZON", ax, "#ff9900"], ["DECART", dx, BLU]].forEach(([n, x, col]) => { c.save(); c.translate(x, 700); rr(-175, -80, 350, 160, 30, "rgba(255,255,255,.06)", col, 5); txt(n, 0, 24, "60px Anton", "#fff", "center"); c.restore(); });
  if (m > .95) { const p = .5 + .5 * Math.sin(t * 8); c.save(); c.globalAlpha = p; txt("+", 540, 735, "70px Anton", YEL, "center"); c.restore(); }
  counterS("$7,000,000,000+", 70, 950, 130, t, t7 - .15); if (t > t7 + .3) txt("REPORTED · NOT YET ANNOUNCED", 76, 1010, "30px Mono", GREY);
  if (t > tLive - .3) { const a = ease(prog(t, tLive - .3, .4)); c.save(); c.globalAlpha = a; rr(140, 1060, 800, 330, 26, "#0d1222", "rgba(255,255,255,.25)", 3);
    c.beginPath(); c.roundRect(140, 1060, 800, 330, 26); c.clip(); const sx = 140 + ((t - tLive) * 300) % 800;
    for (let k = 0; k < 16; k++) { const x = 140 + k * 52, hh = 80 + 60 * Math.sin(k * .8 + t * 2); c.fillStyle = x < sx ? (k % 2 ? "#ff7a4a" : "#ffb35a") : (k % 2 ? "#3b4a66" : "#56617a"); c.fillRect(x, 1390 - hh - 40, 48, hh + 40); }
    c.fillStyle = YEL; c.fillRect(sx - 3, 1060, 6, 330); txt("● LIVE", 170, 1105, "30px Mono", RED); txt("AI STYLE: ON", 740, 1105, "30px Mono", YEL); c.restore(); }
  if (t > tNov - .2) pill("MAYBE REVEALED NOV 30", 540, 1440, t, tNov - .2, YEL, "#111", 40);
};
S[6] = t => {
  const t0 = PS[6]; headline("GAME CHARACTERS", "THAT REMEMBER.", t, t0 + .3, W("memory", 6) - .1, 135);
  const tMB = W("Motherbrain", 6), tMem = W("memory", 6), tJobs = W("cut", 6);
  if (t > tMB - .3) { const a = ease(prog(t, tMB - .3, .3)), gl = (t * 17) % 1 > .85 ? 6 : 0; c.save(); c.globalAlpha = a; c.font = "110px Anton"; c.textAlign = "center"; c.fillStyle = BLU; c.fillText("MOTHERBRAIN", 540 - gl, 690); c.fillStyle = ORG; c.fillText("MOTHERBRAIN", 540 + gl, 690); c.fillStyle = "#fff"; c.fillText("MOTHERBRAIN", 540, 690); c.restore();
    txt("UBISOFT'S NEW AI COMPANY", 540, 750, "34px Mono", CREAM, "center", a); }
  if (t > tMem - .4) { const a = ease(prog(t, tMem - .4, .4)); c.save(); c.globalAlpha = a; rr(80, 820, 920, 380, 30, "rgba(7,10,20,.85)", BLU, 4);
    icon3("brain", 180, 930, 110, BLU); txt("MEMORY", 125, 1030, "32px Mono", BLU);
    const line = "Welcome back. You saved my village last time.", n = Math.floor(line.length * prog(t, tMem, 2.2)); c.font = "700 40px Inter"; c.fillStyle = "#fff";
    const ws = line.slice(0, n).split(" "); let l = "", ly = 900; ws.forEach(wd => { if (c.measureText(l + wd).width > 640) { c.fillText(l, 290, ly); l = ""; ly += 56; } l += wd + " "; }); c.fillText(l + ((t * 3) % 1 > .5 ? "▌" : ""), 290, ly);
    for (let k = 0; k < 5; k++) { const f = clamp(prog(t, tMem + .5 + k * .3, .5)); rr(290 + k * 130, 1120, 110, 30, 10, "rgba(255,255,255,.08)"); rr(290 + k * 130, 1120, 110 * f, 30, 10, BLU); }
    c.restore(); }
  if (t > tJobs - .2) pill("after ~200 job cuts in Canada", 540, 1290, t, tJobs - .2, "rgba(255,255,255,.1)", CREAM, 38);
};
S[7] = t => {
  const t0 = PS[7]; headline("MICROSOFT TO DO", "SHUTS DOWN.", t, t0 + .3, t0 + .6, 140);
  const tJun = W("June", 7), tMove = W("tasks", 7), tExp = W("export", 7);
  const tasks = ["Buy groceries", "Finish homework", "Call mom", "Pay electricity bill", "Learn Python"];
  const x0 = 120, y0 = 580; const a = ease(prog(t, t0 + .2, .4)); c.save(); c.globalAlpha = a; rr(x0, y0, 840, 560, 30, "#f8f6f1"); rr(x0, y0, 840, 80, 30, "#2564cf"); c.fillStyle = "#2564cf"; c.fillRect(x0, y0 + 50, 840, 30); txt("My Day", x0 + 40, y0 + 56, "700 40px Inter", "#fff");
  tasks.forEach((s, i) => { const y = y0 + 140 + i * 88; let dy = 0, al = 1; if (t > tMove) { const q = prog(t, tMove + i * .15, .9); dy = 900 * q * q; al = 1 - q; }
    const done = t > t0 + 1 + i * .5; c.save(); c.globalAlpha = a * al; c.translate(0, dy); c.rotate(dy * .0004 * (i % 2 ? 1 : -1));
    c.beginPath(); c.arc(x0 + 60, y, 22, 0, 7); c.lineWidth = 4; c.strokeStyle = "#2564cf"; c.stroke(); if (done) { c.fillStyle = "#2564cf"; c.fill(); icon3("check", x0 + 60, y, 34, "#fff"); }
    txt(s, x0 + 110, y + 14, "700 40px Inter", done ? "#999" : "#222"); if (done) { c.fillStyle = "#999"; c.fillRect(x0 + 110, y, c.measureText ? 0 : 0, 0); } c.restore(); });
  c.restore();
  if (t > tJun - .3) { const a2 = back(prog(t, tJun - .3, .4)); c.save(); c.translate(780, 1260); c.rotate(.06); c.scale(a2, a2); rr(-190, -150, 380, 300, 30, "#fff"); rr(-190, -150, 380, 80, 30, RED); c.fillStyle = RED; c.fillRect(-190, -100, 380, 30);
    txt("JUN 2027", 0, -92, "40px Anton", "#fff", "center"); txt("30", 0, 100, "170px Anton", "#111", "center"); c.restore(); }
  if (t > tMove) txt("TASKS WON'T MOVE BY THEMSELVES", 540, 1500, "48px Anton", RED, "center", prog(t, tMove, .3));
  if (t > tExp - .2) pill("EXPORT OPTION PROMISED", 330, 1360, t, tExp - .2, YEL, "#111", 38);
};
S[8] = t => {
  const t0 = PS[8]; headline("WHICH ONE", "SURPRISED YOU?", t, t0 + .2, t0 + .5, 140);
  const tC = W("Tell", 8), tF = W("follow", 8);
  const rq = rand(8); c.save(); c.font = "90px Anton"; c.textAlign = "center"; for (let k = 0; k < 9; k++) { const x = 120 + rq() * 840, sp = 120 + rq() * 160, y = 1500 - ((t - t0) * sp + rq() * 900) % 1100; c.globalAlpha = .25; c.fillStyle = k % 2 ? ORG : CREAM; c.fillText("?", x + 30 * Math.sin(t * 2 + k), y); } c.restore();
  const a = back(prog(t, tC - .2, .4)); c.save(); c.translate(540, 900 + 18 * Math.sin(t * 3)); c.rotate(.05 * Math.sin(t * 2.2)); c.scale(a, a); icon("bubble", 0, 0, 300, ORG); txt("TELL ME!", 0, -10, "66px Anton", "#fff", "center", 1, "middle"); c.restore();
  if (t > tF - .2) { const u = ease(prog(t, tF - .2, .4)); txt("Follow @heybytewise", 540, 1270, "700 70px Inter", ORG, "center", u); txt("for simple tech news every morning", 540, 1340, "34px Mono", CREAM, "center", u); }
};

function header(t, i) {
  c.drawImage(badge, 34, 34);
  txt(i === 8 ? "YOUR TURN" : "THE MONDAY EDITION", 1020, 98, "30px Mono", ORG, "right");
}
hit(P[0][1] - .1, 540, 600, .6); hit(W("certified", 1) - .2, 540, 860); hit(W("17", 1), 330, 1230, .7);
hit(W("Reality", 2) - .2, 540, 880, .7); hit(W("stolen", 3), 540, 900, .7); hit(W("next", 3) - .3, 540, 1470, .7); hit(W("Never", 3) - .3, 540, 950, .8);
hit(W("not", 4) - .1, 540, 860); hit(W("7", 5) - .15, 400, 900, .8); hit(W("Motherbrain", 6) - .3, 540, 660, .7); hit(W("June", 7) - .3, 780, 1260, .8); hit(W("Tell", 8) - .2, 540, 900, .6);
for (let k = 1; k < 8; k++) hit(PS[k] + .42, 540, 420, .45);

const bvc = document.getElementById("bv").getContext("2d");
wires.forEach(m => m.visible = false); pts.material.opacity = .55;
async function footage(t, i, rel, dur) {
  const n = Math.min(NJ.bgFrames || 99999, Math.max(1, Math.round(t * 30) + 1));
  const img = await createImageBitmap(await (await fetch(`bg/${String(n).padStart(5, "0")}.jpg`)).blob());
  const k = 1.05 + .05 * prog(rel, 0, dur), dx = (i % 2 ? -1 : 1) * 25 * prog(rel, 0, dur);
  bvc.save(); bvc.translate(540 + dx, 960); bvc.scale(k, k); bvc.drawImage(img, -540, -960, 1080, 1920); bvc.restore(); img.close();
  bvc.fillStyle = "rgba(7,10,20,.42)"; bvc.fillRect(0, 0, 1080, 1920);
  let g = bvc.createLinearGradient(0, 0, 0, 760); g.addColorStop(0, "rgba(7,10,20,.9)"); g.addColorStop(1, "rgba(7,10,20,0)"); bvc.fillStyle = g; bvc.fillRect(0, 0, 1080, 760);
  g = bvc.createLinearGradient(0, 1400, 0, 1920); g.addColorStop(0, "rgba(7,10,20,0)"); g.addColorStop(1, "rgba(7,10,20,.92)"); bvc.fillStyle = g; bvc.fillRect(0, 1400, 1080, 520);
}
window.renderAt = async (t) => {
  const i = sceneAt(t), rel = t - PS[i], dur = (PS[i + 1] || END) - PS[i];
  await footage(t, i, rel, dur);
  const [sx, sy] = shakeAt(t);
  cfx.clearRect(0, 0, 1080, 1920);
  const off = 2.2 * t + PS.slice(1).reduce((a, p) => a + 10 * io(prog(t, p - .45, .9)), 0);
  for (let k = 0; k < NP; k++) ppos[k * 3 + 2] = ((pz0[k] + off) % 50) - 40;
  pg.attributes.position.needsUpdate = true;
  wires.forEach((m, k) => { const p = m.userData.p; m.rotation.set(t * .21 + k, t * .17 * (k % 2 ? 1 : -1), 0); m.position.set(p[0] + .5 * Math.sin(t * .3 + k), p[1] + .6 * Math.cos(t * .25 + k), p[2]); });
  pl.position.set(6 * Math.sin(t * .7), 4 * Math.cos(t * .5), 2); bl.position.set(-6 * Math.cos(t * .4), -5, 3);
  for (let k = 1; k <= 7; k++) { const n = nums[k], on = false; n.grp.visible = on; if (!on) continue;
    const f = io(prog(rel, -.05, .8));
    n.grp.position.set(1.4 + 1.5 * (1 - f), -1.8 + .8 * (1 - f), 15 - 26 * f);
    n.grp.rotation.set(.18 * Math.sin(rel * .45) + .6 * (1 - f), -2.4 * (1 - f) + .45 * Math.sin(rel * .6), .05 * Math.sin(rel * .3));
    n.solid.material.opacity = 1 - .9 * prog(rel, .9, .8); n.edge.material.opacity = .9 - .62 * prog(rel, .9, .8); }
  bgCam.position.set(.5 * Math.sin(t * .23), .4 * Math.cos(t * .19), D); bgCam.lookAt(0, 0, 0);
  c = csc; c.clearRect(0, 0, 1080, 1920); S[i](t); c = cfx; tex.needsUpdate = true;
  // camera: optional shot keyframes per scene (SHOTS[i] = [[relT, scale, focusX, focusY], ...]) + push-through at cuts
  const SH = shotAt(rel, (typeof SHOTS !== "undefined" && SHOTS[i]) || null), fx = SH.fx ?? 540, fy = SH.fy ?? 960;
  const zoom = SH.s * (1 + (i === 0 ? Math.max(0, pushZ(rel, dur) - .35 * Math.pow(1 - clamp(rel / .7), 3)) : pushZ(rel, dur))) * (1 + .03 * prog(rel, 0, dur));
  const u = 10 / 1920;
  card.scale.set(zoom, zoom, 1);
  card.rotation.set(.03 * Math.sin(rel * .5 + i), .05 * Math.sin(rel * .37 + i * 1.3), 0);
  card.position.set(sx * .012 - (fx - 540) * u * (zoom - 1), -sy * .012 + (fy - 960) * u * (zoom - 1), 0);
  renderer.clear(); renderer.render(bgScene, bgCam);
  header(t, i); hitFx(t); captions(t);
  txt("@heybytewise · follow for daily tech news", 60, 1880, "24px Mono", "rgba(243,239,230,.5)");
  leak(t, PS.slice(1)); grain(t);
};
await window.renderAt(0);
window.READY = true;

</script>
</body></html>
