// ---------------- motion kit (ideas adapted from bang-motion, MIT) ----------------
// Needs globals: c (2D context of the scene canvas), clamp, ease, back, rand, and fonts Anton/Inter loaded.
//
// ktext(text, x, y, size, t, t0, opts)  lively text: letters stretch in with a directional motion blur.
//   opts: dir "up" | "left" (alternate between scenes), font "Anton" | "Inter", weight (Inter only, 500-800),
//         color, align "left" | "center", emph {word, kind: "pill"|"under"|"marker"|"box"|"color"|"strike", color},
//         dur (per letter, default .55), stagger (default .024)
//   One highlighted keyword per line at most. Do not use the same size + direction + position in two scenes in a row.
// pocket(x, y, w, h, a)   dark soft pocket behind text when the background is busy.
// leak(t, cuts, W, H)     soft light leak at each cut time in `cuts` (alternating sides). Draw it on the TOP layer.
// pushZ(rel, dur)         push-through camera for a scene: returns extra zoom (born a bit large, push in before the cut).
// shotAt(rel, keys)       camera shot keyframes [[relT, scale, fx, fy], ...] -> {s, fx, fy} eased between keys.

function _ktParts(text, emph) {
  if (!emph) return [{ s: text, hl: false }];
  const i = text.indexOf(emph.word); if (i < 0) return [{ s: text, hl: false }];
  return [{ s: text.slice(0, i), hl: false }, { s: emph.word, hl: true }, { s: text.slice(i + emph.word.length), hl: false }].filter(p => p.s);
}
function ktext(text, x, y, size, t, t0, o = {}) {
  if (t < t0) return;
  const dir = o.dir || "up", fam = o.font || "Anton", wt = fam === "Inter" ? (o.weight || 700) + " " : "";
  const font = `${wt}${size}px ${fam}`, col = o.color || "#fff", dur = o.dur || .55, st = o.stagger || .024;
  c.save(); c.font = font; c.textBaseline = "alphabetic";
  const tw = c.measureText(text).width; const x0 = o.align === "center" ? x - tw / 2 : (o.align === "right" ? x - tw : x);
  const parts = _ktParts(text, o.emph); let cx = x0, li = 0; const ecol = (o.emph && o.emph.color) || "#ff6a2b";
  // emphasis shape is drawn first (behind the word), after the line has landed
  const te = t0 + text.length * st + .35;
  for (const p of parts) {
    const pw = c.measureText(p.s).width;
    if (p.hl && t > te) {
      const u = ease(clamp((t - te) / .45)), k = o.emph.kind || "pill";
      c.save();
      if (k === "pill") { c.fillStyle = ecol; c.beginPath(); c.roundRect(cx - size * .12, y - size * .86, (pw + size * .24) * u, size * 1.04, size * .22); c.fill(); }
      if (k === "under") { c.fillStyle = ecol; c.fillRect(cx, y + size * .08, pw * u, size * .12); }
      if (k === "marker") { c.globalAlpha = .55; c.fillStyle = ecol; c.translate(cx, y); c.rotate(-.025); c.fillRect(-size * .08, -size * .42, (pw + size * .16) * u, size * .48); }
      if (k === "box") { c.strokeStyle = ecol; c.lineWidth = size * .05; c.beginPath(); c.roundRect(cx - size * .1, y - size * .9, pw + size * .2, size * 1.08, size * .1); c.setLineDash([4000]); c.lineDashOffset = 4000 * (1 - u); c.stroke(); }
      if (k === "strike") { c.fillStyle = ecol; c.fillRect(cx, y - size * .38, pw * u, size * .09); }
      c.restore();
    }
    for (const ch of p.s) {
      const w = c.measureText(ch).width;
      if (ch !== " ") {
        const u = clamp((t - (t0 + li * st)) / dur);
        if (u > 0) {
          const e = 1 - Math.pow(1 - u, 4); // power4.out
          const lc = p.hl ? ((o.emph.kind === "pill") ? "#fff" : (o.emph.kind === "color" ? ecol : col)) : col;
          const dx = dir === "left" ? -(1 - e) * size * .45 : 0, dy = dir === "up" ? (1 - e) * size * .6 : 0, sy = dir === "up" ? 1 + (1 - e) * .45 : 1;
          // directional motion blur: ghost copies behind the letter along its path, fading as it lands
          const blur = (1 - e);
          for (let g = 3; g >= 0; g--) {
            const f = g / 3, a = g === 0 ? clamp(u * 3) : clamp(u * 3) * blur * .22;
            if (a <= .01) continue;
            c.save(); c.globalAlpha = a; c.fillStyle = lc;
            c.translate(cx + w / 2 + dx * (1 + f * .9), y + dy * (1 + f * .9)); c.scale(1, sy);
            if (g === 0 && !p.hl) { c.shadowColor = "rgba(0,0,0,.5)"; c.shadowBlur = 24; c.shadowOffsetY = 4; }
            c.fillText(ch, -w / 2, 0); c.restore();
          }
        }
      }
      cx += w; li++;
    }
  }
  c.restore();
}
function pocket(x, y, w, h, a = .55) {
  // soft elliptical dark pocket, fades to nothing before its bounding box (no visible edges)
  const cx = x + w / 2, cy = y + h / 2, R = w * .75;
  c.save(); c.translate(cx, cy); c.scale(1, (h * 1.5) / (w * 1.5));
  const g = c.createRadialGradient(0, 0, 0, 0, 0, R); g.addColorStop(0, `rgba(5,7,15,${a})`); g.addColorStop(.6, `rgba(5,7,15,${a * .6})`); g.addColorStop(1, "rgba(5,7,15,0)");
  c.fillStyle = g; c.fillRect(-R, -R, 2 * R, 2 * R); c.restore();
}
function leak(t, cuts, W = 1080, H = 1920, col = "255,140,70") {
  for (let k = 0; k < cuts.length; k++) {
    const d = t - cuts[k]; if (d < -.35 || d > .55) continue;
    const a = d < 0 ? Math.sin((d + .35) / .35 * Math.PI / 2) : Math.cos(d / .55 * Math.PI / 2);
    const side = k % 2 ? 1 : -1, x = W / 2 + side * W * (.55 - .25 * (d + .35)), y = H * (.3 + .15 * (k % 3));
    c.save(); c.globalCompositeOperation = "screen"; c.globalAlpha = a * .95;
    const g = c.createRadialGradient(x, y, 0, x, y, Math.max(W, H) * .75);
    g.addColorStop(0, `rgba(${col},.95)`); g.addColorStop(.35, `rgba(${col},.45)`); g.addColorStop(1, `rgba(${col},0)`);
    c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore();
  }
}
function pushZ(rel, dur) {
  const born = .35 * Math.pow(1 - clamp(rel / .7), 3);            // new scene is born slightly large, settles (power3.out)
  const out = .55 * Math.pow(clamp((rel - (dur - .4)) / .4), 2);  // push in before the cut (power2.in)
  return born + out;
}
function shotAt(rel, keys) {
  if (!keys || !keys.length) return { s: 1, fx: null, fy: null };
  if (rel <= keys[0][0]) return { s: keys[0][1], fx: keys[0][2], fy: keys[0][3] };
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (rel <= b[0]) { const u = clamp((rel - a[0]) / Math.max(.01, Math.min(.8, b[0] - a[0]))); const e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
      return { s: a[1] + (b[1] - a[1]) * e, fx: a[2] + (b[2] - a[2]) * e, fy: a[3] + (b[3] - a[3]) * e }; }
  }
  const z = keys[keys.length - 1]; return { s: z[1], fx: z[2], fy: z[3] };
}
