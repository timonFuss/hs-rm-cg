
uniform mat4 mvpMatrix; 
uniform mat4 mvMatrix; 
uniform mat3 normalMatrix; 
uniform vec3 lightPosition; 

varying vec3 varyingVertex;
varying vec3 varyingLightDir;
varying vec3 varyingNormal;


void main(void)
{
    // Get surface normal in eye coordinates
    varyingNormal = normalMatrix * gl_Normal; 

    // Get vertex position in eye coordinates
    vec4 vPosition4 = mvMatrix * gl_Vertex; 
    varyingVertex = vPosition4.xyz / vPosition4.w;
    
    // Get vector to light source
    varyingLightDir = normalize(lightPosition - varyingVertex);
    
    // Transform the geometry
    gl_Position = mvpMatrix * gl_Vertex; 
}