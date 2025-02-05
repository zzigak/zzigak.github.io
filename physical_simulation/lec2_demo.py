# import taichi as ti
# import taichi.math as tm
# import numpy as np

# ti.init(arch=ti.cpu)

# # type aliases
# vec2 = tm.vec2

# # System-wide parameters
# N = 1
# width = 800
# height = 800
# stepsize = 1/60  # time step
# m = 1  # mass of each particle
# c = vec2(0.5,0.5)  # center of attraction
# k_s = 20   # coefficient of spring force
# v_init = 1.0
# x_scale = 0.5


# # System of Newtonian particles

# x = ti.Vector.field(2, dtype=float, shape=N)
# x_prev = ti.Vector.field(2, dtype=float, shape=N)
# v = ti.Vector.field(2, dtype=float, shape=N)

    
# @ti.func
# def rand_dir():
#     return 2 * vec2(ti.random(), ti.random()) - 1

# @ti.kernel
# def init():
#     # initialize particles to a square, with random initial velocities
#     for i in x:
#         x[i] = x_scale * rand_dir() + 0.5
#         v[i] = v_init * rand_dir()


# ns = 1/60 // stepsize  # number of timesteps per frame
# dt = 1/60 / ns         # exact stepsize (adjusted to divide frame time)
# @ti.kernel
# def update():
#     for i in x:
#         x_prev[i] = x[i]
#         for k in range(ns):
#             force = vec2(0)
#             # spring force between particle and fixed anchor
#             force -= k_s * (x[i] - c)
#             # update
#             v[i] = v[i] + dt * force / m
#             x[i] = x[i] + dt * v[i]

# init()

# print("ns", ns)
# gui = ti.GUI("particles", res=(width, height))
# while gui.running:
#     update()
#     gui.lines(begin=x_prev.to_numpy(), end=x.to_numpy(), radius=4, color=0xffffcc)
#     gui.show()

import taichi as ti
import taichi.math as tm
import numpy as np

ti.init(arch=ti.cpu)

# type aliases
vec2 = tm.vec2

N = 10000
n = 100
width = 800
height = 800
stepsize = 1/600  
m = 1
g = vec2(0, -1)
k_v = 0.1
k_a = 10
v_init = 10

# state for a system of Newtonian particles
x = ti.Vector.field(2, dtype=float, shape=N)
v = ti.Vector.field(2, dtype=float, shape=N)
x_prev = ti.Vector.field(2, dtype=float, shape=N)
i_next = ti.field(dtype=int, shape=())

# update the particle system for one frame
ns = 1/60 // stepsize  # number of time steps per frame
dt = 1/60 / ns         # duration of one time step

# generate a random direction that is nearly on a sphere, projected into 2D
@ti.func
def rand_dir():
    x = 2 * ti.random() - 1
    y = tm.cos(tm.pi * ti.random()) * tm.sqrt(1 - x**2)
    return vec2(x,y) * (1 + 0.2 * (ti.random() - 0.5))

@ti.kernel
def update():
    for i in x:
        # old position goes in x_prev for simple motion blur
        x_prev[i] = x[i]
        for k in range(ns):
            force = m * g
            force += -k_v * v[i]
            force += -k_a * tm.length(v[i]) * v[i]
            x[i] = x[i] + dt * v[i]
            v[i] = v[i] + dt * force / m

# initialize the particles for the first frame
@ti.kernel
def init(p : vec2):
    for i in range(i_next[None], i_next[None] + n):
        x[i % N] = p
        v[i % N] = v_init * rand_dir()
    i_next[None] += n

# very simple main loop that updates particles and draws them as streaks
gui = ti.GUI("particles", res=(width, height))

init(vec2(0.5, 0.5))
while gui.running:
    if gui.get_event((ti.GUI.PRESS, ti.GUI.LMB)):
        init(vec2(gui.get_cursor_pos()))
    update()
    gui.lines(begin=x_prev.to_numpy(), end=x.to_numpy(), radius=2, color=0xffffff)
    gui.show()

