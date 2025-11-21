import random

from Settings import *

wave = [
    # WAVE 1
    [
        "sedang", "sedang", "elite", "sedang",
        "elite", "elite", "sedang",
        "susah",
        "elite", "sedang"
    ],

    # WAVE 2
    [
        "elite", "elite", "elite", "elite", 
        "sedang", "sedang", 
        "elite", "elite", "elite", "elite",
        "susah", "susah"
    ],

    # WAVE 3
    [
        "susah", "gampang", "susah", 
        "susah", "susah", "susah",
        "sedang", "susah", "susah",
        "elite", "elite"
    ],

    # WAVE 4
    [
        "gampang", "gampang", "gampang", "gampang", 
        "elite", "elite", "elite",
        "susah", "sedang", "susah",
        "elite", "elite", "elite",
        "gampang", "gampang", "gampang"
    ],

    # WAVE 5
    [
        "sedang", "sedang", "sedang",
        "susah", "susah", 
        "boss",
        "elite", "elite", "elite" 
    ],

    # WAVE 6
    [
        "elite", "susah", "elite", "susah",
        "elite", "susah", "elite", "susah",
        "elite", "susah", "elite", "susah",
        "sedang", "sedang"
    ],

    # WAVE 7
    [
        "elite", "gampang", "elite", "gampang",
        "elite", "gampang", "elite", "gampang",
        "elite", "elite", "elite", "elite",
        "elite", "elite", "elite"
    ],

    # WAVE 8
    [
        "susah", "susah", "susah", 
        "elite", "elite", "elite", 
        "sedang", "sedang", "sedang",
        "susah", "susah", "susah",
        "elite", "elite", "elite", 
        "gampang", "gampang", "gampang" 
    ],

    # WAVE 9
    [
        "susah", "elite", "susah", "elite",
        "susah", "elite", "susah", "elite",
        "boss", 
        "susah", "susah"
    ],

    # WAVE 10
    [
        "gampang", "gampang", "gampang", "gampang", "gampang", 
        "susah", "susah", "susah", 
        "boss", 
        "elite", "elite", "elite", 
        "susah", "susah", 
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
                self.spawn_timer = 1
                self.current_wave_idx += 1
            else:
                self.spawn_timer -= dt
                if self.spawn_timer <= 0:
                    self.start_next_wave()
                    
        if self.is_wave_active and len(self.enemy_queue) > 0:
            self.spawn_timer -= dt
            
            if self.spawn_timer <= 0:
                enemy_type = self.enemy_queue.pop(0)
                
                if enemy_type == "BOSS_SKRIPSI":
                    self.spawn_timer = 4.0
                else:
                    self.spawn_timer = random.uniform(1.5, 2.5)
                return enemy_type
                
        return None
                    
            