#!/usr/bin/env python3
"""
AtlasEngine - Trajectory Plotter
Visualizes trajectories, graphs, and scientific data
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import List, Tuple

class TrajectoryPlotter:
    """Interactive trajectory and graph plotter"""
    
    def __init__(self, parent, editor):
        self.editor = editor
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        
        # Control panel
        self.setup_controls()
        
        # Canvas for plotting
        self.canvas = tk.Canvas(
            self.frame,
            bg="#2b2b2b",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas dimensions
        self.width = 800
        self.height = 600
        self.margin = 50
        
        # Data storage
        self.trajectories = []
        self.colors = ['#00ff00', '#ff0000', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
        self.color_index = 0
        
        # Bind resize
        self.canvas.bind('<Configure>', self.on_resize)
    
    def setup_controls(self):
        """Setup control panel"""
        control_frame = tk.Frame(self.frame, bg="#252526", height=60)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        control_frame.pack_propagate(False)
        
        # Title
        tk.Label(
            control_frame,
            text="TRAJECTORY PLOTTER",
            bg="#252526",
            fg="#cccccc",
            font=("Segoe UI", 10, "bold")
        ).pack(side=tk.LEFT, padx=10)
        
        # Clear button
        tk.Button(
            control_frame,
            text="Clear",
            command=self.clear_plot,
            bg="#0e639c",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            font=("Segoe UI", 9)
        ).pack(side=tk.RIGHT, padx=5)
        
        # Grid toggle
        self.show_grid = tk.BooleanVar(value=True)
        tk.Checkbutton(
            control_frame,
            text="Grid",
            variable=self.show_grid,
            command=self.redraw,
            bg="#252526",
            fg="#cccccc",
            selectcolor="#3c3c3c"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Axes toggle
        self.show_axes = tk.BooleanVar(value=True)
        tk.Checkbutton(
            control_frame,
            text="Axes",
            variable=self.show_axes,
            command=self.redraw,
            bg="#252526",
            fg="#cccccc",
            selectcolor="#3c3c3c"
        ).pack(side=tk.RIGHT, padx=5)
    
    def on_resize(self, event):
        """Handle canvas resize"""
        self.width = event.width
        self.height = event.height
        self.redraw()
    
    def clear_plot(self):
        """Clear all plotted data"""
        self.trajectories = []
        self.color_index = 0
        self.canvas.delete("all")
        self.draw_axes()
        self.editor.log("Plot cleared")
    
    def plot_trajectory(self, points: List[Tuple[float, float]], 
                       label: str = "", color: str = None):
        """
        Plot a trajectory or graph
        
        Args:
            points: List of (x, y) tuples
            label: Label for this trajectory
            color: Line color (auto-assigned if None)
        """
        if not points:
            return
        
        if color is None:
            color = self.colors[self.color_index % len(self.colors)]
            self.color_index += 1
        
        self.trajectories.append({
            'points': points,
            'label': label,
            'color': color
        })
        
        self.redraw()
        self.editor.log(f"Plotted: {label} ({len(points)} points)", "success")
    
    def plot_function(self, func, x_min: float, x_max: float, 
                     points: int = 200, label: str = ""):
        """
        Plot a mathematical function
        
        Args:
            func: Function to plot (takes x, returns y)
            x_min: Minimum x value
            x_max: Maximum x value
            points: Number of points to plot
            label: Function label
        """
        trajectory_points = []
        dx = (x_max - x_min) / points
        
        for i in range(points + 1):
            x = x_min + i * dx
            try:
                y = func(x)
                trajectory_points.append((x, y))
            except:
                continue
        
        self.plot_trajectory(trajectory_points, label)
    
    def redraw(self):
        """Redraw the entire plot"""
        self.canvas.delete("all")
        
        if not self.trajectories:
            self.draw_axes()
            return
        
        # Find data bounds
        all_points = []
        for traj in self.trajectories:
            all_points.extend(traj['points'])
        
        if not all_points:
            return
        
        x_coords = [p[0] for p in all_points]
        y_coords = [p[1] for p in all_points]
        
        self.x_min = min(x_coords)
        self.x_max = max(x_coords)
        self.y_min = min(y_coords)
        self.y_max = max(y_coords)
        
        # Add padding
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        if x_range == 0:
            x_range = 1
        if y_range == 0:
            y_range = 1
        
        self.x_min -= x_range * 0.1
        self.x_max += x_range * 0.1
        self.y_min -= y_range * 0.1
        self.y_max += y_range * 0.1
        
        # Draw components
        if self.show_grid.get():
            self.draw_grid()
        
        if self.show_axes.get():
            self.draw_axes()
        
        self.draw_trajectories()
        self.draw_legend()
    
    def world_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = self.margin + (x - self.x_min) / (self.x_max - self.x_min) * (self.width - 2 * self.margin)
        screen_y = self.height - self.margin - (y - self.y_min) / (self.y_max - self.y_min) * (self.height - 2 * self.margin)
        return (int(screen_x), int(screen_y))
    
    def draw_grid(self):
        """Draw background grid"""
        # Vertical lines
        for i in range(11):
            x = self.margin + i * (self.width - 2 * self.margin) / 10
            self.canvas.create_line(
                x, self.margin,
                x, self.height - self.margin,
                fill="#3c3c3c",
                width=1
            )
        
        # Horizontal lines
        for i in range(11):
            y = self.margin + i * (self.height - 2 * self.margin) / 10
            self.canvas.create_line(
                self.margin, y,
                self.width - self.margin, y,
                fill="#3c3c3c",
                width=1
            )
    
    def draw_axes(self):
        """Draw coordinate axes"""
        # X-axis
        if self.trajectories and self.y_min <= 0 <= self.y_max:
            y_screen = self.world_to_screen(0, 0)[1]
        else:
            y_screen = self.height - self.margin
        
        self.canvas.create_line(
            self.margin, y_screen,
            self.width - self.margin, y_screen,
            fill="#666666",
            width=2,
            arrow=tk.LAST
        )
        
        # Y-axis
        if self.trajectories and self.x_min <= 0 <= self.x_max:
            x_screen = self.world_to_screen(0, 0)[0]
        else:
            x_screen = self.margin
        
        self.canvas.create_line(
            x_screen, self.height - self.margin,
            x_screen, self.margin,
            fill="#666666",
            width=2,
            arrow=tk.LAST
        )
        
        # Labels
        if self.trajectories:
            # X-axis labels
            for i in range(5):
                x_val = self.x_min + (self.x_max - self.x_min) * i / 4
                x_screen, y_screen = self.world_to_screen(x_val, self.y_min)
                self.canvas.create_text(
                    x_screen,
                    self.height - self.margin + 20,
                    text=f"{x_val:.1f}",
                    fill="#999999",
                    font=("Consolas", 8)
                )
            
            # Y-axis labels
            for i in range(5):
                y_val = self.y_min + (self.y_max - self.y_min) * i / 4
                x_screen, y_screen = self.world_to_screen(self.x_min, y_val)
                self.canvas.create_text(
                    self.margin - 25,
                    y_screen,
                    text=f"{y_val:.1f}",
                    fill="#999999",
                    font=("Consolas", 8)
                )
    
    def draw_trajectories(self):
        """Draw all trajectories"""
        for traj in self.trajectories:
            points = traj['points']
            color = traj['color']
            
            # Convert to screen coordinates
            screen_points = [self.world_to_screen(x, y) for x, y in points]
            
            # Draw lines
            for i in range(len(screen_points) - 1):
                x1, y1 = screen_points[i]
                x2, y2 = screen_points[i + 1]
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=2
                )
            
            # Draw points
            for x, y in screen_points[::max(1, len(screen_points) // 50)]:
                self.canvas.create_oval(
                    x - 2, y - 2, x + 2, y + 2,
                    fill=color,
                    outline=color
                )
    
    def draw_legend(self):
        """Draw legend for trajectories"""
        legend_x = self.width - 150
        legend_y = 20
        
        for i, traj in enumerate(self.trajectories):
            if traj['label']:
                y_pos = legend_y + i * 25
                
                # Color box
                self.canvas.create_rectangle(
                    legend_x, y_pos,
                    legend_x + 20, y_pos + 10,
                    fill=traj['color'],
                    outline=traj['color']
                )
                
                # Label
                self.canvas.create_text(
                    legend_x + 25,
                    y_pos + 5,
                    text=traj['label'],
                    fill="#cccccc",
                    anchor=tk.W,
                    font=("Consolas", 9)
                )
    
    def plot_parametric(self, x_func, y_func, t_min: float, t_max: float,
                       points: int = 200, label: str = ""):
        """
        Plot parametric equations
        
        Args:
            x_func: Function for x coordinate (takes t)
            y_func: Function for y coordinate (takes t)
            t_min: Minimum parameter value
            t_max: Maximum parameter value
            points: Number of points
            label: Curve label
        """
        trajectory_points = []
        dt = (t_max - t_min) / points
        
        for i in range(points + 1):
            t = t_min + i * dt
            try:
                x = x_func(t)
                y = y_func(t)
                trajectory_points.append((x, y))
            except:
                continue
        
        self.plot_trajectory(trajectory_points, label)
    
    def plot_polar(self, r_func, theta_min: float = 0, theta_max: float = 2*math.pi,
                  points: int = 200, label: str = ""):
        """
        Plot polar equation
        
        Args:
            r_func: Function for radius (takes theta)
            theta_min: Minimum angle (radians)
            theta_max: Maximum angle (radians)
            points: Number of points
            label: Curve label
        """
        trajectory_points = []
        dtheta = (theta_max - theta_min) / points
        
        for i in range(points + 1):
            theta = theta_min + i * dtheta
            try:
                r = r_func(theta)
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                trajectory_points.append((x, y))
            except:
                continue
        
        self.plot_trajectory(trajectory_points, label)
