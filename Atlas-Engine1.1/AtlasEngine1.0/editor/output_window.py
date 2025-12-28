#!/usr/bin/env python3
"""
AtlasEngine - Output Window
Displays script output with text and 2D sprite rendering for RPG games
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Dict, List, Tuple
import math

class Sprite:
    """Simple 2D sprite for the output window"""
    def __init__(self, x, y, width, height, color="#00ff00", text="", image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.image = image
        self.visible = True
        self.layer = 0  # Drawing order
        self.tags = []
    
    def move(self, dx, dy):
        """Move sprite by delta"""
        self.x += dx
        self.y += dy
    
    def move_to(self, x, y):
        """Move sprite to position"""
        self.x = x
        self.y = y

class OutputWindow:
    """Output window with text and 2D sprite rendering"""
    
    def __init__(self, parent, editor):
        self.editor = editor
        
        # Main frame
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        
        # Title bar
        title_bar = tk.Frame(self.frame, bg="#2d2d2d", height=30)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text="OUTPUT", bg="#2d2d2d", fg="#cccccc",
                font=("Segoe UI", 10, "bold"), padx=10).pack(side=tk.LEFT)
        
        # Mode selector
        self.mode_var = tk.StringVar(value="text")
        
        tk.Radiobutton(title_bar, text="Text", variable=self.mode_var, value="text",
                      command=self.switch_mode, bg="#2d2d2d", fg="#cccccc",
                      selectcolor="#1e1e1e", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(title_bar, text="Graphics", variable=self.mode_var, value="graphics",
                      command=self.switch_mode, bg="#2d2d2d", fg="#cccccc",
                      selectcolor="#1e1e1e", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Clear button
        tk.Button(title_bar, text="Clear", command=self.clear,
                 bg="#3c3c3c", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=5)
        
        # Container for modes
        self.content_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text mode
        self.text_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        self.text_output = scrolledtext.ScrolledText(
            self.text_frame,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            insertbackground="#ffffff",
            selectbackground="#264f78",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.text_output.tag_config("info", foreground="#569cd6")
        self.text_output.tag_config("success", foreground="#4ec9b0")
        self.text_output.tag_config("warning", foreground="#dcdcaa")
        self.text_output.tag_config("error", foreground="#f48771")
        self.text_output.tag_config("shout", foreground="#ff6b6b", font=("Consolas", 11, "bold"))
        self.text_output.tag_config("whisper", foreground="#888888", font=("Consolas", 9))
        
        # Graphics mode
        self.graphics_frame = tk.Frame(self.content_frame, bg="#000000")
        
        # Canvas for 2D graphics
        self.canvas = tk.Canvas(
            self.graphics_frame,
            bg="#000000",
            highlightthickness=0,
            width=800,
            height=600
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Sprite management
        self.sprites: Dict[str, Sprite] = {}
        self.sprite_canvas_ids: Dict[str, List] = {}  # Canvas item IDs for each sprite
        
        # Show text mode by default
        self.current_mode = "text"
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Rendering
        self.is_rendering = False
    
    def switch_mode(self):
        """Switch between text and graphics mode"""
        new_mode = self.mode_var.get()
        
        if new_mode == self.current_mode:
            return
        
        # Hide current mode
        if self.current_mode == "text":
            self.text_frame.pack_forget()
        else:
            self.graphics_frame.pack_forget()
        
        # Show new mode
        if new_mode == "text":
            self.text_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.render_sprites()
        
        self.current_mode = new_mode
        self.editor.log(f"Output mode: {new_mode}", "info")
    
    def clear(self):
        """Clear output"""
        if self.current_mode == "text":
            self.text_output.delete(1.0, tk.END)
        else:
            self.canvas.delete("all")
            self.sprites.clear()
            self.sprite_canvas_ids.clear()
    
    # ========== TEXT OUTPUT METHODS ==========
    
    def write(self, text: str, tag: str = None):
        """Write text to output"""
        self.text_output.insert(tk.END, text + "\n", tag)
        self.text_output.see(tk.END)
    
    def write_line(self, text: str, tag: str = None):
        """Write line with optional tag"""
        self.write(text, tag)
    
    def say(self, text: str):
        """Say command - normal output"""
        self.write(f"💬 {text}")
    
    def shout(self, text: str):
        """Shout command - emphasized output"""
        self.write(f"📢 {text.upper()}", "shout")
    
    def whisper(self, text: str):
        """Whisper command - subtle output"""
        self.write(f"🤫 {text}", "whisper")
    
    def show(self, value):
        """Show value"""
        self.write(f"👁️  {value}")
    
    def info(self, text: str):
        """Info message"""
        self.write(f"ℹ️  {text}", "info")
    
    def success(self, text: str):
        """Success message"""
        self.write(f"✓ {text}", "success")
    
    def warning(self, text: str):
        """Warning message"""
        self.write(f"⚠️  {text}", "warning")
    
    def error(self, text: str):
        """Error message"""
        self.write(f"✗ {text}", "error")
    
    # ========== GRAPHICS/SPRITE METHODS ==========
    
    def create_sprite(self, name: str, x: float, y: float, width: float, height: float,
                     color: str = "#00ff00", text: str = "", layer: int = 0):
        """Create a new sprite"""
        sprite = Sprite(x, y, width, height, color, text)
        sprite.layer = layer
        self.sprites[name] = sprite
        self.sprite_canvas_ids[name] = []
        
        if self.current_mode == "graphics":
            self.render_sprites()
    
    def create_rect_sprite(self, name: str, x: float, y: float, width: float, height: float,
                          color: str = "#00ff00", layer: int = 0):
        """Create rectangle sprite"""
        self.create_sprite(name, x, y, width, height, color, "", layer)
    
    def create_circle_sprite(self, name: str, x: float, y: float, radius: float,
                            color: str = "#00ff00", layer: int = 0):
        """Create circle sprite"""
        sprite = Sprite(x - radius, y - radius, radius * 2, radius * 2, color)
        sprite.layer = layer
        sprite.tags.append("circle")
        self.sprites[name] = sprite
        self.sprite_canvas_ids[name] = []
        
        if self.current_mode == "graphics":
            self.render_sprites()
    
    def create_text_sprite(self, name: str, x: float, y: float, text: str,
                          color: str = "#ffffff", size: int = 12, layer: int = 0):
        """Create text sprite"""
        sprite = Sprite(x, y, 0, 0, color, text)
        sprite.layer = layer
        sprite.tags.append("text")
        self.sprites[name] = sprite
        self.sprite_canvas_ids[name] = []
        
        if self.current_mode == "graphics":
            self.render_sprites()
    
    def move_sprite(self, name: str, dx: float, dy: float):
        """Move sprite by delta"""
        if name in self.sprites:
            self.sprites[name].move(dx, dy)
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def move_sprite_to(self, name: str, x: float, y: float):
        """Move sprite to position"""
        if name in self.sprites:
            self.sprites[name].move_to(x, y)
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def change_sprite_color(self, name: str, color: str):
        """Change sprite color"""
        if name in self.sprites:
            self.sprites[name].color = color
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def change_sprite_text(self, name: str, text: str):
        """Change sprite text"""
        if name in self.sprites:
            self.sprites[name].text = text
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def show_sprite(self, name: str):
        """Show sprite"""
        if name in self.sprites:
            self.sprites[name].visible = True
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def hide_sprite(self, name: str):
        """Hide sprite"""
        if name in self.sprites:
            self.sprites[name].visible = False
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def delete_sprite(self, name: str):
        """Delete sprite"""
        if name in self.sprites:
            del self.sprites[name]
            if name in self.sprite_canvas_ids:
                del self.sprite_canvas_ids[name]
            if self.current_mode == "graphics":
                self.render_sprites()
    
    def render_sprites(self):
        """Render all sprites to canvas"""
        if self.is_rendering:
            return
        
        self.is_rendering = True
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Sort sprites by layer
        sorted_sprites = sorted(self.sprites.items(), key=lambda x: x[1].layer)
        
        # Draw each sprite
        for name, sprite in sorted_sprites:
            if not sprite.visible:
                continue
            
            if "circle" in sprite.tags:
                # Draw circle
                self.canvas.create_oval(
                    sprite.x, sprite.y,
                    sprite.x + sprite.width, sprite.y + sprite.height,
                    fill=sprite.color, outline=sprite.color
                )
            elif "text" in sprite.tags:
                # Draw text
                self.canvas.create_text(
                    sprite.x, sprite.y,
                    text=sprite.text,
                    fill=sprite.color,
                    font=("Arial", 12),
                    anchor=tk.NW
                )
            else:
                # Draw rectangle
                self.canvas.create_rectangle(
                    sprite.x, sprite.y,
                    sprite.x + sprite.width, sprite.y + sprite.height,
                    fill=sprite.color, outline=sprite.color
                )
                
                # Draw text if present
                if sprite.text:
                    self.canvas.create_text(
                        sprite.x + sprite.width / 2,
                        sprite.y + sprite.height / 2,
                        text=sprite.text,
                        fill="#ffffff",
                        font=("Arial", 10)
                    )
        
        self.is_rendering = False
    
    # ========== DRAWING PRIMITIVES ==========
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "#ffffff", width: int = 2):
        """Draw a line - ALWAYS works, auto-switches to graphics"""
        # Force switch to graphics mode
        if self.current_mode != "graphics":
            self.mode_var.set("graphics")
            # Manually switch
            self.text_frame.pack_forget()
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.current_mode = "graphics"
        
        # Draw on canvas
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        self.canvas.update_idletasks()
    
    def draw_rect(self, x: float, y: float, width: float, height: float, color: str = "#ffffff", filled: bool = True):
        """Draw a rectangle - ALWAYS works, auto-switches to graphics"""
        # Force switch to graphics mode
        if self.current_mode != "graphics":
            self.mode_var.set("graphics")
            self.text_frame.pack_forget()
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.current_mode = "graphics"
        
        # Draw on canvas
        if filled:
            self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline=color)
        else:
            self.canvas.create_rectangle(x, y, x + width, y + height, outline=color, width=2)
        self.canvas.update_idletasks()
    
    def draw_circle(self, x: float, y: float, radius: float, color: str = "#ffffff", filled: bool = True):
        """Draw a circle - ALWAYS works, auto-switches to graphics"""
        # Force switch to graphics mode
        if self.current_mode != "graphics":
            self.mode_var.set("graphics")
            self.text_frame.pack_forget()
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.current_mode = "graphics"
        
        # Draw on canvas
        if filled:
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                   fill=color, outline=color)
        else:
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                   outline=color, width=2)
        self.canvas.update_idletasks()
    
    def draw_text(self, x: float, y: float, text: str, color: str = "#ffffff", size: int = 12):
        """Draw text - ALWAYS works, auto-switches to graphics"""
        # Force switch to graphics mode
        if self.current_mode != "graphics":
            self.mode_var.set("graphics")
            self.text_frame.pack_forget()
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.current_mode = "graphics"
        
        # Draw on canvas
        self.canvas.create_text(x, y, text=text, fill=color, font=("Arial", size))
        self.canvas.update_idletasks()
    
    def fill_screen(self, color: str):
        """Fill entire screen with color - ALWAYS works, auto-switches to graphics"""
        # Force switch to graphics mode
        if self.current_mode != "graphics":
            self.mode_var.set("graphics")
            self.text_frame.pack_forget()
            self.graphics_frame.pack(fill=tk.BOTH, expand=True)
            self.current_mode = "graphics"
        
        # Set background
        self.canvas.config(bg=color)
        self.canvas.update_idletasks()
    
    # ========== HELPER METHODS ==========
    
    def get_canvas_size(self) -> Tuple[int, int]:
        """Get canvas dimensions"""
        return (self.canvas.winfo_width(), self.canvas.winfo_height())
    
    def sprite_exists(self, name: str) -> bool:
        """Check if sprite exists"""
        return name in self.sprites
    
    def get_sprite_position(self, name: str) -> Tuple[float, float]:
        """Get sprite position"""
        if name in self.sprites:
            sprite = self.sprites[name]
            return (sprite.x, sprite.y)
        return (0, 0)
    
    def count_sprites(self) -> int:
        """Get number of sprites"""
        return len(self.sprites)