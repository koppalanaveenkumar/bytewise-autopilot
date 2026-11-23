"""Learn AI from Zero, Episode 2: if / else and loops. Each scene gets (layer, draw, t, D, B); B = sentence starts."""
from look2x import *

CX = W / 2
TY = 210
CHAPTERS = ["Intro", "Decisions", "Comparisons", "Comparisons", "The if statement", "Indentation", "else", "elif",
            "Grade checker", "Loops", "for loops", "range", "while loops", "Infinite loops", "Guessing game", "Recap and homework"]


def seg(s, c=WHITE, b=False): return (s, c, b)


def tl(lines, sched, t):
    out_ = []
    for s, (a0, a1) in zip(lines, sched):
        out_.append(s[:int(clamp((t - a0) / max(0.01, a1 - a0)) * len(s))])
    return out_


def hl(d, x0, x1, y0, size, i0, i1, c, p):
    if p <= 0: return
    lh = size * 1.45
    ya = y0 + 90 + i0 * lh - 7
    yb = y0 + 90 + (i1 + 1) * lh - 9
    d.rounded_rectangle([x0 + 18, ya, x1 - 18, yb], 10, outline=col(c, p), width=4)
    d.rounded_rectangle([x0 + 6, ya + 4, x0 + 14, yb - 4], 4, fill=col(c, p))


def vbox(d, cx, cy, name, val, p, c=YELLOW):
    if p <= 0: return
    oy = panel(d, cx - 170, cy - 70, cx + 170, cy + 70, p, outline=c)
    d.text((cx - 130, cy + oy), name, font=mono(44, True), fill=col(BLUE, p), anchor="lm")
    d.text((cx + 130, cy + oy), val, font=mono(64, True), fill=col(c, p), anchor="rm")


def note(d, x0, y0, x1, h1, h2, p, c=None, mono_head=False, size=44):
    if p <= 0: return
    oy = panel(d, x0, y0, x1, y0 + 150, p, outline=c)
    if mono_head:
        d.text((x0 + 40, y0 + 52 + oy), h1, font=mono(size, True), fill=col(c or WHITE, p), anchor="lm")
    else:
        text(d, h1, x0 + 40, y0 + 52 + oy, size, WHITE, p, anchor="lm")
    body(d, h2, x0 + 40, y0 + 112 + oy, 32, MUTED, p, anchor="lm")


# 01 ------------------------------------------------------------------
def s01(ly, d, t, D, B):
    if t < B[4] - 0.05:
        q = out(t, B[4] - 0.3, 0.25)
        kw(d, ["Apps", "decide.", "Apps", "repeat."], CX, TY, 100, t, 0.1, 0.25, {"decide.": BLUE, "repeat.": ORANGE})
        cards = [("\U0001F510", "Is the password correct?", B[1]), ("\U0001F4E7", "Should this email go to spam?", B[2]),
                 ("\U0001F4AC", "Next message... and the next...", B[3])]
        for i, (em, lb, st) in enumerate(cards):
            p = a(t, st) * q
            if p <= 0: continue
            y0 = 340 + i * 200
            oy = panel(d, 360, y0, 1560, y0 + 160, p)
            emoji(ly, em, 460, int(y0 + 80 + oy), 90, p)
            text(d, lb, 540, y0 + 80 + oy, 54, WHITE, p, anchor="lm")
    elif t < B[5] - 0.05:
        q = out(t, B[5] - 0.3, 0.25)
        kw(d, ["Two", "superpowers"], CX, TY, 104, t, B[4], 0.12, {"superpowers": YELLOW})
        for i, (em, lb, c) in enumerate([("\U0001F9E0", "Making decisions", BLUE), ("\U0001F501", "Repeating things", ORANGE)]):
            p = pop(t, B[4] + 0.5 + i * 1.2) * q
            if p <= 0: continue
            x = 560 + i * 800
            panel(d, x - 330, 380, x + 330, 820, min(p, 1), outline=c)
            emoji(ly, em, x, 540, 170, p)
            text(d, lb, x, 720, 58, WHITE, min(p, 1))
    else:
        kw(d, ["LEARN", "AI", "FROM", "ZERO"], CX, 380, 150, t, B[5], 0.12, {"ZERO": ACC})
        pill(d, "Episode 2", CX, 590, pop(t, B[5] + 0.6), 60, YELLOW, INK)
        text(d, "if / else  &  loops", CX, 770, 104, WHITE, a(t, B[5] + 0.9))


# 02 ------------------------------------------------------------------
def s02(ly, d, t, D, B):
    kw(d, ["Let's", "start", "with", "decisions"], CX, TY, 100, t, 0.05, 0.12, {"decisions": BLUE})
    body(d, "You already think like this:", CX, 330, 48, MUTED, a(t, B[1]))
    p = a(t, B[2])
    if p > 0:
        oy = panel(d, 200, 420, 900, 800, p, outline=BLUE)
        emoji(ly, "\U0001F327️", 400, 540 + oy, 120, p)
        emoji(ly, "☂️", 700, 540 + oy, 120, pop(t, B[2] + 0.8))
        text(d, "If it's raining:", 550, 680 + oy, 54, WHITE, p)
        body(d, "take an umbrella", 550, 745 + oy, 44, MUTED, p)
    p = a(t, B[3])
    if p > 0:
        oy = panel(d, 1020, 420, 1720, 800, p, outline=YELLOW)
        emoji(ly, "☀️", 1220, 540 + oy, 120, p)
        emoji(ly, "\U0001F576️", 1520, 540 + oy, 120, pop(t, B[3] + 0.6))
        text(d, "Else:", 1370, 680 + oy, 54, WHITE, p)
        body(d, "wear sunglasses", 1370, 745 + oy, 44, MUTED, p)
    pill(d, "Python checks a condition, then chooses what to do", CX, 920, a(t, B[4] + 0.3), 42, ACC, DARK)


# 03 ------------------------------------------------------------------
def s03(ly, d, t, D, B):
    if t < B[1]:
        kw(d, ["Only", "two", "answers:", "True", "or", "False"], CX, TY, 96, t, 0.1, 0.12, {"True": ACC, "False": RED})
        emoji(ly, "❓", CX, 540, 200, pop(t, 0.8))
        return
    kw(d, ["Comparison", "operators"], CX, TY, 100, t, B[1], 0.12, {"operators": ORANGE})
    ops = [(">", "greater than", B[2]), ("<", "less than", B[2] + (B[3] - B[2]) * 0.22),
           (">=", "greater or equal", B[2] + (B[3] - B[2]) * 0.42), ("<=", "less or equal", B[2] + (B[3] - B[2]) * 0.7),
           ("==", "equal to", B[3]), ("!=", "not equal", B[4])]
    for i, (sym, lb, st) in enumerate(ops):
        p = pop(t, st)
        if p <= 0: continue
        x0 = 110 + (i % 3) * 580
        y0 = 320 + (i // 3) * 175
        panel(d, x0, y0, x0 + 540, y0 + 150, min(p, 1), outline=ORANGE if i >= 4 else None)
        d.text((x0 + 120, y0 + 75), sym, font=mono(80, True), fill=col(ORANGE, min(p, 1)), anchor="mm")
        text(d, lb, x0 + 230, y0 + 75, 46, WHITE, min(p, 1), anchor="lm")
    for i, (ex, res, c, st) in enumerate([("10 > 5", "True", ACC, B[5]), ("5 == 6", "False", RED, B[6])]):
        p = a(t, st)
        if p <= 0: continue
        x0 = 230 + i * 760
        oy = panel(d, x0, 720, x0 + 700, 900, p, fill=CODEBG)
        d.text((x0 + 60, 810 + oy), ex, font=mono(70, True), fill=col(WHITE, p), anchor="lm")
        d.text((x0 + 640, 810 + oy), res, font=mono(70, True), fill=col(c, a(t, st + 0.7)), anchor="rm")


# 04 ------------------------------------------------------------------
def s04(ly, d, t, D, B):
    if t < B[2] - 0.05:
        q = out(t, B[2] - 0.3, 0.25)
        emoji(ly, "⚠️", CX, 370, 200, pop(t, 0.05) * q)
        stamp(ly, "CAREFUL!", CX, 640, a(t, 0.25, 0.16) * q, YELLOW, 120, -5)
        pill(d, "The #1 beginner mistake", CX, 880, a(t, B[1]) * q, 50, RED, WHITE)
        return
    kw(d, ["Store", "with", "one,", "compare", "with", "two"], CX, TY, 90, t, B[2] - 0.1, 0.1, {"one,": BLUE, "two": ORANGE})
    for i, (sym, h, code, c, st) in enumerate([("=", "STORES a value", "age = 21", BLUE, B[2]),
                                                ("==", "COMPARES two values", "age == 21", ORANGE, B[3])]):
        p = pop(t, st)
        if p <= 0: continue
        x0 = 160 + i * 830
        panel(d, x0, 340, x0 + 770, 820, min(p, 1), outline=c)
        d.text((x0 + 385, 470), sym, font=mono(150, True), fill=col(c, min(p, 1)), anchor="mm")
        text(d, h, x0 + 385, 620, 56, WHITE, min(p, 1))
        d.text((x0 + 385, 730), code, font=mono(56), fill=col(MUTED, min(p, 1)), anchor="mm")
    pill(d, "Store with ONE  ·  compare with TWO", CX, 940, pop(t, B[4]), 50, YELLOW, INK)


# 05 ------------------------------------------------------------------
def s05(ly, d, t, D, B):
    kw(d, ["The", "if", "statement"], CX, TY, 104, t, 0.05, 0.12, {"if": PURPLE})
    first = "age = 21" if t < B[5] + 0.4 else "age = 15"
    lines = [first, "if age >= 18:", '    print("You can vote!")']
    shown = tl(lines, [(0.4, 1.0), (B[1] + 0.3, B[1] + 1.6), (B[2] + 0.4, B[2] + 2.2)], t)
    if t >= B[5] + 0.4: shown[0] = first
    run1, run2 = B[4] + 0.6, B[5] + 1.2
    bot = code_win(d, 80, 320, 1060, shown, t, 0, 0.01, a(t, 0.2), 48, "Python", run_t=run2 if t >= run2 else run1)
    hl(d, 80, 1060, 320, 48, 0, 0, YELLOW, a(t, B[5] + 0.4) * out(t, B[5] + 2.2, 0.4))
    if t < run2:
        out_win(d, 80, bot + 30, 1060, [([seg("You can vote!", ACC, True)], run1 + 0.35)], t, a(t, run1, 0.25), 50)
    else:
        out_win(d, 80, bot + 30, 1060, [([seg("(nothing)", MUTED)], run2 + 0.35)], t, 1, 50)
    note(d, 1130, 320, 1840, "if", "the keyword that starts a decision", a(t, B[1] + 0.2), PURPLE, True, 50)
    note(d, 1130, 490, 1840, "age >= 18", "the condition: True or False?", a(t, B[1] + 1.0), ORANGE, True, 46)
    note(d, 1130, 660, 1840, ":", "a colon ends the line", a(t, B[1] + 1.8), YELLOW, True, 56)
    if t < B[5]:
        note(d, 1130, 830, 1840, "4 spaces", "this line runs only if True", a(t, B[2] + 0.3), ACC, False, 46)
    else:
        note(d, 1130, 830, 1840, "15 >= 18 is False", "so the print line is skipped", a(t, B[5] + 1.6), RED, True, 42)


# 06 ------------------------------------------------------------------
def s06(ly, d, t, D, B):
    kw(d, ["Indentation", "matters"], CX, TY, 104, t, 0.05, 0.12, {"Indentation": ACC})
    good = ["age = 21", "if age >= 18:", '    print("You can vote!")']
    bad = ["age = 21", "if age >= 18:", 'print("You can vote!")']
    code_win(d, 70, 320, 930, good, t, 0, 0.01, a(t, 0.4), 36, "correct", outline=ACC)
    p = a(t, B[1])
    if p > 0:
        lh = 36 * 1.45
        y = 320 + 90 + 2 * lh - 6
        d.rounded_rectangle([112, y, 112 + 4 * 21.7, y + lh - 8], 8, outline=col(ACC, p), width=4)
        pill(d, "4 spaces = inside the if", 500, 650, pop(t, B[1] + 0.2), 40, ACC, DARK)
    p = a(t, B[2])
    if p > 0:
        bot = code_win(d, 990, 320, 1850, bad, t, 0, 0.01, p, 36, "missing indentation", outline=RED, run_t=B[2] + 0.6)
        out_win(d, 990, bot + 30, 1850, [([seg("IndentationError: expected an", RED, True)], B[2] + 0.9),
                                         ([seg("indented block after 'if'", RED, True)], B[2] + 0.9),
                                         ([seg("statement on line 2", RED, True)], B[2] + 0.9)], t, a(t, B[2] + 0.6, 0.25), 32)
    p = a(t, B[3])
    if p > 0:
        oy = panel(d, 110, 830, 1810, 990, p, outline=ACC)
        emoji(ly, "✅", 200, int(910 + oy), 80, p)
        text(d, "Good news: Colab adds the spaces for you", 270, 880 + oy, 46, WHITE, p, anchor="lm")
        body(d, "when you press Enter after the colon", 270, 945 + oy, 36, MUTED, p, anchor="lm")


# 07 ------------------------------------------------------------------
def s07(ly, d, t, D, B):
    kw(d, ["else:", "the", "backup", "plan"], CX, TY, 100, t, 0.05, 0.12, {"else:": PURPLE})
    lines = ["age = 15", "if age >= 18:", '    print("You can vote!")', "else:", '    print(f"Not yet! You can vote in {18 - age} years.")']
    shown = tl(lines, [(0, 0.01), (0, 0.01), (0, 0.01), (B[1] + 0.3, B[1] + 0.8), (B[2] + 0.2, B[2] + 2.6)], t)
    run = B[3] - 0.3
    bot = code_win(d, 150, 300, 1770, shown, t, 0, 0.01, a(t, 0.1), 40, "Python", run_t=run)
    hl(d, 150, 1770, 300, 40, 3, 4, PURPLE, a(t, B[1] + 0.3) * out(t, B[3] - 0.3))
    if t < run:
        out_win(d, 150, bot + 26, 1770, [([seg("(nothing)", MUTED)], 0)], t, a(t, 0.2), 44)
        emoji(ly, "\U0001F610", 1660, int(bot + 100), 80, pop(t, 0.6) * out(t, run - 0.2))
    else:
        out_win(d, 150, bot + 26, 1770, [([seg("Not yet! You can vote in 3 years.", ACC, True)], run + 0.35)], t, 1, 44)
    if t < B[5]:
        pill(d, "else = if the condition is False, do this instead", CX, 950, a(t, B[2]), 42, PURPLE, WHITE)
    else:
        hl(d, 150, 1770, 300, 40, 4, 4, YELLOW, a(t, B[5]))
        pill(d, "The f-string did the math: 18 - 15 = 3", CX, 950, pop(t, B[5] + 0.3), 44, YELLOW, INK)


# 08 ------------------------------------------------------------------
def traffic(d, cx, cy, on, p):
    if p <= 0: return
    oy = panel(d, cx - 130, cy - 330, cx + 130, cy + 330, p, fill=(20, 22, 30), r=60)
    for i, c in enumerate([RED, YELLOW, ACC]):
        y = cy - 210 + i * 210 + oy
        lit = on == i
        if lit:
            d.ellipse([cx - 115, y - 115, cx + 115, y + 115], fill=col(c, 0.22 * p))
        d.ellipse([cx - 85, y - 85, cx + 85, y + 85], fill=col(c if lit else tuple(v // 4 for v in c), p))


def s08(ly, d, t, D, B):
    if t < B[1]:
        kw(d, ["More", "than", "two", "choices?"], CX, TY, 100, t, 0.05, 0.12, {"choices?": YELLOW})
    else:
        kw(d, ["Use", "elif", "(else", "if)"], CX, TY, 100, t, B[1], 0.12, {"elif": PURPLE})
    on = 0 if t >= B[4] else -1
    if t >= B[5]: on = 1
    if t >= B[6]: on = 2
    traffic(d, 300, 640, on, a(t, B[3] - 0.2))
    lines = ['if light == "red":', '    print("Stop")', 'elif light == "yellow":', '    print("Get ready")', "else:", '    print("Go")']
    shown = tl(lines, [(B[1] + 0.2 + k * 0.45, B[1] + 0.6 + k * 0.45) for k in range(6)], t)
    code_win(d, 620, 320, 1840, shown, t, 0, 0.01, a(t, B[1]), 46, "Python")
    if on >= 0:
        hl(d, 620, 1840, 320, 46, on * 2, on * 2 + 1, [RED, YELLOW, ACC][on], 1)
        word = ["STOP", "GET READY", "GO"][on]
        pill(d, word, 1230, 960, pop(t, [B[4], B[5], B[6]][on] + 0.2), 56, [RED, YELLOW, ACC][on], INK if on else WHITE)
    elif t >= B[2]:
        pill(d, "Top to bottom: only the FIRST True one runs", 1230, 960, a(t, B[2]), 40, PANEL, WHITE)


# 09 ------------------------------------------------------------------
def s09(ly, d, t, D, B):
    kw(d, ["Mini", "practice:", "grade", "checker"], CX, TY, 96, t, 0.05, 0.1, {"grade": YELLOW, "checker": YELLOW})
    lines = ['marks = int(input("Enter your marks: "))', "if marks >= 90:", '    print("Grade A")', "elif marks >= 80:",
             '    print("Grade B")', "elif marks >= 65:", '    print("Grade C")', "else:", '    print("Keep practising!")']
    sch = [(B[1] + 0.2, B[1] + 2.0), (B[2], B[2] + 1.0), (B[2] + 1.0, B[2] + 1.8), (B[3], B[3] + 0.9), (B[3] + 0.9, B[3] + 1.6),
           (B[4], B[4] + 1.0), (B[4] + 1.0, B[4] + 1.7), (B[5], B[5] + 0.5), (B[5] + 0.5, B[5] + 1.4)]
    shown = tl(lines, sch, t)
    run = B[6] + 0.2
    code_win(d, 60, 290, 1110, shown, t, 0, 0.01, a(t, 0.3), 36, "Python", run_t=run)
    hl(d, 60, 1110, 290, 36, 1, 1, RED, a(t, B[7]) * out(t, B[9]))
    hl(d, 60, 1110, 290, 36, 3, 4, ACC, a(t, B[9]))
    out_win(d, 1170, 290, 1860, [([seg("Enter your marks: ", WHITE), seg("84", ACC, True)], run + 0.8),
                                 ([seg("Grade B", YELLOW, True)], B[11] + 0.6)], t, a(t, run, 0.25), 42)
    rows = [("84 >= 90 ?", "No", RED, B[7], B[8]), ("84 >= 80 ?", "Yes!", ACC, B[9], B[10])]
    for i, (q_, ans, c, st, at) in enumerate(rows):
        p = a(t, st)
        if p <= 0: continue
        y0 = 560 + i * 170
        oy = panel(d, 1170, y0, 1860, y0 + 140, p)
        d.text((1210, y0 + 70 + oy), q_, font=mono(48, True), fill=col(WHITE, p), anchor="lm")
        d.text((1820, y0 + 70 + oy), ans, font=font(56), fill=col(c, a(t, at)), anchor="rm")
    pill(d, "Stops checking right there", 1515, 925, pop(t, B[11] + 1.2), 42, ACC, DARK)


# 10 ------------------------------------------------------------------
def s10(ly, d, t, D, B):
    kw(d, ["Part", "2:", "Loops"], CX, TY, 110, t, 0.05, 0.15, {"Loops": ORANGE})
    emoji(ly, "\U0001F501", 1430, TY, 90, pop(t, 0.6))
    lines = ['print("Hello")'] * 5
    shown = tl(lines, [(B[2] + k * 0.45, B[2] + 0.35 + k * 0.45) for k in range(5)], t)
    code_win(d, 120, 330, 900, shown, t, 0, 0.01, a(t, B[1]), 44, "copy, copy, copy...")
    if t >= B[3]:
        n = int(clamp((t - B[3]) / 1.6) ** 1.6 * 1000)
        text(d, f"x {n:,}", 1380, 470, 170, RED, a(t, B[3], 0.2))
        emoji(ly, "\U0001F635", 1380, 690, 150, pop(t, B[3] + 1.0))
    pill(d, "A loop repeats code, without repeating yourself", CX, 950, pop(t, B[4]), 46, ACC, DARK)


# 11 ------------------------------------------------------------------
def s11(ly, d, t, D, B):
    kw(d, ["The", "for", "loop"], CX, TY, 110, t, 0.05, 0.12, {"for": ORANGE})
    shown = tl(["for i in range(5):", "    print(i)"], [(B[1] + 0.3, B[1] + 2.0), (B[1] + 2.4, B[1] + 3.4)], t)
    code_win(d, 90, 320, 1000, shown, t, 0, 0.01, a(t, 0.3), 54, "Python", run_t=B[3] - 0.1)
    st = B[3] + 0.1
    step = max(0.4, (B[4] - B[3] - 0.3) / 5)
    k = int(clamp((t - st) / (step * 5)) * 5) if t >= st else -1
    items = [([seg(str(n), WHITE if n else YELLOW, True)], st + n * step) for n in range(5)]
    out_win(d, 1080, 320, 1830, items, t, a(t, st - 0.2, 0.25), 48)
    if t >= st:
        vbox(d, 545, 700, "i =", str(min(4, max(0, k))), a(t, st, 0.2))
        emoji(ly, "\U0001F501", 820, 700, 90, a(t, st, 0.2))
    pill(d, "5 numbers... starting at 0!", 545, 870, pop(t, B[4]), 44, YELLOW, INK)
    pill(d, "In programming, counting usually starts from 0", CX, 985, a(t, B[5]), 40, PANEL, WHITE)


# 12 ------------------------------------------------------------------
def s12(ly, d, t, D, B):
    if t < B[3] - 0.05:
        q = out(t, B[3] - 0.3, 0.25)
        kw(d, ["Start", "at", "1:", "range(1,", "6)"], CX, TY, 100, t, 0.05, 0.1, {"range(1,": ORANGE, "6)": ORANGE})
        for n in range(7):
            x = 330 + n * 210
            inc = 1 <= n <= 5
            lit = inc and t >= B[1] + 0.3 + (n - 1) * 0.35
            stop = n == 6 and t >= B[2]
            p = a(t, 0.3 + n * 0.06) * q
            if p <= 0: continue
            c = ACC if lit else (RED if stop else (60, 72, 120))
            d.ellipse([x - 80, 480, x + 80, 640], fill=col(PANEL, p), outline=col(c, p), width=8)
            d.text((x, 560), str(n), font=mono(80, True), fill=col(c if (lit or stop) else MUTED, p), anchor="mm")
            if stop:
                d.line([x - 60, 500, x + 60, 620], fill=col(RED, p), width=10)
        pill(d, "Counts 1 to 5", 980, 760, pop(t, B[1] + 1.8) * q, 48, ACC, DARK)
        pill(d, "The stop number is never included", CX, 900, a(t, B[2] + 0.4) * q, 44, RED, WHITE)
        return
    kw(d, ["A", "multiplication", "table"], CX, TY, 100, t, B[3], 0.1, {"multiplication": YELLOW})
    shown = tl(["for i in range(1, 11):", '    print(f"7 x {i} = {7 * i}")'], [(B[4] + 0.2, B[4] + 1.6), (B[4] + 1.8, B[5] - 0.1)], t)
    code_win(d, 70, 320, 1020, shown, t, 0, 0.01, a(t, B[3]), 44, "Python", run_t=B[5] + 0.3)
    items = [([seg(f"7 x {i} = ", WHITE), seg(str(7 * i), YELLOW, True)], B[5] + 0.5 + i * 0.12) for i in range(1, 11)]
    out_win(d, 1090, 300, 1840, items, t, a(t, B[5] + 0.3, 0.25), 36)
    emoji(ly, "⚡", 545, 700, 120, pop(t, B[5] + 1.2))
    body(d, "10 lines of output from 2 lines of code", 545, 830, 40, MUTED, a(t, B[5] + 1.6))


# 13 ------------------------------------------------------------------
def s13(ly, d, t, D, B):
    kw(d, ["The", "while", "loop"], CX, TY, 110, t, 0.05, 0.12, {"while": ORANGE})
    pill(d, "Repeats as long as the condition is True", CX, 330, a(t, B[1]), 40, PANEL, WHITE)
    lines = ["count = 3", "while count > 0:", "    print(count)", "    count = count - 1", 'print("Lift off!")']
    sch = [(B[3], B[3] + 0.8), (B[4], B[4] + 1.2), (B[4] + 1.3, B[4] + 2.2), (B[4] + 2.3, B[4] + 3.4), (B[4] + 3.5, B[5] - 0.2)]
    shown = tl(lines, sch, t)
    code_win(d, 70, 410, 1020, shown, t, 0, 0.01, a(t, B[2]), 44, "Python", run_t=B[5] - 0.1)
    step = max(0.45, (B[6] - B[5]) / 3.2)
    items = [([seg(str(3 - k), WHITE, True)], B[5] + 0.1 + k * step) for k in range(3)]
    items.append(([seg("Lift off!", ACC, True)], B[6] + 2.6))
    out_win(d, 1090, 410, 1840, items, t, a(t, B[5] - 0.1, 0.25), 48)
    if t >= B[5]:
        k = int((t - B[5] - 0.1) / step) if t > B[5] + 0.1 else 0
        val = max(0, 3 - min(3, k)) if t < B[6] + 0.8 else 0
        vbox(d, 300, 955, "count", str(val), a(t, B[5], 0.2), RED if val == 0 else YELLOW)
    if t >= B[6] + 0.8:
        pill(d, "0 > 0 is False: the loop stops", 1000, 955, pop(t, B[6] + 0.8), 40, RED, WHITE)
        emoji(ly, "\U0001F680", 1750, 760, 110, pop(t, B[6] + 2.6))


# 14 ------------------------------------------------------------------
def s14(ly, d, t, D, B):
    emoji(ly, "⚠️", 590, TY, 100, pop(t, 0.05))
    kw(d, ["One", "warning"], CX + 60, TY, 100, t, 0.1, 0.12, {"warning": YELLOW})
    code_win(d, 70, 330, 1000, ["count = 3", "while count > 0:", "    print(count)"], t, 0, 0.01, a(t, B[1] - 0.3), 44, "count never changes!", outline=RED, run_t=B[1] + 0.8)
    if t >= B[1] + 1.0:
        n = int((t - B[1] - 1.0) / 0.12)
        rows = min(8, n + 1)
        oy = panel(d, 1080, 330, 1840, 860, 1, fill=(14, 18, 40), r=26)
        d.text((1120, 366), "Output", font=font(30, "Bold", False), fill=col(MUTED, 1), anchor="lm")
        for r in range(rows):
            d.text((1124, 410 + r * 54), "3", font=mono(44, True), fill=col(WHITE, 1))
        if n >= 8:
            d.text((1460, 640), "...forever", font=font(56), fill=col(RED, 1), anchor="mm")
    stamp(ly, "INFINITE LOOP", CX, 560, a(t, B[2], 0.16) * out(t, B[3] + 0.6, 0.3), RED, 96, -6)
    p = a(t, B[3])
    if p > 0:
        oy = panel(d, 220, 900, 1700, 1020, p, outline=ACC)
        d.ellipse([280, 922 + oy, 356, 998 + oy], fill=col(RED, p))
        d.rectangle([302, 944 + oy, 334, 976 + oy], fill=col(WHITE, p))
        text(d, "Don't panic: in Colab, click the stop button next to the cell", 390, 960 + oy, 38, WHITE, a(t, B[4] - 0.4) * p + (0.35 * p if t < B[4] - 0.4 else 0), anchor="lm")


# 15 ------------------------------------------------------------------
def s15(ly, d, t, D, B):
    if t < B[16]:
        kw(d, ["Mini", "project:", "guessing", "game"], CX, TY, 96, t, 0.05, 0.1, {"guessing": ACC, "game": ACC})
    else:
        kw(d, ["Loops", "+", "decisions", "=", "a", "real", "game"], CX, TY, 90, t, B[16], 0.08, {"game": ACC})
    emoji(ly, "\U0001F3AF", 1830, TY, 80, pop(t, 0.7))
    lines = ["secret = 7", "while True:", '    guess = int(input("Guess the number: "))', "    if guess == secret:",
             '        print("You got it!")', "        break", "    elif guess < secret:", '        print("Too low!")',
             "    else:", '        print("Too high!")']
    sch = [(B[1], B[1] + 0.7), (B[2], B[2] + 0.8), (B[3], B[3] + 1.4), (B[4], B[4] + 0.9), (B[4] + 1.0, B[4] + 1.8),
           (B[5], B[5] + 0.5), (B[7], B[7] + 0.9), (B[7] + 1.0, B[7] + 1.7), (B[8], B[8] + 0.4), (B[8] + 0.5, B[8] + 1.2)]
    shown = tl(lines, sch, t)
    run = B[9]
    code_win(d, 50, 290, 1110, shown, t, 0, 0.01, a(t, 0.3), 34, "Python", run_t=run)
    hl(d, 50, 1110, 290, 34, 1, 1, ORANGE, a(t, B[2]) * out(t, B[3]))
    hl(d, 50, 1110, 290, 34, 5, 5, RED, a(t, B[5] + 0.3) * out(t, B[7]))
    if t >= B[11]: hl(d, 50, 1110, 290, 34, 6, 7, BLUE, a(t, B[11]) * out(t, B[12]))
    if t >= B[13]: hl(d, 50, 1110, 290, 34, 8, 9, ORANGE, a(t, B[13]) * out(t, B[14]))
    if t >= B[15]: hl(d, 50, 1110, 290, 34, 3, 5, ACC, a(t, B[15]))
    if t < run:
        pill(d, "break = stop the loop right now", 1485, 560, pop(t, B[6]) * out(t, run - 0.3), 40, RED, WHITE)
        pill(d, "while True = loop until we say stop", 1485, 420, a(t, B[2] + 0.5) * out(t, run - 0.3), 38, ORANGE, INK)
    items = [([seg("Guess the number: ", WHITE), seg("4", ACC, True)], B[10]),
             ([seg("Too low!", BLUE, True)], B[11] + 0.2),
             ([seg("Guess the number: ", WHITE), seg("9", ACC, True)], B[12]),
             ([seg("Too high!", ORANGE, True)], B[13] + 0.2),
             ([seg("Guess the number: ", WHITE), seg("7", ACC, True)], B[14]),
             ([seg("You got it!", ACC, True)], B[15] + 0.2)]
    out_win(d, 1150, 290, 1860, items, t, a(t, run, 0.25), 38)
    emoji(ly, "\U0001F389", 1505, 820, 130, pop(t, B[15] + 0.4))


# 16 ------------------------------------------------------------------
def s16(ly, d, t, D, B):
    if t < B[8] - 0.05:
        q = out(t, B[8] - 0.3, 0.25)
        kw(d, ["Recap"], CX, TY, 110, t, 0.05, 0.1, {"Recap": ACC})
        items = [("Conditions", "are True or False", B[1]), ("==  compares", "=  stores a value", B[2]),
                 ("if / elif / else", "make decisions", B[3]), ("for + range", "repeats, counting from 0", B[4]),
                 ("while", "repeats while True", B[5]), ("break", "stops a loop", B[6])]
        for i, (h1, h2, st) in enumerate(items):
            p = a(t, st) * q
            if p <= 0: continue
            x0 = 150 if i < 3 else 990
            y0 = 320 + (i % 3) * 170
            oy = panel(d, x0, y0, x0 + 780, y0 + 145, p)
            emoji(ly, "✅", x0 + 70, int(y0 + 72 + oy), 66, p)
            d.text((x0 + 140, y0 + 52 + oy), h1, font=mono(44, True), fill=col(WHITE, p), anchor="lm")
            body(d, h2, x0 + 140, y0 + 108 + oy, 34, MUTED, p, anchor="lm")
        pill(d, "Don't forget the colon  :  and the indentation!", CX, 880 + 60, pop(t, B[7]) * q, 42, YELLOW, INK)
    elif t < B[11] - 0.05:
        q = out(t, B[11] - 0.3, 0.25)
        kw(d, ["Your", "homework"], CX, TY, 100, t, B[8], 0.1, {"homework": YELLOW})
        emoji(ly, "\U0001F4DD", CX, 370, 130, pop(t, B[8] + 0.2) * q)
        p = a(t, B[8] + 0.5) * q
        if p > 0:
            oy = panel(d, 260, 470, 1660, 650, p, outline=YELLOW)
            text(d, "Loop through 1 to 10:", CX, 525 + oy, 60, WHITE, p)
            body(d, "print whether each number is even or odd", CX, 600 + oy, 44, MUTED, p)
        p = a(t, B[9]) * q
        if p > 0:
            oy = panel(d, 460, 690, 1460, 830, p, fill=CODEBG, outline=ORANGE)
            d.text((CX, 760 + oy), "n % 2 == 0  means even", font=mono(54, True), fill=col(ORANGE, p), anchor="mm")
        pill(d, "Post your code in the comments", CX, 920, a(t, B[10]) * q, 44, PANEL, WHITE)
    else:
        text(d, "NEXT EPISODE", CX, 270, 50, MUTED, a(t, B[11]), "Bold", False)
        p = a(t, B[11] + 0.2)
        if p > 0:
            oy = panel(d, 300, 360, 1620, 700, p, outline=BLUE)
            text(d, "Episode 3", CX, 450 + oy, 56, BLUE, p)
            d.text((CX, 560 + oy), "Lists", font=mono(110, True), fill=col(WHITE, p), anchor="mm")
            body(d, "Store many values in one place", CX, 650 + oy, 44, MUTED, p)
        pill(d, "Subscribe: @heybytewise", CX, 830, pop(t, B[12]), 56, ACC, DARK)
        emoji(ly, "\U0001F514", CX + 490, 830, 90, pop(t, B[12] + 0.4))
        emoji(ly, "\U0001F44B", CX, 960, 100, pop(t, B[13]))
