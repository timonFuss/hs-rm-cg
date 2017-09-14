#!/usr/bin/python
# -*- coding: utf-8 -*-

from Vector import Vector

class CheckerboardMaterial(object):
    def __init__(self, baseColor,otherColor):
        self.baseColor = baseColor
        self.otherColor = otherColor
        self.ka = 1.0
        self.kd = 0.6
        self.ks = 0.2
        self.checkSize = 1

    def baseColorAt(self, p):
        v = p.scale(1.0 / self.checkSize)
        if(int(abs(v[0]) +0.5) + int(abs(v[1]) + 0.5) + int(abs(v[2]) + 0.5)) %2:
            return self.otherColor
        return self.baseColor