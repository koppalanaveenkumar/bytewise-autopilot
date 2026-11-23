"""Python for Beginners, Episode 11: Classes and Objects."""
from scenes_ep3 import *
import look2x as L
import math
from PIL import Image, ImageDraw
ease = lambda u: 1 - (1 - max(0.0, min(1.0, u))) ** 3
L.KEYWORDS.update({"def", "self", "class", "return", "and", "not"})

GROUPS = [[i] for i in range(0, 17)]
CHAPTERS = ["Intro", "What is a class?", "Making a class", "The init method", "self and attributes", "Making an object", "Many objects",
            "Methods", "Calling a method", "Common mistake", "Bank account project", "Bank account project", "Bank account project",
            "Bank account project", "Recap", "Homework", "Next episode"]

DOG = ["class Dog:", "    def __init__(self, name):", "        self.name = name"]
BARK = ["    def bark(self):", '        print(f"{self.name} says Woof!")']
BANK = ["class BankAccount:", "    def __init__(self, owner, balance):", "        self.owner = owner", "        self.balance = balance",
        "    def deposit(self, amount):", "        self.balance += amount", '        print(f"Balance: {self.balance}")',
        "    def withdraw(self, amount):", "        if amount <= self.balance:", "            self.balance -= amount", '            print(f"Balance: {self.balance}")',
        "        else:", '            print("Not enough money!")']
USE = ['acc = BankAccount("Priya", 1000)', "acc.deposit(500)", "acc.withdraw(5000)"]


def note_box(d, x0, y0, x1, h1, h2, p, c):
    if p <= 0: return
    oy = panel(d, x0, y0, x1, y0 + 108, p, outline=c)
    d.text((x0 + 30, y0 + 38 + oy), h1, font=mono(30, True), fill=col(c, p), anchor="lm")
    body(d, h2, x0 + 32, y0 + 82 + oy, 28, WHITE, p, anchor="lm")


def star(cx, cy, r, k=0.45, n=5):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * k
        an = -math.pi / 2 + i * math.pi / n
        pts.append((cx + rr * math.cos(an), cy + rr * math.sin(an)))
    return pts


def bank_card(d, ly, x0, y0, bal, p, c=ACC, msg=None, msgc=RED):
    if p <= 0: return
    oy = panel(d, x0, y0, x0 + 620, y0 + 330, p, outline=c)
    body(d, "Priya's account", x0 + 50, y0 + 70 + oy, 36, MUTED, p, anchor="lm")
    d.text((x0 + 50, y0 + 170 + oy), f"₹{bal:,}", font=mono(96, True), fill=col(WHITE, p), anchor="lm")
    if msg: d.text((x0 + 50, y0 + 270 + oy), msg, font=mono(40, True), fill=col(msgc, p), anchor="lm")
    emoji(ly, "\U0001F3E6", x0 + 540, int(y0 + 70 + oy), 70, p)


# 01 hook
def k01(ly, d, t, D, B):
    if t < B[3] - 0.05:
        kw(d, ["Your", "own", "bank", "account"], CX, TY, 110, t, -1, 0.0, {"bank": ACC})
        bal = 1000 if t < B[1] + 2.0 else 1500
        msg, mc = None, RED
        if B[1] + 2.0 <= t < B[2]: msg, mc = "+₹500 deposited", ACC
        if t > B[2] + 2.0: msg, mc = "Not enough money!", RED
        bank_card(d, ly, 650, 330, bal, a(t, -1), ACC, msg, mc)
        for (lb, st, c, y) in [("deposit(500)", B[1] + 0.4, ACC, 420), ("withdraw(5000)", B[2] + 0.5, RED, 600)]:
            pill(d, lb, 1560, y, pop(t, st), 40, c, DARK if c == ACC else WHITE)
        if t > B[2] + 2.0: stamp(ly, "BLOCKED", 960, 830, a(t, B[2] + 2.1, 0.16), RED, 90, -5)
    else:
        kw(d, ["Python", "for", "Beginners"], CX, 280, 120, t, B[3], 0.1, {"Python": YELLOW})
        for i, (em, lb, sub, c, st) in enumerate([("\U0001F36A", "Classes", "the blueprint", YELLOW, B[3] + 1.6), ("\U0001F436", "Objects", "made from it", BLUE, B[3] + 2.3)]):
            p = pop(t, st)
            if p <= 0: continue
            x = 640 + i * 640
            panel(d, x - 260, 400, x + 260, 760, min(p, 1), outline=c)
            emoji(ly, em, x, 520, 130, p)
            text(d, lb, x, 650, 56, WHITE, min(p, 1))
            body(d, sub, x, 712, 34, MUTED, min(p, 1))
        pill(d, "Episode 11:  Classes & Objects", CX, 880, pop(t, B[3] + 3.0), 54, ACC, DARK)


# 02 cookie cutter
def k02(ly, d, t, D, B):
    kw(d, ["A", "class", "is", "a", "blueprint"], CX, TY, 110, t, 0.05, 0.12, {"blueprint": YELLOW})
    p = a(t, B[1] + 0.3)
    if p > 0:
        d.polygon(star(420, 560, 190), fill=None, outline=None)
        pts = star(420, 560, 190)
        d.line(pts + [pts[0]], fill=col(YELLOW, p), width=14, joint="curve")
        text(d, "class", 420, 820, 56, YELLOW, p)
        body(d, "one shape", 420, 885, 34, MUTED, p)
    for i in range(3):
        q = pop(t, B[1] + 2.4 + i * 0.5)
        if q <= 0: continue
        cx = 950 + i * 330
        k = min(q, 1.05)
        d.polygon(star(cx, 560, 130 * k), fill=col((205, 140, 70), min(q, 1)))
        d.polygon(star(cx, 560, 100 * k), fill=col((226, 168, 96), min(q, 1)))
        for dx, dy in ((-30, -10), (25, 20), (5, -45)): d.ellipse([cx + dx - 9, 560 + dy - 9, cx + dx + 9, 560 + dy + 9], fill=col((90, 50, 30), min(q, 1)))
    if t > B[2]:
        text(d, "objects", 1280, 820, 56, BLUE, a(t, B[2] + 0.2))
        body(d, "as many as you like", 1280, 885, 34, MUTED, a(t, B[2] + 0.2))
    if t > B[1] + 2.4:
        q = a(t, B[1] + 2.4)
        d.line([(650, 560), (800, 560)], fill=col(WHITE, q), width=8); d.polygon([(820, 560), (790, 540), (790, 580)], fill=col(WHITE, q))


# 03 class Dog:
def k03(ly, d, t, D, B):
    kw(d, ["Make", "a", "class"], CX, TY, 110, t, 0.05, 0.12, {"class": YELLOW})
    p = pop(t, B[1])
    if p > 0:
        oy = panel(d, 560, 360, 1360, 560, min(p, 1), fill=CODEBG, outline=YELLOW)
        s = "class Dog:"[:int(clamp((t - B[1] - 0.3) / 1.6) * 10)]
        f = mono(96, True)
        x = CX - d.textlength("class Dog:", font=f) / 2
        L.draw_code_line(d, x, 410 + oy, s, f)
    if t > B[2]:
        q = a(t, B[2] + 0.2)
        f = mono(96, True); x = CX - d.textlength("class Dog:", font=f) / 2 + d.textlength("class ", font=f)
        d.ellipse([x - 14, 385, x + d.textlength("D", font=f) + 10, 540], outline=col(ORANGE, q), width=7)
        pill(d, "Capital letter: Dog", CX, 700, pop(t, B[2] + 0.5), 48, ORANGE, INK)
    for i, (lb, st) in enumerate([("class", B[1] + 0.3), ("name", B[1] + 1.0), ("colon", B[1] + 1.8)]):
        pill(d, lb, 640 + i * 320, 860, pop(t, st), 38, PANEL, WHITE)
    emoji(ly, "\U0001F436", 1500, 460, 110, pop(t, B[1] + 1.2))


# 04 __init__
def k04(ly, d, t, D, B):
    kw(d, ["The", "init", "method"], CX, TY, 110, t, 0.05, 0.12, {"init": ACC})
    code_win(d, 70, 300, 1180, tl(DOG[:2], [(0, 0.01), (B[0] + 0.6, B[0] + 2.2)], t), t, 0, 0.01, a(t, 0.2), 44, "Python")
    if t > B[0] + 1.2: hl(d, 70, 1180, 300, 44, 1, 1, ACC, a(t, B[0] + 1.6) * 0.9)
    note_box(d, 1240, 300, 1860, "__init__", "a special setup method", a(t, B[0] + 1.8), ACC)
    note_box(d, 1240, 430, 1860, "runs automatically", "every new object", a(t, B[1] + 0.5), YELLOW)
    note_box(d, 1240, 560, 1860, "its job", "set the object up", a(t, B[2] + 0.3), BLUE)
    emoji(ly, "⚙️", 1550, 820, 110, pop(t, B[1] + 0.8))


# 05 self + attributes
def k05(ly, d, t, D, B):
    kw(d, ["self", "and", "attributes"], CX, TY, 110, t, 0.05, 0.12, {"self": YELLOW, "attributes": BLUE})
    code_win(d, 70, 300, 1180, tl(DOG, [(0, 0.01), (0, 0.01), (B[1] + 0.2, B[1] + 1.6)], t), t, 0, 0.01, 1, 44, "Python")
    if t > B[1] + 0.8: hl(d, 70, 1180, 300, 44, 2, 2, YELLOW, a(t, B[1] + 1.0) * 0.9)
    p = a(t, B[0] + 0.4)
    if p > 0:
        oy = panel(d, 1240, 300, 1860, 640, p, outline=YELLOW)
        text(d, "self = this object", 1550, 360 + oy, 38, YELLOW, p)
        emoji(ly, "\U0001F436", 1550, int(470 + oy), 100, p)
        q = a(t, B[1] + 1.8) * p
        if q > 0:
            d.rounded_rectangle([1300, 540 + oy, 1800, 610 + oy], 16, fill=col(CODEBG, q), outline=col(BLUE, q), width=4)
            d.text((1550, 575 + oy), 'name: "Bruno"', font=mono(34, True), fill=col(WHITE, q), anchor="mm")
    pill(d, "attribute = a value stored inside", 1100, 820, pop(t, B[2] + 0.3), 46, BLUE, WHITE)


# 06 make an object
def k06(ly, d, t, D, B):
    kw(d, ["Make", "an", "object"], CX, TY, 110, t, 0.05, 0.12, {"object": BLUE})
    lines = ['my_dog = Dog("Bruno")', "print(my_dog.name)"]
    code_win(d, 70, 300, 1180, tl(lines, [(B[1] + 0.1, B[1] + 1.6), (B[2] + 0.1, B[2] + 1.4)], t), t, 0, 0.01, a(t, 0.2), 48, "Python", run_t=B[2] + 1.7)
    out_win(d, 1240, 300, 1850, [([seg("Bruno", YELLOW, True)], B[2] + 2.0)], t, a(t, B[2] + 1.7, 0.25), 56)
    p = pop(t, B[1] + 1.2)
    if p > 0:
        oy = panel(d, 1340, 560, 1760, 900, min(p, 1), outline=YELLOW)
        emoji(ly, "\U0001F436", 1550, int(680 + oy), 120, p)
        text(d, "Bruno", 1550, 830 + oy, 52, WHITE, min(p, 1))


# 07 many objects
def k07(ly, d, t, D, B):
    kw(d, ["Same", "blueprint,", "new", "object"], CX, TY, 104, t, 0.05, 0.12, {"blueprint,": YELLOW})
    p = a(t, 0.2)
    if p > 0:
        oy = panel(d, 660, 300, 1260, 440, p, fill=CODEBG, outline=YELLOW)
        L.draw_code_line(d, 760, 342 + oy, "class Dog:", mono(52, True))
    for i, (em, nm, st, c) in enumerate([("\U0001F436", "Bruno", 0.5, BLUE), ("\U0001F415", "Max", B[0] + 0.5, ACC)]):
        q = pop(t, st)
        if q <= 0: continue
        cx = 600 + i * 720
        d.line([(960, 450), (cx, 540)], fill=col(MUTED, min(q, 1)), width=5)
        oy = panel(d, cx - 230, 540, cx + 230, 880, min(q, 1), outline=c)
        emoji(ly, em, cx, int(650 + oy), 110, q)
        d.text((cx, 790 + oy), f'Dog("{nm}")', font=mono(40, True), fill=col(WHITE, min(q, 1)), anchor="mm")
    pill(d, "each keeps its own name", CX, 960, pop(t, B[2] + 0.2), 44, ACC, DARK)


# 08 methods
def k08(ly, d, t, D, B):
    kw(d, ["Objects", "can", "do", "things"], CX, TY, 104, t, 0.05, 0.12, {"do": ORANGE})
    lines = DOG + BARK
    code_win(d, 70, 300, 1300, tl(lines, [(0, 0.01)] * 3 + [(B[2] + 0.2, B[2] + 1.4), (B[2] + 1.5, B[2] + 3.6)], t), t, 0, 0.01, a(t, 0.2), 42, "Python")
    if t > B[2] + 0.6: hl(d, 70, 1300, 300, 42, 3, 4, ORANGE, a(t, B[2] + 0.8) * 0.9)
    note_box(d, 1350, 300, 1870, "method", "a function inside a class", a(t, B[1] + 0.4), ORANGE)
    note_box(d, 1350, 430, 1870, "bark()", "prints the name + Woof", a(t, B[2] + 1.0), YELLOW)


# 09 calling a method
def k09(ly, d, t, D, B):
    kw(d, ["Call", "it", "with", "a", "dot"], CX, TY, 110, t, 0.05, 0.12, {"dot": YELLOW})
    code_win(d, 70, 300, 1180, tl(['my_dog = Dog("Bruno")', "my_dog.bark()"], [(0, 0.01), (B[1] + 0.1, B[1] + 1.2)], t), t, 0, 0.01, a(t, 0.2), 48, "Python",
             run_t=B[2] - 0.1)
    out_win(d, 1240, 300, 1850, [([seg("Bruno says Woof!", YELLOW, True)], B[2] + 0.2)], t, a(t, B[2] - 0.1, 0.25), 44)
    q = pop(t, B[2] + 0.3)
    if q > 0:
        emoji(ly, "\U0001F436", 1400, 700, 160, q)
        oy = panel(d, 1500, 560, 1840, 690, min(q, 1), fill=(255, 255, 255))
        d.text((1670, 625 + oy), "Woof!", font=font(60), fill=col(INK, min(q, 1)), anchor="mm")
    if t > B[0] + 0.4:
        pill(d, "object  .  method()", 625, 700, pop(t, B[0] + 0.5), 46, YELLOW, INK)


# 10 common mistake: forgetting self
def k10(ly, d, t, D, B):
    kw(d, ["Common", "mistake"], CX, TY, 110, t, 0.05, 0.12, {"mistake": RED})
    if t < B[2] - 0.05:
        lines = ["class Dog:", "    def bark():", '        print("Woof!")', "", "Dog().bark()"]
        code_win(d, 70, 300, 1100, lines, t, 0, 0.01, a(t, 0.2), 42, "Python", run_t=B[1] + 2.4)
        if t > B[1] + 0.3: hl(d, 70, 1100, 300, 42, 1, 1, RED, a(t, B[1] + 0.5) * 0.9)
        out_win(d, 1160, 300, 1850, [([seg("TypeError:", RED, True)], B[1] + 2.7), ([seg("Dog.bark() takes 0", RED, True)], B[1] + 2.9),
                                     ([seg("positional arguments", RED, True)], B[1] + 3.0), ([seg("but 1 was given", RED, True)], B[1] + 3.1)], t, a(t, B[1] + 2.4, 0.25), 34)
        stamp(ly, "FORGOT SELF", CX, 850, a(t, B[1] + 4.2, 0.16), RED, 90, -5)
    else:
        lines = ["class Dog:", "    def bark(self):", '        print("Woof!")', "", "Dog().bark()"]
        code_win(d, 70, 300, 1100, lines, t, 0, 0.01, 1, 42, "Python", run_t=B[2] + 0.9)
        hl(d, 70, 1100, 300, 42, 1, 1, ACC, a(t, B[2] + 0.1) * 0.9)
        out_win(d, 1160, 300, 1850, [([seg("Woof!", ACC, True)], B[2] + 1.2)], t, a(t, B[2] + 0.9, 0.25), 48)
        pill(d, "self always comes first", 585, 840, pop(t, B[2] + 0.4), 48, ACC, DARK)


# 11 project intro
def k11(ly, d, t, D, B):
    kw(d, ["Mini", "project:", "bank", "account"], CX, TY, 100, t, 0.05, 0.1, {"bank": ACC, "account": ACC})
    emoji(ly, "\U0001F3E6", 1830, TY, 80, pop(t, 0.7))
    p = a(t, B[1] - 0.2)
    if p > 0:
        oy = panel(d, 560, 330, 1360, 820, p, outline=ACC)
        text(d, "BankAccount", CX, 400 + oy, 56, ACC, p)
        for i, (k_, v, c, st) in enumerate([("owner", '"Priya"', YELLOW, B[1] + 0.6), ("balance", "1000", BLUE, B[1] + 1.6)]):
            q = a(t, st) * p
            if q <= 0: continue
            y0 = 480 + i * 150
            d.rounded_rectangle([640, y0 + oy, 1280, y0 + 110 + oy], 20, fill=col(CODEBG, q), outline=col(c, q), width=4)
            d.text((680, y0 + 55 + oy), k_, font=mono(44, True), fill=col(c, q), anchor="lm")
            d.text((1240, y0 + 55 + oy), v, font=mono(44, True), fill=col(WHITE, q), anchor="rm")


def bank_win(d, t, sched, p=1.0):
    return code_win(d, 40, 270, 1240, tl(BANK, sched, t), t, 0, 0.01, p, 28, "Python")


# 12 init + deposit
def k12(ly, d, t, D, B):
    kw(d, ["Store", "and", "deposit"], CX, TY - 20, 96, t, 0.05, 0.12, {"deposit": ACC})
    sch = [(B[0] + 0.1, B[0] + 0.7), (B[0] + 0.8, B[0] + 2.0), (B[0] + 2.1, B[0] + 2.9), (B[0] + 3.0, B[0] + 3.9),
           (B[1] + 0.2, B[1] + 1.4), (B[1] + 1.5, B[1] + 2.6), (B[1] + 2.7, B[1] + 4.2)] + [(999, 999)] * 6
    bank_win(d, t, sch, a(t, 0.2))
    note_box(d, 1290, 290, 1880, "__init__", "owner + starting balance", a(t, B[0] + 1.6), YELLOW)
    note_box(d, 1290, 420, 1880, "deposit()", "adds to the balance", a(t, B[1] + 1.0), ACC)
    note_box(d, 1290, 550, 1880, "+= amount", "balance = balance + amount", a(t, B[1] + 2.0), BLUE)


# 13 withdraw
def k13(ly, d, t, D, B):
    kw(d, ["Check", "before", "you", "pay"], CX, TY - 20, 96, t, 0.05, 0.12, {"Check": ORANGE})
    sch = [(0, 0.01)] * 7 + [(B[0] + 0.2, B[0] + 1.4), (B[1] + 0.1, B[1] + 1.4), (B[2] + 0.1, B[2] + 1.0), (B[2] + 1.0, B[2] + 1.8),
                              (B[3] + 0.1, B[3] + 0.5), (B[3] + 0.6, B[3] + 1.8)]
    bank_win(d, t, sch)
    note_box(d, 1290, 290, 1880, "if amount <= balance", "enough money?", a(t, B[1] + 0.6), ORANGE)
    note_box(d, 1290, 420, 1880, "yes", "take it out", a(t, B[2] + 0.4), ACC)
    note_box(d, 1290, 550, 1880, "no", '"Not enough money!"', a(t, B[3] + 0.6), RED)


# 14 run it
def k14(ly, d, t, D, B):
    kw(d, ["Let's", "run", "it"], CX, TY, 110, t, 0.05, 0.12, {"run": YELLOW})
    code_win(d, 60, 300, 1060, tl(USE, [(B[1] + 0.1, B[1] + 1.4), (B[2] + 0.1, B[2] + 0.8), (B[3] + 0.0, B[3] + 0.8)], t), t, 0, 0.01, a(t, 0.2), 38, "Python",
             run_t=B[0] + 0.3)
    items = [([seg("Balance: ", WHITE), seg("1500", ACC, True)], B[2] + 1.6), ([seg("Not enough money!", RED, True)], B[4] + 0.1)]
    out_win(d, 60, 640, 1060, items, t, a(t, B[2] + 1.0, 0.25), 44)
    bal = 1000 if t < B[2] + 1.6 else 1500
    msg = None
    if B[2] + 1.6 <= t < B[3]: msg = None
    if t > B[4]: msg = "withdraw blocked"
    bank_card(d, ly, 1180, 330, bal, a(t, B[1] + 0.6), ACC, msg)
    if t > B[5]:
        pill(d, "Balance stays safe", 1490, 760, pop(t, B[5] + 0.2), 46, ACC, DARK)
        emoji(ly, "\U0001F512", 1490, 880, 90, pop(t, B[5] + 0.4))


# 15 recap
def k15(ly, d, t, D, B):
    kw(d, ["Recap"], CX, TY, 110, t, 0.05, 0.1, {"Recap": ACC})
    items = [("class Dog:", "the blueprint", B[1]), ('Dog("Bruno")', "an object made from it", B[1] + 1.8), ("__init__", "sets up each object", B[2]),
             ("self.name", "an attribute", B[3]), ("def bark(self):", "a method", B[4]), ("my_dog.bark()", "call it with a dot", B[4] + 1.6)]
    for i, (h1, h2, st) in enumerate(items):
        p = a(t, st)
        if p <= 0: continue
        x0 = 150 if i < 3 else 990
        y0 = 320 + (i % 3) * 190
        oy = panel(d, x0, y0, x0 + 780, y0 + 160, p)
        emoji(ly, "✅", x0 + 70, int(y0 + 80 + oy), 66, p)
        d.text((x0 + 140, y0 + 56 + oy), h1, font=mono(36, True), fill=col(WHITE, p), anchor="lm")
        body(d, h2, x0 + 140, y0 + 118 + oy, 32, MUTED, p, anchor="lm")


# 16 homework
def k16(ly, d, t, D, B):
    kw(d, ["Your", "homework"], CX, TY, 104, t, 0.05, 0.1, {"homework": YELLOW})
    emoji(ly, "\U0001F393", CX, 350, 110, pop(t, B[0] + 0.3))
    for i, (code, lb, st, c) in enumerate([("class Student:", "name + marks", B[0] + 1.6, YELLOW), ("def result(self):", "a method", B[1] + 0.3, BLUE),
                                            ("marks >= 35", 'print "pass"', B[1] + 2.0, ACC)]):
        p = pop(t, st)
        if p <= 0: continue
        x = 400 + i * 560
        oy = panel(d, x - 260, 470, x + 260, 680, min(p, 1), fill=CODEBG, outline=c)
        d.text((x, 545 + oy), code, font=mono(34, True), fill=col(c, min(p, 1)), anchor="mm")
        body(d, lb, x, 625 + oy, 32, WHITE, min(p, 1))
    pill(d, "Post your code in the comments", CX, 860, pop(t, B[2]), 48, ACC, DARK)


# 17 next episode
def k17(ly, d, t, D, B):
    text(d, "NEXT EPISODE", 530, 270, 46, MUTED, a(t, 0.1), "Bold", False)
    p = a(t, 0.3)
    if p > 0:
        oy = panel(d, 110, 330, 950, 760, p, outline=BLUE)
        text(d, "Episode 12", 530, 410 + oy, 54, BLUE, p)
        d.text((530, 520 + oy), "Quiz Game", font=mono(70, True), fill=col(WHITE, p), anchor="mm")
        body(d, "A full project", 530, 615 + oy, 38, MUTED, p)
        d.text((530, 690 + oy), "score += 1", font=mono(44, True), fill=col(C_STR, p), anchor="mm")
    q_ = out(t, B[1] - 0.4, 0.4)
    for i, (em, lb, st) in enumerate([("\U0001F9E0", "Quiz questions", B[0] + 3.0), ("\U0001F9F0", "Everything so far", B[0] + 4.4)]):
        p = a(t, st) * q_
        if p <= 0: continue
        y0 = 360 + i * 240
        oy = panel(d, 1110, y0, 1800, y0 + 200, p, outline=ORANGE)
        emoji(ly, em, 1210, int(y0 + 100 + oy), 100, p)
        text(d, lb, 1290, y0 + 100 + oy, 44, WHITE, p, anchor="lm")
    pill(d, "Subscribe for Episode 12", 530, 860, pop(t, B[1]), 52, ACC, DARK)
    emoji(ly, "\U0001F514", 945, 860, 80, pop(t, B[1] + 0.4))
    emoji(ly, "\U0001F44B", 530, 975, 90, pop(t, B[2]))
