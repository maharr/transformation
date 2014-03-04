import math

from transformation.transformation.OSTN02 import OSGB36_to_ETRS89, ETRS89_to_OSGB36, GRS80, national_grid
from transformation.transformation.ll_en_converter import lat_long_to_east_north, east_north_to_lat_long


def test_OSGB36_to_ETRS89():
    e, n, h = 651409.792, 313177.448, 105.6
    x, y, z = OSGB36_to_ETRS89(e, n, h)
    lat, long = east_north_to_lat_long(x, y, GRS80, national_grid)
    assert round(lat, 8) == 52.65800783
    assert round(long, 8) == 1.71607397


def test_ETRS89_to_OSGB36():
    lat, long, z = 52.658007833, 1.716073973, 149.844
    x, y = lat_long_to_east_north(math.radians(lat), math.radians(long), GRS80, national_grid)
    e, n, h = ETRS89_to_OSGB36(x, y, z)
    assert round(e, 3) == 651409.792
    assert round(n, 3) == 313177.448