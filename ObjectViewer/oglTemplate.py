from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import array, cross, dot, matrix
from math import sin, cos, acos, sqrt
import sys, os

EXIT = -1
FIRST = 0

# lists
vertices = []  # v
faces = []  # f
normals = []  # vn

draw_vertices = []  # vertices that interpreted from faces

# bounding box
scale = 0
center = []

myVBO = None

WIDTH = 500
HEIGHT = 500

doZoom = False
doRotation = False
doMove = False

# rotation
angle = 0
axis = (1, 0, 0)
actOri = 1

# translation
trans_vector = [0, 0, 0]

# light
light = (10.0, 10.0, 0.0)

p = [1.0, 0.0, 0.0, 0.0,
     0.0, 1.0, 0.0, -1 / light[1],
     0.0, 0.0, 1.0, 0.0,
     0.0, 0.0, 0.0, 0.0]

# shadow
shadow = False

# switch ortho-central projection
ortho = True

# color
WHITE = (1., 1., 1., 0.)  # W
BLACK = (0., 0., 0., 0.)  # S
RED = (1., 0., 0., 0.)  # R
BLUE = (0., 0., 1., 0.)  # B
YELLOW = (1., 1., 0., 0.)  # G
GREEN = (0., 1., 0., 0.)


background = WHITE
obj_color = RED


def init(width, height):
    """ Initialize an OpenGL window """
    global background

    glClearColor(*background)  # background color
    glColor(*obj_color)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)  # switch to projection matrix
    glLoadIdentity()  # set to 1
    glOrtho(-1.5, 1.5, -1.5, 1.5, -10.0, 10.0)  # multiply with new p-matrix
    glMatrixMode(GL_MODELVIEW)  # switch to modelview matrix

    # Beleuchtung aus Folie 195
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)  # Materialfarbe der Tiere zulassen
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glShadeModel(GL_SMOOTH)


def display():
    """ Render all objects"""
    global vertices, myVBO, scale, center, trans_vector, shadow, obj_color, b_box

    glLoadIdentity()
    glClearColor(*background)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear screen

    # set drawstyle
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # switch projection
    calc_projection()

    glScale(scale, scale, scale)
    glTranslate(-center[0], -center[1], -center[2])

    # mouse rotation
    glMultMatrixf((actOri * rotate(angle, axis)).tolist())

    glTranslatef(*trans_vector)

    # Render Vertex Buffer Object
    myVBO.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, myVBO)
    glNormalPointer(GL_FLOAT, 24, myVBO + 12)

    glLight(GL_LIGHT0, GL_POSITION, light)

    if shadow:
        draw_shadow()

    glClearColor(*background)  # background color
    glColor4f(*obj_color)  # render stuff

    glDrawArrays(GL_TRIANGLES, 0, len(draw_vertices))

    myVBO.unbind()

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

    glutSwapBuffers()  # swap buffer


def calc_projection():
    '''Sets the orthogonal/central projection.'''

    global WIDTH, HEIGHT
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        if WIDTH <= HEIGHT:
            glOrtho(-1.5, 1.5,
                    -1.5 * HEIGHT / WIDTH, 1.5 * HEIGHT / WIDTH,
                    -1000.0, 1000.0)
        else:
            glOrtho(-1.5 * WIDTH / HEIGHT, 1.5 * WIDTH / HEIGHT,
                    -1.5, 1.5,
                    -1000.0, 1000.0)
    else:
        fieldofView = 60
        aspect = float(WIDTH) / float(HEIGHT)
        gluPerspective(fieldofView, aspect, 0.1, 100.0)
        gluLookAt(0, 0, 3, 0, 0, 0, 0, 1.0, 0)

    glMatrixMode(GL_MODELVIEW)


def draw_shadow():
    '''Draws the shadow of the object.'''

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    #Shadow Color
    glColor4fv(BLACK)

    glTranslatef(light[0], light[1], light[2])
    glTranslatef(0, b_box[0][1], 0)

    glMultMatrixf(p)

    glTranslatef(0, -b_box[0][1], 0)
    glTranslatef(-light[0], -light[1], -light[2])

    glDrawArrays(GL_TRIANGLES, 0, len(draw_vertices))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glPopMatrix()


def reshape(width, height):
    """ adjust projection matrix to window size"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-1.5, 1.5,
                -1.5 * height / width, 1.5 * height / width,
                -1.0, 1.0)
    else:
        glOrtho(-1.5 * width / height, 1.5 * width / height,
                -1.5, 1.5,
                -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
    """ handle keypress events """
    global shadow, ortho, background, obj_color
    if key == chr(27):  # chr(27) = ESCAPE
        sys.exit()

    if key == 's':
        obj_color = BLACK
    if key == 'S':
        background = BLACK
    if key == 'w':
        obj_color = WHITE
    if key == 'W':
        background = WHITE
        glClearColor(*background)
    if key == 'r':
        obj_color = RED
    if key == 'R':
        background = RED
        glClearColor(*background)
    if key == 'b':
        obj_color = BLUE
    if key == 'B':
        background = BLUE
        glClearColor(*background)
    if key == 'g':
        obj_color = YELLOW
    if key == 'G':
        background = YELLOW
        glClearColor(*background)
    if key == 'o':
        ortho = True
    if key == 'p':
        ortho = False
    if key == 'h':
        shadow = True
    if key == 'H':
        shadow = False

    glutPostRedisplay()


def rotate(angle, axis):
    c, mc = cos(angle), 1 - cos(angle)
    s = sin(angle)
    l = sqrt(dot(array(axis), array(axis)))
    if l == 0:
        l = 0.01

    x, y, z = array(axis) / l
    r = matrix([[x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
                [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
                [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
                [0, 0, 0, 1]])
    # OpenGL uses column major order #  > transpose matrix
    return r.transpose()


def projectOnSphere(x, y, r):
    x, y = x - WIDTH / 2.0, HEIGHT / 2.0 - y
    a = min(r * r, x ** 2 + y ** 2)
    z = sqrt(r * r - a)
    l = sqrt(x ** 2 + y ** 2 + z ** 2)
    return x / l, y / l, z / l


def mouse(button, state, x, y):
    """ handle mouse events """
    global startP, actOri, angle
    global doRotation, doZoom, doMove
    r = min(WIDTH, HEIGHT) / 2.0

    # left mouse button
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            startP = projectOnSphere(x, y, r)
        if state == GLUT_UP:
            doRotation = False
            actOri = actOri * rotate(angle, axis)
            angle = 0

    # middle mouse button
    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            startP = y
            doZoom = True
        if state == GLUT_UP:
            doZoom = False

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            startP = (x, y)
            doMove = True
        if state == GLUT_UP:
            doMove = False


def mouseMotion(x, y):
    """ handle mouse motion """
    global angle, axis, factor, startP, b_box, scale, trans_vector
    global doRotation, doZoom, doMove

    if doRotation:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        angle = acos(dot(startP, moveP))
        axis = cross(startP, moveP)
        glutPostRedisplay()

    if doZoom:
        size = 0.05
        longestEdge = max([(p[1] - p[0]) for p in zip(*b_box)])

        # ZoomOut
        # second condition: avoids to swap coords to negative
        if startP < y and scale > (size / longestEdge):
            scale -= size / longestEdge

        # ZoomIn
        if startP > y:
            scale += size / longestEdge

        startP = y
        glutPostRedisplay()

    if doMove:
        diff_x = float(x - startP[0])
        diff_y = float(y - startP[1])
        trans_vector = [trans_vector[0] + diff_x/200., trans_vector[1] - diff_y/200., 0.]
        startP = (x, y)
        glutPostRedisplay()


def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
        sys.exit()
    glutPostRedisplay()


def calc_bbox():
    '''Calculating the Bounding Box.'''
    global scale, center, b_box
    b_box = [map(min, zip(*vertices)), map(max, zip(*vertices))]
    center = [(ele[0] + ele[1]) / 2.0 for ele in zip(*b_box)]
    scale = 2.0 / max([ele[1] - ele[0] for ele in zip(*b_box)])


def calc_normal(face):
    global vertices

    # Vektoren der Ebene aufspannen ...
    v1 = array(vertices[face[1]-1]) - array(vertices[face[0]-1])
    v2 = array(vertices[face[2]-1]) - array(vertices[face[0]-1])

    n1 = cross(v1, v2)

    v1 = array(vertices[face[2]-1]) - array(vertices[face[1]-1])
    v2 = array(vertices[face[0]-1]) - array(vertices[face[1]-1])

    n2 = cross(v1, v2)

    v1 = array(vertices[face[0]-1]) - array(vertices[face[2]-1])
    v2 = array(vertices[face[1]-1]) - array(vertices[face[2]-1])

    n3 = cross(v1, v2)

    return [vertices[face[0]-1], n1, vertices[face[1]-1],  n2, vertices[face[2]-1],  n3]


def readFile():
    '''Reads the vertices, faces and normals from the file and saves each in a list.'''

    global vertices, normals, faces, myVBO, draw_vertices

    if len(sys.argv) == 1:
        print "Paramater missing."
        sys.exit()

    with open(sys.argv[1]) as f:
        for line in f:
            line.rstrip()

            if line.startswith('vn'):
                normals.append([float(ele) for ele in line.split()[1:]])

            if line.startswith('v '):
                vertices.append([float(ele) for ele in line.split()[1:]])

            if line.startswith('f'):
                if '/' in line:
                    tmp = [ele.split('/') for ele in line.split()[1:]]

                    if tmp[0][1] == '':
                        faces.append([[int(ele[0]), int(ele[2])] for ele in tmp])
                    else:
                        faces.append([[int(ele[0]), int(ele[1]), int(ele[2])] for ele in tmp])
                else:
                    faces.append([int(ele) for ele in line.split()[1:]])

                    # if line.startswith('vt'):
        calc_bbox()

        # interpret faces
        for f in faces:
            if type(f[0]) == list:
                for v in f:
                    draw_vertices.append(vertices[v[0] - 1])
                    draw_vertices.append(normals[v[1] - 1])
            else:
                for n in calc_normal(f):
                    draw_vertices.append(n)

        myVBO = vbo.VBO(array(draw_vertices, 'f'))

        print draw_vertices[:3]


def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    #Fenstergroesse
    glutInitWindowSize(500, 500)
    glutCreateWindow("simple openGL/GLUT template")

    glutDisplayFunc(display)  # register display function
    glutReshapeFunc(reshape)  # register reshape function
    glutKeyboardFunc(keyPressed)  # register keyboard function
    glutMouseFunc(mouse)  # register mouse function
    glutMotionFunc(mouseMotion)  # register motion function
    glutCreateMenu(menu_func)  # register menue function

    glutAddMenuEntry("First Entry", FIRST)  # Add a menu entry
    glutAddMenuEntry("EXIT", EXIT)  # Add another menu entry
    # glutAttachMenu(GLUT_RIGHT_BUTTON)  # Attach mouse button to menue

    readFile()

    init(500, 500)  # initialize OpenGL state

    glutMainLoop()  # start even processing


if __name__ == "__main__":
    main()
