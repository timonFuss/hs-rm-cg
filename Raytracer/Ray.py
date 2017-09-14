#!/usr/bin/python
# -*- coding: utf-8 -*-

class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin    #point
        self.direction = direction.normalize()     #vektor

    def __repr__(self):
        return 'Ray(%s,%s)' %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)