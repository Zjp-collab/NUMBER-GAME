class Complex:
    """
    Complex number of the form a + bi

    >>> a = Complex(5, -6)
    >>> b = Complex(2, 14)
    >>> a*b
    94 + 58i
    >>> b*5
    10 + 70i
    >>> 5*b
    10 + 70i
    >>> isinstance(5*b, Complex)
    True
    >>> a.conjugate()
    5 + 6i
    >>> b.conjugate()
    2 - 14i
    """

    def __init__(self, r, i):
        """Initialize real and imaginary parts"""
        self._real = r
        self._imag = i

    def __str__(self):
        """Display Complex number"""
        if self._imag >= 0:
            return f"{self._real} + {self._imag}i"
        else:
            return f"{self._real} - {abs(self._imag)}i"

    __repr__ = __str__

    def conjugate(self):
        """Return the complex conjugate as a new Complex object"""
        return Complex(self._real, -self._imag)

    def __mul__(self, other):
        """Multiply Complex by another Complex or a real number"""
        if isinstance(other, Complex):
            #Complex * Complex
            real_part = self._real * other._real - self._imag * other._imag
            imag_part = self._real * other._imag + self._imag * other._real
            ans = Complex(real_part, imag_part)
        else:  # assume other is int or float
            # Complex * real (int or float)
            real_part = self._real * other
            imag_part = self._imag * other
            ans = Complex(real_part, imag_part)
        return ans
    
    def __rmul__(self, other):
        """Multiply a real number by a Complex number"""
        return self * other

class Real(Complex):

    def __init__(self, value):
        super().__init__(value, 0)

    def __mul__(self, other):
        if isinstance(other, Real):
            return Real(self._real * other._real)

        if isinstance(other, (int, float)):
            return Real(self._real * other)

        if isinstance(other, Complex):
            return super().__mul__(other)

        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        if isinstance(other, Real):
            return self._real == other._real

        if isinstance(other, Complex):
            return self._real == other._real and other._imag == 0

        return False

    def __int__(self):
        return int(self._real)

    def __float__(self):
        return float(self._real)
