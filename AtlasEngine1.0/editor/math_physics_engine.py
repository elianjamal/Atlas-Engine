#!/usr/bin/env python3
"""
AtlasEngine - Math & Physics Engine
Scientific computation module for trajectories, simulations, and calculations
"""

import math
from typing import List, Tuple, Dict, Any

class Vector3:
    """3D Vector class for physics calculations"""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return self / mag
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class PhysicsEngine:
    """Physics simulation engine"""
    
    def __init__(self):
        self.gravity = -9.81  # m/s^2
        self.air_resistance = 0.0  # Default: no air resistance
    
    def projectile_motion(self, v0: float, angle_deg: float, height: float = 0.0, 
                         timestep: float = 0.01) -> List[Tuple[float, float]]:
        """
        Calculate projectile motion trajectory
        
        Args:
            v0: Initial velocity (m/s)
            angle_deg: Launch angle (degrees)
            height: Initial height (m)
            timestep: Time step for simulation (s)
        
        Returns:
            List of (x, y) coordinates
        """
        angle_rad = math.radians(angle_deg)
        vx = v0 * math.cos(angle_rad)
        vy = v0 * math.sin(angle_rad)
        
        trajectory = []
        t = 0.0
        x, y = 0.0, height
        
        while y >= 0:
            trajectory.append((x, y))
            
            # Update position
            x = vx * t
            y = height + vy * t + 0.5 * self.gravity * t**2
            
            t += timestep
            
            # Safety limit
            if t > 1000:
                break
        
        return trajectory
    
    def projectile_motion_3d(self, v0: float, angle_h: float, angle_v: float,
                            height: float = 0.0, timestep: float = 0.01) -> List[Tuple[float, float, float]]:
        """
        Calculate 3D projectile motion
        
        Args:
            v0: Initial velocity (m/s)
            angle_h: Horizontal angle (degrees)
            angle_v: Vertical angle (degrees)
            height: Initial height (m)
            timestep: Time step (s)
        
        Returns:
            List of (x, y, z) coordinates
        """
        angle_h_rad = math.radians(angle_h)
        angle_v_rad = math.radians(angle_v)
        
        vx = v0 * math.cos(angle_v_rad) * math.cos(angle_h_rad)
        vy = v0 * math.sin(angle_v_rad)
        vz = v0 * math.cos(angle_v_rad) * math.sin(angle_h_rad)
        
        trajectory = []
        t = 0.0
        
        while True:
            x = vx * t
            y = height + vy * t + 0.5 * self.gravity * t**2
            z = vz * t
            
            if y < 0:
                break
            
            trajectory.append((x, y, z))
            t += timestep
            
            if t > 1000:
                break
        
        return trajectory
    
    def orbital_mechanics(self, radius: float, mass_central: float, 
                         timestep: float = 1.0, duration: float = 100.0) -> List[Tuple[float, float]]:
        """
        Calculate circular orbit
        
        Args:
            radius: Orbital radius (m)
            mass_central: Mass of central body (kg)
            timestep: Time step (s)
            duration: Simulation duration (s)
        
        Returns:
            List of (x, y) coordinates
        """
        G = 6.67430e-11  # Gravitational constant
        
        # Orbital velocity for circular orbit
        v = math.sqrt(G * mass_central / radius)
        
        trajectory = []
        angle = 0.0
        angular_velocity = v / radius
        
        t = 0.0
        while t < duration:
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            trajectory.append((x, y))
            
            angle += angular_velocity * timestep
            t += timestep
        
        return trajectory
    
    def spring_motion(self, amplitude: float, frequency: float, 
                     phase: float = 0.0, duration: float = 10.0,
                     timestep: float = 0.01) -> List[Tuple[float, float]]:
        """
        Calculate spring/harmonic motion
        
        Args:
            amplitude: Maximum displacement (m)
            frequency: Oscillation frequency (Hz)
            phase: Phase offset (radians)
            duration: Simulation duration (s)
            timestep: Time step (s)
        
        Returns:
            List of (t, x) coordinates
        """
        omega = 2 * math.pi * frequency
        trajectory = []
        
        t = 0.0
        while t <= duration:
            x = amplitude * math.cos(omega * t + phase)
            trajectory.append((t, x))
            t += timestep
        
        return trajectory
    
    def pendulum_motion(self, length: float, angle0_deg: float,
                       duration: float = 10.0, timestep: float = 0.01) -> List[Tuple[float, float]]:
        """
        Calculate pendulum motion (small angle approximation)
        
        Args:
            length: Pendulum length (m)
            angle0_deg: Initial angle (degrees)
            duration: Simulation duration (s)
            timestep: Time step (s)
        
        Returns:
            List of (t, angle) coordinates in degrees
        """
        g = abs(self.gravity)
        omega = math.sqrt(g / length)
        angle0 = math.radians(angle0_deg)
        
        trajectory = []
        t = 0.0
        
        while t <= duration:
            angle_rad = angle0 * math.cos(omega * t)
            angle_deg = math.degrees(angle_rad)
            trajectory.append((t, angle_deg))
            t += timestep
        
        return trajectory
    
    def free_fall(self, height: float, timestep: float = 0.01) -> List[Tuple[float, float]]:
        """
        Calculate free fall motion
        
        Args:
            height: Initial height (m)
            timestep: Time step (s)
        
        Returns:
            List of (t, y) coordinates
        """
        trajectory = []
        t = 0.0
        y = height
        
        while y >= 0:
            trajectory.append((t, y))
            y = height + 0.5 * self.gravity * t**2
            t += timestep
        
        return trajectory


class ScientificCalculator:
    """Advanced scientific calculator"""
    
    @staticmethod
    def quadratic(a: float, b: float, c: float) -> Tuple[complex, complex]:
        """Solve quadratic equation ax^2 + bx + c = 0"""
        discriminant = b**2 - 4*a*c
        sqrt_disc = complex(discriminant, 0) ** 0.5
        
        x1 = (-b + sqrt_disc) / (2*a)
        x2 = (-b - sqrt_disc) / (2*a)
        
        return (x1, x2)
    
    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two 2D points"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    @staticmethod
    def distance_3d(x1: float, y1: float, z1: float, 
                   x2: float, y2: float, z2: float) -> float:
        """Calculate distance between two 3D points"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    @staticmethod
    def velocity(displacement: float, time: float) -> float:
        """Calculate velocity"""
        return displacement / time if time != 0 else 0
    
    @staticmethod
    def acceleration(velocity_final: float, velocity_initial: float, time: float) -> float:
        """Calculate acceleration"""
        return (velocity_final - velocity_initial) / time if time != 0 else 0
    
    @staticmethod
    def kinetic_energy(mass: float, velocity: float) -> float:
        """Calculate kinetic energy: KE = 0.5 * m * v^2"""
        return 0.5 * mass * velocity**2
    
    @staticmethod
    def potential_energy(mass: float, height: float, g: float = 9.81) -> float:
        """Calculate gravitational potential energy: PE = m * g * h"""
        return mass * g * height
    
    @staticmethod
    def momentum(mass: float, velocity: float) -> float:
        """Calculate momentum: p = m * v"""
        return mass * velocity
    
    @staticmethod
    def force(mass: float, acceleration: float) -> float:
        """Calculate force: F = m * a"""
        return mass * acceleration
    
    @staticmethod
    def work(force: float, distance: float, angle_deg: float = 0) -> float:
        """Calculate work: W = F * d * cos(θ)"""
        angle_rad = math.radians(angle_deg)
        return force * distance * math.cos(angle_rad)
    
    @staticmethod
    def power(work: float, time: float) -> float:
        """Calculate power: P = W / t"""
        return work / time if time != 0 else 0
    
    @staticmethod
    def centripetal_acceleration(velocity: float, radius: float) -> float:
        """Calculate centripetal acceleration: a_c = v^2 / r"""
        return velocity**2 / radius if radius != 0 else 0
    
    @staticmethod
    def escape_velocity(mass: float, radius: float, G: float = 6.67430e-11) -> float:
        """Calculate escape velocity: v_e = sqrt(2 * G * M / R)"""
        return math.sqrt(2 * G * mass / radius) if radius != 0 else 0
    
    @staticmethod
    def frequency_to_period(frequency: float) -> float:
        """Convert frequency to period"""
        return 1 / frequency if frequency != 0 else 0
    
    @staticmethod
    def period_to_frequency(period: float) -> float:
        """Convert period to frequency"""
        return 1 / period if period != 0 else 0
    
    @staticmethod
    def wavelength(velocity: float, frequency: float) -> float:
        """Calculate wavelength: λ = v / f"""
        return velocity / frequency if frequency != 0 else 0
    
    @staticmethod
    def doppler_effect(f_source: float, v_source: float, v_observer: float, 
                      v_wave: float = 343.0) -> float:
        """
        Calculate Doppler effect frequency
        v_wave: speed of wave in medium (default: speed of sound in air)
        """
        return f_source * (v_wave + v_observer) / (v_wave + v_source)
    
    @staticmethod
    def gravitational_force(m1: float, m2: float, r: float, 
                           G: float = 6.67430e-11) -> float:
        """Calculate gravitational force: F = G * m1 * m2 / r^2"""
        return G * m1 * m2 / (r**2) if r != 0 else 0
    
    @staticmethod
    def coulomb_force(q1: float, q2: float, r: float,
                     k: float = 8.99e9) -> float:
        """Calculate Coulomb force: F = k * q1 * q2 / r^2"""
        return k * q1 * q2 / (r**2) if r != 0 else 0
    
    @staticmethod
    def electric_field(q: float, r: float, k: float = 8.99e9) -> float:
        """Calculate electric field: E = k * q / r^2"""
        return k * q / (r**2) if r != 0 else 0
    
    @staticmethod
    def ohms_law_voltage(current: float, resistance: float) -> float:
        """Calculate voltage: V = I * R"""
        return current * resistance
    
    @staticmethod
    def ohms_law_current(voltage: float, resistance: float) -> float:
        """Calculate current: I = V / R"""
        return voltage / resistance if resistance != 0 else 0
    
    @staticmethod
    def ohms_law_resistance(voltage: float, current: float) -> float:
        """Calculate resistance: R = V / I"""
        return voltage / current if current != 0 else 0
    
    @staticmethod
    def electrical_power(voltage: float, current: float) -> float:
        """Calculate electrical power: P = V * I"""
        return voltage * current
    
    @staticmethod
    def lens_equation(object_distance: float, focal_length: float) -> float:
        """Calculate image distance: 1/f = 1/d_o + 1/d_i"""
        if object_distance == focal_length:
            return float('inf')
        return (object_distance * focal_length) / (object_distance - focal_length)
    
    @staticmethod
    def snells_law(n1: float, theta1_deg: float, n2: float) -> float:
        """Calculate refraction angle: n1 * sin(θ1) = n2 * sin(θ2)"""
        theta1_rad = math.radians(theta1_deg)
        sin_theta2 = (n1 * math.sin(theta1_rad)) / n2
        
        if abs(sin_theta2) > 1:
            return None  # Total internal reflection
        
        theta2_rad = math.asin(sin_theta2)
        return math.degrees(theta2_rad)


class MathFunctions:
    """Advanced mathematical functions"""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial"""
        if n < 0:
            raise ValueError("Factorial undefined for negative numbers")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def permutation(n: int, r: int) -> int:
        """Calculate permutation: P(n,r) = n! / (n-r)!"""
        if r > n:
            return 0
        return MathFunctions.factorial(n) // MathFunctions.factorial(n - r)
    
    @staticmethod
    def combination(n: int, r: int) -> int:
        """Calculate combination: C(n,r) = n! / (r! * (n-r)!)"""
        if r > n:
            return 0
        return MathFunctions.factorial(n) // (MathFunctions.factorial(r) * 
                                              MathFunctions.factorial(n - r))
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number"""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor"""
        while b:
            a, b = b, a % b
        return abs(a)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate least common multiple"""
        return abs(a * b) // MathFunctions.gcd(a, b) if a and b else 0
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Get prime factorization"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    @staticmethod
    def derivative_polynomial(coefficients: List[float]) -> List[float]:
        """Calculate derivative of polynomial"""
        if len(coefficients) <= 1:
            return [0]
        
        result = []
        for i in range(1, len(coefficients)):
            result.append(i * coefficients[i])
        return result
    
    @staticmethod
    def integrate_polynomial(coefficients: List[float], constant: float = 0) -> List[float]:
        """Calculate indefinite integral of polynomial"""
        result = [constant]
        for i, coeff in enumerate(coefficients):
            result.append(coeff / (i + 1))
        return result
    
    @staticmethod
    def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Multiply two matrices"""
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    @staticmethod
    def determinant_2x2(matrix: List[List[float]]) -> float:
        """Calculate determinant of 2x2 matrix"""
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    @staticmethod
    def determinant_3x3(matrix: List[List[float]]) -> float:
        """Calculate determinant of 3x3 matrix"""
        return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))


class Statistics:
    """Statistical functions"""
    
    @staticmethod
    def mean(data: List[float]) -> float:
        """Calculate arithmetic mean"""
        return sum(data) / len(data) if data else 0
    
    @staticmethod
    def median(data: List[float]) -> float:
        """Calculate median"""
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if n == 0:
            return 0
        
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    @staticmethod
    def mode(data: List[float]) -> float:
        """Calculate mode"""
        if not data:
            return 0
        
        frequency = {}
        for value in data:
            frequency[value] = frequency.get(value, 0) + 1
        
        return max(frequency, key=frequency.get)
    
    @staticmethod
    def variance(data: List[float]) -> float:
        """Calculate variance"""
        if not data:
            return 0
        
        mean_val = Statistics.mean(data)
        return sum((x - mean_val) ** 2 for x in data) / len(data)
    
    @staticmethod
    def standard_deviation(data: List[float]) -> float:
        """Calculate standard deviation"""
        return math.sqrt(Statistics.variance(data))
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or not x:
            return 0
        
        n = len(x)
        mean_x = Statistics.mean(x)
        mean_y = Statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x) * 
                               sum((yi - mean_y)**2 for yi in y))
        
        return numerator / denominator if denominator != 0 else 0
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
        """Calculate linear regression: y = mx + b"""
        if len(x) != len(y) or not x:
            return (0, 0)
        
        n = len(x)
        mean_x = Statistics.mean(x)
        mean_y = Statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((xi - mean_x)**2 for xi in x)
        
        m = numerator / denominator if denominator != 0 else 0
        b = mean_y - m * mean_x
        
        return (m, b)
