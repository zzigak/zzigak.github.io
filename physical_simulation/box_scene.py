import numpy as np

# Scene to go with mass_and_spring.py

N = 4
k_s = 100
k_d = 0.05
stepsize = 1/600

particle_posns = np.array([
    [0.4, 0.4],
    [0.6, 0.4],
    [0.6, 0.6],
    [0.4, 0.6]
], dtype=np.float32)
pins = []

spring_indices = np.array([
    [0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1,3]
], dtype=np.int32)

spring_params = np.array([
    [1.0*k_s, 1.0*k_d, 0.0],
    [1.0*k_s, 1.0*k_d, 0.0],
    [1.0*k_s, 1.0*k_d, 0.0],
    [1.0*k_s, 1.0*k_d, 0.0],
    [0.5*k_s, 1.0*k_d, 0.0],
    [0.5*k_s, 1.0*k_d, 0.0],
], dtype=np.float32)

particle_masses = np.ones(N, dtype=np.float32)
nSprings = len(spring_indices)

vel_noise = 0.5