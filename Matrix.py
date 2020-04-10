from Vector import Vector


class Matrix:
    def __init__(self, *args, size=None):
        if size is None:
            self.array = list(list(arg) for arg in args)
        else:
            if type(size) == tuple:
                i, j = size
                if args:
                    if len(args) != i * j:
                        raise Exception(f'Dimensions i = {i} and j = {j} do not fit with args of length {len(args)}')
                    else:
                        self.array = [list(args[n*j:(n+1)*j]) for n in range(i)]
                else:
                    self.array = [[0] * j for _ in range(i)]
            else:
                raise Exception(f'Illegal parameter for size of type {type(size)}')
        self.i = len(self.array)
        self.j = len(self.array[0]) if self.array else 0
        self.dim = (self.i, self.j)
    
    def __len__(self):
        return self.i * self.j

    def __repr__(self):
        return 'Matrix(\n' + '\n'.join(str(x) for x in self.array) + '\n)'
    
    def __str__(self):
        return str(self.array)
    
    def __getitem__(self, idx):
        if isinstance(idx, Matrix):
            if idx.dim == self.dim:
                return Matrix(*([a if b else 0 for a, b in zip(a_row, b_row)] for a_row, b_row in zip(self.rows(), idx.rows())))
            else:
                raise Exception('Index Error! Both Matricies must have the same size')
        else:
            try:
                i, j = idx
            except:
                raise Exception('Index must be two dimensional')
            if type(i) == slice:
                return Matrix(*(x[j] for x in self.array[i]))
            else:
                return self.array[i][j]

    def __iter__(self):
        for row in self.array:
            for column in row:
                yield column
    
    def rows(self, *args):
        if len(args) == 0:
            start, stop, step = 0, self.i, 1
        elif len(args) == 1:
            start, stop, step = 0, *args, 1
        elif len(args) == 2:
            start, stop, step = *args, 1
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise Exception('Number of args must be between 0 and 3')
        for row in self.array[start:stop:step]:
            yield Vector(*row)
    
    def columns(self, *args):
        if len(args) == 0:
            start, stop, step = 0, self.j, 1
        elif len(args) == 1:
            start, stop, step = 0, *args, 1
        elif len(args) == 2:
            start, stop, step = *args, 1
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise Exception('Number of args must be between 0 and 3')
        for j in range(start, stop, step):
            yield Vector(*(self.array[i][j] for i in range(self.i)))
    
    def __bool__(self):
        return all(x is not False for x in self)

    def __comp(self, other, func):
        if isinstance(other, Matrix):
            if self.dim != other.dim:
                raise Exception(f'Maticies of dims {self.dim} and {other.dim} don\'t fit together')
            else:
                return Matrix(*([func(a, b) for a, b in zip(a_row, b_row)] for a_row, b_row in zip(self.array, other.array)))
        elif type(other) in {int, float, complex, bool}:
            return Matrix(*([func(x, other) for x in row] for row in self.array))
    
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
    
    def __abs__(self):
        return Matrix(*([abs(x) for x in row] for row in self.array))
    
    def __neg__(self):
        return Matrix(*([-x for x in row] for row in self.array))
    
    def __pos__(self):
        return self
    
    def __or__(self, other):
        if isinstance(other, Matrix):
            if not len(self):
                return other
            elif not len(other):
                return self
            elif self.i != other.i:
                raise Exception('Matricies have unfitting dimensions')
            else:
                return Matrix(*(a|b for a, b in zip(self.rows(), other.rows())))
        elif type(other) == Vector:
            if self.i != len(other):
                raise Exception('Matrix and Vector have unfitting dimensions')
            else:
                return Matrix(*(a|Vector(b) for a, b in zip(self.rows(), other)))
    
    def __ror__(self, other):
        if type(other) == Vector:
            if self.i != len(other):
                raise Exception('Matrix and Vector have unfitting dimensions')
            else:
                return Matrix(*(Vector(a)|b for a, b in zip(other, self.rows())))
    
    def t(self):
        return Matrix(*self.columns())
    
    def det(self):
        if self.i != self.j:
            raise Exception('Matrix must be square')
        elif self.i == 1:
            return self[0, 0]
        else:
            return sum((-1)**i * v * (self[1:,:i]|self[1:,i+1:]).det() for i, v in enumerate(self[0,:]))
    
    def adj(self):
        return Matrix(*([(-1)**(i+j) * ((self[:i,:j]|self[:i,j+1:]).t()|(self[i+1:,:j]|self[i+1:,j+1:]).t()).t().det() for j in range(self.j)] for i in range(self.i))).t()

    def inv(self):
        if not self.det() or self.i != self.j:
            raise Exception('Matrix is not invertable')
        return 1/self.det() * self.adj()

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.j != other.i:
                raise Exception('Matricies have unfitting dimensions')
            else:
                return Matrix(*(Vector(*(row * column for column in other.columns())) for row in self.rows()))
        elif type(other) == Vector:
            if len(other) != self.i:
                raise Exception('Unfitting dimensions')
            else:
                return Vector(*(other * row for row in self.rows()))
        elif type(other) in {int, float, complex}:
            return Matrix(*(other * row for row in self.rows()))
    
    def __rmul__(self, other):
        if type(other) == Vector:
            if len(other) != self.j:
                raise Exception('Unfitting dimensions')
            else:
                return Vector(*(other * column for column in self.columns()))
        elif type(other) in {int, float, complex}:
            return Matrix(*(other * row for row in self.rows()))
    
    def __truediv__(self, other):
        if isinstance(other, Matrix):
            if self.j != other.i:
                raise Exception('Matricies have unfitting dimensions')
            else:
                return self * other.inv()
        elif type(other) in {int, float, complex}:
            return self * (1/other)

    def __rtruediv__(self, other):
        if type(other) in {int, float, complex}:
            return self * (1/other)
        elif type(other) == Vector:
            return self.inv() * other

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.dim != other.dim:
                raise Exception('Matricies have unfitting dimensions')
            else:
                return Matrix(*(s_row + o_row for s_row, o_row in zip(self.rows(), other.rows())))
        elif type(other) in {int, float, complex}:
            return Matrix(*(other + row for row in self.rows()))
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.j != other.i:
                raise Exception('Matricies have unfitting dimensions')
            else:
                return Matrix(*(s_row - o_row for s_row, o_row in zip(self.rows(), other.rows())))
        elif type(other) in {int, float, complex}:
            return Matrix(*(row - other for row in self.rows()))
    
    def __rsub__(self, other):
        return -self + other


class Identity(Matrix):
    def __init__(self, dim):
        super().__init__(*(Vector(1, *(0 for _ in range(dim - 1))) >> i for i in range(dim)))