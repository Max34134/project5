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
lose = font1.render('YOU LOSER', True, (255, 0, 0) )
font2 = font.Font(None, 30)

clock = time.Clock()
FPS = 60
run = True
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
        global num_fireZ
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 7 and rel_time == False:
                num_fire += 1
                #fire_sound.play()
                self.fire()
            if num_fire >= 7 and rel_time == False:
                last_time = timer()
                rel_time = True

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 20 )
        bullets.add(bullet)
        #fire_sound.play()

lost = 0
class Enemy(GameSprite):
    direct = 'down'
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50, 700-50)
            lost = lost + 1

class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            # self.rect.x = randint(50, 700-50)
            # lost = lost + 1000000
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

background = GameSprite('background.jpg', 0, 0, 0, 700, 500)
hero1 = Player('sprite1.png', 400, 400, 10, 100, 100)
boss = Boss('sprite2.png', 500, 500, 1, 200, 200)
enemys = sprite.Group()
for i in range(1, 8):
    hero2 = Enemy('sprite2.png', randint(50, 700-50), 10, 1.5, 70, 70)
    enemys.add(hero2)

#создаём список пуль
bullets = sprite.Group()

score = 0 
goal = 300
life = 3

last_time = 0
rel_time = False
num_fire = 0
boss_hp = 21

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    text_score = font2.render('Счёт:' + str(score), True, (255, 255, 255))
    text_lose = font2.render('Потерь:' + str(lost), True, (255, 255, 255))
    text_life = font2.render('Жизни:' + str(life), True, (255, 0, 0))

    collide = sprite.groupcollide(enemys, bullets, True, True)
    for c in collide:
        # hit_sound.play()
        score += 1
        hero2 = Enemy('sprite2.png', randint(50, 700-50), 10, 1.5, 70, 70)
        enemys.add(hero2)


    if not finish:        
        background.reset()
        win.blit(text_score, (10, 10))
        win.blit(text_lose, (10, 50))
        win.blit(text_life, (10, 100))
        if score >= 10:
            boss.reset()
        enemys.draw(win)
        bullets.draw(win)
        hero1.reset()
        if rel_time  == True:
            now_time = timer()
            if now_time - last_time < 0.5:
                ammo_now = font2.render('Reload...', 1, (255, 0, 0))
                win.blit(ammo_now, (260, 460))
            else:
                num_fire = 0
                rel_time = False 
        enemys.update()
        hero1.update()
        bullets.update()
        boss.update()
        if sprite.spritecollide(boss, bullets, True):
            boss_hp -= 1
        if sprite.spritecollide(hero1, enemys, True) or lost == 15 :
            hero2 = Enemy('sprite2.png', randint(50, 700-50), 10, 1, 70, 70)
            enemys.add(hero2)
            life -= 1
        if life <= 0:
            # hit_sound.play()
            finish = True
            win.blit(lose, (220, 210))
        if score >= goal:
            finish = True
            win.blit(wind1, (220, 210))
        if boss_hp <= 0:
            boss.kill()
        display.update()


    clock.tick(FPS)
