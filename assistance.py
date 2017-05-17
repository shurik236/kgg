import itertools


DELTAS = itertools.product(range(-1, 2), range(-1, 2))


def squared_distance(point_a, point_b):
    return (point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2


def draw_line(point_a, point_b):

    x1, y1 = point_a
    x2, y2 = point_b
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swap = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swap = True

    dx = x2 - x1
    dy = y2 - y1

    err = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    y = y1
    line = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        line.append(coord)
        err -= abs(dy)
        if err < 0:
            y += ystep
            err += dx

    if swap:
        line.reverse()

    return line
