#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from Canvas import *
import sys
import random
import numpy as np
from math import sin,cos,tan, sqrt, pi

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas


ANGLE = 30

#Camera
ASPECTRATIO=WIDTH/HEIGHT
N=1.0
F=10.0

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    global vectorlist

    # 2.0)Sichtkugelverfahren
    cotan = 1.0 / tan((pi * 30.0) / 180.0)

    vectorlist = [[(x * cotan / ASPECTRATIO) / -z, (y * cotan) / -z, (z * (-(F + N) / F - N) + (-2.0 * F * N / F - N)) / -z] for
              x, y, z in setCamera(moved_vectorlist)]


    # 1.3)projektion auf xy-Ebene(Grundriss) -> z=0
    vectorlist2D = [ele[:2] for ele in vectorlist]

    # 1.4)
    # Transformieren: Bild-Bereich nach ViewPort-Bereich
    # y wird an der x achse gespielt und dann wieder ins positive verschoben
    # geht nur weil Bounding Box normiert ist bevor auf das Fenster skaliert wird
    vectorlist = [[(x + 1) * WIDTH / 2.0, (-y + 1) * HEIGHT / 2.0] for x, y in vectorlist2D]


    for x,y in vectorlist:
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                               fill=COLOR, outline=COLOR)
        pointList.insert(0, p)

def setCamera(vectorlist):
    #Punkt (1,1,1) = max  und entspricht der länge wurzel(3) vom Zentrum aus gesehen
    d = 1.0 * sqrt(3)
    return [(x, y, z - d) for x, y, z in vectorlist]

def rotYp():
    """ rotate counterclockwise around y axis """
    can.delete(*pointList)
    rotate(ANGLE)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    can.delete(*pointList)
    rotate(-ANGLE)
    draw()

def rotate(a):
    global moved_vectorlist
    moved_vectorlist = [[x * cos(a) + z * -sin(a), y, x * sin(a) + z * cos(a)] for x, y, z in moved_vectorlist]

def move_and_scale(center,scale,vectorlist):
    #x,y,z Koordinate eines Punktes um den Mittelpunkt der Bounding box
    # verschieben, damit die Verschiebung in den "Ursprung" simuliert wird
    # anschließend skalieren
    return [((x - center[0]) * scale, (y - center[1]) * scale, (z - center[2]) * scale) for x, y, z in vectorlist]


if __name__ == "__main__":

    global moved_vectorlist
    #check parameters
    if len(sys.argv) == 1:
       print("pointViewerTemplate.py")
       sys.exit(-1)

    # Elementliste
    vectorlist = []

    for line in open("cow_points.raw"):
       vectorlist.append([float(x) for x in line.split()])

    #1,1)
    #bounding Box
    b_box = [map(min, zip(*vectorlist)), map(max, zip(*vectorlist))]

    #Center of BoundingBox
    center = map(lambda x: (x[1]-x[0])/2 + x[0], zip(b_box[0], b_box[1]))

    #1,2)
    #Scaling into a normalized ... ("box" ?)
    scale = 2.0/max([(p[1] - p[0]) for p in zip(*b_box)])

    #Translation to (0,0,0)
    moved_vectorlist = move_and_scale(center,scale,vectorlist)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
    
