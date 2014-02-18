import math
import sys
import sqlite3
import os

import numpy

from ll_en_converter import projection_constant, ellipsoid, lat_long_to_east_north, east_north_to_lat_long


national_grid = projection_constant(0.9996012717, math.radians(49), math.radians(-2), 400000, -100000)

airy_1830 = ellipsoid(6377563.396, 6356256.910, "OSGB36 National Grid")
GRS80 = ellipsoid(6378137.0, 6356752.31425, "ETRS89 (WGS84)")

# x, y = 651307.003, 313255.686

class shifts(object):
    eshift = None
    nshift = None
    gshift = None

    def __init__(self, e, n):
        self.e = e
        self.n = n
        self.record = (e + (n * 701) + 1)
        #print(self.record)


def geodetic_to_ECEF(lat, long, height):
    x_1 = math.sqrt(1 - (GRS80.e_sq * ((math.sin(lat)) ** 2)))
    ECEF_x = ((GRS80.a / x_1) + height )
    x = ECEF_x * math.cos(lat) * math.cos(long)
    y = ECEF_x * math.cos(lat) * math.sin(long)
    z = (((GRS80.a * (1 - GRS80.e_sq)) / x_1) + height ) * math.sin(lat)
    #print(x, y, z)
    return x, y, z


def ECEF_to_geodetic(x, y, z):
    # estimate lat
    rootXYSq = math.sqrt((x ** 2) + (y ** 2))
    lat1 = math.atan(z / (rootXYSq * (1 - GRS80.e_sq)))
    v = GRS80.a / (math.sqrt(1 - (GRS80.e_sq * (math.sin(lat1) ** 2))))
    lat2 = math.atan((z + (GRS80.e_sq * v * math.sin(lat1))) / rootXYSq)
    while (lat1 - lat2) > 0.000000001:
        lat1 = lat2
        v = GRS80.a / (math.sqrt(1 - (GRS80.e_sq * (math.sin(lat1) ** 2))))
        lat2 = math.atan((z + (GRS80.e_sq * v * math.sin(lat1))) / rootXYSq)
    lat = math.degrees(lat2)
    #print(lat)
    if x >= 0:
        long = math.degrees(math.atan(y / x))
    elif x < 0 and y >= 0:  # longitude is in the W90 thru 0 to E90 hemisphere
        long = math.degrees(math.atan(y / x)) + 180
    elif x < 0 and y < 0:  # longitude is in the E90 to E180 quadrant
        long = math.degrees(math.atan(y / x)) - 180  # longitude is in the E180 to W90 quadrant
    v = GRS80.a / (math.sqrt(1 - (GRS80.e_sq * (math.sin(lat2) ** 2))))
    height = (rootXYSq / math.cos(lat2)) - v
    #print(lat)
    return lat, long, height


def transform(b, t, d, r):
    rd = numpy.matrix([[d, -r[0, 2], r[0, 1]], [r[0, 2], d, -r[0, 0]], [-r[0, 1], r[0, 0], d]]) + numpy.identity(3)
    a = (b - t) * rd.I
    return a


def ETRS89_to_WGS84(x, y, z):
    #etrs89 -> itrf90
    b = numpy.matrix([x, y, z])
    t = numpy.matrix([0.005, 0.024, -0.038])
    d = 0.0000000034
    r = numpy.matrix([0, 0, 0])
    a = transform(b, t, d, r)
    # itrf90 -> WGS84 (Doppler)
    b = a
    t = numpy.matrix([0.06, -0.517, -0.223])
    d = -0.000000011
    r = numpy.matrix([math.radians(0.0183), math.radians(-0.0003), math.radians(0.0070)]) / 3600
    #a = transform(b, t, d, r)
    #itrf90 -> ITRF2008
    b = a
    t = numpy.matrix([0.03, 0.039, -0.097])
    d = 0.0000000063
    r = numpy.matrix([0.0, 0.0, 0.0]) / 3600
    a = transform(b, t, d, r)

    #print(a)
    return a


def ETRS89_to_OSGB36(x0, y0, h0):
    sx, sy, sg = lookup_shifts(x0, y0)
    return x0 + sx, y0 + sy, h0 - sg


def OSGB36_to_ETRS89(x0, y0, h0):
    x1 = x0
    y1 = y0
    x2 = y2 = 0
    while x1 != x2:
        #print('loop')
        sx, sy, sg = lookup_shifts(x1, y1)
        #print(sx, sy)
        x2 = x1
        y2 = y1
        x1 = x0 - sx
        y1 = y0 - sy
        #print(x0, x1, x2, y0, y1, y2)
    h2 = h0 + sg
    return x1, y1, h2


def lookup_shifts(x, y):
    east_index = math.floor((x / 1000))
    north_index = math.floor(y / 1000)

    #print(east_index, north_index)

    # corners are labeled from the bottom left corner anti-clockwise
    corner = list()
    corner.append(shifts(east_index, north_index))
    corner.append(shifts(east_index + 1, north_index))
    corner.append(shifts(east_index + 1, north_index + 1))
    corner.append(shifts(east_index, north_index + 1))

    # temporary import path used until better solution can be found
    location = os.path.join((os.path.dirname(__file__)), 'OSTN02_OSGM02.db')
    conn = sqlite3.connect(location)
    c = conn.cursor()

    for i in range(0, 4):
        c.execute("SELECT * FROM lookup WHERE record=:record", {"record": corner[i].record})
        row = c.fetchone()
        #j = lookup[str(corner[i].record)][3]
        corner[i].eshift = row[3]
        corner[i].nshift = row[4]
        corner[i].gshift = row[5]
        #k = lookup[str(corner[i].record)][4]
        #corner[i].nshift = float(k.strip(' '))
        #l = lookup[str(corner[i].record)][5]
        #corner[i].gshift = float(l.strip(' '))
        #print(corner[i].eshift, corner[i].nshift, corner[i].gshift)

    x0 = east_index * 1000.
    y0 = north_index * 1000.

    dx = x - x0
    dy = y - y0

    t = round(dx / 1000, 8)
    u = round(dy / 1000, 8)

    #print(t, u)

    se = ((1 - t) * (1 - u) * corner[0].eshift) + (t * (1 - u) * corner[1].eshift) + (t * u * corner[2].eshift) + (
        (1 - t) * u * corner[3].eshift)
    sn = ((1 - t) * (1 - u) * corner[0].nshift) + (t * (1 - u) * corner[1].nshift) + (t * u * corner[2].nshift) + (
        (1 - t) * u * corner[3].nshift)
    sg = ((1 - t) * (1 - u) * corner[0].gshift) + (t * (1 - u) * corner[1].gshift) + (t * u * corner[2].gshift) + (
        (1 - t) * u * corner[3].gshift)

    #print(se, sn, sg)

    return se, sn, sg


def webgui_convert(inpute, inputn, inputh, convert):
    e, n, h = OSGB36_to_ETRS89(inpute, inputn, inputh)
    x, y = east_north_to_lat_long(e, n, GRS80, national_grid)
    if convert:
        x, y, z = geodetic_to_ECEF(math.radians(x), math.radians(y), h)
        a = ETRS89_to_WGS84(x, y, z)
        x, y, z = ECEF_to_geodetic(a[0, 0], a[0, 1], a[0, 2])
    else:
        z = h
    return x, y, z


def webgui_reverse(inputlat, inputlng, inputh):
    x, y = lat_long_to_east_north(math.radians(inputlat), math.radians(inputlng), GRS80, national_grid)
    e, n, h = ETRS89_to_OSGB36(x, y, inputh)
    return e, n, h


if len(sys.argv) > 1:
    arguments = sys.argv
    if arguments[1] == 'OSGB36':
        e, n, h = OSGB36_to_ETRS89(float(arguments[2]), float(arguments[3]), float(arguments[4]))
        x, y = east_north_to_lat_long(e, n, GRS80, national_grid)
        print(x, y, h)
        x, y, z = geodetic_to_ECEF(math.radians(x), math.radians(y), h)
        a = ETRS89_to_WGS84(x, y, z)
        lat, long, height = ECEF_to_geodetic(a[0, 0], a[0, 1], a[0, 2])
        print(lat)
        print(long)
        print(height)
        print(a)




    elif arguments[1] == 'ETRS89':
        if arguments[2] == 'DD':
            x, y = lat_long_to_east_north(math.radians(float(arguments[3])),
                                          math.radians(float(arguments[4])), GRS80, national_grid)
            e, n = ETRS89_to_OSGB36(x, y)
            print(e, n)

        elif arguments[2] == 'DMS':
            print('not currently supported')

    else:
        print('not currently supported')


