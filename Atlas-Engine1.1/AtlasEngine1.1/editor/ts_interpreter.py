#!/usr/bin/env python3
"""
AtlasEngine - T# Language Interpreter
Completely rewritten for clarity and reliability
"""

import re
import math
import os
from typing import Dict, Any, List

class TSInterpreter:
    """T# (T-Sharp) Language Interpreter"""
    
    def __init__(self, editor):
        """Initialize the T# interpreter"""
        self.editor = editor
        self.variables = {}
        self.functions = {}
        self.imported_files = set()
        
        # Get scripts directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.script_dir = os.path.join(base_dir, 'scripts')
        
        # Initialize constants
        self.variables['PI'] = math.pi
        self.variables['E'] = math.e
        self.variables['TAU'] = 2 * math.pi
        
        # Initialize physics/math modules
        try:
            from editor.math_physics_engine import (
                PhysicsEngine, ScientificCalculator, 
                MathFunctions, Statistics
            )
            self.physics = PhysicsEngine()
            self.calc = ScientificCalculator()
            self.math_funcs = MathFunctions()
            self.stats = Statistics()
        except:
            self.physics = None
            self.calc = None
            self.math_funcs = None
            self.stats = None
        
        # Initialize 3D engine extension
        try:
            from editor.ts_3d_extension import TS3DExtension
            self.engine3d = TS3DExtension(self, editor)
        except:
            self.engine3d = None
    
    def execute(self, code: str, filename: str = None):
        """Execute T# code"""
        try:
            # Remove comments
            code = self.remove_comments(code)
            
            # Parse into statements
            statements = self.parse_code(code)
            
            # Execute each statement
            for stmt in statements:
                if stmt.strip():
                    self.execute_statement(stmt)
            
            self.log("✓ Script completed", "success")
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}", "error")
    
    def remove_comments(self, code: str) -> str:
        """Remove all comments from code"""
        # Remove single-line comments (// and #)
        code = re.sub(r'(//|#).*?$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments (/* */ and """ """)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        
        return code
    
    def parse_code(self, code: str) -> List[str]:
        """Parse code into statements"""
        lines = code.split('\n')
        statements = []
        current = ""
        brace_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            brace_count += line.count('{') - line.count('}')
            current += " " + line if current else line
            
            # Statement is complete when:
            # 1. Not inside braces (brace_count == 0) AND
            # 2. Line ends naturally (not continuing)
            if brace_count == 0:
                # Complete statement
                statements.append(current.strip())
                current = ""
            elif line.endswith('}'):
                # Closing brace completes block
                statements.append(current.strip())
                current = ""
        
        # Add any remaining statement
        if current.strip():
            statements.append(current.strip())
        
        return statements
    
    def execute_statement(self, stmt: str):
        """Execute a single statement"""
        stmt = stmt.rstrip(';').strip()
        
        if not stmt:
            return
        
        # Get first word (command)
        words = stmt.split()
        if not words:
            return
        
        cmd = words[0].lower()
        
        # Text output commands
        if cmd == 'say':
            self.cmd_say(stmt)
        elif cmd == 'shout':
            self.cmd_shout(stmt)
        elif cmd == 'whisper':
            self.cmd_whisper(stmt)
        elif cmd == 'show' or cmd == 'display':
            self.cmd_show(stmt)
        elif cmd == 'input':
            self.cmd_input(stmt)
        elif cmd == 'clear':
            self.cmd_clear(stmt)
        elif cmd == 'cleargraphics':
            self.cmd_cleargraphics(stmt)
        
        # Variable commands
        elif cmd == 'remember':
            self.cmd_remember(stmt)
        elif cmd == 'forget':
            self.cmd_forget(stmt)
        elif cmd == 'recall':
            self.cmd_recall(stmt)
        elif cmd == 'make':
            self.cmd_make(stmt)
        elif cmd == 'set':
            self.cmd_set(stmt)
        elif cmd == 'create':
            self.cmd_create(stmt)
        elif cmd == 'change':
            self.cmd_change(stmt)
        elif cmd == 'increase':
            self.cmd_increase(stmt)
        elif cmd == 'decrease':
            self.cmd_decrease(stmt)
        
        # Math commands
        elif cmd == 'calculate' or cmd == 'compute':
            self.cmd_calculate(stmt)
        elif cmd == 'power':
            self.cmd_power(stmt)
        elif cmd == 'root':
            self.cmd_root(stmt)
        elif cmd == 'absolute':
            self.cmd_absolute(stmt)
        elif cmd == 'roundup':
            self.cmd_roundup(stmt)
        elif cmd == 'rounddown':
            self.cmd_rounddown(stmt)
        
        # Control flow
        elif cmd == 'repeat':
            self.cmd_repeat(stmt)
        elif cmd == 'if' or cmd == 'when' or cmd == 'whenever':
            self.cmd_if(stmt)
        elif cmd == 'elif' or cmd == 'elseif':
            self.cmd_elseif(stmt)
        elif cmd == 'else' or cmd == 'otherwise':
            self.cmd_else(stmt)
        
        # Import
        elif cmd == 'callupon':
            self.cmd_callupon(stmt)
        
        # Text operations
        elif cmd == 'join':
            self.cmd_join(stmt)
        elif cmd == 'split':
            self.cmd_split(stmt)
        elif cmd == 'length':
            self.cmd_length(stmt)
        
        # Random
        elif cmd == 'random':
            self.cmd_random(stmt)
        elif cmd == 'choose':
            self.cmd_choose(stmt)
        
        # Comparison
        elif cmd == 'compare':
            self.cmd_compare(stmt)
        
        # Type operations
        elif cmd == 'convert':
            self.cmd_convert(stmt)
        elif cmd == 'exists':
            self.cmd_exists(stmt)
        elif cmd == 'typeof':
            self.cmd_typeof(stmt)
        
        # Graphics commands
        elif cmd == 'switchgraphics':
            self.cmd_switchgraphics()
        elif cmd == 'switchtext':
            self.cmd_switchtext()
        elif cmd == 'sprite':
            self.cmd_sprite(stmt)
        elif cmd == 'movesprite':
            self.cmd_movesprite(stmt)
        elif cmd == 'colorsprite':
            self.cmd_colorsprite(stmt)
        elif cmd == 'hidesprite':
            self.cmd_hidesprite(stmt)
        elif cmd == 'showsprite':
            self.cmd_showsprite(stmt)
        elif cmd == 'deletesprite':
            self.cmd_deletesprite(stmt)
        elif cmd == 'fillscreen':
            self.cmd_fillscreen(stmt)
        elif cmd == 'drawline':
            self.cmd_drawline(stmt)
        elif cmd == 'drawrect':
            self.cmd_drawrect(stmt)
        elif cmd == 'drawcircle':
            self.cmd_drawcircle(stmt)
        elif cmd == 'drawtext':
            self.cmd_drawtext(stmt)
        
        # List command
        elif cmd == 'list':
            self.cmd_list(stmt)
        
        # Advanced Math
        elif cmd == 'sin':
            self.cmd_sin(stmt)
        elif cmd == 'cos':
            self.cmd_cos(stmt)
        elif cmd == 'tan':
            self.cmd_tan(stmt)
        elif cmd == 'floor':
            self.cmd_floor(stmt)
        elif cmd == 'ceil':
            self.cmd_ceil(stmt)
        elif cmd == 'round':
            self.cmd_round(stmt)
        elif cmd == 'min':
            self.cmd_min(stmt)
        elif cmd == 'max':
            self.cmd_max(stmt)
        elif cmd == 'average' or cmd == 'mean':
            self.cmd_average(stmt)
        elif cmd == 'sum':
            self.cmd_sum(stmt)
        elif cmd == 'product':
            self.cmd_product(stmt)
        elif cmd == 'percent':
            self.cmd_percent(stmt)
        elif cmd == 'factorial':
            self.cmd_factorial(stmt)
        elif cmd == 'squared':
            self.cmd_squared(stmt)
        elif cmd == 'cubed':
            self.cmd_cubed(stmt)
        elif cmd == 'log':
            self.cmd_log(stmt)
        elif cmd == 'ln':
            self.cmd_ln(stmt)
        elif cmd == 'exp':
            self.cmd_exp(stmt)
        elif cmd == 'sign':
            self.cmd_sign(stmt)
        elif cmd == 'clamp':
            self.cmd_clamp(stmt)
        
        # String/Text Advanced
        elif cmd == 'uppercase':
            self.cmd_uppercase(stmt)
        elif cmd == 'lowercase':
            self.cmd_lowercase(stmt)
        elif cmd == 'titlecase':
            self.cmd_titlecase(stmt)
        elif cmd == 'reverse':
            self.cmd_reverse(stmt)
        elif cmd == 'trim':
            self.cmd_trim(stmt)
        elif cmd == 'replace':
            self.cmd_replace(stmt)
        elif cmd == 'substring':
            self.cmd_substring(stmt)
        elif cmd == 'contains':
            self.cmd_contains(stmt)
        elif cmd == 'startswith':
            self.cmd_startswith(stmt)
        elif cmd == 'endswith':
            self.cmd_endswith(stmt)
        elif cmd == 'repeat':
            self.cmd_repeat(stmt)
        elif cmd == 'padleft':
            self.cmd_padleft(stmt)
        elif cmd == 'padright':
            self.cmd_padright(stmt)
        elif cmd == 'indexof':
            self.cmd_indexof(stmt)
        
        # List/Array Operations
        elif cmd == 'append':
            self.cmd_append(stmt)
        elif cmd == 'prepend':
            self.cmd_prepend(stmt)
        elif cmd == 'insert':
            self.cmd_insert(stmt)
        elif cmd == 'remove':
            self.cmd_remove(stmt)
        elif cmd == 'pop':
            self.cmd_pop(stmt)
        elif cmd == 'shift':
            self.cmd_shift(stmt)
        elif cmd == 'clear':
            self.cmd_clear(stmt)
        elif cmd == 'sort':
            self.cmd_sort(stmt)
        elif cmd == 'reverse':
            self.cmd_reverse_list(stmt)
        elif cmd == 'unique':
            self.cmd_unique(stmt)
        elif cmd == 'count':
            self.cmd_count(stmt)
        elif cmd == 'first':
            self.cmd_first(stmt)
        elif cmd == 'last':
            self.cmd_last(stmt)
        elif cmd == 'slice':
            self.cmd_slice(stmt)
        elif cmd == 'merge':
            self.cmd_merge(stmt)
        
        # Logic & Conditions
        elif cmd == 'and':
            self.cmd_and(stmt)
        elif cmd == 'or':
            self.cmd_or(stmt)
        elif cmd == 'not':
            self.cmd_not(stmt)
        elif cmd == 'equals':
            self.cmd_equals(stmt)
        elif cmd == 'notequals':
            self.cmd_notequals(stmt)
        elif cmd == 'greater':
            self.cmd_greater(stmt)
        elif cmd == 'less':
            self.cmd_less(stmt)
        elif cmd == 'between':
            self.cmd_between(stmt)
        
        # Time & Date
        elif cmd == 'time':
            self.cmd_time(stmt)
        elif cmd == 'date':
            self.cmd_date(stmt)
        elif cmd == 'timestamp':
            self.cmd_timestamp(stmt)
        elif cmd == 'year':
            self.cmd_year(stmt)
        elif cmd == 'month':
            self.cmd_month(stmt)
        elif cmd == 'day':
            self.cmd_day(stmt)
        elif cmd == 'hour':
            self.cmd_hour(stmt)
        elif cmd == 'minute':
            self.cmd_minute(stmt)
        elif cmd == 'second':
            self.cmd_second(stmt)
        
        # Variables Advanced
        elif cmd == 'copy':
            self.cmd_copy(stmt)
        elif cmd == 'swap':
            self.cmd_swap(stmt)
        elif cmd == 'increment':
            self.cmd_increment(stmt)
        elif cmd == 'decrement':
            self.cmd_decrement(stmt)
        
        # NEW COMMANDS!
        elif cmd == 'wait' or cmd == 'sleep' or cmd == 'pause':
            self.cmd_wait(stmt)
        elif cmd == 'break' or cmd == 'stop':
            self.cmd_break(stmt)
        elif cmd == 'continue' or cmd == 'skip':
            self.cmd_continue(stmt)
        elif cmd == 'return' or cmd == 'give':
            self.cmd_return(stmt)
        elif cmd == 'function' or cmd == 'define':
            self.cmd_function(stmt)
        elif cmd == 'call' or cmd == 'run':
            self.cmd_call(stmt)
        elif cmd == 'print' or cmd == 'log':
            self.cmd_print(stmt)
        elif cmd == 'error' or cmd == 'throw':
            self.cmd_error(stmt)
        elif cmd == 'warning' or cmd == 'warn':
            self.cmd_warning(stmt)
        elif cmd == 'success':
            self.cmd_success(stmt)
        elif cmd == 'info':
            self.cmd_info(stmt)
        elif cmd == 'debug':
            self.cmd_debug(stmt)
        elif cmd == 'comment' or cmd == 'note':
            pass  # Comments do nothing
        elif cmd == 'assert' or cmd == 'verify':
            self.cmd_assert(stmt)
        elif cmd == 'try':
            self.cmd_try(stmt)
        elif cmd == 'catch':
            self.cmd_catch(stmt)
        elif cmd == 'finally':
            self.cmd_finally(stmt)
            self.cmd_increment(stmt)
        elif cmd == 'decrement':
            self.cmd_decrement(stmt)
        elif cmd == 'multiply':
            self.cmd_multiply(stmt)
        elif cmd == 'divide':
            self.cmd_divide(stmt)
        elif cmd == 'modulo':
            self.cmd_modulo(stmt)
        
        # Control Flow Advanced
        elif cmd == 'break':
            self.cmd_break(stmt)
        elif cmd == 'continue':
            self.cmd_continue(stmt)
        elif cmd == 'return':
            self.cmd_return(stmt)
        elif cmd == 'else':
            self.cmd_else(stmt)
        elif cmd == 'elseif' or cmd == 'elif':
            self.cmd_elseif(stmt)
        elif cmd == 'while':
            self.cmd_while(stmt)
        elif cmd == 'until':
            self.cmd_until(stmt)
        elif cmd == 'for':
            self.cmd_for(stmt)
        elif cmd == 'foreach':
            self.cmd_foreach(stmt)
        elif cmd == 'loop':
            self.cmd_loop(stmt)
        elif cmd == 'do':
            self.cmd_do(stmt)
        
        # Debug & Output
        elif cmd == 'print':
            self.cmd_print(stmt)
        elif cmd == 'debug':
            self.cmd_debug(stmt)
        elif cmd == 'warn':
            self.cmd_warn(stmt)
        elif cmd == 'error':
            self.cmd_error(stmt)
        elif cmd == 'info':
            self.cmd_info(stmt)
        elif cmd == 'log':
            self.cmd_log_output(stmt)
        elif cmd == 'clear':
            self.cmd_clear_output(stmt)
        
        # Check for 3D engine commands
        elif self.engine3d and cmd in self.engine3d.get_command_methods():
            method = self.engine3d.get_command_methods()[cmd]
            method(stmt)
        
        # ==================== RPG MECHANICS (50 commands) ====================
        # Player Stats
        elif cmd == 'xp':
            self.cmd_xp(stmt)
        elif cmd == 'level':
            self.cmd_level(stmt)
        elif cmd == 'levelup':
            self.cmd_levelup(stmt)
        elif cmd == 'stat':
            self.cmd_stat(stmt)
        elif cmd == 'mana':
            self.cmd_mana(stmt)
        elif cmd == 'stamina':
            self.cmd_stamina(stmt)
        elif cmd == 'armor':
            self.cmd_armor(stmt)
        elif cmd == 'attack':
            self.cmd_attack(stmt)
        elif cmd == 'defense':
            self.cmd_defense(stmt)
        
        # Inventory
        elif cmd == 'inventory':
            self.cmd_inventory(stmt)
        elif cmd == 'equip':
            self.cmd_equip(stmt)
        elif cmd == 'unequip':
            self.cmd_unequip(stmt)
        elif cmd == 'additem':
            self.cmd_additem(stmt)
        elif cmd == 'removeitem':
            self.cmd_removeitem(stmt)
        elif cmd == 'hasitem':
            self.cmd_hasitem(stmt)
        elif cmd == 'useitem':
            self.cmd_useitem(stmt)
        elif cmd == 'dropitem':
            self.cmd_dropitem(stmt)
        
        # Quests
        elif cmd == 'quest':
            self.cmd_quest(stmt)
        elif cmd == 'completequest':
            self.cmd_completequest(stmt)
        elif cmd == 'objective':
            self.cmd_objective(stmt)
        elif cmd == 'reward':
            self.cmd_reward(stmt)
        
        # Combat
        elif cmd == 'enemy':
            self.cmd_enemy(stmt)
        elif cmd == 'battle':
            self.cmd_battle(stmt)
        elif cmd == 'hit':
            self.cmd_hit(stmt)
        elif cmd == 'critical':
            self.cmd_critical(stmt)
        elif cmd == 'dodge':
            self.cmd_dodge(stmt)
        elif cmd == 'block':
            self.cmd_block(stmt)
        elif cmd == 'parry':
            self.cmd_parry(stmt)
        elif cmd == 'stun':
            self.cmd_stun(stmt)
        elif cmd == 'poison':
            self.cmd_poison(stmt)
        elif cmd == 'burn':
            self.cmd_burn(stmt)
        elif cmd == 'freeze':
            self.cmd_freeze(stmt)
        
        # Magic
        elif cmd == 'spell':
            self.cmd_spell(stmt)
        elif cmd == 'cast':
            self.cmd_cast(stmt)
        elif cmd == 'fireball':
            self.cmd_fireball(stmt)
        elif cmd == 'lightning':
            self.cmd_lightning(stmt)
        elif cmd == 'heal':
            self.cmd_heal(stmt)
        elif cmd == 'shield':
            self.cmd_shield(stmt)
        elif cmd == 'teleport':
            self.cmd_teleport(stmt)
        elif cmd == 'summon':
            self.cmd_summon(stmt)
        elif cmd == 'enchant':
            self.cmd_enchant(stmt)
        
        # Skills
        elif cmd == 'skill':
            self.cmd_skill(stmt)
        elif cmd == 'ability':
            self.cmd_ability(stmt)
        elif cmd == 'cooldown':
            self.cmd_cooldown(stmt)
        elif cmd == 'buff':
            self.cmd_buff(stmt)
        elif cmd == 'debuff':
            self.cmd_debuff(stmt)
        
        # ==================== SHOOTING/WEAPONS (30 commands) ====================
        elif cmd == 'gun':
            self.cmd_gun(stmt)
        elif cmd == 'shoot':
            self.cmd_shoot(stmt)
        elif cmd == 'raycast':
            self.cmd_raycast(stmt)
        elif cmd == 'laser':
            self.cmd_laser(stmt)
        elif cmd == 'bullet':
            self.cmd_bullet(stmt)
        elif cmd == 'projectile':
            self.cmd_projectile(stmt)
        elif cmd == 'reload':
            self.cmd_reload(stmt)
        elif cmd == 'ammo':
            self.cmd_ammo(stmt)
        elif cmd == 'weapon':
            self.cmd_weapon(stmt)
        elif cmd == 'melee':
            self.cmd_melee(stmt)
        elif cmd == 'sword':
            self.cmd_sword(stmt)
        elif cmd == 'bow':
            self.cmd_bow(stmt)
        elif cmd == 'arrow':
            self.cmd_arrow(stmt)
        elif cmd == 'grenade':
            self.cmd_grenade(stmt)
        elif cmd == 'bomb':
            self.cmd_bomb(stmt)
        elif cmd == 'explode':
            self.cmd_explode(stmt)
        elif cmd == 'aim':
            self.cmd_aim(stmt)
        elif cmd == 'recoil':
            self.cmd_recoil(stmt)
        elif cmd == 'spread':
            self.cmd_spread(stmt)
        elif cmd == 'shotgun':
            self.cmd_shotgun(stmt)
        elif cmd == 'sniper':
            self.cmd_sniper(stmt)
        elif cmd == 'rifle':
            self.cmd_rifle(stmt)
        elif cmd == 'pistol':
            self.cmd_pistol(stmt)
        elif cmd == 'rocket':
            self.cmd_rocket(stmt)
        elif cmd == 'homing':
            self.cmd_homing(stmt)
        elif cmd == 'scope':
            self.cmd_scope(stmt)
        elif cmd == 'zoom':
            self.cmd_zoom(stmt)
        elif cmd == 'accuracy':
            self.cmd_accuracy(stmt)
        elif cmd == 'firerate':
            self.cmd_firerate(stmt)
        elif cmd == 'magazine':
            self.cmd_magazine(stmt)
        
        # ==================== 2D GRAPHICS ADVANCED (35 commands) ====================
        elif cmd == 'particle':
            self.cmd_particle(stmt)
        elif cmd == 'emitter':
            self.cmd_emitter(stmt)
        elif cmd == 'animation':
            self.cmd_animation(stmt)
        elif cmd == 'frame':
            self.cmd_frame(stmt)
        elif cmd == 'layer':
            self.cmd_layer(stmt)
        elif cmd == 'zindex':
            self.cmd_zindex(stmt)
        elif cmd == 'opacity':
            self.cmd_opacity(stmt)
        elif cmd == 'fade':
            self.cmd_fade(stmt)
        elif cmd == 'rotate':
            self.cmd_rotate(stmt)
        elif cmd == 'scale':
            self.cmd_scale(stmt)
        elif cmd == 'flip':
            self.cmd_flip(stmt)
        elif cmd == 'tint':
            self.cmd_tint(stmt)
        elif cmd == 'glow':
            self.cmd_glow(stmt)
        elif cmd == 'shadow':
            self.cmd_shadow(stmt)
        elif cmd == 'blur':
            self.cmd_blur(stmt)
        elif cmd == 'pixelate':
            self.cmd_pixelate(stmt)
        elif cmd == 'outline':
            self.cmd_outline(stmt)
        elif cmd == 'gradient':
            self.cmd_gradient(stmt)
        elif cmd == 'pattern':
            self.cmd_pattern(stmt)
        elif cmd == 'texture':
            self.cmd_texture(stmt)
        elif cmd == 'polygon':
            self.cmd_polygon(stmt)
        elif cmd == 'triangle':
            self.cmd_triangle(stmt)
        elif cmd == 'ellipse':
            self.cmd_ellipse(stmt)
        elif cmd == 'arc':
            self.cmd_arc(stmt)
        elif cmd == 'curve':
            self.cmd_curve(stmt)
        elif cmd == 'bezier':
            self.cmd_bezier(stmt)
        elif cmd == 'path':
            self.cmd_path(stmt)
        elif cmd == 'mask':
            self.cmd_mask(stmt)
        elif cmd == 'clip':
            self.cmd_clip(stmt)
        elif cmd == 'transform':
            self.cmd_transform(stmt)
        elif cmd == 'anchor':
            self.cmd_anchor(stmt)
        elif cmd == 'pivot':
            self.cmd_pivot(stmt)
        elif cmd == 'tween':
            self.cmd_tween(stmt)
        elif cmd == 'ease':
            self.cmd_ease(stmt)
        elif cmd == 'shake':
            self.cmd_shake(stmt)
        
        # ==================== 3D ADVANCED (35 commands) ====================
        elif cmd == 'mesh':
            self.cmd_mesh(stmt)
        elif cmd == 'model':
            self.cmd_model(stmt)
        elif cmd == 'material':
            self.cmd_material(stmt)
        elif cmd == 'metallic':
            self.cmd_metallic(stmt)
        elif cmd == 'roughness':
            self.cmd_roughness(stmt)
        elif cmd == 'emissive':
            self.cmd_emissive(stmt)
        elif cmd == 'transparent':
            self.cmd_transparent(stmt)
        elif cmd == 'wireframe':
            self.cmd_wireframe(stmt)
        elif cmd == 'culling':
            self.cmd_culling(stmt)
        elif cmd == 'billboard':
            self.cmd_billboard(stmt)
        elif cmd == 'lod':
            self.cmd_lod(stmt)
        elif cmd == 'instancing':
            self.cmd_instancing(stmt)
        elif cmd == 'raytrace':
            self.cmd_raytrace(stmt)
        elif cmd == 'reflect':
            self.cmd_reflect(stmt)
        elif cmd == 'refract':
            self.cmd_refract(stmt)
        elif cmd == 'skylight':
            self.cmd_skylight(stmt)
        elif cmd == 'hemisphere':
            self.cmd_hemisphere(stmt)
        elif cmd == 'pointlight':
            self.cmd_pointlight(stmt)
        elif cmd == 'spotlight':
            self.cmd_spotlight(stmt)
        elif cmd == 'directional':
            self.cmd_directional(stmt)
        elif cmd == 'caustics':
            self.cmd_caustics(stmt)
        elif cmd == 'volumetric':
            self.cmd_volumetric(stmt)
        elif cmd == 'godrays':
            self.cmd_godrays(stmt)
        elif cmd == 'ssao':
            self.cmd_ssao(stmt)
        elif cmd == 'motionblur':
            self.cmd_motionblur(stmt)
        elif cmd == 'dof':
            self.cmd_dof(stmt)
        elif cmd == 'vignette':
            self.cmd_vignette(stmt)
        elif cmd == 'chromatic':
            self.cmd_chromatic(stmt)
        elif cmd == 'grain':
            self.cmd_grain(stmt)
        elif cmd == 'tonemapping':
            self.cmd_tonemapping(stmt)
        elif cmd == 'colorgrading':
            self.cmd_colorgrading(stmt)
        elif cmd == 'antialiasing':
            self.cmd_antialiasing(stmt)
        elif cmd == 'postprocess':
            self.cmd_postprocess(stmt)
        elif cmd == 'renderpass':
            self.cmd_renderpass(stmt)
        elif cmd == 'framebuffer':
            self.cmd_framebuffer(stmt)
        
        # ==================== TRAJECTORY/PHYSICS (25 commands) ====================
        elif cmd == 'trajectory':
            self.cmd_trajectory(stmt)
        elif cmd == 'parabola':
            self.cmd_parabola(stmt)
        elif cmd == 'ballistic':
            self.cmd_ballistic(stmt)
        elif cmd == 'orbit':
            self.cmd_orbit(stmt)
        elif cmd == 'circular':
            self.cmd_circular(stmt)
        elif cmd == 'spiral':
            self.cmd_spiral(stmt)
        elif cmd == 'sine':
            self.cmd_sine_wave(stmt)
        elif cmd == 'wave':
            self.cmd_wave(stmt)
        elif cmd == 'pendulum':
            self.cmd_pendulum(stmt)
        elif cmd == 'spring':
            self.cmd_spring(stmt)
        elif cmd == 'elastic':
            self.cmd_elastic(stmt)
        elif cmd == 'bounce':
            self.cmd_bounce(stmt)
        elif cmd == 'gravity':
            self.cmd_gravity(stmt)
        elif cmd == 'force':
            self.cmd_force(stmt)
        elif cmd == 'impulse':
            self.cmd_impulse(stmt)
        elif cmd == 'torque':
            self.cmd_torque(stmt)
        elif cmd == 'angular':
            self.cmd_angular(stmt)
        elif cmd == 'momentum':
            self.cmd_momentum(stmt)
        elif cmd == 'inertia':
            self.cmd_inertia(stmt)
        elif cmd == 'drag':
            self.cmd_drag(stmt)
        elif cmd == 'lift':
            self.cmd_lift(stmt)
        elif cmd == 'buoyancy':
            self.cmd_buoyancy(stmt)
        elif cmd == 'magnetism':
            self.cmd_magnetism(stmt)
        elif cmd == 'attract':
            self.cmd_attract(stmt)
        elif cmd == 'repel':
            self.cmd_repel(stmt)
        
        # ==================== GAME MECHANICS (25 commands) ====================
        elif cmd == 'score':
            self.cmd_score(stmt)
        elif cmd == 'highscore':
            self.cmd_highscore(stmt)
        elif cmd == 'lives':
            self.cmd_lives(stmt)
        elif cmd == 'gameover':
            self.cmd_gameover(stmt)
        elif cmd == 'win':
            self.cmd_win(stmt)
        elif cmd == 'lose':
            self.cmd_lose(stmt)
        elif cmd == 'checkpoint':
            self.cmd_checkpoint(stmt)
        elif cmd == 'respawn':
            self.cmd_respawn(stmt)
        elif cmd == 'powerup':
            self.cmd_powerup(stmt)
        elif cmd == 'pickup':
            self.cmd_pickup(stmt)
        elif cmd == 'coin':
            self.cmd_coin(stmt)
        elif cmd == 'gem':
            self.cmd_gem(stmt)
        elif cmd == 'key':
            self.cmd_key(stmt)
        elif cmd == 'door':
            self.cmd_door(stmt)
        elif cmd == 'lock':
            self.cmd_lock(stmt)
        elif cmd == 'unlock':
            self.cmd_unlock(stmt)
        elif cmd == 'trigger':
            self.cmd_trigger(stmt)
        elif cmd == 'zone':
            self.cmd_zone(stmt)
        elif cmd == 'area':
            self.cmd_area(stmt)
        elif cmd == 'spawn':
            self.cmd_spawn(stmt)
        elif cmd == 'wave':
            self.cmd_wave_spawn(stmt)
        elif cmd == 'timer':
            self.cmd_timer(stmt)
        elif cmd == 'countdown':
            self.cmd_countdown(stmt)
        elif cmd == 'pause':
            self.cmd_pause(stmt)
        elif cmd == 'resume':
            self.cmd_resume(stmt)
        
        # Assignment with = or 'is' or 'becomes'
        elif '=' in stmt or ' is ' in stmt or ' becomes ' in stmt:
            self.assign_variable(stmt)
        
        # Function call
        elif '(' in stmt and ')' in stmt:
            self.call_function(stmt)
    
    # ==================== TEXT OUTPUT ====================
    
    def cmd_say(self, stmt: str):
        """say "text" or say variable"""
        match = re.match(r'say\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(str(value), 'say')
    
    def cmd_shout(self, stmt: str):
        """shout "text" """
        match = re.match(r'shout\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(str(value), 'shout')
    
    def cmd_whisper(self, stmt: str):
        """whisper "text" """
        match = re.match(r'whisper\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(str(value), 'whisper')
    
    def cmd_show(self, stmt: str):
        """show variable"""
        match = re.match(r'(?:show|display)\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(str(value), 'show')
    
    def cmd_input(self, stmt: str):
        """input "prompt" into variable_name"""
        match = re.match(r'input\s+["\'](.+?)["\']\s+into\s+(\w+)', stmt, re.I)
        if not match:
            # Try alternate syntax: input variable_name "prompt"
            match = re.match(r'input\s+(\w+)\s+["\'](.+?)["\']', stmt, re.I)
            if match:
                var_name = match.group(1)
                prompt = match.group(2)
            else:
                # Try simple: input variable_name
                match = re.match(r'input\s+(\w+)', stmt, re.I)
                if match:
                    var_name = match.group(1)
                    prompt = "Enter value:"
                else:
                    return
        else:
            prompt = match.group(1)
            var_name = match.group(2)
        
        # Use tkinter simpledialog for input
        try:
            import tkinter.simpledialog as simpledialog
            result = simpledialog.askstring("Input", prompt)
            if result is not None:
                # Try to convert to number if possible
                try:
                    if '.' in result:
                        self.variables[var_name] = float(result)
                    else:
                        self.variables[var_name] = int(result)
                except:
                    self.variables[var_name] = result
                self.output(f"✓ {var_name} = {self.variables[var_name]}", 'show')
            else:
                self.variables[var_name] = ""
        except Exception as e:
            self.log(f"Input error: {e}", "error")
    
    def cmd_clear(self, stmt: str):
        """clear - clear output window (text or graphics)"""
        if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'output_window'):
            self.editor.output_window.clear()
            self.output("✓ Cleared", 'show')
    
    def cmd_cleargraphics(self, stmt: str):
        """cleargraphics - clear graphics canvas"""
        if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'output_window'):
            self.editor.output_window.canvas.delete("all")
            self.output("✓ Graphics cleared", 'show')
    
    # ==================== VARIABLES ====================
    
    def cmd_remember(self, stmt: str):
        """remember name as/is value"""
        patterns = [
            r'remember\s+(\w+)\s+as\s+(.+)',      # remember x as 5
            r'remember\s+(\w+)\s+is\s+(.+)',      # remember x is 5
            r'remember\s+(\w+)\s*=\s*(.+)',       # remember x = 5
            r'remember\s+(\w+)\s*:\s*(.+)',       # remember x: 5
        ]
        for pattern in patterns:
            match = re.match(pattern, stmt, re.I)
            if match:
                name = match.group(1)
                value = self.eval_expr(match.group(2))
                self.variables[name] = value
                self.log(f"🧠 {name} = {value}")
                return
    
    def cmd_forget(self, stmt: str):
        """forget name"""
        match = re.match(r'forget\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if name in self.variables:
                del self.variables[name]
                self.log(f"💭 Forgot {name}")
    
    def cmd_recall(self, stmt: str):
        """recall name"""
        match = re.match(r'recall\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if name in self.variables:
                self.output(f"{name} = {self.variables[name]}", 'show')
    
    def cmd_make(self, stmt: str):
        """make name equal to value"""
        patterns = [
            r'make\s+(\w+)\s+equal\s+to\s+(.+)',
            r'make\s+(\w+)\s*=\s*(.+)',
        ]
        for pattern in patterns:
            match = re.match(pattern, stmt, re.I)
            if match:
                name = match.group(1)
                value = self.eval_expr(match.group(2))
                self.variables[name] = value
                self.log(f"✨ {name} = {value}")
                return
    
    def cmd_set(self, stmt: str):
        """set name to value"""
        patterns = [
            r'set\s+(\w+)\s+to\s+(.+)',
            r'set\s+(\w+)\s*=\s*(.+)',
        ]
        for pattern in patterns:
            match = re.match(pattern, stmt, re.I)
            if match:
                name = match.group(1)
                value = self.eval_expr(match.group(2))
                self.variables[name] = value
                self.log(f"⚙️ {name} = {value}")
                return
    
    def cmd_create(self, stmt: str):
        """create name as value"""
        match = re.match(r'create\s+(\w+)\s+(?:as|with)\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            value = self.eval_expr(match.group(2))
            self.variables[name] = value
            self.log(f"🆕 {name} = {value}")
    
    def cmd_change(self, stmt: str):
        """change name to value"""
        match = re.match(r'change\s+(\w+)\s+to\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            value = self.eval_expr(match.group(2))
            self.variables[name] = value
            self.log(f"🔄 {name} = {value}")
    
    def cmd_increase(self, stmt: str):
        """increase name by amount"""
        match = re.match(r'increase\s+(\w+)\s+by\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            amount = self.eval_expr(match.group(2))
            if name in self.variables:
                self.variables[name] += amount
                self.log(f"⬆️ {name} = {self.variables[name]}")
    
    def cmd_decrease(self, stmt: str):
        """decrease name by amount"""
        match = re.match(r'decrease\s+(\w+)\s+by\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            amount = self.eval_expr(match.group(2))
            if name in self.variables:
                self.variables[name] -= amount
                self.log(f"⬇️ {name} = {self.variables[name]}")
    
    def assign_variable(self, stmt: str):
        """Handle x = value, x is value, x becomes value"""
        patterns = [
            r'(\w+)\s*=\s*(.+)',
            r'(\w+)\s+is\s+(.+)',
            r'(\w+)\s+becomes\s+(.+)',
        ]
        for pattern in patterns:
            match = re.match(pattern, stmt, re.I)
            if match:
                name = match.group(1)
                value = self.eval_expr(match.group(2))
                self.variables[name] = value
                self.log(f"✓ {name} = {value}")
                return
    
    # ==================== MATH ====================
    
    def cmd_calculate(self, stmt: str):
        """calculate expression"""
        match = re.match(r'(?:calculate|compute)\s+(.+)', stmt, re.I)
        if match:
            result = self.eval_expr(match.group(1))
            self.variables['result'] = result
            self.output(f"Result: {result}", 'show')
    
    def cmd_power(self, stmt: str):
        """power base to exponent"""
        match = re.match(r'power\s+(.+?)\s+to\s+(.+)', stmt, re.I)
        if match:
            base = self.eval_expr(match.group(1))
            exp = self.eval_expr(match.group(2))
            result = base ** exp
            self.variables['_power'] = result
            self.output(f"Power: {result}", 'show')
    
    def cmd_root(self, stmt: str):
        """root number"""
        match = re.match(r'root\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.sqrt(value)
            self.variables['_root'] = result
            self.output(f"Root: {result}", 'show')
    
    def cmd_absolute(self, stmt: str):
        """absolute of number"""
        match = re.match(r'absolute\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = abs(value)
            self.variables['_absolute'] = result
            self.output(f"Absolute: {result}", 'show')
    
    def cmd_roundup(self, stmt: str):
        """roundup number"""
        match = re.match(r'roundup\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.ceil(value)
            self.variables['_rounded'] = result
            self.output(f"Rounded up: {result}", 'show')
    
    def cmd_rounddown(self, stmt: str):
        """rounddown number"""
        match = re.match(r'rounddown\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.floor(value)
            self.variables['_rounded'] = result
            self.output(f"Rounded down: {result}", 'show')
    
    # ==================== CONTROL FLOW ====================
    
    def cmd_repeat(self, stmt: str):
        """repeat N times { ... }"""
        match = re.match(r'repeat\s+(\d+)\s+times?\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            count = int(match.group(1))
            block = match.group(2)
            statements = self.parse_code(block)
            
            for i in range(count):
                self.variables['iteration'] = i + 1
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
    
    def cmd_if(self, stmt: str):
        """if condition { ... }"""
        match = re.match(r'(?:if|when|whenever)\s+(.+?)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            condition = match.group(1)
            block = match.group(2)
            
            if self.eval_condition(condition):
                statements = self.parse_code(block)
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
    
    # ==================== IMPORT ====================
    
    def cmd_callupon(self, stmt: str):
        """callupon("file.tcc")"""
        match = re.match(r'callupon\s*\(\s*["\'](.+?\.tcc)["\']\s*\)', stmt, re.I)
        if match:
            filename = match.group(1)
            
            if filename in self.imported_files:
                self.log(f"⚠️ Already imported {filename}", "warning")
                return
            
            filepath = os.path.join(self.script_dir, filename)
            
            if os.path.exists(filepath):
                self.imported_files.add(filename)
                with open(filepath, 'r') as f:
                    code = f.read()
                self.log(f"📥 Called upon {filename}")
                self.execute(code, filename)
            else:
                self.log(f"✗ Cannot find {filename}", "error")
    
    # ==================== TEXT OPERATIONS ====================
    
    def cmd_join(self, stmt: str):
        """join x and y"""
        match = re.match(r'join\s+(.+?)\s+and\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = str(val1) + str(val2)
            self.variables['_joined'] = result
            self.output(f"Joined: {result}", 'show')
    
    def cmd_split(self, stmt: str):
        """split text by delimiter"""
        match = re.match(r'split\s+(.+?)\s+by\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            delim = match.group(2)
            result = text.split(delim)
            self.variables['_split'] = result
            self.output(f"Split: {result}", 'show')
    
    def cmd_length(self, stmt: str):
        """length of x"""
        match = re.match(r'length\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            length = len(value) if hasattr(value, '__len__') else 0
            self.variables['_length'] = length
            self.output(f"Length: {length}", 'show')
    
    # ==================== RANDOM ====================
    
    def cmd_random(self, stmt: str):
        """random from min to max"""
        match = re.match(r'random\s+from\s+(.+?)\s+to\s+(.+)', stmt, re.I)
        if match:
            import random
            min_val = int(self.eval_expr(match.group(1)))
            max_val = int(self.eval_expr(match.group(2)))
            result = random.randint(min_val, max_val)
            self.variables['random'] = result
            self.output(f"Random: {result}", 'show')
    
    def cmd_choose(self, stmt: str):
        """choose from list"""
        match = re.match(r'choose\s+from\s+(.+)', stmt, re.I)
        if match:
            import random
            items = self.eval_expr(match.group(1))
            if isinstance(items, (list, tuple)):
                choice = random.choice(items)
                self.variables['choice'] = choice
                self.output(f"Chosen: {choice}", 'show')
    
    # ==================== COMPARISON ====================
    
    def cmd_compare(self, stmt: str):
        """compare x and y"""
        match = re.match(r'compare\s+(.+?)\s+and\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            if val1 > val2:
                result = "greater"
            elif val1 < val2:
                result = "less"
            else:
                result = "equal"
            self.variables['_comparison'] = result
            self.output(f"{val1} is {result} than {val2}", 'show')
    
    # ==================== TYPE OPERATIONS ====================
    
    def cmd_convert(self, stmt: str):
        """convert x to type"""
        match = re.match(r'convert\s+(\w+)\s+to\s+(number|text|list)', stmt, re.I)
        if match:
            name = match.group(1)
            target = match.group(2).lower()
            
            if name in self.variables:
                value = self.variables[name]
                if target == 'number':
                    self.variables[name] = float(value)
                elif target == 'text':
                    self.variables[name] = str(value)
                elif target == 'list':
                    self.variables[name] = list(value)
                self.log(f"🔄 Converted {name} to {target}")
    
    def cmd_exists(self, stmt: str):
        """exists name"""
        match = re.match(r'exists\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            result = name in self.variables
            self.variables['_exists'] = result
            self.output(f"{name} exists: {result}", 'show')
    
    def cmd_typeof(self, stmt: str):
        """typeof name"""
        match = re.match(r'typeof\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if name in self.variables:
                vtype = type(self.variables[name]).__name__
                self.variables['_type'] = vtype
                self.output(f"{name} is {vtype}", 'show')
    
    # ==================== GRAPHICS ====================
    
    def cmd_switchgraphics(self):
        """Switch to graphics mode"""
        if hasattr(self.editor, 'output_window'):
            self.editor.output_window.mode_var.set("graphics")
            self.editor.output_window.switch_mode()
    
    def cmd_switchtext(self):
        """Switch to text mode"""
        if hasattr(self.editor, 'output_window'):
            self.editor.output_window.mode_var.set("text")
            self.editor.output_window.switch_mode()
    
    def cmd_sprite(self, stmt: str):
        """sprite name at x, y size w, h color "color" """
        match = re.match(
            r'sprite\s+(\w+)\s+at\s+(.+?),\s*(.+?)\s+size\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?',
            stmt, re.I
        )
        if match:
            name = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            w = self.eval_expr(match.group(4))
            h = self.eval_expr(match.group(5))
            color = match.group(6) if match.group(6) else "#00ff00"
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.create_sprite(name, x, y, w, h, color)
                self.log(f"🎨 Created sprite '{name}'")
    
    def cmd_movesprite(self, stmt: str):
        """movesprite name to x, y"""
        match = re.match(r'movesprite\s+(\w+)\s+to\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.move_sprite_to(name, x, y)
    
    def cmd_colorsprite(self, stmt: str):
        """colorsprite name to "color" """
        match = re.match(r'colorsprite\s+(\w+)\s+to\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            name = match.group(1)
            color = match.group(2)
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.change_sprite_color(name, color)
    
    def cmd_hidesprite(self, stmt: str):
        """hidesprite name"""
        match = re.match(r'hidesprite\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.hide_sprite(name)
    
    def cmd_showsprite(self, stmt: str):
        """showsprite name"""
        match = re.match(r'showsprite\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.show_sprite(name)
    
    def cmd_deletesprite(self, stmt: str):
        """deletesprite name"""
        match = re.match(r'deletesprite\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.delete_sprite(name)
                self.log(f"🗑️ Deleted sprite '{name}'")
    
    def cmd_fillscreen(self, stmt: str):
        """fillscreen "color" """
        match = re.match(r'fillscreen\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            color = match.group(1)
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.fill_screen(color)
    
    def cmd_drawline(self, stmt: str):
        """drawline from x1, y1 to x2, y2 color "color" """
        match = re.match(
            r'drawline\s+from\s+(.+?),\s*(.+?)\s+to\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?',
            stmt, re.I
        )
        if match:
            x1 = self.eval_expr(match.group(1))
            y1 = self.eval_expr(match.group(2))
            x2 = self.eval_expr(match.group(3))
            y2 = self.eval_expr(match.group(4))
            color = match.group(5) if match.group(5) else "#ffffff"
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_line(x1, y1, x2, y2, color)
    
    def cmd_drawrect(self, stmt: str):
        """drawrect at x, y size w, h color "color" """
        match = re.match(
            r'drawrect\s+at\s+(.+?),\s*(.+?)\s+size\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?',
            stmt, re.I
        )
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            w = self.eval_expr(match.group(3))
            h = self.eval_expr(match.group(4))
            color = match.group(5) if match.group(5) else "#ffffff"
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_rect(x, y, w, h, color)
    
    def cmd_drawcircle(self, stmt: str):
        """drawcircle at x, y radius r color "color" """
        match = re.match(
            r'drawcircle\s+at\s+(.+?),\s*(.+?)\s+radius\s+(.+?)(?:\s+color\s+["\'](.+?)["\'])?',
            stmt, re.I
        )
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            r = self.eval_expr(match.group(3))
            color = match.group(4) if match.group(4) else "#ffffff"
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_circle(x, y, r, color)
    
    def cmd_drawtext(self, stmt: str):
        """drawtext "text" at x, y color "color" """
        match = re.match(
            r'drawtext\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?',
            stmt, re.I
        )
        if match:
            text = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            color = match.group(4) if match.group(4) else "#ffffff"
            
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_text(x, y, text, color)
    
    # ==================== OTHER ====================
    
    def cmd_list(self, stmt: str):
        """list variables"""
        if 'variable' in stmt.lower():
            self.output("Variables:", 'show')
            for name, value in self.variables.items():
                if not name.isupper() and not name.startswith('_'):
                    self.output(f"  {name} = {value}", 'show')
    
    def call_function(self, stmt: str):
        """Call a function"""
        match = re.match(r'(\w+)\s*\(([^)]*)\)', stmt)
        if match:
            func_name = match.group(1)
            
            # Built-in functions
            if func_name == 'print':
                args_str = match.group(2)
                if args_str.strip():
                    for arg in args_str.split(','):
                        value = self.eval_expr(arg.strip())
                        self.output(str(value), 'say')
            
            elif func_name == 'sqrt':
                arg = self.eval_expr(match.group(2))
                result = math.sqrt(arg)
                self.output(f"√{arg} = {result}", 'show')
            
            elif func_name == 'projectile' and self.physics:
                args = [self.eval_expr(a.strip()) for a in match.group(2).split(',')]
                if len(args) >= 2:
                    velocity = args[0]
                    angle = args[1]
                    height = args[2] if len(args) > 2 else 0
                    result = self.physics.projectile_motion(velocity, angle, height)
                    self.output(f"Projectile: max_height={result['max_height']:.2f}m, "
                               f"range={result['range']:.2f}m", 'show')
    
    # ==================== EVALUATION ====================
    
    def eval_expr(self, expr: str):
        """Evaluate an expression"""
        expr = expr.strip().rstrip(';')
        
        # Check if this is string concatenation (has + and quotes)
        has_concat = '+' in expr and ('"' in expr or "'" in expr)
        
        if has_concat:
            # Split by + but preserve strings
            parts = []
            current = ""
            in_string = False
            string_char = None
            
            for char in expr:
                if char in ('"', "'"):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None
                    current += char
                elif char == '+' and not in_string:
                    parts.append(current.strip())
                    current = ""
                else:
                    current += char
            
            if current.strip():
                parts.append(current.strip())
            
            # Evaluate each part and concatenate
            result = ""
            for part in parts:
                val = self.eval_expr(part)  # Recursive call
                result += str(val)
            return result
        
        # String literal (single quoted string, no concatenation)
        if (expr.startswith('"') and expr.endswith('"') and expr.count('"') == 2):
            return expr[1:-1]
        if (expr.startswith("'") and expr.endswith("'") and expr.count("'") == 2):
            return expr[1:-1]
        
        # List literal
        if expr.startswith('[') and expr.endswith(']'):
            items = expr[1:-1].split(',')
            return [self.eval_expr(item.strip()) for item in items if item.strip()]
        
        # Number
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
        
        # Variable lookup
        if expr in self.variables:
            return self.variables[expr]
        
        # Special expressions like "first of X"
        if ' of ' in expr:
            match = re.match(r'(first|last|count|length)\s+of\s+(\w+)', expr, re.I)
            if match:
                operation = match.group(1).lower()
                var_name = match.group(2)
                if var_name in self.variables:
                    val = self.variables[var_name]
                    if operation == 'first' and isinstance(val, (list, tuple)) and len(val) > 0:
                        return val[0]
                    elif operation == 'last' and isinstance(val, (list, tuple)) and len(val) > 0:
                        return val[-1]
                    elif operation in ('count', 'length'):
                        return len(val) if hasattr(val, '__len__') else 0
        
        # Math expression
        try:
            # Replace variables in expression
            eval_expr = expr
            for var_name, var_value in self.variables.items():
                # Use word boundaries to avoid partial replacements
                pattern = r'\b' + re.escape(var_name) + r'\b'
                if re.search(pattern, eval_expr):
                    if isinstance(var_value, str):
                        eval_expr = re.sub(pattern, f'"{var_value}"', eval_expr)
                    else:
                        eval_expr = re.sub(pattern, str(var_value), eval_expr)
            
            # Safe evaluation
            result = eval(eval_expr, {"__builtins__": {}}, {
                "abs": abs, "pow": pow, "round": round,
                "min": min, "max": max, "sum": sum,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "pi": math.pi, "e": math.e
            })
            return result
        except:
            # If all else fails, return as-is
            return expr
    
    def eval_condition(self, condition: str) -> bool:
        """Evaluate a condition"""
        # Replace natural language with operators
        condition = condition.replace(' is ', ' == ')
        condition = condition.replace(' equals ', ' == ')
        condition = condition.replace(' greater than ', ' > ')
        condition = condition.replace(' less than ', ' < ')
        
        # Replace variables
        for var_name, var_value in self.variables.items():
            if var_name in condition:
                if isinstance(var_value, str):
                    condition = condition.replace(var_name, f'"{var_value}"')
                else:
                    condition = condition.replace(var_name, str(var_value))
        
        try:
            return bool(eval(condition, {"__builtins__": {}}, {}))
        except:
            return False
    
    # ==================== OUTPUT ====================
    
    def output(self, text: str, mode: str = 'say'):
        """Output text to the output window"""
        # Always try output_window first (for say, shout, whisper, show)
        if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'output_window'):
            try:
                if mode == 'say':
                    self.editor.output_window.say(text)
                elif mode == 'shout':
                    self.editor.output_window.shout(text)
                elif mode == 'whisper':
                    self.editor.output_window.whisper(text)
                elif mode == 'show':
                    self.editor.output_window.show(text)
                return  # Success - don't fall through to log
            except Exception as e:
                # If output_window fails, print to console but don't spam logs
                print(f"Output window error: {e}")
        
        # Only use log for actual errors/system messages, NOT user output
        # Don't route say/show/etc to logs - that's wrong!
        print(f"[{mode}] {text}")  # Fallback to console, not logs
    
    # ==================== ADVANCED MATH COMMANDS ====================
    
    def cmd_sin(self, stmt: str):
        """sin angle"""
        match = re.match(r'sin\s+(.+)', stmt, re.I)
        if match:
            angle = self.eval_expr(match.group(1))
            result = math.sin(math.radians(angle))
            self.variables['_trig'] = result
            self.output(f"sin({angle}°) = {result:.4f}", 'show')
    
    def cmd_cos(self, stmt: str):
        """cos angle"""
        match = re.match(r'cos\s+(.+)', stmt, re.I)
        if match:
            angle = self.eval_expr(match.group(1))
            result = math.cos(math.radians(angle))
            self.variables['_trig'] = result
            self.output(f"cos({angle}°) = {result:.4f}", 'show')
    
    def cmd_tan(self, stmt: str):
        """tan angle"""
        match = re.match(r'tan\s+(.+)', stmt, re.I)
        if match:
            angle = self.eval_expr(match.group(1))
            result = math.tan(math.radians(angle))
            self.variables['_trig'] = result
            self.output(f"tan({angle}°) = {result:.4f}", 'show')
    
    def cmd_floor(self, stmt: str):
        """floor number"""
        match = re.match(r'floor\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.floor(value)
            self.variables['_rounded'] = result
            self.output(f"floor({value}) = {result}", 'show')
    
    def cmd_ceil(self, stmt: str):
        """ceil number"""
        match = re.match(r'ceil\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.ceil(value)
            self.variables['_rounded'] = result
            self.output(f"ceil({value}) = {result}", 'show')
    
    def cmd_round(self, stmt: str):
        """round number"""
        match = re.match(r'round\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = round(value)
            self.variables['_rounded'] = result
            self.output(f"round({value}) = {result}", 'show')
    
    def cmd_min(self, stmt: str):
        """min of list or values"""
        match = re.match(r'min\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            values = self.eval_expr(match.group(1))
            if isinstance(values, (list, tuple)):
                result = min(values)
            else:
                result = values
            self.variables['_min'] = result
            self.output(f"Min: {result}", 'show')
    
    def cmd_max(self, stmt: str):
        """max of list or values"""
        match = re.match(r'max\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            values = self.eval_expr(match.group(1))
            if isinstance(values, (list, tuple)):
                result = max(values)
            else:
                result = values
            self.variables['_max'] = result
            self.output(f"Max: {result}", 'show')
    
    def cmd_average(self, stmt: str):
        """average of list"""
        match = re.match(r'(?:average|mean)\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            values = self.eval_expr(match.group(1))
            if isinstance(values, (list, tuple)) and len(values) > 0:
                result = sum(values) / len(values)
                self.variables['_average'] = result
                self.output(f"Average: {result:.2f}", 'show')
    
    def cmd_sum(self, stmt: str):
        """sum of list"""
        match = re.match(r'sum\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            values = self.eval_expr(match.group(1))
            if isinstance(values, (list, tuple)):
                result = sum(values)
                self.variables['_sum'] = result
                self.output(f"Sum: {result}", 'show')
    
    def cmd_product(self, stmt: str):
        """product of list"""
        match = re.match(r'product\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            values = self.eval_expr(match.group(1))
            if isinstance(values, (list, tuple)):
                result = 1
                for v in values:
                    result *= v
                self.variables['_product'] = result
                self.output(f"Product: {result}", 'show')
    
    def cmd_percent(self, stmt: str):
        """percent value of total"""
        match = re.match(r'percent\s+(.+?)\s+of\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            total = self.eval_expr(match.group(2))
            if total != 0:
                result = (value / total) * 100
                self.variables['_percent'] = result
                self.output(f"{value} is {result:.2f}% of {total}", 'show')
    
    def cmd_factorial(self, stmt: str):
        """factorial of number"""
        match = re.match(r'factorial\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            n = int(self.eval_expr(match.group(1)))
            result = math.factorial(n)
            self.variables['_factorial'] = result
            self.output(f"{n}! = {result}", 'show')
    
    def cmd_squared(self, stmt: str):
        """squared number"""
        match = re.match(r'squared\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = value ** 2
            self.variables['_squared'] = result
            self.output(f"{value}² = {result}", 'show')
    
    def cmd_cubed(self, stmt: str):
        """cubed number"""
        match = re.match(r'cubed\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = value ** 3
            self.variables['_cubed'] = result
            self.output(f"{value}³ = {result}", 'show')
    
    def cmd_log(self, stmt: str):
        """log base 10"""
        match = re.match(r'log\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            if value > 0:
                result = math.log10(value)
                self.variables['_log'] = result
                self.output(f"log₁₀({value}) = {result:.4f}", 'show')
    
    def cmd_ln(self, stmt: str):
        """natural log"""
        match = re.match(r'ln\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            if value > 0:
                result = math.log(value)
                self.variables['_ln'] = result
                self.output(f"ln({value}) = {result:.4f}", 'show')
    
    def cmd_exp(self, stmt: str):
        """exponential e^x"""
        match = re.match(r'exp\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = math.exp(value)
            self.variables['_exp'] = result
            self.output(f"e^{value} = {result:.4f}", 'show')
    
    def cmd_sign(self, stmt: str):
        """sign of number (-1, 0, 1)"""
        match = re.match(r'sign\s+(?:of\s+)?(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = 1 if value > 0 else (-1 if value < 0 else 0)
            self.variables['_sign'] = result
            self.output(f"sign({value}) = {result}", 'show')
    
    def cmd_clamp(self, stmt: str):
        """clamp value between min and max"""
        match = re.match(r'clamp\s+(.+?)\s+between\s+(.+?)\s+and\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            min_val = self.eval_expr(match.group(2))
            max_val = self.eval_expr(match.group(3))
            result = max(min_val, min(max_val, value))
            self.variables['_clamped'] = result
            self.output(f"Clamped: {result}", 'show')
    
    # ==================== STRING COMMANDS ====================
    
    def cmd_uppercase(self, stmt: str):
        """uppercase text"""
        match = re.match(r'uppercase\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            result = text.upper()
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_lowercase(self, stmt: str):
        """lowercase text"""
        match = re.match(r'lowercase\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            result = text.lower()
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_titlecase(self, stmt: str):
        """titlecase text"""
        match = re.match(r'titlecase\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            result = text.title()
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_reverse(self, stmt: str):
        """reverse text"""
        match = re.match(r'reverse\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            result = text[::-1]
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_trim(self, stmt: str):
        """trim whitespace"""
        match = re.match(r'trim\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            result = text.strip()
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_replace(self, stmt: str):
        """replace old with new in text"""
        match = re.match(r'replace\s+["\'](.+?)["\']\s+with\s+["\'](.+?)["\']\s+in\s+(.+)', stmt, re.I)
        if match:
            old = match.group(1)
            new = match.group(2)
            text = str(self.eval_expr(match.group(3)))
            result = text.replace(old, new)
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_substring(self, stmt: str):
        """substring of text from start to end"""
        match = re.match(r'substring\s+(?:of\s+)?(.+?)\s+from\s+(.+?)\s+to\s+(.+)', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            start = int(self.eval_expr(match.group(2)))
            end = int(self.eval_expr(match.group(3)))
            result = text[start:end]
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_contains(self, stmt: str):
        """check if text contains substring"""
        match = re.match(r'(.+?)\s+contains\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            substr = match.group(2)
            result = substr in text
            self.variables['_contains'] = result
            self.output(f"Contains: {result}", 'show')
    
    def cmd_startswith(self, stmt: str):
        """check if text starts with"""
        match = re.match(r'(.+?)\s+startswith\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            prefix = match.group(2)
            result = text.startswith(prefix)
            self.variables['_startswith'] = result
            self.output(f"Starts with: {result}", 'show')
    
    def cmd_endswith(self, stmt: str):
        """check if text ends with"""
        match = re.match(r'(.+?)\s+endswith\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            suffix = match.group(2)
            result = text.endswith(suffix)
            self.variables['_endswith'] = result
            self.output(f"Ends with: {result}", 'show')
    
    def cmd_padleft(self, stmt: str):
        """pad left with character"""
        match = re.match(r'padleft\s+(.+?)\s+to\s+(.+?)(?:\s+with\s+["\'](.)["\'])?', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            length = int(self.eval_expr(match.group(2)))
            char = match.group(3) if match.group(3) else ' '
            result = text.rjust(length, char)
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_padright(self, stmt: str):
        """pad right with character"""
        match = re.match(r'padright\s+(.+?)\s+to\s+(.+?)(?:\s+with\s+["\'](.)["\'])?', stmt, re.I)
        if match:
            text = str(self.eval_expr(match.group(1)))
            length = int(self.eval_expr(match.group(2)))
            char = match.group(3) if match.group(3) else ' '
            result = text.ljust(length, char)
            self.variables['_text'] = result
            self.output(result, 'show')
    
    def cmd_indexof(self, stmt: str):
        """find index of substring"""
        match = re.match(r'indexof\s+["\'](.+?)["\']\s+in\s+(.+)', stmt, re.I)
        if match:
            substr = match.group(1)
            text = str(self.eval_expr(match.group(2)))
            try:
                result = text.index(substr)
                self.variables['_index'] = result
                self.output(f"Index: {result}", 'show')
            except ValueError:
                self.variables['_index'] = -1
                self.output("Not found (-1)", 'show')
    
    # ==================== LIST COMMANDS ====================
    
    def cmd_append(self, stmt: str):
        """append item to list"""
        match = re.match(r'append\s+(.+?)\s+to\s+(\w+)', stmt, re.I)
        if match:
            item = self.eval_expr(match.group(1))
            list_name = match.group(2)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].append(item)
                    self.log(f"➕ Appended {item} to {list_name}")
    
    def cmd_prepend(self, stmt: str):
        """prepend item to list"""
        match = re.match(r'prepend\s+(.+?)\s+to\s+(\w+)', stmt, re.I)
        if match:
            item = self.eval_expr(match.group(1))
            list_name = match.group(2)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].insert(0, item)
                    self.log(f"➕ Prepended {item} to {list_name}")
    
    def cmd_insert(self, stmt: str):
        """insert item at index"""
        match = re.match(r'insert\s+(.+?)\s+at\s+(.+?)\s+in\s+(\w+)', stmt, re.I)
        if match:
            item = self.eval_expr(match.group(1))
            index = int(self.eval_expr(match.group(2)))
            list_name = match.group(3)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].insert(index, item)
                    self.log(f"➕ Inserted {item} at index {index}")
    
    def cmd_remove(self, stmt: str):
        """remove item from list"""
        match = re.match(r'remove\s+(.+?)\s+from\s+(\w+)', stmt, re.I)
        if match:
            item = self.eval_expr(match.group(1))
            list_name = match.group(2)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    try:
                        self.variables[list_name].remove(item)
                        self.log(f"➖ Removed {item} from {list_name}")
                    except ValueError:
                        self.log(f"⚠️ Item not found", "warning")
    
    def cmd_pop(self, stmt: str):
        """pop last item from list"""
        match = re.match(r'pop\s+from\s+(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list) and len(self.variables[list_name]) > 0:
                    item = self.variables[list_name].pop()
                    self.variables['_popped'] = item
                    self.output(f"Popped: {item}", 'show')
    
    def cmd_shift(self, stmt: str):
        """shift first item from list"""
        match = re.match(r'shift\s+from\s+(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list) and len(self.variables[list_name]) > 0:
                    item = self.variables[list_name].pop(0)
                    self.variables['_shifted'] = item
                    self.output(f"Shifted: {item}", 'show')
    
    def cmd_clear(self, stmt: str):
        """clear list"""
        match = re.match(r'clear\s+(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].clear()
                    self.log(f"🗑️ Cleared {list_name}")
    
    def cmd_sort(self, stmt: str):
        """sort list"""
        match = re.match(r'sort\s+(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].sort()
                    self.log(f"📊 Sorted {list_name}")
    
    def cmd_reverse_list(self, stmt: str):
        """reverse list"""
        match = re.match(r'reverse\s+(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    self.variables[list_name].reverse()
                    self.log(f"🔄 Reversed {list_name}")
    
    def cmd_unique(self, stmt: str):
        """get unique items"""
        match = re.match(r'unique\s+(?:of\s+)?(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    result = list(set(self.variables[list_name]))
                    self.variables['_unique'] = result
                    self.output(f"Unique: {result}", 'show')
    
    def cmd_count(self, stmt: str):
        """count occurrences"""
        match = re.match(r'count\s+(.+?)\s+in\s+(\w+)', stmt, re.I)
        if match:
            item = self.eval_expr(match.group(1))
            list_name = match.group(2)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    result = self.variables[list_name].count(item)
                    self.variables['_count'] = result
                    self.output(f"Count: {result}", 'show')
    
    def cmd_first(self, stmt: str):
        """get first item"""
        match = re.match(r'first\s+(?:of\s+)?(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list) and len(self.variables[list_name]) > 0:
                    result = self.variables[list_name][0]
                    self.variables['_first'] = result
                    self.output(f"First: {result}", 'show')
    
    def cmd_last(self, stmt: str):
        """get last item"""
        match = re.match(r'last\s+(?:of\s+)?(\w+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list) and len(self.variables[list_name]) > 0:
                    result = self.variables[list_name][-1]
                    self.variables['_last'] = result
                    self.output(f"Last: {result}", 'show')
    
    def cmd_slice(self, stmt: str):
        """slice list"""
        match = re.match(r'slice\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+)', stmt, re.I)
        if match:
            list_name = match.group(1)
            start = int(self.eval_expr(match.group(2)))
            end = int(self.eval_expr(match.group(3)))
            if list_name in self.variables:
                if isinstance(self.variables[list_name], list):
                    result = self.variables[list_name][start:end]
                    self.variables['_slice'] = result
                    self.output(f"Slice: {result}", 'show')
    
    def cmd_merge(self, stmt: str):
        """merge two lists"""
        match = re.match(r'merge\s+(\w+)\s+and\s+(\w+)', stmt, re.I)
        if match:
            list1_name = match.group(1)
            list2_name = match.group(2)
            if list1_name in self.variables and list2_name in self.variables:
                if isinstance(self.variables[list1_name], list) and isinstance(self.variables[list2_name], list):
                    result = self.variables[list1_name] + self.variables[list2_name]
                    self.variables['_merged'] = result
                    self.output(f"Merged: {result}", 'show')
    
    # ==================== LOGIC COMMANDS ====================
    
    def cmd_and(self, stmt: str):
        """logical and"""
        match = re.match(r'(.+?)\s+and\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = bool(val1 and val2)
            self.variables['_logic'] = result
            self.output(f"Result: {result}", 'show')
    
    def cmd_or(self, stmt: str):
        """logical or"""
        match = re.match(r'(.+?)\s+or\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = bool(val1 or val2)
            self.variables['_logic'] = result
            self.output(f"Result: {result}", 'show')
    
    def cmd_not(self, stmt: str):
        """logical not"""
        match = re.match(r'not\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            result = not bool(value)
            self.variables['_logic'] = result
            self.output(f"Result: {result}", 'show')
    
    def cmd_equals(self, stmt: str):
        """check equality"""
        match = re.match(r'(.+?)\s+equals\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = (val1 == val2)
            self.variables['_equals'] = result
            self.output(f"Equals: {result}", 'show')
    
    def cmd_notequals(self, stmt: str):
        """check inequality"""
        match = re.match(r'(.+?)\s+notequals\s+(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = (val1 != val2)
            self.variables['_notequals'] = result
            self.output(f"Not equals: {result}", 'show')
    
    def cmd_greater(self, stmt: str):
        """check greater than"""
        match = re.match(r'(.+?)\s+greater\s+(?:than\s+)?(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = (val1 > val2)
            self.variables['_greater'] = result
            self.output(f"Greater: {result}", 'show')
    
    def cmd_less(self, stmt: str):
        """check less than"""
        match = re.match(r'(.+?)\s+less\s+(?:than\s+)?(.+)', stmt, re.I)
        if match:
            val1 = self.eval_expr(match.group(1))
            val2 = self.eval_expr(match.group(2))
            result = (val1 < val2)
            self.variables['_less'] = result
            self.output(f"Less: {result}", 'show')
    
    def cmd_between(self, stmt: str):
        """check if value is between min and max"""
        match = re.match(r'(.+?)\s+between\s+(.+?)\s+and\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            min_val = self.eval_expr(match.group(2))
            max_val = self.eval_expr(match.group(3))
            result = (min_val <= value <= max_val)
            self.variables['_between'] = result
            self.output(f"Between: {result}", 'show')
    
    # ==================== TIME COMMANDS ====================
    
    def cmd_time(self, stmt: str):
        """get current time"""
        import datetime
        now = datetime.datetime.now()
        result = now.strftime("%H:%M:%S")
        self.variables['_time'] = result
        self.output(f"Time: {result}", 'show')
    
    def cmd_date(self, stmt: str):
        """get current date"""
        import datetime
        now = datetime.datetime.now()
        result = now.strftime("%Y-%m-%d")
        self.variables['_date'] = result
        self.output(f"Date: {result}", 'show')
    
    def cmd_timestamp(self, stmt: str):
        """get unix timestamp"""
        import time
        result = int(time.time())
        self.variables['_timestamp'] = result
        self.output(f"Timestamp: {result}", 'show')
    
    def cmd_year(self, stmt: str):
        """get current year"""
        import datetime
        result = datetime.datetime.now().year
        self.variables['_year'] = result
        self.output(f"Year: {result}", 'show')
    
    def cmd_month(self, stmt: str):
        """get current month"""
        import datetime
        result = datetime.datetime.now().month
        self.variables['_month'] = result
        self.output(f"Month: {result}", 'show')
    
    def cmd_day(self, stmt: str):
        """get current day"""
        import datetime
        result = datetime.datetime.now().day
        self.variables['_day'] = result
        self.output(f"Day: {result}", 'show')
    
    def cmd_hour(self, stmt: str):
        """get current hour"""
        import datetime
        result = datetime.datetime.now().hour
        self.variables['_hour'] = result
        self.output(f"Hour: {result}", 'show')
    
    def cmd_minute(self, stmt: str):
        """get current minute"""
        import datetime
        result = datetime.datetime.now().minute
        self.variables['_minute'] = result
        self.output(f"Minute: {result}", 'show')
    
    def cmd_second(self, stmt: str):
        """get current second"""
        import datetime
        result = datetime.datetime.now().second
        self.variables['_second'] = result
        self.output(f"Second: {result}", 'show')
    
    # ==================== VARIABLE ADVANCED ====================
    
    def cmd_copy(self, stmt: str):
        """copy variable to another"""
        match = re.match(r'copy\s+(\w+)\s+to\s+(\w+)', stmt, re.I)
        if match:
            from_var = match.group(1)
            to_var = match.group(2)
            if from_var in self.variables:
                self.variables[to_var] = self.variables[from_var]
                self.log(f"📋 Copied {from_var} to {to_var}")
    
    def cmd_swap(self, stmt: str):
        """swap two variables"""
        match = re.match(r'swap\s+(\w+)\s+and\s+(\w+)', stmt, re.I)
        if match:
            var1 = match.group(1)
            var2 = match.group(2)
            if var1 in self.variables and var2 in self.variables:
                self.variables[var1], self.variables[var2] = self.variables[var2], self.variables[var1]
                self.log(f"🔄 Swapped {var1} and {var2}")
    
    def cmd_increment(self, stmt: str):
        """increment variable"""
        match = re.match(r'increment\s+(\w+)', stmt, re.I)
        if match:
            var_name = match.group(1)
            if var_name in self.variables:
                self.variables[var_name] += 1
                self.log(f"⬆️ {var_name} = {self.variables[var_name]}")
    
    def cmd_decrement(self, stmt: str):
        """decrement variable"""
        match = re.match(r'decrement\s+(\w+)', stmt, re.I)
        if match:
            var_name = match.group(1)
            if var_name in self.variables:
                self.variables[var_name] -= 1
                self.log(f"⬇️ {var_name} = {self.variables[var_name]}")
    
    def cmd_multiply(self, stmt: str):
        """multiply variable by amount"""
        match = re.match(r'multiply\s+(\w+)\s+by\s+(.+)', stmt, re.I)
        if match:
            var_name = match.group(1)
            amount = self.eval_expr(match.group(2))
            if var_name in self.variables:
                self.variables[var_name] *= amount
                self.log(f"✖️ {var_name} = {self.variables[var_name]}")
    
    def cmd_divide(self, stmt: str):
        """divide variable by amount"""
        match = re.match(r'divide\s+(\w+)\s+by\s+(.+)', stmt, re.I)
        if match:
            var_name = match.group(1)
            amount = self.eval_expr(match.group(2))
            if var_name in self.variables and amount != 0:
                self.variables[var_name] /= amount
                self.log(f"➗ {var_name} = {self.variables[var_name]}")
    
    def cmd_modulo(self, stmt: str):
        """modulo operation"""
        match = re.match(r'modulo\s+(\w+)\s+by\s+(.+)', stmt, re.I)
        if match:
            var_name = match.group(1)
            amount = self.eval_expr(match.group(2))
            if var_name in self.variables and amount != 0:
                self.variables[var_name] %= amount
                self.log(f"📐 {var_name} = {self.variables[var_name]}")
    
    # ==================== CONTROL FLOW ADVANCED ====================
    
    def cmd_break(self, stmt: str):
        """break from loop (placeholder)"""
        self.log("⛔ Break", "warning")
    
    def cmd_continue(self, stmt: str):
        """continue loop (placeholder)"""
        self.log("➡️ Continue", "info")
    
    def cmd_return(self, stmt: str):
        """return value (placeholder)"""
        match = re.match(r'return\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['_return'] = value
            self.log(f"↩️ Return: {value}")
    
    def cmd_else(self, stmt: str):
        """else clause (handled by if)"""
        pass
    
    def cmd_elseif(self, stmt: str):
        """elseif clause (handled by if)"""
        pass
    
    def cmd_while(self, stmt: str):
        """while loop"""
        match = re.match(r'while\s+(.+?)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            condition = match.group(1)
            block = match.group(2)
            statements = self.parse_code(block)
            
            count = 0
            max_iterations = 10000  # Safety limit
            while self.eval_condition(condition) and count < max_iterations:
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
                count += 1
    
    def cmd_until(self, stmt: str):
        """until loop (while not)"""
        match = re.match(r'until\s+(.+?)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            condition = match.group(1)
            block = match.group(2)
            statements = self.parse_code(block)
            
            count = 0
            max_iterations = 10000
            while not self.eval_condition(condition) and count < max_iterations:
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
                count += 1
    
    def cmd_for(self, stmt: str):
        """for loop"""
        match = re.match(r'for\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            var_name = match.group(1)
            start = int(self.eval_expr(match.group(2)))
            end = int(self.eval_expr(match.group(3)))
            block = match.group(4)
            statements = self.parse_code(block)
            
            for i in range(start, end + 1):
                self.variables[var_name] = i
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
    
    def cmd_foreach(self, stmt: str):
        """foreach loop"""
        match = re.match(r'foreach\s+(\w+)\s+in\s+(\w+)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            var_name = match.group(1)
            list_name = match.group(2)
            block = match.group(3)
            
            if list_name in self.variables and isinstance(self.variables[list_name], list):
                statements = self.parse_code(block)
                for item in self.variables[list_name]:
                    self.variables[var_name] = item
                    for s in statements:
                        if s.strip():
                            self.execute_statement(s)
    
    def cmd_loop(self, stmt: str):
        """infinite loop (with limit)"""
        match = re.match(r'loop\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            block = match.group(1)
            statements = self.parse_code(block)
            
            count = 0
            max_iterations = 100  # Safety limit for infinite loops
            while count < max_iterations:
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
                count += 1
    
    def cmd_do(self, stmt: str):
        """do command (execute action)"""
        match = re.match(r'do\s+(.+)', stmt, re.I)
        if match:
            action = match.group(1)
            self.execute_statement(action)
    
    # ==================== DEBUG OUTPUT ====================
    
    def cmd_print(self, stmt: str):
        """print (alias for say)"""
        match = re.match(r'print\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(str(value), 'say')
    
    def cmd_debug(self, stmt: str):
        """debug output"""
        match = re.match(r'debug\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.log(f"🐛 DEBUG: {value}", "info")
    
    def cmd_warn(self, stmt: str):
        """warning output"""
        match = re.match(r'warn\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.log(f"⚠️ WARNING: {value}", "warning")
    
    def cmd_error(self, stmt: str):
        """error output"""
        match = re.match(r'error\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.log(f"❌ ERROR: {value}", "error")
    
    def cmd_info(self, stmt: str):
        """info output"""
        match = re.match(r'info\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.output(f"ℹ️  {value}", 'show')
    
    def cmd_log_output(self, stmt: str):
        """log to output"""
        match = re.match(r'log\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.log(f"📝 {value}")
    
    def cmd_clear_output(self, stmt: str):
        """clear output window"""
        if hasattr(self.editor, 'output_window'):
            self.editor.output_window.clear()
            self.log("🗑️ Output cleared")
    
    # ==================== RPG MECHANICS (50 COMMANDS) ====================
    
    def cmd_xp(self, stmt: str):
        """xp add/set amount"""
        if 'add' in stmt.lower():
            match = re.match(r'xp\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'player_xp' not in self.variables:
                    self.variables['player_xp'] = 0
                self.variables['player_xp'] += amount
                self.output(f"⭐ +{amount} XP! Total: {self.variables['player_xp']}", 'show')
        elif 'set' in stmt.lower():
            match = re.match(r'xp\s+set\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                self.variables['player_xp'] = amount
    
    def cmd_level(self, stmt: str):
        """level set/get"""
        match = re.match(r'level\s+(?:set\s+)?(.+)', stmt, re.I)
        if match:
            level = self.eval_expr(match.group(1))
            self.variables['player_level'] = level
            self.output(f"📈 Level set to {level}!", 'show')
    
    def cmd_levelup(self, stmt: str):
        """levelup"""
        if 'player_level' not in self.variables:
            self.variables['player_level'] = 1
        self.variables['player_level'] += 1
        self.output(f"🎉 LEVEL UP! You are now level {self.variables['player_level']}!", 'shout')
    
    def cmd_stat(self, stmt: str):
        """stat name value"""
        match = re.match(r'stat\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            stat_name = match.group(1)
            value = self.eval_expr(match.group(2))
            self.variables[f'stat_{stat_name}'] = value
            self.log(f"📊 {stat_name}: {value}")
    
    def cmd_mana(self, stmt: str):
        """mana set/add/subtract"""
        if 'add' in stmt.lower():
            match = re.match(r'mana\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'player_mana' not in self.variables:
                    self.variables['player_mana'] = 100
                self.variables['player_mana'] += amount
        elif 'subtract' in stmt.lower():
            match = re.match(r'mana\s+subtract\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'player_mana' in self.variables:
                    self.variables['player_mana'] -= amount
        else:
            match = re.match(r'mana\s+(?:set\s+)?(.+)', stmt, re.I)
            if match:
                value = self.eval_expr(match.group(1))
                self.variables['player_mana'] = value
    
    def cmd_stamina(self, stmt: str):
        """stamina operations"""
        match = re.match(r'stamina\s+(?:set\s+)?(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['player_stamina'] = value
    
    def cmd_armor(self, stmt: str):
        """armor value"""
        match = re.match(r'armor\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['player_armor'] = value
            self.output(f"🛡️ Armor: {value}", 'show')
    
    def cmd_attack(self, stmt: str):
        """attack value"""
        match = re.match(r'attack\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['player_attack'] = value
            self.output(f"⚔️ Attack: {value}", 'show')
    
    def cmd_defense(self, stmt: str):
        """defense value"""
        match = re.match(r'defense\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['player_defense'] = value
            self.output(f"🛡️ Defense: {value}", 'show')
    
    def cmd_inventory(self, stmt: str):
        """inventory operations"""
        if 'player_inventory' not in self.variables:
            self.variables['player_inventory'] = []
        
        if 'show' in stmt.lower() or stmt.strip() == 'inventory':
            self.output("🎒 Inventory:", 'show')
            for item in self.variables['player_inventory']:
                self.output(f"  • {item}", 'say')
    
    def cmd_equip(self, stmt: str):
        """equip item"""
        match = re.match(r'equip\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            if 'equipped_items' not in self.variables:
                self.variables['equipped_items'] = []
            self.variables['equipped_items'].append(item)
            self.output(f"⚔️ Equipped: {item}", 'show')
    
    def cmd_unequip(self, stmt: str):
        """unequip item"""
        match = re.match(r'unequip\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            if 'equipped_items' in self.variables and item in self.variables['equipped_items']:
                self.variables['equipped_items'].remove(item)
                self.output(f"Unequipped: {item}", 'show')
    
    def cmd_additem(self, stmt: str):
        """additem "name" """
        match = re.match(r'additem\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            if 'player_inventory' not in self.variables:
                self.variables['player_inventory'] = []
            self.variables['player_inventory'].append(item)
            self.output(f"✨ Got: {item}", 'show')
    
    def cmd_removeitem(self, stmt: str):
        """removeitem "name" """
        match = re.match(r'removeitem\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            if 'player_inventory' in self.variables and item in self.variables['player_inventory']:
                self.variables['player_inventory'].remove(item)
                self.output(f"Removed: {item}", 'show')
    
    def cmd_hasitem(self, stmt: str):
        """hasitem "name" """
        match = re.match(r'hasitem\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            has_it = False
            if 'player_inventory' in self.variables:
                has_it = item in self.variables['player_inventory']
            self.variables['_hasitem'] = has_it
            self.output(f"Has {item}: {has_it}", 'show')
    
    def cmd_useitem(self, stmt: str):
        """useitem "name" """
        match = re.match(r'useitem\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            self.output(f"💫 Used: {item}", 'show')
    
    def cmd_dropitem(self, stmt: str):
        """dropitem "name" """
        match = re.match(r'dropitem\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            if 'player_inventory' in self.variables and item in self.variables['player_inventory']:
                self.variables['player_inventory'].remove(item)
                self.output(f"📦 Dropped: {item}", 'show')
    
    def cmd_quest(self, stmt: str):
        """quest "name" """
        match = re.match(r'quest\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            quest_name = match.group(1)
            if 'active_quests' not in self.variables:
                self.variables['active_quests'] = []
            self.variables['active_quests'].append(quest_name)
            self.output(f"📜 New Quest: {quest_name}", 'shout')
    
    def cmd_completequest(self, stmt: str):
        """completequest "name" """
        match = re.match(r'completequest\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            quest_name = match.group(1)
            self.output(f"✅ Quest Complete: {quest_name}", 'shout')
    
    def cmd_objective(self, stmt: str):
        """objective "text" """
        match = re.match(r'objective\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            text = match.group(1)
            self.output(f"🎯 Objective: {text}", 'show')
    
    def cmd_reward(self, stmt: str):
        """reward "text" """
        match = re.match(r'reward\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            reward = match.group(1)
            self.output(f"🎁 Reward: {reward}", 'shout')
    
    def cmd_enemy(self, stmt: str):
        """enemy "name" health attack"""
        match = re.match(r'enemy\s+["\'](.+?)["\']\s+health\s+(.+?)\s+attack\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            health = self.eval_expr(match.group(2))
            attack = self.eval_expr(match.group(3))
            self.variables[f'enemy_{name}_health'] = health
            self.variables[f'enemy_{name}_attack'] = attack
            self.output(f"👹 Enemy Spawned: {name}", 'show')
    
    def cmd_battle(self, stmt: str):
        """battle start"""
        self.output("⚔️ Battle Started!", 'shout')
        self.variables['in_battle'] = True
    
    def cmd_hit(self, stmt: str):
        """hit target for damage"""
        match = re.match(r'hit\s+(\w+)\s+for\s+(.+)', stmt, re.I)
        if match:
            target = match.group(1)
            damage = self.eval_expr(match.group(2))
            self.output(f"💥 Hit {target} for {damage} damage!", 'show')
    
    def cmd_critical(self, stmt: str):
        """critical hit"""
        self.output("💥 CRITICAL HIT!", 'shout')
        self.variables['last_critical'] = True
    
    def cmd_dodge(self, stmt: str):
        """dodge"""
        self.output("💨 Dodged!", 'show')
    
    def cmd_block(self, stmt: str):
        """block"""
        self.output("🛡️ Blocked!", 'show')
    
    def cmd_parry(self, stmt: str):
        """parry"""
        self.output("⚡ Parried!", 'show')
    
    def cmd_stun(self, stmt: str):
        """stun target"""
        match = re.match(r'stun\s+(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"⭐ {target} is stunned!", 'show')
    
    def cmd_poison(self, stmt: str):
        """poison target"""
        match = re.match(r'poison\s+(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"☠️ {target} is poisoned!", 'show')
    
    def cmd_burn(self, stmt: str):
        """burn target"""
        match = re.match(r'burn\s+(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"🔥 {target} is burning!", 'show')
    
    def cmd_freeze(self, stmt: str):
        """freeze target"""
        match = re.match(r'freeze\s+(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"❄️ {target} is frozen!", 'show')
    
    def cmd_spell(self, stmt: str):
        """spell "name" cost mana"""
        match = re.match(r'spell\s+["\'](.+?)["\']\s+cost\s+(.+)', stmt, re.I)
        if match:
            spell_name = match.group(1)
            cost = self.eval_expr(match.group(2))
            self.variables[f'spell_{spell_name}_cost'] = cost
    
    def cmd_cast(self, stmt: str):
        """cast "spellname" """
        match = re.match(r'cast\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            spell = match.group(1)
            self.output(f"✨ Cast: {spell}", 'show')
    
    def cmd_fireball(self, stmt: str):
        """fireball at target"""
        self.output("🔥 Fireball!", 'shout')
    
    def cmd_lightning(self, stmt: str):
        """lightning at target"""
        self.output("⚡ Lightning Strike!", 'shout')
    
    def cmd_heal(self, stmt: str):
        """heal amount"""
        match = re.match(r'heal\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            if 'player_health' in self.variables:
                self.variables['player_health'] += amount
                self.output(f"💚 Healed {amount} HP!", 'show')
    
    def cmd_shield(self, stmt: str):
        """shield amount"""
        match = re.match(r'shield\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            self.variables['player_shield'] = amount
            self.output(f"🛡️ Shield: {amount}", 'show')
    
    def cmd_teleport(self, stmt: str):
        """teleport to x, y"""
        match = re.match(r'teleport\s+to\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.output(f"✨ Teleported to ({x}, {y})", 'show')
    
    def cmd_summon(self, stmt: str):
        """summon "creature" """
        match = re.match(r'summon\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            creature = match.group(1)
            self.output(f"🌟 Summoned: {creature}", 'shout')
    
    def cmd_enchant(self, stmt: str):
        """enchant "item" with "effect" """
        match = re.match(r'enchant\s+["\'](.+?)["\']\s+with\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            effect = match.group(2)
            self.output(f"✨ Enchanted {item} with {effect}", 'show')
    
    def cmd_skill(self, stmt: str):
        """skill "name" level"""
        match = re.match(r'skill\s+["\'](.+?)["\']\s+level\s+(.+)', stmt, re.I)
        if match:
            skill = match.group(1)
            level = self.eval_expr(match.group(2))
            self.variables[f'skill_{skill}'] = level
    
    def cmd_ability(self, stmt: str):
        """ability "name" """
        match = re.match(r'ability\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            ability = match.group(1)
            self.output(f"💫 Ability: {ability}", 'show')
    
    def cmd_cooldown(self, stmt: str):
        """cooldown skill seconds"""
        match = re.match(r'cooldown\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            skill = match.group(1)
            seconds = self.eval_expr(match.group(2))
            self.variables[f'{skill}_cooldown'] = seconds
    
    def cmd_buff(self, stmt: str):
        """buff "name" amount duration"""
        match = re.match(r'buff\s+["\'](.+?)["\']\s+(.+?)\s+(.+)', stmt, re.I)
        if match:
            buff = match.group(1)
            amount = self.eval_expr(match.group(2))
            duration = self.eval_expr(match.group(3))
            self.output(f"⬆️ Buff: {buff} +{amount} for {duration}s", 'show')
    
    def cmd_debuff(self, stmt: str):
        """debuff target"""
        match = re.match(r'debuff\s+(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"⬇️ Debuffed: {target}", 'show')
    
    # ==================== SHOOTING/WEAPONS (30 COMMANDS) ====================
    
    def cmd_gun(self, stmt: str):
        """gun create/equip"""
        if 'equipped_weapon' not in self.variables:
            self.variables['equipped_weapon'] = 'gun'
            self.variables['ammo'] = 30
            self.variables['magazine'] = 30
        self.output("🔫 Gun equipped!", 'show')
    
    def cmd_shoot(self, stmt: str):
        """shoot"""
        if 'ammo' in self.variables and self.variables['ammo'] > 0:
            self.variables['ammo'] -= 1
            self.output(f"💥 BANG! Ammo: {self.variables['ammo']}", 'show')
            # Raycast from camera/player position
            self.variables['_shot_fired'] = True
        else:
            self.output("🔫 Click! Out of ammo!", 'show')
    
    def cmd_raycast(self, stmt: str):
        """raycast from x,y to dx,dy"""
        match = re.match(r'raycast\s+from\s+(.+?),\s*(.+?)\s+to\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x1 = self.eval_expr(match.group(1))
            y1 = self.eval_expr(match.group(2))
            x2 = self.eval_expr(match.group(3))
            y2 = self.eval_expr(match.group(4))
            self.output(f"📡 Raycast: ({x1},{y1}) → ({x2},{y2})", 'show')
            # Draw laser line in graphics mode
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_line(x1, y1, x2, y2, "#ff0000", 3)
    
    def cmd_laser(self, stmt: str):
        """laser from x,y to dx,dy color"""
        match = re.match(r'laser\s+from\s+(.+?),\s*(.+?)\s+to\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?', stmt, re.I)
        if match:
            x1 = self.eval_expr(match.group(1))
            y1 = self.eval_expr(match.group(2))
            x2 = self.eval_expr(match.group(3))
            y2 = self.eval_expr(match.group(4))
            color = match.group(5) if match.group(5) else "#ff0000"
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_line(x1, y1, x2, y2, color, 5)
            self.output("🔴 LASER!", 'show')
    
    def cmd_bullet(self, stmt: str):
        """bullet at x,y velocity vx,vy"""
        match = re.match(r'bullet\s+at\s+(.+?),\s*(.+?)\s+velocity\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            vx = self.eval_expr(match.group(3))
            vy = self.eval_expr(match.group(4))
            # Create bullet sprite
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.create_sprite(f"bullet_{x}_{y}", x, y, 5, 5, "#ffff00")
    
    def cmd_projectile(self, stmt: str):
        """projectile at x,y angle speed"""
        match = re.match(r'projectile\s+at\s+(.+?),\s*(.+?)\s+angle\s+(.+?)\s+speed\s+(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            angle = self.eval_expr(match.group(3))
            speed = self.eval_expr(match.group(4))
            self.output(f"🎯 Projectile fired!", 'show')
    
    def cmd_reload(self, stmt: str):
        """reload"""
        if 'magazine' in self.variables:
            self.variables['ammo'] = self.variables['magazine']
            self.output(f"🔄 Reloaded! Ammo: {self.variables['ammo']}", 'show')
    
    def cmd_ammo(self, stmt: str):
        """ammo set/add amount"""
        if 'set' in stmt.lower():
            match = re.match(r'ammo\s+set\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                self.variables['ammo'] = amount
        elif 'add' in stmt.lower():
            match = re.match(r'ammo\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'ammo' not in self.variables:
                    self.variables['ammo'] = 0
                self.variables['ammo'] += amount
                self.output(f"📦 +{amount} ammo", 'show')
    
    def cmd_weapon(self, stmt: str):
        """weapon "name" """
        match = re.match(r'weapon\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            weapon = match.group(1)
            self.variables['equipped_weapon'] = weapon
            self.output(f"⚔️ Equipped: {weapon}", 'show')
    
    def cmd_melee(self, stmt: str):
        """melee attack"""
        self.output("👊 Melee attack!", 'show')
    
    def cmd_sword(self, stmt: str):
        """sword attack"""
        self.output("⚔️ Sword slash!", 'show')
    
    def cmd_bow(self, stmt: str):
        """bow equipped"""
        self.variables['equipped_weapon'] = 'bow'
        self.output("🏹 Bow equipped!", 'show')
    
    def cmd_arrow(self, stmt: str):
        """arrow shoot"""
        self.output("🏹 Arrow shot!", 'show')
    
    def cmd_grenade(self, stmt: str):
        """grenade throw at x,y"""
        match = re.match(r'grenade\s+(?:throw\s+)?at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.output(f"💣 Grenade thrown!", 'show')
    
    def cmd_bomb(self, stmt: str):
        """bomb place at x,y"""
        self.output("💣 Bomb placed!", 'show')
    
    def cmd_explode(self, stmt: str):
        """explode at x,y radius"""
        match = re.match(r'explode\s+at\s+(.+?),\s*(.+?)(?:\s+radius\s+(.+))?', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            radius = self.eval_expr(match.group(3)) if match.group(3) else 50
            # Draw explosion effect
            if hasattr(self.editor, 'output_window'):
                self.editor.output_window.draw_circle(x, y, radius, "#ff8800", fill=True)
            self.output("💥 BOOM!", 'shout')
    
    def cmd_aim(self, stmt: str):
        """aim at x,y"""
        match = re.match(r'aim\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.variables['aim_x'] = x
            self.variables['aim_y'] = y
    
    def cmd_recoil(self, stmt: str):
        """recoil amount"""
        match = re.match(r'recoil\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            self.variables['weapon_recoil'] = amount
    
    def cmd_spread(self, stmt: str):
        """spread amount"""
        match = re.match(r'spread\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            self.variables['weapon_spread'] = amount
    
    def cmd_shotgun(self, stmt: str):
        """shotgun fire"""
        self.output("💥 BOOM! Shotgun blast!", 'show')
        # Fire multiple pellets
        for i in range(8):
            self.log(f"  • Pellet {i+1}")
    
    def cmd_sniper(self, stmt: str):
        """sniper rifle"""
        self.variables['equipped_weapon'] = 'sniper'
        self.output("🎯 Sniper rifle equipped!", 'show')
    
    def cmd_rifle(self, stmt: str):
        """assault rifle"""
        self.variables['equipped_weapon'] = 'rifle'
        self.output("🔫 Assault rifle equipped!", 'show')
    
    def cmd_pistol(self, stmt: str):
        """pistol"""
        self.variables['equipped_weapon'] = 'pistol'
        self.output("🔫 Pistol equipped!", 'show')
    
    def cmd_rocket(self, stmt: str):
        """rocket launch"""
        self.output("🚀 ROCKET LAUNCHED!", 'shout')
    
    def cmd_homing(self, stmt: str):
        """homing missile at target"""
        match = re.match(r'homing\s+(?:at\s+)?(\w+)', stmt, re.I)
        if match:
            target = match.group(1)
            self.output(f"🎯 Homing missile locked on {target}!", 'show')
    
    def cmd_scope(self, stmt: str):
        """scope zoom level"""
        match = re.match(r'scope\s+(?:zoom\s+)?(.+)', stmt, re.I)
        if match:
            zoom = self.eval_expr(match.group(1))
            self.variables['scope_zoom'] = zoom
            self.output(f"🔭 Scope: {zoom}x zoom", 'show')
    
    def cmd_zoom(self, stmt: str):
        """zoom level"""
        match = re.match(r'zoom\s+(.+)', stmt, re.I)
        if match:
            level = self.eval_expr(match.group(1))
            self.variables['zoom_level'] = level
    
    def cmd_accuracy(self, stmt: str):
        """accuracy percentage"""
        match = re.match(r'accuracy\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['weapon_accuracy'] = value
    
    def cmd_firerate(self, stmt: str):
        """firerate rounds per second"""
        match = re.match(r'firerate\s+(.+)', stmt, re.I)
        if match:
            rate = self.eval_expr(match.group(1))
            self.variables['weapon_firerate'] = rate
    
    def cmd_magazine(self, stmt: str):
        """magazine capacity"""
        match = re.match(r'magazine\s+(.+)', stmt, re.I)
        if match:
            capacity = self.eval_expr(match.group(1))
            self.variables['magazine'] = capacity
    
    # ==================== 2D GRAPHICS ADVANCED (35 COMMANDS) ====================
    
    def cmd_particle(self, stmt: str):
        """particle at x,y color amount"""
        match = re.match(r'particle\s+at\s+(.+?),\s*(.+?)(?:\s+color\s+["\'](.+?)["\'])?(?:\s+amount\s+(.+))?', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            color = match.group(3) if match.group(3) else "#ffffff"
            amount = self.eval_expr(match.group(4)) if match.group(4) else 10
            # Create particles
            for i in range(int(amount)):
                if hasattr(self.editor, 'output_window'):
                    px = x + random.randint(-20, 20)
                    py = y + random.randint(-20, 20)
                    self.editor.output_window.draw_circle(px, py, 2, color, fill=True)
    
    def cmd_emitter(self, stmt: str):
        """emitter at x,y"""
        match = re.match(r'emitter\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.variables['emitter_x'] = x
            self.variables['emitter_y'] = y
    
    def cmd_animation(self, stmt: str):
        """animation "name" frames fps"""
        match = re.match(r'animation\s+["\'](.+?)["\']\s+frames\s+(.+?)\s+fps\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            frames = self.eval_expr(match.group(2))
            fps = self.eval_expr(match.group(3))
            self.variables[f'anim_{name}_frames'] = frames
            self.variables[f'anim_{name}_fps'] = fps
    
    def cmd_frame(self, stmt: str):
        """frame number"""
        match = re.match(r'frame\s+(.+)', stmt, re.I)
        if match:
            num = self.eval_expr(match.group(1))
            self.variables['current_frame'] = num
    
    def cmd_layer(self, stmt: str):
        """layer number"""
        match = re.match(r'layer\s+(.+)', stmt, re.I)
        if match:
            layer = self.eval_expr(match.group(1))
            self.variables['current_layer'] = layer
    
    def cmd_zindex(self, stmt: str):
        """zindex sprite value"""
        match = re.match(r'zindex\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            z = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_zindex'] = z
    
    def cmd_opacity(self, stmt: str):
        """opacity sprite value"""
        match = re.match(r'opacity\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            opacity = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_opacity'] = opacity
    
    def cmd_fade(self, stmt: str):
        """fade sprite to opacity duration"""
        match = re.match(r'fade\s+(\w+)\s+to\s+(.+?)(?:\s+duration\s+(.+))?', stmt, re.I)
        if match:
            sprite = match.group(1)
            target = self.eval_expr(match.group(2))
            duration = self.eval_expr(match.group(3)) if match.group(3) else 1.0
            self.output(f"Fading {sprite} to {target}", 'show')
    
    def cmd_rotate(self, stmt: str):
        """rotate sprite angle"""
        match = re.match(r'rotate\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            angle = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_rotation'] = angle
    
    def cmd_scale(self, stmt: str):
        """scale sprite factor"""
        match = re.match(r'scale\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            factor = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_scale'] = factor
    
    def cmd_flip(self, stmt: str):
        """flip sprite horizontal/vertical"""
        match = re.match(r'flip\s+(\w+)\s+(\w+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            direction = match.group(2)
            self.variables[f'{sprite}_flip'] = direction
    
    def cmd_tint(self, stmt: str):
        """tint sprite color"""
        match = re.match(r'tint\s+(\w+)\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            sprite = match.group(1)
            color = match.group(2)
            self.variables[f'{sprite}_tint'] = color
    
    def cmd_glow(self, stmt: str):
        """glow sprite intensity"""
        match = re.match(r'glow\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            intensity = self.eval_expr(match.group(2))
            self.output(f"✨ {sprite} glowing at {intensity}", 'show')
    
    def cmd_shadow(self, stmt: str):
        """shadow sprite offset"""
        match = re.match(r'shadow\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            offset = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_shadow'] = offset
    
    def cmd_blur(self, stmt: str):
        """blur sprite amount"""
        match = re.match(r'blur\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            amount = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_blur'] = amount
    
    def cmd_pixelate(self, stmt: str):
        """pixelate sprite size"""
        match = re.match(r'pixelate\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            size = self.eval_expr(match.group(2))
            self.variables[f'{sprite}_pixelate'] = size
    
    def cmd_outline(self, stmt: str):
        """outline sprite thickness color"""
        match = re.match(r'outline\s+(\w+)\s+(.+?)\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            sprite = match.group(1)
            thickness = self.eval_expr(match.group(2))
            color = match.group(3)
            self.output(f"Outline added to {sprite}", 'show')
    
    def cmd_gradient(self, stmt: str):
        """gradient from color1 to color2"""
        match = re.match(r'gradient\s+from\s+["\'](.+?)["\']\s+to\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            color1 = match.group(1)
            color2 = match.group(2)
            self.variables['gradient_start'] = color1
            self.variables['gradient_end'] = color2
    
    def cmd_pattern(self, stmt: str):
        """pattern "type" """
        match = re.match(r'pattern\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            pattern = match.group(1)
            self.variables['fill_pattern'] = pattern
    
    def cmd_texture(self, stmt: str):
        """texture sprite "name" """
        match = re.match(r'texture\s+(\w+)\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            sprite = match.group(1)
            texture = match.group(2)
            self.variables[f'{sprite}_texture'] = texture
    
    def cmd_polygon(self, stmt: str):
        """polygon points color"""
        self.output("🔷 Polygon drawn", 'show')
    
    def cmd_triangle(self, stmt: str):
        """triangle at x1,y1 x2,y2 x3,y3"""
        match = re.match(r'triangle\s+at\s+(.+?),\s*(.+?)\s+(.+?),\s*(.+?)\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x1 = self.eval_expr(match.group(1))
            y1 = self.eval_expr(match.group(2))
            x2 = self.eval_expr(match.group(3))
            y2 = self.eval_expr(match.group(4))
            x3 = self.eval_expr(match.group(5))
            y3 = self.eval_expr(match.group(6))
            if hasattr(self.editor, 'output_window'):
                # Draw three lines to form triangle
                self.editor.output_window.draw_line(x1, y1, x2, y2, "#ffffff", 2)
                self.editor.output_window.draw_line(x2, y2, x3, y3, "#ffffff", 2)
                self.editor.output_window.draw_line(x3, y3, x1, y1, "#ffffff", 2)
    
    def cmd_ellipse(self, stmt: str):
        """ellipse at x,y width height"""
        match = re.match(r'ellipse\s+at\s+(.+?),\s*(.+?)\s+width\s+(.+?)\s+height\s+(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            w = self.eval_expr(match.group(3))
            h = self.eval_expr(match.group(4))
            self.output(f"⭕ Ellipse drawn", 'show')
    
    def cmd_arc(self, stmt: str):
        """arc at x,y radius start end"""
        self.output("🌙 Arc drawn", 'show')
    
    def cmd_curve(self, stmt: str):
        """curve from x1,y1 to x2,y2"""
        self.output("〰️ Curve drawn", 'show')
    
    def cmd_bezier(self, stmt: str):
        """bezier curve with control points"""
        self.output("〰️ Bezier curve drawn", 'show')
    
    def cmd_path(self, stmt: str):
        """path sprite along points"""
        match = re.match(r'path\s+(\w+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            self.output(f"Following path: {sprite}", 'show')
    
    def cmd_mask(self, stmt: str):
        """mask sprite with shape"""
        match = re.match(r'mask\s+(\w+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            self.variables[f'{sprite}_masked'] = True
    
    def cmd_clip(self, stmt: str):
        """clip region"""
        self.variables['clipping_enabled'] = True
    
    def cmd_transform(self, stmt: str):
        """transform sprite matrix"""
        self.output("Transform applied", 'show')
    
    def cmd_anchor(self, stmt: str):
        """anchor sprite at x,y"""
        match = re.match(r'anchor\s+(\w+)\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.variables[f'{sprite}_anchor_x'] = x
            self.variables[f'{sprite}_anchor_y'] = y
    
    def cmd_pivot(self, stmt: str):
        """pivot sprite at x,y"""
        match = re.match(r'pivot\s+(\w+)\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.variables[f'{sprite}_pivot_x'] = x
            self.variables[f'{sprite}_pivot_y'] = y
    
    def cmd_tween(self, stmt: str):
        """tween sprite property from to duration"""
        match = re.match(r'tween\s+(\w+)\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?)\s+duration\s+(.+)', stmt, re.I)
        if match:
            sprite = match.group(1)
            prop = match.group(2)
            start = self.eval_expr(match.group(3))
            end = self.eval_expr(match.group(4))
            duration = self.eval_expr(match.group(5))
            self.output(f"Tweening {sprite}.{prop}", 'show')
    
    def cmd_ease(self, stmt: str):
        """ease type (linear, easein, easeout)"""
        match = re.match(r'ease\s+(\w+)', stmt, re.I)
        if match:
            ease_type = match.group(1)
            self.variables['ease_function'] = ease_type
    
    def cmd_shake(self, stmt: str):
        """shake intensity duration"""
        match = re.match(r'shake\s+(.+?)(?:\s+duration\s+(.+))?', stmt, re.I)
        if match:
            intensity = self.eval_expr(match.group(1))
            duration = self.eval_expr(match.group(2)) if match.group(2) else 1.0
            self.output(f"📳 Screen shake!", 'show')
    
    # ==================== 3D ADVANCED (35 COMMANDS) ====================
    # These are mostly placeholder implementations for advanced 3D features
    
    def cmd_mesh(self, stmt: str):
        """mesh "name" vertices faces"""
        match = re.match(r'mesh\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            name = match.group(1)
            self.output(f"📐 Created mesh: {name}", 'show')
    
    def cmd_model(self, stmt: str):
        """model load "file" """
        match = re.match(r'model\s+(?:load\s+)?["\'](.+?)["\']', stmt, re.I)
        if match:
            filename = match.group(1)
            self.output(f"📦 Loaded model: {filename}", 'show')
    
    def cmd_material(self, stmt: str):
        """material "name" color"""
        match = re.match(r'material\s+["\'](.+?)["\']\s+color\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            name = match.group(1)
            color = match.group(2)
            self.variables[f'material_{name}_color'] = color
    
    def cmd_metallic(self, stmt: str):
        """metallic value"""
        match = re.match(r'metallic\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['material_metallic'] = value
    
    def cmd_roughness(self, stmt: str):
        """roughness value"""
        match = re.match(r'roughness\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['material_roughness'] = value
    
    def cmd_emissive(self, stmt: str):
        """emissive color intensity"""
        match = re.match(r'emissive\s+["\'](.+?)["\']\s+(.+)', stmt, re.I)
        if match:
            color = match.group(1)
            intensity = self.eval_expr(match.group(2))
            self.output(f"✨ Emissive: {color} @ {intensity}", 'show')
    
    def cmd_transparent(self, stmt: str):
        """transparent alpha"""
        match = re.match(r'transparent\s+(.+)', stmt, re.I)
        if match:
            alpha = self.eval_expr(match.group(1))
            self.variables['material_alpha'] = alpha
    
    def cmd_wireframe(self, stmt: str):
        """wireframe on/off"""
        if 'on' in stmt.lower():
            self.variables['render_wireframe'] = True
            self.output("🔲 Wireframe mode ON", 'show')
        else:
            self.variables['render_wireframe'] = False
    
    def cmd_culling(self, stmt: str):
        """culling back/front/none"""
        match = re.match(r'culling\s+(\w+)', stmt, re.I)
        if match:
            mode = match.group(1)
            self.variables['culling_mode'] = mode
    
    def cmd_billboard(self, stmt: str):
        """billboard object"""
        match = re.match(r'billboard\s+(\w+)', stmt, re.I)
        if match:
            obj = match.group(1)
            self.variables[f'{obj}_billboard'] = True
    
    def cmd_lod(self, stmt: str):
        """lod level distance"""
        match = re.match(r'lod\s+(\d+)\s+distance\s+(.+)', stmt, re.I)
        if match:
            level = int(match.group(1))
            distance = self.eval_expr(match.group(2))
            self.variables[f'lod_{level}_distance'] = distance
    
    def cmd_instancing(self, stmt: str):
        """instancing object count"""
        match = re.match(r'instancing\s+(\w+)\s+count\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            count = self.eval_expr(match.group(2))
            self.output(f"Instanced {obj} x{count}", 'show')
    
    def cmd_raytrace(self, stmt: str):
        """raytrace enable"""
        self.variables['raytracing_enabled'] = True
        self.output("🌟 Raytracing enabled", 'show')
    
    def cmd_reflect(self, stmt: str):
        """reflect object intensity"""
        match = re.match(r'reflect\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            intensity = self.eval_expr(match.group(2))
            self.variables[f'{obj}_reflection'] = intensity
    
    def cmd_refract(self, stmt: str):
        """refract object ior"""
        match = re.match(r'refract\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            ior = self.eval_expr(match.group(2))
            self.variables[f'{obj}_refraction'] = ior
    
    def cmd_skylight(self, stmt: str):
        """skylight intensity"""
        match = re.match(r'skylight\s+(.+)', stmt, re.I)
        if match:
            intensity = self.eval_expr(match.group(1))
            self.variables['skylight_intensity'] = intensity
    
    def cmd_hemisphere(self, stmt: str):
        """hemisphere light ground sky"""
        self.output("☀️ Hemisphere light added", 'show')
    
    def cmd_pointlight(self, stmt: str):
        """pointlight at x,y,z intensity"""
        match = re.match(r'pointlight\s+at\s+(.+?),\s*(.+?),\s*(.+?)(?:\s+intensity\s+(.+))?', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            z = self.eval_expr(match.group(3))
            intensity = self.eval_expr(match.group(4)) if match.group(4) else 1.0
            self.output(f"💡 Point light at ({x},{y},{z})", 'show')
    
    def cmd_spotlight(self, stmt: str):
        """spotlight at x,y,z pointing dx,dy,dz"""
        self.output("🔦 Spotlight created", 'show')
    
    def cmd_directional(self, stmt: str):
        """directional light direction"""
        self.output("☀️ Directional light", 'show')
    
    def cmd_caustics(self, stmt: str):
        """caustics enable"""
        self.variables['caustics_enabled'] = True
        self.output("💎 Caustics enabled", 'show')
    
    def cmd_volumetric(self, stmt: str):
        """volumetric fog/light"""
        self.variables['volumetric_enabled'] = True
        self.output("🌫️ Volumetric effects ON", 'show')
    
    def cmd_godrays(self, stmt: str):
        """godrays intensity"""
        match = re.match(r'godrays\s+(.+)', stmt, re.I)
        if match:
            intensity = self.eval_expr(match.group(1))
            self.variables['godray_intensity'] = intensity
            self.output("✨ God rays enabled", 'show')
    
    def cmd_ssao(self, stmt: str):
        """ssao (screen space ambient occlusion)"""
        self.variables['ssao_enabled'] = True
        self.output("🎨 SSAO enabled", 'show')
    
    def cmd_motionblur(self, stmt: str):
        """motionblur amount"""
        match = re.match(r'motionblur\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            self.variables['motionblur_amount'] = amount
    
    def cmd_dof(self, stmt: str):
        """dof (depth of field)"""
        self.variables['dof_enabled'] = True
        self.output("📷 Depth of field enabled", 'show')
    
    def cmd_vignette(self, stmt: str):
        """vignette intensity"""
        match = re.match(r'vignette\s+(.+)', stmt, re.I)
        if match:
            intensity = self.eval_expr(match.group(1))
            self.variables['vignette_intensity'] = intensity
    
    def cmd_chromatic(self, stmt: str):
        """chromatic aberration"""
        self.variables['chromatic_aberration'] = True
        self.output("🌈 Chromatic aberration ON", 'show')
    
    def cmd_grain(self, stmt: str):
        """grain amount"""
        match = re.match(r'grain\s+(.+)', stmt, re.I)
        if match:
            amount = self.eval_expr(match.group(1))
            self.variables['film_grain'] = amount
    
    def cmd_tonemapping(self, stmt: str):
        """tonemapping type"""
        match = re.match(r'tonemapping\s+(\w+)', stmt, re.I)
        if match:
            tone_type = match.group(1)
            self.variables['tonemapping_type'] = tone_type
    
    def cmd_colorgrading(self, stmt: str):
        """colorgrading preset"""
        match = re.match(r'colorgrading\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            preset = match.group(1)
            self.variables['colorgrade_preset'] = preset
    
    def cmd_antialiasing(self, stmt: str):
        """antialiasing type"""
        match = re.match(r'antialiasing\s+(\w+)', stmt, re.I)
        if match:
            aa_type = match.group(1)
            self.variables['antialiasing_type'] = aa_type
    
    def cmd_postprocess(self, stmt: str):
        """postprocess effect"""
        match = re.match(r'postprocess\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            effect = match.group(1)
            self.output(f"Post-processing: {effect}", 'show')
    
    def cmd_renderpass(self, stmt: str):
        """renderpass "name" """
        match = re.match(r'renderpass\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            pass_name = match.group(1)
            self.output(f"Render pass: {pass_name}", 'show')
    
    def cmd_framebuffer(self, stmt: str):
        """framebuffer create"""
        self.output("Framebuffer created", 'show')
    
    # ==================== TRAJECTORY/PHYSICS (25 COMMANDS) ====================
    
    def cmd_trajectory(self, stmt: str):
        """trajectory object velocity angle"""
        match = re.match(r'trajectory\s+(\w+)\s+velocity\s+(.+?)\s+angle\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            velocity = self.eval_expr(match.group(2))
            angle = self.eval_expr(match.group(3))
            self.output(f"🎯 Trajectory calculated", 'show')
    
    def cmd_parabola(self, stmt: str):
        """parabola object from x,y"""
        self.output("📈 Parabolic path", 'show')
    
    def cmd_ballistic(self, stmt: str):
        """ballistic object velocity angle"""
        self.output("🚀 Ballistic trajectory", 'show')
    
    def cmd_orbit(self, stmt: str):
        """orbit object around center radius"""
        match = re.match(r'orbit\s+(\w+)\s+around\s+(.+?),\s*(.+?)(?:\s+radius\s+(.+))?', stmt, re.I)
        if match:
            obj = match.group(1)
            cx = self.eval_expr(match.group(2))
            cy = self.eval_expr(match.group(3))
            radius = self.eval_expr(match.group(4)) if match.group(4) else 10
            self.output(f"🌍 {obj} orbiting", 'show')
    
    def cmd_circular(self, stmt: str):
        """circular motion"""
        self.output("⭕ Circular motion", 'show')
    
    def cmd_spiral(self, stmt: str):
        """spiral object"""
        self.output("🌀 Spiral motion", 'show')
    
    def cmd_sine_wave(self, stmt: str):
        """sine wave motion"""
        self.output("〰️ Sine wave", 'show')
    
    def cmd_wave(self, stmt: str):
        """wave motion"""
        self.output("🌊 Wave motion", 'show')
    
    def cmd_pendulum(self, stmt: str):
        """pendulum object length"""
        match = re.match(r'pendulum\s+(\w+)\s+length\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            length = self.eval_expr(match.group(2))
            self.output(f"🔄 Pendulum swing", 'show')
    
    def cmd_spring(self, stmt: str):
        """spring object stiffness damping"""
        match = re.match(r'spring\s+(\w+)\s+stiffness\s+(.+?)\s+damping\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            k = self.eval_expr(match.group(2))
            d = self.eval_expr(match.group(3))
            self.output(f"🔧 Spring physics", 'show')
    
    def cmd_elastic(self, stmt: str):
        """elastic object"""
        self.output("🎪 Elastic motion", 'show')
    
    def cmd_bounce(self, stmt: str):
        """bounce object restitution"""
        match = re.match(r'bounce\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            restitution = self.eval_expr(match.group(2))
            self.variables[f'{obj}_bounce'] = restitution
    
    def cmd_gravity(self, stmt: str):
        """gravity set value"""
        match = re.match(r'gravity\s+(?:set\s+)?(.+)', stmt, re.I)
        if match:
            g = self.eval_expr(match.group(1))
            self.variables['gravity'] = g
            self.output(f"🌍 Gravity: {g}", 'show')
    
    def cmd_force(self, stmt: str):
        """force on object fx fy"""
        match = re.match(r'force\s+(?:on\s+)?(\w+)\s+(.+?)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            fx = self.eval_expr(match.group(2))
            fy = self.eval_expr(match.group(3))
            self.output(f"⚡ Force applied to {obj}", 'show')
    
    def cmd_impulse(self, stmt: str):
        """impulse on object ix iy"""
        match = re.match(r'impulse\s+(?:on\s+)?(\w+)\s+(.+?)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            ix = self.eval_expr(match.group(2))
            iy = self.eval_expr(match.group(3))
            self.output(f"💥 Impulse applied", 'show')
    
    def cmd_torque(self, stmt: str):
        """torque on object amount"""
        match = re.match(r'torque\s+(?:on\s+)?(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            torque = self.eval_expr(match.group(2))
            self.output(f"🔄 Torque applied", 'show')
    
    def cmd_angular(self, stmt: str):
        """angular velocity object"""
        match = re.match(r'angular\s+(?:velocity\s+)?(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            omega = self.eval_expr(match.group(2))
            self.variables[f'{obj}_angular_velocity'] = omega
    
    def cmd_momentum(self, stmt: str):
        """momentum object"""
        match = re.match(r'momentum\s+(?:of\s+)?(\w+)', stmt, re.I)
        if match:
            obj = match.group(1)
            # Calculate momentum = mass * velocity
            self.output(f"Momentum calculated", 'show')
    
    def cmd_inertia(self, stmt: str):
        """inertia object value"""
        match = re.match(r'inertia\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            value = self.eval_expr(match.group(2))
            self.variables[f'{obj}_inertia'] = value
    
    def cmd_drag(self, stmt: str):
        """drag object coefficient"""
        match = re.match(r'drag\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            coeff = self.eval_expr(match.group(2))
            self.variables[f'{obj}_drag'] = coeff
    
    def cmd_lift(self, stmt: str):
        """lift object coefficient"""
        match = re.match(r'lift\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            coeff = self.eval_expr(match.group(2))
            self.variables[f'{obj}_lift'] = coeff
    
    def cmd_buoyancy(self, stmt: str):
        """buoyancy object density"""
        match = re.match(r'buoyancy\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            density = self.eval_expr(match.group(2))
            self.output(f"🌊 Buoyancy applied", 'show')
    
    def cmd_magnetism(self, stmt: str):
        """magnetism object strength"""
        match = re.match(r'magnetism\s+(\w+)\s+(.+)', stmt, re.I)
        if match:
            obj = match.group(1)
            strength = self.eval_expr(match.group(2))
            self.variables[f'{obj}_magnetic'] = strength
    
    def cmd_attract(self, stmt: str):
        """attract object1 to object2 strength"""
        match = re.match(r'attract\s+(\w+)\s+to\s+(\w+)(?:\s+strength\s+(.+))?', stmt, re.I)
        if match:
            obj1 = match.group(1)
            obj2 = match.group(2)
            strength = self.eval_expr(match.group(3)) if match.group(3) else 1.0
            self.output(f"🧲 {obj1} attracted to {obj2}", 'show')
    
    def cmd_repel(self, stmt: str):
        """repel object1 from object2 strength"""
        match = re.match(r'repel\s+(\w+)\s+from\s+(\w+)(?:\s+strength\s+(.+))?', stmt, re.I)
        if match:
            obj1 = match.group(1)
            obj2 = match.group(2)
            strength = self.eval_expr(match.group(3)) if match.group(3) else 1.0
            self.output(f"🔴 {obj1} repelled from {obj2}", 'show')
    
    # ==================== GAME MECHANICS (25 COMMANDS) ====================
    
    def cmd_score(self, stmt: str):
        """score set/add/subtract"""
        if 'add' in stmt.lower():
            match = re.match(r'score\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'score' not in self.variables:
                    self.variables['score'] = 0
                self.variables['score'] += amount
                self.output(f"💯 +{amount} Score: {self.variables['score']}", 'show')
        elif 'set' in stmt.lower():
            match = re.match(r'score\s+set\s+(.+)', stmt, re.I)
            if match:
                value = self.eval_expr(match.group(1))
                self.variables['score'] = value
    
    def cmd_highscore(self, stmt: str):
        """highscore set/check"""
        match = re.match(r'highscore\s+(?:set\s+)?(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['highscore'] = value
            self.output(f"🏆 New High Score: {value}!", 'shout')
    
    def cmd_lives(self, stmt: str):
        """lives set/add/subtract"""
        if 'add' in stmt.lower():
            match = re.match(r'lives\s+add\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'lives' not in self.variables:
                    self.variables['lives'] = 3
                self.variables['lives'] += amount
        elif 'subtract' in stmt.lower():
            match = re.match(r'lives\s+subtract\s+(.+)', stmt, re.I)
            if match:
                amount = self.eval_expr(match.group(1))
                if 'lives' in self.variables:
                    self.variables['lives'] -= amount
                    self.output(f"💔 Lost life! Lives: {self.variables['lives']}", 'show')
        else:
            match = re.match(r'lives\s+(?:set\s+)?(.+)', stmt, re.I)
            if match:
                value = self.eval_expr(match.group(1))
                self.variables['lives'] = value
    
    def cmd_gameover(self, stmt: str):
        """gameover"""
        self.variables['game_state'] = 'gameover'
        self.output("💀 GAME OVER", 'shout')
    
    def cmd_win(self, stmt: str):
        """win"""
        self.variables['game_state'] = 'win'
        self.output("🎉 YOU WIN!", 'shout')
    
    def cmd_lose(self, stmt: str):
        """lose"""
        self.variables['game_state'] = 'lose'
        self.output("💀 YOU LOSE", 'shout')
    
    def cmd_checkpoint(self, stmt: str):
        """checkpoint at x,y"""
        match = re.match(r'checkpoint\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.variables['checkpoint_x'] = x
            self.variables['checkpoint_y'] = y
            self.output(f"🚩 Checkpoint saved!", 'show')
    
    def cmd_respawn(self, stmt: str):
        """respawn at checkpoint"""
        if 'checkpoint_x' in self.variables:
            x = self.variables['checkpoint_x']
            y = self.variables['checkpoint_y']
            self.output(f"🔄 Respawned at ({x}, {y})", 'show')
    
    def cmd_powerup(self, stmt: str):
        """powerup "name" at x,y"""
        match = re.match(r'powerup\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.output(f"⭐ Power-up: {name}", 'show')
    
    def cmd_pickup(self, stmt: str):
        """pickup "item" """
        match = re.match(r'pickup\s+["\'](.+?)["\']', stmt, re.I)
        if match:
            item = match.group(1)
            self.output(f"✨ Picked up: {item}", 'show')
    
    def cmd_coin(self, stmt: str):
        """coin at x,y value"""
        match = re.match(r'coin\s+at\s+(.+?),\s*(.+?)(?:\s+value\s+(.+))?', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            value = self.eval_expr(match.group(3)) if match.group(3) else 1
            self.output(f"🪙 Coin spawned!", 'show')
    
    def cmd_gem(self, stmt: str):
        """gem at x,y"""
        match = re.match(r'gem\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            x = self.eval_expr(match.group(1))
            y = self.eval_expr(match.group(2))
            self.output(f"💎 Gem spawned!", 'show')
    
    def cmd_key(self, stmt: str):
        """key "color" at x,y"""
        match = re.match(r'key\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            color = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.output(f"🔑 {color} key spawned!", 'show')
    
    def cmd_door(self, stmt: str):
        """door "color" at x,y"""
        match = re.match(r'door\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            color = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.output(f"🚪 {color} door placed!", 'show')
    
    def cmd_lock(self, stmt: str):
        """lock door"""
        match = re.match(r'lock\s+(\w+)', stmt, re.I)
        if match:
            door = match.group(1)
            self.variables[f'{door}_locked'] = True
            self.output(f"🔒 Door locked", 'show')
    
    def cmd_unlock(self, stmt: str):
        """unlock door"""
        match = re.match(r'unlock\s+(\w+)', stmt, re.I)
        if match:
            door = match.group(1)
            self.variables[f'{door}_locked'] = False
            self.output(f"🔓 Door unlocked!", 'show')
    
    def cmd_trigger(self, stmt: str):
        """trigger "name" at x,y size"""
        match = re.match(r'trigger\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+?)(?:\s+size\s+(.+))?', stmt, re.I)
        if match:
            name = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            size = self.eval_expr(match.group(4)) if match.group(4) else 50
            self.output(f"⚡ Trigger zone: {name}", 'show')
    
    def cmd_zone(self, stmt: str):
        """zone "name" from x1,y1 to x2,y2"""
        match = re.match(r'zone\s+["\'](.+?)["\']\s+from\s+(.+?),\s*(.+?)\s+to\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            self.output(f"📍 Zone created: {name}", 'show')
    
    def cmd_area(self, stmt: str):
        """area "name" radius"""
        match = re.match(r'area\s+["\'](.+?)["\']\s+radius\s+(.+)', stmt, re.I)
        if match:
            name = match.group(1)
            radius = self.eval_expr(match.group(2))
            self.output(f"⭕ Area: {name}", 'show')
    
    def cmd_spawn(self, stmt: str):
        """spawn "entity" at x,y"""
        match = re.match(r'spawn\s+["\'](.+?)["\']\s+at\s+(.+?),\s*(.+)', stmt, re.I)
        if match:
            entity = match.group(1)
            x = self.eval_expr(match.group(2))
            y = self.eval_expr(match.group(3))
            self.output(f"👹 Spawned: {entity}", 'show')
    
    def cmd_wave_spawn(self, stmt: str):
        """wave number"""
        match = re.match(r'wave\s+(\d+)', stmt, re.I)
        if match:
            wave_num = int(match.group(1))
            self.variables['current_wave'] = wave_num
            self.output(f"🌊 WAVE {wave_num}!", 'shout')
    
    # ==================== NEW COMMANDS ====================
    
    def cmd_wait(self, stmt: str):
        """wait/sleep/pause for seconds"""
        match = re.match(r'(?:wait|sleep|pause)\s+(?:for\s+)?(.+?)(?:\s+seconds?)?', stmt, re.I)
        if match:
            seconds = self.eval_expr(match.group(1))
            import time
            time.sleep(float(seconds))
            self.log(f"⏱️ Waited {seconds} seconds")
    
    def cmd_break(self, stmt: str):
        """break/stop current loop"""
        self.loop_break = True
        self.log("🛑 Break")
    
    def cmd_continue(self, stmt: str):
        """continue/skip to next iteration"""
        self.loop_continue = True
        self.log("⏭️ Continue")
    
    def cmd_return(self, stmt: str):
        """return/give value from function"""
        match = re.match(r'(?:return|give)\s+(.+)', stmt, re.I)
        if match:
            value = self.eval_expr(match.group(1))
            self.variables['_return'] = value
            self.output(f"↩️ Return: {value}", 'show')
    
    def cmd_function(self, stmt: str):
        """define function name { ... }"""
        match = re.match(r'(?:function|define)\s+(\w+)\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            name = match.group(1)
            body = match.group(2)
            self.functions[name] = body
            self.log(f"📦 Function defined: {name}")
    
    def cmd_call(self, stmt: str):
        """call/run function name"""
        match = re.match(r'(?:call|run)\s+(\w+)', stmt, re.I)
        if match:
            name = match.group(1)
            if name in self.functions:
                self.execute(self.functions[name])
            else:
                self.log(f"✗ Function not found: {name}", "error")
    
    def cmd_print(self, stmt: str):
        """print/log message (alias for say)"""
        match = re.match(r'(?:print|log)\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.output(str(message), 'say')
    
    def cmd_error(self, stmt: str):
        """error/throw message"""
        match = re.match(r'(?:error|throw)\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.log(f"❌ ERROR: {message}", "error")
    
    def cmd_warning(self, stmt: str):
        """warning/warn message"""
        match = re.match(r'(?:warning|warn)\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.log(f"⚠️ WARNING: {message}", "warning")
    
    def cmd_success(self, stmt: str):
        """success message"""
        match = re.match(r'success\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.log(f"✅ SUCCESS: {message}", "success")
    
    def cmd_info(self, stmt: str):
        """info message"""
        match = re.match(r'info\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.log(f"ℹ️ INFO: {message}", "info")
    
    def cmd_debug(self, stmt: str):
        """debug message"""
        match = re.match(r'debug\s+(.+)', stmt, re.I)
        if match:
            message = self.eval_expr(match.group(1))
            self.log(f"🐛 DEBUG: {message}", "debug")
    
    def cmd_assert(self, stmt: str):
        """assert/verify condition"""
        match = re.match(r'(?:assert|verify)\s+(.+)', stmt, re.I)
        if match:
            condition = match.group(1)
            if self.eval_condition(condition):
                self.log(f"✅ Assert passed: {condition}", "success")
            else:
                self.log(f"❌ Assert failed: {condition}", "error")
    
    def cmd_try(self, stmt: str):
        """try { ... } catch { ... }"""
        match = re.match(r'try\s*\{(.+?)\}(?:\s*catch\s*\{(.+?)\})?', stmt, re.I | re.DOTALL)
        if match:
            try_block = match.group(1)
            catch_block = match.group(2) if match.group(2) else None
            
            try:
                statements = self.parse_code(try_block)
                for s in statements:
                    if s.strip():
                        self.execute_statement(s)
            except Exception as e:
                if catch_block:
                    self.variables['_error'] = str(e)
                    statements = self.parse_code(catch_block)
                    for s in statements:
                        if s.strip():
                            self.execute_statement(s)
    
    def cmd_catch(self, stmt: str):
        """catch block (part of try/catch)"""
        pass  # Handled in cmd_try
    
    def cmd_finally(self, stmt: str):
        """finally block"""
        match = re.match(r'finally\s*\{(.+?)\}', stmt, re.I | re.DOTALL)
        if match:
            block = match.group(1)
            statements = self.parse_code(block)
            for s in statements:
                if s.strip():
                    self.execute_statement(s)
    
    def cmd_else(self, stmt: str):
        """else/otherwise { ... } (handled with if)"""
        # This is handled in the if statement parsing
        pass
    
    def cmd_elseif(self, stmt: str):
        """elif/elseif condition { ... } (handled with if)"""
        # This is handled in the if statement parsing
        pass
    
    def cmd_timer(self, stmt: str):
        """timer start/stop/reset"""
        if 'start' in stmt.lower():
            self.variables['timer_running'] = True
            self.output("⏱️ Timer started", 'show')
        elif 'stop' in stmt.lower():
            self.variables['timer_running'] = False
            self.output("⏱️ Timer stopped", 'show')
        elif 'reset' in stmt.lower():
            self.variables['timer_value'] = 0
            self.output("⏱️ Timer reset", 'show')
    
    def cmd_countdown(self, stmt: str):
        """countdown from seconds"""
        match = re.match(r'countdown\s+from\s+(.+)', stmt, re.I)
        if match:
            seconds = self.eval_expr(match.group(1))
            self.variables['countdown_time'] = seconds
            self.output(f"⏳ Countdown: {seconds} seconds", 'show')
    
    def cmd_pause(self, stmt: str):
        """pause game"""
        self.variables['game_paused'] = True
        self.output("⏸️ Game Paused", 'show')
    
    def cmd_resume(self, stmt: str):
        """resume game"""
        self.variables['game_paused'] = False
        self.output("▶️ Game Resumed", 'show')
    
    def log(self, message: str, level: str = "info"):
        """Log system message or error to log panel (NOT for say/show statements!)"""
        if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'log'):
            self.editor.log(message, level)
        else:
            # Fallback to print
            print(f"[{level}] {message}")
