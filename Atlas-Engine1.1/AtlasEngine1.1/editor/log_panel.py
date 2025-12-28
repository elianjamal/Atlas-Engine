#!/usr/bin/env python3
"""
AtlasEngine - Log Panel
Output and logging panel for script execution and system messages
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class LogPanel:
    """Log output panel"""
    
    def __init__(self, parent, editor):
        self.editor = editor
        
        # Create frame
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        
        # Header
        header = tk.Frame(self.frame, bg="#252526")
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="OUTPUT",
            bg="#252526",
            fg="#cccccc",
            font=("Segoe UI", 10, "bold"),
            pady=5,
            padx=10
        ).pack(side=tk.LEFT)
        
        clear_btn = tk.Button(
            header,
            text="Clear",
            command=self.clear,
            bg="#3c3c3c",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            font=("Segoe UI", 9)
        )
        clear_btn.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            self.frame,
            bg="#1e1e1e",
            fg="#cccccc",
            font=("Consolas", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for different log levels
        self.log_text.tag_config("info", foreground="#4ec9b0")
        self.log_text.tag_config("warning", foreground="#ce9178")
        self.log_text.tag_config("error", foreground="#f48771")
        self.log_text.tag_config("success", foreground="#6a9955")
        self.log_text.tag_config("timestamp", foreground="#858585")
    
    def log(self, message, level="info"):
        """Add a log message"""
        self.log_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message with appropriate color
        self.log_text.insert(tk.END, f"{message}\n", level)
        
        # Auto-scroll to bottom
        self.log_text.see(tk.END)
        
        self.log_text.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear all log messages"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("Log cleared", "info")
