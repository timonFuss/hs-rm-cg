#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from Vector import Vector
from Camera import Camera
from Sphere import Sphere
from Plane import Plane
from Triangle import Triangle
from Light import Light
from Material import Material
from Ray import Ray
from CheckerboardMaterial import CheckerboardMaterial

# Bildgroesse
WIDTH = 400
HEIGHT = 400

# Kamera
e = Vector(0, 1.8, 10)
c = Vector(0, 3, 0)
up = Vector(0, 1, 0)
fov = 45.0
RATIO = 0.0
SHINY = 50.0

#Material
M1=Material(0.6,0.9,0.9)
M2=Material(0.2,1.3,0.25)
M3=Material(0.3,0.4,0.125)


# Farben
BACKGROUND_COLOR = (0, 0, 0)
COLOR_BLUE=(0,255,255)
COLOR_GREEN=(18,183,0)
COLOR_RED=(255,0,0)
COLOR_YELLOW=(255,255,0)
COLOR_WHITE=(255,255,255)

CB = CheckerboardMaterial(BACKGROUND_COLOR,COLOR_WHITE)

# Geometrie
object_list = []

object_list.append(Sphere(Vector(0, 4.5, 0), 1,COLOR_BLUE,M1))
object_list.append(Sphere(Vector(-1.25, 2.5, 0), 1,COLOR_GREEN,M1))
object_list.append(Sphere(Vector(1.25, 2.5, 0), 1,COLOR_RED,M1))
object_list.append(Plane(Vector(0, 0, 0), Vector(0, 1, 0),(255,255,255),CB))
object_list.append(Triangle(Vector(0,4.5,0),Vector(-1.25,2.5,0),Vector(1.25,2.5,0),COLOR_YELLOW,M1))

light_list = []

light_list.append(Light(Vector(30,30,10), COLOR_WHITE,SHINY))

def colorAt(ray,object,maxdist):

    s = ray.pointAtParameter(maxdist)                   #Schnittpunkt Ray/Object

    if isinstance(object.material, CheckerboardMaterial):
        obj_color = object.material.baseColorAt(s)
    else:
        obj_color = object.color

    #ambienter Anteil
    ca_ka = tuple([x * object.material.ka for x in obj_color])      # ca * ka

    #diffuser Anteil
    l = (light_list[0].position - s).normalize()                    #laenge
    normal=object.normalAt(s)                                       #normale
    cd = map(lambda x: x * object.material.kd * l.dot(normal),light_list[0].color)


    #spekularer Anteil
    lr=(l-(2*normal.dot(l)*normal)).normalize()
    diffdot = lr.dot(normal)
    cs = Vector(0,0,0)

    if diffdot < 0:
        cs = map(lambda x: x * object.material.ks * (lr.dot(ray.direction.normalize()*(-1))**light_list[0].shiny),light_list[0].color)
    c_out = tuple([int(sum(x)) for x in zip(ca_ka,cd,cs)])


    #Schattierung
    light_ray = Ray(s,l)       #Strahl von der Lichtquelle aus
    distance = (light_list[0].position - s).norm()  #Abstand zwischen akt Object und Lichtquelle

    for object in object_list:
        hitdist = object.intersectionParameter(light_ray)

        if hitdist and  (10**(-5)) < hitdist and hitdist < distance :
            return tuple(map(lambda x: int(x/3), c_out))



    return c_out

if __name__ == "__main__":
    cam = Camera(c, e, up, fov, HEIGHT, WIDTH)

    img = Image.new('RGB', (WIDTH, HEIGHT))
    pixels = img.load()

    img.save("test", "png")

    for x in range(img.size[0]):
        for y in range(img.size[1]):

            ray = cam.calcRay(x, y)
            maxdist = float('inf')
            color = BACKGROUND_COLOR

            for object in object_list:
                hitdist = object.intersectionParameter(ray)

                if hitdist and hitdist > 0:

                    if hitdist < maxdist:
                        maxdist = hitdist
                        color = colorAt(ray,object,maxdist)
                        #color = (0, 255, 255)
            pixels[x, y] = color

    img.save("test.png")
    img.show()
