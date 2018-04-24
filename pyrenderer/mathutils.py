from __future__ import division
import math


class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(self.y*other.z - self.z*other.y,
                        self.z*other.x - self.x*other.z,
                        self.x*other.y - self.y-other.x)

    def normalize(self):
        norm = self.norm()
        self.x /= norm
        self.y /= norm
        self.z /= norm

    def norm(self):
        return (self.x**2 + self.y**2 + self.z**2)**.5

    def norm2(self):
        return self.x**2 + self.y**2 + self.z**2

    def __div__(self, num):
        return Vector3D(self.x/num, self.y/num, self.z/num)

    def __truediv__(self, num):
        return Vector3D(self.x/num, self.y/num, self.z/num)

    def __mul__(self, num):
        return Vector3D(self.x*num, self.y*num, self.z*num)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __str__(self):
        return "(%f, %f ,%f)" % (self.x, self.y, self.z)


class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, vector):
        return Point3D(self.x + vector.x, self.y + vector.y, self.z + vector.z)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
        self.direction.normalize()

    def position(self, t):
        return self.origin + self.direction*t


class Hit:
    def __init__(self, obj, ray, t0):
        self.obj = obj
        self.ray = ray
        self.t0 = t0
        self.normal = None


def uniform_over_hemisphere(r1, r2):
    sinTheta = math.sqrt(1 - r1*r1)
    phi = 2*math.pi*r2
    x = sinTheta * math.cos(phi)
    z = sinTheta * math.sin(phi)
    return Vector3D(x, r1, z)
