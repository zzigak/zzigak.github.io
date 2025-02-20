import taichi as ti
import numpy as np
from taichi.math import vec3

# Initialize Taichi
ti.init(arch=ti.gpu)

# Load OBJ file
def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vertex
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):  # Face
                faces.append([int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]])
    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32)

# Load the OBJ file
vertices, faces = load_obj('stanford-bunny.obj')
num_vertices = len(vertices)
num_faces = len(faces)

# Taichi fields
pos = ti.Vector.field(3, dtype=ti.f32, shape=num_vertices)
vel = ti.Vector.field(3, dtype=ti.f32, shape=num_vertices)
rest_pos = ti.Vector.field(3, dtype=ti.f32, shape=num_vertices)
faces_ti = ti.field(ti.i32, shape=num_faces * 3)  # Flattened faces array
springs = ti.field(ti.i32, shape=(num_faces * 3, 2))  # Each face contributes 3 springs

# Ground mesh fields
ground_pos = ti.Vector.field(3, dtype=ti.f32, shape=4)
ground_indices = ti.field(ti.i32, shape=6)  # 2 triangles, 3 vertices each

# Parameters
dt = 0.01
gravity = vec3(0, -9.8, 0)
spring_stiffness = 100.0
damping = 0.1
ground_y = -1.0  # Y position of the ground
restitution = 0.5  # Bounce factor

# Initialize ground mesh
@ti.kernel
def initialize_ground():
    # Set ground vertices
    ground_pos[0] = vec3(-2, ground_y, -2)
    ground_pos[1] = vec3(2, ground_y, -2)
    ground_pos[2] = vec3(2, ground_y, 2)
    ground_pos[3] = vec3(-2, ground_y, 2)
    
    # Set ground indices (two triangles)
    ground_indices[0] = 0
    ground_indices[1] = 1
    ground_indices[2] = 2
    ground_indices[3] = 0
    ground_indices[4] = 2
    ground_indices[5] = 3

# Initialize positions and velocities
@ti.kernel
def initialize():
    for i in range(num_vertices):
        pos[i] = rest_pos[i]
        vel[i] = vec3(0.0)

# Set up springs (edges of the mesh)
@ti.kernel
def setup_springs():
    for i in range(num_faces):
        # Access flattened faces array
        a = faces_ti[i * 3]      # First vertex of the face
        b = faces_ti[i * 3 + 1]  # Second vertex of the face
        c = faces_ti[i * 3 + 2]  # Third vertex of the face
        springs[i * 3, 0] = a
        springs[i * 3, 1] = b
        springs[i * 3 + 1, 0] = b
        springs[i * 3 + 1, 1] = c
        springs[i * 3 + 2, 0] = c
        springs[i * 3 + 2, 1] = a

# Ground collision handling
@ti.kernel
def handle_ground_collision():
    for i in range(num_vertices):
        if pos[i].y < ground_y:
            pos[i].y = ground_y
            if vel[i].y < 0:
                vel[i].y = -vel[i].y * restitution
                # Add friction when hitting the ground
                vel[i].x *= 0.9
                vel[i].z *= 0.9

# Simulation step
@ti.kernel
def step():
    # Apply forces and update positions
    for i in range(num_vertices):
        # Apply gravity
        vel[i] += gravity * dt
        # Damping
        vel[i] *= (1 - damping)
        # Update position
        pos[i] += vel[i] * dt

    # Apply spring forces
    for i in range(springs.shape[0]):
        a, b = springs[i, 0], springs[i, 1]
        delta = pos[a] - pos[b]
        length = delta.norm()
        rest_length = (rest_pos[a] - rest_pos[b]).norm()
        force = -spring_stiffness * (length - rest_length) * delta.normalized()
        vel[a] += force * dt
        vel[b] -= force * dt

# Main function
def main():
    # Load rest positions
    rest_pos.from_numpy(vertices)
    # Load faces into flattened Taichi field
    faces_ti.from_numpy(faces.flatten())
    initialize()
    setup_springs()
    initialize_ground()

    # GUI setup
    window = ti.ui.Window("Spring-Mass System with Ground", (800, 600))
    canvas = window.get_canvas()
    scene = window.get_scene()  # Use window.get_scene() instead of ti.ui.Scene()
    camera = ti.ui.Camera()
    camera.position(0, 0, 3)
    camera.lookat(0, 0, 0)

    while window.running:
        step()
        handle_ground_collision()

        # Render
        camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
        scene.set_camera(camera)
        scene.point_light(pos=(0, 1, 2), color=(1, 1, 1))
        
        # Render ground
        scene.mesh(ground_pos, indices=ground_indices, color=(0.3, 0.5, 0.3))
        
        # Render bunny
        scene.mesh(pos, indices=faces_ti, color=(0.5, 0.5, 0.5))
        
        canvas.scene(scene)
        window.show()

if __name__ == "__main__":
    main()