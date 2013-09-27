import math

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
        self.e_sq = (a ** 2. - b ** 2.) / a ** 2.
        print(self.description, ' e squared: ', self.e_sq)
        self.n = (a - b) / (a + b)
        print('n: ', self.n)


def calculate_m(phi, ellipsoid_used, projection_used):
    phi_minus = phi - projection_used.phi_0
    phi_plus = phi + projection_used.phi_0
    m = ellipsoid_used.b * projection_used.F_0 * (
        ((1. + ellipsoid_used.n + ((5. / 4) * (ellipsoid_used.n ** 2.)) + (
            (5. / 4) * (ellipsoid_used.n ** 3.))) * phi_minus) - (
            ((3. * ellipsoid_used.n) + (3. * (ellipsoid_used.n ** 2.)) + (
                (21. / 8) * (ellipsoid_used.n ** 3.))) * math.sin(
                phi_minus) * math.cos(phi_plus)) + (
            (((15. / 8) * (ellipsoid_used.n ** 2.)) + ((15. / 8) * (ellipsoid_used.n ** 3))) * math.sin(
                2. * phi_minus) * math.cos(2 * phi_plus)) - (
            ((35. / 24) * (ellipsoid_used.n ** 3.)) * math.sin(3. * phi_minus) * math.cos(3. * phi_plus)))

    print('m: ', m)
    return m


national_grid = projection_constant(0.9996012717, math.radians(49), math.radians(-2), 400000, -100000)

airy_1830 = ellipsoid(6377563.396, 6356256.910, "OSGB36 National Grid")
GRS80 = ellipsoid(6378137.0, 6356752.31425, "ETRS89 (WGS84)")


def lat_long_to_east_north(phi, lam, ellipsoid_used, projection_used):
    nu = ellipsoid_used.a * projection_used.F_0 * ((1. - (ellipsoid_used.e_sq * ((math.sin(phi)) ** 2.) )) ** -0.5)
    print('v: ', nu)
    rho = ellipsoid_used.a * projection_used.F_0 * (1. - ellipsoid_used.e_sq) * (
        1. - (ellipsoid_used.e_sq * (math.sin(phi) ** 2.))) ** -1.5
    print('rho: ', rho)
    eta_sq = (nu / rho) - 1.
    print('eta squared: ', eta_sq)

    m = calculate_m(phi, ellipsoid_used, projection_used)

    i = m + projection_used.N_0
    print('i: ', i)

    ii = (nu / 2.) * math.sin(phi) * math.cos(phi)
    print('ii: ', ii)

    iii = (nu / 24. * math.sin(phi) * (math.cos(phi) ** 3.) * (5. - ((math.tan(phi) ** 2.)) + 9. * eta_sq))
    print('iii: ', iii)

    iiia = (nu / 720) * math.sin(phi) * (math.cos(phi) ** 5.) * (
        61. - (58. * ((math.tan(phi) ** 2.))) + ((math.tan(phi) ** 4.)))
    print('iiia: ', iiia)

    iv = nu * math.cos(phi)
    print('iv: ', iv)

    v = nu / 6. * ((math.cos(phi) ** 3.)) * ((nu / rho) - (math.tan(phi) ** 2.))
    print('v: ', v)

    vi = (nu / 120.) * (math.cos(phi) ** 5) * (
        5. - (18. * (math.tan(phi) ** 2)) + (math.tan(phi) ** 4.) + (14. * eta_sq) - (
            58. * (math.tan(phi) ** 2) * eta_sq))
    print('vi: ', vi)

    lam_minus = lam - projection_used.lambda_0

    N = i + (ii * lam_minus ** 2.) + (iii * lam_minus ** 4.) + (iiia * lam_minus ** 6.)
    print('n: ', N)

    E = projection_used.E_0 + (iv * lam_minus) + (v * lam_minus ** 3.) + (vi * lam_minus ** 5.)
    print('e: ', E)

    return round(E, 3), round(N, 3)


def east_north_to_lat_long(E, N, ellipsoid_used, projection_used):
    phi_dash = ((N - projection_used.N_0) / (ellipsoid_used.a * projection_used.F_0)) + projection_used.phi_0
    print('phi\': ', phi_dash)
    m = calculate_m(phi_dash, ellipsoid_used, projection_used)

    while (N - projection_used.N_0 - m) >= 0.01:
        phi_dash_new = ((N - projection_used.N_0 - m) / (ellipsoid_used.a * projection_used.F_0)) + phi_dash
        m = calculate_m(phi_dash_new, ellipsoid_used, projection_used)
        phi_dash = phi_dash_new

    nu = ellipsoid_used.a * projection_used.F_0 * ((1. - (ellipsoid_used.e_sq * ((math.sin(phi_dash)) ** 2.) )) ** -0.5)
    print('v: ', nu)
    rho = ellipsoid_used.a * projection_used.F_0 * (1. - ellipsoid_used.e_sq) * (
        1. - (ellipsoid_used.e_sq * (math.sin(phi_dash) ** 2.))) ** -1.5
    print('rho: ', rho)
    eta_sq = (nu / rho) - 1.
    print('eta squared: ', eta_sq)

    vii = (math.tan(phi_dash)) / (2 * rho * nu)
    print('vii: ', vii)

    viii = (math.tan(phi_dash) / (24. * rho * (nu ** 3))) * (
    5 + (3 * (math.tan(phi_dash) ** 2)) + eta_sq - (9 * (math.tan(phi_dash) ** 2) * eta_sq))
    print('viii: ', viii)

    ix = (math.tan(phi_dash) / (720. * rho * (nu ** 5))) * (
    61 + (90 * (math.tan(phi_dash) ** 2)) + (45 * (math.tan(phi_dash) ** 4)))
    print('ix: ', ix)

    x = (1. / math.cos(phi_dash)) / nu
    print('x: ', x)

    xi = (1. / math.cos(phi_dash)) / (6 * (nu ** 3)) * ((nu / rho) + (2 * (math.tan(phi_dash) ** 2)))
    print('xi: ', xi)

    xii = (1. / math.cos(phi_dash)) / (120 * (nu ** 5)) * (
    5 + (28 * (math.tan(phi_dash) ** 2)) + (24 * (math.tan(phi_dash) ** 4)))
    print('xii: ', xii)

    xiia = (1. / math.cos(phi_dash)) / (5040 * (nu ** 7)) * (
    61 + (662 * (math.tan(phi_dash) ** 2)) + (1320 * (math.tan(phi_dash) ** 4)) + (720 * (math.tan(phi_dash) ** 6)))
    print('xiia: ', xiia)

    phi = phi_dash - vii * (E - projection_used.E_0) ** 2 + viii * (E - projection_used.E_0) ** 4 - ix * (
                                                                                                         E - projection_used.E_0) ** 6
    lam = projection_used.lambda_0 + x * (E - projection_used.E_0) - xi * (E - projection_used.E_0) ** 3 + xii * (
                                                                                                                 E - projection_used.E_0) ** 5 - xiia * (
                                                                                                                                                        E - projection_used.E_0) ** 7

    return math.degrees(phi), math.degrees(lam)

# temporary eastings and northing for testing

latitude = 52.658007833
longitude = 1.716073973

eastings, northings = lat_long_to_east_north(math.radians(latitude), math.radians(longitude), GRS80, national_grid)

print('\n', eastings, northings)

eastings = 651409.903
northings = 313177.270

latitude, longitude = east_north_to_lat_long(eastings, northings, GRS80, national_grid)

print('\n', latitude, longitude)