from collections.abc import Iterable, Hashable, Container, Sized
from enum import IntEnum, unique
from numbers import Real
import sys
import math



@unique
class Rotation(IntEnum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class Vector2D(Sized, Iterable, Hashable, Container):
    @staticmethod
    def round(vec, n):
        vec.x = round(vec.x, n)
        vec.y = round(vec.y, n)
        return vec

    @staticmethod
    def wrap_around(vec, maxx, maxy):
        if vec.x > maxx:
            vec.x = 0
        if vec.x < 0:
            vec.x = maxx
        if vec.y > maxy:
            vec.y = 0
        if vec.y < 0:
            vec.y = maxy
        return vec

    @staticmethod
    def inside_region_vec(vec, vec_top_left, vec_bottom_right):
        return (vec.x >= vec_top_left.x and vec.y >= vec_top_left.y and
                vec.x <= vec_bottom_right.x and vec.x <= vec_bottom_right.y)

    @staticmethod
    def inside_region_pt(vec, top, left, bottom, right):
        return (vec.x >= left and vec.y >= top and
                vec.x <= right and vec.x <= bottom)

    @staticmethod
    def in_FOV(source, direction, target, fov):
        to_target = (target - source).normalize()
        return direction * to_target >= math.cos(fov / 2.0)

    __slots__ = ('__x', '__y')

    def __init__(self, x=0, y=0):
        self.__x = None
        self.__y = None
        self.__sub_init(x, y)

    def __sub_init(self, x, y):
        self.x = x
        self.y = y

    def __get_x(self):
        return self.__x

    def __set_x(self, value):
        assert isinstance(value, Real)
        self.__x = value

    def __get_y(self):
        return self.__y

    def __set_y(self, value):
        assert isinstance(value, Real)
        self.__y = value

    def __get_length(self):
        '''Returns the length of a 2D vector
        '''
        return (self.__x**2 + self.__y**2)**0.5

    def __get_length_sq(self):
        '''Returns the squared length of the vector (thereby avoiding the sqrt)
        '''
        return self.__x**2 + self.__y**2

    def __get_perp(self):
        '''Returns the vector that is perpendicular to this one
        '''
        return Vector2D(-self.__y, self.__x)

    def __get_reverse(self):
        '''The vector that is the reverse of this vector
        '''
        return Vector2D(-self.__x, -self.__y)

    x = property(__get_x, __set_x)
    y = property(__get_y, __set_y)
    length = property(__get_length)
    length_sq = property(__get_length_sq)
    perp = property(__get_perp)
    reverse = property(__get_reverse)

    def set(self, vec):
        self.__x = vec.x
        self.__y = vec.y
        return self

    def make_zero(self):
        '''Sets x and y to zero
        '''
        self.__x = 0
        self.__y = 0
        return self

    def is_zero(self):
        '''Returns true if both x and y are zero
        '''
        return self.__x**2 + self.__y**2 < sys.float_info.min

    def sign(self, other):
        '''Returns positive if <other> is clockwise of this vector,
        negative if anticlockwise (assuming the Y axis is pointing down,
        X axis to right like a pygame app)
        '''
        return (Rotation.COUNTERCLOCKWISE
                if self.__y * other.__x > self.__x * other.__y
                else Rotation.CLOCKWISE)

    def normalize(self):
        '''Normalizes a 2D vector in place
        '''
        vector_length = self.length
        if vector_length > sys.float_info.min:
            self.__x /= vector_length
            self.__y /= vector_length
        return self

    def truncate(self, max_length):
        '''Adjusts x and y so that the length of the vector does not exceed max
        Truncates a vector so that its length does not exceed max
        '''
        if self.length > max_length:
            self.normalize()
            self.mul(max_length)
        return self

    def distance(self, other):
        '''Calculates the euclidean distance between two vectors
        '''
        return ((self.__x - other.__x)**2 + (self.__y - other.__y)**2)**0.5

    def distance_sq(self, other):
        '''Squared version of distance.
        Calculates the euclidean distance squared between two vectors
        '''
        return (self.__x - other.__x)**2 + (self.__y - other.__y)**2

    def reflect(self, norm):
        '''Given a normalized vector this method reflects the vector it
        is operating upon. (like the path of a ball bouncing off a wall)
        '''
        return self.add(norm.reverse.mul(2 * self.dot(norm)))

    def __getitem__(self, key):
        if key == 'x' or key == 0:
            return self.__x
        elif key == 'y' or key == 1:
            return self.__y
        else:
            raise KeyError('Invalid key \'{}\' supplied'.format(key))

    def __setitem__(self, key, value):
        if key == 'x' or key == 0:
            self.x = value
        elif key == 'y' or key == 1:
            self.y = value
        else:
            raise KeyError('Invalid key \'{}\' supplied'.format(key))

    def add(self, other):
        self.__x += other.__x
        self.__y += other.__y
        return self

    def sub(self, other):
        self.__x -= other.__x
        self.__y -= other.__y
        return self

    def mul(self, other):
        self.x *= other
        self.y *= other
        return self

    def dot(self, other):
        '''Calculates the dot product
        '''
        return self.__x * other.__x + self.__y * other.__y

    def __lt__(self, other):
        try:
            return self.length_sq < other.length_sq
        except AttributeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.length_sq >= other.length_sq
        except AttributeError:
            return NotImplemented

    def __eq__(self, other):
        try:
            return self.__x == other.__x and self.__y == other.__y
        except AttributeError:
            return NotImplemented

    def __hash__(self):
        k1 = self.__x
        k2 = self.__y
        return 0.5 * (k1 + k2) * (k1 + k2 + 1) + k2

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __contains__(self, value):
        return value == self.__x or value == self.__y

    def __len__(self):
        return 2

    def __repr__(self):
        return '<Vector2D ({}, {})>'.format(self.x, self.y)

def main():
    v1 = Vector2D(12, 123)
    v2 = Vector2D(123, 13)
    print(v1)
    v1.add(v2)
    print(v1)


if __name__ == '__main__':
    main()
