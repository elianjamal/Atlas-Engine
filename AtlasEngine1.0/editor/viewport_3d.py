#!/usr/bin/env python3
"""
AtlasEngine - 3D Viewport
Custom 3D rendering with shapes, physics, and first-person game mode
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import List, Tuple, Dict, Optional

class Vector3D:
    """3D Vector for viewport"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector3D(self.x/length, self.y/length, self.z/length)
        return Vector3D(0, 0, 0)
    
    def copy(self):
        return Vector3D(self.x, self.y, self.z)


class Shape3D:
    """Base class for 3D shapes"""
    def __init__(self, position: Vector3D, size: float = 1.0):
        self.position = position
        self.size = size
        self.scale = Vector3D(1.0, 1.0, 1.0)  # Non-uniform scale
        self.rotation = Vector3D(0, 0, 0)  # Euler angles in degrees
        self.velocity = Vector3D(0, 0, 0)
        self.angular_velocity = Vector3D(0, 0, 0)  # For rolling
        self.color = "#00ff00"
        self.has_physics = False
        self.is_static = False
        self.on_ground = False
        self.has_collision = False  # Player can collide with this
        self.is_rolling = False  # For spheres
        self.mass = 1.0  # Mass for physics
        self.friction = 0.5  # Surface friction
        self.restitution = 0.3  # Bounciness (0-1)
    
    def get_vertices(self) -> List[Vector3D]:
        """Override in subclasses"""
        return []
    
    def get_edges(self) -> List[Tuple[int, int]]:
        """Override in subclasses"""
        return []


class Cube(Shape3D):
    """Cube shape"""
    def get_vertices(self):
        # Apply non-uniform scale to base size
        sx = self.size * self.scale.x / 2
        sy = self.size * self.scale.y / 2
        sz = self.size * self.scale.z / 2
        
        vertices = [
            Vector3D(-sx, -sy, -sz), Vector3D(sx, -sy, -sz),
            Vector3D(sx, sy, -sz), Vector3D(-sx, sy, -sz),
            Vector3D(-sx, -sy, sz), Vector3D(sx, -sy, sz),
            Vector3D(sx, sy, sz), Vector3D(-sx, sy, sz)
        ]
        
        # Apply rotation
        rotated = []
        for v in vertices:
            rotated.append(self.rotate_vertex(v))
        
        # Apply position
        return [Vector3D(v.x + self.position.x, 
                        v.y + self.position.y, 
                        v.z + self.position.z) for v in rotated]
    
    def get_edges(self):
        return [
            (0,1), (1,2), (2,3), (3,0),  # Back face
            (4,5), (5,6), (6,7), (7,4),  # Front face
            (0,4), (1,5), (2,6), (3,7)   # Connecting edges
        ]
    
    def rotate_vertex(self, v: Vector3D) -> Vector3D:
        """Rotate vertex by rotation angles"""
        # Rotate around X
        rx = math.radians(self.rotation.x)
        y = v.y * math.cos(rx) - v.z * math.sin(rx)
        z = v.y * math.sin(rx) + v.z * math.cos(rx)
        v = Vector3D(v.x, y, z)
        
        # Rotate around Y
        ry = math.radians(self.rotation.y)
        x = v.x * math.cos(ry) + v.z * math.sin(ry)
        z = -v.x * math.sin(ry) + v.z * math.cos(ry)
        v = Vector3D(x, v.y, z)
        
        # Rotate around Z
        rz = math.radians(self.rotation.z)
        x = v.x * math.cos(rz) - v.y * math.sin(rz)
        y = v.x * math.sin(rz) + v.y * math.cos(rz)
        
        return Vector3D(x, y, v.z)


class Plane(Shape3D):
    """Plane/ground shape"""
    def __init__(self, position: Vector3D, size: float = 10.0):
        super().__init__(position, size)
        self.color = "#666666"
        self.is_static = True
    
    def get_vertices(self):
        s = self.size
        return [
            Vector3D(self.position.x - s, self.position.y, self.position.z - s),
            Vector3D(self.position.x + s, self.position.y, self.position.z - s),
            Vector3D(self.position.x + s, self.position.y, self.position.z + s),
            Vector3D(self.position.x - s, self.position.y, self.position.z + s)
        ]
    
    def get_edges(self):
        return [(0,1), (1,2), (2,3), (3,0),
                (0,2), (1,3)]  # Diagonals for grid


class Sphere(Shape3D):
    """Sphere shape (approximated with vertices)"""
    def __init__(self, position: Vector3D, size: float = 1.0):
        super().__init__(position, size)
        self.segments = 12
        self.is_rolling = True  # Spheres can roll
        self.color = "#ff8800"
    
    def get_vertices(self):
        vertices = []
        radius = self.size / 2
        
        for i in range(self.segments):
            theta = (i / self.segments) * 2 * math.pi
            for j in range(self.segments):
                phi = (j / self.segments) * math.pi
                
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                
                vertices.append(Vector3D(
                    x + self.position.x,
                    y + self.position.y,
                    z + self.position.z
                ))
        
        return vertices
    
    def get_edges(self):
        edges = []
        for i in range(self.segments - 1):
            for j in range(self.segments):
                current = i * self.segments + j
                next_ring = (i + 1) * self.segments + j
                next_segment = i * self.segments + ((j + 1) % self.segments)
                
                edges.append((current, next_ring))
                edges.append((current, next_segment))
        
        return edges


class Camera:
    """3D Camera for viewport"""
    def __init__(self):
        self.position = Vector3D(0, 3, -10)
        self.rotation = Vector3D(0, 0, 0)
        self.fov = 60
        self.near = 0.1
        self.far = 100
        
        # First-person mode
        self.is_first_person = False
        self.yaw = 0.0
        self.pitch = 0.0


class Viewport3D:
    """3D Viewport with rendering and game engine"""
    
    MODE_TRAJECTORY = "trajectory"
    MODE_GAME = "game"
    
    def __init__(self, parent, editor):
        self.editor = editor
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        
        # Scene data
        self.shapes: List[Shape3D] = []
        self.camera = Camera()
        self.selected_shape: Optional[Shape3D] = None
        
        # Physics
        self.physics_enabled = False
        self.gravity = -9.81
        self.dt = 0.016  # ~60 FPS
        
        # Player
        self.player: Optional[Cube] = None
        self.player_speed = 5.0
        self.player_controls_enabled = False
        
        # Mode
        self.mode = self.MODE_TRAJECTORY
        
        # Input state (MUST be before UI setup)
        self.keys_pressed = set()
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_dragging = False
        self.middle_mouse_dragging = False
        self.camera_speed = 0.5  # Units per frame
        self.zoom_speed = 0.5
        
        # Gizmo state for object manipulation
        self.gizmo_visible = False
        self.gizmo_mode = 'translate'  # 'translate', 'rotate', 'scale'
        self.active_axis = None  # 'x', 'y', 'z', or None
        self.drag_start_pos = None
        self.drag_start_object_pos = None
        
        # Clipboard for copy/paste
        self.clipboard_object = None
        
        # Animation
        self.animation_running = False
        
        # UI (after all attributes are initialized)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup viewport UI"""
        # Top toolbar
        toolbar = tk.Frame(self.frame, bg="#252526", height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # Mode selector
        tk.Label(toolbar, text="Mode:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value=self.MODE_TRAJECTORY)
        mode_combo = ttk.Combobox(toolbar, textvariable=self.mode_var, 
                                  values=[self.MODE_TRAJECTORY, self.MODE_GAME],
                                  state='readonly', width=12)
        mode_combo.pack(side=tk.LEFT, padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # Add shape buttons
        tk.Label(toolbar, text="Add:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        tk.Button(toolbar, text="Cube", command=self.add_cube,
                 bg="#0e639c", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=2)
        
        tk.Button(toolbar, text="Sphere", command=self.add_sphere,
                 bg="#0e639c", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=2)
        
        tk.Button(toolbar, text="Plane", command=self.add_plane,
                 bg="#0e639c", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=2)
        
        # Physics button
        self.physics_btn = tk.Button(toolbar, text="▶ Physics", command=self.toggle_physics,
                                     bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=10)
        self.physics_btn.pack(side=tk.LEFT, padx=(20,2))
        
        # Player button
        self.player_btn = tk.Button(toolbar, text="+ Player", command=self.add_player,
                                    bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=10)
        self.player_btn.pack(side=tk.LEFT, padx=2)
        
        # Gizmo mode buttons
        tk.Label(toolbar, text="Gizmo:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        self.gizmo_translate_btn = tk.Button(toolbar, text="Move", command=lambda: self.set_gizmo_mode('translate'),
                                            bg="#0e639c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_translate_btn.pack(side=tk.LEFT, padx=2)
        
        self.gizmo_rotate_btn = tk.Button(toolbar, text="Rotate", command=lambda: self.set_gizmo_mode('rotate'),
                                         bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_rotate_btn.pack(side=tk.LEFT, padx=2)
        
        self.gizmo_scale_btn = tk.Button(toolbar, text="Scale", command=lambda: self.set_gizmo_mode('scale'),
                                        bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_scale_btn.pack(side=tk.LEFT, padx=2)
        
        # Collision toggle button
        tk.Label(toolbar, text="Physics:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        self.collision_btn = tk.Button(toolbar, text="🛡️ Collision", command=self.toggle_collision,
                                      bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.collision_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear button
        tk.Button(toolbar, text="Clear", command=self.clear_scene,
                 bg="#c24545", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=2)
        
        # Help/Controls info
        tk.Label(toolbar, text="[WASD+QE: Move] [Arrows: Rotate/Look] [Wheel: Zoom]", 
                bg="#252526", fg="#888888", font=("Consolas", 8)).pack(side=tk.RIGHT, padx=10)
        
        # Canvas for 3D rendering
        canvas_frame = tk.Frame(self.frame, bg="#2b2b2b")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Property panel (bottom)
        prop_frame = tk.Frame(self.frame, bg="#252526", height=120)
        prop_frame.pack(fill=tk.X, padx=5, pady=5)
        prop_frame.pack_propagate(False)
        
        tk.Label(prop_frame, text="PROPERTIES", bg="#252526", fg="#cccccc",
                font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        # Transform controls
        controls = tk.Frame(prop_frame, bg="#252526")
        controls.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Position
        pos_frame = tk.Frame(controls, bg="#252526")
        pos_frame.pack(fill=tk.X, pady=2)
        tk.Label(pos_frame, text="Position:", bg="#252526", fg="#cccccc", width=10).pack(side=tk.LEFT)
        
        self.pos_x_var = tk.StringVar(value="0.0")
        self.pos_y_var = tk.StringVar(value="0.0")
        self.pos_z_var = tk.StringVar(value="0.0")
        
        for label, var in [("X:", self.pos_x_var), ("Y:", self.pos_y_var), ("Z:", self.pos_z_var)]:
            tk.Label(pos_frame, text=label, bg="#252526", fg="#888888").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(pos_frame, textvariable=var, width=8, bg="#3c3c3c", fg="white")
            entry.pack(side=tk.LEFT, padx=2)
            entry.bind('<Return>', self.update_transform)
        
        # Rotation
        rot_frame = tk.Frame(controls, bg="#252526")
        rot_frame.pack(fill=tk.X, pady=2)
        tk.Label(rot_frame, text="Rotation:", bg="#252526", fg="#cccccc", width=10).pack(side=tk.LEFT)
        
        self.rot_x_var = tk.StringVar(value="0.0")
        self.rot_y_var = tk.StringVar(value="0.0")
        self.rot_z_var = tk.StringVar(value="0.0")
        
        for label, var in [("X:", self.rot_x_var), ("Y:", self.rot_y_var), ("Z:", self.rot_z_var)]:
            tk.Label(rot_frame, text=label, bg="#252526", fg="#888888").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(rot_frame, textvariable=var, width=8, bg="#3c3c3c", fg="white")
            entry.pack(side=tk.LEFT, padx=2)
            entry.bind('<Return>', self.update_transform)
        
        # Scale
        scale_frame = tk.Frame(controls, bg="#252526")
        scale_frame.pack(fill=tk.X, pady=2)
        tk.Label(scale_frame, text="Scale:", bg="#252526", fg="#cccccc", width=10).pack(side=tk.LEFT)
        
        self.scale_x_var = tk.StringVar(value="1.0")
        self.scale_y_var = tk.StringVar(value="1.0")
        self.scale_z_var = tk.StringVar(value="1.0")
        
        for label, var in [("X:", self.scale_x_var), ("Y:", self.scale_y_var), ("Z:", self.scale_z_var)]:
            tk.Label(scale_frame, text=label, bg="#252526", fg="#888888").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(scale_frame, textvariable=var, width=6, bg="#3c3c3c", fg="white")
            entry.pack(side=tk.LEFT, padx=2)
            entry.bind('<Return>', self.update_transform)
        
        # Uniform size (kept for compatibility)
        size_frame = tk.Frame(controls, bg="#252526")
        size_frame.pack(fill=tk.X, pady=2)
        tk.Label(size_frame, text="Uniform:", bg="#252526", fg="#cccccc", width=10).pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar(value="1.0")
        entry = tk.Entry(size_frame, textvariable=self.size_var, width=8, bg="#3c3c3c", fg="white")
        entry.pack(side=tk.LEFT, padx=2)
        entry.bind('<Return>', self.update_transform)
        tk.Label(size_frame, text="(scales all axes)", bg="#252526", fg="#666666", 
                font=("Consolas", 8)).pack(side=tk.LEFT, padx=5)
        
        # Collision checkbox
        collision_frame = tk.Frame(controls, bg="#252526")
        collision_frame.pack(fill=tk.X, pady=2)
        tk.Label(collision_frame, text="Collision:", bg="#252526", fg="#cccccc", width=10).pack(side=tk.LEFT)
        
        self.collision_var = tk.BooleanVar(value=False)
        self.collision_check = tk.Checkbutton(collision_frame, text="Enable player collision", 
                                             variable=self.collision_var, command=self.update_collision,
                                             bg="#252526", fg="#cccccc", selectcolor="#1e1e1e",
                                             activebackground="#252526", activeforeground="#cccccc")
        self.collision_check.pack(side=tk.LEFT, padx=2)
        
        # Bind events
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)  # Windows/Mac
        self.canvas.bind('<Button-4>', self.on_mouse_wheel)    # Linux scroll up
        self.canvas.bind('<Button-5>', self.on_mouse_wheel)    # Linux scroll down
        
        # Middle mouse button for panning
        self.canvas.bind('<Button-2>', self.on_middle_mouse_down)
        self.canvas.bind('<B2-Motion>', self.on_middle_mouse_drag)
        self.canvas.bind('<ButtonRelease-2>', self.on_middle_mouse_up)
        
        # Keyboard for camera control and game mode
        self.canvas.bind('<KeyPress>', self.on_key_press)
        self.canvas.bind('<KeyRelease>', self.on_key_release)
        self.canvas.focus_set()
        
        # Initial render
        self.width = 800
        self.height = 600
        self.render()
        
        # Start camera update loop after window is ready (delayed start)
        self.canvas.after(100, self.update_camera_movement)
    
    def on_mode_change(self, event=None):
        """Handle mode change"""
        new_mode = self.mode_var.get()
        self.mode = new_mode
        
        if new_mode == self.MODE_GAME:
            self.editor.log("Switched to GAME mode", "success")
            self.canvas.config(cursor="cross")
            self.canvas.focus_set()
        else:
            self.editor.log("Switched to TRAJECTORY mode", "info")
            self.canvas.config(cursor="")
            self.player_controls_enabled = False
        
        self.render()
    
    def set_gizmo_mode(self, mode):
        """Set the gizmo transformation mode"""
        self.gizmo_mode = mode
        
        # Update button colors
        self.gizmo_translate_btn.config(bg="#3c3c3c")
        self.gizmo_rotate_btn.config(bg="#3c3c3c")
        self.gizmo_scale_btn.config(bg="#3c3c3c")
        
        if mode == 'translate':
            self.gizmo_translate_btn.config(bg="#0e639c")
            self.editor.log("Gizmo mode: MOVE (drag XYZ arrows)", "info")
        elif mode == 'rotate':
            self.gizmo_rotate_btn.config(bg="#0e639c")
            self.editor.log("Gizmo mode: ROTATE (drag XYZ arrows)", "info")
        elif mode == 'scale':
            self.gizmo_scale_btn.config(bg="#0e639c")
            self.editor.log("Gizmo mode: SCALE (drag XYZ arrows)", "info")
        
        self.render()
    
    def toggle_collision(self):
        """Toggle collision for selected object"""
        if not self.selected_shape:
            self.editor.log("No object selected! Select an object first.", "warning")
            return
        
        self.selected_shape.has_collision = not self.selected_shape.has_collision
        
        if self.selected_shape.has_collision:
            self.collision_btn.config(bg="#4caf50")
            self.editor.log(f"Collision ENABLED for {type(self.selected_shape).__name__}", "success")
            # Update visual feedback
            if self.selected_shape.color == "#00ff00":
                self.selected_shape.color = "#00ffff"  # Cyan for collision
        else:
            self.collision_btn.config(bg="#3c3c3c")
            self.editor.log(f"Collision DISABLED for {type(self.selected_shape).__name__}", "info")
            # Restore original color
            if isinstance(self.selected_shape, Sphere):
                self.selected_shape.color = "#ff8800"
            elif isinstance(self.selected_shape, Cube):
                self.selected_shape.color = "#00ff00"
        
        self.collision_var.set(self.selected_shape.has_collision)
        self.render()
    
    def update_collision(self):
        """Update collision from checkbox"""
        if self.selected_shape:
            self.selected_shape.has_collision = self.collision_var.get()
            if self.selected_shape.has_collision:
                self.collision_btn.config(bg="#4caf50")
                if self.selected_shape.color == "#00ff00":
                    self.selected_shape.color = "#00ffff"
            else:
                self.collision_btn.config(bg="#3c3c3c")
                if isinstance(self.selected_shape, Sphere):
                    self.selected_shape.color = "#ff8800"
                elif isinstance(self.selected_shape, Cube):
                    self.selected_shape.color = "#00ff00"
            self.render()
    
    def add_cube(self):
        """Add a cube to the scene"""
        cube = Cube(Vector3D(0, 2, 0), 1.0)
        cube.color = "#00ff00"
        self.shapes.append(cube)
        self.selected_shape = cube
        self.update_property_panel()
        self.editor.log(f"Added cube at (0, 2, 0)")
        self.render()
    
    def add_sphere(self):
        """Add a sphere to the scene"""
        sphere = Sphere(Vector3D(2, 3, 0), 1.0)
        sphere.color = "#ff8800"
        self.shapes.append(sphere)
        self.selected_shape = sphere
        self.update_property_panel()
        self.editor.log(f"Added sphere at (2, 3, 0)")
        self.render()
    
    def add_plane(self):
        """Add a plane to the scene"""
        plane = Plane(Vector3D(0, 0, 0), 10.0)
        self.shapes.append(plane)
        self.selected_shape = plane
        self.update_property_panel()
        self.editor.log(f"Added plane at (0, 0, 0)")
        self.render()
    
    def add_player(self):
        """Add player character"""
        if self.player:
            self.editor.log("Player already exists!", "warning")
            return
        
        # Create player cube
        self.player = Cube(Vector3D(0, 2, 0), 1.0)
        self.player.color = "#ff0000"
        self.player.has_physics = True
        self.shapes.append(self.player)
        
        # Enable player controls
        self.player_controls_enabled = True
        
        # Switch to game mode
        self.mode = self.MODE_GAME
        self.mode_var.set(self.MODE_GAME)
        
        # Setup camera for first person
        self.camera.is_first_person = True
        self.camera.position = self.player.position.copy()
        self.camera.position.y += 0.8  # Eye height
        
        self.editor.log("Player added! Use WASD to move, Space to jump", "success")
        self.editor.log("Mouse to look around (click canvas first)")
        
        self.canvas.focus_set()
        self.render()
    
    def toggle_physics(self):
        """Toggle physics simulation"""
        self.physics_enabled = not self.physics_enabled
        
        if self.physics_enabled:
            self.physics_btn.config(text="⏸ Physics", bg="#4caf50")
            self.editor.log("Physics simulation STARTED", "success")
            
            # Enable physics on all non-static shapes
            for shape in self.shapes:
                if not shape.is_static and not isinstance(shape, Plane):
                    shape.has_physics = True
            
            self.start_animation()
        else:
            self.physics_btn.config(text="▶ Physics", bg="#3c3c3c")
            self.editor.log("Physics simulation STOPPED", "warning")
            self.animation_running = False
    
    def clear_scene(self):
        """Clear all shapes"""
        self.shapes.clear()
        self.selected_shape = None
        self.player = None
        self.player_controls_enabled = False
        self.camera.is_first_person = False
        self.update_property_panel()
        self.editor.log("Scene cleared")
        self.render()
    
    def update_property_panel(self):
        """Update property panel with selected shape data"""
        if self.selected_shape:
            self.pos_x_var.set(f"{self.selected_shape.position.x:.2f}")
            self.pos_y_var.set(f"{self.selected_shape.position.y:.2f}")
            self.pos_z_var.set(f"{self.selected_shape.position.z:.2f}")
            
            self.rot_x_var.set(f"{self.selected_shape.rotation.x:.2f}")
            self.rot_y_var.set(f"{self.selected_shape.rotation.y:.2f}")
            self.rot_z_var.set(f"{self.selected_shape.rotation.z:.2f}")
            
            self.scale_x_var.set(f"{self.selected_shape.scale.x:.2f}")
            self.scale_y_var.set(f"{self.selected_shape.scale.y:.2f}")
            self.scale_z_var.set(f"{self.selected_shape.scale.z:.2f}")
            
            self.size_var.set(f"{self.selected_shape.size:.2f}")
            
            # Update collision checkbox and button
            self.collision_var.set(self.selected_shape.has_collision)
            if self.selected_shape.has_collision:
                self.collision_btn.config(bg="#4caf50")
            else:
                self.collision_btn.config(bg="#3c3c3c")
    
    def update_transform(self, event=None):
        """Update selected shape from property panel"""
        if not self.selected_shape:
            return
        
        try:
            self.selected_shape.position.x = float(self.pos_x_var.get())
            self.selected_shape.position.y = float(self.pos_y_var.get())
            self.selected_shape.position.z = float(self.pos_z_var.get())
            
            self.selected_shape.rotation.x = float(self.rot_x_var.get())
            self.selected_shape.rotation.y = float(self.rot_y_var.get())
            self.selected_shape.rotation.z = float(self.rot_z_var.get())
            
            self.selected_shape.scale.x = float(self.scale_x_var.get())
            self.selected_shape.scale.y = float(self.scale_y_var.get())
            self.selected_shape.scale.z = float(self.scale_z_var.get())
            
            self.selected_shape.size = float(self.size_var.get())
            
            self.render()
        except ValueError:
            pass
    
    def project_3d_to_2d(self, point: Vector3D) -> Tuple[float, float]:
        """Project 3D point to 2D screen coordinates"""
        # Simple perspective projection
        
        # Transform to camera space
        rel = Vector3D(
            point.x - self.camera.position.x,
            point.y - self.camera.position.y,
            point.z - self.camera.position.z
        )
        
        # Apply camera rotation
        if self.camera.is_first_person:
            # First-person: use pitch and yaw
            # Rotate around Y (yaw)
            yaw_rad = math.radians(self.camera.yaw)
            x = rel.x * math.cos(yaw_rad) - rel.z * math.sin(yaw_rad)
            z = rel.x * math.sin(yaw_rad) + rel.z * math.cos(yaw_rad)
            rel = Vector3D(x, rel.y, z)
            
            # Rotate around X (pitch)
            pitch_rad = math.radians(self.camera.pitch)
            y = rel.y * math.cos(pitch_rad) - rel.z * math.sin(pitch_rad)
            z = rel.y * math.sin(pitch_rad) + rel.z * math.cos(pitch_rad)
            rel = Vector3D(rel.x, y, z)
        else:
            # Trajectory mode: use rotation.y
            angle = math.radians(self.camera.rotation.y)
            x = rel.x * math.cos(angle) - rel.z * math.sin(angle)
            z = rel.x * math.sin(angle) + rel.z * math.cos(angle)
            rel = Vector3D(x, rel.y, z)
        
        # Perspective divide
        if rel.z > self.camera.near:
            fov_factor = 1.0 / math.tan(math.radians(self.camera.fov / 2))
            
            screen_x = rel.x / rel.z * fov_factor * self.width / 2 + self.width / 2
            screen_y = -rel.y / rel.z * fov_factor * self.height / 2 + self.height / 2
            
            return (screen_x, screen_y)
        
        return None
    
    def render(self):
        """Render the 3D scene"""
        self.canvas.delete("all")
        
        # Draw grid
        self.draw_grid()
        
        # Draw axes
        self.draw_axes()
        
        # Draw all shapes
        for shape in self.shapes:
            self.draw_shape(shape)
        
        # Draw gizmo if object is selected
        if self.selected_shape and self.gizmo_visible and self.mode == self.MODE_TRAJECTORY:
            self.draw_gizmo()
        
        # Draw HUD for game mode
        if self.mode == self.MODE_GAME and self.player:
            self.draw_hud()
        else:
            # Draw camera info in trajectory mode
            self.draw_camera_info()
    
    def draw_grid(self):
        """Draw ground grid"""
        grid_size = 10
        grid_spacing = 1
        
        for i in range(-grid_size, grid_size + 1):
            # Lines parallel to X
            start = Vector3D(i * grid_spacing, 0, -grid_size * grid_spacing)
            end = Vector3D(i * grid_spacing, 0, grid_size * grid_spacing)
            
            p1 = self.project_3d_to_2d(start)
            p2 = self.project_3d_to_2d(end)
            
            if p1 and p2:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                       fill="#333333", width=1)
            
            # Lines parallel to Z
            start = Vector3D(-grid_size * grid_spacing, 0, i * grid_spacing)
            end = Vector3D(grid_size * grid_spacing, 0, i * grid_spacing)
            
            p1 = self.project_3d_to_2d(start)
            p2 = self.project_3d_to_2d(end)
            
            if p1 and p2:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                       fill="#333333", width=1)
    
    def draw_axes(self):
        """Draw XYZ axes"""
        origin = Vector3D(0, 0, 0)
        
        # X axis (red)
        x_end = Vector3D(2, 0, 0)
        p1 = self.project_3d_to_2d(origin)
        p2 = self.project_3d_to_2d(x_end)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                   fill="#ff0000", width=2, arrow=tk.LAST)
        
        # Y axis (green)
        y_end = Vector3D(0, 2, 0)
        p2 = self.project_3d_to_2d(y_end)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                   fill="#00ff00", width=2, arrow=tk.LAST)
        
        # Z axis (blue)
        z_end = Vector3D(0, 0, 2)
        p2 = self.project_3d_to_2d(z_end)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                   fill="#0000ff", width=2, arrow=tk.LAST)
    
    def draw_shape(self, shape: Shape3D):
        """Draw a 3D shape"""
        vertices = shape.get_vertices()
        edges = shape.get_edges()
        
        # Project vertices
        projected = []
        for v in vertices:
            p = self.project_3d_to_2d(v)
            projected.append(p)
        
        # Determine line width and style
        width = 2 if shape == self.selected_shape else 1
        color = shape.color
        
        # Draw collision indicator (dashed lines for collision objects)
        if shape.has_collision:
            dash_pattern = (4, 2)  # Dashed line
        else:
            dash_pattern = ()  # Solid line
        
        # Draw edges
        for edge in edges:
            if edge[0] < len(projected) and edge[1] < len(projected):
                p1 = projected[edge[0]]
                p2 = projected[edge[1]]
                
                if p1 and p2:
                    self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                           fill=color, width=width, dash=dash_pattern)
        
        # Draw collision badge if enabled
        if shape.has_collision and shape != self.selected_shape:
            center = self.project_3d_to_2d(shape.position)
            if center:
                self.canvas.create_text(center[0], center[1] - 30, 
                                       text="🛡️", font=("Arial", 16),
                                       fill="#00ffff")
    
    def draw_hud(self):
        """Draw game mode HUD"""
        # Crosshair
        cx, cy = self.width / 2, self.height / 2
        size = 10
        self.canvas.create_line(cx - size, cy, cx + size, cy,
                               fill="white", width=2)
        self.canvas.create_line(cx, cy - size, cx, cy + size,
                               fill="white", width=2)
        
        # Player info
        if self.player:
            info = f"Position: ({self.player.position.x:.1f}, " \
                   f"{self.player.position.y:.1f}, {self.player.position.z:.1f})"
            self.canvas.create_text(10, 10, text=info, anchor=tk.NW,
                                   fill="white", font=("Consolas", 10))
            
            status = "On Ground" if self.player.on_ground else "In Air"
            self.canvas.create_text(10, 30, text=f"Status: {status}",
                                   anchor=tk.NW, fill="white",
                                   font=("Consolas", 10))
            
            # Camera angle info
            look_info = f"Look: Yaw {self.camera.yaw:.0f}° Pitch {self.camera.pitch:.0f}°"
            self.canvas.create_text(10, 50, text=look_info,
                                   anchor=tk.NW, fill="white",
                                   font=("Consolas", 10))
            
            # Controls reminder
            self.canvas.create_text(10, self.height - 40, 
                                   text="Arrow Keys: Look Around",
                                   anchor=tk.NW, fill="#888888",
                                   font=("Consolas", 9))
            self.canvas.create_text(10, self.height - 20,
                                   text="WASD: Move | Space: Jump",
                                   anchor=tk.NW, fill="#888888",
                                   font=("Consolas", 9))
    
    def draw_camera_info(self):
        """Draw camera position info in trajectory mode"""
        if self.mode == self.MODE_TRAJECTORY:
            cam_info = f"Camera: ({self.camera.position.x:.1f}, " \
                      f"{self.camera.position.y:.1f}, {self.camera.position.z:.1f})"
            self.canvas.create_text(10, 10, text=cam_info, anchor=tk.NW,
                                   fill="#888888", font=("Consolas", 9))
            
            rot_info = f"Rotation: ({self.camera.rotation.x:.0f}°, " \
                      f"{self.camera.rotation.y:.0f}°, {self.camera.rotation.z:.0f}°)"
            self.canvas.create_text(10, 25, text=rot_info, anchor=tk.NW,
                                   fill="#888888", font=("Consolas", 9))
            
            # Object count
            obj_count = f"Objects: {len(self.shapes)}"
            self.canvas.create_text(10, 40, text=obj_count, anchor=tk.NW,
                                   fill="#888888", font=("Consolas", 9))
    
    def on_resize(self, event):
        """Handle canvas resize"""
        self.width = event.width
        self.height = event.height
        self.render()
    
    def on_mouse_down(self, event):
        """Handle mouse down"""
        self.mouse_x = event.x
        self.mouse_y = event.y
        
        # Check if we clicked on a gizmo arrow
        if self.selected_shape and self.gizmo_visible:
            axis = self.check_gizmo_click(event.x, event.y)
            if axis:
                self.active_axis = axis
                self.drag_start_pos = (event.x, event.y)
                if self.gizmo_mode == 'translate':
                    self.drag_start_object_pos = self.selected_shape.position.copy()
                elif self.gizmo_mode == 'rotate':
                    self.drag_start_object_pos = self.selected_shape.rotation.copy()
                elif self.gizmo_mode == 'scale':
                    self.drag_start_object_pos = self.selected_shape.size
                self.editor.log(f"Dragging {axis.upper()} axis ({self.gizmo_mode})", "info")
                return
        
        # Check if we clicked on an object
        clicked_shape = self.pick_object(event.x, event.y)
        if clicked_shape:
            self.selected_shape = clicked_shape
            self.gizmo_visible = True
            self.update_property_panel()
            self.editor.log(f"Selected {type(clicked_shape).__name__}", "info")
            self.render()
            return
        
        # Otherwise, start camera rotation
        self.mouse_dragging = True
    
    def on_mouse_drag(self, event):
        """Handle mouse drag for camera rotation or gizmo manipulation"""
        dx = event.x - self.mouse_x
        dy = event.y - self.mouse_y
        
        # If dragging a gizmo axis
        if self.active_axis and self.selected_shape:
            sensitivity = 0.1
            
            if self.gizmo_mode == 'translate':
                # Move object along axis
                if self.active_axis == 'x':
                    self.selected_shape.position.x = self.drag_start_object_pos.x + dx * sensitivity
                elif self.active_axis == 'y':
                    self.selected_shape.position.y = self.drag_start_object_pos.y - dy * sensitivity
                elif self.active_axis == 'z':
                    self.selected_shape.position.z = self.drag_start_object_pos.z + dx * sensitivity
                
            elif self.gizmo_mode == 'rotate':
                # Rotate object around axis
                rotation_speed = 2.0
                if self.active_axis == 'x':
                    self.selected_shape.rotation.x = self.drag_start_object_pos.x + dy * rotation_speed
                elif self.active_axis == 'y':
                    self.selected_shape.rotation.y = self.drag_start_object_pos.y + dx * rotation_speed
                elif self.active_axis == 'z':
                    self.selected_shape.rotation.z = self.drag_start_object_pos.z + dx * rotation_speed
                
            elif self.gizmo_mode == 'scale':
                # Scale object
                scale_speed = 0.01
                delta = (dx - dy) * scale_speed
                self.selected_shape.size = max(0.1, self.drag_start_object_pos + delta)
            
            self.update_property_panel()
            self.render()
            return
        
        # Camera rotation
        if self.mouse_dragging and not self.camera.is_first_person:
            self.camera.rotation.y += dx * 0.5
            self.camera.rotation.x += dy * 0.5
            
            self.mouse_x = event.x
            self.mouse_y = event.y
            
            self.render()
    
    def on_mouse_up(self, event):
        """Handle mouse up"""
        self.mouse_dragging = False
        self.active_axis = None
        self.drag_start_pos = None
        self.drag_start_object_pos = None
    
    def on_middle_mouse_down(self, event):
        """Handle middle mouse button down for panning"""
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.middle_mouse_dragging = True
    
    def on_middle_mouse_drag(self, event):
        """Handle middle mouse drag for camera panning"""
        if self.middle_mouse_dragging and not self.camera.is_first_person:
            dx = (event.x - self.mouse_x) * 0.05
            dy = (event.y - self.mouse_y) * 0.05
            
            # Pan camera
            self.camera.position.x -= dx
            self.camera.position.z += dy
            
            self.mouse_x = event.x
            self.mouse_y = event.y
            
            self.render()
    
    def on_middle_mouse_up(self, event):
        """Handle middle mouse up"""
        self.middle_mouse_dragging = False
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if self.camera.is_first_person:
            return  # No zoom in first person
        
        # Handle different platforms
        if event.num == 4 or event.delta > 0:  # Scroll up
            zoom_factor = -self.zoom_speed
        elif event.num == 5 or event.delta < 0:  # Scroll down
            zoom_factor = self.zoom_speed
        else:
            return
        
        # Move camera forward/backward along viewing direction
        # Simple zoom: move along Z axis
        self.camera.position.z += zoom_factor
        
        self.render()
    
    def on_key_press(self, event):
        """Handle key press"""
        key = event.keysym.lower()
        self.keys_pressed.add(key)
        
        # Copy/Paste functionality (only in trajectory mode)
        if self.mode == self.MODE_TRAJECTORY:
            # Ctrl+C - Copy selected object
            if key == 'c' and 'control_l' in self.keys_pressed or 'control_r' in self.keys_pressed:
                if self.selected_shape:
                    self.copy_object()
                return
            
            # Ctrl+V - Paste copied object
            if key == 'v' and ('control_l' in self.keys_pressed or 'control_r' in self.keys_pressed):
                if self.clipboard_object:
                    self.paste_object()
                return
        
        # Gizmo shortcuts (only in trajectory mode)
        if self.mode == self.MODE_TRAJECTORY:
            if key == 'g':
                self.set_gizmo_mode('translate')
                self.keys_pressed.discard('g')
                return
            elif key == 'r':
                self.set_gizmo_mode('rotate')
                self.keys_pressed.discard('r')
                return
            elif key == 's' and 'control_l' not in self.keys_pressed and 'control_r' not in self.keys_pressed:
                # Only if Ctrl not pressed (to avoid conflict with Ctrl+S save)
                self.set_gizmo_mode('scale')
                self.keys_pressed.discard('s')
                return
            elif key == 'delete' or key == 'backspace':
                if self.selected_shape:
                    self.delete_selected_object()
                return
        
        # Shift key for faster movement
        if key == 'shift_l' or key == 'shift_r':
            self.camera_speed = 1.0  # Faster
    
    def on_key_release(self, event):
        """Handle key release"""
        key = event.keysym.lower()
        self.keys_pressed.discard(key)
        
        # Reset speed when shift released
        if key == 'shift_l' or key == 'shift_r':
            self.camera_speed = 0.5  # Normal speed
    
    def update_camera_movement(self):
        """Update camera position based on held keys"""
        # Safety check: make sure canvas still exists
        try:
            if not self.canvas.winfo_exists():
                return  # Canvas destroyed, stop updating
        except:
            return  # Canvas gone, stop updating
        
        # This runs continuously for smooth camera movement
        
        moved = False
        
        # Only allow camera movement in trajectory mode or when not in first person
        if self.mode == self.MODE_TRAJECTORY or not self.camera.is_first_person:
            # WASD for camera movement in viewport
            if 'w' in self.keys_pressed:
                self.camera.position.z += self.camera_speed
                moved = True
            if 's' in self.keys_pressed:
                self.camera.position.z -= self.camera_speed
                moved = True
            if 'a' in self.keys_pressed:
                self.camera.position.x -= self.camera_speed
                moved = True
            if 'd' in self.keys_pressed:
                self.camera.position.x += self.camera_speed
                moved = True
            
            # Q/E for vertical movement
            if 'q' in self.keys_pressed:
                self.camera.position.y -= self.camera_speed
                moved = True
            if 'e' in self.keys_pressed:
                self.camera.position.y += self.camera_speed
                moved = True
            
            # Arrow keys for camera rotation
            if 'left' in self.keys_pressed:
                self.camera.rotation.y -= 2.0
                moved = True
            if 'right' in self.keys_pressed:
                self.camera.rotation.y += 2.0
                moved = True
            if 'up' in self.keys_pressed:
                self.camera.rotation.x -= 2.0
                moved = True
            if 'down' in self.keys_pressed:
                self.camera.rotation.x += 2.0
                moved = True
            
            # R to reset camera
            if 'r' in self.keys_pressed:
                self.reset_camera()
                self.keys_pressed.discard('r')
                moved = True
        
        # Render if camera moved
        if moved:
            self.render()
        
        # Schedule next update
        self.canvas.after(16, self.update_camera_movement)  # ~60 FPS
    
    def reset_camera(self):
        """Reset camera to default position"""
        self.camera.position = Vector3D(0, 3, -10)
        self.camera.rotation = Vector3D(0, 0, 0)
        self.editor.log("Camera reset to default position", "info")
    
    def draw_gizmo(self):
        """Draw XYZ manipulation gizmo at selected object"""
        if not self.selected_shape:
            return
        
        # Get object center in screen space
        center = self.project_3d_to_2d(self.selected_shape.position)
        if not center:
            return
        
        cx, cy = center
        arrow_length = 60
        arrow_head = 10
        
        # X axis - RED
        x_end = self.project_3d_to_2d(Vector3D(
            self.selected_shape.position.x + 1,
            self.selected_shape.position.y,
            self.selected_shape.position.z
        ))
        if x_end:
            # Draw arrow shaft
            self.canvas.create_line(cx, cy, x_end[0], x_end[1],
                                   fill="#ff0000", width=3, tags="gizmo_x")
            # Draw arrow head
            angle = math.atan2(x_end[1] - cy, x_end[0] - cx)
            head_x = x_end[0]
            head_y = x_end[1]
            self.canvas.create_polygon(
                head_x, head_y,
                head_x - arrow_head * math.cos(angle - 0.5), head_y - arrow_head * math.sin(angle - 0.5),
                head_x - arrow_head * math.cos(angle + 0.5), head_y - arrow_head * math.sin(angle + 0.5),
                fill="#ff0000", outline="#ff0000", tags="gizmo_x"
            )
            # Label
            self.canvas.create_text(x_end[0] + 15, x_end[1], text="X", 
                                   fill="#ff0000", font=("Arial", 12, "bold"), tags="gizmo_x")
        
        # Y axis - GREEN
        y_end = self.project_3d_to_2d(Vector3D(
            self.selected_shape.position.x,
            self.selected_shape.position.y + 1,
            self.selected_shape.position.z
        ))
        if y_end:
            self.canvas.create_line(cx, cy, y_end[0], y_end[1],
                                   fill="#00ff00", width=3, tags="gizmo_y")
            angle = math.atan2(y_end[1] - cy, y_end[0] - cx)
            head_x = y_end[0]
            head_y = y_end[1]
            self.canvas.create_polygon(
                head_x, head_y,
                head_x - arrow_head * math.cos(angle - 0.5), head_y - arrow_head * math.sin(angle - 0.5),
                head_x - arrow_head * math.cos(angle + 0.5), head_y - arrow_head * math.sin(angle + 0.5),
                fill="#00ff00", outline="#00ff00", tags="gizmo_y"
            )
            self.canvas.create_text(y_end[0] + 15, y_end[1], text="Y",
                                   fill="#00ff00", font=("Arial", 12, "bold"), tags="gizmo_y")
        
        # Z axis - BLUE
        z_end = self.project_3d_to_2d(Vector3D(
            self.selected_shape.position.x,
            self.selected_shape.position.y,
            self.selected_shape.position.z + 1
        ))
        if z_end:
            self.canvas.create_line(cx, cy, z_end[0], z_end[1],
                                   fill="#0088ff", width=3, tags="gizmo_z")
            angle = math.atan2(z_end[1] - cy, z_end[0] - cx)
            head_x = z_end[0]
            head_y = z_end[1]
            self.canvas.create_polygon(
                head_x, head_y,
                head_x - arrow_head * math.cos(angle - 0.5), head_y - arrow_head * math.sin(angle - 0.5),
                head_x - arrow_head * math.cos(angle + 0.5), head_y - arrow_head * math.sin(angle + 0.5),
                fill="#0088ff", outline="#0088ff", tags="gizmo_z"
            )
            self.canvas.create_text(z_end[0] + 15, z_end[1], text="Z",
                                   fill="#0088ff", font=("Arial", 12, "bold"), tags="gizmo_z")
    
    def check_gizmo_click(self, x, y):
        """Check if mouse click is on a gizmo arrow"""
        # Get items at click position
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        
        for item in items:
            tags = self.canvas.gettags(item)
            if 'gizmo_x' in tags:
                return 'x'
            elif 'gizmo_y' in tags:
                return 'y'
            elif 'gizmo_z' in tags:
                return 'z'
        
        return None
    
    def pick_object(self, x, y):
        """Pick/select object at mouse position"""
        # Simple picking: check which object's center is closest to click
        min_dist = 50  # Pixel threshold
        closest_shape = None
        
        for shape in self.shapes:
            if isinstance(shape, Plane):
                continue  # Skip planes for selection
            
            center = self.project_3d_to_2d(shape.position)
            if center:
                dist = math.sqrt((center[0] - x)**2 + (center[1] - y)**2)
                if dist < min_dist:
                    min_dist = dist
                    closest_shape = shape
        
        return closest_shape
    
    def delete_selected_object(self):
        """Delete the currently selected object"""
        if self.selected_shape in self.shapes:
            shape_type = type(self.selected_shape).__name__
            self.shapes.remove(self.selected_shape)
            
            # Clear player reference if deleting player
            if self.selected_shape == self.player:
                self.player = None
                self.player_controls_enabled = False
                self.camera.is_first_person = False
            
            self.selected_shape = None
            self.gizmo_visible = False
            self.update_property_panel()
            self.editor.log(f"Deleted {shape_type}", "warning")
            self.render()
    
    def copy_object(self):
        """Copy the selected object to clipboard"""
        if not self.selected_shape:
            self.editor.log("No object selected to copy!", "warning")
            return
        
        # Store a copy of the object's properties
        self.clipboard_object = {
            'type': type(self.selected_shape).__name__,
            'position': self.selected_shape.position.copy(),
            'rotation': self.selected_shape.rotation.copy(),
            'scale': self.selected_shape.scale.copy(),
            'size': self.selected_shape.size,
            'color': self.selected_shape.color,
            'has_collision': self.selected_shape.has_collision,
            'has_physics': self.selected_shape.has_physics,
            'mass': self.selected_shape.mass,
            'friction': self.selected_shape.friction,
            'restitution': self.selected_shape.restitution
        }
        
        self.editor.log(f"Copied {self.clipboard_object['type']}", "success")
    
    def paste_object(self):
        """Paste object from clipboard"""
        if not self.clipboard_object:
            self.editor.log("Nothing to paste!", "warning")
            return
        
        # Create new object based on type
        obj_type = self.clipboard_object['type']
        
        # Offset position slightly so it doesn't overlap
        new_pos = self.clipboard_object['position'].copy()
        new_pos.x += 1.0
        new_pos.z += 1.0
        
        if obj_type == 'Cube':
            new_obj = Cube(new_pos, self.clipboard_object['size'])
        elif obj_type == 'Sphere':
            new_obj = Sphere(new_pos, self.clipboard_object['size'])
        elif obj_type == 'Plane':
            new_obj = Plane(new_pos, self.clipboard_object['size'])
        else:
            self.editor.log(f"Cannot paste {obj_type}", "error")
            return
        
        # Copy properties
        new_obj.rotation = self.clipboard_object['rotation'].copy()
        new_obj.scale = self.clipboard_object['scale'].copy()
        new_obj.color = self.clipboard_object['color']
        new_obj.has_collision = self.clipboard_object['has_collision']
        new_obj.has_physics = self.clipboard_object['has_physics']
        new_obj.mass = self.clipboard_object['mass']
        new_obj.friction = self.clipboard_object['friction']
        new_obj.restitution = self.clipboard_object['restitution']
        
        # Add to scene
        self.shapes.append(new_obj)
        self.selected_shape = new_obj
        self.gizmo_visible = True
        self.update_property_panel()
        
        self.editor.log(f"Pasted {obj_type} at ({new_pos.x:.1f}, {new_pos.y:.1f}, {new_pos.z:.1f})", "success")
        self.render()
    
    def start_animation(self):
        """Start animation loop"""
        self.animation_running = True
        self.animate()
    
    def animate(self):
        """Animation loop for physics and player"""
        if not self.animation_running:
            return
        
        # Update physics
        if self.physics_enabled:
            self.update_physics()
        
        # Update player
        if self.player_controls_enabled and self.player:
            self.update_player()
        
        # Render
        self.render()
        
        # Continue animation
        self.canvas.after(16, self.animate)  # ~60 FPS
    
    def update_physics(self):
        """Update physics simulation"""
        for shape in self.shapes:
            if not shape.has_physics or shape.is_static:
                continue
            
            # Apply gravity
            shape.velocity.y += self.gravity * self.dt
            
            # Apply friction if on ground
            if shape.on_ground:
                friction_factor = 1.0 - (shape.friction * self.dt * 5)
                shape.velocity.x *= friction_factor
                shape.velocity.z *= friction_factor
            
            # Update position
            shape.position.x += shape.velocity.x * self.dt
            shape.position.y += shape.velocity.y * self.dt
            shape.position.z += shape.velocity.z * self.dt
            
            # Rolling physics for spheres
            if isinstance(shape, Sphere) and shape.is_rolling and shape.on_ground:
                # Calculate rotation based on velocity (rolling)
                radius = shape.size / 2
                if abs(shape.velocity.x) > 0.01 or abs(shape.velocity.z) > 0.01:
                    # Rotate around axis perpendicular to movement
                    shape.rotation.z += (shape.velocity.x / radius) * self.dt * 50
                    shape.rotation.x -= (shape.velocity.z / radius) * self.dt * 50
            
            # Ground collision
            shape.on_ground = False
            for other in self.shapes:
                if isinstance(other, Plane) and other.is_static:
                    # Check if shape is on plane
                    ground_level = other.position.y + shape.size / 2
                    if shape.position.y <= ground_level:
                        shape.position.y = ground_level
                        
                        # Bounce with restitution
                        if shape.velocity.y < -0.1:
                            shape.velocity.y = -shape.velocity.y * shape.restitution
                        else:
                            shape.velocity.y = 0
                        
                        shape.on_ground = True
    
    def update_player(self):
        """Update player movement"""
        if not self.player:
            return
        
        # Only move player in game mode with controls enabled
        if self.mode != self.MODE_GAME or not self.player_controls_enabled:
            return
        
        # Store old position for collision resolution
        old_pos = self.player.position.copy()
        
        # Camera/look rotation with arrow keys
        rotation_speed = 3.0  # Degrees per frame
        if 'left' in self.keys_pressed:
            self.camera.yaw -= rotation_speed
        if 'right' in self.keys_pressed:
            self.camera.yaw += rotation_speed
        if 'up' in self.keys_pressed:
            self.camera.pitch += rotation_speed
            # Clamp pitch to prevent flipping
            if self.camera.pitch > 89:
                self.camera.pitch = 89
        if 'down' in self.keys_pressed:
            self.camera.pitch -= rotation_speed
            if self.camera.pitch < -89:
                self.camera.pitch = -89
        
        # Movement relative to camera direction
        move_speed = self.player_speed * self.dt
        
        # Convert yaw to radians for movement calculation
        yaw_rad = math.radians(self.camera.yaw)
        
        # Forward/backward (W/S) - relative to where player is looking
        forward_x = math.sin(yaw_rad)
        forward_z = math.cos(yaw_rad)
        
        if 'w' in self.keys_pressed:
            self.player.position.x += forward_x * move_speed
            self.player.position.z += forward_z * move_speed
        if 's' in self.keys_pressed:
            self.player.position.x -= forward_x * move_speed
            self.player.position.z -= forward_z * move_speed
        
        # Strafe left/right (A/D) - perpendicular to look direction
        right_x = math.sin(yaw_rad + math.pi / 2)
        right_z = math.cos(yaw_rad + math.pi / 2)
        
        if 'a' in self.keys_pressed:
            self.player.position.x -= right_x * move_speed
            self.player.position.z -= right_z * move_speed
        if 'd' in self.keys_pressed:
            self.player.position.x += right_x * move_speed
            self.player.position.z += right_z * move_speed
        
        # Check collision with objects that have collision enabled
        collision_detected = False
        for shape in self.shapes:
            if shape == self.player or not shape.has_collision:
                continue
            
            if self.check_collision_aabb(self.player, shape):
                collision_detected = True
                # Push player back
                self.player.position = old_pos.copy()
                
                # Stop movement in collision direction
                dx = self.player.position.x - shape.position.x
                dz = self.player.position.z - shape.position.z
                
                # Push player away slightly
                if abs(dx) > abs(dz):
                    self.player.position.x = shape.position.x + (shape.size / 2 + self.player.size / 2) * (1 if dx > 0 else -1)
                else:
                    self.player.position.z = shape.position.z + (shape.size / 2 + self.player.size / 2) * (1 if dz > 0 else -1)
                
                break
        
        # Jump
        if 'space' in self.keys_pressed and self.player.on_ground:
            self.player.velocity.y = 5.0
            self.keys_pressed.discard('space')  # Prevent multi-jump
        
        # Update camera to follow player with rotation
        self.camera.position = self.player.position.copy()
        self.camera.position.y += 0.8  # Eye height
        
        # Apply camera rotation
        self.camera.rotation.x = self.camera.pitch
        self.camera.rotation.y = self.camera.yaw
    
    def check_collision_aabb(self, obj1, obj2):
        """Check collision between two objects using AABB"""
        # Get bounding boxes with non-uniform scale
        half_size1_x = obj1.size * obj1.scale.x / 2
        half_size1_y = obj1.size * obj1.scale.y / 2
        half_size1_z = obj1.size * obj1.scale.z / 2
        
        half_size2_x = obj2.size * obj2.scale.x / 2
        half_size2_y = obj2.size * obj2.scale.y / 2
        half_size2_z = obj2.size * obj2.scale.z / 2
        
        # Check overlap on all axes
        x_overlap = abs(obj1.position.x - obj2.position.x) < (half_size1_x + half_size2_x)
        y_overlap = abs(obj1.position.y - obj2.position.y) < (half_size1_y + half_size2_y)
        z_overlap = abs(obj1.position.z - obj2.position.z) < (half_size1_z + half_size2_z)
        
        return x_overlap and y_overlap and z_overlap