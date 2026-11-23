// ---------------- Example episode scenes (Ep12 Inheritance, 3 paragraphs) ----------------
// One scene per paragraph of el_script.txt. Rewrite S[], CHAPTERS and SHOTS for each episode; keep renderAt.
// Tools available: ktext (kinetic text + one highlighted word), slam-free titles, codeWin/outputWin, glow sketch
// (gsketch/GS/gflow/gtype), pocket, shotAt camera keys, leak at cuts (automatic), captions (automatic).
const S = [];
const CHAPTERS = ["Intro", "Making a child class", "Recap"];   // chapter name per paragraph (merge short ones in the description)
const SHOTS = [];                                                // optional: SHOTS[i] = [[relT, scale, focusX, focusY], ...]

S[0] = t => {   // hook: one idea, motion from frame 0
  ktext("Write less code", 960, 470, 170, t, -1, { dir: "up", align: "center" });
  ktext("with inheritance", 960, 650, 150, t, -.6, { dir: "up", align: "center", emph: { word: "inheritance", kind: "pill", color: ORG } });
  gsketch(GS.rect(660, 760, 240, 120), t, -1, .9, GCY, 7, 1); gsketch(GS.rect(1020, 760, 240, 120), t, -.4, .9, GOR, 7, 2);
  const ar = GS.arrow(900, 820, 1015, 820); gsketch(ar, t, .3, .4, GYE, 6, 3); gflow(ar, t, .8);
};

const CODE = ['class Animal:', '    def eat(self):', '        print("nom nom")', '', 'class Dog(Animal):', '    def bark(self):', '        print("Woof!")', '', 'rex = Dog()', 'rex.eat()', 'rex.bark()'];
S[1] = t => {
  const tA = W("A", 1) - .1, tDog = W("Dog", 1) + .2, tFree = W("for", 1, W("everything", 1)), tTricks = W("tricks", 1), tBark = W("bark", 1);
  const T = [tA, tA + .35, tA + .75, 0, tDog + .4, tTricks - .4, tTricks, 0, tBark - .9, tBark - .6, tBark - .3];
  codeWin(t, 80, 240, 900, 570, CODE, T, { hi: t > tFree && t < tTricks ? [4, tFree] : null });
  outputWin(t, 80, 830, 900, ["nom nom", "Woof!"], tBark + .2);
  gsketch(GS.rect(1200, 280, 520, 170), t, tA, .8, GCY, 8, 4); gtype("Animal", 1460, 350, 64, GCY, t, tA + .5, .4, "center"); gtype("eat()", 1460, 420, 44, CREAM, t, tA + .9, .3, "center");
  const ar = GS.arrow(1460, 460, 1460, 600); gsketch(ar, t, tDog - .1, .5, GYE, 7, 5); txt("IS-A", 1500, 545, "32px Mono", GYE, "left", prog(t, tDog + .3, .3));
  gsketch(GS.rect(1200, 610, 520, 250), t, tDog, .8, GOR, 8, 6); gtype("Dog", 1460, 680, 64, GOR, t, tDog + .5, .4, "center");
  if (t > tFree) { gflow(ar, t, tFree, GYE, 4, 1.2); gtype("eat()  ✓ for free", 1460, 760, 44, "#4ade80", t, tFree + .1, .6, "center"); }
  gtype("bark()  ★ new", 1460, 830, 44, YEL, t, tTricks, .5, "center");
};
SHOTS[1] = [[0, 1, 960, 540], [4.2, 1, 960, 540], [5.0, 1.35, 1460, 580], [7.6, 1.35, 1460, 580], [8.4, 1, 960, 540]];

S[2] = t => {
  const t0 = PS[2];
  pocket(460, 250, 1000, 520, .5);
  ktext("Recap", 960, 330, 120, t, t0 + .2, { dir: "up", align: "center" });
  ["A child class gets the parent's methods", "Then it adds its own"].forEach((s, k) =>
    ktext(s, 960, 500 + k * 110, 64, t, t0 + .9 + k * 1.2, { dir: "left", font: "Inter", weight: 700, align: "center", emph: k ? { word: "own", kind: "under", color: YEL } : { word: "parent's", kind: "marker", color: ORG } }));
  if (t > W("Subscribe", 2) - .2) { const u = ease(prog(t, W("Subscribe", 2) - .2, .4)); c.save(); c.globalAlpha = u; rr(560, 760, 800, 130, 30, "rgba(255,106,43,.14)", ORG, 4);
    txt(`Subscribe for Episode ${EP.ep + 1}`, 960, 840, "700 54px Inter", "#fff", "center"); c.restore(); }
};

window.renderAt = async t => {
  const i = sceneAt(t), rel = t - PS[i], dur = (PS[i + 1] ?? END) - PS[i];
  c = cmain; bg(t);
  c = clay; c.clearRect(0, 0, 1920, 1080); S[i](t);
  const SH = shotAt(rel, SHOTS[i]), fx = SH.fx ?? 960, fy = SH.fy ?? 540;
  const z = SH.s * (1 + (i === 0 ? Math.max(0, pushZ(rel, dur) - .35 * Math.pow(1 - clamp(rel / .7), 3)) : pushZ(rel, dur))) * (1 + .02 * prog(rel, 0, dur));
  // keep the camera inside the frame: focus clamped so edges never show
  const hx = 960 / z, hy = 540 / z, cx = Math.min(1920 - hx, Math.max(hx, fx)), cy = Math.min(1080 - hy, Math.max(hy, fy));
  c = cmain; c.save(); c.translate(960, 540); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(layer, 0, 0); c.restore();
  header(t, CHAPTERS[i]); captions(t); leak(t, PS.slice(1), 1920, 1080);
};
await Promise.all([document.fonts.load("100px Anton"), document.fonts.load("40px Mono"), document.fonts.load("700 40px Inter"), badge.decode()]);
await window.renderAt(0);
window.READY = true;
