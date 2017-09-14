// Phong fragment shader from 
// Richard S. Wright Jr. 
// OpenGL SuperBible
//# version 330

//out vec4 vFragColor;
//vec4 vFragColor;

uniform vec4 ambientColor;
uniform vec4 diffuseColor;
uniform vec4 specularColor; 

//in vec3 vVaryingNormal;
//in vec3 vVaryingLightDir;

varying vec3 varyingNormal;
varying vec3 varyingLightDir;

float intensity(vec3 u, vec3 v) {
	return  max(0.0, dot(normalize(u), normalize(v)));
}

void main(void) 
{
    // Dot product gives diffuse intensity
    float diff =intensity(varyingNormal,varyingLightDir);
    
    // Multiply intensity by diffuse color, force alpha to 1.0
    vec4 vFragColor = diff * diffuseColor;
    
    // Add in ambient light
    vFragColor += ambientColor;
    
    // Specular light
    vec3 vReflection = normalize(reflect(-normalize(varyingLightDir), normalize(varyingNormal)));
    float spec = intensity(varyingNormal, vReflection);
    
    // If diffuse light is zero, don't even bother with the power function
    if(diff != 0.0) {
        float fSpec = pow(spec, 128.0);
        vFragColor.rgb += vec3(fSpec, fSpec, fSpec); 
    }
	gl_FragColor = vFragColor;
}
