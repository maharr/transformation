import math

# temporary eastings and northing for testing

latitude = 52.658007833
longitude = 1.716073973


class projection_constant(object):
    def __init__(self, F_0, phi_0, lambda_0, E_0, N_0):
        super(projection_constant, self).__init__()
        self.F_0 = F_0
        self.phi_0 = phi_0
        self.lambda_0 = lambda_0
        self.E_0 = E_0
        self.N_0 = N_0


class ellipsoid(object):
    def __init__(self, a, b, description):
        self.a = a
        self.b = b
        self.description = description
        self.e_sq = (a ** 2 - b ** 2) / a ** 2


national_grid = projection_constant(0.9996012717, math.radians(49), math.radians(2), 400000, -100000)

airy_1830 = ellipsoid(6377563.396, 6356256.910, "OSGB36 National Grid")
GRS80 = ellipsoid(6378137.0, 6356752.314, "ETRS89 (WGS84)")


def lat_long_to_east_north(lat, long, ellipsoid_used, projection_used):
    n = (ellipsoid_used.a - ellipsoid_used.b) / (ellipsoid_used.a + ellipsoid_used.b)
    v = ellipsoid_used.a * projection_used.F_0 * (1 - (ellipsoid_used.e_sq * (math.sin(lat) ** 2))) ** -0.5
    print v
    rho = ellipsoid_used.a * projection_used.F_0 * (1 - ellipsoid_used.e_sq) * (
        1 - (ellipsoid_used.e_sq * (math.sin(lat) ** 2))) ** -1.5
    print rho
    eta_sq = (v / rho) - 1
    print eta_sq


lat_long_to_east_north(latitude, longitude, GRS80, national_grid)

print airy_1830.e_sq
print GRS80.e_sq