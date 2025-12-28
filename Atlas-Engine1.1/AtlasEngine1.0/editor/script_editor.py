#!/usr/bin/env python3
"""
AtlasEngine - Script Editor
Text editor with T# syntax highlighting
"""

import tkinter as tk
from tkinter import scrolledtext
import re

class ScriptEditor:
    """Code editor with syntax highlighting"""
    
    def __init__(self, parent, editor):
        self.editor = editor
        
        # Create frame
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        
        # Line numbers frame
        self.line_numbers_frame = tk.Frame(self.frame, bg="#1e1e1e", width=50)
        self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.line_numbers = tk.Text(
            self.line_numbers_frame,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background="#1e1e1e",
            foreground="#858585",
            state=tk.DISABLED,
            font=("Consolas", 11)
        )
        self.line_numbers.pack(fill=tk.Y, expand=True)
        
        # Text editor
        self.text_widget = scrolledtext.ScrolledText(
            self.frame,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            selectbackground="#264f78",
            font=("Consolas", 11),
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            relief=tk.FLAT
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure syntax highlighting tags
        self.setup_syntax_tags()
        
        # Bind events
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<MouseWheel>", self.on_scroll)
        self.text_widget.bind("<Button-1>", self.on_click)
        
        # Initial line numbers
        self.update_line_numbers()
    
    def setup_syntax_tags(self):
        """Setup syntax highlighting tags"""
        # Keywords
        self.text_widget.tag_config("keyword", foreground="#569cd6")
        # Strings
        self.text_widget.tag_config("string", foreground="#ce9178")
        # Comments
        self.text_widget.tag_config("comment", foreground="#6a9955")
        # Numbers
        self.text_widget.tag_config("number", foreground="#b5cea8")
        # Functions
        self.text_widget.tag_config("function", foreground="#dcdcaa")
        # Operators
        self.text_widget.tag_config("operator", foreground="#d4d4d4")
    
    def highlight_syntax(self):
        """Apply syntax highlighting to the text"""
        content = self.text_widget.get("1.0", tk.END)
        
        # Remove all tags
        for tag in ["keyword", "string", "comment", "number", "function", "operator"]:
            self.text_widget.tag_remove(tag, "1.0", tk.END)
        
        # Keywords
        keywords = [
            "var", "func", "if", "else", "while", "for", "return",
            "true", "false", "null", "spawn", "move", "rotate",
            "print", "input", "destroy"
        ]
        
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_widget.tag_add("keyword", start, end)
        
        # Strings (single and double quotes)
        for match in re.finditer(r'["\'].*?["\']', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_widget.tag_add("string", start, end)
        
        # Comments
        for match in re.finditer(r'//.*?$', content, re.MULTILINE):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_widget.tag_add("comment", start, end)
        
        # Numbers
        for match in re.finditer(r'\b\d+\.?\d*\b', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_widget.tag_add("number", start, end)
        
        # Functions
        for match in re.finditer(r'\b(\w+)\s*\(', content):
            start = f"1.0+{match.start(1)}c"
            end = f"1.0+{match.end(1)}c"
            self.text_widget.tag_add("function", start, end)
    
    def update_line_numbers(self):
        """Update line numbers display"""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        
        line_count = int(self.text_widget.index(tk.END).split('.')[0]) - 1
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state=tk.DISABLED)
    
    def on_key_release(self, event=None):
        """Handle key release events"""
        self.update_line_numbers()
        self.highlight_syntax()
    
    def on_scroll(self, event=None):
        """Sync line numbers scrolling"""
        self.update_line_numbers()
    
    def on_click(self, event=None):
        """Handle click events"""
        self.update_line_numbers()
    
    def get_content(self):
        """Get the editor content"""
        return self.text_widget.get("1.0", tk.END)
    
    def set_content(self, content):
        """Set the editor content"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", content)
        self.highlight_syntax()
        self.update_line_numbers()
    
    def save(self, filepath):
        """Save content to file"""
        content = self.get_content()
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            self.editor.log(f"Error saving file: {e}", "error")
            return False
