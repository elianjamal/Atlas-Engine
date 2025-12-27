// T# Scientific Demo
// Demonstrates physics, math, and calculator functions

func demonstrateProjectileMotion() {
    print('=== PROJECTILE MOTION ===');
    
    // Launch projectile at 45 degrees, 30 m/s
    var v0 = 30;
    var angle = 45;
    print('Launching projectile:');
    print('  Initial velocity:', v0, 'm/s');
    print('  Angle:', angle, 'degrees');
    
    projectile(v0, angle, 0);
    print('');
}

func demonstrateMathFunctions() {
    print('=== MATH FUNCTIONS ===');
    
    // Trigonometry
    var angle_rad = PI / 4;
    print('sin(π/4) =', sin(angle_rad));
    print('cos(π/4) =', cos(angle_rad));
    print('tan(π/4) =', tan(angle_rad));
    
    // Powers and roots
    print('sqrt(144) =', sqrt(144));
    print('pow(2, 10) =', pow(2, 10));
    
    // Advanced math
    print('5! =', factorial(5));
    print('fib(10) =', fibonacci(10));
    print('gcd(48, 18) =', gcd(48, 18));
    
    // Logarithms
    print('log(100) =', log(100));
    print('ln(E) =', ln(E));
    
    print('');
}

func demonstratePhysicsCalculations() {
    print('=== PHYSICS CALCULATIONS ===');
    
    // Kinematics
    var mass = 10;
    var velocity = 20;
    var height = 50;
    
    print('Object properties:');
    print('  Mass:', mass, 'kg');
    print('  Velocity:', velocity, 'm/s');
    print('  Height:', height, 'm');
    
    var ke = kineticEnergy(mass, velocity);
    print('Kinetic Energy:', ke, 'J');
    
    var pe = potentialEnergy(mass, height);
    print('Potential Energy:', pe, 'J');
    
    var p = momentum(mass, velocity);
    print('Momentum:', p, 'kg·m/s');
    
    print('');
}

func demonstrateQuadraticSolver() {
    print('=== QUADRATIC EQUATION SOLVER ===');
    
    // Solve x² - 5x + 6 = 0
    print('Solving: x² - 5x + 6 = 0');
    quadratic(1, -5, 6);
    
    // Solve 2x² + 3x - 2 = 0
    print('Solving: 2x² + 3x - 2 = 0');
    quadratic(2, 3, -2);
    
    print('');
}

func demonstrateDistanceCalculations() {
    print('=== DISTANCE CALCULATIONS ===');
    
    // 2D distance
    print('Point A: (0, 0)');
    print('Point B: (3, 4)');
    var dist2d = distance2d(0, 0, 3, 4);
    print('Distance (2D):', dist2d);
    
    // 3D distance
    print('Point C: (1, 2, 3)');
    print('Point D: (4, 6, 8)');
    var dist3d = distance3d(1, 2, 3, 4, 6, 8);
    print('Distance (3D):', dist3d);
    
    print('');
}

func demonstrateFreefall() {
    print('=== FREE FALL SIMULATION ===');
    
    var initial_height = 100;
    print('Dropping object from', initial_height, 'm');
    
    freefall(initial_height);
    
    print('');
}

func demonstrateOscillations() {
    print('=== HARMONIC MOTION ===');
    
    // Spring oscillation
    print('Spring: Amplitude=2m, Frequency=1Hz');
    spring(2, 1);
    
    // Pendulum
    print('Pendulum: Length=1m, Initial angle=30°');
    pendulum(1, 30);
    
    print('');
}

func demonstrateStatistics() {
    print('=== STATISTICS ===');
    
    // Note: In full implementation, you'd pass arrays
    print('Dataset: 2, 4, 6, 8, 10');
    print('Mean: 6.0');
    print('Median: 6.0');
    print('Std Dev: ~2.83');
    
    print('');
}

func runCompleteDemo() {
    print('╔════════════════════════════════════╗');
    print('║   ATLASENGINE SCIENTIFIC DEMO     ║');
    print('║   Math, Physics & Trajectories    ║');
    print('╚════════════════════════════════════╝');
    print('');
    
    demonstrateProjectileMotion();
    demonstrateMathFunctions();
    demonstratePhysicsCalculations();
    demonstrateQuadraticSolver();
    demonstrateDistanceCalculations();
    demonstrateFreefall();
    demonstrateOscillations();
    
    print('╔════════════════════════════════════╗');
    print('║         DEMO COMPLETE!            ║');
    print('║                                    ║');
    print('║  Check the Trajectory Plotter tab ║');
    print('║  to see visualizations            ║');
    print('╚════════════════════════════════════╝');
}

// Run the complete demonstration
runCompleteDemo();
