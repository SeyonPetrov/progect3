import pygame as p


a, n = 0, 0
try:
    a, n = [int(x) for x in input().split()]
except ValueError:
    print('Неправильный формат ввода')


def chess_draw(screen):
    t = a // n
    r, f = 'black', 'white'
    u = r
    for z in range(n):
        if z % 2 != 0:
            u = r
        else:
            u = f
        for x in range(n):
            if u == r:
                u = f
            else:
                u = r
            p.draw.rect(screen, (u), (x * t, z * t, t, t), 0)


if __name__ == '__main__':
    p.init()
    size = (a, a)
    screen = p.display.set_mode(size)
    chess_draw(screen)
    p.display.flip()
    while p.event.wait().type != p.QUIT:
        pass
    p.quit()
