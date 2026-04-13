import numpy as np
import time
import pygame
import sys
import os

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
    gridb_rect = pygame.Rect(20,        r2y, icon_bw, icon_bw)
    theme_rect = pygame.Rect(20+icon_bw+8, r2y, icon_bw, icon_bw)
    trail_rect = pygame.Rect(20,        r2y, 80, 30)

    r3y = r2y + 56

    return (dd_rect, track_rect, gridb_rect, theme_rect, trail_rect,
            play_rect, reset_rect, r3y, r2y, icon_bw)

SW, SW_GAP = 26, 6

def swatches(y, kind):
    base = 20 if kind == "bg" else 20 + 5*(SW+SW_GAP) + 28
    return {i: pygame.Rect(base + i*(SW+SW_GAP), y, SW, 22) for i in range(5)}

def do_render(screen, cells, trail, prev, size, gen, font, font_s,
              sp_idx, tmpl_sel, dd_open, bg, aliven, dragging,
              mx, my, fps, th, show_grid, show_trail, running, W, H, GH,
              icons):

    (dd_rect, track_rect, gridb_rect, theme_rect, trail_rect,
     play_rect, reset_rect, r3y, r2y, icon_bw) = make_rects(W, H, GH)

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

    trail_rect2 = pygame.Rect(20 + 2*(icon_bw+8), r2y, 80, icon_bw)
    c = th["btn_act"] if show_trail else th["btn_hov"] if trail_rect2.collidepoint(mx, my) else th["btn"]
    pygame.draw.rect(screen, c, trail_rect2, border_radius=5)
    pygame.draw.rect(screen, th["div"], trail_rect2, 1, border_radius=5)
    tl = font_s.render("trail", True, th["text"])
    screen.blit(tl, (trail_rect2.x+(trail_rect2.w-tl.get_width())//2,
                     trail_rect2.y+(trail_rect2.h-tl.get_height())//2))

    screen.blit(font_s.render("bg",   True, th["text_dim"]), (20,  r3y-14))
    for i, col in enumerate(th["bg_presets"]):
        r = swatches(r3y, "bg")[i]
        draw_swatch(screen, r, col, r.collidepoint(mx, my), col == bg, th)

    cell_lbl_x = 20 + 5*(SW+SW_GAP) + 28
    screen.blit(font_s.render("cell", True, th["text_dim"]), (cell_lbl_x, r3y-14))
    for i, col in enumerate(th["cell_presets"]):
        r = swatches(r3y, "cell")[i]
        draw_swatch(screen, r, col, r.collidepoint(mx, my), col == aliven, th)

    draw_dropdown(screen, font_s, dd_rect, tmpl_sel or "select pattern",
                  dd_open, mx, my, th, GH)

    pygame.display.update()

def build_reset_text_surf(font, th):
    t = font.render("R", True, th["text"])
    s = pygame.Surface((t.get_width()+4, t.get_height()+4), pygame.SRCALPHA)
    s.blit(t, (2, 2))
    return s

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
         play_rect, reset_rect, r3y, r2y, icon_bw) = make_rects(W, H, GH)
        trail_rect2 = pygame.Rect(20 + 2*(icon_bw+8), r2y, 80, icon_bw)

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