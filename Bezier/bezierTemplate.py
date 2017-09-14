from Tkinter import *
from Canvas import *
import sys

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 2  # half of point size (must be integer)
CCOLOR = "#0000FF"  # blue (color of control-points and polygon)

BCOLOR = "#000000"  # black (color of bezier curve)
BWIDTH = 2  # width of bezier curve

pointList = []  # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))
bezierPoints = []

A = 0.
B = 1.
N = 20
DEGREE = 10


def drawPoints(points, color):
    """ draw (control-)points """
    for p in points:
        element = can.create_oval(p[0] - HPSIZE, p[1] - HPSIZE,
                                  p[0] + HPSIZE, p[1] + HPSIZE,
                                  fill=color, outline=color)
        elementList.append(element)


def drawPolygon(points, color):
    """ draw (control-)polygon conecting (control-)points """
    if len(points) > 1:
        for i in range(len(points) - 1):
            element = can.create_line(points[i][0], points[i][1],
                                      points[i + 1][0], points[i + 1][1],
                                      fill=color)
            elementList.append(element)


# drawBezierCurve(r=0,point_controls=pointList,i=0,n=len(pointList))
def drawBezierCurve(t, control_points):
    """ draw bezier curve defined by (control-)points """
    global fragmentation, pointList

    n = len(pointList)

    if len(control_points) == 1:
        return control_points[0]

    else:
        cp_new = []
        for (p, q) in zip(control_points, control_points[1:]):
            x = ((B - t) / (B - A)) * p[0] + ((t - A) / (B - A)) * q[0]
            y = ((B - t) / (B - A)) * p[1] + ((t - A) / (B - A)) * q[1]
            cp_new.append([x, y])

        return drawBezierCurve(t, cp_new)


def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    global pointList

    can.delete(*elementList)
    drawPoints(pointList, CCOLOR)
    drawPolygon(pointList, CCOLOR)

    if len(bezierPoints) > 2:
        calc_fragmentation()
        drawPolygon(bezierPoints, BCOLOR)


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    global pointList

    print "left mouse button clicked at ", event.x, event.y
    pointList.append([event.x, event.y])
    if len(pointList) > 1:
        calc_fragmentation()
    draw()


def calc_fragmentation():
    """"""
    global N

    for i in range(0, N+1):
        # ti = A + i * (B - A) / len(pointList)
        t = A + float(i) / float(N)
        bezierPoints.append(drawBezierCurve(t, pointList))
    bezierPoints.append(pointList[-1])



if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print "pointViewerTemplate.py"
        sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>", mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()
