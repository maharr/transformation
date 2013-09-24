import math
class projection_constant(object):
	"""docstring for projection_constant"""
	def __init__(self, F_0, phi_0, lambda_0, E_0, N_0):
		super(projection_constant, self).__init__()
		self.F_0 = F_0
		self.phi_0 = phi_0
		self.lambda_0 = lambda_0
		self.E_0 = E_0
		self.N_0 = N_0
		

class ellipsoid(object):
	"""docstring for ellipsoid"""
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.e_sq = (math.pow(a,2) - math.pow(b,2)) / math.pow(a,2)
		self.n = (a-b)/(a+b)


national_grid = projection_constant(0.9996012717, math.radians(49), math.radians(2), 400000, -100000)



airy_1830 = ellipsoid(6377563.396,6356256.910)
GRS80 = ellipsoid(6378137.0, 6356752.314)


print airy_1830.e_sq
print GRS80.e_sq