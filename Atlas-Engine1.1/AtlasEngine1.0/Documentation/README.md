# AtlasEngine v0.1

Professional Game Engine with Integrated Editor

## Overview

AtlasEngine is a complete game engine built in Python featuring:
- Custom T# (TScript) scripting language
- Professional code editor with syntax highlighting
- Real-time script execution
- Project management system
- Integrated logging and debugging tools

## Project Structure

```
AtlasEngine/
├── editor/
│   ├── main.py              - Entry point
│   ├── editor_window.py     - Main editor window
│   ├── script_sidebar.py    - Script management
│   ├── script_editor.py     - Code editor with highlighting
│   ├── log_panel.py         - Output logging
│   ├── ts_interpreter.py    - T# script interpreter
│   └── ts_highlighter.py    - Syntax highlighter
├── scripts/
│   └── (auto-generated .ts files)
└── logs/
    └── output.log
```

## Getting Started

### Installation

```bash
# No additional dependencies required (uses tkinter)
python3 editor/main.py
```

### Creating Your First Project

1. Launch the editor: `python3 editor/main.py`
2. Click `File > New Project...`
3. Select a folder for your project
4. Click the "+ New" button in the Script Sidebar
5. Write your T# code
6. Press F5 or click `Run > Run Script` to execute

## T# Scripting Language

### Features

- **Variables**: `var x = 10;`
- **Functions**: `func name(params) { ... }`
- **Control Flow**: `if`, `else`, `while`, `for`
- **Game Objects**: `spawn()`, `move()`, `rotate()`, `destroy()`
- **I/O**: `print()`, `input()`

### Built-in Functions

#### `print(message)`
Output text to the log panel
```typescript
print('Hello, AtlasEngine!');
```

#### `spawn(type)`
Create a new game object
```typescript
var player = spawn('Player');
var enemy = spawn('Enemy');
```

#### `move(objectId, x, y, z)`
Move an object to a position
```typescript
move(player, 10, 0, 5);
```

#### `rotate(objectId, rx, ry, rz)`
Rotate an object (in degrees)
```typescript
rotate(player, 0, 90, 0);
```

#### `destroy(objectId)`
Remove an object from the scene
```typescript
destroy(enemy);
```

### Example Script

```typescript
// Create player
func createPlayer() {
    var playerId = spawn('Player');
    move(playerId, 0, 0, 0);
    print('Player created!');
    return playerId;
}

// Main game function
func main() {
    print('Game starting...');
    var player = createPlayer();
    print('Game initialized!');
}

main();
```

## Keyboard Shortcuts

- **Ctrl+S**: Save current script
- **F5**: Run script
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+X**: Cut
- **Ctrl+C**: Copy
- **Ctrl+V**: Paste

## Editor Features

### Version 0.1 Includes:

- Script bar (sidebar)
-  Add/remove scripts
-  T# scripting language
-  T# syntax highlighting
-  T# interpreter
-  Log output panel
-  Project folders
-  File management

### Coming Soon:

- 3D Viewport rendering
- Visual scene editor
- Asset management
- Physics engine
- Audio system
- Export to standalone game

## Architecture

### Editor Components

1. **EditorWindow**: Main application window and coordinator
2. **ScriptSidebar**: File browser and script manager
3. **ScriptEditor**: Code editor with syntax highlighting
4. **LogPanel**: Output console for debugging
5. **TSInterpreter**: Executes T# scripts
6. **TSHighlighter**: Provides syntax coloring

### T# Language Design

The T# language is designed specifically for game development with:
- Simple, readable syntax
- Built-in game object management
- Real-time execution
- Easy debugging through print statements

## Development

### Adding New Built-in Functions

Edit `editor/ts_interpreter.py` and add your function:

```python
def builtin_yourfunction(self, args_str: str):
    """Your new function"""
    args = self.parse_arguments(args_str)
    # Implementation
    self.editor.log(f"Your function executed", "success")
```

Then register it in `execute_function_call()`:

```python
elif func_name == 'yourfunction':
    self.builtin_yourfunction(args_str)
```

### Extending Syntax Highlighting

Edit `editor/ts_highlighter.py` to add new keywords or patterns.

## Technical Notes

- Built with Python 3 and Tkinter
- No external dependencies required
- Cross-platform compatible (Windows, Linux, macOS)
- Modular architecture for easy extension

## Troubleshooting

### "No module named 'editor'"

Make sure you're running from the correct directory:
```bash
cd AtlasEngine
python3 editor/main.py
```

### Scripts not showing up

- Make sure your project folder contains .ts files
- Use the "+ New" button to create scripts
- Check file permissions

## License

AtlasEngine is provided as-is for educational and game development purposes.

## Credits

Created as a professional game engine demonstration with integrated scripting language and editor.

---

**Version**: 0.1  
**Status**: Early Development  
**Python**: 3.8+
