import numpy as np
import time
import pygame
import sys
import os
import math

BAR_H = 160
TRAIL_DECAY = 6
speeds = [0.2, 0.1, 0.05, 0.02, 0.005, 0.001]
speed_labels = ["0.25x", "0.5x", "Normal", "2x", "4x", "8x"]

DARK = {
    "text": (220, 220, 220), "text_dim": (100, 100, 100), "btn": (40, 40, 40),
    "btn_hov": (65, 65, 65), "btn_act": (150, 20, 40), "bar_bg": (18, 18, 18),
    "div": (55, 55, 55), "slider_bg": (48, 48, 48), "slider_fill": (150, 20, 40),
    "dd_bg": (22, 22, 22), "dd_hov": (60, 60, 60), "sec": (75, 75, 75),
    "sec_lbl": (150, 150, 150), "status_col": (255, 80, 80), "swatch_bdr": (55, 55, 55),
    "bg_presets": [(0, 0, 0), (15, 15, 30), (10, 20, 10), (20, 10, 10), (25, 20, 5)],
    "cell_presets": [(196, 16, 43), (0, 200, 120), (30, 140, 255), (255, 180, 0), (200, 200, 200)],
    "grid_line": (35, 35, 35),
}

LIGHT = {
    "text": (30, 30, 30), "text_dim": (140, 140, 140), "btn": (210, 210, 210),
    "btn_hov": (185, 185, 185), "btn_act": (180, 30, 50), "bar_bg": (235, 235, 235),
    "div": (190, 190, 190), "slider_bg": (200, 200, 200), "slider_fill": (180, 30, 50),
    "dd_bg": (245, 245, 245), "dd_hov": (210, 210, 210), "sec": (170, 170, 170),
    "sec_lbl": (120, 120, 120), "status_col": (200, 20, 20), "swatch_bdr": (180, 180, 180),
    "bg_presets": [(255, 255, 255), (230, 235, 255), (230, 245, 230), (255, 235, 230), (255, 250, 220)],
    "cell_presets": [(180, 20, 40), (0, 160, 100), (20, 110, 210), (200, 140, 0), (80, 80, 80)],
    "grid_line": (210, 210, 210),
}

templates = {
    "Block": [(0,0),(0,1),(1,0),(1,1)],
    "Loaf": [(0,1),(0,2),(1,0),(1,3),(2,1),(2,3),(3,2)],
    "Beehive": [(0,1),(0,2),(1,0),(1,3),(2,1),(2,2)],
    "Boat": [(0,0),(0,1),(1,0),(1,2),(2,1)],
    "Tub": [(0,1),(1,0),(1,2),(2,1)],
    "Pond": [(0,1),(0,2),(1,0),(1,3),(2,0),(2,3),(3,1),(3,2)],
    "Blinker": [(0,0),(0,1),(0,2)],
    "Toad": [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2)],
    "Beacon": [(0,0),(0,1),(1,0),(2,3),(3,2),(3,3)],
    "Pulsar": [(0,2),(0,3),(0,4),(0,8),(0,9),(0,10),(2,0),(2,5),(2,7),(2,12),(3,0),(3,5),(3,7),(3,12),(4,0),(4,5),(4,7),(4,12),(5,2),(5,3),(5,4),(5,8),(5,9),(5,10),(7,2),(7,3),(7,4),(7,8),(7,9),(7,10),(8,0),(8,5),(8,7),(8,12),(9,0),(9,5),(9,7),(9,12),(10,0),(10,5),(10,7),(10,12),(12,2),(12,3),(12,4),(12,8),(12,9),(12,10)],
    "Pentadecathlon": [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(0,1),(9,1),(0,-1),(9,-1)],
    "Figure Eight": [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)],
    "Glider": [(0,1),(1,2),(2,0),(2,1),(2,2)],
    "Spaceship": [(0,1),(0,4),(1,0),(2,0),(2,4),(3,0),(3,1),(3,2),(3,3)],
    "Copperhead": [(0,2),(0,3),(1,0),(1,1),(1,4),(1,5),(2,0),(2,1),(2,4),(2,5),(3,2),(3,3),(5,2),(5,3),(6,1),(6,4),(7,2),(7,3),(9,2),(9,3),(10,1),(10,2),(10,3),(10,4)],
    "Crab": [(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(1,6),(1,7),(2,0),(2,1),(2,4),(2,5),(2,6),(2,7),(3,2),(3,3),(3,4),(3,5),(4,1),(4,2),(4,5),(4,6),(5,0),(5,7),(6,1),(6,6)],
    "Weekender": [(0,1),(0,2),(0,5),(0,6),(1,0),(1,3),(1,4),(1,7),(2,0),(2,3),(2,4),(2,7),(3,1),(3,6),(4,2),(4,5),(5,2),(5,5),(6,2),(6,3),(6,4),(6,5)],
    "Gosper Gun": [(0,24),(1,22),(1,24),(2,12),(2,13),(2,20),(2,21),(2,34),(2,35),(3,11),(3,15),(3,20),(3,21),(3,34),(3,35),(4,0),(4,1),(4,10),(4,16),(4,20),(4,21),(5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),(6,10),(6,16),(6,24),(7,11),(7,15),(8,12),(8,13)],
    "Simkin Gun": [(0,0),(0,1),(1,0),(1,1),(4,0),(4,1),(5,0),(5,1),(8,2),(8,3),(9,2),(9,3),(0,14),(0,15),(1,14),(1,15),(4,14),(4,15),(5,14),(5,15),(8,16),(8,17),(9,16),(9,17),(14,5),(14,6),(15,5),(15,6),(16,7),(17,5),(17,6),(17,7),(17,8),(18,6),(22,4),(22,5),(23,3),(24,3),(24,7),(25,3),(25,4),(25,5),(25,6),(26,5)],
    "R-Pentomino": [(0,1),(0,2),(1,0),(1,1),(2,1)],
    "Diehard": [(0,6),(1,0),(1,1),(2,1),(2,5),(2,6),(2,7)],
    "Acorn": [(0,1),(1,3),(2,0),(2,1),(2,4),(2,5),(2,6)],
    "Pi Heptomino": [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,2)],
    "Switch Engine": [(0,1),(1,3),(2,0),(2,1),(2,4),(2,5),(2,6),(3,3),(3,5),(3,6),(4,5)],
    "Infinite 1": [(0,11),(1,9),(1,11),(2,1),(2,2),(2,7),(2,8),(2,9),(2,10),(2,11),(3,1),(3,2),(3,7),(3,8),(3,9),(3,10),(4,7),(4,8),(5,9),(5,10),(5,11)],
    "Thunderbird": [(0,0),(0,1),(0,2),(2,1),(3,1),(4,1)],
    "Queen Bee": [(0,0),(0,1),(0,5),(0,6),(1,2),(1,4),(2,3),(3,2),(3,4),(4,2),(4,4),(5,2),(5,4),(6,3),(7,2),(7,4),(8,0),(8,1),(8,5),(8,6)],
    "Vampire": [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,4),(2,0),(2,2),(2,4),(3,0),(3,4),(4,0),(4,1),(4,2),(4,3),(4,4),(6,1),(6,2),(6,3),(7,0),(7,4),(8,0),(8,4),(9,1),(9,2),(9,3)],
    "Glider Pair": [(0,1),(1,2),(2,0),(2,1),(2,2),(5,4),(6,5),(7,3),(7,4),(7,5)],
    "Eater 1": [(0,0),(0,1),(1,0),(1,2),(2,2),(3,2),(3,3)],
    "Snake": [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)],
    "Canoe": [(0,0),(0,1),(1,0),(1,3),(2,2),(2,3)],
    "Bi-block": [(0,0),(0,1),(1,0),(1,1),(3,0),(3,1),(4,0),(4,1)],
    "Clock": [(0,1),(1,0),(1,2),(2,3),(3,1),(3,2)],
    "Koksgalaxy": [(0,0),(0,1),(0,5),(0,6),(1,0),(1,1),(1,5),(1,6),(3,2),(3,3),(4,2),(4,3),(3,4),(3,5),(4,4),(4,5),(6,0),(6,1),(6,5),(6,6),(7,0),(7,1),(7,5),(7,6)],
    "Pulsar 3": [(0,2),(0,3),(0,4),(0,8),(0,9),(0,10),(2,0),(2,5),(2,7),(2,12),(3,0),(3,5),(3,7),(3,12),(4,0),(4,5),(4,7),(4,12),(5,2),(5,3),(5,4),(5,8),(5,9),(5,10),(7,2),(7,3),(7,4),(7,8),(7,9),(7,10),(8,0),(8,5),(8,7),(8,12),(9,0),(9,5),(9,7),(9,12),(10,0),(10,5),(10,7),(10,12),(12,2),(12,3),(12,4),(12,8),(12,9),(12,10)],
    "Star": [(0,2),(1,1),(1,3),(2,0),(2,4),(3,1),(3,3),(4,2)],
    "Tumbler": [(0,1),(0,5),(1,1),(1,5),(2,1),(2,2),(2,4),(2,5),(3,0),(3,2),(3,4),(3,6),(4,0),(4,1),(4,5),(4,6)],
}

sections = [
    ("still life", ["Block","Loaf","Beehive","Boat","Tub","Pond","Snake","Canoe","Bi-block","Eater 1"]),
    ("oscillators", ["Blinker","Toad","Beacon","Pulsar","Pentadecathlon","Figure Eight","Clock","Tumbler","Star","Koksgalaxy"]),
    ("spaceships", ["Glider","Spaceship","Copperhead","Crab","Weekender","Glider Pair"]),
    ("guns", ["Gosper Gun","Simkin Gun"]),
    ("cool stuff", ["R-Pentomino","Diehard","Thunderbird","Acorn","Pi Heptomino","Switch Engine","Infinite 1","Vampire","Queen Bee","Pulsar 3"]),
]

def update_cells(cells):
    p = np.pad(cells, 1, mode='constant')
    nb = (p[:-2,:-2]+p[:-2,1:-1]+p[:-2,2:]+p[1:-1,:-2]+p[1:-1,2:]+p[2:,:-2]+p[2:,1:-1]+p[2:,2:])
    return np.where(cells==1, np.where((nb==2)|(nb==3),1,0), np.where(nb==3,1,0)).astype(float)

def resize_grid(cells, new_n):
    new = np.zeros((new_n, new_n))
    live = np.argwhere(cells == 1)
    if not len(live): return new
    rmin, cmin = live.min(0); rmax, cmax = live.max(0)
    or_ = (new_n-(rmax-rmin+1))//2; oc_ = (new_n-(cmax-cmin+1))//2
    for r, c in live:
        nr, nc = r-rmin+or_, c-cmin+oc_
        if 0 <= nr < new_n and 0 <= nc < new_n: new[nr, nc] = 1
    return new

def place_template(cells, name, gn):
    pat = templates[name]
    pr = [r for r,c in pat]; pc = [c for r,c in pat]
    oh = (gn-max(pr))//2 - min(pr); ow = (gn-max(pc))//2 - min(pc)
    for r, c in pat:
        nr, nc = r+oh, c+ow
        if 0 <= nr < gn and 0 <= nc < gn: cells[nr, nc] = 1
    return cells

def get_status(cells, prev):
    if np.sum(cells) == 0: return "total exictinction"
    if prev is not None and np.array_equal(cells, prev): return "still life population stable"
    return None

def load_icon(path, size, color, bg_color=None):
    raw = pygame.image.load(path).convert_alpha()
    raw = pygame.transform.scale(raw, (size, size))
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for x in range(size):
        for y in range(size):
            r, g, b, a = raw.get_at((x, y))
            brightness = (r + g + b) / 3
            if brightness > 128:
                surf.set_at((x, y), color + (255,))
            else:
                surf.set_at((x, y), (0, 0, 0, 0))
    return surf

def draw_icon_btn(screen, rect, icon, active, hovered, th):
    c = th["btn_act"] if active else th["btn_hov"] if hovered else th["btn"]
    pygame.draw.rect(screen, c, rect, border_radius=5)
    pygame.draw.rect(screen, th["div"], rect, 1, border_radius=5)
    ix = rect.x + (rect.w - icon.get_width()) // 2
    iy = rect.y + (rect.h - icon.get_height()) // 2
    screen.blit(icon, (ix, iy))

def draw_swatch(screen, rect, color, hovered, active, th):
    pygame.draw.rect(screen, color, rect, border_radius=4)
    border = th["text"] if active else (150,150,150) if hovered else th["swatch_bdr"]
    pygame.draw.rect(screen, border, rect, 2 if active else 1, border_radius=4)

def draw_slider(screen, font, track, val, dragging, mx, my, th, label, val_label, fill=None, n=1):
    fill = fill or th["slider_fill"]
    screen.blit(font.render(label, True, th["text_dim"]), (track.x, track.y-16))
    lbl = font.render(val_label, True, th["text"])
    screen.blit(lbl, (track.right-lbl.get_width(), track.y-16))
    pygame.draw.rect(screen, th["slider_bg"], track, border_radius=4)
    ratio = val/n; fw = int(track.w*ratio)
    if fw > 0: pygame.draw.rect(screen, fill, pygame.Rect(track.x, track.y, fw, track.h), border_radius=4)
    tx = track.x+int(track.w*ratio)
    hov = pygame.Rect(tx-7, track.centery-7, 14, 14).collidepoint(mx, my) or dragging
    pygame.draw.circle(screen, th["text"] if hov else th["text_dim"], (tx, track.centery), 7)
    pygame.draw.circle(screen, th["div"], (tx, track.centery), 7, 1)

def build_dd_rows(dd_rect, GH):
    item_h, sec_h = 22, 18
    total_h = sum(sec_h + item_h*len(names) for _, names in sections)
    top_y = max(5, dd_rect.top - total_h - 4)
    rows = []
    y = top_y
    for sec_name, names in sections:
        rows.append(("section", sec_name, pygame.Rect(dd_rect.x, y, dd_rect.w, sec_h)))
        y += sec_h
        for name in names:
            rows.append(("item", name, pygame.Rect(dd_rect.x+1, y, dd_rect.w-2, item_h)))
            y += item_h
    return rows

def draw_dropdown(screen, font, dd_rect, selected, open_, mx, my, th, GH):
    hov = dd_rect.collidepoint(mx, my)
    pygame.draw.rect(screen, th["btn_hov"] if (hov or open_) else th["btn"], dd_rect, border_radius=5)
    pygame.draw.rect(screen, th["div"], dd_rect, 1, border_radius=5)
    t = font.render(selected, True, th["text"])
    screen.blit(t, (dd_rect.x+8, dd_rect.y+(dd_rect.h-t.get_height())//2))
    arrow = "▴" if open_ else "▾"
    screen.blit(font.render(arrow, True, th["text_dim"]),
                (dd_rect.right-14, dd_rect.y+(dd_rect.h-font.size(arrow)[1])//2))
    if not open_: return
    rows = build_dd_rows(dd_rect, GH)
    all_r = [r for _, _, r in rows]
    if not all_r: return
    bg_r = all_r[0].unionall(all_r[1:]).inflate(2, 4)
    pygame.draw.rect(screen, th["dd_bg"], bg_r, border_radius=4)
    pygame.draw.rect(screen, th["div"], bg_r, 1, border_radius=4)
    for kind, name, r in rows:
        if kind == "section":
            pygame.draw.line(screen, th["sec"], (r.x+4, r.centery), (r.right-4, r.centery), 1)
            lbl = font.render(name.upper(), True, th["sec_lbl"])
            lbg = pygame.Surface((lbl.get_width()+6, lbl.get_height()))
            lbg.fill(th["dd_bg"])
            screen.blit(lbg, (r.x+10, r.centery-lbl.get_height()//2))
            screen.blit(lbl, (r.x+13, r.centery-lbl.get_height()//2))
        else:
            if r.collidepoint(mx, my): pygame.draw.rect(screen, th["dd_hov"], r)
            elif name == selected: pygame.draw.rect(screen, (80, 20, 25), r)
            screen.blit(font.render(name, True, th["text"]),
                        (r.x+10, r.y+(r.h-font.size(name)[1])//2))

# ─── layout constants ───────────────────────────────────────────────
TRAIL_BINARY_GAP = 20   # extra gap between trail and binary buttons

def make_rects(W, H, GH):
    icon_sz = 36
    ov_gap = 12
    total_ov = icon_sz + icon_sz + ov_gap
    play_rect  = pygame.Rect((W-total_ov)//2, 14, icon_sz, icon_sz)
    reset_rect = pygame.Rect(play_rect.right+ov_gap, 14, icon_sz, icon_sz)

    r1y = GH + 30
    dd_rect    = pygame.Rect(20, r1y, 170, 26)
    track_rect = pygame.Rect(210, r1y+9, W-230, 8)

    r2y = r1y + 52
    icon_bw = 40

    gridb_rect  = pygame.Rect(20,              r2y, icon_bw, icon_bw)
    theme_rect  = pygame.Rect(20+icon_bw+8,    r2y, icon_bw, icon_bw)
    trail_rect  = pygame.Rect(20,              r2y, 80, 30)   # placeholder kept for compat

    trail_rect2 = pygame.Rect(20 + 2*(icon_bw+8), r2y, 80, icon_bw)
    # binary button: trail_rect2.right + TRAIL_BINARY_GAP (was just +8 before)
    binary_rect = pygame.Rect(trail_rect2.right + TRAIL_BINARY_GAP, r2y, icon_bw, icon_bw)

    r3y = r2y + 56

    return (dd_rect, track_rect, gridb_rect, theme_rect, trail_rect,
            play_rect, reset_rect, r3y, r2y, icon_bw, binary_rect, trail_rect2)

SW, SW_GAP = 26, 6

def swatches(y, kind):
    base = 20 if kind == "bg" else 20 + 5*(SW+SW_GAP) + 28
    return {i: pygame.Rect(base + i*(SW+SW_GAP), y, SW, 22) for i in range(5)}


# ─── Color Wheel Popup ──────────────────────────────────────────────

def hsv_to_rgb(h, s, v):
    """h in [0,360], s,v in [0,1] → (r,g,b) each in [0,255]"""
    h = h % 360
    hi = int(h / 60) % 6
    f  = h / 60 - int(h / 60)
    p  = v * (1 - s)
    q  = v * (1 - f * s)
    t  = v * (1 - (1 - f) * s)
    variants = [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]
    r, g, b = variants[hi]
    return (int(r*255), int(g*255), int(b*255))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    d = mx - mn
    v = mx
    s = 0 if mx == 0 else d / mx
    if d == 0:
        h = 0
    elif mx == r:
        h = 60 * ((g - b) / d % 6)
    elif mx == g:
        h = 60 * ((b - r) / d + 2)
    else:
        h = 60 * ((r - g) / d + 4)
    return h, s, v

def build_wheel_surface(radius):
    """Pre-render the hue/saturation wheel (value=1) into a Surface."""
    size = radius * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = radius
    for px in range(size):
        for py in range(size):
            dx, dy = px - cx, py - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= radius:
                angle = math.degrees(math.atan2(-dy, dx)) % 360
                sat   = dist / radius
                r, g, b = hsv_to_rgb(angle, sat, 1.0)
                a = 255 if dist <= radius else 0
                surf.set_at((px, py), (r, g, b, a))
    return surf

def show_color_wheel(current_color, font_s, main_W, main_H):
    """
    Show a color-wheel popup.  Returns the chosen (r,g,b) tuple,
    or current_color if the user cancels.
    """
    WIN_W, WIN_H = 340, 400
    win = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
    pygame.display.set_caption("cell color  —  esc to cancel")

    WHEEL_R   = 120
    wheel_cx  = WIN_W // 2
    wheel_cy  = 140
    bar_x     = 30
    bar_y     = WIN_H - 110
    bar_w     = WIN_W - 60
    bar_h     = 16

    BG        = (20, 20, 20)
    BORDER    = (70, 70, 70)
    TEXT_COL  = (210, 210, 210)
    DIM       = (110, 110, 110)

    wheel_surf = build_wheel_surface(WHEEL_R)

    # Parse current color into HSV
    h, s, v = rgb_to_hsv(*current_color)
    chosen = list(current_color)

    # Buttons
    ok_rect     = pygame.Rect(WIN_W//2 - 90, WIN_H - 46, 80, 30)
    cancel_rect = pygame.Rect(WIN_W//2 + 10, WIN_H - 46, 80, 30)

    drag_wheel = False
    drag_val   = False
    clock      = pygame.time.Clock()

    def hue_sat_to_xy(h, s):
        angle = math.radians(h)
        px = wheel_cx + int(s * WHEEL_R * math.cos(angle))
        py = wheel_cy - int(s * WHEEL_R * math.sin(angle))
        return px, py

    def xy_to_hue_sat(px, py):
        dx, dy = px - wheel_cx, py - wheel_cy
        dist = math.sqrt(dx*dx + dy*dy)
        sat  = min(dist / WHEEL_R, 1.0)
        hue  = math.degrees(math.atan2(-dy, dx)) % 360
        return hue, sat

    def val_x(v):
        return bar_x + int(v * bar_w)

    def make_val_bar():
        surf = pygame.Surface((bar_w, bar_h))
        for bx in range(bar_w):
            vv = bx / bar_w
            col = hsv_to_rgb(h, s, vv)
            pygame.draw.line(surf, col, (bx, 0), (bx, bar_h - 1))
        return surf

    running = True
    result  = current_color

    while running:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_RETURN:
                    result = tuple(chosen); running = False

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Wheel hit?
                dx, dy = mx - wheel_cx, my - wheel_cy
                if math.sqrt(dx*dx + dy*dy) <= WHEEL_R:
                    drag_wheel = True
                    h, s = xy_to_hue_sat(mx, my)
                    chosen = list(hsv_to_rgb(h, s, v))
                # Value bar hit?
                elif pygame.Rect(bar_x, bar_y, bar_w, bar_h).collidepoint(mx, my):
                    drag_val = True
                    v = max(0.0, min(1.0, (mx - bar_x) / bar_w))
                    chosen = list(hsv_to_rgb(h, s, v))
                elif ok_rect.collidepoint(mx, my):
                    result = tuple(chosen); running = False
                elif cancel_rect.collidepoint(mx, my):
                    running = False

            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                drag_wheel = drag_val = False

            elif ev.type == pygame.MOUSEMOTION:
                if drag_wheel:
                    dx, dy = mx - wheel_cx, my - wheel_cy
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist > 0:
                        h, s = xy_to_hue_sat(mx, my)
                        chosen = list(hsv_to_rgb(h, s, v))
                if drag_val:
                    v = max(0.0, min(1.0, (mx - bar_x) / bar_w))
                    chosen = list(hsv_to_rgb(h, s, v))

            elif ev.type == pygame.VIDEORESIZE:
                WIN_W, WIN_H = ev.w, ev.h
                win = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)

        # ── draw ──────────────────────────────────────────────────
        win.fill(BG)

        # title
        title = font_s.render("cell color", True, TEXT_COL)
        win.blit(title, (WIN_W//2 - title.get_width()//2, 12))

        # wheel
        win.blit(wheel_surf, (wheel_cx - WHEEL_R, wheel_cy - WHEEL_R))

        # darken wheel by value
        if v < 1.0:
            dark_overlay = pygame.Surface((WHEEL_R*2, WHEEL_R*2), pygame.SRCALPHA)
            alpha = int((1 - v) * 255)
            pygame.draw.circle(dark_overlay, (0, 0, 0, alpha), (WHEEL_R, WHEEL_R), WHEEL_R)
            win.blit(dark_overlay, (wheel_cx - WHEEL_R, wheel_cy - WHEEL_R))

        # wheel border
        pygame.draw.circle(win, BORDER, (wheel_cx, wheel_cy), WHEEL_R, 1)

        # selector dot on wheel
        dot_x, dot_y = hue_sat_to_xy(h, s)
        pygame.draw.circle(win, (0,0,0), (dot_x, dot_y), 7, 2)
        pygame.draw.circle(win, (255,255,255), (dot_x, dot_y), 6, 2)

        # value bar
        val_bar = make_val_bar()
        win.blit(val_bar, (bar_x, bar_y))
        pygame.draw.rect(win, BORDER, pygame.Rect(bar_x, bar_y, bar_w, bar_h), 1)
        vx = val_x(v)
        pygame.draw.circle(win, (255,255,255), (vx, bar_y + bar_h//2), 8, 2)
        pygame.draw.circle(win, (0,0,0),       (vx, bar_y + bar_h//2), 7, 1)

        # brightness label
        bl = font_s.render("brightness", True, DIM)
        win.blit(bl, (bar_x, bar_y - 18))

        # preview swatch
        swatch_y = bar_y + bar_h + 14
        preview_rect = pygame.Rect(bar_x, swatch_y, bar_w, 22)
        pygame.draw.rect(win, tuple(chosen), preview_rect, border_radius=4)
        pygame.draw.rect(win, BORDER, preview_rect, 1, border_radius=4)

        # hex label
        hex_str = "#{:02X}{:02X}{:02X}".format(*chosen)
        hl = font_s.render(hex_str, True, TEXT_COL)
        win.blit(hl, (WIN_W//2 - hl.get_width()//2, swatch_y + 28))

        # OK / Cancel buttons
        for rect, label, is_ok in [(ok_rect, "OK", True), (cancel_rect, "cancel", False)]:
            hov = rect.collidepoint(mx, my)
            col = (100, 160, 80) if (is_ok and hov) else (60, 100, 50) if is_ok else \
                  (80, 80, 80) if hov else (50, 50, 50)
            pygame.draw.rect(win, col, rect, border_radius=5)
            pygame.draw.rect(win, BORDER, rect, 1, border_radius=5)
            lt = font_s.render(label, True, TEXT_COL)
            win.blit(lt, (rect.x + (rect.w - lt.get_width())//2,
                          rect.y + (rect.h - lt.get_height())//2))

        pygame.display.update()

    # restore main window
    pygame.display.set_mode((main_W, main_H), pygame.RESIZABLE)
    pygame.display.set_caption("c0nway_gam3_of_lif3")
    return result


def show_binary_view(cells, font, main_W, main_H):
    rows, cols = cells.shape
    char_w = font.size("0")[0]
    char_h = font.get_height()
    pad = 20
    WIN_W = min(cols * char_w + pad * 2, 1400)
    WIN_H = min(rows * char_h + pad * 2, 900)

    win = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
    pygame.display.set_caption("binary view  —  esc or click to close")

    BG    = (10, 10, 10)
    WHITE = (255, 255, 255)
    DARK  = (45,  45,  45)

    full_w = cols * char_w + pad * 2
    full_h = rows * char_h + pad * 2
    canvas = pygame.Surface((full_w, full_h))
    canvas.fill(BG)

    zero_surf = font.render("0", True, DARK)
    one_surf  = font.render("1", True, WHITE)

    for r in range(rows):
        for c in range(cols):
            x = pad + c * char_w
            y = pad + r * char_h
            canvas.blit(one_surf if cells[r, c] == 1 else zero_surf, (x, y))

    scroll_x = scroll_y = 0
    max_sx = max(0, full_w - WIN_W)
    max_sy = max(0, full_h - WIN_H)

    hint_font = pygame.font.SysFont("monospace", 13)
    hint = hint_font.render("scroll: arrow keys / mouse wheel  |  esc or click to close", True, (80, 80, 80))

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_LEFT:
                    scroll_x = max(0, scroll_x - char_w * 5)
                elif ev.key == pygame.K_RIGHT:
                    scroll_x = min(max_sx, scroll_x + char_w * 5)
                elif ev.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - char_h * 3)
                elif ev.key == pygame.K_DOWN:
                    scroll_y = min(max_sy, scroll_y + char_h * 3)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    running = False
                elif ev.button == 4:
                    scroll_y = max(0, scroll_y - char_h * 3)
                elif ev.button == 5:
                    scroll_y = min(max_sy, scroll_y + char_h * 3)
            elif ev.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(max_sy, scroll_y - ev.y * char_h * 3))
                scroll_x = max(0, min(max_sx, scroll_x - ev.x * char_w * 3))
            elif ev.type == pygame.VIDEORESIZE:
                WIN_W, WIN_H = ev.w, ev.h
                win = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
                max_sx = max(0, full_w - WIN_W)
                max_sy = max(0, full_h - WIN_H)

        win.fill(BG)
        win.blit(canvas, (0, 0), area=pygame.Rect(scroll_x, scroll_y, WIN_W, WIN_H))
        win.blit(hint, (8, WIN_H - hint.get_height() - 6))
        pygame.display.update()

    pygame.display.set_mode((main_W, main_H), pygame.RESIZABLE)
    pygame.display.set_caption("c0nway_gam3_of_lif3")


def do_render(screen, cells, trail, prev, size, gen, font, font_s,
              sp_idx, tmpl_sel, dd_open, bg, aliven, dragging,
              mx, my, fps, th, show_grid, show_trail, running, W, H, GH,
              icons):

    (dd_rect, track_rect, gridb_rect, theme_rect, trail_rect,
     play_rect, reset_rect, r3y, r2y, icon_bw, binary_rect, trail_rect2) = make_rects(W, H, GH)

    screen.fill(bg, pygame.Rect(0, 0, W, GH))

    if show_trail:
        for r in range(trail.shape[0]):
            for c in range(trail.shape[1]):
                v = trail[r, c]
                if v > 0 and cells[r, c] == 0:
                    a = int(255*(v/TRAIL_DECAY))
                    faded = tuple(int(aliven[i]*(a/255)+bg[i]*(1-a/255)) for i in range(3))
                    pygame.draw.rect(screen, faded, pygame.Rect(c*size, r*size,
                        size-(1 if show_grid else 0), size-(1 if show_grid else 0)))

    cw = size - (1 if show_grid else 0)
    for r in range(cells.shape[0]):
        for c in range(cells.shape[1]):
            if cells[r, c] == 1:
                pygame.draw.rect(screen, aliven, pygame.Rect(c*size, r*size, cw, cw))

    if show_grid:
        gc = th["grid_line"]
        for x in range(0, W, size): pygame.draw.line(screen, gc, (x, 0), (x, GH))
        for y in range(0, GH, size): pygame.draw.line(screen, gc, (0, y), (W, y))

    if my < GH:
        col_, row_ = mx//size, my//size
        if 0 <= row_ < cells.shape[0] and 0 <= col_ < cells.shape[1]:
            pygame.draw.rect(screen, aliven, pygame.Rect(col_*size, row_*size, cw, cw), 1)

    screen.blit(font.render(f"G{gen}", True, th["text"]), (10, 10))
    fl = font_s.render(f"{fps:.0f} fps", True, th["text_dim"])
    screen.blit(fl, (W-fl.get_width()-10, 10))
    status = get_status(cells, prev)
    if status:
        screen.blit(font_s.render(status, True, th["status_col"]), (10, 32))

    play_icon  = icons["pause"] if running else icons["play"]
    reset_icon = icons["reset_text"]
    draw_icon_btn(screen, play_rect,  play_icon,  running, play_rect.collidepoint(mx, my), th)
    draw_icon_btn(screen, reset_rect, reset_icon, False,   reset_rect.collidepoint(mx, my), th)

    screen.fill(th["bar_bg"], pygame.Rect(0, GH, W, BAR_H))
    pygame.draw.line(screen, th["div"], (0, GH), (W, GH), 1)

    draw_slider(screen, font_s, track_rect, sp_idx, dragging, mx, my, th,
                "speed", speed_labels[sp_idx], n=len(speeds)-1)

    draw_icon_btn(screen, gridb_rect, icons["grid"],  show_grid, gridb_rect.collidepoint(mx, my), th)
    theme_icon = icons["light"] if th is DARK else icons["dark"]
    draw_icon_btn(screen, theme_rect, theme_icon, False, theme_rect.collidepoint(mx, my), th)

    # Trail button
    c = th["btn_act"] if show_trail else th["btn_hov"] if trail_rect2.collidepoint(mx, my) else th["btn"]
    pygame.draw.rect(screen, c, trail_rect2, border_radius=5)
    pygame.draw.rect(screen, th["div"], trail_rect2, 1, border_radius=5)
    tl = font_s.render("trail", True, th["text"])
    screen.blit(tl, (trail_rect2.x+(trail_rect2.w-tl.get_width())//2,
                     trail_rect2.y+(trail_rect2.h-tl.get_height())//2))

    # Binary view button (with TRAIL_BINARY_GAP spacing)
    bc = th["btn_hov"] if binary_rect.collidepoint(mx, my) else th["btn"]
    pygame.draw.rect(screen, bc, binary_rect, border_radius=5)
    pygame.draw.rect(screen, th["div"], binary_rect, 1, border_radius=5)
    bl = font_s.render("01", True, th["text"])
    screen.blit(bl, (binary_rect.x + (binary_rect.w - bl.get_width())//2,
                     binary_rect.y + (binary_rect.h - bl.get_height())//2))

    screen.blit(font_s.render("bg",   True, th["text_dim"]), (20,  r3y-14))
    for i, col in enumerate(th["bg_presets"]):
        r = swatches(r3y, "bg")[i]
        draw_swatch(screen, r, col, r.collidepoint(mx, my), col == bg, th)

    # Cell color label + swatches + color wheel trigger swatch
    cell_lbl_x = 20 + 5*(SW+SW_GAP) + 28
    screen.blit(font_s.render("cell", True, th["text_dim"]), (cell_lbl_x, r3y-14))
    for i, col in enumerate(th["cell_presets"]):
        r = swatches(r3y, "cell")[i]
        draw_swatch(screen, r, col, r.collidepoint(mx, my), col == aliven, th)

    # "⊕" color-wheel trigger button (after the 5 swatches)
    cw_x = cell_lbl_x + 5*(SW+SW_GAP) + 4
    cw_rect = pygame.Rect(cw_x, r3y, SW, 22)
    hov_cw = cw_rect.collidepoint(mx, my)
    pygame.draw.rect(screen, th["btn_hov"] if hov_cw else th["btn"], cw_rect, border_radius=4)
    pygame.draw.rect(screen, th["div"], cw_rect, 1, border_radius=4)
    plus_lbl = font_s.render("+", True, th["text"])
    screen.blit(plus_lbl, (cw_rect.x+(cw_rect.w-plus_lbl.get_width())//2,
                            cw_rect.y+(cw_rect.h-plus_lbl.get_height())//2))

    draw_dropdown(screen, font_s, dd_rect, tmpl_sel or "select pattern",
                  dd_open, mx, my, th, GH)

    pygame.display.update()

def main():
    pygame.init()
    W, H, GH = 800, 960, 800
    screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption("c0nway_gam3_of_lif3")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font   = pygame.font.Font(os.path.join(base_dir, "ByteBounce.ttf"), 32)
    font_s = pygame.font.Font(os.path.join(base_dir, "ByteBounce.ttf"), 20)

    ICON_SIZE = 24
    icon_color = (220, 220, 220)

    def load(name):
        return load_icon(os.path.join(base_dir, name), ICON_SIZE, icon_color)

    icons = {
        "play":  font.render("P", True, icon_color),
        "pause": font.render("S", True, icon_color),
        "grid":  load("grid.png"),
        "light": load("light.png"),
        "dark":  load("darkmode.png"),
    }
    reset_surf = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    rt = font.render("R", True, icon_color)
    reset_surf.blit(rt, ((ICON_SIZE-rt.get_width())//2, (ICON_SIZE-rt.get_height())//2))
    icons["reset_text"] = reset_surf

    size   = 10
    grid_n = GH // size
    cells  = np.zeros((grid_n, grid_n))
    trail  = np.zeros((grid_n, grid_n))
    history = [cells.copy()]
    idx = 0
    running = False
    sp_idx  = 2
    tmpl_sel = None
    th = DARK
    bg, aliven = th["bg_presets"][0], th["cell_presets"][0]
    dd_open = dragging = False
    show_grid = True; show_trail = False
    mx = my = 0
    clock = pygame.time.Clock()
    fps = 0.0

    def render(prev_c=None):
        do_render(screen, cells, trail, prev_c, size, idx, font, font_s,
                  sp_idx, tmpl_sel, dd_open, bg, aliven, dragging,
                  mx, my, fps, th, show_grid, show_trail, running, W, H, GH, icons)

    def reset_trail(): trail[:] = 0

    def do_reset():
        nonlocal cells, running, tmpl_sel, dd_open, history, idx
        cells = np.zeros((grid_n, grid_n))
        reset_trail()
        history, idx = [cells.copy()], 0
        running = False; tmpl_sel = None; dd_open = False
        render()

    def step_fwd():
        nonlocal cells, idx
        prev = cells.copy()
        if idx < len(history)-1:
            idx += 1
        else:
            nc = update_cells(cells)
            if show_trail:
                died = (cells==1)&(nc==0)
                trail[died] = TRAIL_DECAY; trail[nc==1] = 0
                trail[:] = np.maximum(trail-1, 0)
            history.append(nc.copy()); idx = len(history)-1; cells = nc
        cells = history[idx].copy()
        render(prev)

    render()

    while True:
        clock.tick(120)
        fps = clock.get_fps()
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        mx, my = pygame.mouse.get_pos()
        (dd_rect, track_rect, gridb_rect, theme_rect, trail_rect,
         play_rect, reset_rect, r3y, r2y, icon_bw, binary_rect, trail_rect2) = make_rects(W, H, GH)
        cell_lbl_x = 20 + 5*(SW+SW_GAP) + 28
        cw_x = cell_lbl_x + 5*(SW+SW_GAP) + 4
        cw_trigger_rect = pygame.Rect(cw_x, r3y, SW, 22)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                W, H = event.w, event.h; GH = H - BAR_H
                grid_n = GH // size
                cells = resize_grid(cells, grid_n)
                trail = np.zeros((grid_n, grid_n))
                history = [cells.copy()]; idx = 0
                render()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running; dd_open = False
                elif event.key == pygame.K_r:
                    do_reset()
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS) and ctrl:
                    size = min(size+1, 40); grid_n = GH//size
                    cells = resize_grid(cells, grid_n); trail = np.zeros((grid_n,grid_n))
                    history, idx, running = [cells.copy()], 0, False; render()
                elif event.key == pygame.K_MINUS and ctrl:
                    size = max(size-1, 2); grid_n = GH//size
                    cells = resize_grid(cells, grid_n); trail = np.zeros((grid_n,grid_n))
                    history, idx, running = [cells.copy()], 0, False; render()
                elif event.key == pygame.K_RIGHT:
                    running = dd_open = False; step_fwd()
                elif event.key == pygame.K_LEFT:
                    running = dd_open = False
                    prev = history[idx-1].copy() if idx > 1 else None
                    if idx > 0: idx -= 1
                    cells = history[idx].copy(); render(prev)
                elif event.key == pygame.K_g:
                    show_grid = not show_grid; render()
                elif event.key == pygame.K_l:
                    th = LIGHT if th is DARK else DARK
                    bg, aliven = th["bg_presets"][0], th["cell_presets"][0]; render()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dd_open:
                    rows = build_dd_rows(dd_rect, GH)
                    clicked = False
                    for kind, name, r in rows:
                        if kind == "item" and r.collidepoint(mx, my):
                            tmpl_sel = name; dd_open = False; clicked = True
                            cells = place_template(np.zeros((grid_n,grid_n)), name, grid_n)
                            reset_trail()
                            history, idx, running = [cells.copy()], 0, False
                            render(); break
                    if not clicked:
                        dd_open = False; render()
                else:
                    if play_rect.collidepoint(mx, my):
                        running = not running; render()
                    elif reset_rect.collidepoint(mx, my):
                        do_reset()
                    elif dd_rect.collidepoint(mx, my):
                        dd_open = True; render()
                    elif track_rect.inflate(0, 20).collidepoint(mx, my):
                        dragging = True
                        sp_idx = max(0, min(len(speeds)-1,
                            round((mx-track_rect.x)/track_rect.w*(len(speeds)-1)))); render()
                    elif gridb_rect.collidepoint(mx, my):
                        show_grid = not show_grid; render()
                    elif theme_rect.collidepoint(mx, my):
                        th = LIGHT if th is DARK else DARK
                        bg, aliven = th["bg_presets"][0], th["cell_presets"][0]; render()
                    elif trail_rect2.collidepoint(mx, my):
                        show_trail = not show_trail
                        if not show_trail: reset_trail()
                        render()
                    elif binary_rect.collidepoint(mx, my):
                        was_running = running
                        running = False
                        show_binary_view(cells, font_s, W, H)
                        running = was_running
                        render()
                    elif cw_trigger_rect.collidepoint(mx, my):
                        was_running = running
                        running = False
                        new_color = show_color_wheel(aliven, font_s, W, H)
                        aliven = new_color
                        running = was_running
                        render()
                    else:
                        for i, r in swatches(r3y, "bg").items():
                            if r.collidepoint(mx, my):
                                bg = th["bg_presets"][i]; render(); break
                        for i, r in swatches(r3y, "cell").items():
                            if r.collidepoint(mx, my):
                                aliven = th["cell_presets"][i]; render(); break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    sp_idx = max(0, min(len(speeds)-1,
                        round((mx-track_rect.x)/track_rect.w*(len(speeds)-1))))
                render()

        if pygame.mouse.get_pressed()[0] and my < GH and not dd_open and not dragging:
            if not play_rect.collidepoint(mx,my) and not reset_rect.collidepoint(mx,my):
                col_, row_ = mx//size, my//size
                if 0 <= row_ < grid_n and 0 <= col_ < grid_n:
                    cells[row_, col_] = 1
                    history = history[:idx+1]; history[idx] = cells.copy(); render()

        if pygame.mouse.get_pressed()[2] and my < GH and not dd_open:
            col_, row_ = mx//size, my//size
            if 0 <= row_ < grid_n and 0 <= col_ < grid_n:
                cells[row_, col_] = 0
                history = history[:idx+1]; history[idx] = cells.copy(); render()

        if running:
            prev = cells.copy()
            new_c = update_cells(cells)
            if show_trail:
                died = (cells==1)&(new_c==0)
                trail[died] = TRAIL_DECAY; trail[new_c==1] = 0
                trail[:] = np.maximum(trail-1, 0)
            cells = new_c
            history = history[:idx+1]; history.append(cells.copy()); idx = len(history)-1
            render(prev)
            time.sleep(speeds[sp_idx])

if __name__ == "__main__":
    main()
