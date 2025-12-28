#!/usr/bin/env python3
"""
AtlasEngine Launcher
Quick start script for the game engine
"""

import sys
import os

# Ensure we're in the right directory
engine_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(engine_dir)

print("=" * 50)
print("   _   _   _           _____             _            ")
print("  / \ | |_| | __ _ ___| ____|_ __   __ _(_)_ __   ___ ")
print(" / _ \| __| |/ _` / __|  _| | '_ \ / _` | | '_ \ / _ \\")
print("/ ___ \ |_| | (_| \__ \ |___| | | | (_| | | | | |  __/")
print("/_/   \_\__|_|\__,_|___/_____|_| |_|\__, |_|_| |_|\___|")
print("                                    |___/              ")
print("              AtlasEngine v1.0")
print("        Professional Game Engine")
print("=" * 50)
print()
print("Starting editor...")
print()

# Import and run the editor
try:
    from editor.main import main
    main()
except ImportError as e:
    print(f"Error: Could not import editor module: {e}")
    print("Make sure all required files are present.")
    sys.exit(1)
except Exception as e:
    print(f"Error starting editor: {e}")
    sys.exit(1)
