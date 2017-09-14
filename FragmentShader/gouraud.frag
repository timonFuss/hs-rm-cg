// Gouraud fragment shader from 
// Richard S. Wright Jr. 
// OpenGL SuperBible
//# version 330

varying vec4 varyingColor;

void main(void) 
{
	gl_FragColor = varyingColor;
}
