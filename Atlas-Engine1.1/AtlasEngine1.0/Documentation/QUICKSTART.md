# AtlasEngine - Quick Start Guide

## Installation

1. Extract the AtlasEngine folder
2. Open terminal/command prompt
3. Navigate to the AtlasEngine directory:
   ```bash
   cd AtlasEngine
   ```

## Running the Engine

### Option 1: Using the launcher
```bash
python3 launch.py
```

### Option 2: Direct launch
```bash
python3 editor/main.py
```

## First Steps

1. **Create a New Project**
   - File → New Project...
   - Select an empty folder
   - This will be your game project directory

2. **Create Your First Script**
   - Click "+ New" in the Script Sidebar
   - Name your script (e.g., "game.ts")
   - The editor opens with a template

3. **Write T# Code**
   ```typescript
   // Your first T# script
   func main() {
       print('Hello from AtlasEngine!');
       var player = spawn('Player');
       move(player, 0, 0, 0);
       print('Player spawned!');
   }
   
   main();
   ```

4. **Run Your Script**
   - Press **F5** or
   - Run → Run Script
   - Check the OUTPUT panel for results

## Example Scripts

### Simple Object Spawning
```typescript
func createWorld() {
    print('Creating game world...');
    
    // Spawn player
    var player = spawn('Player');
    move(player, 0, 0, 0);
    
    // Spawn enemies
    var enemy1 = spawn('Enemy');
    move(enemy1, 5, 0, 5);
    
    var enemy2 = spawn('Enemy');
    move(enemy2, -5, 0, 5);
    
    print('World created!');
}

createWorld();
```

### Loop Example
```typescript
func spawnCircle(count) {
    var i = 0;
    while (i < count) {
        var obj = spawn('Cube');
        print('Spawned object:', i);
        i = i + 1;
    }
}

spawnCircle(10);
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+S | Save current script |
| F5 | Run script |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+X | Cut |
| Ctrl+C | Copy |
| Ctrl+V | Paste |

## T# Built-in Functions

### `print(message)`
Output to console
```typescript
print('Hello World!');
```

### `spawn(type)`
Create game object
```typescript
var id = spawn('Enemy');
```

### `move(id, x, y, z)`
Move object to position
```typescript
move(id, 10, 0, 5);
```

### `rotate(id, rx, ry, rz)`
Rotate object
```typescript
rotate(id, 0, 90, 0);
```

### `destroy(id)`
Remove object
```typescript
destroy(id);
```

## Troubleshooting

### "tkinter not found"
Install tkinter:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Included with Python
- **Windows**: Included with Python

### Script won't run
- Check for syntax errors in OUTPUT panel
- Ensure all braces {} and parentheses () are matched
- Verify function names are spelled correctly

### Scripts not appearing
- Make sure you created a project first
- Scripts must have .ts extension
- Use "+ New" button to create scripts

## Tips

1. **Save Often**: Use Ctrl+S frequently
2. **Check Output**: Always look at the OUTPUT panel after running
3. **Start Simple**: Test small scripts before complex ones
4. **Use Comments**: Document your code with //
5. **Experiment**: Try different combinations of functions

## Next Steps

- Explore the demo.ts script in scripts/ folder
- Read the full README.md for advanced features
- Experiment with creating multiple objects
- Try different movement patterns

## Support

For more information, see README.md in the AtlasEngine folder.

---

**Have fun creating with AtlasEngine!**
