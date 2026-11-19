#!/usr/bin/env python3
"""Generator v2 for the 18 November 2026 news front page.

Bold redesign: black masthead, dark-red radar lead panel, dense
grid. Draws a 1024x1024 PNG with a custom 5x7 bitmap font and a
hand-rolled PNG encoder. Pure standard library only (zlib, struct,
math). Deterministic: every run writes identical bytes.
"""
import math
import struct
import zlib

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
}
FONT.update({
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01000", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "00010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01111", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "•": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
    "’": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
})

W = 1024
H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GOLD = (198, 142, 26)
GREY = (110, 108, 100)
LIGHT = (255, 255, 255)
NAVY = (13, 27, 54)
TEAL = (32, 178, 170)
CREAM = (250, 246, 235)
STORM = (16, 60, 96)
SAND = (232, 226, 210)
WAR = (46, 10, 14)


class Canvas:
    def __init__(self, width, height, color):
        self.w = width
        self.h = height
        self.px = bytearray(color * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d2 <= r * r:
                        self.set(xx, yy, color)
                else:
                    if abs(d2 - r * r) <= r:
                        self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        for k in range(t):
            self.circle(cx, cy, r - k, color, fill=False)

    def star(self, cx, cy, r, color):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.42
            pts.append((cx + int(rr * math.cos(ang)),
                        cy + int(rr * math.sin(ang))))
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            xs = []
            for i in range(10):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % 10]
                if (y0 <= yy < y1) or (y1 <= yy < y0):
                    xs.append(x0 + (yy - y0) * (x1 - x0) // (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for xx in range(xs[j], xs[j + 1] + 1):
                    self.set(xx, yy, color)
        for i in range(10):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % 10]
            self.line(x0, y0, x1, y1, color)

    def triangle(self, pts, color):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            row = []
            for i in range(3):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % 3]
                if (y0 <= yy < y1) or (y1 <= yy < y0):
                    row.append(x0 + (yy - y0) * (x1 - x0) // (y1 - y0))
            row.sort()
            if len(row) >= 2:
                for xx in range(row[0], row[-1] + 1):
                    self.set(xx, yy, color)


def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, color):
    for ch in text:
        glyph = FONT.get(ch, FONT["?"])
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "1":
                    cv.rect(x + c * scale, y + r * scale, scale, scale, color)
        x += 6 * scale


def text_center(cv, cx, y, text, scale, color):
    draw_text(cv, cx - text_width(text, scale) // 2, y, text, scale, color)


def wrap_text(text, scale, max_width):
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if text_width(trial, scale) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def halftone(cv, x, y, w, h, color, step=12, size=2):
    for yy in range(y + 4, y + h - 2, step):
        off = 6 if ((yy - y) // step) % 2 else 0
        for xx in range(x + 4 + off, x + w - 2, step):
            cv.rect(xx, yy, size, size, color)


def chip(cv, x, y, text, bg, fg):
    w = text_width(text, 1) + 16
    cv.rect(x, y, w, 22, bg)
    cv.frame(x, y, w, 22, INK, 2)
    draw_text(cv, x + 8, y + 7, text, 1, fg)
    return w


def burst(cv, cx, cy, r, color, inner=None):
    for a in range(0, 360, 30):
        ang = math.radians(a)
        cv.line(cx, cy, cx + int(r * math.cos(ang)),
                cy + int(r * math.sin(ang)), color)
        cv.line(cx + 1, cy, cx + 1 + int(r * math.cos(ang)),
                cy + int(r * math.sin(ang)), color)
    if inner is not None:
        cv.circle(cx, cy, max(3, r // 3), inner)


def thick_line(cv, x0, y0, x1, y1, color, t=3):
    for k in range(t):
        cv.line(x0, y0 + k, x1, y1 + k, color)



# ---------------------------------------------------------------- flags
def flag_us(cv, x, y, w, h):
    stripe = h // 7
    for s in range(7):
        cv.rect(x, y + s * stripe, w, stripe + (1 if s == 6 else 0),
                RED if s % 2 == 0 else LIGHT)
    cv.rect(x, y, w * 2 // 5, stripe * 4, BLUE)
    for sy in range(4):
        for sx in range(5):
            cv.rect(x + 5 + sx * 9, y + 4 + sy * 8, 3, 3, LIGHT)
    cv.frame(x, y, w, h, INK, 2)


def flag_ph(cv, x, y, w, h):
    cv.rect(x, y, w, h // 2, BLUE)
    cv.rect(x, y + h // 2, w, h - h // 2, RED)
    cv.triangle([(x, y), (x, y + h), (x + w * 9 // 20, y + h // 2)], LIGHT)
    cv.circle(x + w // 6, y + h // 2, 7, GOLD)
    cv.circle(x + w // 6, y + h // 2, 3, GOLD)
    cv.frame(x, y, w, h, INK, 2)


def flag_ca(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    bw = w // 5
    cv.rect(x, y, bw, h, RED)
    cv.rect(x + w - bw, y, bw, h, RED)
    cx, cy = x + w // 2, y + h // 2 - 6
    cv.star(cx, cy, 13, RED)
    cv.rect(cx - 2, cy + 8, 4, 14, RED)
    cv.frame(x, y, w, h, INK, 2)


def flag_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, (222, 41, 16))
    cv.star(x + 20, y + 16, 10, GOLD)
    for dx, dy in ((38, 6), (44, 14), (44, 24), (38, 32)):
        cv.circle(x + dx, y + dy, 3, GOLD)
    cv.frame(x, y, w, h, INK, 2)


# ---------------------------------------------------------------- art
def art_flags_us_ph(cv, x, y, w, h):
    cv.rect(x, y, w, h, SAND)
    fw = w - 30
    fh = (h - 28) // 2
    flag_us(cv, x + 15, y + 7, fw, fh)
    flag_ph(cv, x + 15, y + 21 + fh, fw, fh)


def art_flags_ca_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, SAND)
    fw = w - 30
    fh = (h - 28) // 2
    flag_ca(cv, x + 15, y + 7, fw, fh)
    flag_cn(cv, x + 15, y + 21 + fh, fw, fh)


def art_bridge(cv, x, y, w, h):
    cv.rect(x, y, w, h, NAVY)
    draw_text(cv, x + 8, y + 8, "DAY TWO", 2, GOLD)
    deck_y = y + 96
    t1, t2 = x + 30, x + w - 38
    cv.rect(t1, y + 34, 8, deck_y - y - 34, INK)
    cv.rect(t2, y + 34, 8, deck_y - y - 34, INK)
    cv.vline(t1 + 8, y + 34, deck_y - y - 34, LIGHT, 1)
    cv.vline(t2 - 1, y + 34, deck_y - y - 34, LIGHT, 1)
    cv.rect(t1, y + 34, 8, 4, GOLD)
    cv.rect(t2, y + 34, 8, 4, GOLD)
    cv.rect(x + 6, deck_y, w - 12, 8, INK)
    mid = x + w // 2
    # sagging cables: tower tops to deck centre in two segments
    cv.line(t1 + 4, y + 34, x + w // 4, deck_y - 14, LIGHT)
    cv.line(x + w // 4, deck_y - 14, mid, deck_y, LIGHT)
    cv.line(mid, deck_y, x + 3 * w // 4, deck_y - 14, LIGHT)
    cv.line(x + 3 * w // 4, deck_y - 14, t2 + 4, y + 34, LIGHT)
    cv.line(t1 + 4, y + 34, x + 10, deck_y, LIGHT)
    cv.line(t2 + 4, y + 34, x + w - 10, deck_y, LIGHT)
    burst(cv, mid, deck_y + 2, 22, RED, GOLD)
    cv.circle(mid, deck_y + 2, 5, GOLD)
    for i, wx in enumerate(range(x + 12, x + w - 20, 24)):
        wy = y + 122 + (6 if i % 2 else 0)
        cv.hline(wx, wy, 14, TEAL, 3)


def art_israel(cv, x, y, w, h):
    cv.rect(x, y, w, h, SAND)
    cx = x + w // 2 - 8
    # dome
    cv.circle(cx, y + 44, 26, GREY)
    cv.rect(cx - 26, y + 44, 52, 10, GREY)
    cv.vline(cx - 1, y + 8, 12, INK, 2)
    cv.rect(cx - 8, y + 8, 14, 8, BLUE)
    # entablature, columns, base
    cv.rect(cx - 44, y + 56, 88, 10, (88, 86, 80))
    for i in range(4):
        cv.rect(cx - 38 + i * 22, y + 70, 10, 48, (150, 148, 140))
    cv.rect(cx - 48, y + 122, 96, 10, (88, 86, 80))
    cv.rect(cx - 54, y + 134, 108, 8, INK)
    # flag pole at left
    cv.vline(x + 14, y + 30, 90, INK, 2)
    cv.rect(x + 16, y + 30, 20, 12, BLUE)
    cv.hline(x + 16, y + 35, 20, LIGHT, 2)
    # gold starburst with ? at top-right
    bx, by = x + w - 24, y + 22
    burst(cv, bx, by, 16, GOLD)
    cv.circle(bx, by, 10, GOLD)
    draw_text(cv, bx - 3, by - 4, "?", 1, INK)


def art_radar(cv, x, y, w, h):
    cv.rect(x, y, w, h, (24, 6, 8))
    halftone(cv, x, y, w, h, (70, 22, 26))
    cx, cy = x + 118, y + h // 2
    for r in (88, 66, 44, 22):
        cv.ring(cx, cy, r, (255, 90, 80), 3)
    cv.hline(cx - 92, cy, 184, (255, 90, 80), 2)
    cv.vline(cx, cy - 92, 184, (255, 90, 80), 2)
    # gold sweep at -38 degrees
    ang = math.radians(-38)
    ex, ey = cx + int(88 * math.cos(ang)), cy + int(88 * math.sin(ang))
    thick_line(cv, cx, cy, ex, ey, GOLD, 3)
    # three gold blips
    for bx, by, br in ((cx - 44, cy - 30, 5), (cx + 30, cy + 42, 4),
                       (cx + 52, cy - 52, 4)):
        cv.circle(bx, by, br, GOLD)
        cv.ring(bx, by, br + 5, GOLD, 1)
    # three grey drone triangles, top-right
    for dx, dy in ((248, 26), (286, 44), (316, 20)):
        cv.triangle([(x + dx, y + dy), (x + dx + 22, y + dy + 7),
                     (x + dx, y + dy + 14)], GREY)
        cv.rect(x + dx + 4, y + dy + 6, 8, 3, INK)
    # red missile trail + starburst, bottom-right
    cv.line(x + w - 96, y + h - 28, x + w - 42, y + h - 74, RED)
    cv.line(x + w - 95, y + h - 25, x + w - 41, y + h - 71, RED)
    burst(cv, x + w - 36, y + h - 80, 18, RED, GOLD)
    draw_text(cv, x + 10, y + h - 40, "STRAIT OF", 2, GOLD)
    draw_text(cv, x + 10, y + h - 22, "HORMUZ", 2, GOLD)


# ---------------------------------------------------------------- panels
def grid_panel(cv, x, y, kicker, kcolor, headline, body, art_fn):
    w, h = 488, 172
    cv.rect(x, y, w, h, LIGHT)
    cv.frame(x, y, w, h, INK, 3)
    art_fn(cv, x + 10, y + 10, 150, h - 20)
    tx = x + 176
    draw_text(cv, tx, y + 14, kicker, 1, kcolor)
    ty = y + 28
    for line in wrap_text(headline, 2, 296):
        draw_text(cv, tx, ty, line, 2, INK)
        ty += 16
    ty += 4
    for line in wrap_text(body, 2, 296):
        draw_text(cv, tx, ty, line, 2, (40, 40, 40))
        ty += 14


def build():
    cv = Canvas(W, H, PAPER)
    # 1. masthead
    cv.rect(0, 0, 1024, 118, INK)
    text_center(cv, 512, 22, "THE WORLD", 11, CREAM)
    draw_text(cv, 24, 38, "EST.", 1, GOLD)
    draw_text(cv, 24, 54, "TODAY", 1, GOLD)
    draw_text(cv, 1024 - 24 - text_width("ONE PAGE", 1), 38,
              "ONE PAGE", 1, GOLD)
    draw_text(cv, 1024 - 24 - text_width("ONLY", 1), 54, "ONLY", 1, GOLD)
    cv.hline(0, 106, 1024, GOLD, 3)
    # 2. red band
    cv.rect(0, 118, 1024, 34, RED)
    text_center(cv, 512, 128, "WEDNESDAY 18 NOVEMBER 2026", 2, CREAM)
    draw_text(cv, 16, 128, "EXTRA", 2, GOLD)
    draw_text(cv, 1024 - 16 - text_width("EXTRA", 2), 128, "EXTRA", 2, GOLD)
    # 3. lead panel
    lx, ly = 16, 164
    cv.rect(lx, ly, 992, 272, WAR)
    cv.frame(lx, ly, 992, 272, INK, 3)
    cv.rect(lx + 3, ly + 3, 986, 4, RED)
    draw_text(cv, lx + 20, ly + 16, "MIDDLE EAST  •  LEAD STORY", 2, GOLD)
    draw_text(cv, lx + 20, ly + 44, "IRAN-US STRIKES", 4, CREAM)
    draw_text(cv, lx + 20, ly + 82, "ESCALATE", 6, CREAM)
    body = ("Iran attacks a US military radar system in Bahrain with "
            "drones. The US answers with precision strikes on an "
            "IRGC missile launch site on Qeshm Island.")
    ty = ly + 138
    for line in wrap_text(body, 2, 540):
        draw_text(cv, lx + 20, ty, line, 2, (240, 228, 226))
        ty += 17
    cxp = lx + 20
    for text, bg, fg in (("RADAR HIT: BAHRAIN", GOLD, INK),
                         ("QESHM ISLAND STRUCK", RED, CREAM),
                         ("DRONES + MISSILES", TEAL, INK)):
        cxp += chip(cv, cxp, ly + 232, text, bg, fg) + 10
    art_radar(cv, lx + 612, ly + 16, 364, 240)
    # 4. grid panels
    grid_panel(cv, 16, 448, "DIPLOMACY", RED, "TRUMP LANDS IN MANILA",
               "The US president arrives in the Philippines for Quad "
               "talks ahead of his China visit and the APEC summit "
               "in Shenzhen.", art_flags_us_ph)
    grid_panel(cv, 520, 448, "WAR IN UKRAINE", RED,
               "CRIMEA BRIDGE HIT AGAIN",
               "Ukraine strikes the bridge for a second straight "
               "day, as Russia keeps pounding Kyiv's bridges.",
               art_bridge)
    grid_panel(cv, 16, 632, "TRADE", GOLD, "CANADA, CHINA EXTEND DEALS",
               "Trade deals extended as Xi meets PM Mark Carney "
               "ahead of the APEC summit.", art_flags_ca_cn)
    grid_panel(cv, 520, 632, "ISRAEL", BLUE, "ISRAEL POWER SHIFT",
               "Herzog asks ex-army chief Gadi Eisenkot to form the "
               "next government, bypassing Netanyahu; UK sanctions "
               "settlement firms.", art_israel)
    # 5. bottom strip: Gaza aid
    bx, by = 16, 816
    cv.rect(bx, by, 992, 152, LIGHT)
    cv.frame(bx, by, 992, 152, INK, 3)
    cv.rect(bx + 3, by + 3, 986, 4, RED)
    ax, ay = bx + 10, by + 10
    cv.rect(ax, ay, 280, 132, STORM)
    wbx, wby = ax + (280 - 108) // 2, ay + (132 - 84) // 2
    cv.rect(wbx, wby, 108, 84, LIGHT)
    cv.frame(wbx, wby, 108, 84, INK, 3)
    cv.rect(wbx + 44, wby + 14, 20, 56, RED)
    cv.rect(wbx + 26, wby + 32, 56, 20, RED)
    for i, wx in enumerate(range(ax + 150, ax + 268, 28)):
        cv.hline(wx, ay + 108 + (6 if i % 2 else 0), 18, TEAL, 3)
    for i, wx in enumerate(range(ax + 160, ax + 268, 28)):
        cv.hline(wx, ay + 122 - (6 if i % 2 else 0), 18, TEAL, 3)
    draw_text(cv, ax + 8, ay + 110, "4 NATIONS", 2, GOLD)
    tx = bx + 306
    draw_text(cv, tx, by + 16, "GAZA", 1, RED)
    draw_text(cv, tx, by + 32, "AID CALL FOR FLOODED GAZA", 3, INK)
    ty = by + 68
    for line in wrap_text("Australia, Canada, Italy and the UK jointly "
                          "call on Israel to let aid reach flooded Gaza.",
                          2, 662):
        draw_text(cv, tx, ty, line, 2, (40, 40, 40))
        ty += 16
    # 6. footer
    cv.hline(16, 984, 992, INK, 3)
    cv.hline(16, 990, 992, INK, 1)
    text_center(cv, 512, 998,
                "DRAWN FROM NEWS FIRST REPORTED ON WEDNESDAY "
                "18 NOVEMBER 2026", 1, GREY)
    return cv


def chunk(ctype, data):
    out = struct.pack(">I", len(data)) + ctype + data
    out += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


if __name__ == "__main__":
    import os
    import sys
    data = encode_png(build())
    path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    with open(path, "wb") as fh:
        fh.write(data)
    os.chmod(path, 0o644)
    print("wrote %s (%d bytes)" % (path, len(data)))
