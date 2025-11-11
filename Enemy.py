import cairo
import math
from Settings import *
import random

enemy_data = {
    "gampang":{
        "word_list": ["NT","WOI", "L" ],
        "speed": 85,
        "radius": 15,
        "shape": "Goblin"
    },
    "sedang":{
        "word_list": ["ERROR","DEBUG","TUGAS" ],
        "speed": 70,
        "radius": 20,
        "shape": "Skeleton"
    },
    "elite":{
        "word_list": ["MATDAS","MATDIS","GRAFKOM" ],
        "speed": 90,
        "radius": 10,
        "shape": "Ahmat"
    },
    "susah":{
        "word_list": ["GABUT","MALES","NGANTUK" ],
        "speed": 40,
        "radius": 23,
        "shape": "Alpin"
    },
    "boss":{
        "word_list": ["METODOLOGI","PENELITIAN", ],
        "speed": 30,
        "radius": 50,
        "shape": "Erick"
    }
}
    

class Enemy:
    def __init__(self,x,y, enemy_type):
        
        if enemy_type not in enemy_data:
            enemy_type = "gampang"
            
            
        data = enemy_data[enemy_type]
        
        self.x = float(x)
        self.y = float(y)
        self.is_alive = True
        
        self.enemy_type = enemy_type
        self.target_word = random.choice(data["word_list"]).upper()
        
        
        self.speed = data["speed"]
        self.radius = data["radius"]
        self.shape = data["shape"]
    
    def update(self, dt, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)
        
        if distance > 1:
            dx = dx / distance
            dy = dy / distance
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        if distance < self.radius + 20:
            self.is_alive = False
            
    def draw(self,ctx):
        
        
        ctx.save()
        ctx.translate(self.x, self.y) 
        ctx.set_source_rgb(*C_RED_ENEMY) 
        
        if self.shape == "Goblin":
            ctx.arc(0, 0, self.radius, 0, 2 * math.pi)
            ctx.fill()
        elif self.shape == "Skeleton":
            ctx.move_to(0, -self.radius)
            ctx.line_to(self.radius, self.radius)
            ctx.line_to(-self.radius, self.radius)
            ctx.close_path()
            ctx.fill()
        elif self.shape == "Ahmat":
            ctx.rectangle(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
            ctx.fill()
        elif self.shape == "Alpin":
            ctx.set_line_width(3)
            ctx.rectangle(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
            ctx.stroke()
        elif self.shape == "Erick":
            ctx.rectangle(-self.radius/2, -self.radius/2, self.radius, self.radius)
            ctx.fill()
            ctx.set_source_rgb(*C_BLACK)
            ctx.set_line_width(5)
            ctx.move_to(0, -self.radius); ctx.line_to(0, self.radius) 
            ctx.move_to(-self.radius, 0); ctx.line_to(self.radius, 0) 
            ctx.stroke()
        
        
        ctx.restore()
        
    def speed_up(self):
        self.speed *= 1.5