#!/usr/bin/env python3
"""
AtlasEngine - Script Sidebar
Manages and displays available scripts in the project
"""

import tkinter as tk
from tkinter import ttk
import os

class ScriptSidebar:
    """Sidebar for managing scripts"""
    
    def __init__(self, parent, editor):
        self.editor = editor
        
        # Create frame
        self.frame = tk.Frame(parent, bg="#252526", width=250)
        
        # Title
        title = tk.Label(
            self.frame,
            text="SCRIPTS",
            bg="#252526",
            fg="#cccccc",
            font=("Segoe UI", 10, "bold"),
            pady=5
        )
        title.pack(fill=tk.X)
        
        # Toolbar
        toolbar = tk.Frame(self.frame, bg="#252526")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = tk.Button(
            toolbar,
            text="+ New",
            command=self.new_script,
            bg="#0e639c",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            font=("Segoe UI", 9)
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        remove_btn = tk.Button(
            toolbar,
            text="− Remove",
            command=self.remove_script,
            bg="#3c3c3c",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            font=("Segoe UI", 9)
        )
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        # Script list
        list_frame = tk.Frame(self.frame, bg="#1e1e1e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.script_list = tk.Listbox(
            list_frame,
            bg="#1e1e1e",
            fg="#cccccc",
            selectbackground="#094771",
            selectforeground="white",
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT
        )
        self.script_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.script_list.yview)
        
        # Bind double-click to open script
        self.script_list.bind("<Double-Button-1>", self.open_selected)
        
        self.scripts = []
    
    def load_scripts(self, path):
        """Load all .ts scripts from project directory"""
        self.script_list.delete(0, tk.END)
        self.scripts = []
        
        if not os.path.exists(path):
            return
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.ts'):
                    full_path = os.path.join(root, file)
                    self.scripts.append(full_path)
                    rel_path = os.path.relpath(full_path, path)
                    self.script_list.insert(tk.END, rel_path)
        
        self.editor.log(f"Loaded {len(self.scripts)} script(s)")
    
    def new_script(self):
        """Create a new script"""
        if not self.editor.project_path:
            self.editor.log("Please open or create a project first", "warning")
            return
        
        # Simple input dialog
        dialog = tk.Toplevel(self.frame)
        dialog.title("New Script")
        dialog.geometry("300x100")
        dialog.configure(bg="#1e1e1e")
        dialog.transient(self.frame)
        
        tk.Label(
            dialog,
            text="Script name:",
            bg="#1e1e1e",
            fg="#cccccc"
        ).pack(pady=10)
        
        name_entry = tk.Entry(dialog, bg="#3c3c3c", fg="white", width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def create():
            name = name_entry.get().strip()
            if name:
                if not name.endswith('.ts'):
                    name += '.ts'
                
                filepath = os.path.join(self.editor.project_path, name)
                
                # Create file with template
                with open(filepath, 'w') as f:
                    f.write("// T# Script\n")
                    f.write(f"// {name}\n\n")
                    f.write("func main() {\n")
                    f.write("    print('Hello from T#!');\n")
                    f.write("}\n\n")
                    f.write("main();\n")
                
                self.load_scripts(self.editor.project_path)
                self.editor.log(f"Created new script: {name}")
                dialog.destroy()
        
        tk.Button(
            dialog,
            text="Create",
            command=create,
            bg="#0e639c",
            fg="white"
        ).pack(pady=10)
        
        name_entry.bind("<Return>", lambda e: create())
    
    def remove_script(self):
        """Remove selected script"""
        selection = self.script_list.curselection()
        if selection:
            idx = selection[0]
            script_path = self.scripts[idx]
            
            result = tk.messagebox.askyesno(
                "Confirm Delete",
                f"Delete {os.path.basename(script_path)}?"
            )
            
            if result:
                try:
                    os.remove(script_path)
                    self.load_scripts(self.editor.project_path)
                    self.editor.log(f"Deleted: {os.path.basename(script_path)}")
                except Exception as e:
                    self.editor.log(f"Error deleting script: {e}", "error")
    
    def open_selected(self, event=None):
        """Open the selected script in the editor"""
        selection = self.script_list.curselection()
        if selection:
            idx = selection[0]
            script_path = self.scripts[idx]
            
            try:
                with open(script_path, 'r') as f:
                    content = f.read()
                
                self.editor.script_editor.set_content(content)
                self.editor.current_script = script_path
                self.editor.update_file_info(os.path.basename(script_path))
                self.editor.log(f"Opened: {os.path.basename(script_path)}")
            except Exception as e:
                self.editor.log(f"Error opening script: {e}", "error")
