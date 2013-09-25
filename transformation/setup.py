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
        print self.description, ' e squared: ', self.e_sq


national_grid = projection_constant(0.9996012717, math.radians(49), math.radians(-2), 400000, -100000)

airy_1830 = ellipsoid(6377563.396, 6356256.910, "OSGB36 National Grid")
GRS80 = ellipsoid(6378137.0, 6356752.31425, "ETRS89 (WGS84)")


def lat_long_to_east_north(lat, long, ellipsoid_used, projection_used):
    n = (ellipsoid_used.a - ellipsoid_used.b) / (ellipsoid_used.a + ellipsoid_used.b)
    print 'n: ', n
    nu = ellipsoid_used.a * projection_used.F_0 * ((1 - (ellipsoid_used.e_sq * ((math.sin(lat)) ** 2) )) ** -0.5)
    print 'v: ', nu
    rho = ellipsoid_used.a * projection_used.F_0 * (1 - ellipsoid_used.e_sq) * (
        1 - (ellipsoid_used.e_sq * (math.sin(lat) ** 2))) ** -1.5
    print 'rho: ', rho
    eta_sq = (nu / rho) - 1
    print 'eta squared: ', eta_sq
    phi_minus = lat - projection_used.phi_0
    phi_plus = lat + projection_used.phi_0
    m = ellipsoid_used.b * projection_used.F_0 * (
        ((1 + n + ((5. / 4) * (n ** 2)) + ((5. / 4) * (n ** 3))) * (phi_minus)) - (
            ((3 * n) + (3 * (n ** 2)) + ((21. / 8) * (n ** 3))) * math.sin(phi_minus) * math.cos(phi_plus)) + (
            (((15. / 8) * (n ** 2)) + ((15. / 8) * ( n ** 3))) * math.sin(2 * phi_minus) * math.cos(2 * phi_plus)) - (
            ((35. / 24) * (n ** 3)) * math.sin(3 * phi_minus) * math.cos(3 * (phi_plus))))

    print 'm: ', m

    i = m + projection_used.N_0
    print 'i: ', i

    ii = (nu / 2) * math.sin(lat) * math.cos(lat)
    print 'ii: ', ii

    iii = (nu / 24) * math.sin(lat) * (math.cos(lat) ** 3) * (5 - ((math.tan(lat) ** 2)) + 9 * eta_sq)
    print 'iii: ', iii

    iiia = (nu / 720) * math.sin(lat) * (math.cos(lat) ** 5) * (
        61 - (58 * ((math.tan(lat) ** 2))) + ((math.tan(lat) ** 4)))
    print 'iiia: ', iiia

    iv = nu * math.cos(lat)
    print 'iv: ', iv

    v = nu / 6 * ((math.cos(lat) ** 3)) * ((nu / rho) - (math.tan(lat) ** 2))
    print 'v: ', v

    vi = (nu / 120.) * (math.cos(lat) ** 5) * (
        5. - (18. * (math.tan(lat) ** 2)) + (math.tan(lat) ** 4) + (14. * eta_sq) - (
        58. * (math.tan(lat) ** 2) * eta_sq))
    print 'vi: ', vi

    lam_minus = long - projection_used.lambda_0

    n = i + (ii * lam_minus ** 2) + (iii * lam_minus ** 4) + (iiia * lam_minus ** 6)
    print 'n: ', n

    e = projection_used.E_0 + (iv * lam_minus) + (v * lam_minus ** 3) + (vi * lam_minus ** 5)
    print 'e: ', e

    return round(e, 3), round(n, 3)


eastings, northings = lat_long_to_east_north(math.radians(latitude), math.radians(longitude), GRS80, national_grid)

print '\n', eastings, northings