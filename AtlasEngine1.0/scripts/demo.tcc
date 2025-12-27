// T# Script Example
// Game Object Management Demo

// Create a player character
func createPlayer() {
    var playerId = spawn('Player');
    move(playerId, 0, 0, 0);
    print('Player spawned at origin');
    return playerId;
}

// Create enemies in a circle
func createEnemies(count) {
    var i = 0;
    while (i < count) {
        var enemyId = spawn('Enemy');
        var angle = i * 6.28 / count;
        var x = 5 * cos(angle);
        var z = 5 * sin(angle);
        move(enemyId, x, 0, z);
        rotate(enemyId, 0, angle, 0);
        i = i + 1;
    }
    print('Spawned enemies in formation');
}

// Main game loop
func main() {
    print('======================');
    print('AtlasEngine Game Demo');
    print('======================');
    
    // Initialize game
    var player = createPlayer();
    createEnemies(8);
    
    print('Game initialized!');
    print('Total objects:', 9);
}

// Run the game
main();
