#!/usr/bin/python
# -*- coding: utf-8 -*-

class Triangle(object):

    def __init__(self, a, b, c, color, material):
        self.a = a  #point
        self.b = b  #point
        self.c = c  #point
        self.u = self.b - self.a    #direction vector
        self.v = self.c - self.a    #direction vector
        self.color = color
        self.material = material

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross_product(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross_product(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s<=1:
            return wu.dot(self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross_product(self.v).normalize()
