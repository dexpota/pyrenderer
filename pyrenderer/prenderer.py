from __future__ import division
from random import random, seed
import math
from mathutils import Vector3D, Point3D, Ray, Hit
from imageutils import Color, Image
from geometry import Sphere, Circle, Plane
from raytracer import render, UniformPointLight, trace_ray

class Path:
    def __init__(self, primary_hit, last_hit):
        self.primary_hit = primary_hit
        self.last_hit = last_hit
        self.depth = 0


# def indirectIllumination(path, point, incoming_direction):
#     estimatedRadiance = 0
#     nsamples = 100
#     if path.depth < 3:
#         for i in range(0, nsamples):
#             r1 = random()
#             sample = uniformSampleHemisphere(r1, random())
#
#             last_hit = path.last_hit
#             N = last_hit.normal
#             if abs(N.x) > abs(N.y):
#                 Nt = Vector3D(N.z, 0, -N.x)/math.sqrt(N.dot(N))
#             else:
#                 Nt = Vector3D(0, -N.z, N.y)/math.sqrt(N.dot(N))
#             Nb = N.cross(Nt)
#
#             sampleWorld = Vector3D(
#                 sample.x * Nb.x + sample.y * N.x + sample.z * Nt.x,
#                 sample.x * Nb.y + sample.y * N.y + sample.z * Nt.y,
#                 sample.x * Nb.z + sample.y * N.z + sample.z * Nt.z)
#
#             new_ray = Ray(last_hit.ray.position(last_hit.t0)+sampleWorld*0.01, sampleWorld)
#             new_hit = scene.intersect(new_ray)
#
#             if new_hit is None:
#                 estimatedRadiance += background() * r1
#             else:
#                 new_path = Path(path.primary_hit, new_hit)
#                 new_path.depth = path.depth + 1
#
#                 estimatedRadiance += estimateRadiance(new_path, new_hit.ray.position(new_hit.t0), new_hit.ray) * r1
#
#         estimatedRadiance /= float(nsamples) * (1.0/(2*math.pi))
#     return estimatedRadiance
#



class Scene:
    def __init__(self):
        self.objects = [#Plane(Point3D(0, 0, -2), Vector3D(0, 0, 1), color=Color(1, 0, 0)),
                        #Plane(Point3D(-.7, 0, -1), Vector3D(1, 0, 0), color=Color(1, 0, 0)),
                        #Plane(Point3D(+.7, 0, -1), Vector3D(-1, 0, 0), color=Color(0, 1, 0)),
                        Plane(Point3D(0, -.5, 0), Vector3D(0, 1, 0), color=Color(1, 1, 1)),
                        #Plane(Point3D(0, +.7, 0), Vector3D(0, -1, 0), color=Color(1, 1, 1)),
                        Sphere(Point3D(0, 0, -1.0), 0.1, color=Color(1.0, 0, 0))]
        self.lights = [UniformPointLight(Point3D(-.5, 0, -1), Color(100, 100, 100))]

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

