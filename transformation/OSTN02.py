import math
import csv
from decimal import Decimal

x, y = 651307.003, 313255.686


class shifts(object):
    eshift = None
    nshift = None
    gshift = None

    def __init__(self, e, n):
        self.e = e
        self.n = n
        self.record = (e + (n * 701) + 1)
        print(self.record)


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

e = x + se
n = y + sn

print(round(e, 3), round(n, 3))