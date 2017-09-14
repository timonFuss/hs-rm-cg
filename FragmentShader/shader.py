from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.arrays import vbo
from numpy import array, dot, matrix, identity, cross, tan, linalg
from math import cos, sin, acos, sqrt, pi

import OpenGL
OpenGL.ERROR_ON_COPY = True
OpenGL.FORWARD_COMPATIBLE_ONLY = True

# PyOpenGL 3.0.1 introduces this convenience module ...
from OpenGL.GL.shaders import *

import sys, math

myVBO = None
data = []
wireframe = False
startP = 0,0
WIDTH, HEIGHT = 500, 500
angle = 0
axis = [1,0,0]
actOrient = identity(4,float)
doRotation, doScale = False, False
scaleFactor = 1.0
program,  vertexShader,  fragmentShader  = None, None, None
program2, vertexShader2, fragmentShader2 = None, None, None
program3, vertexShader3, fragmentShader3 = None, None, None
gouraud = 0
projectionMatrix = identity(4)


def initGL(width,   height):
	# Set background color to blue
	glClearColor(0.0, 0.0, 1.0, 0.0)
	# Set perspective projection
	projectionMatrix = perspectiveMatrix(45.0, 1., 0.1, 100.0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_NORMALIZE)

	if not glUseProgram:
		print "Missing Shader Objects!"
		sys.exit(1)

	global program
	program = compileProgram(\
				compileShader(vertexShader, GL_VERTEX_SHADER),
				compileShader(fragmentShader, GL_FRAGMENT_SHADER),)
	global program2
	program2 = compileProgram(\
				compileShader(vertexShader2, GL_VERTEX_SHADER),
				compileShader(fragmentShader2, GL_FRAGMENT_SHADER),)
	global program3
	program3 = compileProgram(\
				compileShader(vertexShader3, GL_VERTEX_SHADER),
				compileShader(fragmentShader3, GL_FRAGMENT_SHADER),)


def rotationMatrix(angle, axis):
	c, mc, s = cos(angle), 1-cos(angle), sin(angle)
	x, y, z = array(axis)/sqrt(dot(array(axis),array(axis)))
	r = matrix([[x*x*mc+c, 	 x*y*mc-z*s, x*z*mc+y*s, 0],\
				[x*y*mc+z*s, y*y*mc+c,   y*z*mc-x*s, 0],\
				[x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
				[0 ,0 , 0, 1]])
	return r


def scaleMatrix(sx, sy, sz):
    s = matrix([[sx, 0,  0, 0],\
				[0, sy,  0, 0],\
				[0,  0, sz, 0],
				[0,  0,  0, 1]])
    return s


def translationMatrix(tx, ty, tz):
    t = matrix([[1,  0,  0, tx],\
                [0,  1,  0, ty],\
                [0,  0,  1, tz],
                [0,  0,  0,  1]])
    return t


def lookAtMatrix(ex,ey,ez, cx,cy,cz, ux,uy,uz):
	e = array([ex, ey, ez])  # eye position
	c = array([cx, cy, cz])  # center
	up = array([ux, uy, uz]) # up vector
	# normalize up vector
	lup = sqrt(dot(up, up))
	up = up / lup
	# determine view direction
	f = c - e
	lf = sqrt(dot(f,f))
	f = f / lf
	# determine s
	s = cross(f, up)
	ls = sqrt(dot(s, s))
	s = s / ls
	# determine u
	u = cross(s, f)
	# create lookAt matrix
	l = matrix([[ s[0],  s[1],  s[2], -dot(s,e)],\
				[ u[0],  u[1],  u[2], -dot(u,e)],\
				[-f[0], -f[1], -f[2],  dot(f,e)],\
				[    0,     0,     0,         1]])
	return l


def perspectiveMatrix(fovy, aspect, zNear, zFar):
	f = 1.0 / tan(fovy/2.0) # cotan(fovy/2)
	aspect = float(aspect)
	zNear = float(zNear)
	zFar = float(zFar)
	p = matrix([[f/aspect, 0,                         0,                           0],\
				[       0, f,                         0,                           0],\
				[       0, 0, (zFar+zNear)/(zNear-zFar), (2*zFar*zNear)/(zNear-zFar)],\
				[       0, 0,                        -1,                           0]])
	return p


def sendVec3(shaderProgram, varName, value):
	# determine location of uniform variable varName
	varLocation = glGetUniformLocation(shaderProgram, varName)
	# pass value to shader
	glUniform3f(varLocation, *value)


def sendVec4(shaderProgram, varName, value):
	# determine location of uniform variable varName
	varLocation = glGetUniformLocation(shaderProgram, varName)
	# pass value to shader
	glUniform4f(varLocation, *value)
	#glUniform4f(varLocation, *array(value))


def sendMatrix3(shaderProgram, varName, matrix):
	# determine location of uniform variable varName
	varLocation = glGetUniformLocation(shaderProgram, varName)
	# pass value to shader
	#glUniformMatrix3fv(varLocation, 1, GL_TRUE, matrix.tostring())
	glUniformMatrix3fv(varLocation, 1, GL_TRUE, matrix.tolist())


def sendMatrix4(shaderProgram, varName, matrix):
	# determine location of uniform variable varName
	varLocation = glGetUniformLocation(shaderProgram, varName)
	# pass value to shader
	#glUniformMatrix4fv(varLocation, 1, GL_TRUE, matrix.tostring())
	glUniformMatrix4fv(varLocation, 1, GL_TRUE, matrix.tolist())


def display():
	# Clear framebuffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# modelview matrix
	mvMatrix = lookAtMatrix(0,0,2.5, 0,0,0, 0,1,0)
	mvMatrix *= (rotationMatrix(angle, axis) * actOrient)
	mvMatrix *= scaleMatrix(scale, scale, scale)
	mvMatrix *= translationMatrix(-center[0],-center[1],-center[2])

	# normal matrix
	normalMatrix = linalg.inv(mvMatrix[0:3, 0:3]).T

	# modelview_projection matrix
	mvpMatrix = projectionMatrix * mvMatrix

    # set lighting
	lightPosition = [0, 0, 1]
	diffuseColor = [180/255., 100/255., 60/255., 1]
	ambientColor = [45/255., 25/255., 15/255., 1]
	specularColor = [90/255., 50/255., 30/255., 1]

    # switch between different shaders
	if gouraud == 0:
		glUseProgram(program)
		sendMatrix4(program, "mvMatrix", mvMatrix)
		sendMatrix4(program, "mvpMatrix", mvpMatrix)
		sendMatrix3(program, "normalMatrix", normalMatrix)
		sendVec4(program, "diffuseColor", diffuseColor)
		sendVec4(program, "ambientColor", ambientColor)
		sendVec4(program, "specularColor", specularColor)
		sendVec3(program, "lightPosition", lightPosition)
	elif gouraud == 1:
		glUseProgram(program2)
		sendMatrix4(program2, "mvMatrix", mvMatrix)
		sendMatrix4(program2, "mvpMatrix", mvpMatrix)
		sendMatrix3(program2, "normalMatrix", normalMatrix)
		sendVec4(program2, "diffuseColor", diffuseColor)
		sendVec4(program2, "ambientColor", ambientColor)
		sendVec4(program2, "specularColor", specularColor)
		sendVec3(program2, "lightPosition", lightPosition)
	elif gouraud == 2:
		glUseProgram(program3)
		sendMatrix4(program3, "mvMatrix", mvMatrix)
		sendMatrix4(program3, "mvpMatrix", mvpMatrix)
		sendMatrix3(program3, "normalMatrix", normalMatrix)
		sendVec4(program3, "diffuseColor", diffuseColor)
		sendVec4(program3, "ambientColor", ambientColor)
		sendVec4(program3, "specularColor", specularColor)
		sendVec3(program3, "lightPosition", lightPosition)

    # render object
	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_NORMAL_ARRAY)
	myVBO.bind()
	glVertexPointer(3, GL_FLOAT, 24, myVBO)
	glNormalPointer(GL_FLOAT, 24, myVBO+12)
	glDrawArrays(GL_TRIANGLES, 0, len(data))
	myVBO.unbind()
	glDisableClientState(GL_VERTEX_ARRAY)
	glDisableClientState(GL_NORMAL_ARRAY)

	glutSwapBuffers()


def projectOnSphere(x, y, r):
	x, y = x-WIDTH/2.0, HEIGHT/2.0-y
	a = min(r*r, x**2 + y**2)
	z = sqrt(r*r - a)
	l = sqrt(x**2 + y**2 + z**2)
	return x/l, y/l, z/l


def mousebuttonpressed(button, state, x, y):
	global startP, actOrient, angle, doRotation, doScale
	r = min(WIDTH, HEIGHT)/2.0
	if button == GLUT_LEFT_BUTTON:
		if state == GLUT_DOWN:
			doRotation = True
			startP = projectOnSphere(x, y, r)
		if state == GLUT_UP:
			doRotation = False
			actOrient = rotationMatrix(angle, axis) * actOrient
			angle = 0
	if button == GLUT_RIGHT_BUTTON:
		if state == GLUT_DOWN:
			doScale = True
			startP = y
		if state == GLUT_UP:
			doScale = False


def mousemoved(x, y):
	global angle, axis,scaleFactor
	if doRotation:
		r = min(WIDTH, HEIGHT)/2.0
		moveP = projectOnSphere(x, y, r)
		angle = acos(dot(startP, moveP))
		axis = cross(startP, moveP)
	if doScale:
		d = 0.1*(startP - y)/float(HEIGHT)
		scaleFactor += d
	glutPostRedisplay()


def main():
	# Initialize GLUT
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH| GLUT_RGB)
	glutInitWindowSize(WIDTH, HEIGHT)
	glutCreateWindow("Simple OBJ-Viewer using Shader")
	# Register display callback function
	glutDisplayFunc(display)
	glutKeyboardFunc(keypressed)
	glutMouseFunc(mousebuttonpressed)
	glutMotionFunc(mousemoved)
	glutReshapeFunc(resizeViewport)
	# Initialize OpenGL Context
	initGL(WIDTH, HEIGHT)
	# Start GLUT mainloop
	glutMainLoop()


def keypressed(key, x, y):
	global wireframe, gouraud
	if key == 'q' or key == 'Q':
		sys.exit()
	if key == 'w':
		wireframe ^= True
		if wireframe:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	if key == 's':
		gouraud = (gouraud +1) % 3
		print gouraud
	glutPostRedisplay()


def resizeViewport(width, height):
	global WIDTH, HEIGHT
	# Prevent division by zero
	if height == 0:
		height = 1
	WIDTH, HEIGHT = width, height
	# Reset current viewport
	glViewport(0, 0, width, height)
	global projectionMatrix
	projectionMatrix = perspectiveMatrix(45.0, float(width)/height, 0.1, 100.0)
	glutPostRedisplay()



if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "no obj-file"
		sys.exit()
    # setup shaders
	#vertexShader = open("spotlight.vert","r").read()
	#fragmentShader = open("spotlight.frag","r").read()
	vertexShader3 = open("phong2.vert","r").read()
	fragmentShader3 = open("phong2.frag","r").read()
	vertexShader2 = open("phong.vert","r").read()
	fragmentShader2 = open("phong.frag","r").read()
	vertexShader = open("gouraud.vert","r").read()
	fragmentShader = open("gouraud.frag","r").read()
	#vertexShader = open("gouraud.vert","r").read()
	#fragmentShader = open("gouraud.frag","r").read()
	#vertexShader = open("flat.vert","r").read()
	#fragmentShader = open("flat.frag","r").read()

	# load data
	vertices, normals, faces = [], [], []
	f = file(sys.argv[1])
	for line in f:
		sl = line.split()
		if len(sl)>0:
			if sl[0] == 'v':
				vertices.append(map(float,sl[1:]))
			if sl[0] == 'vn':
				normals.append(map(float,sl[1:]))
			if sl[0] == 'f':
				vv = [v.split("/") for v in sl[1:]]
				faces.append(vv)

	# bounding box
	bb = [map(min,zip(*vertices)), map(max,zip(*vertices))]
	# bounding box center
	center = [(x[1]+x[0])/2.0 for x in zip(*bb)]
	# scale factor
	scale = 2.0/max([(x[1]-x[0]) for x in zip(*bb)])

	# set data
	data = []
	for face in faces:
		for vertex in face:
			vnr = int(vertex[0])-1
			nnr = int(vertex[2])-1
			data.append(vertices[vnr]+normals[nnr])

	myVBO = vbo.VBO(array(data,'f'))

	main()
