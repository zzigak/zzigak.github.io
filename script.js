function toggleBib(element) {
    const bibliography = element.parentElement.nextElementSibling;
    if (bibliography.style.display === "none" || bibliography.style.display === "") {
        bibliography.style.display = "block";
        element.innerHTML = "[hide bibtex]";
    } else {
        bibliography.style.display = "none";
        element.innerHTML = "[show bibtex]";
    }
}

// This line starts the shader background when the page is loaded.
document.addEventListener('DOMContentLoaded', initShaderBackground);

// The code that caused the text to animate in has been removed from here.

function initShaderBackground() {
    const canvas = document.getElementById('shader-canvas');
    const gl = canvas.getContext('webgl');
    if (!gl) {
        console.error('WebGL not supported');
        return;
    }

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);
    }
    window.addEventListener('resize', resize);
    resize();

    function compile(type, src) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, src);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.error(gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
        }
        return shader;
    }

    const vertexSrc = `attribute vec2 aPos;void main(){gl_Position=vec4(aPos,0.0,1.0);}`;
    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;const mat3 K=mat3(127.1,311.7,74.7,269.5,183.3,246.1,113.5,271.9,314.3);float w(vec3 s){vec3 i=floor(s),f=fract(s);float m=1.;for(int Z=-1;Z<=1;Z++)for(int Y=-1;Y<=1;Y++)for(int X=-1;X<=1;X++){vec3 o=vec3(X,Y,Z),p=fract(sin((i+o)*K)*43758.5453);m=min(m,length(o+p-f));}return m;}float f(vec2 u,float t){float S=0.,A=.8,F=5.;for(int I=0;I<3;I++){float n=w(vec3(u*F,t));S+=n*n*n*A;F*=100.;A*=.5;}return pow(S,1.5);}void main(){vec2 u=gl_FragCoord.xy/iResolution;float t=iTime*.15,d_s=.05;vec2 d=vec2(sin(u.x*10.+t)*cos(u.y*8.+t*.5),cos(u.y*10.-t)*sin(u.x*8.-t*.5))*.5+.5;u+=(d*2.-1.)*d_s;float n=f(u*3.,t);gl_FragColor=vec4(mix(mix(vec3(0.),vec3(0,0,.5),clamp(n*2.,0.,1.)),mix(vec3(0,0,.5),vec3(.2,.2,.7),clamp(n*2.-1.,0.,1.)),step(.5,n)),1.);}`;

    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;const mat3 K=mat3(127.1,311.7,74.7,269.5,183.3,246.1,113.5,271.9,314.3);float w(vec3 s){vec3 i=floor(s),f=fract(s);float m=1.;for(int Z=-1;Z<=1;Z++)for(int Y=-1;Y<=1;Y++)for(int X=-1;X<=1;X++){vec3 o=vec3(X,Y,Z),p=fract(sin((i+o)*K)*43758.5453);m=min(m,length(o+p-f));}return m;}float f(vec2 u,float t){float S=0.,A=.8,F=5.;for(int I=0;I<3;I++){float n=w(vec3(u*F,t));S+=n*n*n*A;F*=100.;A*=.5;}return pow(S,1.5);}void main(){vec2 u=gl_FragCoord.xy/iResolution;float t=iTime*.15,d_s=.05;vec2 d=vec2(sin(u.x*10.+t)*cos(u.y*8.+t*.5),cos(u.y*10.-t)*sin(u.x*8.-t*.5))*.5+.5;u+=(d*2.-1.)*d_s;float n=f(u*3.,t);vec3 color_bg=vec3(1.0);vec3 color_wave=vec3(0.85,0.90,1.0);gl_FragColor=vec4(mix(color_bg,color_wave,1.0-smoothstep(0.0,0.8,n)),1.);}`;
    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;const mat3 K=mat3(127.1,311.7,74.7,269.5,183.3,246.1,113.5,271.9,314.3);float w(vec3 s){vec3 i=floor(s),f=fract(s);float m=1.;for(int Z=-1;Z<=1;Z++)for(int Y=-1;Y<=1;Y++)for(int X=-1;X<=1;X++){vec3 o=vec3(X,Y,Z),p=fract(sin((i+o)*K)*43758.5453);m=min(m,length(o+p-f));}return m;}float f(vec2 u,float t){float S=0.,A=.8,F=5.;for(int I=0;I<3;I++){float n=w(vec3(u*F,t));S+=n*n*n*A;F*=100.;A*=.5;}return pow(S,1.5);}void main(){vec2 u=gl_FragCoord.xy/iResolution;float t=iTime*.15,d_s=.05;vec2 d=vec2(sin(u.x*10.+t)*cos(u.y*8.+t*.5),cos(u.y*10.-t)*sin(u.x*8.-t*.5))*.5+.5;u+=(d*2.-1.)*d_s;float n=f(u*3.,t);vec3 color_base = vec3(1.0); vec3 color_mid = vec3(0.95, 0.96, 0.98); vec3 color_highlight = vec3(0.9, 0.92, 1.0); gl_FragColor=vec4(mix(mix(color_base,color_mid,clamp(n*2.,0.,1.)),mix(color_mid,color_highlight,clamp(n*2.-1.,0.,1.)),step(.5,n)),1.);}`;

    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;const mat3 K=mat3(127.1,311.7,74.7,269.5,183.3,246.1,113.5,271.9,314.3);float w(vec3 s){vec3 i=floor(s),f=fract(s);float m=1.;for(int Z=-1;Z<=1;Z++)for(int Y=-1;Y<=1;Y++)for(int X=-1;X<=1;X++){vec3 o=vec3(X,Y,Z),p=fract(sin((i+o)*K)*43758.5453);m=min(m,length(o+p-f));}return m;}float f(vec2 u,float t){float S=0.,A=.8,F=5.;for(int I=0;I<3;I++){float n=w(vec3(u*F,t));S+=n*n*n*A;F*=100.;A*=.5;}return pow(S,1.5);}void main(){vec2 u=gl_FragCoord.xy/iResolution;float t=iTime*.15,d_s=.05;vec2 d=vec2(sin(u.x*10.+t)*cos(u.y*8.+t*.5),cos(u.y*10.-t)*sin(u.x*8.-t*.5))*.5+.5;u+=(d*2.-1.)*d_s;float n=f(u*3.,t);vec3 color_base = vec3(1.0); vec3 color_mid = vec3(0.92, 0.94, 0.99); vec3 color_highlight = vec3(0.85, 0.90, 1.0); gl_FragColor=vec4(mix(mix(color_base,color_mid,clamp(n*2.,0.,1.)),mix(color_mid,color_highlight,clamp(n*2.-1.,0.,1.)),step(.5,n)),1.);}`;

    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;vec2 hash(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return-1.0+2.0*fract(sin(p)*43758.5453);}float noise(vec2 p){vec2 i=floor(p);vec2 f=fract(p);vec2 u=f*f*(3.0-2.0*f);return mix(mix(dot(hash(i+vec2(0.0,0.0)),f-vec2(0.0,0.0)),dot(hash(i+vec2(1.0,0.0)),f-vec2(1.0,0.0)),u.x),mix(dot(hash(i+vec2(0.0,1.0)),f-vec2(0.0,1.0)),dot(hash(i+vec2(1.0,1.0)),f-vec2(1.0,1.0)),u.x),u.y);}const mat2 m=mat2(0.8,-0.6,0.6,0.8);float fbm(vec2 p){float f=0.0;f+=0.5000*noise(p);p=m*p*2.02;f+=0.2500*noise(p);p=m*p*2.03;f+=0.1250*noise(p);p=m*p*2.01;f+=0.0625*noise(p);return f/0.9375;}void main(){float speed=0.1;float zoom=1.0;float contrast=10.0;vec2 u=gl_FragCoord.xy/iResolution.y;float t=iTime*speed;vec2 q=vec2(fbm(u*zoom+t),fbm(u*zoom+vec2(5.2,1.3)+t));vec2 r=vec2(fbm(u*zoom+q*0.5+vec2(1.7,9.2)+t),fbm(u*zoom+q*0.5+vec2(8.3,2.8)+t));float n=fbm(u*zoom+r);n=0.5+0.5*n;n=(n-0.5)*contrast+0.5;vec3 color_base=vec3(1.0);vec3 color_mid=vec3(0.92,0.94,0.99);vec3 color_highlight=vec3(0.85,0.90,1.0);vec3 final_color=mix(color_base,color_mid,smoothstep(0.3,0.6,n));final_color=mix(final_color,color_highlight,smoothstep(0.6,0.9,n));gl_FragColor=vec4(final_color,1.0);}`;
    // const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;vec3 hash(vec3 p){p=vec3(dot(p,vec3(127.1,311.7,74.7)),dot(p,vec3(269.5,183.3,246.1)),dot(p,vec3(113.5,271.9,314.3)));return-1.0+2.0*fract(sin(p)*43758.5453);}float noise(vec3 p){vec3 i=floor(p);vec3 f=fract(p);vec3 u=f*f*f*(f*(f*6.0-15.0)+10.0);return mix(mix(mix(dot(hash(i+vec3(0,0,0)),f-vec3(0,0,0)),dot(hash(i+vec3(1,0,0)),f-vec3(1,0,0)),u.x),mix(dot(hash(i+vec3(0,1,0)),f-vec3(0,1,0)),dot(hash(i+vec3(1,1,0)),f-vec3(1,1,0)),u.x),u.y),mix(mix(dot(hash(i+vec3(0,0,1)),f-vec3(0,0,1)),dot(hash(i+vec3(1,0,1)),f-vec3(1,0,1)),u.x),mix(dot(hash(i+vec3(0,1,1)),f-vec3(0,1,1)),dot(hash(i+vec3(1,1,1)),f-vec3(1,1,1)),u.x),u.y),u.z);}const mat3 m=mat3(0.00,0.80,0.60,-0.80,0.36,-0.48,-0.60,-0.48,0.64);float fbm(vec3 p){float f=0.0;f+=0.5000*noise(p);p=m*p*2.02;f+=0.2500*noise(p);p=m*p*2.03;f+=0.1250*noise(p);p=m*p*2.01;f+=0.0625*noise(p);return f/0.9375;}void main(){float t=iTime;vec2 u=gl_FragCoord.xy/iResolution.y;float contrast=10.0;float speed_slow=0.05;float zoom_slow=0.8;float speed_fast=0.15;float zoom_fast=1.8;float distortion_zoom=2.5;float distortion_speed=0.25;float distortion_strength=0.15;float distortion_pattern=fbm(vec3(u*distortion_zoom,t*distortion_speed));vec2 distorted_uv=u+vec2(distortion_pattern)*distortion_strength;float n1=fbm(vec3(distorted_uv*zoom_slow,t*speed_slow));float n2=fbm(vec3(distorted_uv*zoom_fast+20.0,t*speed_fast));float n=n1*0.65+n2*0.35;n=0.5+0.5*n;n=(n-0.5)*contrast+0.5;vec3 color_base=vec3(1.0);vec3 color_mid=vec3(0.92,0.94,0.99);vec3 color_highlight=vec3(0.85,0.90,1.0);vec3 final_color=mix(color_base,color_mid,smoothstep(0.3,0.6,n));final_color=mix(final_color,color_highlight,smoothstep(0.6,0.9,n));gl_FragColor=vec4(final_color,1.0);}`;

    //     const fragmentSrc = `
    // // Set the precision for floating point numbers
    // precision highp float;

    // // Uniforms: values passed in from your JavaScript
    // uniform vec2 iResolution; // The resolution of the canvas
    // uniform float iTime;       // The current time in secondsa

    // // --- CONFIGURATION ---
    // // Feel free to tweak these values!
    // const vec3 COLOR1 = vec3(0.9, 0.95, 1.0); // Lightest color (almost white with a hint of blue)
    // const vec3 COLOR2 = vec3(0.15, 0.4, 0.7); // Darker blue for the highlights/vortices
    // const float SPEED = 0.1;        // How fast the animation plays
    // const float ZOOM = 1.5;         // Zoom level of the noise
    // const int OCTAVES = 4;          // Number of noise layers to stack for detail

    // // 2D Random function
    // float random(vec2 st) {
    //     return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
    // }

    // // 2D Noise function (a simplified version)
    // float noise(vec2 st) {
    //     vec2 i = floor(st);
    //     vec2 f = fract(st);

    //     float a = random(i);
    //     float b = random(i + vec2(1.0, 0.0));
    //     float c = random(i + vec2(0.0, 1.0));
    //     float d = random(i + vec2(1.0, 1.0));

    //     vec2 u = f * f * (3.0 - 2.0 * f);
    //     return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
    // }

    // // Fractal Brownian Motion (FBM) - stacking noise for more detail
    // float fbm(vec2 st) {
    //     float value = 0.0;
    //     float amplitude = 0.5;
    //     float frequency = 0.0;

    //     for (int i = 0; i < OCTAVES; i++) {
    //         value += amplitude * noise(st);
    //         st *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return value;
    // }

    // void main() {
    //     // Normalize the coordinates to go from 0.0 to 1.0
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;

    //     // Correct for aspect ratio
    //     uv.x *= iResolution.x / iResolution.y;

    //     // --- The Curl Noise Magic ---
    //     float time = iTime * SPEED;

    //     // We sample the noise field at four points close to our current position
    //     // to calculate the "curl" (the amount of rotation)
    //     float eps = 0.01; // A small offset

    //     // The "q" and "r" vectors represent the field we are distorting
    //     vec2 q = vec2( fbm(uv + vec2(0.0, 0.0) + time), fbm(uv + vec2(5.2, 1.3) + time) );
    //     vec2 r = vec2( fbm(uv + q + vec2(1.7, 9.2) + time), fbm(uv + q + vec2(8.3, 2.8) + time) );

    //     // We use the derivatives of the noise (its curl) to distort the coordinate space
    //     // This is what creates the swirling, advection-like effect.
    //     float f = fbm(uv + r * ZOOM);

    //     // --- Coloring ---
    //     // Mix between our two colors based on the final noise value
    //     // The pow() function increases the contrast, creating sharper "wisps"
    //     vec3 color = mix(COLOR1, COLOR2, pow(f, 2.5));

    //     // Final output color
    //     gl_FragColor = vec4(color, 1.0);
    // }
    // `;

    // // The GLSL code for our "faked" but visually rich lava effect.
    // const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Feel free to tweak these!
    // #define OCTAVES 5 // How many layers of noise to stack for detail.
    // const float SEED = 43758.5453;
    // const float SPEED = 0.1; // How fast the lava flows.
    // const float ZOOM = 1.2; // Zoom level of the main pattern.
    // const float BUMP_STRENGTH = 25.0; // How "bumpy" the lighting looks.

    // // Color palette
    // const vec3 COLOR1 = vec3(0.1, 0.05, 0.03); // Deep, dark red
    // const vec3 COLOR2 = vec3(1.0, 0.2, 0.0);   // Fiery orange
    // const vec3 COLOR3 = vec3(1.0, 0.9, 0.0);   // Bright yellow

    // // 2D Hash function to create pseudo-randomness
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }

    // // 2D Simplex-like noise function
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404; // (sqrt(3)-1)/2;
    //     const float K2 = 0.211324865; // (3-sqrt(3))/6;

    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }

    // // Fractal Brownian Motion (FBM) to stack noise for detail
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y; // Correct for aspect ratio

    //     float time = iTime * SPEED;

    //     // --- Domain Warping ---
    //     // This is the key to the swirling motion.
    //     // We use one noise field (q) to distort the coordinates of a second noise field (f).
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3)));

    //     float f = fbm(uv + q * 0.3 + time);

    //     // Normalize the final noise value to a 0-1 range.
    //     float height = 0.5 + 0.5 * f;

    //     // --- Coloring ---
    //     // Map the height value to our color palette.
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.2, 0.6, height));
    //     color = mix(color, COLOR3, smoothstep(0.5, 0.8, height));

    //     // --- Faked Lighting (Procedural Normals) ---
    //     // Calculate the "slope" of the noise field to create a normal vector.
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     // Simple lighting calculation
    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);
    //     float lighting = 0.4 + 0.8 * diffuse; // Ambient + Diffuse

    //     // Final color is the procedural color multiplied by the faked lighting.
    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;

    //     // The GLSL code for a "calm liquid" background effect.
    //     const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Feel free to tweak these!
    // #define OCTAVES 5 // How many layers of noise to stack for detail.
    // const float SEED = 43758.5453;
    // const float SPEED = 0.05;         // CHANGED: Slowed down the animation significantly.
    // const float ZOOM = 1.2;
    // const float BUMP_STRENGTH = 8.0;  // CHANGED: Drastically reduced bumpiness for a softer look.

    // // Color palette - CHANGED to a cool, gentle blue scheme
    // const vec3 COLOR1 = vec3(0.1, 0.2, 0.35);  // Deep, dark blue
    // const vec3 COLOR2 = vec3(0.3, 0.6, 0.7);   // Mid-tone cyan/teal
    // const vec3 COLOR3 = vec3(0.8, 0.95, 1.0);  // Very light, soft sky blue

    // // 2D Hash function to create pseudo-randomness
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }

    // // 2D Simplex-like noise function
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404; // (sqrt(3)-1)/2;
    //     const float K2 = 0.211324865; // (3-sqrt(3))/6;

    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }

    // // Fractal Brownian Motion (FBM) to stack noise for detail
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y; // Correct for aspect ratio

    //     // We still use ZOOM here, which was missing in the original main()
    //     uv *= ZOOM;

    //     float time = iTime * SPEED;

    //     // --- Domain Warping ---
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3)));

    //     float f = fbm(uv + q * 0.3 + time);

    //     // Normalize the final noise value to a 0-1 range.
    //     float height = 0.5 + 0.5 * f;

    //     // --- Coloring ---
    //     // Map the height value to our NEW color palette.
    //     // I've adjusted the smoothstep ranges slightly for a softer blend.
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.1, 0.5, height));
    //     color = mix(color, COLOR3, smoothstep(0.4, 0.7, height));

    //     // --- Faked Lighting (Procedural Normals) ---
    //     // Calculate the "slope" of the noise field to create a normal vector.
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     // Simple lighting calculation
    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     // CHANGED: The lighting model is now much brighter and has less contrast.
    //     // Higher ambient light (0.7) and lower diffuse contribution (0.3).
    //     float lighting = 0.7 + 0.3 * diffuse;

    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;



    // // The GLSL code for a "blue lava" effect, matching the style of the original.
    // const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Feel free to tweak these!
    // #define OCTAVES 5
    // const float SEED = 43758.5453;
    // const float SPEED = 0.1;          // KEPT: Original fast speed
    // const float ZOOM = 1.2;           // KEPT: But still unused, like the original
    // const float BUMP_STRENGTH = 25.0; // KEPT: Original high bumpiness for sharp highlights

    // // Color palette - CHANGED to a high-contrast blue scheme
    // const vec3 COLOR1 = vec3(0.01, 0.05, 0.15); // Deep, dark blue (almost black)
    // const vec3 COLOR2 = vec3(0.1, 0.5, 1.0);    // Vibrant, electric blue
    // const vec3 COLOR3 = vec3(0.8, 0.9, 1.0);    // Bright, near-white cyan highlight

    // // 2D Hash function to create pseudo-randomness
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }

    // // 2D Simplex-like noise function
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404; // (sqrt(3)-1)/2;
    //     const float K2 = 0.211324865; // (3-sqrt(3))/6;

    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }

    // // Fractal Brownian Motion (FBM) to stack noise for detail
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y; // Correct for aspect ratio

    //     // NOTE: uv is NOT multiplied by ZOOM, exactly like the original lava shader.

    //     float time = iTime * SPEED;

    //     // --- Domain Warping ---
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3)));

    //     float f = fbm(uv + q * 0.3 + time);

    //     // Normalize the final noise value to a 0-1 range.
    //     float height = 0.5 + 0.5 * f;

    //     // --- Coloring ---
    //     // Map the height value to our color palette.
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.2, 0.6, height));
    //     color = mix(color, COLOR3, smoothstep(0.5, 0.8, height));

    //     // --- Faked Lighting (Procedural Normals) ---
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     // Simple lighting calculation
    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     // KEPT: Original high-contrast lighting formula
    //     float lighting = 0.4 + 0.8 * diffuse;

    //     // Final color is the procedural color multiplied by the faked lighting.
    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;

    //     // The GLSL code for a turbulent, mostly-white background with blue highlights.
    //     const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Tuned for a bright, white, and energetic feel
    // #define OCTAVES 5
    // const float SEED = 43758.5453;
    // const float SPEED = 0.1;           // KEPT: Original fast speed for the "boiling" motion.
    // const float ZOOM = 1.2;            // KEPT: Unused, to match original fine-grained pattern.
    // const float BUMP_STRENGTH = 20.0;  // KEPT: High value for sharp, defined highlights.

    // // Color palette - CHANGED: Base is now white, highlights are blue.
    // const vec3 COLOR1 = vec3(0.95, 0.95, 0.95); // The base color: a very light, soft gray/off-white.
    // const vec3 COLOR2 = vec3(0.85, 0.92, 1.0);  // The mid-tone: a soft, light blue for the highlights.
    // const vec3 COLOR3 = vec3(1.0, 1.0, 1.0);    // The peak highlight: pure, crisp white.

    // // 2D Hash function to create pseudo-randomness
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }

    // // 2D Simplex-like noise function
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404; // (sqrt(3)-1)/2;
    //     const float K2 = 0.211324865; // (3-sqrt(3))/6;

    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }

    // // Fractal Brownian Motion (FBM) to stack noise for detail
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y;

    //     // NOTE: uv is NOT multiplied by ZOOM, matching the lava shader's fine-grained look.

    //     float time = iTime * SPEED;

    //     // --- Domain Warping ---
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3)));
    //     float f = fbm(uv + q * 0.3 + time);
    //     float height = 0.5 + 0.5 * f;

    //     // --- Coloring ---
    //     // The noise value now maps from off-white -> light blue -> pure white.
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.6, height)); // Blue appears in the mid-range
    //     color = mix(color, COLOR3, smoothstep(0.55, 0.8, height));   // Hottest spots become pure white

    //     // --- Faked Lighting ---
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     // We can use a slightly higher contrast lighting model now because the base colors are so bright.
    //     float lighting = 0.8 + 0.2 * diffuse;

    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;

    //     // The GLSL code for a "Living Marble" effect: slow, internal swirling.
    //     const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Tuned for slow, viscous, internal motion
    // #define OCTAVES 5a
    // const float SEED = 43758.5453;
    // const float SPEED = 2.0;          // CHANGED: Significantly slower for a more majestic feel.
    // const float ZOOM = 1.2;            // KEPT: Unused, for the fine-grained texture.
    // const float BUMP_STRENGTH = 15.0;  // CHANGED: Slightly softened for a more liquid feel.

    // // Color palette - "Turbulent Marble" (White & Blue)
    // const vec3 COLOR1 = vec3(0.95, 0.95, 0.95); // Base: soft off-white
    // const vec3 COLOR2 = vec3(0.85, 0.92, 1.0);  // Mid: soft light blue
    // const vec3 COLOR3 = vec3(1.0, 1.0, 1.0);    // Peak: crisp white

    // // --- FUNCTIONS (hash, noise, fbm) are unchanged ---
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404;
    //     const float K2 = 0.211324865;
    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y;

    //     float time = iTime * SPEED;

    //     // --- NEW ANIMATION LOGIC ---
    //     // 1. The "Stirring Rod": A non-linear, wandering motion for the distortion field.
    //     // This uses sin/cos to create a path that is not a straight line.
    //     vec2 distortion_flow = vec2(cos(time * 0.3), sin(time * 0.5)) * 0.3;

    //     // 2. The "Base Drift": A very slow, almost unnoticeable scroll for the main texture.
    //     // This prevents it from being perfectly static, adding a subtle underlying drift.
    //     vec2 base_drift = vec2(time * 0.02, time * 0.02);

    //     // --- Domain Warping ---
    //     // The distortion field 'q' is animated strongly by 'distortion_flow'.
    //     vec2 q_uv = uv + distortion_flow;
    //     vec2 q = vec2(fbm(q_uv),
    //                   fbm(q_uv + vec2(5.2, 1.3)));

    //     // The base field 'f' is warped by 'q' and animated only by the slow 'base_drift'.
    //     // This is the key: the main texture is not scrolling, it's being churned in place.
    //     vec2 final_uv = uv + q * 0.3 + base_drift;
    //     float height = 0.5 + 0.5 * fbm(final_uv);

    //     // --- Coloring ---
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.6, height));
    //     color = mix(color, COLOR3, smoothstep(0.55, 0.8, height));

    //     // --- Faked Lighting ---
    //     // Normals are calculated based on the final, warped coordinates for accuracy.
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(final_uv + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(final_uv + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     float lighting = 0.85 + 0.15 * diffuse;

    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;

    // // The GLSL code for a soft, distinctly blue, and text-friendly background.
    // const fragmentSrc = `
    //    precision highp float;

    //    uniform vec2 iResolution;
    //    uniform float iTime;

    //    // --- CONFIGURATION --- Feel free to tweak these!
    //    #define OCTAVES 5
    //    const float SEED = 43758.5453;
    //    const float SPEED = 0.04;
    //    const float ZOOM = 1.2;
    //    const float BUMP_STRENGTH = 5.0; // Slightly increased bump for a bit more visual interest

    //    // Color palette - CHANGED to be distinctly blue while remaining light.
    //    const vec3 COLOR1 = vec3(0.65, 0.75, 0.90); // A clear, soft dusky blue
    //    const vec3 COLOR2 = vec3(0.80, 0.88, 0.98); // A light, airy blue
    //    const vec3 COLOR3 = vec3(0.95, 0.98, 1.00); // An extremely light, icy blue highlight

    //    // 2D Hash function to create pseudo-randomness
    //    vec2 hash(vec2 p) {
    //        p = vec2(dot(p, vec2(127.1, 311.7)),
    //                 dot(p, vec2(269.5, 183.3)));
    //        return -1.0 + 2.0 * fract(sin(p) * SEED);
    //    }

    //    // 2D Simplex-like noise function
    //    float noise(in vec2 p) {
    //        const float K1 = 0.366025404; // (sqrt(3)-1)/2;
    //        const float K2 = 0.211324865; // (3-sqrt(3))/6;

    //        vec2 i = floor(p + (p.x + p.y) * K1);
    //        vec2 a = p - i + (i.x + i.y) * K2;
    //        float m = step(a.y, a.x);
    //        vec2 o = vec2(m, 1.0 - m);
    //        vec2 b = a - o + K2;
    //        vec2 c = a - 1.0 + 2.0 * K2;
    //        vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //        vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //        return dot(n, vec3(70.0));
    //    }

    //    // Fractal Brownian Motion (FBM) to stack noise for detail
    //    float fbm(in vec2 p) {
    //        float total = 0.0;
    //        float amplitude = 0.5;
    //        for (int i = 0; i < OCTAVES; i++) {
    //            total += noise(p) * amplitude;
    //            p *= 2.0;
    //            amplitude *= 0.5;
    //        }
    //        return total;
    //    }

    //    void main() {
    //        vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //        uv.x *= iResolution.x / iResolution.y;
    //        uv *= ZOOM;

    //        float time = iTime * SPEED;

    //        // --- Domain Warping ---
    //        vec2 q = vec2(fbm(uv + time),
    //                      fbm(uv + vec2(5.2, 1.3)));
    //        float f = fbm(uv + q * 0.3 + time);
    //        float height = 0.5 + 0.5 * f;

    //        // --- Coloring ---
    //        vec3 color = mix(COLOR1, COLOR2, smoothstep(0.1, 0.5, height));
    //        color = mix(color, COLOR3, smoothstep(0.4, 0.7, height));

    //        // --- Faked Lighting (Procedural Normals) ---
    //        float epsilon = 0.001;
    //        float h_x = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(epsilon, 0.0));
    //        float h_y = 0.5 + 0.5 * fbm(uv + q * 0.3 + time + vec2(0.0, epsilon));
    //        vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //        vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //        float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //        // Keep the lighting model bright to ensure readability
    //        float lighting = 0.85 + 0.15 * diffuse;

    //        gl_FragColor = vec4(color * lighting, 1.0);
    //    }
    //    `;


    // // The GLSL code for a "Deepwater Flow" effect.
    // const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;

    // // --- CONFIGURATION --- Tuned for deep, powerful, flowing motion
    // #define OCTAVES 5
    // const float SEED = 43758.5453;
    // const float SPEED = 0.25;          // CHANGED: Much faster overall speed for the fluid itself.
    // const float ZOOM = 1.2;            // CHANGED: Using zoom for larger, more liquid-like features.
    // const float BUMP_STRENGTH = 6.0;   // A good mid-range value for this look.

    // // Color palette - USING YOUR PREFERRED BLUE PALETTE
    // const vec3 COLOR1 = vec3(0.65, 0.75, 0.90); // A clear, soft dusky blue
    // const vec3 COLOR2 = vec3(0.80, 0.88, 0.98); // A light, airy blue
    // const vec3 COLOR3 = vec3(0.95, 0.98, 1.00); // An extremely light, icy blue highlight

    // // --- FUNCTIONS (hash, noise, fbm) are unchanged ---
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404;
    //     const float K2 = 0.211324865;
    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y;
    //     uv *= ZOOM; // Apply zoom for larger features

    //     float time = iTime * SPEED;

    //     // --- NEW ANIMATION LOGIC ---
    //     // 1. "The Steering Wheel": The direction of flow.
    //     // The multipliers for time are now very small (0.05, 0.08), so the
    //     // direction changes very slowly and gracefully.
    //     vec2 steering_direction = vec2(cos(time * 0.05), sin(time * 0.08));

    //     // 2. The Distortion Field 'q' is what "stirs" the liquid.
    //     // We animate it with the fast 'time' variable, causing rapid internal churning.
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3) + time * 0.5));

    //     // 3. The final coordinates are warped by the fast-churning 'q',
    //     // and also pushed along the slow-changing 'steering_direction'.
    //     // The magnitude ( * 0.3 ) of the steering is subtle.
    //     vec2 final_uv = uv + q * 0.3 + steering_direction * 0.3;
    //     float height = 0.5 + 0.5 * fbm(final_uv);

    //     // --- Coloring ---
    //     // Using your requested colors.
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.65, height));
    //     color = mix(color, COLOR3, smoothstep(0.6, 0.8, height));

    //     // --- Faked Lighting ---
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(final_uv + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(final_uv + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     // A bright lighting model that complements the blue palette.
    //     float lighting = 0.85 + 0.15 * diffuse;

    //     gl_FragColor = vec4(color * lighting, 1.0);
    // }
    // `;

    // //     // The GLSL code for the "Glimmering Current" effect.
    // const fragmentSrc = `
    // precision highp float;

    // uniform vec2 iResolution;
    // uniform float iTime;
    // uniform float uSeed;

    // // --- CONFIGURATION --- Tuned for a SHIMMERING, high-contrast look
    // #define OCTAVES 10
    // const float SEED = 43758.5453;
    // const float SPEED = 0.2;
    // const float ZOOM = 1.2;
    // const float BUMP_STRENGTH = 12.0; // Strong bumpiness to catch the light.

    // // Color palette - Your preferred blues
    // const vec3 COLOR1 = vec3(0.70, 0.80, 0.95); // Slightly brighter dusky blue
    // const vec3 COLOR2 = vec3(0.85, 0.93, 1.00); // Slightly brighter airy blue
    // const vec3 COLOR3 = vec3(1.00, 1.00, 1.00); // Pure white for highlight

    // // --- FUNCTIONS (hash, noise, fbm) are unchanged ---
    // vec2 hash(vec2 p) {
    //     p = vec2(dot(p, vec2(127.1, 311.7)),
    //              dot(p, vec2(269.5, 183.3)));
    //     return -1.0 + 2.0 * fract(sin(p) * SEED);
    // }
    // float noise(in vec2 p) {
    //     const float K1 = 0.366025404;
    //     const float K2 = 0.211324865;
    //     vec2 i = floor(p + (p.x + p.y) * K1);
    //     vec2 a = p - i + (i.x + i.y) * K2;
    //     float m = step(a.y, a.x);
    //     vec2 o = vec2(m, 1.0 - m);
    //     vec2 b = a - o + K2;
    //     vec2 c = a - 1.0 + 2.0 * K2;
    //     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    //     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    //     return dot(n, vec3(70.0));
    // }
    // float fbm(in vec2 p) {
    //     float total = 0.0;
    //     float amplitude = 0.5;
    //     for (int i = 0; i < OCTAVES; i++) {
    //         total += noise(p) * amplitude;
    //         p *= 2.0;
    //         amplitude *= 0.5;
    //     }
    //     return total;
    // }

    // void main() {
    //     vec2 uv = gl_FragCoord.xy / iResolution.xy;
    //     uv.x *= iResolution.x / iResolution.y;
    //     uv *= ZOOM;

    //     float time = iTime * SPEED + uSeed * 100.0;

    //     // Motion logic is preserved
    //     vec2 steering_direction = vec2(cos(time * 0.05), sin(time * 0.08));
    //     vec2 q = vec2(fbm(uv + time),
    //                   fbm(uv + vec2(5.2, 1.3) + time * 0.5));
    //     vec2 final_uv = uv + q * 0.3 + steering_direction * 0.3;
    //     float height = 0.5 + 0.5 * fbm(final_uv);

    //     // --- Coloring ---
    //     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.65, height));
    //     color = mix(color, COLOR3, smoothstep(0.6, 0.8, height));

    //     // --- Faked Lighting ---
    //     float epsilon = 0.001;
    //     float h_x = 0.5 + 0.5 * fbm(final_uv + vec2(epsilon, 0.0));
    //     float h_y = 0.5 + 0.5 * fbm(final_uv + vec2(0.0, epsilon));
    //     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    //     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    //     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);

    //     // --- CRITICAL CHANGE: SPECULAR HIGHLIGHTS ---
    //     // We add a specular term to create sharp, bright glints.
    //     // pow(diffuse, N) tightens the highlight. A larger N means a smaller, sharper glint.
    //     float specular_power = 32.0;
    //     float specular = pow(diffuse, specular_power);

    //     // The final color is now the base color PLUS a strong specular highlight.
    //     // This adds a bright white layer on top, breaking the homogeneity.
    //     vec3 final_color = color + vec3(1.0) * specular * 0.7;

    //     gl_FragColor = vec4(final_color, 1.0);
    // }
    // `;

   // The GLSL code for the "Glimmering Current" effect.
// const fragmentSrc = `
// precision highp float;

// uniform vec2 iResolution;
// uniform float iTime;
// uniform float uSeed;

// // --- CONFIGURATION (Unchanged) ---
// #define OCTAVES 10
// const float SEED = 43758.5453;
// const float SPEED = 0.15;
// const float ZOOM = 1.2;
// const float BUMP_STRENGTH = 30.0;

// // --- COLOR PALETTE: COMPRESSED & LUMINOUS ---
// // *** CHANGE 1: Softer, closer colors to reduce harsh contrast ***
// // The "darkest" color is now a pleasant, bright dusky blue.
// const vec3 COLOR1 = vec3(0.78, 0.84, 0.97);
// // The "mid" color is a very light, airy blue, creating a subtle, pearlescent shift.
// const vec3 COLOR2 = vec3(0.97, 0.98, 1.0);
// // Pure white is reserved only for the sharpest highlights.
// const vec3 COLOR3 = vec3(1.0, 1.0, 1.0);

// // --- FUNCTIONS (hash, noise, fbm) are unchanged ---
// vec2 hash(vec2 p) {
//     p = vec2(dot(p, vec2(127.1, 311.7)),
//              dot(p, vec2(269.5, 183.3)));
//     return -1.0 + 2.0 * fract(sin(p) * SEED);
// }
// float noise(in vec2 p) {
//     const float K1 = 0.366025404;
//     const float K2 = 0.211324865;
//     vec2 i = floor(p + (p.x + p.y) * K1);
//     vec2 a = p - i + (i.x + i.y) * K2;
//     float m = step(a.y, a.x);
//     vec2 o = vec2(m, 1.0 - m);
//     vec2 b = a - o + K2;
//     vec2 c = a - 1.0 + 2.0 * K2;
//     vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
//     vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
//     return dot(n, vec3(70.0));
// }
// float fbm(in vec2 p) {
//     float total = 0.0;
//     float amplitude = 0.5;
//     for (int i = 0; i < OCTAVES; i++) {
//         total += noise(p) * amplitude;
//         p *= 2.0;
//         amplitude *= 0.5;
//     }
//     return total;
// }

// void main() {

//     vec2 uv = gl_FragCoord.xy / iResolution.xy;
//     uv.x *= iResolution.x / iResolution.y;
//     uv *= ZOOM;

//     float time = iTime * SPEED + uSeed * 100.0;

//     vec2 steering_direction = vec2(cos(time * 0.05), sin(time * 0.08));
//     vec2 q = vec2(fbm(uv + time),
//                   fbm(uv + vec2(5.2, 1.3) + time * 0.5));
//     vec2 final_uv = uv + q * 0.3 + steering_direction * 0.3;
//     float height = 0.5 + 0.5 * fbm(final_uv);

//     // --- Coloring ---
//     // *** CHANGE 2: Smoother, wider transition range ***
//     vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.7, height));
//     color = mix(color, COLOR3, smoothstep(0.65, 0.8, height));

//     // --- Faked Lighting (Unchanged) ---
//     float epsilon = 0.0075;
//     float h_x = 0.5 + 0.5 * fbm(final_uv + vec2(epsilon, 0.0));
//     float h_y = 0.5 + 0.5 * fbm(final_uv + vec2(0.0, epsilon));
//     vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

//     vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
//     float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);
    
//     float specular_power = 32.0;
//     float specular = pow(diffuse, specular_power);

//     // *** CHANGE 3: Balanced highlight that adds shimmer without blowing out the image ***
//     // vec3 final_color = color + vec3(1.0) * specular * 0.3;
//     vec3 final_color = mix(color, vec3(1.0), specular * 0.8);


//     gl_FragColor = vec4(final_color, 1.0);
// }
// `;

// // The GLSL code for the "Glimmering Current" effect.
const fragmentSrc = `
precision highp float;

uniform vec2 iResolution;
uniform float iTime;
uniform float uSeed;

// --- CONFIGURATION (Unchanged) ---
#define OCTAVES 10
const float SEED = 43758.5453;
const float SPEED = 0.15;
const float ZOOM = 1.2;
const float BUMP_STRENGTH = 30.0;

// --- COLOR PALETTE: COMPRESSED & LUMINOUS ---
const vec3 COLOR1 = vec3(0.78, 0.84, 0.97);
const vec3 COLOR2 = vec3(0.97, 0.98, 1.0);
const vec3 COLOR3 = vec3(1.0, 1.0, 1.0);

// --- FUNCTIONS (hash, noise, fbm) are unchanged ---
vec2 hash(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * SEED);
}
float noise(in vec2 p) {
    const float K1 = 0.366025404;
    const float K2 = 0.211324865;
    vec2 i = floor(p + (p.x + p.y) * K1);
    vec2 a = p - i + (i.x + i.y) * K2;
    float m = step(a.y, a.x);
    vec2 o = vec2(m, 1.0 - m);
    vec2 b = a - o + K2;
    vec2 c = a - 1.0 + 2.0 * K2;
    vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
    return dot(n, vec3(70.0));
}
float fbm(in vec2 p) {
    float total = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < OCTAVES; i++) {
        total += noise(p) * amplitude;
        p *= 2.0;
        amplitude *= 0.5;
    }
    return total;
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    uv.x *= iResolution.x / iResolution.y;
    uv *= ZOOM;

    float time = iTime * SPEED + uSeed * 100.0;

    vec2 steering_direction = vec2(cos(time * 0.05), sin(time * 0.08));
    vec2 q = vec2(fbm(uv + time),
                  fbm(uv + vec2(5.2, 1.3) + time * 0.5));
    vec2 final_uv = uv + q * 0.3 + steering_direction * 0.3;
    float height = 0.5 + 0.5 * fbm(final_uv);

    // --- Coloring ---
    vec3 color = mix(COLOR1, COLOR2, smoothstep(0.3, 0.7, height));
    color = mix(color, COLOR3, smoothstep(0.65, 0.8, height));

    // --- Faked Lighting (Unchanged) ---
    float epsilon = 0.0075;
    float h_x = 0.5 + 0.5 * fbm(final_uv + vec2(epsilon, 0.0));
    float h_y = 0.5 + 0.5 * fbm(final_uv + vec2(0.0, epsilon));
    vec3 normal = normalize(vec3( (height - h_x) * BUMP_STRENGTH, (height - h_y) * BUMP_STRENGTH, 1.0));

    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);
    
    float specular_power = 32.0;
    float specular = pow(diffuse, specular_power);

    // *** MODIFIED LINE ***
    // Use mix() to blend the highlight in. This prevents color values from
    // exceeding 1.0, which was causing the blown-out white spot.
    vec3 final_color = mix(color, vec3(1.0), specular * 0.8);

    gl_FragColor = vec4(final_color, 1.0);
}
`;


    const vs = compile(gl.VERTEX_SHADER, vertexSrc);
    const fs = compile(gl.FRAGMENT_SHADER, fragmentSrc);
    if (!vs || !fs) return;

    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.bindAttribLocation(prog, 0, 'aPos');
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(prog));
        return;
    }
    gl.useProgram(prog);

    const quad = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quad);
    gl.bufferData(
        gl.ARRAY_BUFFER,
        new Float32Array([
            -1, -1, 1, -1, -1, 1,
            1, -1, 1, 1, -1, 1
        ]),
        gl.STATIC_DRAW
    );
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    const uRes = gl.getUniformLocation(prog, 'iResolution');
    const uTime = gl.getUniformLocation(prog, 'iTime');
    const uSeed = gl.getUniformLocation(prog, 'uSeed');

    // Generate a random seed for this session
    const randomSeed = Math.random();

    const start = performance.now();
    function render(now) {
        const t = (now - start) * 0.001;
        let W = canvas.width, H = canvas.height;
        let resX = W, resY = H;
        if (H > W) {
            resX = W * 2;
            resY = H * 1.5;
        }
        gl.uniform2f(uRes, resX, resY);
        gl.uniform1f(uTime, t);
        gl.uniform1f(uSeed, randomSeed);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
}

