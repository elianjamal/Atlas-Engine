# AtlasEngine - Scientific Features Guide

## Overview

AtlasEngine includes a comprehensive suite of scientific, mathematical, and physics calculation tools, making it perfect for:
- **Trajectory Analysis** - Projectile motion, orbits, oscillations
- **Scientific Calculations** - Physics formulas, energy, momentum, forces
- **Advanced Mathematics** - Trigonometry, calculus, statistics, number theory
- **Data Visualization** - Interactive trajectory plotting and graphing

---

## Physics Functions

### Trajectory & Motion

#### `projectile(v0, angle, height)`
Calculate and plot projectile motion trajectory.

**Parameters:**
- `v0` - Initial velocity (m/s)
- `angle` - Launch angle (degrees)
- `height` - Initial height (m, default: 0)

**Example:**
```typescript
// Launch at 30 m/s, 45 degrees
projectile(30, 45, 0);

// Launch from 10m height
projectile(25, 30, 10);
```

**Output:** Plots trajectory and displays max height and range.

---

#### `freefall(height)`
Simulate free fall motion.

**Parameters:**
- `height` - Initial height (m)

**Example:**
```typescript
// Drop from 50 meters
freefall(50);
```

---

#### `orbit(radius, mass, duration)`
Calculate circular orbital motion.

**Parameters:**
- `radius` - Orbital radius (m)
- `mass` - Mass of central body (kg)
- `duration` - Simulation time (s, default: 100)

**Example:**
```typescript
// Earth orbit simulation
orbit(6.371e6 + 400000, 5.972e24, 5400);
```

---

#### `spring(amplitude, frequency)`
Simulate harmonic spring motion.

**Parameters:**
- `amplitude` - Maximum displacement (m)
- `frequency` - Oscillation frequency (Hz)

**Example:**
```typescript
// Spring with 2m amplitude, 1Hz
spring(2, 1);
```

---

#### `pendulum(length, angle0)`
Simulate pendulum motion (small angle approximation).

**Parameters:**
- `length` - Pendulum length (m)
- `angle0` - Initial angle (degrees)

**Example:**
```typescript
// 1m pendulum, 30 degree release
pendulum(1, 30);
```

---

## Calculator Functions

### Kinematics

#### `velocity(displacement, time)`
Calculate average velocity.

**Formula:** v = Δx / Δt

**Example:**
```typescript
var v = velocity(100, 5);  // 100m in 5s = 20 m/s
print('Velocity:', v, 'm/s');
```

---

#### `acceleration(vf, vi, time)`
Calculate acceleration.

**Formula:** a = (v_f - v_i) / t

**Example:**
```typescript
var a = acceleration(30, 10, 4);  // 5 m/s²
```

---

#### `distance2d(x1, y1, x2, y2)`
Calculate 2D Euclidean distance.

**Formula:** d = √[(x₂-x₁)² + (y₂-y₁)²]

**Example:**
```typescript
var d = distance2d(0, 0, 3, 4);  // = 5
```

---

#### `distance3d(x1, y1, z1, x2, y2, z2)`
Calculate 3D Euclidean distance.

**Example:**
```typescript
var d = distance3d(0, 0, 0, 1, 2, 2);  // = 3
```

---

### Energy & Work

#### `kineticEnergy(mass, velocity)`
Calculate kinetic energy.

**Formula:** KE = ½mv²

**Example:**
```typescript
var ke = kineticEnergy(10, 20);  // 2000 J
print('Kinetic Energy:', ke, 'J');
```

---

#### `potentialEnergy(mass, height)`
Calculate gravitational potential energy.

**Formula:** PE = mgh (g = 9.81 m/s²)

**Example:**
```typescript
var pe = potentialEnergy(5, 10);  // 490.5 J
```

---

#### `work(force, distance, angle)`
Calculate work done.

**Formula:** W = F · d · cos(θ)

**Example:**
```typescript
var w = work(100, 5, 0);  // 500 J (0° angle)
var w2 = work(100, 5, 60);  // 250 J (60° angle)
```

---

#### `power(work, time)`
Calculate power.

**Formula:** P = W / t

**Example:**
```typescript
var p = power(1000, 2);  // 500 W
```

---

### Forces & Momentum

#### `momentum(mass, velocity)`
Calculate momentum.

**Formula:** p = mv

**Example:**
```typescript
var p = momentum(70, 8);  // 560 kg·m/s
```

---

#### `force(mass, acceleration)`
Calculate force using Newton's 2nd law.

**Formula:** F = ma

**Example:**
```typescript
var f = force(10, 5);  // 50 N
```

---

## Mathematics Functions

### Trigonometry

All trig functions use **radians**. Use `PI` constant for conversions.

```typescript
// Constants available
PI = 3.14159...
E = 2.71828...
TAU = 6.28318... (2π)

// Convert degrees to radians
var angle_rad = 45 * PI / 180;

// Trig functions
sin(angle_rad)
cos(angle_rad)
tan(angle_rad)

// Inverse trig
asin(0.5)  // Returns radians
acos(0.5)
atan(1.0)
```

**Example:**
```typescript
// Right triangle calculations
var angle = 30 * PI / 180;  // 30 degrees
var opposite = 5;
var hypotenuse = opposite / sin(angle);
print('Hypotenuse:', hypotenuse);
```

---

### Powers & Roots

```typescript
// Powers
pow(2, 10)     // 2^10 = 1024
pow(3, 3)      // 27

// Roots
sqrt(144)      // 12
sqrt(2)        // 1.414...

// Exponential
exp(1)         // e^1 = e
exp(2)         // e^2 = 7.389...
```

---

### Logarithms

```typescript
// Common logarithm (base 10)
log(100)       // 2
log(1000)      // 3

// Natural logarithm (base e)
ln(E)          // 1
ln(7.389)      // ≈ 2

// Relationship: e^x and ln(x) are inverses
exp(ln(5))     // 5
ln(exp(3))     // 3
```

---

### Number Theory

#### `factorial(n)`
Calculate n!

**Example:**
```typescript
factorial(5)   // 120
factorial(10)  // 3628800
```

---

#### `fibonacci(n)`
Calculate nth Fibonacci number.

**Example:**
```typescript
fibonacci(10)  // 55
fibonacci(20)  // 6765
```

---

#### `isPrime(n)`
Check if number is prime.

**Example:**
```typescript
isPrime(17)    // true
isPrime(18)    // false
isPrime(97)    // true
```

---

#### `gcd(a, b)`
Greatest common divisor.

**Example:**
```typescript
gcd(48, 18)    // 6
gcd(100, 35)   // 5
```

---

#### `lcm(a, b)`
Least common multiple.

**Example:**
```typescript
lcm(12, 18)    // 36
lcm(15, 20)    // 60
```

---

### Rounding & Absolute Value

```typescript
floor(3.7)     // 3
ceil(3.2)      // 4
round(3.5)     // 4
abs(-42)       // 42
abs(15)        // 15
```

---

## Algebra

### `quadratic(a, b, c)`
Solve quadratic equation ax² + bx + c = 0

**Example:**
```typescript
// Solve x² - 5x + 6 = 0
quadratic(1, -5, 6);
// Solutions: x1=3, x2=2

// Solve 2x² + 3x - 2 = 0
quadratic(2, 3, -2);
// Solutions: x1=0.5, x2=-2
```

---

## Statistics Functions

### `mean(data)`
Calculate arithmetic mean (average).

**Example:**
```typescript
// Dataset: 2, 4, 6, 8, 10
mean(2, 4, 6, 8, 10)  // 6.0
```

---

### `median(data)`
Calculate median (middle value).

---

### `stddev(data)`
Calculate standard deviation.

---

## Plotting & Visualization

### Using the Trajectory Plotter

1. Write script with physics functions
2. Run script (F5)
3. Switch to **Trajectory Plotter** tab
4. View plotted trajectories

### Multiple Trajectories

Compare different scenarios:

```typescript
// Compare different launch angles
projectile(25, 15, 0);
projectile(25, 30, 0);
projectile(25, 45, 0);
projectile(25, 60, 0);
projectile(25, 75, 0);
```

Each trajectory is plotted in a different color with automatic legend.

---

## Real-World Examples

### Example 1: Cannon Range Calculation

```typescript
func cannonRange() {
    var muzzle_velocity = 150;  // m/s
    var angle = 30;             // degrees
    
    print('Cannon specifications:');
    print('  Muzzle velocity:', muzzle_velocity, 'm/s');
    print('  Firing angle:', angle, '°');
    
    projectile(muzzle_velocity, angle, 0);
}
```

---

### Example 2: Basketball Physics

```typescript
func basketballShot() {
    var distance = 4.57;   // Free throw distance (m)
    var hoop_height = 3.05; // Hoop height (m)
    var release_height = 2.0; // Release height (m)
    
    // Typical free throw velocity
    var v0 = 7.5;  // m/s
    var angle = 52; // degrees
    
    projectile(v0, angle, release_height);
    
    print('Free throw trajectory calculated');
}
```

---

### Example 3: Satellite Orbit

```typescript
func satelliteOrbit() {
    var earth_radius = 6.371e6;     // m
    var altitude = 400000;          // 400 km
    var earth_mass = 5.972e24;      // kg
    
    var orbit_radius = earth_radius + altitude;
    
    print('ISS Orbital Parameters:');
    print('  Altitude:', altitude / 1000, 'km');
    print('  Orbital radius:', orbit_radius / 1000, 'km');
    
    orbit(orbit_radius, earth_mass, 5400);
}
```

---

### Example 4: Energy Conservation

```typescript
func energyConservation() {
    var mass = 2;      // kg
    var height = 50;   // m
    var velocity = 0;  // Initially at rest
    
    // Initial energy (all potential)
    var pe_initial = potentialEnergy(mass, height);
    var ke_initial = kineticEnergy(mass, velocity);
    var total = pe_initial + ke_initial;
    
    print('Initial state (at height):');
    print('  PE =', pe_initial, 'J');
    print('  KE =', ke_initial, 'J');
    print('  Total =', total, 'J');
    
    // Final state (just before impact)
    var v_final = sqrt(2 * 9.81 * height);
    var pe_final = 0;
    var ke_final = kineticEnergy(mass, v_final);
    
    print('Final state (at ground):');
    print('  PE =', pe_final, 'J');
    print('  KE =', ke_final, 'J');
    print('  Total =', ke_final, 'J');
    
    print('Energy conserved!');
}
```

---

## Tips for Scientific Computing

1. **Use Constants**: `PI`, `E`, `TAU` are pre-defined
2. **Units Matter**: Keep track of units (m, s, kg, etc.)
3. **Visualize**: Always check the Trajectory Plotter tab
4. **Compare**: Plot multiple scenarios for analysis
5. **Verify**: Check results against known values

---

## Keyboard Shortcuts

- **F5**: Run script
- **Ctrl+S**: Save script
- **Ctrl+Tab**: Switch between tabs

---

## Advanced Topics

### Custom Physics Simulations

Combine multiple functions for complex analysis:

```typescript
func projectileEnergyAnalysis(v0, angle, mass) {
    // Initial kinetic energy
    var ke0 = kineticEnergy(mass, v0);
    print('Initial KE:', ke0, 'J');
    
    // Calculate trajectory
    projectile(v0, angle, 0);
    
    // Velocity components
    var angle_rad = angle * PI / 180;
    var vx = v0 * cos(angle_rad);
    var vy = v0 * sin(angle_rad);
    
    // At peak: vy = 0, only vx remains
    var ke_peak = kineticEnergy(mass, vx);
    print('KE at peak:', ke_peak, 'J');
    
    // Energy converted to PE
    var pe_peak = ke0 - ke_peak;
    print('PE at peak:', pe_peak, 'J');
    
    // Calculate max height from energy
    var h_max = pe_peak / (mass * 9.81);
    print('Max height:', h_max, 'm');
}
```

---

## Troubleshooting

### "Unknown function" error
- Check function spelling
- Ensure you're using correct parameter count

### No plot appears
- Make sure to switch to Trajectory Plotter tab
- Check that script ran successfully (no errors in Output)

### Incorrect results
- Verify units (m, s, kg, radians)
- Check that angles are in radians for trig functions
- Use `PI / 180` to convert degrees to radians

---

## Function Reference Quick List

**Physics:** projectile, orbit, freefall, spring, pendulum

**Kinematics:** velocity, acceleration, distance2d, distance3d

**Energy:** kineticEnergy, potentialEnergy, work, power

**Forces:** momentum, force

**Math:** sin, cos, tan, asin, acos, atan, sqrt, pow, abs, floor, ceil, round, log, ln, exp

**Algebra:** quadratic

**Number Theory:** factorial, fibonacci, isPrime, gcd, lcm

**Statistics:** mean, median, stddev

---

For more examples, see:
- `scripts/scientific_demo.ts`
- `scripts/trajectory_analysis.ts`
- `scripts/calculator_demo.ts`
