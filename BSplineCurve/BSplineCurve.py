from Tkinter import *
from Canvas import *
import sys
import numpy as np

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 1  # half of point size (must be integer)
CCOLOR = "#0000FF"  # blue (color of control-points and polygon)

BCOLOR = "#000000"  # black (color of bezier curve)
BWIDTH = 1  # width of bezier curve

pointList = []  # list of (control-)points
bezierList = []  # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))

#k = 4  # Ordnung
acc = 4  # Max points


def drawPoints(points, color):
    for p in points:
        element = can.create_oval(p[0] - HPSIZE, p[1] - HPSIZE,
                                  p[0] + HPSIZE, p[1] + HPSIZE,
                                  fill=color, outline=color)
        elementList.append(element)


def drawPolygon(points, color):
    if len(points) > 1:
        for i in range(len(points) - 1):
            element = can.create_line(points[i][0], points[i][1],
                                      points[i + 1][0], points[i + 1][1],
                                      fill=color)
            elementList.append(element)

#calculates the first index of the intevall
def find_r(knotvector, t):
    temp_v_idx = 0
    for idx in range(0, len(knotvector) - 1):
        if knotvector[idx] <= t:
            temp_v_idx = idx
    return temp_v_idx


def deboor(k, points, knotvector, t, j):
    r = find_r(knotvector, t)
    i = r - k + (1 + j)
    if len(points) == 1:
        return points[0]
    newPoints = []

    if j == 1:

        #different actions for the first iteration
        while i <= r:
            alpha = ((t - knotvector[i]) * 1.0) / ((knotvector[i - j + k]) - knotvector[i]) * 1.0

            #different index for the first iteration
            x = points[i - 1][0]
            y = points[i - 1][1]

            next_x = points[i][0]
            next_y = points[i][1]


            bx = (1 - alpha) * x + alpha * next_x
            by = (1 - alpha) * y + alpha * next_y
            b = [bx, by]

            newPoints.append(b)
            i += 1
    else:
        #
        for idx in range(0, len(points) - 1):
            alpha = ((t - knotvector[i]) * 1.0) / ((knotvector[i - j + k]) - knotvector[i]) * 1.0

            x = points[idx][0]
            y = points[idx][1]

            next_x = points[idx + 1][0]
            next_y = points[idx + 1][1]

            bx = (1 - alpha) * x + alpha * next_x
            by = (1 - alpha) * y + alpha * next_y
            b = [bx, by]

            newPoints.append(b)
            i += 1

    return deboor(k, newPoints, knotvector, t, j + 1)


def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def create_knot_vector(k):
    #k times the first number
    a = [0 for _ in range(k)]
    #fills the space between with numbers
    b = [x for x in range(1,len(pointList)-1-(k-1)+1)]
    #k times the last number
    c = [len(pointList)-1-(k-2) for _ in range(k)]

    return a + b + c


def draw():
    global deboorpoints
    """ draw elements """
    can.delete(*elementList)
    drawPoints(pointList, CCOLOR)
    bezierList = []
    #drawDeBoorPoints()
    drawPolygon(pointList, CCOLOR)

    n = len(pointList)
    if n >= k:

        knot_vector=create_knot_vector(k)

        j = 1
        for t in range(0, max(knot_vector) * acc):
            point = deboor(k, pointList, knot_vector, t / float(acc), j)
            bezierList.append(point)

        bezierList.append(pointList[-1])
        #drawPoints(bezierList, BCOLOR)

    drawPolygon(bezierList, BCOLOR)


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]
    del bezierList[:]


def mouseEvent(event):
    """ process mouse events """
    global pointList
    print "left mouse button clicked at ", event.x, event.y
    pointList.append([event.x, event.y])
    draw()


def grad_update(new):
    global k
    k = int(new)
    draw()


def max_update(new):
    global acc
    acc = int(new)
    draw()


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
    bExit = Button(cFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    eFr = Frame(mw)
    eFr.pack(side="right")
    k_slider_label = Label(eFr, text="degree")
    k_slider = Scale(eFr, from_=2, to=20, orient=HORIZONTAL, command=grad_update)
    k_slider_label.pack(side="left")
    k_slider.pack(side="left")

    max_slider_label = Label(eFr, text="curve point")
    max_slider = Scale(eFr, from_=4, to=100, orient=HORIZONTAL, command=max_update)
    max_slider_label.pack(side="right")
    max_slider.pack(side="right")

    # start
    mw.mainloop()