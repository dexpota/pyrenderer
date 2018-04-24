from __future__ import division
from random import seed
from mathutils import Vector3D, Point3D
from imageutils import Color, Image
from geometry import Sphere, Plane
from raytracer import render, UniformPointLight, trace_ray


class Path:
    def __init__(self, primary_hit, last_hit):
        self.primary_hit = primary_hit
        self.last_hit = last_hit
        self.depth = 0


class Scene:
    def __init__(self):
        self.objects = [Plane(Point3D(0, -.5, 0),
                              Vector3D(0, 1, 0),
                              color=Color(1, 1, 1)),
                        Sphere(Point3D(0, 0, -1.0), 0.1,
                               color=Color(1.0, 0, 0))]

        self.lights = [UniformPointLight(Point3D(-.5, 0, -1),
                                         Color(100, 100, 100))]

    def intersect(self, ray):
        hits = [s.intersect(ray) for s in self.objects]
        hits = list(filter(None, hits))

        if hits:
            hits = sorted(hits, key=lambda h: h.t0)
            return hits[0]
        return None


if __name__ == "__main__":
    scene = Scene()
    seed(10)
    camera_position = Point3D(0, 0, 0)
    image = Image()
    render(scene, camera_position, image)
    image.write("out.ppm")

    trace_ray(129, 188, camera_position, scene)
