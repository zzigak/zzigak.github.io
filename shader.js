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

document.addEventListener('DOMContentLoaded', initShaderBackground);
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".entry, .contact-info, h1, h2, p").forEach((el, i) => {
      el.classList.add("fade-in");
      el.style.animationDelay = `${i * 0.1}s`;
    });
  });
  

function initShaderBackground() {
    const canvas = document.getElementById('shader-canvas');
    const gl = canvas.getContext('webgl');
    if (!gl) {
        console.error('WebGL not supported');
        return;
    }

    function resize() {
        canvas.width  = window.innerWidth;
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
    const fragmentSrc = `precision highp float;uniform vec2 iResolution;uniform float iTime;const mat3 K=mat3(127.1,311.7,74.7,269.5,183.3,246.1,113.5,271.9,314.3);float w(vec3 s){vec3 i=floor(s),f=fract(s);float m=1.;for(int Z=-1;Z<=1;Z++)for(int Y=-1;Y<=1;Y++)for(int X=-1;X<=1;X++){vec3 o=vec3(X,Y,Z),p=fract(sin((i+o)*K)*43758.5453);m=min(m,length(o+p-f));}return m;}float f(vec2 u,float t){float S=0.,A=.7,F=4.;for(int I=0;I<3;I++){float n=w(vec3(u*F,t));S+=n*n*n*A;F*=80.;A*=.6;}return pow(S,1.3);}void main(){vec2 u=gl_FragCoord.xy/iResolution;float t=iTime*.08,d_s=.02;vec2 d=vec2(sin(u.x*6.+t)*cos(u.y*5.+t*.6),cos(u.y*6.-t)*sin(u.x*5.-t*.6))*.5+.5;u+=(d*2.-1.)*d_s;float n=f(u*2.,t);vec3 nord5=vec3(0.90,0.92,0.95);vec3 nord6=vec3(0.93,0.94,0.96);vec3 nord9=vec3(0.25,0.35,0.52);vec3 nord10=vec3(0.18,0.28,0.44);gl_FragColor=vec4(mix(mix(nord6,nord5,clamp(n*2.0,0.,1.)),mix(nord5,mix(nord9,nord10,sin(t*0.3)*0.4+0.5),clamp(n*2.0-0.5,0.,1.)),step(0.2,n)),1.);}`;

    const vs = compile(gl.VERTEX_SHADER,   vertexSrc);
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
            -1, -1,  1, -1, -1, 1,
             1, -1,  1,  1, -1, 1
        ]),
        gl.STATIC_DRAW
    );
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    const uRes  = gl.getUniformLocation(prog, 'iResolution');
    const uTime = gl.getUniformLocation(prog, 'iTime');

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
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
}
