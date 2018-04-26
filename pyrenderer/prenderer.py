from __future__ import division
from random import seed
from mathutils import Point3D
from imageutils import Image
from raytracer import render, trace_ray
from scenegraph import Scene


class Path:
    def __init__(self, primary_hit, last_hit):
        self.primary_hit = primary_hit
        self.last_hit = last_hit
        self.depth = 0


if __name__ == "__main__":
    scene = Scene()
    seed(10)
    camera_position = Point3D(0, 0, 0)
    image = Image()
    render(scene, camera_position, image)
    image.write("out.ppm")

    trace_ray(129, 188, camera_position, scene)
