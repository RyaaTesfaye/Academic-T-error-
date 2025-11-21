import cairo
import math
from Settings import *
import random
from Player import *
import json
from lib.functions.drawGhost import draw_ghost
from lib.functions.drawSkeleton import draw_skeleton
from lib.functions.drawBook import draw_book
from lib.functions.drawHeart import draw_heart


# settings
Image = 'enemy/Enemy.json'
EnemyData = 'enemy/EnemyDifficultyData.json'

with open(Image, 'r') as file:
    imageEnemy = json.load(file)

with open(EnemyData, 'r') as file:
    DataEnemy = json.load(file)


image = imageEnemy["Tema1"]["ghost"]
image2 = imageEnemy["Tema1"]["Skeleton"]
image3 = imageEnemy["Tema1"]["book"]
image4 = imageEnemy["Tema1"]["heart"]

enemy_data = DataEnemy
class Enemy:
    def __init__(self,x,y, enemy_type):
        
        if enemy_type not in enemy_data:
            enemy_type = "gampang"
            
            
        data = enemy_data[enemy_type]
        
        self.x = float(x)
        self.y = float(y)
        self.is_alive = True
        self.possition = True
        
        self.enemy_type = enemy_type
        self.target_word = random.choice(data["word_list"]).upper()
        
        
        self.speed = data["speed"]
        self.radius = data["radius"]
        self.shape = data["shape"]
    
    def update(self, dt, player_objek):
        relative_x = self.x - player_objek.x
        dead_zone = 5
        
        if relative_x > dead_zone:
            self.possition = True
            pass
        elif relative_x < -dead_zone:
            self.possition = False
            pass
        else:
            self.possition = False
            pass


        dx = player_objek.x - self.x
        dy = player_objek.y - self.y
        distance = math.hypot(dx, dy)
        
        if distance > 1:
            dx = dx / distance
            dy = dy / distance
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        if distance < self.radius + 20:
            self.is_alive = False
            player_objek.take_damage(1) 
            
    def draw(self,ctx):
         
        ctx.save()
        ctx.translate(self.x, self.y) 
        ctx.set_source_rgb(*C_RED_ENEMY) 
        
        if self.shape == "Goblin":
            draw_ghost(ctx, 0, 0, 1, image, self.possition)
        elif self.shape == "Skeleton":
            draw_skeleton(ctx, 0, 0, 0.5, image2, self.possition)
        elif self.shape == "Ahmat":
            draw_book(ctx, 0, 0, 0.7, image3, self.possition)
        elif self.shape == "Alpin":
            draw_heart(ctx, 0, 0, 1, image4, self.possition)
        elif self.shape == "Boss":
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