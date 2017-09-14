#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

class Sphere(object):
    def __init__(self, center, radius, color, material):
        self.center = center    #point
        self.radius = radius    #scalar
        self.color = color
        self.material = material

    def __repr__(self):
        return 'Sphere(%s,%s)' %(repr(self.center), repr(self.radius))

    def intersectionParameter(self, ray):
        co = self.center -ray.origin
        v=co.dot(ray.direction)
        discriminant = v*v -co.dot(co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalize()