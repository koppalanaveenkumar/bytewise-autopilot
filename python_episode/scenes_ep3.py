"""Python for Beginners, Episode 3: Lists. Each scene gets (layer, draw, t, D, B); B = sentence starts within the scene."""
from scenes2 import *
import look2x as L

L.KEYWORDS.update({"for", "in", "while", "break", "elif"})
L.BUILTINS.update({"len", "sum", "max"})

CHAPTERS = ["Intro", "Why lists?", "What is a list?", "Index", "Last item and errors", "Change, add and remove",
            "Change, add and remove", "Count with len", "Lists of numbers", "Loop through a list", "Check with in",
            "To-do list app", "To-do list app", "Recap", "Homework", "Next episode"]
GREY = (70, 84, 140)


def q(s): return f'"{s}"'


def xs(n, sp=380): return [CX + (i - (n - 1) / 2) * sp for i in range(n)]


def cell(d, cx, y, al, labels, oc=GREY, w=340, h=118, size=40, yo=0, fillc=PANEL):
    """A box in a list. labels: list of (text, colour, alpha, y offset)."""
    if al <= 0: return
    al = clamp(al)
    x0, x1 = cx - w / 2, cx + w / 2
    d.rounded_rectangle([x0 + 6, y - h / 2 + yo + 8, x1 + 6, y + h / 2 + yo + 8], 22, fill=(0, 0, 0, int(70 * al)))
    d.rounded_rectangle([x0, y - h / 2 + yo, x1, y + h / 2 + yo], 22, fill=col(fillc, al), outline=col(oc, al), width=5)
    for s, c, la, dy in labels:
        if la * al > 0.01:
            d.text((cx, y + yo + dy), s, font=mono(size, True), fill=col(c, al * clamp(la)), anchor="mm")


def lab(d, cx, y, s, al, c=MUTED, size=40):
    if al > 0: d.text((cx, y), s, font=mono(size, True), fill=col(c, clamp(al)), anchor="mm")


def badge(d, cx, cy, s, p, c=ACC, fg=DARK, r=34):
    if p <= 0: return
    k = min(p, 1.1)
    d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], fill=col(c, min(p, 1)))
    d.text((cx, cy), s, font=font(int(36 * k) + 1), fill=col(fg, min(p, 1)), anchor="mm")


SONGS = ["Sunrise", "Monsoon", "Chai Time"]


# 01 Intro ---------------------------------------------------------------
def k01(ly, d, t, D, B):
    # B0 phone keeps... B1 How does a program remember... B2 With lists. B3 In five minutes... B4 In episode two... B5 Today...
    if t < B[2] - 0.05:
        if t < B[1]:
            kw(d, ["Your", "phone", "remembers", "a", "lot"], CX, TY, 104, t, 0.1, 0.12, {"lot": YELLOW})
        else:
            kw(d, ["How", "does", "a", "program", "remember", "it", "all?"], CX, TY, 96, t, B[1], 0.09, {"program": BLUE})
        dim = 1 - 0.45 * a(t, B[1] + 0.3)
        for i, (em, lb, n, c) in enumerate([("\U0001F3B5", "Songs", 248, ORANGE), ("\U0001F465", "Contacts", 512, BLUE),
                                            ("\U0001F4AC", "Messages", 1904, ACC)]):
            st = B[0] + 0.5 + i * 0.7
            p = pop(t, st)
            if p <= 0: continue
            x = 420 + i * 540
            panel(d, x - 230, 360, x + 230, 800, min(p, 1) * dim, outline=c)
            emoji(ly, em, x, 480, 130, p)
            text(d, lb, x, 630, 50, WHITE, min(p, 1) * dim)
            v = int(n * clamp((t - st) / 1.3))
            text(d, f"{v:,}", x, 715, 60, c, min(p, 1) * dim)
        emoji(ly, "❓", CX, 935, 120, pop(t, B[1] + 0.8))
    elif t < B[3] - 0.05:
        q_ = out(t, B[3] - 0.3, 0.25)
        kw(d, ["With", "lists!"], CX, 470, 210, t, B[2], 0.15, {"lists!": YELLOW})
        p = a(t, B[2] + 0.5) * q_
        if p > 0:
            d.text((CX, 720), '[ "song", "song", "song", ... ]', font=mono(64, True), fill=col(C_STR, p), anchor="mm")
    elif t < B[4] - 0.05:
        q_ = out(t, B[4] - 0.3, 0.25)
        kw(d, ["In", "5", "minutes,", "you'll..."], CX, TY, 100, t, B[3], 0.1, {"5": YELLOW})
        for i, (em, lb, c, st) in enumerate([("\U0001F4CB", "Learn lists", BLUE, B[3] + 0.6), ("✅", "Build a to-do list app", ACC, B[3] + 2.0)]):
            p = pop(t, st) * q_
            if p <= 0: continue
            x = 560 + i * 800
            panel(d, x - 340, 360, x + 340, 820, min(p, 1), outline=c)
            emoji(ly, em, x, 530, 170, p)
            text(d, lb, x, 720, 56, WHITE, min(p, 1))
    else:
        kw(d, ["Python", "for", "Beginners"], CX, 300, 130, t, B[4], 0.12, {"Python": YELLOW})
        pill(d, "Episode 3:  Lists", CX, 480, pop(t, B[4] + 0.5), 58, ACC, DARK)
        steps = [("Episode 1", "Store information", B[4] + 1.0, MUTED, None), ("Episode 2", "Decide & repeat", B[4] + 2.2, MUTED, None),
                 ("Episode 3", "Remember many things", B[5] + 0.3, WHITE, ACC)]
        for i, (h1, h2, st, c, oc) in enumerate(steps):
            p = a(t, st)
            if p <= 0: continue
            x = 400 + i * 560
            oy = panel(d, x - 250, 620, x + 250, 820, p, outline=oc)
            text(d, h1, x, 680 + oy, 40, ACC if oc else MUTED, p, "Bold", False)
            text(d, h2, x, 750 + oy, 38, c, p)
            if i < 2:
                text(d, "→", x + 280, 720, 60, MUTED, a(t, steps[i + 1][2]))


# 02 Why lists? -----------------------------------------------------------
def k02(ly, d, t, D, B):
    # B0 Say you want to store... B1 So far... song one, two, three. B2 Now imagine 500. B3 That's a mess.
    kw(d, ["Storing", "many", "songs"], CX, TY, 104, t, 0.05, 0.12, {"many": ORANGE})
    s = B[1] + 2.2
    shown = tl(['song1 = "Sunrise"', 'song2 = "Monsoon"', 'song3 = "Chai Time"'], [(s, s + 0.9), (s + 1.0, s + 1.9), (s + 2.0, s + 3.0)], t)
    code_win(d, 90, 320, 1000, shown, t, 0, 0.01, a(t, 0.3), 50, "Python")
    body(d, "One variable for every song", 545, 720, 44, MUTED, a(t, B[1] + 0.4))
    p = a(t, B[2])
    if p > 0:
        oy = panel(d, 1080, 320, 1840, 860, p, fill=CODEBG, r=26)
        top = 4 + int(clamp((t - B[2] - 0.2) / 2.4) ** 1.6 * 488)
        for j in range(9):
            n = top + j
            d.text((1124, 360 + oy + j * 52), f'song{n} = "..."', font=mono(36), fill=col(MUTED if j < 8 else WHITE, p))
        text(d, f"{top + 8} variables!", 545, 830, 72, RED, a(t, B[2] + 0.6))
    stamp(ly, "MESSY!", 1460, 590, a(t, B[3], 0.16), RED, 120, -8)


# 03 What is a list? -------------------------------------------------------
def k03(ly, d, t, D, B):
    # B0 A list stores many values... B1 Think of a playlist... B2 To make a list... B3 Inside... B4 Print it... B5 Don't worry...
    if t < B[2] - 0.05:
        q_ = out(t, B[2] - 0.3, 0.25)
        kw(d, ["A", "list", "=", "many", "values,", "one", "name"], CX, TY, 96, t, 0.05, 0.1, {"list": YELLOW})
        p = a(t, B[0] + 1.6) * q_
        if p > 0:
            oy = panel(d, 640, 300, 1180, 1010, p, fill=(12, 15, 34), outline=(90, 104, 160), r=48)
            d.rounded_rectangle([850, 318 + oy, 970, 334 + oy], 8, fill=col((60, 70, 110), p))
            emoji(ly, "\U0001F3B5", 720, int(400 + oy), 60, p)
            text(d, "My Playlist", 770, 400 + oy, 50, WHITE, p, anchor="lm")
            for i, s in enumerate(SONGS):
                pr = a(t, B[0] + 2.0 + i * 0.35) * q_
                if pr <= 0: continue
                y0 = 480 + i * 140 + oy
                d.rounded_rectangle([680, y0, 1140, y0 + 115], 22, fill=col(PANEL, pr))
                d.text((730, y0 + 58), str(i + 1), font=mono(44, True), fill=col(MUTED, pr), anchor="mm")
                text(d, s, 790, y0 + 58, 46, WHITE, pr, "Bold", False, anchor="lm")
        pill(d, "← one name", 1480, 400, pop(t, B[1] + 2.0) * q_, 44, YELLOW, INK)
        pill(d, "← many songs, in order", 1500, 620, pop(t, B[1] + 3.2) * q_, 44, ACC, DARK)
        return
    kw(d, ["Make", "a", "list"], CX, TY, 104, t, B[2], 0.12, {"list": YELLOW})
    shown = tl(['playlist = ["Sunrise", "Monsoon", "Chai Time"]', "print(playlist)"],
               [(B[2] + 0.3, B[3] + 2.6), (B[4] + 0.05, B[4] + 0.9)], t)
    code_win(d, 120, 300, 1800, shown, t, 0, 0.01, a(t, B[2]), 46, "Python", run_t=B[4] + 1.0)
    items = [([seg("['Sunrise', 'Monsoon', 'Chai Time']", WHITE, True)], B[4] + 1.2)]
    out_win(d, 120, 600, 1800, items, t, a(t, B[4] + 1.0, 0.25), 46)
    pill(d, "[ ]  square brackets", 560, 860, pop(t, B[2] + 2.4), 42, ORANGE, INK)
    pill(d, ",  commas between values", 1360, 860, pop(t, B[3] + 1.2), 42, BLUE, WHITE)
    pill(d, "'Sunrise' and \"Sunrise\" are the same text", CX, 975, a(t, B[5] + 0.4), 40, YELLOW, INK)


# 04 Index -------------------------------------------------------------------
def k04(ly, d, t, D, B):
    # B0 Every item has an index. B1 starts at zero. B2 Write list name then index. B3 Index zero... B4 Index two...
    kw(d, ["Every", "item", "has", "an", "index"], CX, TY, 104, t, 0.05, 0.1, {"index": YELLOW})
    X = xs(3, 400)
    for i, s in enumerate(SONGS):
        hi_ = (i == 0 and t >= B[3]) or (i == 2 and t >= B[4])
        cell(d, X[i], 420, a(t, B[0] + 0.3 + i * 0.15), [(q(s), C_STR, 1, 0)], YELLOW if hi_ else GREY, 360)
        lab(d, X[i], 535, str(i), pop(t, B[0] + 1.6 + i * 0.35), YELLOW, 48)
    pill(d, "Counting starts at 0, like range()", CX, 640, pop(t, B[1] + 0.8) * out(t, B[2] - 0.2, 0.25), 44, YELLOW, INK)
    shown = tl(["print(playlist[0])", "print(playlist[2])"], [(B[2] + 0.6, B[2] + 2.4), (B[4] + 0.05, B[4] + 1.0)], t)
    code_win(d, 160, 650, 1040, shown, t, 0, 0.01, a(t, B[2]), 48, "Python", run_t=B[3] - 0.1)
    items = [([seg("Sunrise", WHITE, True)], B[3] + 0.5), ([seg("Chai Time", WHITE, True)], B[4] + 1.2)]
    out_win(d, 1100, 650, 1760, items, t, a(t, B[3] - 0.1, 0.25), 48)


# 05 Last item and errors -----------------------------------------------------
def k05(ly, d, t, D, B):
    # B0 Want the last song? B1 Use minus one. B2 ask for index three... error. B3 no fourth song. B4 last index is one less...
    if t < B[2] - 0.05:
        kw(d, ["The", "last", "item"], CX, TY, 104, t, 0.05, 0.12, {"last": YELLOW})
    else:
        kw(d, ["Index", "out", "of", "range"], CX, TY, 100, t, B[2], 0.1, {"range": RED})
    X = xs(4, 390)
    for i, s in enumerate(SONGS):
        hi_ = i == 2 and B[1] + 0.8 <= t < B[2]
        cell(d, X[i], 430, 1, [(q(s), C_STR, 1, 0)], YELLOW if hi_ else GREY, 350)
        lab(d, X[i], 536, str(i), 1, MUTED, 44)
        lab(d, X[i], 326, str(i - 3), pop(t, B[1] + 0.3 + i * 0.2), ORANGE, 44)
    pg = a(t, B[2] + 1.2)
    if pg > 0:
        x = X[3]
        d.rounded_rectangle([x - 175, 371, x + 175, 489], 22, outline=col(RED, pg), width=5)
        d.text((x, 430), "?", font=font(70), fill=col(RED, pg), anchor="mm")
        lab(d, x, 536, "3", pg, RED, 44)
        emoji(ly, "❌", int(x + 150), 380, 70, pop(t, B[3]))
    shown = tl(["print(playlist[-1])", "print(playlist[3])"], [(B[1] + 0.4, B[1] + 1.8), (B[2] + 0.4, B[2] + 1.8)], t)
    code_win(d, 90, 640, 900, shown, t, 0, 0.01, 1, 44, "Python", run_t=B[1] + 2.0)
    items = [([seg("Chai Time", WHITE, True)], B[1] + 2.2), ([seg("IndexError: list index out of range", RED, True)], B[2] + 2.2)]
    out_win(d, 960, 640, 1840, items, t, a(t, B[1] + 2.0, 0.25), 34)
    pill(d, "3 items  →  last index is 2", CX, 965, pop(t, B[4] + 0.3), 46, YELLOW, INK)


# 06 Change an item -------------------------------------------------------------
def k06(ly, d, t, D, B):
    # B0 change an item. B1 index and one equals sign. B2 Set index one to Rainy Day...
    kw(d, ["Change", "an", "item"], CX, TY, 104, t, 0.05, 0.12, {"Change": ACC})
    X = xs(3, 400)
    k = a(t, B[2] + 1.6, 0.35)
    for i, s in enumerate(SONGS):
        if i == 1:
            oc = ACC if k > 0.5 else (YELLOW if t >= B[1] + 0.6 else GREY)
            cell(d, X[i], 420, 1, [(q("Monsoon"), C_STR, 1 - k, -50 * k), (q("Rainy Day"), C_STR, k, 50 * (1 - k))], oc, 360)
        else:
            cell(d, X[i], 420, 1, [(q(s), C_STR, 1, 0)], GREY, 360)
        lab(d, X[i], 535, str(i), 1, YELLOW if i == 1 else MUTED, 44)
    shown = tl(['playlist[1] = "Rainy Day"'], [(B[1] + 0.4, B[2] + 1.2)], t)
    code_win(d, 360, 640, 1560, shown, t, 0, 0.01, a(t, B[0] + 0.3), 52, "Python")
    pill(d, "One = puts a new value in", CX, 920, pop(t, B[1] + 1.0), 44, YELLOW, INK)


# 07 Grow and shrink -------------------------------------------------------------
def k07(ly, d, t, D, B):
    # B0 grow and shrink. B1 Append adds... B2 append Night Drive... B3 Remove deletes... B4 remove Sunrise...
    kw(d, ["Grow", "and", "shrink"], CX, TY, 104, t, 0.05, 0.12, {"Grow": ACC, "shrink": RED})
    ta, tr = B[2] + 2.6, B[4] + 2.0
    ka, kr, ks = a(t, ta, 0.45), a(t, tr, 0.4), a(t, tr + 0.35, 0.45)
    names = ["Sunrise", "Rainy Day", "Chai Time", "Night Drive"]
    p3, p4 = xs(3, 380), xs(4, 380)
    for i, s in enumerate(names):
        if i < 3:
            x = p3[i] + (p4[i] - p3[i]) * ka
        else:
            x = p4[3] + (1 - ka) * 320
        al, yo, oc = 1.0, 0, GREY
        if i == 3:
            al, oc = ka, ACC
        if i == 0:
            al, yo = 1 - kr, 80 * kr
            if t >= tr - 0.7: oc = RED
        if i > 0:
            x = x + (p3[i - 1] - p4[i]) * ks
        cell(d, x, 430, al, [(q(s), C_STR, 1, 0)], oc, 340, size=38, yo=yo)
        ix = i - (1 if ks > 0.5 and i > 0 else 0)
        if i > 0 or kr < 0.5:
            lab(d, x, 540, str(ix), al * (1 if i < 3 else ka), MUTED, 40)
    shown = tl(['playlist.append("Night Drive")', 'playlist.remove("Sunrise")'], [(B[2] + 0.2, B[2] + 2.3), (B[4] + 0.1, B[4] + 1.8)], t)
    code_win(d, 300, 620, 1620, shown, t, 0, 0.01, a(t, B[1]), 46, "Python")
    pill(d, "append = add to the end", 560, 960, pop(t, B[1] + 0.3), 42, ACC, DARK)
    pill(d, "remove = delete by value", 1360, 960, pop(t, B[3] + 0.3), 42, RED, WHITE)


NOW = ["Rainy Day", "Chai Time", "Night Drive"]


# 08 Count with len -----------------------------------------------------------------
def k08(ly, d, t, D, B):
    # B0 How many songs now? B1 Use len. B2 Len of playlist gives three. B3 always the exact count.
    kw(d, ["How", "many", "songs?"], CX, TY, 104, t, 0.05, 0.12, {"many": YELLOW})
    X = xs(3, 400)
    for i, s in enumerate(NOW):
        cell(d, X[i], 420, 1, [(q(s), C_STR, 1, 0)], ACC if t >= B[2] + 0.5 + i * 0.3 else GREY, 360)
        badge(d, X[i] + 165, 365, str(i + 1), pop(t, B[2] + 0.5 + i * 0.3))
    shown = tl(["print(len(playlist))"], [(B[1] + 0.4, B[2] + 0.3)], t)
    code_win(d, 260, 620, 1120, shown, t, 0, 0.01, a(t, B[0] + 0.3), 52, "Python", run_t=B[2] + 0.4)
    out_win(d, 1180, 620, 1660, [([seg("3", YELLOW, True)], B[2] + 0.6)], t, a(t, B[2] + 0.4, 0.25), 60)
    pill(d, "len = length: the exact count, always", CX, 950, pop(t, B[3] + 0.3), 46, YELLOW, INK)


# 09 Lists of numbers ------------------------------------------------------------------
def k09(ly, d, t, D, B):
    # B0 numbers too. B1 marks... B2 Sum... B3 Max... B4 average...
    kw(d, ["Lists", "of", "numbers"], CX, TY, 104, t, 0.05, 0.12, {"numbers": ORANGE})
    shown = tl(["marks = [78, 92, 85]", "print(sum(marks))", "print(max(marks))", "print(sum(marks) / len(marks))"],
               [(B[1] + 0.3, B[1] + 2.6), (B[2] + 0.05, B[2] + 1.0), (B[3] + 0.05, B[3] + 1.0), (B[4] + 0.1, B[4] + 1.8)], t)
    code_win(d, 70, 300, 1100, shown, t, 0, 0.01, a(t, B[0]), 46, "Python", run_t=B[2] + 1.1)
    items = [([seg("255", YELLOW, True)], B[2] + 1.4), ([seg("92", YELLOW, True)], B[3] + 1.3), ([seg("85.0", YELLOW, True)], B[4] + 2.6)]
    out_win(d, 1160, 300, 1840, items, t, a(t, B[2] + 1.1, 0.25), 54)
    for i, (h1, h2, st) in enumerate([("sum", "adds them up", B[2]), ("max", "the biggest", B[3]), ("sum / len", "the average", B[4])]):
        p = a(t, st + 0.3)
        if p <= 0: continue
        x = 360 + i * 600
        oy = panel(d, x - 270, 780, x + 270, 930, p, outline=ORANGE if i == 2 else None)
        d.text((x, 830 + oy), h1, font=mono(48, True), fill=col(ORANGE, p), anchor="mm")
        body(d, h2, x, 892 + oy, 36, MUTED, p)
    pill(d, "Division always gives a decimal", 1500, 690, pop(t, B[4] + 3.0), 36, PANEL, WHITE)


# 10 Loop through a list -----------------------------------------------------------------
def k10(ly, d, t, D, B):
    # B0 best part. B1 Remember the for loop? B2 works with lists too. B3 For song in playlist... B4 one item at a time. B5 No index needed.
    if t < B[2] - 0.05:
        kw(d, ["Now", "the", "best", "part"], CX, TY, 104, t, 0.05, 0.12, {"best": YELLOW})
        emoji(ly, "\U0001F501", CX, 560, 200, pop(t, B[1] + 0.2))
        text(d, "The for loop from Episode 2", CX, 760, 56, WHITE, a(t, B[1] + 0.5))
        return
    kw(d, ["for", "loop", "+", "list"], CX, TY, 110, t, B[2], 0.12, {"for": ORANGE, "list": ACC})
    shown = tl(["for song in playlist:", '    print("Now playing:", song)'], [(B[3] + 0.1, B[3] + 1.4), (B[3] + 1.5, B[4] - 0.2)], t)
    code_win(d, 70, 300, 1040, shown, t, 0, 0.01, a(t, B[2]), 40, "Python", run_t=B[4])
    st, step = B[4] + 0.3, 1.0
    items = [([seg("Now playing: ", WHITE), seg(s, YELLOW, True)], st + j * step) for j, s in enumerate(NOW)]
    out_win(d, 1100, 300, 1850, items, t, a(t, B[4], 0.25), 36)
    X = xs(3, 400)
    k = int((t - st) / step) if t >= st else -1
    k = min(2, k)
    for i, s in enumerate(NOW):
        cell(d, X[i], 790, a(t, B[2] + 0.4 + i * 0.12), [(q(s), C_STR, 1, 0)], ORANGE if i == k else GREY, 360)
    if k >= 0:
        xk = X[k] if t > st + k * step + 0.25 else (X[max(0, k - 1)] + (X[k] - X[max(0, k - 1)]) * a(t, st + k * step, 0.25))
        pill(d, "song", xk, 665, a(t, st, 0.2), 40, ORANGE, INK)
        d.polygon([(xk - 16, 700), (xk + 16, 700), (xk, 722)], fill=col(ORANGE, a(t, st, 0.2)))
    pill(d, "No index needed!", CX, 965, pop(t, B[5]), 48, ACC, DARK)


# 11 Check with in --------------------------------------------------------------------------
def k11(ly, d, t, D, B):
    # B0 check if something is in a list. B1 Write if Chai Time in playlist... B2 condition, True or False
    kw(d, ["Is", "it", "in", "the", "list?"], CX, TY, 104, t, 0.05, 0.1, {"in": BLUE})
    shown = tl(['if "Chai Time" in playlist:', '    print("Found it!")'], [(B[1] + 0.1, B[1] + 1.6), (B[1] + 1.7, B[1] + 2.5)], t)
    code_win(d, 70, 300, 1040, shown, t, 0, 0.01, a(t, B[0]), 42, "Python", run_t=B[1] + 2.6)
    out_win(d, 1100, 300, 1850, [([seg("Found it!", ACC, True)], B[1] + 2.8)], t, a(t, B[1] + 2.6, 0.25), 46)
    emoji(ly, "\U0001F50D", 1475, 560, 110, pop(t, B[1] + 3.0))
    for i, (ex, res, c, st) in enumerate([('"Chai Time" in playlist', "True", ACC, B[2] + 0.4), ('"Sunrise" in playlist', "False", RED, B[2] + 1.6)]):
        p = a(t, st)
        if p <= 0: continue
        x0 = 60 + i * 920
        oy = panel(d, x0, 700, x0 + 880, 860, p, fill=CODEBG)
        d.text((x0 + 44, 780 + oy), ex, font=mono(42, True), fill=col(WHITE, p), anchor="lm")
        d.text((x0 + 840, 780 + oy), res, font=mono(52, True), fill=col(c, a(t, st + 0.5)), anchor="rm")
    body(d, "(we removed Sunrise earlier!)", 1420, 920, 36, MUTED, a(t, B[2] + 2.2))


TODO = ["tasks = []", "while True:", '    task = input("Add a task (or done): ")', '    if task == "done":', "        break",
        "    else:", "        tasks.append(task)", "", 'print(f"You have {len(tasks)} tasks:")', "for task in tasks:", '    print("-", task)']


# 12 To-do app: write it ------------------------------------------------------------------
def k12(ly, d, t, D, B):
    # B0 mini project. B1 empty list. B2 while True. B3 Ask for a task. B4 if done, break. B5 Else, append. B6 After the loop...
    kw(d, ["Mini", "project:", "to-do", "list", "app"], CX, TY, 96, t, 0.05, 0.1, {"to-do": ACC, "app": ACC})
    emoji(ly, "\U0001F4DD", 1830, TY, 80, pop(t, 0.7))
    sch = [(B[1] + 0.2, B[1] + 0.9), (B[2] + 0.1, B[2] + 0.8), (B[3], B[3] + 1.3), (B[4], B[4] + 0.9), (B[4] + 1.0, B[4] + 1.5),
           (B[5], B[5] + 0.4), (B[5] + 0.5, B[5] + 1.4), (B[6], B[6]), (B[6] + 0.2, B[6] + 2.2), (B[6] + 2.8, B[6] + 3.8), (B[6] + 3.9, B[6] + 4.8)]
    code_win(d, 50, 290, 1110, tl(TODO, sch, t), t, 0, 0.01, a(t, 0.3), 34, "Python")
    for (i0, i1, c, s0, s1) in [(0, 0, ACC, B[1], B[2]), (1, 1, ORANGE, B[2], B[3]), (2, 2, BLUE, B[3], B[4]), (3, 4, RED, B[4], B[5]),
                                (5, 6, ACC, B[5], B[6]), (8, 8, YELLOW, B[6], B[6] + 2.6), (9, 10, ORANGE, B[6] + 2.8, D + 1)]:
        if t >= s0: hl(d, 50, 1110, 290, 34, i0, i1, c, a(t, s0) * out(t, s1))
    notes = [("[ ]", "an empty list", B[1], ACC), ("while True", "keep asking", B[2], ORANGE), ("input()", "ask for a task", B[3], BLUE),
             ("break", "stop at \"done\"", B[4], RED), ("append()", "add the task", B[5], ACC), ("f-string + len", "count the tasks", B[6], YELLOW)]
    for i, (h1, h2, st, c) in enumerate(notes):
        p = a(t, st + 0.2)
        if p <= 0: continue
        y0 = 290 + i * 112
        oy = panel(d, 1160, y0, 1860, y0 + 98, p, outline=c)
        d.text((1195, y0 + 49 + oy), h1, font=mono(36, True), fill=col(c, p), anchor="lm")
        body(d, h2, 1530, y0 + 49 + oy, 34, WHITE, p, anchor="lm")


# 13 To-do app: run it ---------------------------------------------------------------------
def k13(ly, d, t, D, B):
    # B0 Let's run it. B1 Buy milk. B2 Study Python. B3 Recharge phone. B4 Done. B5 Python prints... B6 ten lines.
    kw(d, ["Let's", "run", "it!"], CX, TY, 110, t, 0.05, 0.12, {"run": ACC})
    code_win(d, 40, 290, 960, TODO, t, 0, 0.01, 1, 30, "Python", run_t=B[0] + 0.5)
    P = "Add a task (or done): "
    items = [([seg(P, WHITE), seg("Buy milk", ACC, True)], B[1]), ([seg(P, WHITE), seg("Study Python", ACC, True)], B[2]),
             ([seg(P, WHITE), seg("Recharge phone", ACC, True)], B[3]), ([seg(P, WHITE), seg("done", RED, True)], B[4]),
             ([seg("You have 3 tasks:", YELLOW, True)], B[5] + 0.3), ([seg("- Buy milk", WHITE)], B[5] + 0.9),
             ([seg("- Study Python", WHITE)], B[5] + 1.3), ([seg("- Recharge phone", WHITE)], B[5] + 1.7)]
    out_win(d, 1010, 290, 1870, items, t, a(t, B[0] + 0.5, 0.25), 32)
    p = a(t, B[1])
    if p > 0:
        d.text((1030, 850), "tasks:", font=mono(34, True), fill=col(BLUE, p), anchor="lm")
        f = font(27, "Bold", False)
        x = 1170
        for s, st in [("Buy milk", B[1] + 0.3), ("Study Python", B[2] + 0.3), ("Recharge phone", B[3] + 0.3)]:
            w = d.textlength(s, font=f) + 34
            pc = pop(t, st)
            if pc > 0:
                d.rounded_rectangle([x, 822, x + w, 878], 28, fill=col(ACC, min(pc, 1)))
                d.text((x + w / 2, 850), s, font=f, fill=col(DARK, min(pc, 1)), anchor="mm")
            x += w + 10
    pill(d, "A real app in 10 lines of code", 1440, 975, pop(t, B[6]), 42, YELLOW, INK)
    emoji(ly, "\U0001F389", 1840, 975, 80, pop(t, B[6] + 0.4))


# 14 Recap ----------------------------------------------------------------------------------
def k14(ly, d, t, D, B):
    kw(d, ["Recap"], CX, TY, 110, t, 0.05, 0.1, {"Recap": ACC})
    items = [("[ ]", "many values, in order", B[1]), ("[0]   [-1]", "first and last item", B[2]), ("append / remove", "add to end, delete by value", B[3]),
             ("len  sum  max", "count, add up, biggest", B[4]), ("for song in list", "goes through every item", B[5]), ("in", "is it in the list?", B[5] + 1.9)]
    for i, (h1, h2, st) in enumerate(items):
        p = a(t, st)
        if p <= 0: continue
        x0 = 150 if i < 3 else 990
        y0 = 320 + (i % 3) * 190
        oy = panel(d, x0, y0, x0 + 780, y0 + 160, p)
        emoji(ly, "✅", x0 + 70, int(y0 + 80 + oy), 66, p)
        d.text((x0 + 140, y0 + 56 + oy), h1, font=mono(46, True), fill=col(WHITE, p), anchor="lm")
        body(d, h2, x0 + 140, y0 + 118 + oy, 36, MUTED, p, anchor="lm")


# 15 Homework ---------------------------------------------------------------------------------
def k15(ly, d, t, D, B):
    kw(d, ["Your", "homework"], CX, TY, 104, t, 0.05, 0.1, {"homework": YELLOW})
    emoji(ly, "\U0001F3AC", CX, 350, 110, pop(t, B[0] + 0.3))
    p = a(t, B[0] + 0.6)
    if p > 0:
        oy = panel(d, 260, 430, 1660, 570, p, outline=YELLOW)
        text(d, "Make a list of your 5 favourite movies", CX, 500 + oy, 56, WHITE, p)
    for i, (code, lb, st) in enumerate([("[0]", "print the first", B[1] + 0.3), ("[-1]", "print the last", B[1] + 1.2),
                                         ("len()", "print how many", B[1] + 2.2), ("append()", "add one more", B[2] + 0.2)]):
        p = pop(t, st)
        if p <= 0: continue
        x = 330 + i * 420
        oy = panel(d, x - 190, 620, x + 190, 790, min(p, 1), fill=CODEBG, outline=ORANGE)
        d.text((x, 675 + oy), code, font=mono(52, True), fill=col(ORANGE, min(p, 1)), anchor="mm")
        body(d, lb, x, 745 + oy, 36, WHITE, min(p, 1))
    pill(d, "Post your code in the comments", CX, 900, pop(t, B[3]), 48, ACC, DARK)


# 16 Next episode (right side kept clear for YouTube end-screen elements) --------------------------
def k16(ly, d, t, D, B):
    text(d, "NEXT EPISODE", 530, 270, 46, MUTED, a(t, 0.1), "Bold", False)
    p = a(t, 0.3)
    if p > 0:
        oy = panel(d, 110, 330, 950, 760, p, outline=BLUE)
        text(d, "Episode 4", 530, 410 + oy, 54, BLUE, p)
        d.text((530, 520 + oy), "Dictionaries", font=mono(84, True), fill=col(WHITE, p), anchor="mm")
        body(d, "Store information with labels", 530, 615 + oy, 42, MUTED, p)
        d.text((530, 690 + oy), 'contact = {"name": "Riya"}', font=mono(38, True), fill=col(C_STR, p), anchor="mm")
    q_ = out(t, B[1] - 0.4, 0.4)
    p = a(t, B[0] + 3.0) * q_
    if p > 0:
        oy = panel(d, 1150, 330, 1750, 820, p, fill=(12, 15, 34), outline=(90, 104, 160), r=48)
        emoji(ly, "\U0001F4C7", 1240, int(410 + oy), 60, p)
        text(d, "Contacts", 1290, 410 + oy, 50, WHITE, p, anchor="lm")
        for i, (n, v) in enumerate([("name", "Riya"), ("city", "Hyderabad"), ("age", "21")]):
            pr = a(t, B[0] + 3.4 + i * 0.4) * q_
            y0 = 480 + i * 105 + oy
            d.rounded_rectangle([1190, y0, 1710, y0 + 88], 20, fill=col(PANEL, pr))
            d.text((1220, y0 + 44), n, font=mono(36, True), fill=col(BLUE, pr), anchor="lm")
            d.text((1680, y0 + 44), v, font=mono(36, True), fill=col(C_STR, pr), anchor="rm")
    pill(d, "Subscribe for Episode 4", 530, 860, pop(t, B[1]), 52, ACC, DARK)
    emoji(ly, "\U0001F514", 905, 860, 80, pop(t, B[1] + 0.4))
    emoji(ly, "\U0001F44B", 530, 975, 90, pop(t, B[2]))
