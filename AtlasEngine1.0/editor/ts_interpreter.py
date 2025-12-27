#!/usr/bin/env python3
"""
AtlasEngine - T# Interpreter
Interprets and executes T# scripting language
"""

import re
import math
from typing import Dict, Any, List
from editor.math_physics_engine import (
    PhysicsEngine, ScientificCalculator, MathFunctions, 
    Statistics, Vector3
)

class TSInterpreter:
    """T# (TScript) Language Interpreter"""
    
    def __init__(self, editor):
        self.editor = editor
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, tuple] = {}
        self.game_objects: List[Dict] = []
        
        # Scientific modules
        self.physics = PhysicsEngine()
        self.calc = ScientificCalculator()
        self.math_funcs = MathFunctions()
        self.stats = Statistics()
        
        # Add math constants to variables
        self.variables['PI'] = math.pi
        self.variables['E'] = math.e
        self.variables['TAU'] = 2 * math.pi
    
    def execute(self, code: str):
        """Execute T# code"""
        try:
            # Remove comments
            code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
            
            # Split into lines
            lines = [line.strip() for line in code.split('\n') if line.strip()]
            
            # Execute line by line
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Variable declaration
                if line.startswith('var '):
                    self.execute_var_declaration(line)
                
                # Function declaration
                elif line.startswith('func '):
                    i = self.parse_function(lines, i)
                
                # Function call
                elif '(' in line and ')' in line:
                    self.execute_function_call(line)
                
                # Assignment
                elif '=' in line and not line.startswith('var'):
                    self.execute_assignment(line)
                
                i += 1
            
            self.editor.log("Script execution completed", "success")
            
        except Exception as e:
            self.editor.log(f"Runtime Error: {str(e)}", "error")
    
    def execute_var_declaration(self, line: str):
        """Execute variable declaration"""
        # var name = value;
        match = re.match(r'var\s+(\w+)\s*=\s*(.+?);?$', line)
        if match:
            var_name = match.group(1)
            var_value = self.evaluate_expression(match.group(2))
            self.variables[var_name] = var_value
            self.editor.log(f"Variable '{var_name}' = {var_value}")
    
    def execute_assignment(self, line: str):
        """Execute variable assignment"""
        match = re.match(r'(\w+)\s*=\s*(.+?);?$', line)
        if match:
            var_name = match.group(1)
            var_value = self.evaluate_expression(match.group(2))
            self.variables[var_name] = var_value
            self.editor.log(f"'{var_name}' = {var_value}")
    
    def parse_function(self, lines: List[str], start_idx: int) -> int:
        """Parse function definition"""
        func_line = lines[start_idx]
        
        # func name(params) {
        match = re.match(r'func\s+(\w+)\s*\((.*?)\)\s*\{', func_line)
        if match:
            func_name = match.group(1)
            params = [p.strip() for p in match.group(2).split(',') if p.strip()]
            
            # Find function body
            body_lines = []
            i = start_idx + 1
            brace_count = 1
            
            while i < len(lines) and brace_count > 0:
                line = lines[i]
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                
                if brace_count > 0:
                    body_lines.append(line)
                
                i += 1
            
            self.functions[func_name] = (params, body_lines)
            self.editor.log(f"Function '{func_name}' defined")
            
            return i - 1
        
        return start_idx
    
    def execute_function_call(self, line: str):
        """Execute function call"""
        # Extract function name and arguments
        match = re.match(r'(\w+)\s*\((.*?)\);?$', line)
        if not match:
            return
        
        func_name = match.group(1)
        args_str = match.group(2)
        
        # Built-in game functions
        if func_name == 'print':
            self.builtin_print(args_str)
        elif func_name == 'spawn':
            self.builtin_spawn(args_str)
        elif func_name == 'move':
            self.builtin_move(args_str)
        elif func_name == 'rotate':
            self.builtin_rotate(args_str)
        elif func_name == 'destroy':
            self.builtin_destroy(args_str)
        
        # Math functions
        elif func_name == 'sin':
            return self.builtin_sin(args_str)
        elif func_name == 'cos':
            return self.builtin_cos(args_str)
        elif func_name == 'tan':
            return self.builtin_tan(args_str)
        elif func_name == 'asin':
            return self.builtin_asin(args_str)
        elif func_name == 'acos':
            return self.builtin_acos(args_str)
        elif func_name == 'atan':
            return self.builtin_atan(args_str)
        elif func_name == 'sqrt':
            return self.builtin_sqrt(args_str)
        elif func_name == 'pow':
            return self.builtin_pow(args_str)
        elif func_name == 'abs':
            return self.builtin_abs(args_str)
        elif func_name == 'floor':
            return self.builtin_floor(args_str)
        elif func_name == 'ceil':
            return self.builtin_ceil(args_str)
        elif func_name == 'round':
            return self.builtin_round(args_str)
        elif func_name == 'log':
            return self.builtin_log(args_str)
        elif func_name == 'ln':
            return self.builtin_ln(args_str)
        elif func_name == 'exp':
            return self.builtin_exp(args_str)
        
        # Physics functions
        elif func_name == 'projectile':
            self.builtin_projectile(args_str)
        elif func_name == 'orbit':
            self.builtin_orbit(args_str)
        elif func_name == 'freefall':
            self.builtin_freefall(args_str)
        elif func_name == 'spring':
            self.builtin_spring(args_str)
        elif func_name == 'pendulum':
            self.builtin_pendulum(args_str)
        
        # Calculator functions
        elif func_name == 'quadratic':
            return self.builtin_quadratic(args_str)
        elif func_name == 'distance2d':
            return self.builtin_distance2d(args_str)
        elif func_name == 'distance3d':
            return self.builtin_distance3d(args_str)
        elif func_name == 'velocity':
            return self.builtin_velocity(args_str)
        elif func_name == 'acceleration':
            return self.builtin_acceleration(args_str)
        elif func_name == 'kineticEnergy':
            return self.builtin_kinetic_energy(args_str)
        elif func_name == 'potentialEnergy':
            return self.builtin_potential_energy(args_str)
        elif func_name == 'momentum':
            return self.builtin_momentum(args_str)
        elif func_name == 'force':
            return self.builtin_force(args_str)
        elif func_name == 'work':
            return self.builtin_work(args_str)
        elif func_name == 'power':
            return self.builtin_power(args_str)
        
        # Advanced math
        elif func_name == 'factorial':
            return self.builtin_factorial(args_str)
        elif func_name == 'fibonacci':
            return self.builtin_fibonacci(args_str)
        elif func_name == 'isPrime':
            return self.builtin_is_prime(args_str)
        elif func_name == 'gcd':
            return self.builtin_gcd(args_str)
        elif func_name == 'lcm':
            return self.builtin_lcm(args_str)
        
        # Statistics
        elif func_name == 'mean':
            return self.builtin_mean(args_str)
        elif func_name == 'median':
            return self.builtin_median(args_str)
        elif func_name == 'stddev':
            return self.builtin_stddev(args_str)
        
        # Plotting
        elif func_name == 'plot':
            self.builtin_plot(args_str)
        elif func_name == 'plotFunc':
            self.builtin_plot_func(args_str)
        
        # User-defined functions
        elif func_name in self.functions:
            self.execute_user_function(func_name, args_str)
        else:
            self.editor.log(f"Unknown function: {func_name}", "warning")
    
    def execute_user_function(self, func_name: str, args_str: str):
        """Execute user-defined function"""
        params, body = self.functions[func_name]
        
        # Parse arguments
        args = self.parse_arguments(args_str)
        
        # Create local scope (simple implementation)
        old_vars = self.variables.copy()
        
        # Bind parameters
        for i, param in enumerate(params):
            if i < len(args):
                self.variables[param] = args[i]
        
        # Execute function body
        for line in body:
            if line.startswith('var '):
                self.execute_var_declaration(line)
            elif '(' in line and ')' in line:
                self.execute_function_call(line)
            elif 'return' in line:
                break  # Simple return handling
        
        # Restore scope
        self.variables = old_vars
    
    def builtin_print(self, args_str: str):
        """Built-in print function"""
        args = self.parse_arguments(args_str)
        output = ' '.join(str(arg) for arg in args)
        self.editor.log(f">>> {output}", "info")
    
    def builtin_spawn(self, args_str: str):
        """Built-in spawn function - creates a game object"""
        args = self.parse_arguments(args_str)
        if args:
            obj_type = args[0]
            obj = {
                'type': obj_type,
                'position': [0, 0, 0],
                'rotation': [0, 0, 0],
                'id': len(self.game_objects)
            }
            self.game_objects.append(obj)
            self.editor.log(f"Spawned {obj_type} (ID: {obj['id']})", "success")
            return obj['id']
    
    def builtin_move(self, args_str: str):
        """Built-in move function"""
        args = self.parse_arguments(args_str)
        if len(args) >= 4:
            obj_id = int(args[0])
            x, y, z = float(args[1]), float(args[2]), float(args[3])
            
            if obj_id < len(self.game_objects):
                self.game_objects[obj_id]['position'] = [x, y, z]
                self.editor.log(f"Moved object {obj_id} to ({x}, {y}, {z})", "success")
    
    def builtin_rotate(self, args_str: str):
        """Built-in rotate function"""
        args = self.parse_arguments(args_str)
        if len(args) >= 4:
            obj_id = int(args[0])
            rx, ry, rz = float(args[1]), float(args[2]), float(args[3])
            
            if obj_id < len(self.game_objects):
                self.game_objects[obj_id]['rotation'] = [rx, ry, rz]
                self.editor.log(f"Rotated object {obj_id} to ({rx}, {ry}, {rz})", "success")
    
    def builtin_destroy(self, args_str: str):
        """Built-in destroy function"""
        args = self.parse_arguments(args_str)
        if args:
            obj_id = int(args[0])
            if obj_id < len(self.game_objects):
                obj_type = self.game_objects[obj_id]['type']
                self.game_objects[obj_id] = None
                self.editor.log(f"Destroyed {obj_type} (ID: {obj_id})", "success")
    
    def parse_arguments(self, args_str: str) -> List[Any]:
        """Parse function arguments"""
        if not args_str.strip():
            return []
        
        args = []
        for arg in args_str.split(','):
            arg = arg.strip()
            args.append(self.evaluate_expression(arg))
        
        return args
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate an expression"""
        expr = expr.strip().rstrip(';')
        
        # String literal
        if expr.startswith('"') or expr.startswith("'"):
            return expr[1:-1]
        
        # Number
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
        
        # Boolean
        if expr == 'true':
            return True
        if expr == 'false':
            return False
        
        # Variable
        if expr in self.variables:
            return self.variables[expr]
        
        # Arithmetic expression (simple)
        try:
            return eval(expr, {"__builtins__": {}}, self.variables)
        except:
            return expr
    
    # ==================== MATH FUNCTIONS ====================
    
    def builtin_sin(self, args_str: str):
        """Sine function (radians)"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.sin(args[0])
            self.editor.log(f"sin({args[0]}) = {result}")
            return result
    
    def builtin_cos(self, args_str: str):
        """Cosine function (radians)"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.cos(args[0])
            self.editor.log(f"cos({args[0]}) = {result}")
            return result
    
    def builtin_tan(self, args_str: str):
        """Tangent function (radians)"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.tan(args[0])
            self.editor.log(f"tan({args[0]}) = {result}")
            return result
    
    def builtin_asin(self, args_str: str):
        """Arcsine function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.asin(args[0])
            self.editor.log(f"asin({args[0]}) = {result}")
            return result
    
    def builtin_acos(self, args_str: str):
        """Arccosine function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.acos(args[0])
            self.editor.log(f"acos({args[0]}) = {result}")
            return result
    
    def builtin_atan(self, args_str: str):
        """Arctangent function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.atan(args[0])
            self.editor.log(f"atan({args[0]}) = {result}")
            return result
    
    def builtin_sqrt(self, args_str: str):
        """Square root"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.sqrt(args[0])
            self.editor.log(f"sqrt({args[0]}) = {result}")
            return result
    
    def builtin_pow(self, args_str: str):
        """Power function"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            result = args[0] ** args[1]
            self.editor.log(f"pow({args[0]}, {args[1]}) = {result}")
            return result
    
    def builtin_abs(self, args_str: str):
        """Absolute value"""
        args = self.parse_arguments(args_str)
        if args:
            result = abs(args[0])
            self.editor.log(f"abs({args[0]}) = {result}")
            return result
    
    def builtin_floor(self, args_str: str):
        """Floor function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.floor(args[0])
            self.editor.log(f"floor({args[0]}) = {result}")
            return result
    
    def builtin_ceil(self, args_str: str):
        """Ceiling function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.ceil(args[0])
            self.editor.log(f"ceil({args[0]}) = {result}")
            return result
    
    def builtin_round(self, args_str: str):
        """Round function"""
        args = self.parse_arguments(args_str)
        if args:
            result = round(args[0])
            self.editor.log(f"round({args[0]}) = {result}")
            return result
    
    def builtin_log(self, args_str: str):
        """Logarithm base 10"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.log10(args[0])
            self.editor.log(f"log10({args[0]}) = {result}")
            return result
    
    def builtin_ln(self, args_str: str):
        """Natural logarithm"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.log(args[0])
            self.editor.log(f"ln({args[0]}) = {result}")
            return result
    
    def builtin_exp(self, args_str: str):
        """Exponential function"""
        args = self.parse_arguments(args_str)
        if args:
            result = math.exp(args[0])
            self.editor.log(f"exp({args[0]}) = {result}")
            return result
    
    # ==================== PHYSICS FUNCTIONS ====================
    
    def builtin_projectile(self, args_str: str):
        """Calculate projectile motion"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            v0 = args[0]
            angle = args[1]
            height = args[2] if len(args) > 2 else 0.0
            
            trajectory = self.physics.projectile_motion(v0, angle, height)
            
            # Get plotter if available
            if hasattr(self.editor, 'plotter'):
                self.editor.plotter.plot_trajectory(
                    trajectory,
                    f"Projectile v0={v0}m/s, θ={angle}°"
                )
            
            # Calculate key values
            max_height = max(p[1] for p in trajectory)
            max_range = max(p[0] for p in trajectory)
            
            self.editor.log(f"Projectile: v0={v0}m/s, angle={angle}°", "success")
            self.editor.log(f"Max height: {max_height:.2f}m")
            self.editor.log(f"Range: {max_range:.2f}m")
            
            return trajectory
    
    def builtin_orbit(self, args_str: str):
        """Calculate orbital motion"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            radius = args[0]
            mass = args[1]
            duration = args[2] if len(args) > 2 else 100.0
            
            trajectory = self.physics.orbital_mechanics(radius, mass, 1.0, duration)
            
            if hasattr(self.editor, 'plotter'):
                self.editor.plotter.plot_trajectory(
                    trajectory,
                    f"Orbit r={radius}m"
                )
            
            self.editor.log(f"Orbital motion: radius={radius}m", "success")
            return trajectory
    
    def builtin_freefall(self, args_str: str):
        """Calculate free fall"""
        args = self.parse_arguments(args_str)
        if args:
            height = args[0]
            trajectory = self.physics.free_fall(height)
            
            if hasattr(self.editor, 'plotter'):
                self.editor.plotter.plot_trajectory(
                    trajectory,
                    f"Free fall from {height}m"
                )
            
            fall_time = trajectory[-1][0] if trajectory else 0
            self.editor.log(f"Free fall: height={height}m, time={fall_time:.2f}s", "success")
            return trajectory
    
    def builtin_spring(self, args_str: str):
        """Calculate spring motion"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            amplitude = args[0]
            frequency = args[1]
            
            trajectory = self.physics.spring_motion(amplitude, frequency)
            
            if hasattr(self.editor, 'plotter'):
                self.editor.plotter.plot_trajectory(
                    trajectory,
                    f"Spring A={amplitude}m, f={frequency}Hz"
                )
            
            self.editor.log(f"Spring motion: A={amplitude}m, f={frequency}Hz", "success")
            return trajectory
    
    def builtin_pendulum(self, args_str: str):
        """Calculate pendulum motion"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            length = args[0]
            angle = args[1]
            
            trajectory = self.physics.pendulum_motion(length, angle)
            
            if hasattr(self.editor, 'plotter'):
                self.editor.plotter.plot_trajectory(
                    trajectory,
                    f"Pendulum L={length}m, θ0={angle}°"
                )
            
            self.editor.log(f"Pendulum: L={length}m, θ0={angle}°", "success")
            return trajectory
    
    # ==================== CALCULATOR FUNCTIONS ====================
    
    def builtin_quadratic(self, args_str: str):
        """Solve quadratic equation"""
        args = self.parse_arguments(args_str)
        if len(args) >= 3:
            a, b, c = args[0], args[1], args[2]
            x1, x2 = self.calc.quadratic(a, b, c)
            self.editor.log(f"Quadratic {a}x² + {b}x + {c} = 0", "success")
            self.editor.log(f"Solutions: x1={x1}, x2={x2}")
            return (x1, x2)
    
    def builtin_distance2d(self, args_str: str):
        """Calculate 2D distance"""
        args = self.parse_arguments(args_str)
        if len(args) >= 4:
            dist = self.calc.distance_2d(args[0], args[1], args[2], args[3])
            self.editor.log(f"Distance 2D: {dist:.3f}")
            return dist
    
    def builtin_distance3d(self, args_str: str):
        """Calculate 3D distance"""
        args = self.parse_arguments(args_str)
        if len(args) >= 6:
            dist = self.calc.distance_3d(args[0], args[1], args[2], 
                                        args[3], args[4], args[5])
            self.editor.log(f"Distance 3D: {dist:.3f}")
            return dist
    
    def builtin_velocity(self, args_str: str):
        """Calculate velocity"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            v = self.calc.velocity(args[0], args[1])
            self.editor.log(f"Velocity: {v:.3f} m/s")
            return v
    
    def builtin_acceleration(self, args_str: str):
        """Calculate acceleration"""
        args = self.parse_arguments(args_str)
        if len(args) >= 3:
            a = self.calc.acceleration(args[0], args[1], args[2])
            self.editor.log(f"Acceleration: {a:.3f} m/s²")
            return a
    
    def builtin_kinetic_energy(self, args_str: str):
        """Calculate kinetic energy"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            ke = self.calc.kinetic_energy(args[0], args[1])
            self.editor.log(f"Kinetic Energy: {ke:.3f} J")
            return ke
    
    def builtin_potential_energy(self, args_str: str):
        """Calculate potential energy"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            pe = self.calc.potential_energy(args[0], args[1])
            self.editor.log(f"Potential Energy: {pe:.3f} J")
            return pe
    
    def builtin_momentum(self, args_str: str):
        """Calculate momentum"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            p = self.calc.momentum(args[0], args[1])
            self.editor.log(f"Momentum: {p:.3f} kg·m/s")
            return p
    
    def builtin_force(self, args_str: str):
        """Calculate force"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            f = self.calc.force(args[0], args[1])
            self.editor.log(f"Force: {f:.3f} N")
            return f
    
    def builtin_work(self, args_str: str):
        """Calculate work"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            angle = args[2] if len(args) > 2 else 0
            w = self.calc.work(args[0], args[1], angle)
            self.editor.log(f"Work: {w:.3f} J")
            return w
    
    def builtin_power(self, args_str: str):
        """Calculate power"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            p = self.calc.power(args[0], args[1])
            self.editor.log(f"Power: {p:.3f} W")
            return p
    
    # ==================== ADVANCED MATH ====================
    
    def builtin_factorial(self, args_str: str):
        """Calculate factorial"""
        args = self.parse_arguments(args_str)
        if args:
            result = self.math_funcs.factorial(int(args[0]))
            self.editor.log(f"{int(args[0])}! = {result}")
            return result
    
    def builtin_fibonacci(self, args_str: str):
        """Calculate Fibonacci number"""
        args = self.parse_arguments(args_str)
        if args:
            result = self.math_funcs.fibonacci(int(args[0]))
            self.editor.log(f"fib({int(args[0])}) = {result}")
            return result
    
    def builtin_is_prime(self, args_str: str):
        """Check if prime"""
        args = self.parse_arguments(args_str)
        if args:
            result = self.math_funcs.is_prime(int(args[0]))
            self.editor.log(f"{int(args[0])} is {'prime' if result else 'not prime'}")
            return result
    
    def builtin_gcd(self, args_str: str):
        """Calculate GCD"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            result = self.math_funcs.gcd(int(args[0]), int(args[1]))
            self.editor.log(f"gcd({int(args[0])}, {int(args[1])}) = {result}")
            return result
    
    def builtin_lcm(self, args_str: str):
        """Calculate LCM"""
        args = self.parse_arguments(args_str)
        if len(args) >= 2:
            result = self.math_funcs.lcm(int(args[0]), int(args[1]))
            self.editor.log(f"lcm({int(args[0])}, {int(args[1])}) = {result}")
            return result
    
    # ==================== STATISTICS ====================
    
    def builtin_mean(self, args_str: str):
        """Calculate mean"""
        args = self.parse_arguments(args_str)
        if args:
            # If single arg that's a list, use it; otherwise use all args
            data = args if isinstance(args[0], (int, float)) else args[0]
            result = self.stats.mean(data)
            self.editor.log(f"Mean: {result:.3f}")
            return result
    
    def builtin_median(self, args_str: str):
        """Calculate median"""
        args = self.parse_arguments(args_str)
        if args:
            data = args if isinstance(args[0], (int, float)) else args[0]
            result = self.stats.median(data)
            self.editor.log(f"Median: {result:.3f}")
            return result
    
    def builtin_stddev(self, args_str: str):
        """Calculate standard deviation"""
        args = self.parse_arguments(args_str)
        if args:
            data = args if isinstance(args[0], (int, float)) else args[0]
            result = self.stats.standard_deviation(data)
            self.editor.log(f"Std Dev: {result:.3f}")
            return result
    
    # ==================== PLOTTING ====================
    
    def builtin_plot(self, args_str: str):
        """Plot trajectory from data"""
        self.editor.log("Plot function requires plotter module", "warning")
    
    def builtin_plot_func(self, args_str: str):
        """Plot mathematical function"""
        self.editor.log("Plot function requires plotter module", "warning")
