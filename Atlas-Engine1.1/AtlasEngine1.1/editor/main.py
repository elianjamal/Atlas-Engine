#!/usr/bin/env python3
"""
AtlasEngine - Main Entry Point
Professional Game Engine with Integrated Editor
Version 0.1
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from editor.editor_window import EditorWindow
import tkinter as tk

def main():
    """Initialize and run the AtlasEngine Editor"""
    root = tk.Tk()
    app = EditorWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
