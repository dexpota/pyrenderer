from imageutils import Color
from random import random
from mathutils import Hit
import math


class Sphere:
    def __init__(self, center, radius, color=Color(random(), random(), random())):
        self.center = center
        self.radius = radius
        self.c = color

    def color(self):
        return self.c


    def intersect(self, ray):
        hit = None

        po = ray.origin - self.center

        delta = (2*ray.direction.dot(po))**2 - 4*ray.direction.norm2()*(po.norm2() - self.radius**2)

        if delta > 0:
            b = 2 * ray.direction.dot(po)
            t0 = (-b + (delta) ** .5) / (2*ray.direction.norm2())
            t1 = (-b - (delta) ** .5) / (2*ray.direction.norm2())


            if 0 < t0 and (t0 < t1 or t1 < 0):
                hit = Hit(self, ray, t0)
                hit.normal = ray.position(hit.t0) - self.center
                hit.normal.normalize()
            elif 0 < t1 and (t1 < t0 or t1 < 0):
                hit = Hit(self, ray, t1)
                hit.normal = ray.position(hit.t0) - self.center
                hit.normal.normalize()
            else:
                return hit

        return hit


    def reflection(self, point, incoming_direction, outgoing_direction):
        return self.c / math.pi


class Plane:
    def __init__(self, origin, normal, color):
        self.origin = origin
        self.normal = normal
        self.normal.normalize()
        self.c = color

    def color(self):
        return self.c

    def intersect(self, ray):
        hit = None

        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            p0l0 = ray.origin - self.origin
            t = - p0l0.dot(self.normal) / (denom)

            if t > 0:
                hit = Hit(self, ray, t)
                hit.normal = self.normal
        return hit

    def reflection(self, point, incoming_direction, outgoing_direction):
        return self.c / math.pi


class Circle:
    def __init__(self, origin, normal, color):
        self.origin = origin
        self.normal = normal
        self.c = color

    def color(self):
        return self.c

    def intersect(self, ray):
        hit = None

        denom = self.normal.dot(ray.direction)
        if denom > 1e-6:
            p0l0 = self.origin - ray.origin
            t = p0l0.dot(self.normal) / denom

            if t > 0 and (ray.position(t) - self.origin).norm() < .2:
                hit = Hit(self, ray, t)
                hit.normal = self.normal
        return hit

    def reflection(self, point, incoming_direction, outgoing_direction):
        return self.c / math.pi
