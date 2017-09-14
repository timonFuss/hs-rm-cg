// Gouraud vertex shader from 
// Richard S. Wright Jr. 
// OpenGL SuperBible
//#version 330

uniform vec4 ambientColor; 
uniform vec4 diffuseColor; 
uniform vec4 specularColor; 

uniform vec3 lightPosition; 

uniform mat4 mvpMatrix; 
uniform mat4 mvMatrix; 
uniform mat3 normalMatrix; 

varying vec4 varyingColor;

void main(void)
{
    // Get surface normal in eye coordinates
    vec3 eyeNormal = normalize(normalMatrix * gl_Normal); 

    // Get vertex position in eye coordinates
    vec4 vPosition4 = mvMatrix * gl_Vertex; 
    vec3 vPosition3 = vPosition4.xyz / vPosition4.w;
    
    // Get vector to light source
    vec3 vLightDir = normalize(lightPosition - vPosition3);
    
	// Dot product gives the diffuse intensity
	float diff = max(0.0, dot(eyeNormal, vLightDir)); 
	
	// Multiply intensity by diffuse color, force alpha to 1.0
	varyingColor = diff * diffuseColor; 

	// Add in ambient light
	varyingColor += ambientColor;
	
	// Specular light
	vec3 reflection = normalize(reflect(-vLightDir, eyeNormal));
	float spec = max(0.0, dot(eyeNormal, reflection));
	if (diff != 0.0) {
		float fSpec = pow(spec, 128.0);
		varyingColor.rgb += vec3(fSpec, fSpec, fSpec);
	}
	
    // Transform the geometry
    gl_Position = mvpMatrix * gl_Vertex; 
}