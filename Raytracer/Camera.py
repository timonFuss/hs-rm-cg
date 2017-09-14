#!/usr/bin/python
# -*- coding: utf-8 -*-

from Ray import Ray
import math

class Camera(object):
    def __init__(self,c,e,up,fov,pixel_height,pixel_width):
        self.c=c
        self.e=e
        self.up=up
        self.fov=fov
        self.image_height=pixel_height  #tatsächliche Pixelhöhe
        self.image_width=pixel_width    #tatsächliche Pixelbreite

        self.f = (self.c - self.e) / (self.c - self.e).norm()
        self.s = self.f.cross_product(self.up)/self.f.cross_product(self.up).norm()
        self.u = self.s.cross_product(self.f)*(-1.0)

        self.alpha=(self.fov / 180 * math.pi)/2.0
        self.height=2.0*math.tan(self.alpha)
        self.width=(self.image_width/self.image_height)*self.height

        self.pixel_width= self.width/(self.image_width-1.0)
        self.pixel_height= self.height/(self.image_height-1.0)

    def calcRay(self,x,y):
        xcomp=self.s.scale(x*self.pixel_width - self.width/2.0)
        ycomp=self.u.scale(y*self.pixel_width - self.height/2.0)

        return Ray(self.e, self.f + xcomp + ycomp)    #evtl. mehrere Strahlen pro Pixel