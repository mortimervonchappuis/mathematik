from math import sqrt


class Vector:
    def __init__(self, *args, size=None):
        if size is None:
            self.array = args
        else:
            if type(size) == int:
                if args:
                    self.array = args * (size//len(args))
                else:
                    self.array = [0] * size
            else:
                raise Exception(f'Illegal size of type {type(size)}')
        self.dim = len(self.array)
    
    def __len__(self):
        return self.dim
    
    def __repr__(self):
        return f'Vector({", ".join(str(x) for x in self)})'
    
    def __str__(self):
        return str(self.array)
    
    def __or__(self, other):
        return Vector(*self.array, *other.array)
    
    def __lshift__(self, idx):
        return Vector(*self[idx:], *self[:idx])
    
    def __rshift__(self, idx):
        return Vector(*self[-idx:], *self[:-idx])

    def __getitem__(self, idx):
        if type(idx) == Vector:
            if self.dim != idx.dim:
                raise Exception(f'Vectors of dimensions {self.dim} and {idx.dim} are not compatible for addition')
            return Vector(*(x if y else 0 for x, y in zip(self, idx)))
        elif type(idx) == int:
            return self.array[idx % self.dim]
        elif type(idx) == slice:
            return self.array[idx]
        else:
            raise Exception(f'Illegal index of type {type(idx)}')
    
    def __iter__(self, idx=None):
        if idx is None:
            for x in self.array:
                yield x
        else:
            for x in self.array[idx]:
                yield x

    def __bool__(self):
        return all(x is not False for x in self)

    def __comp(self, other, func):
        if type(other) == Vector:
            if self.dim != other.dim:
                raise Exception(f'Vectors of dim {self.dim} and {other.dim} don\'t fit together')
            else:
                return Vector(*(func(a, b) for a, b in zip(self.array, other.array)))
        elif type(other) in {int, float, complex, bool}:
            return Vector(*(func(x, other) for x in self))
    
    def __eq__(self, other):
        return self.__comp(other, func=lambda a, b: a == b)
    
    def __ne__(self, other):
        return self.__comp(other, func=lambda a, b: a != b)
    
    def __lt__(self, other):
        return self.__comp(other, func=lambda a, b: a < b)
    
    def __le__(self, other):
        return self.__comp(other, func=lambda a, b: a <= b)
    
    def __gt__(self, other):
        return self.__comp(other, func=lambda a, b: a > b)
    
    def __ge__(self, other):
        return self.__comp(other, func=lambda a, b: a >= b)
    
    def __req__(self, other):
        return self.__comp(other, func=lambda a, b: b == a)
    
    def __rne__(self, other):
        return self.__comp(other, func=lambda a, b: b != a)
    
    def __rlt__(self, other):
        return self.__comp(other, func=lambda a, b: b > a)
    
    def __rle__(self, other):
        return self.__comp(other, func=lambda a, b: b >= a)
    
    def __rgt__(self, other):
        return self.__comp(other, func=lambda a, b: b < a)
    
    def __rge__(self, other):
        return self.__comp(other, func=lambda a, b: b <= a)
    
    def __neg__(self):
        return Vector(*(-x for x in self))
    
    def __pos__(self):
        return self
                
    def __add__(self, other):
        if type(other) == Vector:
            if self.dim != other.dim:
                raise Exception(f'Vectors of dimensions {self.dim} and {other.dim} are not compatible for addition')
            return Vector(*(x + y for x, y in zip(self, other)))
        elif type(other) in {float, int, complex}:
            return Vector(*(x + other for x in self))
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if type(other) == Vector:
            if self.dim != other.dim:
                raise Exception(f'Vectors of dimensions {self.dim} and {other.dim} are not compatible for addition')
            return Vector(*(x - y for x, y in zip(self, other)))
        elif type(other) in {float, int, complex}:
            return Vector(*(x - other for x in self))
    
    def __rsub__(self, other):
        return -1*self + other
    
    def __mul__(self, other):
        if type(other) == Vector:
            if self.dim != other.dim:
                raise Exception(f'Vectors of dimensions {self.dim} and {other.dim} are not compatible for dot product')
            return sum(x * y for x, y in zip(self, other))
        elif type(other) in {int, float, complex}:
            return Vector(*(x * other for x in self))
        else:
            raise Exception(f'Illegal index of type {type(other)}')
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        if type(other) in {int, float, complex}:
            return self * (1/other)
        try:
            return other.inv() * self
        except:
            raise Exception('Undefined')

    def __abs__(self):
        return Vector(*(abs(x) for x in self))

    def norm(self):
        return sqrt(self*self)
