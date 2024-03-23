from pygame import *
from typing import Any


win = display.set_mode((700, 500))
display.set_caption('Догонялки')
#background = transform.scale(image.load('background.jpg'), (700, 500))


mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

#sound = mixer.Sound('hit.mp3')
#damage = mixer.Sound('hit.mp3')
#finish = mixer.Sound('money.mp3')

font.init()
font = font.Font(None, 70)
wind1 = font.render('YOU WIN', True, (225, 255, 0) )
wind2 = font.render('YOU LOSE', True, (255, 0, 0) )



clock = time.Clock()
FPS = 60
game = True


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
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 445:
            self.rect.y += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direct = 'left'
    def update(self):
        if self.rect.x >= 450:
            self.direct = 'left'
        if self.rect.x <= 200:
            self.direct = 'right'

        if self.direct == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


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
hero1 = Player('sprite1.png', 100, 70, 5, 65, 65)
hero2 = Enemy('sprite2.png', 400, 300, 5, 100, 100)

w1 = Wall(154, 205, 50, 100, 20, 450, 10) #g
w2 = Wall(154, 205, 50, 350, 30, 10, 380) #v
w3 = Wall(154, 205, 50, 200, 120, 10, 380) #v


while game:
    #win.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False

    key_pressed = key.get_pressed()
    if key_pressed[K_q]:
        sound.play()

    background.reset()
    hero1.update()
    hero1.reset()
    hero2.reset()
    hero2.update()
    victory.reset()
    w1.draw_wall()
    w2.draw_wall()
    w3.draw_wall()

    if sprite.collide_rect(hero1, victory):
        win.blit(wind1, (200, 200))
        #finish.play()

    if sprite.collide_rect(hero1, hero2) or sprite.collide_rect(hero1, w1) or sprite.collide_rect(hero1, w2) or sprite.collide_rect(hero1, w3):
        win.blit(wind2, (200, 200))
        #damage.play()
        hero1.rect.x = 100
        hero1.rect.y = 70


    clock.tick(FPS)
    display.update()
