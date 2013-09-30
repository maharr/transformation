import math
import csv
from decimal import Decimal
import sys
import ll_en_converter

national_grid = ll_en_converter.projection_constant(0.9996012717, math.radians(49), math.radians(-2), 400000, -100000)

airy_1830 = ll_en_converter.ellipsoid(6377563.396, 6356256.910, "OSGB36 National Grid")
GRS80 = ll_en_converter.ellipsoid(6378137.0, 6356752.31425, "ETRS89 (WGS84)")

# x, y = 651307.003, 313255.686


class shifts(object):
    eshift = None
    nshift = None
    gshift = None

    def __init__(self, e, n):
        self.e = e
        self.n = n
        self.record = (e + (n * 701) + 1)
        print(self.record)


def ETRS89_to_OSGB36(x0, y0):
    sx, sy = lookup_shifts(x0, y0)
    return x0 + sx, y0 + sy


def OSGB36_to_ETRS89(x0, y0):
    x1 = x0
    y1 = y0
    x2 = y2 = 0
    while x1 != x2:
        print('loop')
        sx, sy = lookup_shifts(x1, y1)
        print(sx, sy)
        x2 = x1
        y2 = y1
        x1 = x0 - sx
        y1 = y0 - sy
        print(x0, x1, x2, y0, y1, y2)
    return x1, y1


def lookup_shifts(x, y):
    east_index = math.floor((x / 1000))
    north_index = math.floor(y / 1000)

    print(east_index, north_index)

    # corners are labeled from the bottom left corner anti-clockwise
    corner = list()
    corner.append(shifts(east_index, north_index))
    corner.append(shifts(east_index + 1, north_index))
    corner.append(shifts(east_index + 1, north_index + 1))
    corner.append(shifts(east_index, north_index + 1))

    with open('OSTN02_OSGM02_GB.csv') as fin:
        csvin = csv.reader(fin)
        lookup = {row[0]: row for row in csvin}

    for i in range(0, 4):
        j = lookup[str(corner[i].record)][3]
        corner[i].eshift = float(j.strip(' '))
        k = lookup[str(corner[i].record)][4]
        corner[i].nshift = float(k.strip(' '))
        l = lookup[str(corner[i].record)][5]
        corner[i].gshift = float(l.strip(' '))
        print(corner[i].eshift, corner[i].nshift, corner[i].gshift)

    x0 = east_index * 1000.
    y0 = north_index * 1000.

    dx = x - x0
    dy = y - y0

    t = round(dx / 1000, 8)
    u = round(dy / 1000, 8)

    print(t, u)

    se = ((1 - t) * (1 - u) * corner[0].eshift) + (t * (1 - u) * corner[1].eshift) + (t * u * corner[2].eshift) + (
        (1 - t) * u * corner[3].eshift)
    sn = ((1 - t) * (1 - u) * corner[0].nshift) + (t * (1 - u) * corner[1].nshift) + (t * u * corner[2].nshift) + (
        (1 - t) * u * corner[3].nshift)
    sg = ((1 - t) * (1 - u) * corner[0].gshift) + (t * (1 - u) * corner[1].gshift) + (t * u * corner[2].gshift) + (
        (1 - t) * u * corner[3].gshift)

    print(se, sn, sg)

    return se, sn


if len(sys.argv) > 1:
    arguments = sys.argv
    if arguments[1] == 'OSGB36':
        e, n = OSGB36_to_ETRS89(float(arguments[2]), float(arguments[3]))
        x, y = ll_en_converter.east_north_to_lat_long(e, n, GRS80, national_grid)
        print(e, n)


    elif arguments[1] == 'ETRS89':
        if arguments[2] == 'DD':
            x, y = ll_en_converter.lat_long_to_east_north(math.radians(float(arguments[3])),
                                                          math.radians(float(arguments[4])), GRS80, national_grid)
            e, n = ETRS89_to_OSGB36(x, y)
            print(e, n)

        elif arguments[2] == 'DMS':
            print('not currently supported')

    else:
        print('not currently supported')


