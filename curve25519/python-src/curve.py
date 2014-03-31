import _curve25519
from intbytes import int2bytes, bytes2int
from numbers import Integral

def curve(element, point):
    assert isinstance(element, SubElement)
    assert isinstance(point, Point)
    return Point(_curve25519.curve(element, point))

class Point(bytes):
    """Class representing the x coordinate of points on Curve25519"""
    def __new__(cls, x):
        if isinstance(x, Integral):
            x = int2bytes(x, length=32, endian='little')
        if not isinstance(x, bytes):
            raise TypeError("Can only instantiate Point instances from integers or bytes")
        return super(Point, cls).__new__(cls, x)
    def __mul__(self, other):
        if not isinstance(other, Element):
            raise TypeError("Points can only be multiplied by elements")
        return Point(_curve25519.curve(other, self))
    def __rmul__(self, other):
        return self * other

class Element(bytes):
    """Class representing elements of the field Z_p"""
    def __new__(cls, x):
        if isinstance(x, Integral):
            x = int2bytes(x % bytes2int(p, endian='little'),
                          length=32,
                          endian='little')
        elif isinstance(x, bytes):
            if len(x) != 32:
                raise ValueError("When instantiating Element from bytes, argument must be of length 32")
            x = int2bytes(bytes2int(x, endian='little') % bytes2int(p, endian='little'),
                          length=32,
                          endian='little')
        else:
            raise TypeError("Can only instantiate Element instances from integers or bytes")
        return super(Element, cls).__new__(cls, x)
    def __mul__(self, other):
        if not isinstance(other, Element):
            raise TypeError("Multiplication is only defined on Element's")
        return Element(_curve25519.mul(self, other))
    def __rmul__(self, other):
        return self * other
    def __div__(self, other):
        if not isinstance(other, Element):
            raise TypeError("Division is only defined on Element's")
        return Element(_curve25519.mul(self, _curve25519.recip(other)))
    def __rdiv__(self, other):
        if not isinstance(other, Element):
            raise TypeError("Division is only defined on Element's")
        return Element(_curve25519.mul(_curve25519.recip(self), other))

class SubElement(Element):
    """Class representing values of n for which it is safe to calculate n*G on Curve25519 (where G is the base point)"""
    def __new__(cls, x):
        if isinstance(x, Integral):
            x = _curve25519.make_seckey(int2bytes(x, length=32, endian='little'))
        elif isinstance(x, bytes):
            if len(x) != 32:
                raise ValueError("When instantiating SubElement from bytes, argument must be of length 32")
            x = _curve25519.make_seckey(x)
        else:
            raise TypeError("Can only instantiate SubElement instances from integers or bytes")
        return super(SubElement, cls).__new__(cls, x)


p = 2**255 - 19 # curve is defined over the field Z_p
q = 2**252 + 27742317777372353535851937790883648493 # order of the group generated by the base
base = 9
bad_public_keys = [0,
                   1,
                   325606250916557431795983626356110631294008115727848805560023387167927233504,
                   39382357235489614581723060781553021112529911719440698176882885853963445705823,
                   p - 1,
                   p,
                   p + 1,
                   p + 325606250916557431795983626356110631294008115727848805560023387167927233504,
                   p + 39382357235489614581723060781553021112529911719440698176882885853963445705823,
                   2*p - 1,
                   2*p,
                   2*p + 1]
p = int2bytes(p, length=32, endian='little')
q = int2bytes(q, length=32, endian='little')
base = Point(base)
bad_public_keys = map(Point,
                      bad_public_keys)
    
__all__ = ['p','q','base','bad_public_keys','curve','Point','Element','SubElement']
