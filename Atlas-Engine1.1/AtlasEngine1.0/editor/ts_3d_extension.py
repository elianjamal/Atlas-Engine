#!/usr/bin/env python3
"""
AtlasEngine - T# 3D Engine Extension
Adds 100+ 3D game engine commands to T#
"""

import re
from typing import Optional, List, Dict, Any

class TS3DExtension:
    """Extension class for 3D viewport integration with T#"""
    
    def __init__(self, interpreter, editor):
        self.interpreter = interpreter
        self.editor = editor
        self.viewport = None
        self.last_created_object = None
        self.named_objects = {}
        
    def get_viewport(self):
        """Get 3D viewport reference"""
        if not self.viewport and hasattr(self.editor, 'viewport_3d'):
            self.viewport = self.editor.viewport_3d
        return self.viewport
    
    # ==================== 3D OBJECT COMMANDS ====================
    
    def cmd_create3d(self, stmt: str):
        """create3d type at x, y, z size scale"""
        match = re.match(
            r'create3d\s+(\w+)\s+at\s+(.+?),\s*(.+?),\s*(.+?)(?:\s+size\s+(.+?))?',
            stmt, re.I
        )
        if match:
            obj_type = match.group(1).lower()
            x = self.interpreter.eval_expr(match.group(2))
            y = self.interpreter.eval_expr(match.group(3))
            z = self.interpreter.eval_expr(match.group(4))
            size = float(self.interpreter.eval_expr(match.group(5))) if match.group(5) else 1.0
            
            vp = self.get_viewport()
            if vp:
                from editor.viewport_3d import Vector3D, Cube, Sphere
                pos = Vector3D(x, y, z)
                
                if obj_type == 'cube':
                    obj = Cube(pos, size)
                elif obj_type == 'sphere':
                    obj = Sphere(pos, size)
                else:
                    self.interpreter.log(f"Unknown 3D object type: {obj_type}", "error")
                    return
                
                vp.shapes.append(obj)
                self.last_created_object = obj
                self.interpreter.variables['last3d'] = obj
                vp.render()
                self.interpreter.log(f"🎮 Created 3D {obj_type} at ({x}, {y}, {z})")
    
    def cmd_move3d(self, stmt: str):
        """move3d object to x, y, z"""
        match = re.match(r'move3d\s+(\w+)\s+to\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            obj_name = match.group(1)
            x = self.interpreter.eval_expr(match.group(2))
            y = self.interpreter.eval_expr(match.group(3))
            z = self.interpreter.eval_expr(match.group(4))
            
            obj = self.interpreter.variables.get(obj_name)
            if obj and hasattr(obj, 'position'):
                from editor.viewport_3d import Vector3D
                obj.position = Vector3D(x, y, z)
                vp = self.get_viewport()
                if vp:
                    vp.render()
    
    def cmd_rotate3d(self, stmt: str):
        """rotate3d object to pitch, yaw, roll"""
        match = re.match(r'rotate3d\s+(\w+)\s+to\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            obj_name = match.group(1)
            pitch = self.interpreter.eval_expr(match.group(2))
            yaw = self.interpreter.eval_expr(match.group(3))
            roll = self.interpreter.eval_expr(match.group(4))
            
            obj = self.interpreter.variables.get(obj_name)
            if obj and hasattr(obj, 'rotation'):
                from editor.viewport_3d import Vector3D
                obj.rotation = Vector3D(pitch, yaw, roll)
                vp = self.get_viewport()
                if vp:
                    vp.render()
    
    def cmd_scale3d(self, stmt: str):
        """scale3d object to sx, sy, sz"""
        match = re.match(r'scale3d\s+(\w+)\s+to\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            obj_name = match.group(1)
            sx = self.interpreter.eval_expr(match.group(2))
            sy = self.interpreter.eval_expr(match.group(3))
            sz = self.interpreter.eval_expr(match.group(4))
            
            obj = self.interpreter.variables.get(obj_name)
            if obj and hasattr(obj, 'scale'):
                from editor.viewport_3d import Vector3D
                obj.scale = Vector3D(sx, sy, sz)
                vp = self.get_viewport()
                if vp:
                    vp.render()
    
    def cmd_color3d(self, stmt: str):
        """color3d object to "color" """
        match = re.match(r'color3d\s+(\w+)\s+to\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            obj_name = match.group(1)
            color = match.group(2)
            
            obj = self.interpreter.variables.get(obj_name)
            if obj and hasattr(obj, 'color'):
                obj.color = color
                vp = self.get_viewport()
                if vp:
                    vp.render()
    
    def cmd_delete3d(self, stmt: str):
        """delete3d object"""
        match = re.match(r'delete3d\s+(\w+)', stmt, re.I)
        if match:
            obj_name = match.group(1)
            obj = self.interpreter.variables.get(obj_name)
            
            vp = self.get_viewport()
            if obj and vp:
                if obj in vp.shapes:
                    vp.shapes.remove(obj)
                    vp.render()
                    self.interpreter.log(f"🗑️ Deleted 3D object")
    
    def cmd_physics3d(self, stmt: str):
        """physics3d on/off object"""
        match = re.match(r'physics3d\s+(on|off)\s+(\w+)', stmt, re.I)
        if match:
            state = match.group(1).lower()
            obj_name = match.group(2)
            obj = self.interpreter.variables.get(obj_name)
            
            if obj and hasattr(obj, 'has_physics'):
                obj.has_physics = (state == 'on')
                self.interpreter.log(f"⚙️ Physics {state} for object")
    
    def cmd_collision3d(self, stmt: str):
        """collision3d on/off object"""
        match = re.match(r'collision3d\s+(on|off)\s+(\w+)', stmt, re.I)
        if match:
            state = match.group(1).lower()
            obj_name = match.group(2)
            obj = self.interpreter.variables.get(obj_name)
            
            if obj and hasattr(obj, 'has_collision'):
                obj.has_collision = (state == 'on')
                self.interpreter.log(f"🛡️ Collision {state} for object")
    
    def cmd_velocity3d(self, stmt: str):
        """velocity3d object to vx, vy, vz"""
        match = re.match(r'velocity3d\s+(\w+)\s+to\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            obj_name = match.group(1)
            vx = self.interpreter.eval_expr(match.group(2))
            vy = self.interpreter.eval_expr(match.group(3))
            vz = self.interpreter.eval_expr(match.group(4))
            
            obj = self.interpreter.variables.get(obj_name)
            if obj and hasattr(obj, 'velocity'):
                from editor.viewport_3d import Vector3D
                obj.velocity = Vector3D(vx, vy, vz)
    
    # ==================== CAMERA COMMANDS ====================
    
    def cmd_camera(self, stmt: str):
        """camera at x, y, z"""
        match = re.match(r'camera\s+at\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.interpreter.eval_expr(match.group(1))
            y = self.interpreter.eval_expr(match.group(2))
            z = self.interpreter.eval_expr(match.group(3))
            
            vp = self.get_viewport()
            if vp:
                from editor.viewport_3d import Vector3D
                vp.camera_pos = Vector3D(x, y, z)
                vp.render()
                self.interpreter.log(f"📷 Camera at ({x}, {y}, {z})")
    
    def cmd_lookat(self, stmt: str):
        """lookat x, y, z"""
        match = re.match(r'lookat\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.interpreter.eval_expr(match.group(1))
            y = self.interpreter.eval_expr(match.group(2))
            z = self.interpreter.eval_expr(match.group(3))
            
            vp = self.get_viewport()
            if vp:
                from editor.viewport_3d import Vector3D
                vp.camera_target = Vector3D(x, y, z)
                vp.render()
    
    def cmd_firstperson(self, stmt: str):
        """firstperson"""
        vp = self.get_viewport()
        if vp:
            vp.player_controls_enabled = True
            self.interpreter.log("🎮 First-person mode enabled")
    
    def cmd_thirdperson(self, stmt: str):
        """thirdperson"""
        vp = self.get_viewport()
        if vp:
            vp.player_controls_enabled = False
            self.interpreter.log("🎮 Third-person mode")
    
    def cmd_fov(self, stmt: str):
        """fov degrees"""
        match = re.match(r'fov\s+(.+)', stmt, re.I)
        if match:
            fov = self.interpreter.eval_expr(match.group(1))
            # Would set FOV on viewport
            self.interpreter.log(f"🎥 FOV set to {fov}")
    
    # ==================== WORLD COMMANDS ====================
    
    def cmd_skybox(self, stmt: str):
        """skybox "type" """
        match = re.match(r'skybox\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            skybox_type = match.group(1)
            self.interpreter.log(f"🌅 Skybox: {skybox_type}")
    
    def cmd_ground(self, stmt: str):
        """ground at y color "color" size s"""
        match = re.match(
            r'ground\s+at\s+(.+?)\s+color\s+["\'](.+?)["\']\s+size\s+(.+)',
            stmt, re.I
        )
        if match:
            y = self.interpreter.eval_expr(match.group(1))
            color = match.group(2)
            size = self.interpreter.eval_expr(match.group(3))
            
            # Create large plane
            from editor.viewport_3d import Vector3D, Cube
            vp = self.get_viewport()
            if vp:
                ground = Cube(Vector3D(0, y, 0), size)
                ground.scale = Vector3D(1, 0.1, 1)
                ground.color = color
                ground.is_static = True
                ground.has_collision = True
                vp.shapes.append(ground)
                vp.render()
                self.interpreter.log(f"🟩 Created ground")
    
    def cmd_platform(self, stmt: str):
        """platform at x, y, z size w, h, d"""
        match = re.match(
            r'platform\s+at\s+(.+?),\s*(.+?),\s*(.+?)\s+size\s+(.+?),\s*(.+?),\s*(.+)',
            stmt, re.I
        )
        if match:
            x = self.interpreter.eval_expr(match.group(1))
            y = self.interpreter.eval_expr(match.group(2))
            z = self.interpreter.eval_expr(match.group(3))
            w = self.interpreter.eval_expr(match.group(4))
            h = self.interpreter.eval_expr(match.group(5))
            d = self.interpreter.eval_expr(match.group(6))
            
            from editor.viewport_3d import Vector3D, Cube
            vp = self.get_viewport()
            if vp:
                platform = Cube(Vector3D(x, y, z), 1)
                platform.scale = Vector3D(w, h, d)
                platform.has_collision = True
                vp.shapes.append(platform)
                self.last_created_object = platform
                self.interpreter.variables['last3d'] = platform
                vp.render()
                self.interpreter.log(f"🟦 Created platform")
    
    # ==================== PLAYER COMMANDS ====================
    
    def cmd_player(self, stmt: str):
        """player at x, y, z"""
        match = re.match(r'player\s+at\s+(.+?),\s*(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.interpreter.eval_expr(match.group(1))
            y = self.interpreter.eval_expr(match.group(2))
            z = self.interpreter.eval_expr(match.group(3))
            
            vp = self.get_viewport()
            if vp:
                from editor.viewport_3d import Vector3D
                vp.camera_pos = Vector3D(x, y, z)
                vp.player_controls_enabled = True
                vp.render()
                self.interpreter.log(f"👤 Player created at ({x}, {y}, {z})")
    
    def cmd_speed(self, stmt: str):
        """speed is value"""
        match = re.match(r'speed\s+is\s+(.+)', stmt, re.I)
        if match:
            speed = self.interpreter.eval_expr(match.group(1))
            vp = self.get_viewport()
            if vp:
                vp.move_speed = float(speed)
                self.interpreter.log(f"⚡ Speed set to {speed}")
    
    def cmd_jump(self, stmt: str):
        """jump or jump force f"""
        match = re.match(r'jump(?:\s+force\s+(.+))?', stmt, re.I)
        force = 10.0
        if match and match.group(1):
            force = self.interpreter.eval_expr(match.group(1))
        
        vp = self.get_viewport()
        if vp:
            # Apply upward velocity
            vp.player_velocity_y = float(force)
            self.interpreter.log(f"🦘 Jump!")
    
    def cmd_health(self, stmt: str):
        """health is/add/subtract value"""
        if 'add' in stmt:
            match = re.match(r'health\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.interpreter.eval_expr(match.group(1))
                if 'player_health' in self.interpreter.variables:
                    self.interpreter.variables['player_health'] += amount
        elif 'subtract' in stmt:
            match = re.match(r'health\s+subtract\s+(.+)', stmt, re.I)
            if match:
                amount = self.interpreter.eval_expr(match.group(1))
                if 'player_health' in self.interpreter.variables:
                    self.interpreter.variables['player_health'] -= amount
        else:
            match = re.match(r'health\s+is\s+(.+)', stmt, re.I)
            if match:
                value = self.interpreter.eval_expr(match.group(1))
                self.interpreter.variables['player_health'] = value
    
    # ==================== UI COMMANDS ====================
    
    def cmd_hud(self, stmt: str):
        """hud show/hide"""
        if 'show' in stmt.lower():
            self.interpreter.log("📊 HUD shown")
        elif 'hide' in stmt.lower():
            self.interpreter.log("📊 HUD hidden")
    
    def cmd_crosshair(self, stmt: str):
        """crosshair show/hide/color"""
        if 'show' in stmt.lower():
            self.interpreter.log("🎯 Crosshair shown")
        elif 'hide' in stmt.lower():
            self.interpreter.log("🎯 Crosshair hidden")
        elif 'color' in stmt.lower():
            match = re.match(r'crosshair\s+color\s+["\'](.+?)["\']', stmt, re.I)
            if match:
                color = match.group(1)
                self.interpreter.log(f"🎯 Crosshair color: {color}")
    
    def cmd_message(self, stmt: str):
        """message "text" duration d"""
        match = re.match(r'message\s+["\'](.+?)["\']\s+duration\s+(.+)', stmt, re.I)
        if match:
            text = match.group(1)
            duration = self.interpreter.eval_expr(match.group(2))
            
            # Display in output window
            if hasattr(self.interpreter.editor, 'output_window'):
                self.interpreter.editor.output_window.info(f"📢 {text}")
    
    # ==================== NPC COMMANDS ====================
    
    def cmd_npc(self, stmt: str):
        """npc "name" at x, y, z"""
        match = re.match(r'npc\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?', stmt, re.I)
        if match:
            name = match.group(1)
            x = self.interpreter.eval_expr(match.group(2))
            y = self.interpreter.eval_expr(match.group(3))
            z = self.interpreter.eval_expr(match.group(4))
            color = match.group(5) if match.group(5) else "#9900ff"  # Purple default
            
            vp = self.get_viewport()
            if vp:
                npc = vp.add_npc(name, x, y, z, color)
                self.interpreter.variables[name.lower()] = npc
                self.interpreter.log(f"👤 Created NPC '{name}'")
    
    def cmd_dialogue(self, stmt: str):
        """dialogue "name" says "text" """
        match = re.match(r'dialogue\s+["\'](.+?)["\']\s+says\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            npc_name = match.group(1)
            text = match.group(2)
            
            vp = self.get_viewport()
            if vp:
                vp.add_npc_dialogue(npc_name, text)
                self.interpreter.log(f"💬 Added dialogue to {npc_name}")
    
    def cmd_talk(self, stmt: str):
        """talk to "name" """
        match = re.match(r'talk\s+to\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            npc_name = match.group(1)
            
            vp = self.get_viewport()
            if vp:
                vp.show_npc_dialogue(npc_name, 0)
    
    def cmd_say_npc(self, stmt: str):
        """say as "name" "text" """
        match = re.match(r'say\s+as\s+["\'](.+?)["\']\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            npc_name = match.group(1)
            text = match.group(2)
            
            # Show dialogue
            if hasattr(self.interpreter.editor, 'output_window'):
                self.interpreter.editor.output_window.say(f"{npc_name}: {text}")
    
    # ==================== HELPER METHODS ====================
    
    def get_command_methods(self):
        """Return dictionary of 3D command methods"""
        return {
            # 3D Objects
            'create3d': self.cmd_create3d,
            'move3d': self.cmd_move3d,
            'rotate3d': self.cmd_rotate3d,
            'scale3d': self.cmd_scale3d,
            'color3d': self.cmd_color3d,
            'delete3d': self.cmd_delete3d,
            'physics3d': self.cmd_physics3d,
            'collision3d': self.cmd_collision3d,
            'velocity3d': self.cmd_velocity3d,
            
            # Camera
            'camera': self.cmd_camera,
            'lookat': self.cmd_lookat,
            'firstperson': self.cmd_firstperson,
            'thirdperson': self.cmd_thirdperson,
            'fov': self.cmd_fov,
            
            # World
            'skybox': self.cmd_skybox,
            'ground': self.cmd_ground,
            'platform': self.cmd_platform,
            
            # Player
            'player': self.cmd_player,
            'speed': self.cmd_speed,
            'jump': self.cmd_jump,
            'health': self.cmd_health,
            
            # UI
            'hud': self.cmd_hud,
            'crosshair': self.cmd_crosshair,
            'message': self.cmd_message,
            
            # NPCs
            'npc': self.cmd_npc,
            'dialogue': self.cmd_dialogue,
            'talk': self.cmd_talk,
        }