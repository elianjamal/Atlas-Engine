// T# Calculator Demo
// Comprehensive physics and math calculations

func kinematicsProblems() {
    print('=== KINEMATICS PROBLEMS ===');
    print('');
    
    // Problem 1: Velocity calculation
    print('Problem 1: Car travels 100m in 5s');
    var v = velocity(100, 5);
    print('Solution: Average velocity =', v, 'm/s');
    print('');
    
    // Problem 2: Acceleration
    print('Problem 2: Car accelerates from 10 m/s to 30 m/s in 4s');
    var a = acceleration(30, 10, 4);
    print('Solution: Acceleration =', a, 'm/s²');
    print('');
    
    // Problem 3: Distance
    print('Problem 3: Distance between (0,0) and (3,4)');
    var d = distance2d(0, 0, 3, 4);
    print('Solution: Distance =', d, 'm');
    print('');
}

func energyProblems() {
    print('=== ENERGY PROBLEMS ===');
    print('');
    
    // Kinetic energy
    print('Problem 1: 1000kg car at 20 m/s');
    var ke = kineticEnergy(1000, 20);
    print('Kinetic energy =', ke, 'J');
    print('');
    
    // Potential energy
    print('Problem 2: 50kg object at 10m height');
    var pe = potentialEnergy(50, 10);
    print('Potential energy =', pe, 'J');
    print('');
    
    // Work calculation
    print('Problem 3: 100N force pushes box 5m');
    var w = work(100, 5, 0);
    print('Work done =', w, 'J');
    print('');
    
    // Power
    print('Problem 4: 1000J of work in 2s');
    var p = power(1000, 2);
    print('Power =', p, 'W');
    print('');
}

func momentumProblems() {
    print('=== MOMENTUM PROBLEMS ===');
    print('');
    
    print('Problem: 70kg person running at 8 m/s');
    var p = momentum(70, 8);
    print('Momentum =', p, 'kg·m/s');
    print('');
    
    print('Problem: Force on 5kg object with 10 m/s² acceleration');
    var f = force(5, 10);
    print('Force =', f, 'N');
    print('');
}

func mathProblems() {
    print('=== MATHEMATICS PROBLEMS ===');
    print('');
    
    // Quadratic equations
    print('Solve: x² - 7x + 12 = 0');
    quadratic(1, -7, 12);
    print('');
    
    print('Solve: 2x² - x - 6 = 0');
    quadratic(2, -1, -6);
    print('');
    
    // Factorials and combinations
    print('Calculate 7!');
    var fact = factorial(7);
    print('7! =', fact);
    print('');
    
    // Fibonacci
    print('First 10 Fibonacci numbers:');
    var i = 0;
    while (i < 10) {
        var fib = fibonacci(i);
        print('  fib(', i, ') =', fib);
        i = i + 1;
    }
    print('');
    
    // Prime numbers
    print('Testing prime numbers:');
    print('  Is 17 prime?', isPrime(17));
    print('  Is 18 prime?', isPrime(18));
    print('  Is 97 prime?', isPrime(97));
    print('');
    
    // GCD and LCM
    print('GCD and LCM:');
    print('  gcd(48, 18) =', gcd(48, 18));
    print('  lcm(12, 18) =', lcm(12, 18));
    print('');
}

func trigonometryProblems() {
    print('=== TRIGONOMETRY PROBLEMS ===');
    print('');
    
    print('Right triangle with angle 30°:');
    var angle_30 = PI / 6;
    print('  sin(30°) =', sin(angle_30));
    print('  cos(30°) =', cos(angle_30));
    print('  tan(30°) =', tan(angle_30));
    print('');
    
    print('Special angles:');
    print('  sin(45°) =', sin(PI / 4));
    print('  cos(60°) =', cos(PI / 3));
    print('  tan(45°) =', tan(PI / 4));
    print('');
    
    // Inverse trig
    print('Inverse functions:');
    print('  asin(0.5) =', asin(0.5), 'rad');
    print('  acos(0.5) =', acos(0.5), 'rad');
    print('  atan(1) =', atan(1), 'rad');
    print('');
}

func logarithmProblems() {
    print('=== LOGARITHM PROBLEMS ===');
    print('');
    
    print('Common logarithms:');
    print('  log(1) =', log(1));
    print('  log(10) =', log(10));
    print('  log(100) =', log(100));
    print('  log(1000) =', log(1000));
    print('');
    
    print('Natural logarithms:');
    print('  ln(1) =', ln(1));
    print('  ln(E) =', ln(E));
    print('  ln(7.389) ≈', ln(7.389));
    print('');
    
    print('Exponentials:');
    print('  exp(0) =', exp(0));
    print('  exp(1) =', exp(1));
    print('  exp(2) =', exp(2));
    print('');
}

func advancedCalculations() {
    print('=== ADVANCED CALCULATIONS ===');
    print('');
    
    // Powers and roots
    print('Powers:');
    print('  2^10 =', pow(2, 10));
    print('  3^4 =', pow(3, 4));
    print('  10^3 =', pow(10, 3));
    print('');
    
    print('Roots:');
    print('  √16 =', sqrt(16));
    print('  √2 =', sqrt(2));
    print('  √100 =', sqrt(100));
    print('');
    
    // Absolute value and rounding
    print('Rounding:');
    print('  floor(3.7) =', floor(3.7));
    print('  ceil(3.2) =', ceil(3.2));
    print('  round(3.5) =', round(3.5));
    print('  abs(-42) =', abs(-42));
    print('');
}

func main() {
    print('╔════════════════════════════════════════╗');
    print('║   ATLASENGINE CALCULATOR SUITE        ║');
    print('║   Physics & Math Problem Solver       ║');
    print('╚════════════════════════════════════════╝');
    print('');
    
    kinematicsProblems();
    energyProblems();
    momentumProblems();
    mathProblems();
    trigonometryProblems();
    logarithmProblems();
    advancedCalculations();
    
    print('╔════════════════════════════════════════╗');
    print('║      CALCULATION SUITE COMPLETE!      ║');
    print('║                                        ║');
    print('║  All problems solved successfully     ║');
    print('╚════════════════════════════════════════╝');
}

main();
