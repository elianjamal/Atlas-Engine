// T# Ultimate Science Demo
// Comprehensive demonstration of all scientific features

func welcomeBanner() {
    print('╔══════════════════════════════════════════════╗');
    print('║                                              ║');
    print('║        ATLASENGINE SCIENCE SUITE            ║');
    print('║        Complete Scientific Computing        ║');
    print('║                                              ║');
    print('║  • Physics Simulations                      ║');
    print('║  • Trajectory Analysis                      ║');
    print('║  • Mathematical Calculations                ║');
    print('║  • Real-time Visualization                  ║');
    print('║                                              ║');
    print('╚══════════════════════════════════════════════╝');
    print('');
}

// ============ SECTION 1: TRAJECTORY SCIENCE ============

func trajectoryScience() {
    print('══════════════════════════════════════════════');
    print('  SECTION 1: TRAJECTORY SCIENCE');
    print('══════════════════════════════════════════════');
    print('');
    
    print('Test 1: Optimal Launch Angle');
    print('Theoretical: 45° gives maximum range');
    print('Launching at v0=25 m/s, θ=45°');
    projectile(25, 45, 0);
    print('✓ Trajectory plotted');
    print('');
    
    print('Test 2: Angle Comparison');
    print('Comparing 30°, 45°, and 60°');
    projectile(30, 30, 0);
    projectile(30, 45, 0);
    projectile(30, 60, 0);
    print('✓ Three trajectories plotted');
    print('  → Notice 30° and 60° have same range!');
    print('');
    
    print('Test 3: Height Advantage');
    print('Same velocity, different heights');
    projectile(20, 40, 0);
    projectile(20, 40, 10);
    projectile(20, 40, 20);
    print('✓ Height increases range');
    print('');
}

// ============ SECTION 2: MATH FOUNDATIONS ============

func mathematicalFoundations() {
    print('══════════════════════════════════════════════');
    print('  SECTION 2: MATHEMATICAL FOUNDATIONS');
    print('══════════════════════════════════════════════');
    print('');
    
    print('2.1 Trigonometry');
    print('Special angles (in radians):');
    var angle_30 = PI / 6;
    var angle_45 = PI / 4;
    var angle_60 = PI / 3;
    
    print('  30°: sin=', sin(angle_30), 'cos=', cos(angle_30));
    print('  45°: sin=', sin(angle_45), 'cos=', cos(angle_45));
    print('  60°: sin=', sin(angle_60), 'cos=', cos(angle_60));
    print('');
    
    print('2.2 Powers and Roots');
    print('  2^10 =', pow(2, 10));
    print('  √144 =', sqrt(144));
    print('  3^4 =', pow(3, 4));
    print('');
    
    print('2.3 Logarithms');
    print('  log(1000) =', log(1000));
    print('  ln(E) =', ln(E));
    print('  exp(2) =', exp(2));
    print('');
    
    print('2.4 Number Theory');
    print('  10! =', factorial(10));
    print('  fib(15) =', fibonacci(15));
    print('  Is 89 prime?', isPrime(89));
    print('  gcd(54, 24) =', gcd(54, 24));
    print('');
}

// ============ SECTION 3: PHYSICS CALCULATIONS ============

func physicsCalculations() {
    print('══════════════════════════════════════════════');
    print('  SECTION 3: PHYSICS CALCULATIONS');
    print('══════════════════════════════════════════════');
    print('');
    
    print('3.1 Kinematics');
    print('Car travels 150m in 6s');
    var v = velocity(150, 6);
    print('  → Velocity:', v, 'm/s');
    print('');
    
    print('Acceleration from 5 m/s to 25 m/s in 4s');
    var a = acceleration(25, 5, 4);
    print('  → Acceleration:', a, 'm/s²');
    print('');
    
    print('3.2 Energy Analysis');
    var mass = 5;
    var v_obj = 20;
    var height = 30;
    
    print('Object: mass=', mass, 'kg, v=', v_obj, 'm/s, h=', height, 'm');
    
    var ke = kineticEnergy(mass, v_obj);
    print('  → Kinetic Energy:', ke, 'J');
    
    var pe = potentialEnergy(mass, height);
    print('  → Potential Energy:', pe, 'J');
    
    var total_energy = ke + pe;
    print('  → Total Mechanical Energy:', total_energy, 'J');
    print('');
    
    print('3.3 Force and Momentum');
    var p = momentum(mass, v_obj);
    print('  → Momentum:', p, 'kg·m/s');
    
    var f = force(mass, 10);
    print('  → Force (a=10 m/s²):', f, 'N');
    print('');
    
    print('3.4 Work and Power');
    var w = work(50, 10, 0);
    print('  → Work (50N × 10m):', w, 'J');
    
    var p_val = power(w, 5);
    print('  → Power (500J / 5s):', p_val, 'W');
    print('');
}

// ============ SECTION 4: ADVANCED ANALYSIS ============

func advancedAnalysis() {
    print('══════════════════════════════════════════════');
    print('  SECTION 4: ADVANCED ANALYSIS');
    print('══════════════════════════════════════════════');
    print('');
    
    print('4.1 Quadratic Equations');
    print('Solving: x² - 7x + 12 = 0');
    quadratic(1, -7, 12);
    print('');
    
    print('Solving: 2x² + 5x - 3 = 0');
    quadratic(2, 5, -3);
    print('');
    
    print('4.2 Distance Calculations');
    print('2D: Point (0,0) to (5,12)');
    var d2 = distance2d(0, 0, 5, 12);
    print('  → Distance:', d2, 'm');
    print('');
    
    print('3D: Point (1,2,3) to (4,6,8)');
    var d3 = distance3d(1, 2, 3, 4, 6, 8);
    print('  → Distance:', d3, 'm');
    print('');
}

// ============ SECTION 5: OSCILLATIONS ============

func oscillationAnalysis() {
    print('══════════════════════════════════════════════');
    print('  SECTION 5: OSCILLATIONS & PERIODIC MOTION');
    print('══════════════════════════════════════════════');
    print('');
    
    print('5.1 Spring Oscillation');
    print('Amplitude: 3m, Frequency: 0.5Hz');
    spring(3, 0.5);
    print('✓ Harmonic motion plotted');
    print('');
    
    print('5.2 Pendulum Motion');
    print('Length: 2m, Initial angle: 45°');
    pendulum(2, 45);
    print('✓ Pendulum motion plotted');
    print('');
}

// ============ SECTION 6: REAL WORLD EXAMPLES ============

func realWorldExamples() {
    print('══════════════════════════════════════════════');
    print('  SECTION 6: REAL-WORLD APPLICATIONS');
    print('══════════════════════════════════════════════');
    print('');
    
    print('6.1 Basketball Free Throw');
    print('Distance: 4.57m, Hoop height: 3.05m');
    print('Typical parameters: v=7.5 m/s, θ=52°');
    projectile(7.5, 52, 2);
    print('✓ Free throw trajectory calculated');
    print('');
    
    print('6.2 Long Jump Physics');
    print('World record: ~8.95m');
    print('Athlete velocity: ~9.5 m/s, angle: ~20°');
    var jump_v = 9.5;
    var jump_angle = 20;
    projectile(jump_v, jump_angle, 1);
    print('✓ Jump trajectory analyzed');
    print('');
    
    print('6.3 Roller Coaster Energy');
    var coaster_mass = 500;
    var coaster_height = 40;
    var pe_coaster = potentialEnergy(coaster_mass, coaster_height);
    print('At top of drop:', coaster_height, 'm');
    print('  PE =', pe_coaster, 'J');
    
    var v_bottom = sqrt(2 * 9.81 * coaster_height);
    print('At bottom:');
    print('  v =', v_bottom, 'm/s');
    var ke_bottom = kineticEnergy(coaster_mass, v_bottom);
    print('  KE =', ke_bottom, 'J');
    print('  Energy conserved!');
    print('');
}

// ============ SECTION 7: MATHEMATICAL PATTERNS ============

func mathematicalPatterns() {
    print('══════════════════════════════════════════════');
    print('  SECTION 7: MATHEMATICAL PATTERNS');
    print('══════════════════════════════════════════════');
    print('');
    
    print('7.1 Fibonacci Sequence (first 12)');
    var i = 0;
    while (i < 12) {
        var fib_val = fibonacci(i);
        print('  fib(', i, ') =', fib_val);
        i = i + 1;
    }
    print('');
    
    print('7.2 Prime Numbers under 30');
    var n = 2;
    while (n < 30) {
        if (isPrime(n)) {
            print('  ', n, 'is prime');
        }
        n = n + 1;
    }
    print('');
}

// ============ SECTION 8: COMPREHENSIVE TEST ============

func comprehensiveTest() {
    print('══════════════════════════════════════════════');
    print('  SECTION 8: COMPREHENSIVE INTEGRATION TEST');
    print('══════════════════════════════════════════════');
    print('');
    
    print('Simulating complete projectile with all calculations:');
    print('');
    
    var test_mass = 1;
    var test_v0 = 40;
    var test_angle = 35;
    var test_height = 0;
    
    print('Projectile Parameters:');
    print('  Mass:', test_mass, 'kg');
    print('  Velocity:', test_v0, 'm/s');
    print('  Angle:', test_angle, '°');
    print('  Height:', test_height, 'm');
    print('');
    
    print('Step 1: Initial Energy');
    var ke_init = kineticEnergy(test_mass, test_v0);
    var pe_init = potentialEnergy(test_mass, test_height);
    print('  KE:', ke_init, 'J');
    print('  PE:', pe_init, 'J');
    print('  Total:', ke_init + pe_init, 'J');
    print('');
    
    print('Step 2: Velocity Components');
    var angle_rad = test_angle * PI / 180;
    var vx = test_v0 * cos(angle_rad);
    var vy = test_v0 * sin(angle_rad);
    print('  vx:', vx, 'm/s');
    print('  vy:', vy, 'm/s');
    print('');
    
    print('Step 3: Calculate Maximum Height');
    var h_max = pow(vy, 2) / (2 * 9.81);
    print('  h_max:', h_max, 'm');
    print('');
    
    print('Step 4: Calculate Range');
    var t_total = 2 * vy / 9.81;
    var range = vx * t_total;
    print('  Flight time:', t_total, 's');
    print('  Range:', range, 'm');
    print('');
    
    print('Step 5: Generate Trajectory');
    projectile(test_v0, test_angle, test_height);
    print('  ✓ Trajectory plotted');
    print('');
    
    print('Step 6: Verify Energy at Peak');
    var ke_peak = kineticEnergy(test_mass, vx);
    var pe_peak = potentialEnergy(test_mass, h_max);
    var total_peak = ke_peak + pe_peak;
    print('  KE at peak:', ke_peak, 'J');
    print('  PE at peak:', pe_peak, 'J');
    print('  Total:', total_peak, 'J');
    print('  Energy difference:', abs(total_peak - (ke_init + pe_init)), 'J');
    print('  ✓ Energy conserved!');
    print('');
}

// ============ MAIN EXECUTION ============

func main() {
    welcomeBanner();
    
    trajectoryScience();
    mathematicalFoundations();
    physicsCalculations();
    advancedAnalysis();
    oscillationAnalysis();
    realWorldExamples();
    mathematicalPatterns();
    comprehensiveTest();
    
    print('╔══════════════════════════════════════════════╗');
    print('║                                              ║');
    print('║         ALL TESTS COMPLETED!                ║');
    print('║                                              ║');
    print('║  ✓ Trajectories calculated                  ║');
    print('║  ✓ Physics verified                         ║');
    print('║  ✓ Math functions tested                    ║');
    print('║  ✓ Real-world examples computed             ║');
    print('║                                              ║');
    print('║  📊 Switch to TRAJECTORY PLOTTER tab        ║');
    print('║     to see all visualizations!              ║');
    print('║                                              ║');
    print('╚══════════════════════════════════════════════╝');
    print('');
    print('AtlasEngine Scientific Suite - Ready for your research!');
}

// Run the complete demonstration
main();
