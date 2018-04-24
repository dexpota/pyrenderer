from tqdm import tqdm
from mathutils import Point3D, Vector3D, Ray, uniform_over_hemisphere
from random import random
from imageutils import Color
import math


class UniformPointLight:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def emission(self, point, direction):
        return self.color


def background(ray):
    t = 0.5 * (ray.direction.y + 1)
    return (1 - t) * Color(10, 10, 10) + t * Color(5, 6, 10)


def direct_illumination(scene, hit):
    # compute the radiance due to direct illumination

    # direction from the surface is being seen
    outgoing_direction = -hit.ray.direction
    point = hit.ray.position(hit.t0)

    radiance = Color(0, 0, 0)
    for light in scene.lights:
        incoming_direction = (light.position - point)
        incoming_direction.normalize()

        if hit.normal.dot(incoming_direction) < 0:
            continue

        # light radiance from position in direction
        contribution = (light.emission(light.position, incoming_direction)
                        * hit.obj.reflection(point, incoming_direction, outgoing_direction)
                        * hit.normal.dot(incoming_direction))

        shadow_ray = Ray(point + incoming_direction*0.001, incoming_direction)
        distance = (light.position - point).norm()

        another_hit = scene.intersect(shadow_ray)

        if another_hit is not None and another_hit.obj == hit.obj:
            continue

        if another_hit is None:
            radiance += contribution
        elif (another_hit.ray.position(another_hit.t0) - point).norm() >= distance:
            radiance += contribution

    return radiance


def indirect_illumination(scene, hit, depth):
    outgoing_direction = -hit.ray.direction
    point = hit.ray.position(hit.t0)
    radiance = Color(0, 0, 0)

    if depth > 1:
        return radiance

    # number of samples
    n = 128+64
    for i in range(0, n):
        r1 = random()
        sample = uniform_over_hemisphere(r1, random())

        # from local to global coordinates
        normal = hit.normal
        if abs(normal.x) > abs(normal.y):
            tangent = (Vector3D(normal.z, 0, -normal.x)
                       / math.sqrt(normal.dot(normal)))
        else:
            tangent = (Vector3D(0, -normal.z, normal.y)
                       / math.sqrt(normal.dot(normal)))
        nb = normal.cross(tangent)

        incoming_direction = Vector3D(
            sample.x * nb.x + sample.y * normal.x + sample.z * tangent.x,
            sample.x * nb.y + sample.y * normal.y + sample.z * tangent.y,
            sample.x * nb.z + sample.y * normal.z + sample.z * tangent.z)
        incoming_direction.normalize()

        new_ray = Ray(point + incoming_direction * 0.001, incoming_direction)

        incoming_radiance = trace(scene, new_ray, depth + 1)
        v = (incoming_radiance
             * hit.obj.reflection(point, incoming_direction, outgoing_direction)
             * hit.normal.dot(incoming_direction))
        radiance = radiance + v

    radiance = radiance / float(n) * (2 * math.pi)
    return radiance


def trace(scene, ray, depth=0):
    hit = scene.intersect(ray)

    if hit is not None:
        # compute the radiance
        return direct_illumination(scene, hit) + indirect_illumination(scene, hit, depth)
    else:
        return background(ray)


def render(scene, eye, image):
    # iterate over pixels
    for pixel in tqdm(image):
        # center point on each pixel i, j
        # mirror y coordinate because the image origin is on top
        im_point = Point3D(float(pixel.j)/image.w - 0.5,
                           -(float(pixel.i)/image.h - 0.5), -1)

        # change randomly the sample position inside the pixel, antialiasing
        aa_samples = 1
        radiances = []
        for _ in range(aa_samples):
            # ray = Ray(eye, im_point + Vector3D((random() - .5) / image.w, (random() - .5) / image.h, 0) - eye)
            ray = Ray(eye, im_point - eye)
            radiances.append(trace(scene, ray))

        # mean radiance between all samples
        radiance = sum(radiances, Color(0, 0, 0))/aa_samples

        pixel.r = radiance.r
        pixel.g = radiance.g
        pixel.b = radiance.b


def trace_ray(i, j, eye, scene):
    im_point = Point3D(float(j) / 200 - 0.5, -(float(i) / 200 - 0.5), -1)

    # change randomly the sample position inside the pixel, antialiasing
    aa_samples = 16
    radiances = []
    for _ in range(aa_samples):
        ray = Ray(eye,
                  im_point + Vector3D((random() - .5) / 200,
                                      (random() - .5) / 200,
                                      0) - eye)
        radiances.append(trace(scene, ray))

    # mean radiance between all samples
    radiance = (sum(radiances, Color(0, 0, 0))
                / aa_samples)
