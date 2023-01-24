import pygame as pg
import sys
import math
pg.init()


def equation(x, y):
    try:
        return x * x - y  # this is the equation that will be displayed
    except Exception:
        return 100000000000000  # this is ideally always over the treshold


def update_screen():
    for x in range(W):
        for y in range(H):
            t_x = (x - x_offset) * xm  # transformed x
            t_y = -(y - y_offset) * ym  # transformed y
            if abs(equation(t_x, t_y)) < treshold:
                screen.set_at((x, y), (0, 0, 0))
            elif abs(int((x - x_offset))) == 0 or abs(int((y - y_offset))) == 0:
                screen.set_at((x, y), (0, 0, 0))
            elif abs(t_x - int(t_x)) < 0.1 and abs(t_y - int(t_y)) < 0.1:
                screen.set_at((x, y), (0, 0, 0))
            else:
                screen.set_at((x, y), (255, 255, 255))

    pg.display.update()


W = 500
H = 500
treshold = 0.2
xm = 0.1  # x multipiler
ym = 0.1  # y multiplier
x_offset = W // 2
y_offset = H // 2
MAX_ZOOM = 0.01
screen = pg.display.set_mode((W, H))
pg.display.set_caption("BER (Bad Equation Renderer)")
update_screen()

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_KP_PLUS:
                treshold += 0.1
                update_screen()
            elif e.key == pg.K_KP_MINUS:
                treshold -= 0.1
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
            print(treshold, xm, ym)
            update_screen()
