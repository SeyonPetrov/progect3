import pygame as pg


def balls(*all_need):
    clock = pg.time.Clock()
    screen, x, z = all_need
    for _ in range(1000):
        screen.fill(('black'))
        pg.draw.circle(screen, (('white')), (x, z), 10)
        x += 40 * clock.tick() / 1000
        z += 40 * clock.tick() / 1000


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Шарики')
    size = width, height = 500, 400
    screen = pg.display.set_mode(size)
    x, z = 0, 0

    running = True

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.MOUSEBUTTONUP and e.button == 1:
                x, z = pg.mouse.get_pos()
        if x or z:
            balls(screen, x, z)
    pg.quit()
