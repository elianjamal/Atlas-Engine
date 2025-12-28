#!/usr/bin/env python3
"""
AtlasEngine - Editor Window
Main editor interface with viewport, script editor, and tools
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys

# Import other editor components
from editor.script_sidebar import ScriptSidebar
from editor.script_editor import ScriptEditor
from editor.log_panel import LogPanel
from editor.output_window import OutputWindow
from editor.ts_interpreter import TSInterpreter
from editor.ts_highlighter import TSHighlighter
from editor.trajectory_plotter import TrajectoryPlotter
from editor.viewport_3d import Viewport3D

class EditorWindow:
    """Main editor window for AtlasEngine"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AtlasEngine Editor v0.1")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")
        
        # Current project path
        self.project_path = None
        self.current_script = None
        
        # Initialize logger
        self.log_buffer = []
        
        # Setup UI
        self.setup_menubar()
        self.setup_main_layout()
        self.setup_status_bar()
        
        # Initialize T# interpreter
        self.interpreter = TSInterpreter(self)
        
        self.log("AtlasEngine Editor initialized")
        self.log(f"Python version: {sys.version}")
        self.log("Ready for creation")
    
    def setup_menubar(self):
        """Create the top menu bar"""
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white")
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project...", command=self.new_project)
        file_menu.add_command(label="Open Project...", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_script, accelerator="Ctrl+S")
        file_menu.add_command(label="Save All", command=self.save_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Script", command=self.run_script, accelerator="F5")
        run_menu.add_command(label="Stop", command=self.stop_script)
        run_menu.add_separator()
        run_menu.add_command(label="Clear Output", command=self.clear_output)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Script Sidebar", command=self.toggle_sidebar)
        view_menu.add_command(label="Toggle Log Panel", command=self.toggle_log)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard bindings
        self.root.bind("<Control-s>", lambda e: self.save_script())
        self.root.bind("<F5>", lambda e: self.run_script())
    
    def setup_main_layout(self):
        """Setup the main editor layout with panels"""
        # Main container
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, 
                                       bg="#1e1e1e", sashwidth=3)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Script sidebar
        self.sidebar = ScriptSidebar(main_container, self)
        main_container.add(self.sidebar.frame, minsize=200)
        
        # Center panel - Vertical split
        center_panel = tk.PanedWindow(main_container, orient=tk.VERTICAL,
                                     bg="#1e1e1e", sashwidth=3)
        main_container.add(center_panel, minsize=600)
        
        # Top of center - Tabs for editor and viewport
        self.notebook = ttk.Notebook(center_panel)
        center_panel.add(self.notebook, minsize=400)
        
        # Script Editor tab
        self.script_editor = ScriptEditor(self.notebook, self)
        self.notebook.add(self.script_editor.frame, text="Script Editor")
        
        # Trajectory Plotter tab
        self.plotter = TrajectoryPlotter(self.notebook, self)
        self.notebook.add(self.plotter.frame, text="Trajectory Plotter")
        
        # 3D Viewport tab
        self.viewport_3d = Viewport3D(self.notebook, self)
        self.notebook.add(self.viewport_3d.frame, text="3D Viewport")
        
        # Bottom of center - Horizontal split for Output and Log
        bottom_panel = tk.PanedWindow(center_panel, orient=tk.HORIZONTAL,
                                     bg="#1e1e1e", sashwidth=3)
        center_panel.add(bottom_panel, minsize=150)
        
        # Output Window (left side of bottom)
        self.output_window = OutputWindow(bottom_panel, self)
        bottom_panel.add(self.output_window.frame, minsize=400)
        
        # Log panel (right side of bottom)
        self.log_panel = LogPanel(bottom_panel, self)
        bottom_panel.add(self.log_panel.frame, minsize=300)
    
    def setup_status_bar(self):
        """Create the bottom status bar"""
        status_frame = tk.Frame(self.root, bg="#007acc", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg="#007acc",
            fg="white",
            anchor=tk.W,
            padx=10,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # File info
        self.file_info_label = tk.Label(
            status_frame,
            text="No file",
            bg="#007acc",
            fg="white",
            anchor=tk.E,
            padx=10,
            font=("Segoe UI", 9)
        )
        self.file_info_label.pack(side=tk.RIGHT)
    
    def new_project(self):
        """Create a new project"""
        path = filedialog.askdirectory(title="Select Project Location")
        if path:
            self.project_path = path
            self.log(f"New project created at: {path}")
            self.sidebar.load_scripts(path)
            self.update_status(f"Project: {os.path.basename(path)}")
    
    def open_project(self):
        """Open an existing project"""
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.project_path = path
            self.log(f"Opened project: {path}")
            self.sidebar.load_scripts(path)
            self.update_status(f"Project: {os.path.basename(path)}")
    
    def save_script(self):
        """Save current script"""
        if self.current_script:
            self.script_editor.save(self.current_script)
            self.log(f"Saved: {os.path.basename(self.current_script)}")
        else:
            self.save_script_as()
    
    def save_script_as(self):
        """Save script with new name"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".ts",
            filetypes=[("T# Scripts", "*.ts"), ("All Files", "*.*")]
        )
        if filepath:
            self.script_editor.save(filepath)
            self.current_script = filepath
            self.log(f"Saved as: {os.path.basename(filepath)}")
    
    def save_all(self):
        """Save all open scripts"""
        if self.current_script:
            self.save_script()
        self.log("All scripts saved")
    
    def run_script(self):
        """Run the current T# script"""
        content = self.script_editor.get_content()
        if content.strip():
            self.log("="*50)
            self.log("Running script...")
            self.log("="*50)
            self.interpreter.execute(content)
        else:
            self.log("No script to run", "warning")
    
    def stop_script(self):
        """Stop script execution"""
        self.log("Script execution stopped", "warning")
    
    def clear_output(self):
        """Clear the log panel"""
        self.log_panel.clear()
    
    def toggle_sidebar(self):
        """Toggle script sidebar visibility"""
        pass  # Implement panel hiding
    
    def toggle_log(self):
        """Toggle log panel visibility"""
        pass  # Implement panel hiding
    
    def show_docs(self):
        """Show documentation"""
        messagebox.showinfo(
            "Documentation",
            "AtlasEngine v0.1\n\n"
            "T# Scripting Language Features:\n"
            "- Variables: var x = 10\n"
            "- Functions: func name(args) { }\n"
            "- Print: print('text')\n"
            "- Game objects: spawn, move, rotate\n\n"
            "More documentation coming soon!"
        )
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About AtlasEngine",
            "AtlasEngine v0.1\n"
            "Professional Game Engine\n\n"
            "Features:\n"
            "• T# Scripting Language\n"
            "• Integrated Editor\n"
            "• Real-time Preview\n"
            "• Project Management\n\n"
            "Built with Python & Tkinter"
        )
    
    def undo(self):
        """Undo last action"""
        try:
            self.script_editor.text_widget.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Redo last action"""
        try:
            self.script_editor.text_widget.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Cut selected text"""
        self.script_editor.text_widget.event_generate("<<Cut>>")
    
    def copy(self):
        """Copy selected text"""
        self.script_editor.text_widget.event_generate("<<Copy>>")
    
    def paste(self):
        """Paste text"""
        self.script_editor.text_widget.event_generate("<<Paste>>")
    
    def log(self, message, level="info"):
        """Log a message to the output panel"""
        self.log_panel.log(message, level)
    
    def update_status(self, text):
        """Update status bar text"""
        self.status_label.config(text=text)
    
    def update_file_info(self, text):
        """Update file info in status bar"""
        self.file_info_label.config(text=text)