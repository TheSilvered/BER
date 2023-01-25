import pygame as pg
import sys
from math import *
pg.init()


def equation(x, y):
    try:
        # this is the equation that will be plotted
        return sin(cos(tan(x * y))) - sin(cos(tan(x))) - sin(cos(tan(y)))
    except Exception:
        return 1


def update_section(from_x, from_y, to_x, to_y):
    for x in range(from_x, to_x, 1):
        for y in range(from_y, to_y, 1):
            t_x = (x - x_offset) * xm  # transformed x
            t_y = -(y - y_offset) * ym  # transformed y
            res = abs(equation(t_x, t_y))
            if res > treshold:
                res = 1
            else:
                res *= 1 / treshold
            screen.set_at((x, y), (255 * res, 255 * res, 255 * res))

            if abs(int((x - x_offset))) == 0 or abs(int((y - y_offset))) == 0:
                screen.set_at((x, y), (0, 0, 0))
            if abs(t_x - int(t_x)) < 0.1 and abs(t_y - int(t_y)) < 0.1:
                screen.set_at((x, y), (0, 0, 0))


def update_screen():
    global prev_x_offset, prev_y_offset, prev_treshold, prev_xm, prev_ym

    if xm != prev_xm or ym != prev_ym or treshold != prev_treshold:
        update_section(0, 0, W, H)
    else:
        delta_x = x_offset - prev_x_offset
        delta_y = y_offset - prev_y_offset

        if delta_x > 0:
            x_from = 0
            x_to = delta_x
        else:
            x_from = W + delta_x
            x_to = W

        if delta_y > 0:
            y_from = 0
            y_to = delta_y
        else:
            y_from = H + delta_y
            y_to = H

        temp = pg.Surface((W, H))
        temp.blit(screen, (delta_x, delta_y))
        screen.blit(temp, (0, 0))
        update_section(x_from, 0, x_to, H)
        if delta_x < 0:
            update_section(0, y_from, W + delta_x, y_to)
        else:
            update_section(delta_x, y_from, W, y_to)

    prev_x_offset = x_offset
    prev_y_offset = y_offset
    prev_treshold = treshold
    prev_xm = xm
    prev_ym = ym

    pg.display.update()

W = 500
H = 500
treshold = 1.0
xm = 0.05  # x multipiler
ym = 0.05  # y multiplier
x_offset = W // 2
y_offset = H // 2
MAX_ZOOM = 0.01
screen = pg.display.set_mode((W, H))
pg.display.set_caption("BER (Bad Equation Renderer)")

prev_xm = xm
prev_ym = ym
prev_x_offset = -x_offset
prev_y_offset = -y_offset
prev_treshold = treshold

update_screen()

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_KP_PLUS:
                if treshold < 0.10005:
                    treshold += 0.01
                else:
                    treshold += 0.1
                if treshold > 1:
                    treshold = 1
                update_screen()
            elif e.key == pg.K_KP_MINUS:
                if treshold < 0.10005:
                    treshold -= 0.01
                else:
                    treshold -= 0.1
                if treshold < 0.01:
                    treshold = 0.01
                update_screen()
            elif e.key == pg.K_l:
                xm -= 0.06 * xm
                if xm < MAX_ZOOM:
                    xm = MAX_ZOOM
                update_screen()
            elif e.key == pg.K_j:
                xm += 0.06 * xm
                update_screen()
            elif e.key == pg.K_i:
                ym -= 0.06 * ym
                if ym < MAX_ZOOM:
                    ym = MAX_ZOOM
                update_screen()
            elif e.key == pg.K_k:
                ym += 0.06 * ym
                update_screen()

        elif e.type == pg.MOUSEMOTION and e.buttons[0]:
            x_offset += e.rel[0]
            y_offset += e.rel[1]
            update_screen()
        elif e.type == pg.MOUSEWHEEL:
            delta_x = e.y * 0.03 * xm
            delta_y = e.y * 0.03 * ym
            xm -= delta_x
            ym -= delta_y

            if xm != ym:
                if xm < ym and xm < MAX_ZOOM:
                    ym += delta_y
                    xm = MAX_ZOOM
                elif ym < MAX_ZOOM:
                    xm += delta_x
                    ym = MAX_ZOOM
            elif xm < MAX_ZOOM:
                xm = MAX_ZOOM
                ym = MAX_ZOOM

            m_x, m_y = pg.mouse.get_pos()
            x_offset -= int(round(((m_x - x_offset) * delta_x) / xm))
            y_offset -= int(round(((m_y - y_offset) * delta_y) / ym))
            update_screen()
