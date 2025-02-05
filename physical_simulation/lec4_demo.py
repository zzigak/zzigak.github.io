import taichi as ti
import taichi.math as tm
import numpy as np

ti.init(arch=ti.cpu)

# type aliases
vec2 = tm.vec2
vec3 = tm.vec3

width = 800
height = 800
stepsize = 1/600
g = vec2(0.0, -1.0)
k_v = 0

# data defining particles and springs
# from rope_scene import *
from box_scene import *

# System of Newtonian particles: mass, position, velocity
m = ti.field(dtype=float, shape=N)
x = ti.Vector.field(2, dtype=float, shape=N)
v = ti.Vector.field(2, dtype=float, shape=N)

# previous position, for drawing
x_prev = ti.Vector.field(2, dtype=float, shape=N)

# Taichi fields to hold the list of springs
# first one holds the indices of the two particles connected by the spring
ij_springs = ti.Vector.field(2, dtype=int, shape=nSprings)
# second one holds the parameters of the spring (k_s, k_d, l_0)
sdl_springs = ti.Vector.field(3, dtype=float, shape=nSprings)

# initialize all the fields from scene data imported above
m.from_numpy(particle_masses)
x.from_numpy(particle_posns)
ij_springs.from_numpy(spring_indices)
sdl_springs.from_numpy(spring_params)


@ti.func
def rand_dir():
    return 2 * vec2(ti.random(), ti.random()) - 1
    
@ti.kernel
def init():

    vtotal = vec2(0)
    for i in range(N):
        v[i] = vel_noise * rand_dir()
        vtotal += v[i]

    for i in ti.static(pins):
        vtotal =- v[i]
        v[i] = vec2(0)

    for i in range(N):
        v[i] -= vtotal / N    

    for k in ij_springs:
        i,j = ij_springs[k]
        sdl_springs[k][2] = tm.length(x[j] - x[i])


# Taichi field to hold the forces as they are accumulated
forces = ti.Vector.field(2, dtype=float, shape=N)

ns = int((1/60) // stepsize)
dt = (1/60) / ns
@ti.kernel
def update():

    for i in x:
        x_prev[i] = x[i]
        x[i] = x[i] + dt * v[i]
        forces[i] = g / m[i]
        forces[i] -= k_v * v[i]

    for k in ij_springs:
        i,j = ij_springs[k]
        k_s, k_d, l0 = sdl_springs[k]
        spring_offset = x[j] - x[i]
        l = tm.length(spring_offset)
        spring_dir = tm.normalize(spring_offset)
        f = k_s * (l - l0) * spring_dir
        f += k_d * k_s * (v[j] - v[i]).dot(spring_dir) * spring_dir
        forces[i] += f
        forces[j] -= f

    for i in v:
        v[i] = v[i] + dt * forces[i] / m[i]
        if x[i][1] < 0.0:
            x[i][1] = 0.0
            v[i][1] = tm.max(v[i][1], 0.0)

    for i in ti.static(pins):
        v[i] = vec2(0)


init()

gui = ti.GUI("particles", res=(width, height))
while gui.running:
    for k in range(ns):
        update()
    xa = x.to_numpy()
    xpa = x_prev.to_numpy()
    xma = (xa + xpa) / 2
    ij = ij_springs.to_numpy()
    spring_start = xma[ij[:,0]]
    spring_end = xma[ij[:,1]]
    gui.lines(begin=spring_start, end=spring_end, radius=2, color=0x888888)
    gui.lines(begin=xpa, end=xa, radius=4, color=0xffffcc)
    gui.show()
