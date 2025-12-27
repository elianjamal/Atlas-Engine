#!/usr/bin/env python3
"""
PARABOX - SYSTEM
2D Maze Generator
"""

import os
import random
import time
import sys

class ParadoxMaze:
    def __init__(self, width=25, height=25):
        self.width = width
        self.height = height
        self.maze = []
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the Paradox ASCII header"""
        header = """
    ╔═══════════════════════════════════╗
    ║   ___  ___  ___  ___  ___  ___   ║
    ║  | _ \\/ _ \\| _ \\/ _ \\| _ )/ _ \\\ ║
    ║  |  _/ (_) |   / (_) | _ \\ (_) |  ║
    ║  |_|  \\___/|_|_\\\\___/|___/\\___/  ║
    ║                                   ║
    ║      P A R A B O X - S Y S T E M  ║
    ╚═══════════════════════════════════╝
        """
        print("\033[92m" + header + "\033[0m")
    
    def boot_sequence(self):
        """Simulate the boot sequence from the image"""
        self.clear_screen()
        self.print_header()
        
        messages = [
            "Booting PARABOX AI Modules...",
            "Locating HL-1...",
            "HL-1 Located",
            "Utilizing ExampleMaps",
            "Please wait...",
            "Loading.",
            "Loading..",
            "Loading...",
            "Loading....",
            "Loading.....",
            "Loading......",
            "",
            "Ready for creation (refer to manual.txt)",
            ""
        ]
        
        for msg in messages:
            print("\033[92m" + msg + "\033[0m")
            time.sleep(0.3)
    
    def generate_maze_dfs(self):
        """Generate maze using Depth-First Search algorithm"""
        # Initialize maze with all walls
        self.maze = [['█' for _ in range(self.width)] for _ in range(self.height)]
        
        # Starting position
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = ' '
        
        # Stack for DFS
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            
            # Find unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < self.width - 1 and 
                    0 < ny < self.height - 1 and 
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose random neighbor
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Remove wall between current and neighbor
                self.maze[y + dy // 2][x + dx // 2] = ' '
                self.maze[ny][nx] = ' '
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Set entrance and exit
        self.maze[1][0] = 'S'  # Start
        self.maze[self.height - 2][self.width - 1] = 'E'  # Exit
    
    def display_maze(self):
        """Display the maze in the terminal"""
        print("\n\033[92m" + "="*50 + "\033[0m")
        print("\033[96mGENERATED MAZE - DIMENSIONS: {}x{}\033[0m".format(self.width, self.height))
        print("\033[92m" + "="*50 + "\033[0m\n")
        
        for row in self.maze:
            line = ""
            for cell in row:
                if cell == 'S':
                    line += "\033[93mS\033[0m"  # Yellow start
                elif cell == 'E':
                    line += "\033[91mE\033[0m"  # Red exit
                elif cell == '█':
                    line += "\033[92m█\033[0m"  # Green walls
                else:
                    line += " "
            print(line)
        
        print("\n\033[92m" + "="*50 + "\033[0m")
        print("\033[93mS\033[0m = Start | \033[91mE\033[0m = Exit | \033[92m█\033[0m = Wall")
        print("\033[92m" + "="*50 + "\033[0m\n")
    
    def save_maze(self, filename="maze_output.txt"):
        """Save maze to a file"""
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"PARABOX MAZE - {self.width}x{self.height}\n")
            f.write("="*50 + "\n\n")
            
            for row in self.maze:
                f.write(''.join(row) + '\n')
            
            f.write("\n" + "="*50 + "\n")
            f.write("S = Start | E = Exit | █ = Wall\n")
        
        print(f"\033[92m✓ Maze saved to: {filepath}\033[0m")
    
    def export_coordinates(self, filename="maze_coords.txt"):
        """Export maze as coordinate map for game engines"""
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w') as f:
            f.write("// PARABOX MAZE COORDINATES\n")
            f.write(f"// Dimensions: {self.width}x{self.height}\n\n")
            
            f.write("WALLS = [\n")
            for y, row in enumerate(self.maze):
                for x, cell in enumerate(row):
                    if cell == '█':
                        f.write(f"    ({x}, {y}),\n")
            f.write("]\n\n")
            
            # Find start and exit positions
            for y, row in enumerate(self.maze):
                for x, cell in enumerate(row):
                    if cell == 'S':
                        f.write(f"START = ({x}, {y})\n")
                    elif cell == 'E':
                        f.write(f"EXIT = ({x}, {y})\n")
        
        print(f"\033[92m✓ Coordinates exported to: {filepath}\033[0m")

def main():
    """Main program loop"""
    try:
        generator = ParadoxMaze()
        generator.boot_sequence()
        
        print("\033[96mType command: GENERATE\033[0m")
        
        while True:
            command = input("\033[92m> \033[0m").strip().upper()
            
            if command == "GENERATE":
                print("\033[92mGenerating...\033[0m")
                time.sleep(0.5)
                
                # Get custom dimensions if desired
                try:
                    width = int(input("\033[96mMaze width (odd number, default 25): \033[0m") or "25")
                    height = int(input("\033[96mMaze height (odd number, default 25): \033[0m") or "25")
                    
                    # Ensure odd dimensions
                    width = width if width % 2 == 1 else width + 1
                    height = height if height % 2 == 1 else height + 1
                    
                    generator = ParadoxMaze(width, height)
                except ValueError:
                    print("\033[91mInvalid input. Using defaults.\033[0m")
                    generator = ParadoxMaze()
                
                generator.generate_maze_dfs()
                generator.clear_screen()
                generator.print_header()
                generator.display_maze()
                
                # Ask if user wants to save
                save = input("\033[96mSave maze to file? (y/n): \033[0m").strip().lower()
                if save == 'y':
                    generator.save_maze()
                    
                    export = input("\033[96mExport coordinates for HL1? (y/n): \033[0m").strip().lower()
                    if export == 'y':
                        generator.export_coordinates()
                
                print("\n\033[96mType GENERATE for new maze or EXIT to quit\033[0m")
                
            elif command == "EXIT" or command == "QUIT":
                print("\033[92mShutting down PARABOX system...\033[0m")
                time.sleep(0.5)
                break
                
            elif command == "CLEAR":
                generator.clear_screen()
                generator.print_header()
                
            elif command == "HELP":
                print("\n\033[96mAvailable commands:\033[0m")
                print("  GENERATE - Create a new maze")
                print("  CLEAR    - Clear the screen")
                print("  EXIT     - Quit the program")
                print("  HELP     - Show this help\n")
                
            else:
                print("\033[91mUnknown command. Type HELP for available commands.\033[0m")
    
    except KeyboardInterrupt:
        print("\n\033[91m\nInterrupted. Shutting down...\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
