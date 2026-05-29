import taichi as ti
import numpy as np
import math
import os
import sys
from taichi.tools.video import VideoManager

if sys.platform == "darwin":
    ti.init(arch=ti.metal, default_fp=ti.f32)
else:
    ti.init(arch=ti.cuda, default_fp=ti.f32)

# -----------------------------------------------------------
                                        
# -----------------------------------------------------------
import numpy as np  # Only for validation, NOT Taichi computation!
quality = 1
n_grid = 128 * quality
dx, inv_dx = 1.0 / n_grid, float(n_grid)
dt = 1e-4 / quality
substeps_per_frame = int(1e-2 // dt)  # 100 sub-steps approx. 0.01 s / frame
# -----------------------------------------------------------
#  Materials
# -----------------------------------------------------------
SNOW = 0
LIQUID = 1
N_MATERIALS = 2

rho_material = ti.field(dtype=ti.f32, shape=N_MATERIALS)
rho_material[SNOW] = 3.0
rho_material[LIQUID] = 1.0

E, nu = 5e3, 0.2
mu_0, lambda_0 = E / (2 * (1 + nu)), E * nu / ((1 + nu)*(1 - 2 * nu))

p_vol = (dx * 0.5) ** 2
material_mass = ti.field(dtype=ti.f32, shape=N_MATERIALS)
for i in range(N_MATERIALS):
    material_mass[i] = p_vol * rho_material[i]

# -----------------------------------------------------------
#  Fields
# -----------------------------------------------------------
n_particles = 16000
x = ti.Vector.field(2, dtype=ti.f32, shape=n_particles)
v = ti.Vector.field(2, dtype=ti.f32, shape=n_particles)
C = ti.Matrix.field(2, 2, dtype=ti.f32, shape=n_particles)
F = ti.Matrix.field(2, 2, dtype=ti.f32, shape=n_particles)
material = ti.field(dtype=ti.i32, shape=n_particles)
Jp = ti.field(dtype=ti.f32, shape=n_particles)  # Only used for snow plasticity

grid_v = ti.Vector.field(2, dtype=ti.f32, shape=(n_grid, n_grid))
grid_m = ti.field(dtype=ti.f32, shape=(n_grid, n_grid))
gravity = ti.Vector.field(2, dtype=ti.f32, shape=())
gravity[None] = ti.Vector([0.0, -9.8])

# -----------------------------------------------------------
#  Circular Obstacles (static pillars)
# -----------------------------------------------------------
n_obstacles = 2
obstacle_centers = ti.Vector.field(2, dtype=ti.f32, shape=n_obstacles)
obstacle_radii = ti.field(dtype=ti.f32, shape=n_obstacles)
obstacle_radii.from_numpy(np.array([0.08, 0.08], np.float32))
friction_coeff_obst = 0.4

# -----------------------------------------------------------
#  Rotating Rigid Fan (5 blades)
# -----------------------------------------------------------
fan_center = ti.Vector.field(2, dtype=ti.f32, shape=())
fan_radius = ti.field(dtype=ti.f32, shape=())
fan_omega = ti.field(dtype=ti.f32, shape=())  # angular velocity
fan_theta = ti.field(dtype=ti.f32, shape=())  # current angle

# -----------------------------------------------------------
#  Initialization Kernel
# -----------------------------------------------------------
@ti.kernel
def reset():
    # Set fixed size/property parameters
    fan_radius[None] = 0.15
    fan_omega[None] = 30.0  # rad / s
    fan_theta[None] = 0.0

    # Fan centered below the two circles
    fan_center[None][0] = 0.5
    fan_center[None][1] = 0.25

    # Two circles below the top blocks, slightly closer together
    obstacle_centers[0][0] = 0.40
    obstacle_centers[0][1] = 0.50
    obstacle_centers[1][0] = 0.60
    obstacle_centers[1][1] = 0.50

    # Particle blocks at top-left and top-right
    snow_width = 0.28
    snow_height = 0.18
    snow_left = 0.12
    snow_bottom = 0.7

    liquid_width = 0.28
    liquid_height = 0.18
    liquid_left = 0.6
    liquid_bottom = 0.7

    # Snow (left top)
    for i in range(n_particles // 2):
        material[i] = SNOW
        x[i] = [snow_left + ti.random() * snow_width, snow_bottom + ti.random() * snow_height]
        v[i] = [0.0, -0.5]
        F[i] = ti.Matrix.identity(ti.f32, 2)
        C[i] = ti.Matrix.zero(ti.f32, 2, 2)
        Jp[i] = 1.0

    # Liquid (right top)
    for i in range(n_particles // 2, n_particles):
        material[i] = LIQUID
        x[i] = [liquid_left + ti.random() * liquid_width, liquid_bottom + ti.random() * liquid_height]
        v[i] = [0.0, -0.5]
        F[i] = ti.Matrix.identity(ti.f32, 2)
        C[i] = ti.Matrix.zero(ti.f32, 2, 2)
        Jp[i] = 1.0


# -----------------------------------------------------------
#  Substep Kernel
# -----------------------------------------------------------
@ti.kernel
def substep():
    # 1. Clear grid
    for I in ti.grouped(grid_m):
        grid_v[I] = ti.Vector.zero(ti.f32, 2)
        grid_m[I] = 0.0

    # 2. P2G
    for p in x:
        # Update deformation gradient
        F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * C[p]) @ F[p]

        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(float)
        w = [0.5 * (1.5 - fx) ** 2,
             0.75 - (fx - 1.0) ** 2,
             0.5 * (fx - 0.5) ** 2]

        # Material-specific constitutive model
        mat = material[p]
        stress = ti.Matrix.zero(ti.f32, 2, 2)

        if mat == SNOW:
            h = ti.max(0.1, ti.min(5.0, ti.exp(10 * (1.0 - Jp[p]))))
            mu, la = mu_0 * h, lambda_0 * h
            U, sig, V = ti.svd(F[p])
            J = 1.0
            for d in ti.static(range(2)):
                new_sig = ti.math.clamp(sig[d, d], 1 - 2.5e-2, 1 + 4.5e-3)
                Jp[p] *= sig[d, d] / new_sig
                sig[d, d] = new_sig
                J *= new_sig
            F[p] = U @ sig @ V.transpose()
            stress = 2 * mu * (F[p] - U @ V.transpose()) @ F[p].transpose() +\
                     ti.Matrix.identity(ti.f32, 2) * la * J * (J - 1)
        else:  # LIQUID
            mu, la = 0.0, lambda_0
            U, sig, V = ti.svd(F[p])
            J = 1.0
            for d in ti.static(range(2)):
                J *= sig[d, d]
            # Reset shear
            F[p] = ti.Matrix.identity(ti.f32, 2) * ti.sqrt(J)
            stress = ti.Matrix.identity(ti.f32, 2) * la * J * (J - 1)

        mass = material_mass[mat]
        stress_term = (-dt * p_vol * 4 * inv_dx * inv_dx) * stress
        affine = stress_term + mass * C[p]

        for i, j in ti.static(ti.ndrange(3, 3)):
            dpos = (ti.Vector([i, j]).cast(float) - fx) * dx
            weight = w[i][0] * w[j][1]
            grid_v[base + ti.Vector([i, j])] += weight * (mass * v[p] + affine @ dpos)
            grid_m[base + ti.Vector([i, j])] += weight * mass

    # 3. Grid operations (gravity, boundaries, obstacles, fan)
    for I in ti.grouped(grid_m):
        if grid_m[I] > 0:
            grid_v[I] = grid_v[I] / grid_m[I]
            grid_v[I] += dt * gravity[None]

            # Domain boundaries
            if I[0] < 3 and grid_v[I][0] < 0: grid_v[I][0] = 0
            if I[0] > n_grid - 3 and grid_v[I][0] > 0: grid_v[I][0] = 0
            if I[1] < 3 and grid_v[I][1] < 0: grid_v[I][1] = 0
            if I[1] > n_grid - 3 and grid_v[I][1] > 0: grid_v[I][1] = 0

            pos = I.cast(float) * dx  # grid node world‐space position

            # Obstacle collisions (circular pillars)
            for k in ti.static(range(n_obstacles)):
                rel = pos - obstacle_centers[k]
                if rel.norm_sqr() < (obstacle_radii[k] + dx) ** 2:
                    n_vec = rel.normalized(1e-8)
                    v_in = grid_v[I]
                    vn = v_in.dot(n_vec)
                    if vn < 0:
                        vt = v_in - vn * n_vec
                        vt_norm = vt.norm()
                        if vt_norm > 1e-8:
                            vt_new = ti.max(0.0, vt_norm + vn * friction_coeff_obst) * (vt / vt_norm)
                            grid_v[I] = vt_new
                        else:
                            grid_v[I] = ti.Vector.zero(ti.f32, 2)

            # Fan collision (five blades)
            rel_fan = pos - fan_center[None]
            for b in ti.static(range(5)):
                phi = fan_theta[None] + 2.0 * math.pi * b / 5.0
                dir_b = ti.Vector([ti.cos(phi), ti.sin(phi)])
                proj = rel_fan.dot(dir_b)
                if 0 <= proj <= fan_radius[None]:
                    perp = rel_fan - dir_b * proj
                    d = perp.norm()
                    if d < dx:
                        n_vec = perp / (d + 1e-6)
                        v_surface = ti.Vector([-fan_omega[None] * rel_fan.y,
                                               fan_omega[None] * rel_fan.x])
                        v_rel = grid_v[I] - v_surface
                        vn = v_rel.dot(n_vec)
                        if vn < 0:
                            vt = v_rel - vn * n_vec
                            mu_f = 0.1
                            vt_norm = vt.norm()
                            vt_new = ti.max(0.0, vt_norm + vn * mu_f) * (vt / (vt_norm + 1e-6))
                            grid_v[I] = v_surface + vt_new

    # 4. G2P
    for p in x:
        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(float)
        w = [0.5 * (1.5 - fx) ** 2,
             0.75 - (fx - 1.0) ** 2,
             0.5 * (fx - 0.5) ** 2]
        new_v = ti.Vector.zero(ti.f32, 2)
        new_C = ti.Matrix.zero(ti.f32, 2, 2)
        for i, j in ti.static(ti.ndrange(3, 3)):
            dpos = ti.Vector([i, j]).cast(float) - fx
            weight = w[i][0] * w[j][1]
            g_v = grid_v[base + ti.Vector([i, j])]
            new_v += weight * g_v
            new_C += 4 * inv_dx * weight * g_v.outer_product(dpos)
        v[p], C[p] = new_v, new_C
        x[p] += dt * v[p]

        # Simple particle‐fan positional correction (keep outside blades)
        rel_p = x[p] - fan_center[None]
        for b in ti.static(range(5)):
            phi = fan_theta[None] + 2.0 * math.pi * b / 5.0
            dir_b = ti.Vector([ti.cos(phi), ti.sin(phi)])
            proj = rel_p.dot(dir_b)
            if 0 <= proj <= fan_radius[None]:
                perp = rel_p - dir_b * proj
                d = perp.norm()
                if d < 0.5 * dx:
                    n_vec = perp / (d + 1e-6)
                    x[p] = fan_center[None] + dir_b * proj + n_vec * 0.5 * dx
                    vn = v[p].dot(n_vec)
                    if vn < 0:
                        v[p] -= (1.0 + 0.0) * vn * n_vec  # perfectly inelastic along normal

    # 5. Advance fan rotation
    fan_theta[None] += fan_omega[None] * dt


# -----------------------------------------------------------
#  Main Loop
# -----------------------------------------------------------
reset()

# Output dirs
output_dir = "mixed_snow_water_fan_output"
os.makedirs(output_dir, exist_ok=True)
video_manager = VideoManager(output_dir=output_dir,
                             framerate=30,
                             automatic_build=False)

gui = ti.GUI("Snow & Water Mixing with Fan", res=512,
             background_color=0x000000, show_gui=False)

frame = 0
max_frames = 300
prev_visible = n_particles

try:
    while gui.running and frame < max_frames:
        for s in range(substeps_per_frame):
            substep()

        gui.clear(0x000000)
        # Draw obstacles
        gui.circles(obstacle_centers.to_numpy(),
                    radius=(obstacle_radii.to_numpy() * gui.res[0]).astype(np.int32),
                    color=0xFF4500)

        # Draw fan blades
        center_np = fan_center[None].to_numpy()
        theta_val = fan_theta[None]
        rad_val = fan_radius[None]
        for b in range(5):
            phi = theta_val + 2 * math.pi * b / 5
            start = tuple(center_np)
            end = tuple(center_np + np.array([math.cos(phi), math.sin(phi)], np.float32) * rad_val)
            gui.line(begin=start, end=end, radius=2, color=0xFFD700)

        # Draw particles
        palette = np.array([0xFFFFFF, 0x4169E1], dtype=np.uint32)
        gui.circles(x.to_numpy(), radius=2,
                    palette=palette,
                    palette_indices=material.to_numpy())

        video_manager.write_frame(gui.get_image())
        if frame % 30 == 0:
            print(f"Recording frame {frame}/{max_frames}")
        gui.show()
        frame += 1

except RuntimeError as e:
    print("Simulation halted:", e)

finally:
    print("Building video...")
    video_manager.make_video(gif=False, mp4=True)
    print(f"Video saved to {output_dir}")