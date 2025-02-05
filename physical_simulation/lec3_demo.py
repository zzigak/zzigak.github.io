import taichi as ti
import taichi.math as tm
import numpy as np

ti.init(arch=ti.gpu)

# type aliases
vec2 = tm.vec2

N = 5000
width = 800
height = 800
dt = 1/60


# Particle system that advects particles along prescribed field

@ti.func
def velocity_field(p : vec2):
    return vec2(p.x, p.y*p.y)

x = ti.Vector.field(2, dtype=float, shape=N)
x_prev = ti.Vector.field(2, dtype=float, shape=N)

@ti.kernel
def update(s : float, h : float, midpoint : int):
    ns = int((1/60) // h) + 1
    dt = (1/60) / ns
    for i in x:
        x_prev[i] = x[i]
        for k in range(ns):
            if midpoint:
                xm = x[i] + (dt/2) * s * velocity_field(x[i])
                x[i] = x[i] + dt * s * velocity_field(xm)
            else:
                x[i] = x[i] + dt * s * velocity_field(x[i])

@ti.kernel
def init():
    for i in x:
        x[i] = 1.5 * tm.vec2(ti.random(), ti.random()) - 0.75

init()

gui = ti.GUI("lines", res=(width, height))
speed = gui.slider('speed', 1, 10)
stepsize = gui.slider('log step size', -3, -1)
midpoint = gui.slider('midpoint', 0, 1)
while gui.running:
    update(
        float(speed.value), 
        np.power(10.0, float(stepsize.value)),
        int(round(float(midpoint.value)))
    )
    gui.lines(begin=x_prev.to_numpy() + 0.5, end=x.to_numpy() + 0.5, radius=2, color=0xffff40)
    gui.show()
