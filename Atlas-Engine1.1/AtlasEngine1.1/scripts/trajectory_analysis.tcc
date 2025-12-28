// T# Trajectory Analysis
// Compare different projectile launches

func compareAngles() {
    print('=== PROJECTILE ANGLE COMPARISON ===');
    print('Comparing projectiles at different angles');
    print('Initial velocity: 25 m/s');
    print('');
    
    var v0 = 25;
    
    // Test different angles
    var angles = 15;
    print('Launch angle: 15°');
    projectile(v0, 15, 0);
    
    print('Launch angle: 30°');
    projectile(v0, 30, 0);
    
    print('Launch angle: 45° (optimal)');
    projectile(v0, 45, 0);
    
    print('Launch angle: 60°');
    projectile(v0, 60, 0);
    
    print('Launch angle: 75°');
    projectile(v0, 75, 0);
    
    print('');
    print('Switch to Trajectory Plotter tab to see results!');
}

func calculateOptimalAngle() {
    print('=== OPTIMAL LAUNCH ANGLE ===');
    print('For maximum range, launch at 45°');
    print('');
    
    var v0 = 30;
    print('Velocity:', v0, 'm/s');
    print('Optimal angle: 45°');
    
    // Calculate theoretical maximum range
    var range_max = pow(v0, 2) / 9.81;
    print('Theoretical max range:', range_max, 'm');
    
    projectile(v0, 45, 0);
}

func heightAdvantage() {
    print('=== HEIGHT ADVANTAGE DEMO ===');
    print('Launching from elevated positions');
    print('');
    
    var v0 = 20;
    var angle = 30;
    
    print('Ground level (h=0m)');
    projectile(v0, angle, 0);
    
    print('From 10m height');
    projectile(v0, angle, 10);
    
    print('From 20m height');
    projectile(v0, angle, 20);
    
    print('Higher starting positions increase range!');
}

func realWorldExamples() {
    print('=== REAL WORLD EXAMPLES ===');
    print('');
    
    // Basketball shot
    print('Basketball free throw:');
    print('  Distance: 4.57m');
    print('  Height: 3.05m');
    print('  Typical angle: 52°');
    var v_basketball = 7.5;
    projectile(v_basketball, 52, 2);
    
    print('');
    
    // Cannon
    print('Historical cannon:');
    print('  Velocity: 150 m/s');
    print('  Angle: 30°');
    projectile(150, 30, 0);
}

func energyAnalysis() {
    print('=== ENERGY ANALYSIS ===');
    print('');
    
    var mass = 5;
    var v0 = 30;
    var height = 0;
    
    print('Projectile mass:', mass, 'kg');
    print('Launch velocity:', v0, 'm/s');
    
    var ke_initial = kineticEnergy(mass, v0);
    print('Initial kinetic energy:', ke_initial, 'J');
    
    var pe_initial = potentialEnergy(mass, height);
    print('Initial potential energy:', pe_initial, 'J');
    
    var total_energy = ke_initial + pe_initial;
    print('Total mechanical energy:', total_energy, 'J');
    
    print('');
    print('At maximum height:');
    print('  Vertical velocity = 0');
    print('  All vertical KE → PE');
    
    // Horizontal component of velocity
    var v_horizontal = v0 * cos(PI / 4);
    print('  Horizontal velocity:', v_horizontal, 'm/s');
    
    var ke_at_peak = kineticEnergy(mass, v_horizontal);
    print('  KE at peak:', ke_at_peak, 'J');
}

func main() {
    print('╔════════════════════════════════════════╗');
    print('║   TRAJECTORY ANALYSIS SYSTEM          ║');
    print('║   Advanced Projectile Motion Study    ║');
    print('╚════════════════════════════════════════╝');
    print('');
    
    compareAngles();
    print('');
    
    calculateOptimalAngle();
    print('');
    
    heightAdvantage();
    print('');
    
    realWorldExamples();
    print('');
    
    energyAnalysis();
    print('');
    
    print('╔════════════════════════════════════════╗');
    print('║         ANALYSIS COMPLETE!            ║');
    print('║                                        ║');
    print('║  Multiple trajectories plotted        ║');
    print('║  View in Trajectory Plotter tab       ║');
    print('╚════════════════════════════════════════╝');
}

main();
