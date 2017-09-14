// Phong vertex shader from 
// Richard S. Wright Jr. 
// OpenGL SuperBible
//#version 330

// Incomming per vertex ... position and normal
//in vec4 vVertex; 
//in vec3 vNormal;

//vec4 vVertex; 
//	vec3 vNormal;


uniform mat4 mvpMatrix; 
uniform mat4 mvMatrix; 
uniform mat3 normalMatrix; 
uniform vec3 lightPosition; 

// Color to fragment programm
// smooth out vec3 vVaryingNormal;
// smooth out vec3 vVaryingLightDir; 
varying vec3 varyingNormal;
varying vec3 varyingLightDir;


void main(void)
{
    // Get surface normal in eye coordinates
    varyingNormal = normalMatrix * gl_Normal; 

    // Get vertex position in eye coordinates
    vec4 vPosition4 = mvMatrix * gl_Vertex; 
    vec3 vPosition3 = vPosition4.xyz / vPosition4.w;
    
    // Get vector to light source
    varyingLightDir = normalize(lightPosition - vPosition3);
    
    // Transform the geometry
    gl_Position = mvpMatrix * gl_Vertex; 
    //gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	//gl_Position = ftransform();
}