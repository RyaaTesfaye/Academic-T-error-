import random

from Settings import *

wave = [
    # WAVE 1
    [
        "boss","gampang", "gampang", "sedang", "gampang", 
        "elite", "sedang", "gampang", "elite"
    ],

    # WAVE 2
    [
        "elite", "elite", "gampang", "gampang", 
        "elite", "elite", "elite", 
        "sedang", "sedang", "elite"
    ],

    # WAVE 3
    [
        "susah", "sedang", "susah", 
        "gampang", "gampang",
        "susah", "susah", "susah"
    ],

    # WAVE 4
    [
        "gampang", "gampang", "gampang", "gampang", "gampang",
        "sedang", "sedang", "sedang",
        "elite", "elite", "elite",
        "susah", "gampang", "susah"
    ],

    # WAVE 
    [
        "sedang", "sedang", 
        "boss", 
        "sedang", "sedang", "elite", "elite"
    ],

    # WAVE 6
    [
        "elite", "susah", "elite", "susah",
        "elite", "susah", "elite", "susah",
        "elite", "elite", "elite"
    ],

    # WAVE 7
    [
        "susah", "susah",
        "boss",
        "gampang", "gampang", "gampang", "gampang", 
        "boss",
        "susah"
    ],

    # WAVE 8
    [
        "gampang", "gampang", "gampang", "gampang",
        "sedang", "sedang", "sedang",
        "elite", "elite", "elite", "elite",
        "susah", "susah", "susah", "susah",
        "boss"
    ],

    # WAVE 9
    [
        "boss", "boss", 
        "susah", "susah", "susah", "susah",
        "elite", "elite", "elite"
    ],

    # WAVE 10
    [
        "gampang", "gampang", "gampang", "gampang", "gampang",
        "boss", "boss", "boss", 
        "susah", "susah", "susah", 
        "elite", "elite", "elite", "elite", 
        "gampang", "gampang", "gampang" 
    ]
]

class wave_managers:
    def __init__(self):
        self.current_wave_idx = 0
        self.spawn_timer = 0
        self.base_spawn_interval = interval_spawn
        self.enemy_queue =  []
        self.is_wave_active = False
        self.is_game_cleared = False
        
        self.start_next_wave()
    
    def start_next_wave(self):
        if self.current_wave_idx < len(wave):
            self.enemy_queue = wave[self.current_wave_idx].copy()
            self.is_wave_active = True
            self.spawn_timer = 1
        else:
            self.is_game_cleared = True
            self.is_wave_active = False
            
    def update(self, dt, active_enemy_count):
        if self.is_game_cleared:
            return
        
        if len(self.enemy_queue) == 0 and active_enemy_count == 0:
            
            if self.is_wave_active:
                self.is_wave_active = False
                self.current_wave_idx += 1
                return "WAVE_CLEARED" 
            
            return None
                    
        if self.is_wave_active and len(self.enemy_queue) > 0:
            self.spawn_timer -= dt
            
            if self.spawn_timer <= 0:
                enemy_type = self.enemy_queue.pop(0)
                
                if enemy_type == "BOSS_SKRIPSI":
                    self.spawn_timer = 3.0
                else:
                    self.spawn_timer = random.uniform(1.5, 2.5)
                return enemy_type
                
        return None
                    
            