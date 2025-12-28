"""
Diagnostic script to check viewport_3d.py
"""
import sys
import os

print("=" * 50)
print("VIEWPORT_3D.PY DIAGNOSTIC")
print("=" * 50)
print()

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check file exists
viewport_path = os.path.join(os.path.dirname(__file__), 'editor', 'viewport_3d.py')
print(f"1. Checking file: {viewport_path}")
if os.path.exists(viewport_path):
    print("   ✓ File exists")
    file_size = os.path.getsize(viewport_path)
    print(f"   ✓ File size: {file_size:,} bytes")
else:
    print("   ✗ File NOT found!")
    sys.exit(1)

print()

# Check for class definition
print("2. Checking for Viewport3D class...")
with open(viewport_path, 'r', encoding='utf-8') as f:
    content = f.read()
    if 'class Viewport3D:' in content:
        print("   ✓ Class definition found")
        # Find line number
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('class Viewport3D:'):
                print(f"   ✓ At line {i}")
                break
    else:
        print("   ✗ Class definition NOT found!")
        print("   File might be corrupted or incomplete")

print()

# Try to import
print("3. Attempting import...")
try:
    from editor.viewport_3d import Viewport3D
    print("   ✓ Import successful!")
    print(f"   ✓ Class: {Viewport3D}")
    print(f"   ✓ Type: {type(Viewport3D)}")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    print()
    print("CHECKING WHAT'S IN THE MODULE:")
    try:
        import editor.viewport_3d as vp
        print(f"   Module: {vp}")
        print(f"   Module file: {vp.__file__}")
        print()
        print("   Available attributes:")
        attrs = [a for a in dir(vp) if not a.startswith('_')]
        for attr in attrs[:20]:  # First 20
            print(f"     - {attr}")
        if 'Viewport3D' in attrs:
            print("   ✓ Viewport3D IS in module!")
        else:
            print("   ✗ Viewport3D NOT in module!")
    except Exception as e2:
        print(f"   Can't even load module: {e2}")

print()
print("=" * 50)
print("DIAGNOSTIC COMPLETE")
print("=" * 50)
