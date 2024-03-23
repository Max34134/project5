from pygame import *
from typing import Any
from random import randint
from time import time as timer

win = display.set_mode((700, 500))
display.set_caption('Догонялки')


mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
# fire_sound = mixer.Sound('fire.mp3')
# boom_sound = mixer.Sound('boom.mp3')
# hit_sound = mixer.Sound('hit.mp3')


font.init()
font1 = font.Font(None, 70)
wind1 = font1.render('YOU WIN', True, (225, 255, 0) )
wind2 = font1.render('YOU LOSER', True, (255, 0, 0) )
font2 = font.Font(None, 30)

clock = time.Clock()
FPS = 60
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):

        global last_time
        global rel_time
        global num_fire
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 7 and rel_time == False:
                num_fire += 1
                #fire_sound.play()
                self.fire()
            if num_fire >= 7 and rel_time == False:
                last_time = timer()
                rel_time = True

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 15, 20, 20 )
        bullets.add(bullet)
        #fire_sound.play()

lost = 0
class Enemy(GameSprite):
    direct = 'left'
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50, 700-50)
            lost = lost + 1

# class Boss(GameSprite):
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.y > 500:
#             self.rect.y = 0
#             # self.rect.x = randint(50, 700-50)
#             # lost = lost + 1000000
        

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700:
            self.kill()


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_widht, wall_hight):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.wall_widht = wall_widht
        self.wall_hight = wall_hight
        self.image = Surface((self.wall_widht, self.wall_hight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


background = GameSprite('background.jpg', 0, 0, 0, 700, 500)
victory = GameSprite('victory.png', 550, 370, 7, 90, 90)
hero1 = Player('sprite1.png', 100, 350, 5, 65, 65)
hero2 = Enemy('sprite2.png', 400, 300, 5, 100, 100)
enemys = sprite.Group()
for i in range(1, 8):
    hero2 = Enemy('sprite2.png', randint(500, 700-50), randint(50, 400-50), 1.5, 70, 70)
    enemys.add(hero2)

score = 0 
goal = 300
life = 3

last_time = 0
rel_time = False
num_fire = 0

#создаём список пуль
bullets = sprite.Group()

w1 = Wall(154, 205, 50, 100, 20, 450, 10) #g
w2 = Wall(154, 205, 50, 350, 30, 10, 380) #v
w3 = Wall(154, 205, 50, 200, 120, 10, 380) #v


while game:
    #win.blit(background, (0,0))

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    text_score = font2.render('Счёт:' + str(score), True, (255, 255, 255))
    text_lose = font2.render('Потерь:' + str(lost), True, (255, 255, 255))
    text_life = font2.render('Жизни:' + str(life), True, (255, 0, 0))

    collide = sprite.groupcollide(enemys, bullets, True, True)
    for c in collide:
        # hit_sound.play()
        score += 1
        hero2 = Enemy('sprite2.png', randint(500, 700-50), 10, 1.5, 70, 70)
        enemys.add(hero2)
        hero2.update()
        

    if not finish:        
            background.reset()
            win.blit(text_score, (10, 10))
            win.blit(text_lose, (10, 50))
            win.blit(text_life, (10, 100))
            enemys.draw(win)
            bullets.draw(win)
            hero1.reset()
            hero2.reset()
            victory.reset()
            w1.draw_wall()
            w2.draw_wall()
            w3.draw_wall()
            bullets.update()
            hero1.update()
            hero2.update()
            if rel_time  == True:
                now_time = timer()
                if now_time - last_time < 0.5:
                    ammo_now = font2.render('Reload...', 1, (255, 0, 0))
                    win.blit(ammo_now, (260, 460))
                else:
                    num_fire = 0
                    rel_time = False 


    if sprite.collide_rect(hero1, victory):
        win.blit(wind1, (200, 200))
        score += 1000
        #finish.play()

    if sprite.collide_rect(hero1, hero2) or sprite.collide_rect(hero1, w1) or sprite.collide_rect(hero1, w2) or sprite.collide_rect(hero1, w3):
        win.blit(wind2, (200, 200))
        #damage.play()
        hero1.rect.x = 100
        hero1.rect.y = 350

    if sprite.spritecollide(hero1, enemys, True) or lost == 15 :
        hero2 = Enemy('sprite2.png', randint(50, 700-50), 10, 1, 70, 70)
        enemys.add(hero2)
        life -= 1
    if life <= 0:
        # hit_sound.play()
        finish = True
        win.blit(wind2, (220, 210))
    if score >= goal:
        finish = True
        win.blit(wind1, (220, 210))


    clock.tick(FPS)
    display.update()