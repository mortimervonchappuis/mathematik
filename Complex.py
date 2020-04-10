from math import cos, sin, sqrt


class Complex:
	def __init__(self, *args):
		if not args:
			self.real = 0
			self.imag = 0
		elif len(args) == 1:
			self.real = cos(*args)
			self.imag = sin(*args)
		elif len(args) == 2:
			self.real, self.imag = args
		else:
			raise Exception(f'Too many arguments')

	def __mul__(self, other):
		if type(other) in {int, float}:
			return Complex(other*self.real, other*self.imag)
		elif type(other) in {Complex, complex}:
			return Complex(other.real*self.real - other.imag*self.imag, other.real*self.imag + other.imag*self.real)

	def __rmul__(self, other):
		return self * other

	def __add__(self, other):
		if type(other) in {int, float}:
			return Complex(other + self.real, self.imag)
		elif type(other) in {Complex, complex}:
			return Complex(other.real + self.real, other.imag + self.imag)

	def __radd__(self, other):
		return self + other

	def __truediv__(self, other):
		if type(other) in {int, float}:
			return Complex(self.real/other, self.imag/other)
	
	def __neg__(self):
		return -1 * self

	def __sub__(self, other):
		return self + - other

	def __repr__(self):
		return f"{self.real}{'+' if self.imag >= 0 else ''}{str(self.imag)}i"

	def __abs__(self):
		return sqrt(self.real**2 + self.imag**2)

	def __eq__(self, other):
		if type(other) in {float, int}:
			return self.real == other and self.imag == 0
		elif type(other) in {Complex, complex}:
			return self.real == other and self.imag == self.imag

	def __complex__(self):
		return self.real + 1j * self.imag
