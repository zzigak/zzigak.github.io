import taichi as ti
import taichi.math as tm
import numpy as np

ti.init(arch=ti.cpu)

# type aliases
vec2 = tm.vec2

width = 800
height = 800
g = vec2(0.0, -1.0)
k_v = .01

N = 20

k_s = 1000*N
k_d = 0.01
k_b = 1
stepsize = 1/6000

# Rope starts out horizontal
particle_posns = np.array([
    0.5 + 0.5 * np.arange(N) / N,
    0.75 * np.ones(N)
], dtype=np.float32).T

# left end is pinned in place
pins = [0]

# masses
particle_masses = 5 * np.ones(N, dtype=np.float32) / N
particle_masses[-1] *= 5

# System of Newtonian particles: mass, position, velocity
m = ti.field(dtype=float, shape=N)
x = ti.Vector.field(2, dtype=float, shape=N)
v = ti.Vector.field(2, dtype=float, shape=N)

# previous position, for drawing
x_prev = ti.Vector.field(2, dtype=float, shape=N)

# initialize all the fields from scene data above
m.from_numpy(particle_masses)
x.from_numpy(particle_posns)
    
@ti.kernel
def init():
    for i in v:
        v[i] = vec2(0)

# Taichi field to hold the forces as they are accumulated
forces = ti.Vector.field(2, dtype=float, shape=N)

ns = int((1/60) // stepsize)
dt = (1/60) / ns
@ti.kernel
def update():

    for i in x:
        x_prev[i] = x[i]
        x[i] = x[i] + dt * v[i]
        forces[i] = vec2(0)

    for i in x:
        forces[i] += g * m[i]
        forces[i] -= k_v * v[i]
        if i < N-1:
            spring_offset = x[i+1] - x[i]
            l = tm.length(spring_offset)
            spring_dir = tm.normalize(spring_offset)
            f = k_s * (l - (0.5/N)) * spring_dir
            f += k_d * k_s * (v[i+1] - v[i]).dot(spring_dir) * spring_dir
            forces[i] += f
            forces[i+1] -= f
        if 1 <= i < N-1:
            x12, x23 = x[i] - x[i-1], x[i+1] - x[i]
            l12, l23 = tm.length(x12), tm.length(x23)
            x12hat, x23hat = x12 / l12, x23 / l23
            f1 = k_b / (2*l12) * (x23hat.dot(x12hat) * x12hat - x23hat)
            f3 = k_b / (2*l23) * (x12hat - x12hat.dot(x23hat) * x23hat)
            f2 = -(f1 + f3)
            forces[i-1] += f1
            forces[i] += f2
            forces[i+1] += f3

    for i in v:
        v[i] = v[i] + dt * forces[i] / m[i]

    for i in ti.static(pins):
        v[i] = vec2(0)


init()

gui = ti.GUI("particles", res=(width, height))
while gui.running:
    # print(x[0], forces[0], x[1], forces[1])
    for k in range(ns):
        update()
    xa = x.to_numpy()
    xpa = x_prev.to_numpy()
    xma = (xa + xpa) / 2
    gui.lines(begin=xma[:-1], end=xma[1:], radius=2, color=0x888888)
    gui.lines(begin=xpa, end=xa, radius=4, color=0xffffcc)
    gui.show()
