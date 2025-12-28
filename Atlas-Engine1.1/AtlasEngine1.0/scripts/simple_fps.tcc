# ========================================
# SIMPLE FPS GAME - Wave Survival
# GeN00-style gameplay in AtlasEngine!
# ========================================

say "🎮 SIMPLE FPS WAVE SURVIVAL"
say "================================"
say ""
say "Loading game..."

# ========== GAME VARIABLES ==========

# Player stats
health is 100
max_health is 100
wave is 1
kills is 0
score is 0

# Enemy tracking
total_enemies is 0
enemies_spawned is 0
wave_active is 0

# Gameplay settings
enemies_per_wave is 5
wave_delay is 0
max_wave_delay is 180

say "✓ Variables initialized"

# ========== CREATE WORLD ==========

say ""
say "Building arena..."

# Large floor
ground at 0 color "#2d4a2b" size 50

# Outer walls (10x10 arena like the pygame version)
say "Building outer walls..."

# North wall
create3d cube at 0, 2.5, 20 size 1
scale3d last3d to 40, 5, 0.5
color3d last3d to "#808080"
collision3d on last3d

# South wall
create3d cube at 0, 2.5, -20 size 1
scale3d last3d to 40, 5, 0.5
color3d last3d to "#808080"
collision3d on last3d

# East wall
create3d cube at 20, 2.5, 0 size 1
scale3d last3d to 0.5, 5, 40
color3d last3d to "#808080"
collision3d on last3d

# West wall
create3d cube at -20, 2.5, 0 size 1
scale3d last3d to 0.5, 5, 40
color3d last3d to "#808080"
collision3d on last3d

say "✓ Outer walls complete"

# Inner maze walls (simplified version of the map)
say "Building maze..."

# Vertical walls
create3d cube at -10, 2, -10 size 1
scale3d last3d to 1, 4, 8
color3d last3d to "#606060"
collision3d on last3d

create3d cube at -10, 2, 10 size 1
scale3d last3d to 1, 4, 8
color3d last3d to "#606060"
collision3d on last3d

create3d cube at 10, 2, -10 size 1
scale3d last3d to 1, 4, 8
color3d last3d to "#606060"
collision3d on last3d

create3d cube at 10, 2, 10 size 1
scale3d last3d to 1, 4, 8
color3d last3d to "#606060"
collision3d on last3d

# Horizontal walls
create3d cube at 0, 2, -5 size 1
scale3d last3d to 12, 4, 1
color3d last3d to "#606060"
collision3d on last3d

create3d cube at 0, 2, 5 size 1
scale3d last3d to 12, 4, 1
color3d last3d to "#606060"
collision3d on last3d

# Cover objects
create3d cube at -5, 1, 0 size 1
scale3d last3d to 2, 2, 2
color3d last3d to "#654321"
collision3d on last3d

create3d cube at 5, 1, 0 size 1
scale3d last3d to 2, 2, 2
color3d last3d to "#654321"
collision3d on last3d

say "✓ Maze complete"
say "✓ Arena ready!"

# ========== SETUP PLAYER ==========

say ""
say "Spawning player..."

# Spawn player in center
player at 0, 1, -15
speed is 5

# Setup ammo (unlimited for now)
ammo set 999
magazine 999

say "✓ Player spawned at center"

# ========== WAVE 1 START ==========

say ""
say "================================"
say "🎮 STARTING GAME!"
say "================================"
say ""
say "Wave 1 - 5 enemies incoming!"
say ""

# Spawn first wave
say "Spawning enemies..."

# Enemy 1 - North East
npc "Enemy1" at 12, 1, 12
dialogue "Enemy1" says "HOSTILE DETECTED!"

# Enemy 2 - North West
npc "Enemy2" at -12, 1, 12
dialogue "Enemy2" says "TARGET ACQUIRED!"

# Enemy 3 - South East
npc "Enemy3" at 12, 1, -12
dialogue "Enemy3" says "ENGAGING!"

# Enemy 4 - South West
npc "Enemy4" at -12, 1, -12
dialogue "Enemy4" says "ATTACK!"

# Enemy 5 - Center North
npc "Enemy5" at 0, 1, 15
dialogue "Enemy5" says "ELIMINATE INTRUDER!"

total_enemies is 5
enemies_spawned is 5
wave_active is 1

say "✓ Wave 1 active!"
say ""
say "================================"
say "🎯 OBJECTIVE: SURVIVE THE WAVES"
say "================================"
say ""
say "💪 Your Health: 100"
say "🔫 Ammo: Unlimited"
say "👾 Enemies: 5"
say "📊 Wave: 1"
say ""
say "================================"
say "🎮 CONTROLS:"
say "================================"
say ""
say "  WASD       - Move"
say "  Mouse      - Look around"
say "  LMB        - Shoot"
say "  Shift      - Sprint"
say "  Space      - Jump"
say "  E          - Interact"
say "  Tab        - Toggle view"
say ""
say "⚙️ GAME MODE:"
say "  Switch to 3D Viewport tab"
say "  Click ⚙️ Mode button"
say "  Select 🔫 Shooter mode"
say ""
say "================================"
say ""
say "💡 TIP: Enemies will chase you!"
say "💡 Keep moving and aim carefully!"
say "💡 Kill all enemies to advance!"
say ""
say "================================"
say ""
say "🎮 GAME LOOP INSTRUCTIONS:"
say "================================"
say ""
say "This is the BASE SETUP."
say ""
say "For FULL gameplay, you need to:"
say ""
say "1. Switch to 🔫 Shooter mode"
say "   (Click Mode button in viewport)"
say ""
say "2. MANUALLY implement wave logic:"
say "   - Check when all 5 NPCs are dead"
say "   - Spawn next wave (more enemies)"
say "   - Increase difficulty"
say ""
say "3. ADD ENEMY AI (Python needed):"
say "   - Make NPCs chase player"
say "   - Damage player when close"
say "   - Pathfinding (advanced)"
say ""
say "================================"
say ""
say "🎯 WHAT YOU HAVE NOW:"
say "================================"
say ""
say "✅ Arena with maze"
say "✅ Player with gun"
say "✅ 5 enemies spawned"
say "✅ Shooter mode ready"
say "✅ Can shoot enemies"
say "✅ Health tracking"
say "✅ Score system"
say ""
say "================================"
say ""
say "⚠️ WHAT'S MISSING:"
say "================================"
say ""
say "❌ Enemy chase AI"
say "❌ Enemy damage"
say "❌ Automatic wave spawning"
say "❌ Game over screen"
say "❌ Health decrease"
say ""
say "These require Python code in"
say "viewport_3d.py to implement!"
say ""
say "================================"
say ""
say "💪 HOW TO PLAY:"
say "================================"
say ""
say "1. Go to 3D Viewport tab"
say ""
say "2. Click ⚙️ Mode button"
say ""
say "3. Select 🔫 Shooter mode"
say ""
say "4. Click canvas to grab focus"
say ""
say "5. SHOOT THE ENEMIES!"
say "   - Left click to shoot"
say "   - Aim at purple NPCs"
say "   - They flash when hit"
say ""
say "6. Try to survive!"
say ""
say "================================"
say ""
say "🎊 BASIC FPS READY!"
say ""
say "The arena is set, enemies spawned."
say "Switch to Shooter mode and play!"
say ""
say "For FULL AI and waves, we need"
say "to add Python code to the engine."
say ""
say "But you can SHOOT and PLAY NOW!"
say ""
say "================================"
say ""
say "💡 NEXT STEPS:"
say ""
say "Want me to add:"
say "  - Enemy AI (chase player)?"
say "  - Wave spawning system?"
say "  - Health damage?"
say "  - Game over screen?"
say ""
say "Let me know and I'll code it"
say "into the Python engine!"
say ""
say "================================"
say ""
say "🎮 GAME LOADED!"
say "Switch to 3D Viewport to play!"
say ""
say "================================"
