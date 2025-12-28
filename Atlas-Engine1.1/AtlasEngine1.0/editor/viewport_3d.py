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
        self.filled = False  # NEW: Render as filled vs wireframe
        self.light_level = 1.0  # NEW: Brightness (0.0 to 1.0)
    
    def get_vertices(self) -> List[Vector3D]:
        """Override in subclasses"""
        return []
    
    def get_edges(self) -> List[Tuple[int, int]]:
        """Override in subclasses"""
        return []
    
    def get_faces(self) -> List[List[int]]:
        """Override in subclasses for filled rendering"""
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
    
    def get_faces(self):
        """Return faces for filled rendering (list of vertex indices for each face)"""
        return [
            [0, 1, 2, 3],  # Back face
            [4, 5, 6, 7],  # Front face
            [0, 1, 5, 4],  # Bottom face
            [2, 3, 7, 6],  # Top face
            [0, 3, 7, 4],  # Left face
            [1, 2, 6, 5],  # Right face
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


class Cone(Shape3D):
    """Cone shape (pyramid with circular base)"""
    def __init__(self, position: Vector3D, size: float = 1.0):
        super().__init__(position, size)
        self.segments = 16  # Number of segments around base
        self.color = "#ff0000"  # RED!
    
    def get_vertices(self):
        vertices = []
        radius = self.size / 2
        height = self.size
        
        # Apex (top point)
        apex = Vector3D(
            self.position.x,
            self.position.y + height / 2,
            self.position.z
        )
        vertices.append(apex)
        
        # Base center
        base_center = Vector3D(
            self.position.x,
            self.position.y - height / 2,
            self.position.z
        )
        vertices.append(base_center)
        
        # Base circle vertices
        for i in range(self.segments):
            theta = (i / self.segments) * 2 * math.pi
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            
            vertices.append(Vector3D(
                self.position.x + x,
                self.position.y - height / 2,
                self.position.z + z
            ))
        
        return vertices
    
    def get_edges(self):
        edges = []
        
        # Edges from apex to base circle
        for i in range(self.segments):
            edges.append((0, i + 2))  # Apex to base circle vertex
        
        # Base circle edges
        for i in range(self.segments):
            current = i + 2
            next_vertex = ((i + 1) % self.segments) + 2
            edges.append((current, next_vertex))
        
        # Optional: Edges from base center to circle (for wireframe visibility)
        for i in range(self.segments):
            edges.append((1, i + 2))  # Base center to base circle vertex
        
        return edges


class Wedge(Shape3D):
    """Wedge/Ramp shape - triangular prism for stairs/slopes"""
    def __init__(self, position: Vector3D, size: float = 1.0):
        super().__init__(position, size)
        self.color = "#a0826d"  # Light brown
    
    def get_vertices(self):
        # Apply non-uniform scale to base size
        sx = self.size * self.scale.x / 2
        sy = self.size * self.scale.y / 2
        sz = self.size * self.scale.z / 2
        
        # Wedge vertices (like a ramp)
        # Bottom face: 4 vertices (rectangular base)
        # Top edge: 2 vertices (the top edge of the ramp)
        vertices = [
            # Bottom face (4 vertices)
            Vector3D(-sx, -sy, -sz),  # 0: bottom back left
            Vector3D(sx, -sy, -sz),   # 1: bottom back right
            Vector3D(sx, -sy, sz),    # 2: bottom front right
            Vector3D(-sx, -sy, sz),   # 3: bottom front left
            
            # Top edge (2 vertices - the high end of the ramp)
            Vector3D(-sx, sy, -sz),   # 4: top back left
            Vector3D(sx, sy, -sz),    # 5: top back right
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
            # Bottom face
            (0, 1), (1, 2), (2, 3), (3, 0),
            
            # Top edge
            (4, 5),
            
            # Vertical edges
            (0, 4), (1, 5),
            
            # Sloped faces
            (2, 4), (2, 5), (3, 4), (3, 5)
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
    
    # 8 Gameplay Modes
    GAMEPLAY_MODE_SHOOTER = "🔫 Shooter"
    GAMEPLAY_MODE_EXPLORER = "🗺️ Explorer"
    GAMEPLAY_MODE_BUILDER = "🏗️ Builder"
    GAMEPLAY_MODE_RPG = "⚔️ RPG"
    GAMEPLAY_MODE_PUZZLE = "🧩 Puzzle"
    GAMEPLAY_MODE_RACING = "🏎️ Racing"
    GAMEPLAY_MODE_SURVIVAL = "🌲 Survival"
    GAMEPLAY_MODE_SANDBOX = "🎨 Sandbox"
    
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
        self.gameplay_mode = self.GAMEPLAY_MODE_EXPLORER  # Default gameplay mode
        
        # Professional Mode (compact UI)
        self.professional_mode = False  # Toggle for compact buttons
        
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
        self.toolbar = tk.Frame(self.frame, bg="#252526", height=40)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        self.toolbar.pack_propagate(False)
        toolbar = self.toolbar  # For backward compatibility
        
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
        
        tk.Button(toolbar, text="Cone", command=self.add_cone,
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
        
        # Toggle Player/Viewport Mode button - RIGHT NEXT TO PLAYER BUTTON
        self.toggle_player_mode_btn = tk.Button(toolbar, text="🚪 Exit Player", command=self.toggle_player_viewport_mode,
                                               bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=10,
                                               state=tk.DISABLED)
        self.toggle_player_mode_btn.pack(side=tk.LEFT, padx=2)  # Pack immediately after Player button
        
        # Gameplay Mode Sidebar Toggle Button
        mode_text = "⚙️" if self.professional_mode else "⚙️ Mode"
        self.mode_sidebar_btn = tk.Button(toolbar, text=mode_text, command=self.toggle_mode_sidebar,
                                         bg="#0e639c", fg="white", relief=tk.FLAT, padx=10)
        self.mode_sidebar_btn.pack(side=tk.LEFT, padx=2)
        
        # Professional Mode Toggle (compact UI)
        pro_text = "💼" if self.professional_mode else "💼 Pro"
        self.pro_mode_btn = tk.Button(toolbar, text=pro_text, command=self.toggle_professional_mode,
                                      bg="#666666", fg="white", relief=tk.FLAT, padx=6)
        self.pro_mode_btn.pack(side=tk.LEFT, padx=2)
        
        # Gizmo mode buttons
        if not self.professional_mode:
            tk.Label(toolbar, text="Gizmo:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        move_text = "↔️" if self.professional_mode else "Move"
        self.gizmo_translate_btn = tk.Button(toolbar, text=move_text, command=lambda: self.set_gizmo_mode('translate'),
                                            bg="#0e639c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_translate_btn.pack(side=tk.LEFT, padx=2)
        
        rotate_text = "🔄" if self.professional_mode else "Rotate"
        self.gizmo_rotate_btn = tk.Button(toolbar, text=rotate_text, command=lambda: self.set_gizmo_mode('rotate'),
                                         bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_rotate_btn.pack(side=tk.LEFT, padx=2)
        
        scale_text = "📏" if self.professional_mode else "Scale"
        self.gizmo_scale_btn = tk.Button(toolbar, text=scale_text, command=lambda: self.set_gizmo_mode('scale'),
                                        bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_scale_btn.pack(side=tk.LEFT, padx=2)
        
        # Fill/Bucket button
        fill_text = "🪣" if self.professional_mode else "🪣 Fill"
        self.fill_btn = tk.Button(toolbar, text=fill_text, command=self.toggle_fill,
                                 bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.fill_btn.pack(side=tk.LEFT, padx=2)
        
        # Collision toggle button
        if not self.professional_mode:
            tk.Label(toolbar, text="Physics:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        collision_text = "🛡️" if self.professional_mode else "🛡️ Collision"
        self.collision_btn = tk.Button(toolbar, text=collision_text, command=self.toggle_collision,
                                      bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=8)
        self.collision_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear button
        clear_text = "🗑️" if self.professional_mode else "Clear"
        tk.Button(toolbar, text=clear_text, command=self.clear_scene,
                 bg="#c24545", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=2)
        
        # Canvas for 3D rendering (left side)
        main_container = tk.Frame(self.frame, bg="#2b2b2b")
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Gameplay Mode Sidebar (collapsible)
        self.mode_sidebar_frame = tk.Frame(main_container, bg="#1e1e1e", width=200)
        self.mode_sidebar_visible = False  # Start hidden
        self.setup_mode_sidebar()
        
        # Split into canvas and code panel
        canvas_frame = tk.Frame(main_container, bg="#2b2b2b")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Code panel (right side) - collapsible
        self.code_panel_frame = tk.Frame(main_container, bg="#1e1e1e", width=350)
        self.code_panel_visible = False  # Start hidden
        
        # Toggle button for code panel
        toggle_frame = tk.Frame(self.frame, bg="#252526")
        toggle_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.code_panel_toggle_btn = tk.Button(toggle_frame, text="▶ Show Code Panel", 
                                              command=self.toggle_code_panel,
                                              bg="#0e639c", fg="white", relief=tk.FLAT, padx=10)
        self.code_panel_toggle_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(toggle_frame, text="Write T# commands to control 3D scene in real-time!", 
                bg="#252526", fg="#888888", font=("Consolas", 8)).pack(side=tk.LEFT, padx=10)
        
        # Setup code panel content
        self.setup_code_panel()
        
        # Setup code panel content
        self.setup_code_panel()
        
        # NPC system
        self.npcs = []
        self.npc_dialogues = {}
        
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
        self.canvas.bind('<FocusIn>', self.on_canvas_focus_in)
        self.canvas.bind('<FocusOut>', self.on_canvas_focus_out)
        self.canvas.bind('<Enter>', self.on_canvas_enter)  # Mouse enters canvas
        self.canvas.focus_set()
        
        # Focus state tracking
        self.canvas_has_focus = True
        
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
            elif isinstance(self.selected_shape, Cone):
                self.selected_shape.color = "#ff00ff"
        
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
                elif isinstance(self.selected_shape, Cone):
                    self.selected_shape.color = "#ff00ff"
            self.render()
    
    def toggle_fill(self):
        """Toggle filled rendering for selected object"""
        if not self.selected_shape:
            self.editor.log("No object selected! Select an object first.", "warning")
            return
        
        self.selected_shape.filled = not self.selected_shape.filled
        
        if self.selected_shape.filled:
            self.fill_btn.config(bg="#4caf50")
            self.editor.log(f"✅ FILLED rendering for {type(self.selected_shape).__name__}", "success")
        else:
            self.fill_btn.config(bg="#3c3c3c")
            self.editor.log(f"Wireframe rendering for {type(self.selected_shape).__name__}", "info")
        
        self.render()
    
    def toggle_professional_mode(self):
        """Toggle professional mode (compact UI)"""
        self.professional_mode = not self.professional_mode
        
        if self.professional_mode:
            self.editor.log("💼 PROFESSIONAL MODE: Compact UI enabled!", "success")
        else:
            self.editor.log("Regular UI mode enabled", "info")
        
        # Rebuild toolbar buttons with new mode
        self.rebuild_toolbar_buttons()
    
    def rebuild_toolbar_buttons(self):
        """Rebuild toolbar buttons dynamically based on professional mode"""
        # Find and destroy old buttons (everything after mode selector)
        for widget in self.toolbar.winfo_children():
            # Keep the mode selector and Add buttons, rebuild everything after
            if isinstance(widget, tk.Button) and hasattr(widget, 'config'):
                widget_text = widget.cget('text')
                # Rebuild gizmo and utility buttons
                if any(x in str(widget_text) for x in ['Mode', 'Pro', 'Move', '↔️', 'Rotate', '🔄', 
                                                         'Scale', '📏', 'Fill', '🪣', 'Collision', '🛡️', 
                                                         'Clear', '🗑️']):
                    widget.destroy()
            elif isinstance(widget, tk.Label):
                label_text = widget.cget('text')
                if 'Gizmo:' in label_text or 'Physics:' in label_text:
                    widget.destroy()
        
        # Rebuild buttons with current mode
        toolbar = self.toolbar
        
        # Mode button
        mode_text = "⚙️" if self.professional_mode else "⚙️ Mode"
        self.mode_sidebar_btn = tk.Button(toolbar, text=mode_text, command=self.toggle_mode_sidebar,
                                         bg="#0e639c", fg="white", relief=tk.FLAT, padx=10)
        self.mode_sidebar_btn.pack(side=tk.LEFT, padx=2)
        
        # Pro button
        pro_text = "💼" if self.professional_mode else "💼 Pro"
        pro_bg = "#4caf50" if self.professional_mode else "#666666"
        self.pro_mode_btn = tk.Button(toolbar, text=pro_text, command=self.toggle_professional_mode,
                                      bg=pro_bg, fg="white", relief=tk.FLAT, padx=6)
        self.pro_mode_btn.pack(side=tk.LEFT, padx=2)
        
        # Gizmo label
        if not self.professional_mode:
            tk.Label(toolbar, text="Gizmo:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        # Gizmo buttons
        move_text = "↔️" if self.professional_mode else "Move"
        move_bg = "#0e639c" if self.gizmo_mode == 'translate' else "#3c3c3c"
        self.gizmo_translate_btn = tk.Button(toolbar, text=move_text, command=lambda: self.set_gizmo_mode('translate'),
                                            bg=move_bg, fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_translate_btn.pack(side=tk.LEFT, padx=2)
        
        rotate_text = "🔄" if self.professional_mode else "Rotate"
        rotate_bg = "#0e639c" if self.gizmo_mode == 'rotate' else "#3c3c3c"
        self.gizmo_rotate_btn = tk.Button(toolbar, text=rotate_text, command=lambda: self.set_gizmo_mode('rotate'),
                                         bg=rotate_bg, fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_rotate_btn.pack(side=tk.LEFT, padx=2)
        
        scale_text = "📏" if self.professional_mode else "Scale"
        scale_bg = "#0e639c" if self.gizmo_mode == 'scale' else "#3c3c3c"
        self.gizmo_scale_btn = tk.Button(toolbar, text=scale_text, command=lambda: self.set_gizmo_mode('scale'),
                                        bg=scale_bg, fg="white", relief=tk.FLAT, padx=8)
        self.gizmo_scale_btn.pack(side=tk.LEFT, padx=2)
        
        # Fill button
        fill_text = "🪣" if self.professional_mode else "🪣 Fill"
        fill_bg = "#4caf50" if self.selected_shape and self.selected_shape.filled else "#3c3c3c"
        self.fill_btn = tk.Button(toolbar, text=fill_text, command=self.toggle_fill,
                                 bg=fill_bg, fg="white", relief=tk.FLAT, padx=8)
        self.fill_btn.pack(side=tk.LEFT, padx=2)
        
        # Physics label
        if not self.professional_mode:
            tk.Label(toolbar, text="Physics:", bg="#252526", fg="#cccccc").pack(side=tk.LEFT, padx=(20,5))
        
        # Collision button
        collision_text = "🛡️" if self.professional_mode else "🛡️ Collision"
        collision_bg = "#4caf50" if self.selected_shape and self.selected_shape.has_collision else "#3c3c3c"
        self.collision_btn = tk.Button(toolbar, text=collision_text, command=self.toggle_collision,
                                      bg=collision_bg, fg="white", relief=tk.FLAT, padx=8)
        self.collision_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear button
        clear_text = "🗑️" if self.professional_mode else "Clear"
        tk.Button(toolbar, text=clear_text, command=self.clear_scene,
                 bg="#c24545", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=2)
    
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
    
    def add_cone(self):
        """Add a cone to the scene"""
        cone = Cone(Vector3D(-2, 2, 0), 1.0)
        cone.color = "#ff00ff"
        self.shapes.append(cone)
        self.selected_shape = cone
        self.update_property_panel()
        self.editor.log(f"Added cone at (-2, 2, 0)")
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
        self.player.velocity = Vector3D(0, 0, 0)  # Initialize velocity
        self.player.on_ground = False  # Initialize ground state
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
        
        # Initialize weapon system
        self.weapon_bob_time = 0
        self.weapon_recoil_time = 0
        self.show_muzzle_flash = False
        
        # Initialize ammo if not already set
        if hasattr(self.editor, 'interpreter'):
            if 'ammo' not in self.editor.interpreter.variables:
                self.editor.interpreter.variables['ammo'] = 30
            if 'magazine' not in self.editor.interpreter.variables:
                self.editor.interpreter.variables['magazine'] = 30
        
        # Start animation loop for player physics!
        if not self.animation_running:
            self.start_animation()
        
        # Enable toggle button and update text
        self.toggle_player_mode_btn.config(text="🚪 Exit Game", bg="#ff4444", state=tk.NORMAL)
        
        self.editor.log("🔫 Player added with gun! LMB to shoot", "success")
        self.editor.log("Press '🚪 Exit Game' button to leave player mode", "info")
        
        self.canvas.focus_set()
        self.render()
    
    def toggle_player_viewport_mode(self):
        """Toggle between Player mode and Viewport mode"""
        if not self.player:
            self.editor.log("No player exists!", "warning")
            return
        
        if self.player_controls_enabled:
            # Switch to Viewport mode (free camera)
            self.player_controls_enabled = False
            self.camera.is_first_person = False
            
            # Move camera away from player for better view
            self.camera.position = Vector3D(
                self.player.position.x - 5,
                self.player.position.y + 5,
                self.player.position.z - 5
            )
            self.camera.rotation = Vector3D(20, 45, 0)
            
            # Update button
            self.toggle_player_mode_btn.config(text="🎮 Enter Game", bg="#4caf50")
            
            self.editor.log("📷 Viewport Mode: Free camera, no player control", "info")
            self.editor.log("Click '🎮 Enter Game' to go back to playing")
        else:
            # Switch to Player mode (first person)
            self.player_controls_enabled = True
            self.camera.is_first_person = True
            
            # Reset camera to player position
            self.camera.position = self.player.position.copy()
            self.camera.position.y += 0.8  # Eye height
            self.camera.yaw = 0
            self.camera.pitch = 0
            
            # Update button
            self.toggle_player_mode_btn.config(text="🚪 Exit Game", bg="#ff4444")
            
            self.editor.log("🎮 Player Mode: First-person control active", "success")
            self.editor.log("Click '🚪 Exit Game' to leave and view from outside")
        
        self.render()
    
    def show_build_menu(self):
        """Show quick build menu in Builder mode"""
        if not self.player_controls_enabled:
            self.editor.log("⚠️ Switch to Player mode to use build menu", "warning")
            return
        
        # Log available build options
        self.editor.log("🏗️ BUILD MENU:", "info")
        self.editor.log("  1️⃣ - Place Cube", "show")
        self.editor.log("  2️⃣ - Place Sphere", "show")
        self.editor.log("  3️⃣ - Place Plane", "show")
        self.editor.log("  4️⃣ - Place Wall", "show")
        self.editor.log("  5️⃣ - Place Floor", "show")
        self.editor.log("  6️⃣ - Place Slope/Stairs", "show")
        self.editor.log("  7️⃣ - Place Light Block 💡", "show")
        self.editor.log("Press number keys to place objects in front of you!", "show")
        
        # Enable build mode flag
        if not hasattr(self, 'build_mode_active'):
            self.build_mode_active = False
        self.build_mode_active = True
    
    def quick_build(self, key):
        """Quick build object in front of player"""
        if not self.player:
            return
        
        # Calculate position in front of player
        import math
        yaw_rad = math.radians(self.camera.yaw)
        pitch_rad = math.radians(self.camera.pitch)
        distance = 3  # Place 3 units in front
        
        # Calculate 3D direction based on pitch and yaw
        # This allows placing blocks up/down based on where you're looking!
        x = self.player.position.x + math.sin(yaw_rad) * math.cos(pitch_rad) * distance
        y = self.player.position.y + math.sin(pitch_rad) * distance  # FIXED: Positive pitch = look up = place higher!
        z = self.player.position.z + math.cos(yaw_rad) * math.cos(pitch_rad) * distance
        
        # Snap to grid for better stacking
        grid_size = 1.0
        x = round(x / grid_size) * grid_size
        y = round(y / grid_size) * grid_size
        z = round(z / grid_size) * grid_size
        
        # Check if there's already a block at this position
        existing_block = None
        for shape in self.shapes:
            if isinstance(shape, Cube):
                # Check if positions are very close (within snapping tolerance)
                if (abs(shape.position.x - x) < 0.5 and 
                    abs(shape.position.y - y) < 0.5 and 
                    abs(shape.position.z - z) < 0.5):
                    existing_block = shape
                    break
        
        # If placing a wall and there's already a block, stack on top of it!
        if existing_block and key == '4':
            y = existing_block.position.y + existing_block.size * existing_block.scale.y
            self.editor.log("🧱 Stacking wall on top!", "info")
        
        # Create object based on key
        if key == '1':
            # Cube
            cube = Cube(Vector3D(x, y, z), 1.0)
            cube.color = "#888888"
            cube.has_collision = True
            self.shapes.append(cube)
            self.editor.log(f"📦 Placed Cube at Y={y:.1f}", "success")
        elif key == '2':
            # Sphere
            sphere = Sphere(Vector3D(x, y, z), 0.5)
            sphere.color = "#ff8800"
            sphere.has_collision = True  # Enable collision for sphere too!
            self.shapes.append(sphere)
            self.editor.log(f"⚪ Placed Sphere at Y={y:.1f}", "success")
        elif key == '3':
            # Plane
            plane = Plane(Vector3D(x, y, z), 5.0)
            plane.color = "#44aa44"
            plane.has_collision = True
            plane.is_static = True
            self.shapes.append(plane)
            self.editor.log(f"⬜ Placed Plane at Y={y:.1f}", "success")
        elif key == '4':
            # Wall (tall thin cube)
            wall = Cube(Vector3D(x, y, z), 1.0)
            wall.scale = Vector3D(2, 4, 0.5)
            wall.color = "#654321"
            wall.has_collision = True
            self.shapes.append(wall)
            self.editor.log(f"🧱 Placed Wall at Y={y:.1f}", "success")
        elif key == '5':
            # Floor/Roof (flat cube)
            floor = Cube(Vector3D(x, y, z), 1.0)
            floor.scale = Vector3D(3, 0.2, 3)
            floor.color = "#8b7355"
            floor.has_collision = True
            self.shapes.append(floor)
            # Check if placing above player (roof)
            if y > self.player.position.y + 1:
                self.editor.log(f"🏠 Placed Roof at Y={y:.1f}", "success")
            else:
                self.editor.log(f"⬛ Placed Floor at Y={y:.1f}", "success")
        elif key == '6':
            # Slope/Stairs (Wedge shape - proper ramp!)
            slope = Wedge(Vector3D(x, y, z), 1.0)
            slope.scale = Vector3D(2, 4, 3)  # Width 2, Height 4 (same as wall), Depth 3
            slope.color = "#a0826d"  # Light brown color
            slope.has_collision = True
            
            # Orient slope based on player's yaw direction
            # So it faces the direction you're looking
            slope.rotation.y = self.camera.yaw
            
            self.shapes.append(slope)
            self.editor.log(f"📐 Placed Wedge/Ramp at Y={y:.1f}", "success")
        elif key == '7':
            # Light Block (small glowing yellow cube)
            light = Cube(Vector3D(x, y, z), 0.5)  # Smaller size (0.5 instead of 1.0)
            light.color = "#ffff00"  # Bright yellow
            light.filled = True  # Auto-filled!
            light.light_level = 1.5  # Extra bright! (above 1.0 makes it glow)
            self.shapes.append(light)
            self.editor.log(f"💡 Placed Light Block at Y={y:.1f}", "success")
        
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
        # Always show in trajectory mode, AND show in Builder mode too!
        if self.selected_shape and self.gizmo_visible:
            if self.mode == self.MODE_TRAJECTORY or (self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER):
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
        
        # FILLED RENDERING (if shape.filled is True)
        if shape.filled and hasattr(shape, 'get_faces'):
            faces = shape.get_faces()
            
            for face in faces:
                # Get projected points for this face
                face_points = []
                valid_face = True
                for idx in face:
                    if idx < len(projected) and projected[idx]:
                        face_points.append(projected[idx])
                    else:
                        valid_face = False
                        break
                
                if valid_face and len(face_points) >= 3:
                    # Calculate face normal for shading
                    # Get 3D vertices for normal calculation
                    v0 = vertices[face[0]]
                    v1 = vertices[face[1]]
                    v2 = vertices[face[2]]
                    
                    # Two edges of the face
                    edge1 = Vector3D(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
                    edge2 = Vector3D(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
                    
                    # Cross product to get normal
                    normal = Vector3D(
                        edge1.y * edge2.z - edge1.z * edge2.y,
                        edge1.z * edge2.x - edge1.x * edge2.z,
                        edge1.x * edge2.y - edge1.y * edge2.x
                    )
                    
                    # Normalize
                    normal_len = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
                    if normal_len > 0:
                        normal.x /= normal_len
                        normal.y /= normal_len
                        normal.z /= normal_len
                    
                    # Camera direction (view vector)
                    face_center = Vector3D(
                        (v0.x + v1.x + v2.x) / 3,
                        (v0.y + v1.y + v2.y) / 3,
                        (v0.z + v1.z + v2.z) / 3
                    )
                    
                    view_dir = Vector3D(
                        self.camera.position.x - face_center.x,
                        self.camera.position.y - face_center.y,
                        self.camera.position.z - face_center.z
                    )
                    
                    view_len = math.sqrt(view_dir.x**2 + view_dir.y**2 + view_dir.z**2)
                    if view_len > 0:
                        view_dir.x /= view_len
                        view_dir.y /= view_len
                        view_dir.z /= view_len
                    
                    # Dot product for shading (how much face faces camera)
                    dot = normal.x * view_dir.x + normal.y * view_dir.y + normal.z * view_dir.z
                    
                    # Only draw faces facing camera (backface culling)
                    if dot > 0:
                        # Calculate brightness based on angle
                        brightness = abs(dot) * shape.light_level
                        brightness = max(0.2, min(1.0, brightness))  # Clamp between 0.2 and 1.0
                        
                        # Adjust color based on brightness
                        # Parse hex color
                        hex_color = shape.color.lstrip('#')
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        
                        # Apply brightness
                        r = int(r * brightness)
                        g = int(g * brightness)
                        b = int(b * brightness)
                        
                        shaded_color = f'#{r:02x}{g:02x}{b:02x}'
                        
                        # Draw filled polygon
                        flat_points = []
                        for px, py in face_points:
                            flat_points.extend([px, py])
                        
                        self.canvas.create_polygon(flat_points, fill=shaded_color, 
                                                   outline=shaded_color, width=1)
        
        # WIREFRAME RENDERING (always draw edges on top or if not filled)
        # Draw collision indicator (dashed lines for collision objects)
        if shape.has_collision:
            dash_pattern = (4, 2)  # Dashed line
        else:
            dash_pattern = ()  # Solid line
        
        # Only draw wireframe if not filled, or draw outline if filled
        if not shape.filled or shape == self.selected_shape:
            # Draw edges
            for edge in edges:
                if edge[0] < len(projected) and edge[1] < len(projected):
                    p1 = projected[edge[0]]
                    p2 = projected[edge[1]]
                    
                    if p1 and p2:
                        edge_color = color if not shape.filled else "#ffffff"
                        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                               fill=edge_color, width=width, dash=dash_pattern)
        
        # Draw collision badge if enabled
        if shape.has_collision and shape != self.selected_shape:
            center = self.project_3d_to_2d(shape.position)
            if center:
                self.canvas.create_text(center[0], center[1] - 30, 
                                       text="🛡️", font=("Arial", 16),
                                       fill="#00ffff")
    
    def draw_hud(self):
        """Draw game mode HUD"""
        # Focus warning if canvas doesn't have focus
        if not self.canvas_has_focus:
            # Big warning overlay
            overlay_alpha = int(128)  # Semi-transparent
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill="black", stipple="gray50", tags="focus_overlay"
            )
            
            # Warning text
            warning_y = self.height / 2 - 50
            self.canvas.create_text(
                self.width / 2, warning_y,
                text="⚠️ CLICK TO CONTROL",
                fill="#ffff00", font=("Segoe UI", 32, "bold"),
                tags="focus_warning"
            )
            
            self.canvas.create_text(
                self.width / 2, warning_y + 50,
                text="Click anywhere on this viewport to regain control",
                fill="white", font=("Segoe UI", 14),
                tags="focus_warning"
            )
            
            # Pulsing border
            border_width = 5
            self.canvas.create_rectangle(
                border_width, border_width,
                self.width - border_width, self.height - border_width,
                outline="#ffaa00", width=border_width, tags="focus_border"
            )
        
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
            
            # Gameplay mode indicator
            mode_text = f"Mode: {self.gameplay_mode}"
            self.canvas.create_text(10, 70, text=mode_text,
                                   anchor=tk.NW, fill="#ffaa00",
                                   font=("Consolas", 10, "bold"))
            
            # Controls reminder (varies by mode)
            if self.gameplay_mode == self.GAMEPLAY_MODE_SHOOTER:
                controls1 = "Arrow Keys: Look Around | LMB: Shoot"
                controls2 = "WASD: Move | Space: Jump | E: Interact | Tab: Toggle View"
            elif self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER:
                controls1 = "Arrow Keys: Look | Q: Build Menu | LMB: Place"
                controls2 = "WASD: Move | Space: Jump | Tab: Toggle View"
            elif self.gameplay_mode == self.GAMEPLAY_MODE_RPG:
                controls1 = "Arrow Keys: Look | I: Inventory | E: Interact"
                controls2 = "WASD: Move | Space: Jump | Q: Quest Log | Tab: Toggle View"
            else:  # Explorer and others
                controls1 = "Arrow Keys: Look Around | Tab: Toggle View"
                controls2 = "WASD: Move | Space: Jump | E: Interact"
            
            self.canvas.create_text(10, self.height - 40, 
                                   text=controls1,
                                   anchor=tk.NW, fill="#888888",
                                   font=("Consolas", 9))
            self.canvas.create_text(10, self.height - 20,
                                   text=controls2,
                                   anchor=tk.NW, fill="#888888",
                                   font=("Consolas", 9))
        
        # Draw weapon (Quake-style center gun)
        # Only show gun in Shooter mode
        if self.gameplay_mode == self.GAMEPLAY_MODE_SHOOTER:
            self.draw_weapon()
    
    def draw_weapon(self):
        """Draw Quake-style weapon in center bottom of screen (SHOOTER MODE ONLY)"""
        # Weapon position (center bottom)
        w_center_x = self.width / 2
        w_bottom_y = self.height - 80
        
        # Apply weapon bob/sway if moving
        bob_offset = 0
        sway_offset = 0
        if hasattr(self, 'player') and self.player:
            # Simple bob animation
            if not hasattr(self, 'weapon_bob_time'):
                self.weapon_bob_time = 0
            
            if any(k in self.keys_pressed for k in ['w', 'a', 's', 'd']):
                self.weapon_bob_time += 0.2
                bob_offset = math.sin(self.weapon_bob_time) * 3
                sway_offset = math.cos(self.weapon_bob_time * 0.5) * 2
        
        # Apply recoil animation
        recoil_offset = 0
        if hasattr(self, 'weapon_recoil_time'):
            if self.weapon_recoil_time > 0:
                recoil_offset = self.weapon_recoil_time * 15
                self.weapon_recoil_time -= 0.1
                if self.weapon_recoil_time < 0:
                    self.weapon_recoil_time = 0
        
        # Final weapon position
        weapon_x = w_center_x + sway_offset
        weapon_y = w_bottom_y + bob_offset + recoil_offset
        
        # Draw gun body (blue block - Quake style)
        gun_width = 80
        gun_height = 60
        gun_depth = 40
        
        # Main gun body (rectangle)
        self.canvas.create_rectangle(
            weapon_x - gun_width/2, weapon_y - gun_height,
            weapon_x + gun_width/2, weapon_y,
            fill="#3366ff", outline="#2244aa", width=2
        )
        
        # Gun barrel (darker rectangle on top)
        barrel_width = 20
        barrel_height = 40
        self.canvas.create_rectangle(
            weapon_x - barrel_width/2, weapon_y - gun_height - barrel_height,
            weapon_x + barrel_width/2, weapon_y - gun_height,
            fill="#1144aa", outline="#003388", width=2
        )
        
        # Gun highlights (to give it depth)
        self.canvas.create_line(
            weapon_x - gun_width/2, weapon_y - gun_height,
            weapon_x - gun_width/2 + 10, weapon_y - gun_height + 10,
            fill="#5588ff", width=2
        )
        
        # Gun grip (bottom part)
        grip_width = 30
        grip_height = 25
        self.canvas.create_rectangle(
            weapon_x - grip_width/2, weapon_y,
            weapon_x + grip_width/2, weapon_y + grip_height,
            fill="#2244aa", outline="#1133aa", width=2
        )
        
        # Muzzle flash if just shot
        if hasattr(self, 'show_muzzle_flash') and self.show_muzzle_flash:
            flash_size = 30
            flash_colors = ["#ffff00", "#ffaa00", "#ff6600"]
            for i, color in enumerate(flash_colors):
                size = flash_size - i * 10
                self.canvas.create_oval(
                    weapon_x - size, weapon_y - gun_height - barrel_height - size,
                    weapon_x + size, weapon_y - gun_height - barrel_height + size,
                    fill=color, outline=""
                )
            self.show_muzzle_flash = False
        
        # Ammo counter
        if hasattr(self.editor, 'interpreter'):
            ammo = self.editor.interpreter.variables.get('ammo', 30)
            magazine = self.editor.interpreter.variables.get('magazine', 30)
            self.canvas.create_text(
                self.width - 20, self.height - 80,
                text=f"{ammo}/{magazine}",
                anchor=tk.E, fill="white",
                font=("Consolas", 18, "bold")
            )
            
            # Ammo text
            self.canvas.create_text(
                self.width - 20, self.height - 60,
                text="AMMO",
                anchor=tk.E, fill="#888888",
                font=("Consolas", 10)
            )
    
    def shoot_weapon(self):
        """Fire the weapon (raycast) - SHOOTER MODE ONLY"""
        # Only allow shooting in Shooter mode
        if self.gameplay_mode != self.GAMEPLAY_MODE_SHOOTER:
            return
        
        if not hasattr(self.editor, 'interpreter'):
            return
        
        # Check ammo
        ammo = self.editor.interpreter.variables.get('ammo', 0)
        if ammo <= 0:
            self.editor.log("🔫 Click! Out of ammo!", "warning")
            return
        
        # Decrease ammo
        self.editor.interpreter.variables['ammo'] = ammo - 1
        
        # Trigger muzzle flash
        self.show_muzzle_flash = True
        
        # Trigger recoil
        if not hasattr(self, 'weapon_recoil_time'):
            self.weapon_recoil_time = 0
        self.weapon_recoil_time = 1.0
        
        # Raycast from camera position in look direction
        # Calculate ray direction from camera yaw and pitch
        yaw_rad = math.radians(self.camera.yaw)
        pitch_rad = math.radians(self.camera.pitch)
        
        # Ray direction
        dx = math.sin(yaw_rad) * math.cos(pitch_rad)
        dy = -math.sin(pitch_rad)
        dz = math.cos(yaw_rad) * math.cos(pitch_rad)
        
        # Ray start point (camera/player position)
        ray_start = self.camera.position
        ray_length = 1000  # Max distance
        
        # Check for hits
        hit_target = None
        closest_distance = ray_length
        
        for shape in self.shapes:
            if shape == self.player:
                continue
            
            # Simple sphere/box intersection test
            dx_to_shape = shape.position.x - ray_start.x
            dy_to_shape = shape.position.y - ray_start.y
            dz_to_shape = shape.position.z - ray_start.z
            
            distance_to_shape = math.sqrt(dx_to_shape**2 + dy_to_shape**2 + dz_to_shape**2)
            
            # Check if ray points towards shape
            dot = dx_to_shape * dx + dy_to_shape * dy + dz_to_shape * dz
            
            if dot > 0 and distance_to_shape < closest_distance:
                # Simple collision: check if close enough to ray line
                hit_threshold = shape.size * 1.5
                
                # Project point onto ray
                projection_length = dot / math.sqrt(dx**2 + dy**2 + dz**2)
                
                # Calculate distance from shape to ray line
                proj_x = ray_start.x + dx * projection_length
                proj_y = ray_start.y + dy * projection_length
                proj_z = ray_start.z + dz * projection_length
                
                dist_to_ray = math.sqrt(
                    (shape.position.x - proj_x)**2 +
                    (shape.position.y - proj_y)**2 +
                    (shape.position.z - proj_z)**2
                )
                
                if dist_to_ray < hit_threshold:
                    hit_target = shape
                    closest_distance = distance_to_shape
        
        # Process hit
        if hit_target:
            # Check if it's an NPC
            if hasattr(hit_target, 'is_npc') and hit_target.is_npc:
                # Initialize health if not set
                if not hasattr(hit_target, 'health'):
                    hit_target.health = 3
                
                # Damage enemy
                hit_target.health -= 2  # Gun damage
                
                self.editor.log(f"💥 Hit {hit_target.name}! HP: {hit_target.health}", "success")
                
                # Check if enemy died
                if hit_target.health <= 0:
                    self.editor.log(f"☠️ {hit_target.name} eliminated!", "success")
                    
                    # Remove from scene
                    if hit_target in self.shapes:
                        self.shapes.remove(hit_target)
                    
                    # Add score and kills
                    if hasattr(self.editor, 'interpreter'):
                        kills = self.editor.interpreter.variables.get('kills', 0)
                        self.editor.interpreter.variables['kills'] = kills + 1
                        
                        score = self.editor.interpreter.variables.get('score', 0)
                        self.editor.interpreter.variables['score'] = score + 10
                        
                        self.editor.log(f"🎯 +10 points! Score: {score + 10}", "success")
                else:
                    # Flash NPC (still alive)
                    original_color = hit_target.color
                    hit_target.color = "#ffff00"
                    self.render()
                    self.canvas.after(100, lambda: self.restore_hit_color(hit_target, original_color))
            else:
                self.editor.log(f"💥 Hit object!", "success")
                # Flash object
                original_color = hit_target.color
                hit_target.color = "#ff0000"
                self.render()
                self.canvas.after(100, lambda: self.restore_hit_color(hit_target, original_color))
        else:
            self.editor.log("💨 Miss!", "info")
        
        # Visual feedback - draw laser beam briefly
        self.draw_laser_beam(ray_start, dx, dy, dz, closest_distance)
        
        # Render to show muzzle flash
        self.render()
    
    def restore_hit_color(self, shape, color):
        """Restore shape color after hit"""
        shape.color = color
        self.render()
    
    def draw_laser_beam(self, start, dx, dy, dz, length):
        """Draw laser beam for visual feedback"""
        # Calculate end point
        end_x = start.x + dx * length
        end_y = start.y + dy * length
        end_z = start.z + dz * length
        
        # Project both points to screen
        start_2d = self.project_3d_to_2d(start)
        end_point = Vector3D(end_x, end_y, end_z)
        end_2d = self.project_3d_to_2d(end_point)
        
        if start_2d and end_2d:
            # Draw laser line
            self.canvas.create_line(
                start_2d[0], start_2d[1],
                end_2d[0], end_2d[1],
                fill="#00ff00", width=3, tags="laser"
            )
            
            # Remove laser after short delay
            self.canvas.after(50, lambda: self.canvas.delete("laser"))
    
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
        
        # Always grab focus when canvas is clicked
        self.canvas.focus_set()
        self.canvas_has_focus = True
        
        # Left click in GAME mode = SHOOT (but NOT in Builder mode!)
        if self.mode == self.MODE_GAME and self.player_controls_enabled:
            # Allow object selection in Builder mode
            if self.gameplay_mode != self.GAMEPLAY_MODE_BUILDER:
                self.shoot_weapon()
                return
            # In Builder mode, continue to object selection below
        
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
        
        # Otherwise, start camera rotation (only if not in first person)
        if not self.camera.is_first_person:
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
        
        # V key - Toggle fly/noclip in Builder mode
        if key == 'v':
            if self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER and self.player:
                # Toggle noclip mode
                if not hasattr(self, 'noclip_mode'):
                    self.noclip_mode = False
                
                self.noclip_mode = not self.noclip_mode
                
                if self.noclip_mode:
                    self.editor.log("✈️ FLY MODE ENABLED! (WASD to fly, QE up/down)", "success")
                    # Disable gravity
                    if hasattr(self.player, 'has_physics'):
                        self.player.has_physics = False
                else:
                    self.editor.log("🚶 WALK MODE (Gravity ON)", "info")
                    # Re-enable gravity
                    if hasattr(self.player, 'has_physics'):
                        self.player.has_physics = True
            
            self.keys_pressed.discard('v')
            return
        
        # I/O keys - Adjust height in Builder mode
        if self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER and self.player:
            if key == 'i':
                # Move up
                self.player.position.y += 0.5
                self.editor.log(f"⬆️ Height: {self.player.position.y:.1f}", "info")
                return
            elif key == 'o':
                # Move down
                self.player.position.y -= 0.5
                self.editor.log(f"⬇️ Height: {self.player.position.y:.1f}", "info")
                return
        
        # E key - Interact with NPCs
        if key == 'e':
            closest_npc = self.check_npc_proximity()
            if closest_npc:
                self.interact_with_npc(closest_npc)
            self.keys_pressed.discard('e')
            return
        
        # Tab key - Toggle Player/Viewport mode
        if key == 'tab':
            if self.player:
                self.toggle_player_viewport_mode()
            self.keys_pressed.discard('tab')
            return
        
        # Q key - Mode-specific actions
        if key == 'q':
            if self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER:
                # Open build menu in Builder mode (Q is not used for vertical movement in builder)
                self.show_build_menu()
            elif self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_RPG:
                # Open quest log (future implementation)
                self.editor.log("📜 Quest Log (Coming soon!)", "info")
            self.keys_pressed.discard('q')
            return
        
        # Number keys for quick building (Builder mode)
        if self.mode == self.MODE_GAME and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER and self.player_controls_enabled:
            if key in ['1', '2', '3', '4', '5', '6', '7']:
                self.quick_build(key)
                self.keys_pressed.discard(key)
                return
        
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
        
        # Gizmo shortcuts (only in trajectory mode and when not in first person)
        if self.mode == self.MODE_TRAJECTORY and not self.camera.is_first_person:
            if key == 'g':
                self.set_gizmo_mode('translate')
                self.keys_pressed.discard('g')
                return
            elif key == 'r':
                self.set_gizmo_mode('rotate')
                self.keys_pressed.discard('r')
                return
            elif key == 's' and not self.player_controls_enabled:
                # Only scale mode if player controls NOT enabled
                # This prevents conflict with S = move backward
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
    
    def on_canvas_focus_in(self, event):
        """Canvas gained focus"""
        self.canvas_has_focus = True
        self.render()  # Re-render to remove focus warning
    
    def on_canvas_focus_out(self, event):
        """Canvas lost focus"""
        self.canvas_has_focus = False
        self.render()  # Re-render to show focus warning
    
    def on_canvas_enter(self, event):
        """Mouse entered canvas - auto-grab focus in game mode"""
        if self.mode == self.MODE_GAME and self.player_controls_enabled:
            self.canvas.focus_set()
            self.canvas_has_focus = True
    
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
        
        # ========== ENEMY AI (FPS GAME) ==========
        # Make enemies chase player in Shooter mode
        if self.mode == self.MODE_GAME and self.player and self.player_controls_enabled and self.gameplay_mode == self.GAMEPLAY_MODE_SHOOTER:
            import math
            
            # Damage cooldown
            if not hasattr(self, 'damage_cooldown_timer'):
                self.damage_cooldown_timer = 0
            
            if self.damage_cooldown_timer > 0:
                self.damage_cooldown_timer -= 1
            
            # Update each enemy
            for shape in self.shapes:
                if not hasattr(shape, 'is_npc') or not shape.is_npc:
                    continue
                
                # Calculate distance to player
                dx = self.player.position.x - shape.position.x
                dy = self.player.position.y - shape.position.y
                dz = self.player.position.z - shape.position.z
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                # CHASE: Move toward player if within range
                if distance > 0.5 and distance < 20:
                    # Normalize direction and move
                    move_speed = 0.04  # Enemy speed
                    move_x = (dx / distance) * move_speed
                    move_z = (dz / distance) * move_speed
                    
                    # Move enemy
                    shape.position.x += move_x
                    shape.position.z += move_z
                    
                    # Keep enemy on ground
                    shape.position.y = 1.0
                
                # ATTACK: Damage player if very close
                if distance < 1.5 and self.damage_cooldown_timer == 0:
                    # Damage player
                    if hasattr(self.editor, 'interpreter'):
                        health = self.editor.interpreter.variables.get('health', 100)
                        health -= 5
                        self.editor.interpreter.variables['health'] = max(0, health)
                        self.damage_cooldown_timer = 30  # 0.5 second cooldown
                        
                        self.editor.log(f"💥 Enemy hit! Health: {health}", "warning")
                        
                        # Check game over
                        if health <= 0:
                            self.editor.log("☠️ GAME OVER!", "error")
                            score = self.editor.interpreter.variables.get('score', 0)
                            kills = self.editor.interpreter.variables.get('kills', 0)
                            self.editor.log(f"📊 Final Score: {score}", "show")
                            self.editor.log(f"👾 Kills: {kills}", "show")
                            self.editor.log("Press Tab to exit player mode", "info")
                            self.player_controls_enabled = False
        
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
            
            # Check NPC proximity
            self.check_npc_proximity()
        
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
        
        # Initialize noclip mode if not exists
        if not hasattr(self, 'noclip_mode'):
            self.noclip_mode = False
        
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
        
        # FLY MODE - Vertical movement with Q/E in Builder mode
        if self.noclip_mode and self.gameplay_mode == self.GAMEPLAY_MODE_BUILDER:
            if 'q' in self.keys_pressed:
                self.player.position.y -= move_speed
            if 'e' in self.keys_pressed:
                self.player.position.y += move_speed
        
        # Collision detection (skip if noclip enabled)
        if not self.noclip_mode:
            # Check horizontal collision with objects that have collision enabled
            # BUT: Don't push player away if they're jumping onto the top!
            collision_detected = False
            for shape in self.shapes:
                if shape == self.player or not shape.has_collision:
                    continue
                
                # Check if player is ABOVE the block (landing on top)
                player_bottom = self.player.position.y - self.player.size / 2
                block_top = shape.position.y + (shape.size * shape.scale.y) / 2
                
                # If player's bottom is above or near the block's top, they're landing on it
                # Don't do horizontal collision pushback!
                if player_bottom >= block_top - 0.3:
                    # Player is above block - allow landing, skip horizontal collision
                    continue
                
                # Player is at the SIDE of the block - check horizontal collision
                if self.check_collision_aabb(self.player, shape):
                    collision_detected = True
                    # Push player back horizontally
                    self.player.position.x = old_pos.x
                    self.player.position.z = old_pos.z
                    
                    # Stop movement in collision direction
                    dx = self.player.position.x - shape.position.x
                    dz = self.player.position.z - shape.position.z
                    
                    # Push player away slightly
                    if abs(dx) > abs(dz):
                        self.player.position.x = shape.position.x + (shape.size / 2 + self.player.size / 2) * (1 if dx > 0 else -1)
                    else:
                        self.player.position.z = shape.position.z + (shape.size / 2 + self.player.size / 2) * (1 if dz > 0 else -1)
                    
                    break
            
            # Apply gravity to player
            if not hasattr(self.player, 'velocity'):
                self.player.velocity = Vector3D(0, 0, 0)
            
            # Apply gravity
            self.player.velocity.y += self.gravity * self.dt
            
            # Update vertical position
            self.player.position.y += self.player.velocity.y * self.dt
            
            # Check if standing on collision block (for jumping)
            self.player.on_ground = False
            
            # First check for planes (ground)
            for shape in self.shapes:
                if isinstance(shape, Plane) and shape.is_static:
                    ground_level = shape.position.y + self.player.size / 2
                    if self.player.position.y <= ground_level:
                        self.player.position.y = ground_level
                        self.player.velocity.y = 0
                        self.player.on_ground = True
                        break
            
            # Then check for collision blocks to stand on
            if not self.player.on_ground:
                for shape in self.shapes:
                    if shape == self.player or not shape.has_collision:
                        continue
                    
                    # SPECIAL HANDLING FOR WEDGE RAMPS!
                    if isinstance(shape, Wedge):
                        # Calculate if player is on the ramp
                        # Wedge: low end at +Z (front), high end at -Z (back)
                        
                        # Check horizontal overlap (X and Z)
                        half_size_x = (shape.size * shape.scale.x) / 2
                        half_size_z = (shape.size * shape.scale.z) / 2
                        
                        # Transform player position relative to wedge (accounting for rotation)
                        yaw_rad = math.radians(shape.rotation.y)
                        
                        # Relative position (player - wedge center)
                        rel_x = self.player.position.x - shape.position.x
                        rel_z = self.player.position.z - shape.position.z
                        
                        # Rotate relative position by negative yaw to get local coordinates
                        local_x = rel_x * math.cos(-yaw_rad) - rel_z * math.sin(-yaw_rad)
                        local_z = rel_x * math.sin(-yaw_rad) + rel_z * math.cos(-yaw_rad)
                        
                        # Check if within wedge bounds (X and Z)
                        if abs(local_x) < half_size_x and abs(local_z) < half_size_z:
                            # Calculate height on slope based on Z position
                            # Wedge goes from bottom (Y = -sy) at front (Z = +sz) to top (Y = +sy) at back (Z = -sz)
                            half_height = (shape.size * shape.scale.y) / 2
                            
                            # Normalize Z position within wedge (0 at front, 1 at back)
                            # local_z ranges from -sz (back) to +sz (front)
                            z_normalized = (half_size_z - local_z) / (2 * half_size_z)  # 0 at front, 1 at back
                            z_normalized = max(0, min(1, z_normalized))  # Clamp to 0-1
                            
                            # Height on slope: interpolate from bottom to top
                            # Bottom (front, z=1): shape.y - half_height
                            # Top (back, z=0): shape.y + half_height
                            slope_height = shape.position.y - half_height + (z_normalized * 2 * half_height)
                            
                            # Check if player should be on the slope
                            player_bottom = self.player.position.y - self.player.size / 2
                            
                            if abs(player_bottom - slope_height) < 0.5:
                                # Snap player to slope surface!
                                self.player.position.y = slope_height + self.player.size / 2
                                self.player.velocity.y = 0
                                self.player.on_ground = True
                                break
                    
                    # Regular block collision (cubes, spheres, etc)
                    else:
                        # Check if player is on top of block
                        # Player's bottom should be at or slightly above block's top
                        player_bottom = self.player.position.y - self.player.size / 2
                        
                        # For spheres, use radius; for other shapes, use scale
                        if isinstance(shape, Sphere):
                            block_top = shape.position.y + (shape.size / 2)  # Sphere radius
                        else:
                            block_top = shape.position.y + (shape.size * shape.scale.y) / 2
                        
                        # Check horizontal overlap
                        if isinstance(shape, Sphere):
                            half_size_x = shape.size / 2
                            half_size_z = shape.size / 2
                        else:
                            half_size_x = (shape.size * shape.scale.x) / 2
                            half_size_z = (shape.size * shape.scale.z) / 2
                        
                        x_overlap = abs(self.player.position.x - shape.position.x) < (self.player.size / 2 + half_size_x)
                        z_overlap = abs(self.player.position.z - shape.position.z) < (self.player.size / 2 + half_size_z)
                        
                        # Check if standing on top
                        # Tolerance: 0.3 units for better landing (was 0.2, now more forgiving)
                        if x_overlap and z_overlap and abs(player_bottom - block_top) < 0.3:
                            # Snap player to top of block
                            self.player.position.y = block_top + self.player.size / 2
                            self.player.velocity.y = 0
                            self.player.on_ground = True
                            break
        else:
            # In noclip mode, always allow jumping/flying
            self.player.on_ground = True
        
        # Jump
        if 'space' in self.keys_pressed and self.player.on_ground and not self.noclip_mode:
            self.player.velocity.y = 5.0
            self.player.on_ground = False  # Leave ground when jumping
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
    
    # ==================== CODE PANEL ====================
    
    def setup_code_panel(self):
        """Setup the code panel UI"""
        # Header
        header = tk.Frame(self.code_panel_frame, bg="#1e1e1e")
        header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(header, text="3D CODE PANEL", bg="#1e1e1e", fg="#ffffff",
                font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(header, text="Run (F5)", command=self.run_code_panel,
                 bg="#0e639c", fg="white", relief=tk.FLAT, padx=8).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(header, text="Clear", command=self.clear_code_panel,
                 bg="#c24545", fg="white", relief=tk.FLAT, padx=8).pack(side=tk.RIGHT, padx=2)
        
        # Info label
        tk.Label(self.code_panel_frame, text="Write T# commands to control the 3D scene:",
                bg="#1e1e1e", fg="#888888", font=("Consolas", 8)).pack(anchor=tk.W, padx=10)
        
        # Code editor
        editor_frame = tk.Frame(self.code_panel_frame, bg="#1e1e1e")
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Line numbers
        self.code_line_numbers = tk.Text(editor_frame, width=4, bg="#252526", fg="#858585",
                                         font=("Consolas", 10), state=tk.DISABLED,
                                         relief=tk.FLAT, padx=5)
        self.code_line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(editor_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text editor
        self.code_editor = tk.Text(editor_frame, bg="#1e1e1e", fg="#d4d4d4",
                                   font=("Consolas", 10), insertbackground="white",
                                   yscrollcommand=scrollbar.set, wrap=tk.NONE,
                                   relief=tk.FLAT, padx=5, pady=5)
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.code_editor.yview)
        
        # Bind events
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.code_editor.bind('<F5>', lambda e: self.run_code_panel())
        
        # Default code
        default_code = """# 3D Code Panel - T# Commands
# Run with F5

# Example: Create objects
create3d cube at 0, 0, 0 size 2
color3d last3d to "blue"
physics3d on last3d

create3d sphere at 5, 2, 0 size 1
color3d last3d to "red"

# Example: Camera
camera at 0, 5, 15
lookat 0, 0, 0

# Example: NPC
npc "Guard" at -5, 0, 0
dialogue "Guard" says "Welcome to the village!"

say "3D scene ready!"
"""
        self.code_editor.insert("1.0", default_code)
        self.update_line_numbers()
        
        # Output/Console
        console_frame = tk.Frame(self.code_panel_frame, bg="#1e1e1e")
        console_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(console_frame, text="Output:", bg="#1e1e1e", fg="#cccccc",
                font=("Consolas", 9, "bold")).pack(anchor=tk.W)
        
        self.code_output = tk.Text(console_frame, height=8, bg="#0c0c0c", fg="#00ff00",
                                   font=("Consolas", 9), state=tk.DISABLED,
                                   relief=tk.FLAT, padx=5, pady=5)
        self.code_output.pack(fill=tk.X, pady=2)
    
    # ==================== GAMEPLAY MODE SIDEBAR ====================
    
    def setup_mode_sidebar(self):
        """Setup the gameplay mode sidebar"""
        # Header
        header = tk.Frame(self.mode_sidebar_frame, bg="#1e1e1e")
        header.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Label(header, text="GAMEPLAY MODE", bg="#1e1e1e", fg="#ffffff",
                font=("Segoe UI", 11, "bold")).pack(pady=5)
        
        tk.Label(header, text="Choose your playstyle:", bg="#1e1e1e", fg="#888888",
                font=("Segoe UI", 9)).pack()
        
        # Mode buttons container
        modes_frame = tk.Frame(self.mode_sidebar_frame, bg="#1e1e1e")
        modes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Define all 8 modes with descriptions
        modes = [
            (self.GAMEPLAY_MODE_SHOOTER, "FPS with gun & shooting", "#ff4444"),
            (self.GAMEPLAY_MODE_EXPLORER, "Free exploration mode", "#44ff44"),
            (self.GAMEPLAY_MODE_BUILDER, "Build & create freely", "#4444ff"),
            (self.GAMEPLAY_MODE_RPG, "Stats, quests, combat", "#ff44ff"),
            (self.GAMEPLAY_MODE_PUZZLE, "Logic & puzzles", "#ffaa44"),
            (self.GAMEPLAY_MODE_RACING, "Speed & vehicles", "#44ffff"),
            (self.GAMEPLAY_MODE_SURVIVAL, "Gather & survive", "#88ff44"),
            (self.GAMEPLAY_MODE_SANDBOX, "Do anything!", "#ff88ff"),
        ]
        
        self.mode_buttons = {}
        
        for mode_name, description, color in modes:
            # Mode button frame
            btn_frame = tk.Frame(modes_frame, bg="#2d2d2d", relief=tk.RAISED, bd=1)
            btn_frame.pack(fill=tk.X, pady=5)
            
            # Mode button
            btn = tk.Button(btn_frame, text=mode_name, 
                           command=lambda m=mode_name: self.set_gameplay_mode(m),
                           bg="#3c3c3c", fg="white", relief=tk.FLAT,
                           font=("Segoe UI", 10, "bold"),
                           activebackground=color, activeforeground="white",
                           cursor="hand2", pady=8)
            btn.pack(fill=tk.X, padx=2, pady=2)
            
            # Description
            tk.Label(btn_frame, text=description, bg="#2d2d2d", fg="#aaaaaa",
                    font=("Segoe UI", 8)).pack(padx=5, pady=(0, 5))
            
            self.mode_buttons[mode_name] = btn
        
        # Highlight current mode
        self.update_mode_buttons()
        
        # Info label
        info_frame = tk.Frame(self.mode_sidebar_frame, bg="#1e1e1e")
        info_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        
        tk.Label(info_frame, text="💡 Tip:", bg="#1e1e1e", fg="#ffaa00",
                font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        
        self.mode_info_label = tk.Label(info_frame, text="Explorer mode: No weapons, just explore!",
                                        bg="#1e1e1e", fg="#cccccc",
                                        font=("Segoe UI", 8), wraplength=180, justify=tk.LEFT)
        self.mode_info_label.pack(anchor=tk.W, pady=5)
    
    def toggle_mode_sidebar(self):
        """Toggle mode sidebar visibility"""
        if self.mode_sidebar_visible:
            # Hide sidebar
            self.mode_sidebar_frame.pack_forget()
            self.mode_sidebar_btn.config(text="⚙️ Mode")
            self.mode_sidebar_visible = False
        else:
            # Show sidebar
            self.mode_sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
            self.mode_sidebar_btn.config(text="✖ Mode")
            self.mode_sidebar_visible = True
    
    def set_gameplay_mode(self, mode):
        """Set the current gameplay mode"""
        self.gameplay_mode = mode
        self.update_mode_buttons()
        
        # Update info text
        mode_info = {
            self.GAMEPLAY_MODE_SHOOTER: "Shooter mode: Gun appears, left-click to shoot!",
            self.GAMEPLAY_MODE_EXPLORER: "Explorer mode: No weapons, just explore!",
            self.GAMEPLAY_MODE_BUILDER: "Builder mode: Focus on creating & building!",
            self.GAMEPLAY_MODE_RPG: "RPG mode: Stats, inventory, quests!",
            self.GAMEPLAY_MODE_PUZZLE: "Puzzle mode: Solve challenges!",
            self.GAMEPLAY_MODE_RACING: "Racing mode: Speed & vehicles!",
            self.GAMEPLAY_MODE_SURVIVAL: "Survival mode: Gather resources!",
            self.GAMEPLAY_MODE_SANDBOX: "Sandbox mode: Total freedom!",
        }
        
        self.mode_info_label.config(text=mode_info.get(mode, "Have fun!"))
        
        self.editor.log(f"🎮 Gameplay mode: {mode}", "success")
        
        # Re-render to apply changes
        self.render()
    
    def update_mode_buttons(self):
        """Update mode button highlights"""
        for mode_name, btn in self.mode_buttons.items():
            if mode_name == self.gameplay_mode:
                btn.config(bg="#0e639c", relief=tk.SUNKEN)
            else:
                btn.config(bg="#3c3c3c", relief=tk.FLAT)
    
    def toggle_code_panel(self):
        """Toggle code panel visibility"""
        if self.code_panel_visible:
            # Hide panel
            self.code_panel_frame.pack_forget()
            self.code_panel_toggle_btn.config(text="▶ Show Code Panel")
            self.code_panel_visible = False
        else:
            # Show panel
            self.code_panel_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
            self.code_panel_toggle_btn.config(text="◀ Hide Code Panel")
            self.code_panel_visible = True
    
    def update_line_numbers(self, event=None):
        """Update line numbers in code editor"""
        self.code_line_numbers.config(state=tk.NORMAL)
        self.code_line_numbers.delete("1.0", tk.END)
        
        # Get number of lines
        lines = self.code_editor.get("1.0", tk.END).split('\n')
        line_numbers = '\n'.join(str(i) for i in range(1, len(lines)))
        
        self.code_line_numbers.insert("1.0", line_numbers)
        self.code_line_numbers.config(state=tk.DISABLED)
    
    def run_code_panel(self):
        """Execute code from code panel"""
        code = self.code_editor.get("1.0", tk.END)
        
        # Clear output
        self.code_output.config(state=tk.NORMAL)
        self.code_output.delete("1.0", tk.END)
        
        # Log start
        self.log_code_output("Running 3D code...\n", "info")
        
        try:
            # Get T# interpreter
            if hasattr(self.editor, 'interpreter'):
                interpreter = self.editor.interpreter
                
                # IMPORTANT: Set the active viewport so commands work here
                interpreter.viewport_3d = self
                
                # Execute code
                interpreter.execute(code)
                
                self.log_code_output("Code executed successfully!\n", "success")
                self.log_code_output(f"Objects in scene: {len(self.shapes)}\n", "info")
                
                # Force render to show changes
                self.render()
            else:
                self.log_code_output("ERROR: Interpreter not available\n", "error")
        
        except Exception as e:
            self.log_code_output(f"ERROR: {str(e)}\n", "error")
            import traceback
            self.log_code_output(f"{traceback.format_exc()}\n", "error")
        
        self.code_output.config(state=tk.DISABLED)
    
    def clear_code_panel(self):
        """Clear code panel"""
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", "# Write your 3D T# code here\n")
        self.update_line_numbers()
    
    def log_code_output(self, message: str, level: str = "info"):
        """Log message to code panel output"""
        self.code_output.config(state=tk.NORMAL)
        
        # Color coding
        if level == "success":
            color = "#00ff00"
        elif level == "error":
            color = "#ff0000"
        elif level == "warning":
            color = "#ffaa00"
        else:
            color = "#00ff00"
        
        # Insert with color
        self.code_output.insert(tk.END, message)
        self.code_output.see(tk.END)
        self.code_output.config(state=tk.DISABLED)
    
    # ==================== NPC SYSTEM ====================
    
    def add_npc(self, name: str, x: float, y: float, z: float, color: str = "#9900ff"):
        """Add an NPC to the scene"""
        # NPCs are cubes now
        npc = Cube(Vector3D(x, y, z), 1.0)
        npc.color = color  # Default purple
        npc.is_static = True
        npc.has_collision = True
        npc.name = name
        npc.is_npc = True
        npc.dialogue_index = 0  # Track which dialogue line to show
        npc.in_range = False  # Track if player is in range
        
        self.shapes.append(npc)
        self.npcs.append(npc)
        
        # Initialize dialogue
        if name not in self.npc_dialogues:
            self.npc_dialogues[name] = []
        
        self.editor.log(f"👤 NPC '{name}' added at ({x}, {y}, {z})")
        self.render()
        
        return npc
    
    def add_npc_dialogue(self, npc_name: str, text: str):
        """Add dialogue line to NPC"""
        if npc_name not in self.npc_dialogues:
            self.npc_dialogues[npc_name] = []
        
        self.npc_dialogues[npc_name].append(text)
        self.editor.log(f"💬 Dialogue added to {npc_name}: \"{text}\"")
    
    def get_npc_dialogue(self, npc_name: str):
        """Get all dialogue for an NPC"""
        return self.npc_dialogues.get(npc_name, [])
    
    def show_npc_dialogue(self, npc_name: str, index: int = 0):
        """Show NPC dialogue in output window"""
        dialogues = self.get_npc_dialogue(npc_name)
        
        if dialogues and 0 <= index < len(dialogues):
            text = dialogues[index]
            
            # Show in output window
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.say(f"{npc_name}: {text}")
            
            self.editor.log(f"💬 {npc_name}: {text}")
            
            return text
        
        return None
    
    def check_npc_proximity(self):
        """Check if player is near any NPCs"""
        if not self.player or not self.npcs:
            return
        
        interaction_range = 3.0
        closest_npc = None
        closest_distance = float('inf')
        
        # Reset all NPCs
        for npc in self.npcs:
            npc.in_range = False
        
        for npc in self.npcs:
            # Calculate distance
            dx = self.player.position.x - npc.position.x
            dy = self.player.position.y - npc.position.y
            dz = self.player.position.z - npc.position.z
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            # If within interaction range
            if distance < interaction_range:
                npc.in_range = True
                if distance < closest_distance:
                    closest_distance = distance
                    closest_npc = npc
        
        # Show interaction prompt for closest NPC
        if closest_npc and hasattr(closest_npc, 'name'):
            # Show prompt in output window
            if hasattr(self.editor, 'output_window'):
                prompt = f"💬 Press E to talk to {closest_npc.name}"
                # Could display this as UI overlay
        
        return closest_npc
    
    def interact_with_npc(self, npc):
        """Interact with an NPC (show dialogue with sound effect)"""
        if hasattr(npc, 'name') and hasattr(npc, 'is_npc') and npc.is_npc:
            # Play sound effect
            self.play_dialogue_sound()
            
            # Get current dialogue index
            if not hasattr(npc, 'dialogue_index'):
                npc.dialogue_index = 0
            
            # Show dialogue
            dialogue_text = self.show_npc_dialogue(npc.name, npc.dialogue_index)
            
            if dialogue_text:
                # Advance to next dialogue line
                dialogues = self.get_npc_dialogue(npc.name)
                npc.dialogue_index = (npc.dialogue_index + 1) % len(dialogues) if dialogues else 0
                
                # Visual feedback - flash NPC color
                original_color = npc.color
                npc.color = "#ffffff"  # Flash white
                self.render()
                
                # Restore color after short delay
                self.canvas.after(100, lambda: self.restore_npc_color(npc, original_color))
    
    def restore_npc_color(self, npc, color):
        """Restore NPC color after interaction flash"""
        npc.color = color
        self.render()
    
    def play_dialogue_sound(self):
        """Play dialogue sound effect"""
        try:
            # Try to play a beep sound (cross-platform)
            import winsound
            winsound.Beep(800, 100)  # 800Hz for 100ms
        except:
            try:
                # Alternative for other platforms
                import os
                os.system('echo -e "\a"')  # Terminal bell
            except:
                # Silent fallback
                self.editor.log("🔊 *dialogue sound*")
                pass