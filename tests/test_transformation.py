from transformation.OSTN02 import OSGB36_to_ETRS89, ETRS89_to_OSGB36, GRS80, national_grid
from transformation.ll_en_converter import lat_long_to_east_north, east_north_to_lat_long
import math


def test_OSGB36_to_ETRS89():
    lat, long = 651409.792, 313177.448
    e, n = OSGB36_to_ETRS89(lat, long)
    x, y = east_north_to_lat_long(e, n, GRS80, national_grid)
    assert round(x, 8) == 52.65800783
    assert round(y, 8) == 1.71607397


def test_ETRS89_to_OSGB36():
    x, y = 52.658007833, 1.716073973
    x, y = lat_long_to_east_north(math.radians(x), math.radians(y), GRS80, national_grid)
    e, n = ETRS89_to_OSGB36(x, y)
    assert round(e, 3) == 651409.792
    assert round(n, 3) == 313177.448
