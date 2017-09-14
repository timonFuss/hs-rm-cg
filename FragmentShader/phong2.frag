
uniform vec4 ambientColor;
uniform vec4 diffuseColor;
uniform vec4 specularColor; 

varying vec3 varyingVertex;
varying vec3 varyingLightDir;
varying vec3 varyingNormal;


float intensity(vec3 u, vec3 v) {
	return  max(0.0, dot(normalize(u), normalize(v)));
}

void main(void) 
{
    // Eye position is view direction
    vec3 eye = normalize(-varyingVertex);

    // Direction of reflected light
    vec3 reflected = normalize(reflect(-varyingLightDir, varyingNormal));

    // Ambient color
    vec4 ambientC  = gl_LightSource[0].ambient * ambientColor;
    gl_FragColor = ambientC;

    // Dot product between normal and light direction gives diffuse intensity
    float dI = intensity(varyingNormal,varyingLightDir);
    vec4 diffuseC  = dI * gl_LightSource[0].diffuse * diffuseColor;
    gl_FragColor += diffuseC;

    // If diffuse light is zero, don't even bother with the power function
    if(dI != 0.0) {
        // Dot product between reflected light direction and view direction gives specular intensity
        float shininess = 128.0; 
        float sI = pow(intensity(reflected, eye), shininess);
        vec4 specularC = sI * gl_LightSource[0].specular * specularColor;
        gl_FragColor  += specularC;
    }
}
