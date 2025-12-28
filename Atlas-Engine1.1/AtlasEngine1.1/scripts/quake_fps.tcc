# ========================================
# QUAKE-STYLE FPS SHOOTER
# Blue gun in center with raycast shooting!
# ========================================

say "🔫 QUAKE-STYLE FPS GAME"
say "================================"
say ""
say "Setting up world..."

# ========== WORLD SETUP ==========

# Ground
ground at 0 color "#2d4a2b" size 50

# Walls
create3d cube at 20, 2.5, 0 size 1
scale3d last3d to 0.5, 5, 50
color3d last3d to "#808080"
collision3d on last3d

create3d cube at -20, 2.5, 0 size 1
scale3d last3d to 0.5, 5, 50
color3d last3d to "#808080"
collision3d on last3d

create3d cube at 0, 2.5, 20 size 1
scale3d last3d to 50, 5, 0.5
color3d last3d to "#808080"
collision3d on last3d

create3d cube at 0, 2.5, -20 size 1
scale3d last3d to 50, 5, 0.5
color3d last3d to "#808080"
collision3d on last3d

say "✓ Arena created"

# ========== TARGETS/ENEMIES ==========

# Target 1 - Purple NPC cube
npc "Enemy1" at 10, 1, 5
dialogue "Enemy1" says "You'll never defeat me!"

# Target 2 - Purple NPC cube
npc "Enemy2" at -8, 1, 8
dialogue "Enemy2" says "Come get me!"

# Target 3 - Purple NPC cube
npc "Enemy3" at 0, 1, 15
dialogue "Enemy3" says "I'm waiting..."

# Regular cubes as targets
create3d cube at 5, 1, -5 size 2
color3d last3d to "#ff0000"
collision3d on last3d

create3d cube at -10, 1, -8 size 2
color3d last3d to "#ff4400"
collision3d on last3d

say "✓ 5 targets spawned"
say "  • 3 Purple NPC cubes"
say "  • 2 Red target cubes"

# ========== OBSTACLES ==========

# Cover objects
create3d cube at 3, 1, 3 size 1.5
scale3d last3d to 2, 2, 0.5
color3d last3d to "#654321"
collision3d on last3d

create3d cube at -5, 1, -2 size 1.5
scale3d last3d to 0.5, 2, 2
color3d last3d to "#654321"
collision3d on last3d

say "✓ Cover objects placed"

# ========== PLAYER SETUP ==========

say ""
say "Spawning player..."

# Create player at spawn point
player at 0, 1, -10
speed is 5

# Player stats
health is 100
armor 25

# Weapon is auto-equipped (blue gun)
ammo set 30
magazine 30

say "✓ Player spawned"
say "  Position: (0, 1, -10)"
say "  Health: 100"
say "  Armor: 25"
say "  Ammo: 30/30"

# ========== INSTRUCTIONS ==========

say ""
say "================================"
say "🎮 CONTROLS:"
say "================================"
say "  WASD - Move"
say "  Mouse - Look around"
say "  LEFT CLICK - SHOOT!"
say "  Space - Jump"
say "  E - Talk to NPCs"
say ""
say "🎯 OBJECTIVE:"
say "  Shoot all targets!"
say "  Hit NPCs and cubes"
say ""
say "🔫 WEAPON:"
say "  Blue gun appears in center"
say "  Raycast laser beam"
say "  Green laser on hit"
say "  Targets flash when hit"
say ""
say "================================"

say ""
say "✓ GAME READY!"
say ""
say "Switch to 3D Viewport tab"
say "Click canvas to grab mouse"
say "LEFT CLICK TO SHOOT!"
say ""
say "The blue gun will appear at"
say "the bottom center of screen!"
say ""
say "================================"
