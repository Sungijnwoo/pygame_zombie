import gettext
import math
import random
import sys
import numpy as np
from time import sleep

import pygame
from pygame.locals import * 
from datetime import datetime

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
YELLOW = (250, 250, 20)
BLUE = (20, 20, 250)

pygame.init()
score = 0
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('PyZombie : 좀비 소탕 게임')
pygame.display.set_icon(pygame.image.load('./imgs/zombie_icon.jpg'))
fps_clock = pygame.time.Clock()
FPS = 120

default_font = pygame.font.Font('NanumGothic.ttf', 28)
background_img = [pygame.image.load('./imgs/background1.jpg'), pygame.image.load('./imgs/background2.png')]
gun1_img = pygame.image.load('./imgs/gun_1.png')
fire = pygame.image.load('./imgs/fire.png')

pygame.mixer.music.load('./sound/Zombi_Ambience.mp3') 
gun_sound1 = pygame.mixer.Sound('./sound/gun_sound1.wav')
gun_sound1.set_volume(0.3)
gun_sound2 = pygame.mixer.Sound('./sound/gun_sound2.wav')
gun_sound3 = pygame.mixer.Sound('./sound/gun_sound3.wav')
become_zombie = pygame.mixer.Sound('./sound/become_zombie.wav')
bullet_reload = pygame.mixer.Sound('./sound/bullet_reload.wav')
nuclear = pygame.mixer.Sound('./sound/nuclear.wav')
damage_sound = pygame.mixer.Sound('./sound/damage.wav')
bullet_reload.set_volume(1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.image = pygame.image.load('./imgs/player_l.png')
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.gun = pygame.image.load('./imgs/gun_1.png')
        self.dx = 0
        self.dy = 0
        self.hp = 100
        self.speed = 5
        
        

    def set_pos(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x <= 10:
            self.rect.x = 10
        elif self.rect.x >= WINDOW_WIDTH - 60:
           self.rect.x = WINDOW_WIDTH - 60
        elif self.rect.y <= 10:
            self.rect.y = 10
        elif self.rect.y >= WINDOW_HEIGHT - 60:
            self.rect.y = WINDOW_HEIGHT - 60

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
    
    
    
  

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        super(Aim,self).__init__()
        self.image = pygame.image.load('./imgs/gun_point.png')
        self.rect = self.image.get_rect()
        self.rest = '∞'
        self.bullets = 30
        self.damage = 10
        self.fire = 0
        self.sound = gun_sound1

    def set_pos(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def shoot(self):
        if self.bullets > 0:
            self.sound.play()
            self.bullets -= 1
        else:
            pass  

    def fire_shoot(self):
        self.fire -= 1
        nuclear.play()
            

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

    def fireinthehole(self):
        self.image = pygame.image.load('./imgs/fire_point.png')
        self.rect = self.image.get_rect()
        self.damage = 100





class Zombie(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Zombie, self).__init__()
        zombies=('./imgs/zombie_n.jpg', './imgs/zombie_s.png', './imgs/zombie_ad.jpg')
        self.image = pygame.image.load(random.choice(zombies))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.hp = 100


    def update(self, x, y):
        try:
            self.hspeed = self.speed*(x-self.rect.x)/(abs(x-self.rect.x)+abs(y-self.rect.y))
            self.vspeed = self.speed*(y-self.rect.y)/(abs(x-self.rect.x)+abs(y-self.rect.y))
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed

        except ZeroDivisionError:
            pass

    def stop(self):
        self.rect.x -= self.hspeed * 10
        self.rect.y -= self.vspeed * 10
    
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
        
def zombie_direction(speed):
    random_direction = random.randint(1,4)
    if random_direction == 1:
        return Zombie(random.randint(0, WINDOW_WIDTH), 0, speed)
    elif random_direction == 2:
        return Zombie(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT, speed)
    elif random_direction == 3:
        return Zombie(0, random.randint(0, WINDOW_HEIGHT), speed)
    elif random_direction == 4:
        return Zombie(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT), speed)


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Gun, self).__init__()
        GUNS = ('./imgs/gun_2.png', './imgs/gun_3.png', './imgs/fire.png', './imgs/hp.jpg', './imgs/speed.png')
        self.choice = random.choice(GUNS)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



def game_screen():
    background_rect = [background_img[0].get_rect(), background_img[1].get_rect()]
    screen.blit(background_img[0], Rect(0, 0, background_rect[0].width, background_rect[0].height))
    screen.blit(background_img[1], Rect(WINDOW_WIDTH/2, 0, background_rect[1].width, background_rect[1].height))

    draw_text('좀비 소탕하기', pygame.font.Font('NanumGothic.ttf', 70), screen, WINDOW_WIDTH/2, WINDOW_HEIGHT/3.4, BLUE)
    draw_text('점수 : {}'.format(score), default_font, screen, WINDOW_WIDTH/2, WINDOW_HEIGHT/2.4, BLACK)
    draw_text("마우스 버튼이나 's'키를 누르면 게임이 시작됩니다.", default_font, screen, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, BLUE)
    draw_text("게임을 종료하려면 'Q'키를 누르세요", default_font, screen, WINDOW_WIDTH/2, WINDOW_HEIGHT/1.8, BLACK)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'quit'
            elif event.key == pygame.K_s:
                return 'play'
        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'play'
        if event.type == QUIT:
            return 'quit'
        

    return 'game_screen'

def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y 
    surface.blit(text_obj, text_rect)

def game_loop():
    a = 0
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)

    player = Player()
    aim = Aim()
    player.set_pos(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    zombies = pygame.sprite.Group()
    guns = pygame.sprite.Group()

    score = 0
    occur_prob = 600
    paused = False
    re = 0

    while True:
        pygame.display.update()
        fps_clock.tick(FPS)
        aim.set_pos(*pygame.mouse.get_pos())

        if paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_visible(False)
                    if event.key == pygame.K_q:
                        return 'quit'

        else:   
            screen.fill(WHITE)
            occur_of_zombie = 1 + int(score/500)
            min_zombie_speed = 2 + int(score/500)
            max_zombie_speed = 4 + int(score/500)

            if random.randint(1, occur_prob) == 1:
                for i in range(occur_of_zombie):
                    zombies.add(zombie_direction(random.randint(min_zombie_speed, max_zombie_speed)))
                    score += 10

            if random.randint(1, occur_prob*3) == 1:
                gun = Gun(random.randint(70, WINDOW_WIDTH - 70), random.randint(70, WINDOW_HEIGHT - 70))
                guns.add(gun)
            
            player.move()
            
            draw_text('점수 : {}'.format(score), default_font, screen, 80, 40, BLACK)
            draw_text('체력 : {}'.format(player.hp), default_font, screen, WINDOW_WIDTH-80, 40, BLACK)
            draw_text('총알 : {} / {}'.format(aim.bullets,aim.rest), default_font, screen, WINDOW_WIDTH/2, 40, BLUE)
            draw_text('수류탄 : {}'.format(aim.fire),default_font, screen, WINDOW_WIDTH - 220, 40, BLACK)
            screen.blit(player.gun, (WINDOW_WIDTH/2 + 100, 20))
            


            zombies.update(player.rect.x, player.rect.y)
            guns.update()
            zombies.draw(screen)
            guns.draw(screen)
            screen.blit(aim.image, aim.rect)
            screen.blit(player.image, player.rect)
            guns.draw(screen)
            for x,i in enumerate(list(zombies)):
                zombie_collide = i.collide(list(zombies)[x+1:])
                if zombie_collide:
                    zombie_collide.stop()

            attacking_zombie = player.collide(zombies)
            gun = player.collide(guns)

            if attacking_zombie:
                damage_sound.play()
                player.hp -= 1
                attacking_zombie.stop()

            elif gun:
                if gun.choice == 'gun_2.png':
                    player.gun = gun.image
                    aim.sound = gun_sound2
                    aim.bullets = 30
                    aim.rest = 90
                    aim.damage = 20
                elif gun.choice == 'gun_3.png':
                    player.gun = gun.image
                    aim.sound = gun_sound3
                    aim.bullets = 30
                    aim.rest = 90
                    aim.damage = 30 

                elif gun.choice == 'fire.png':
                    aim.fire += 1
                
                elif gun.choice == 'hp.jpg':
                    player.hp += 30

                elif gun.choice == 'speed.jpg':
                    plyaer.speed += 1

                gun.kill()

            if player.hp < 0:
                become_zombie.play()
                pygame.mixer.music.stop()
                sleep(4)
                zombies.empty()
                return 'game_screen'

                
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    aim.set_pos(*pygame.mouse.get_pos())
                    if aim.rect.x < player.rect.x:
                        player.image = pygame.image.load('./imgs/player_l.png')
                    else:
                        player.image = pygame.image.load('./imgs/player_r.png')

                if aim.bullets != 0:
                    re = 0
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if aim.damage == 100:
                            aim.fire_shoot()
                            aim.damage = temp
                            aim.image = pygame.image.load('./imgs/gun_point.png')
                            shooting_zombie = aim.collide(zombies)
                            sleep(1)
                            while shooting_zombie:
                                shooting_zombie.kill()
                                shooting_zombie = aim.collide(zombies)
                            
                        else:
                            aim.shoot()
                            shooting_zombie = aim.collide(zombies)
                            if shooting_zombie:
                                shooting_zombie.hp -= aim.damage
                                shooting_zombie.stop()
                                if shooting_zombie.hp <= 0:
                                    shooting_zombie.kill()

                elif aim.bullets == 0 and not re:
                    bullet_reload.play()
                    if aim.rest == 0:
                        aim.bullets = 30
                        aim.rest = '∞'
                        player.gun = pygame.image.load('./imgs/gun_1.png')
                        aim.sound = gun_sound1
                        aim.damage = 10
                        break
                    temp = datetime.now()   
                    re = 1

                elif aim.bullets == 0 and re:
                    temp2 = datetime.now()
                    if (temp2 - temp).seconds > 4:
                        aim.bullets = 30
                        if type(aim.rest) == int:
                            aim.rest -= 30 
                        re = 0 

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if aim.fire > 0:
                        temp = aim.damage
                        aim.fireinthehole()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        player.dx = player.speed
                    elif event.key == pygame.K_a:
                        player.dx = -player.speed
                    elif event.key == pygame.K_w:
                        player.dy = -player.speed
                    elif event.key == pygame.K_s:
                        player.dy = player.speed

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        player.dx = 0
                    elif event.key == pygame.K_a:
                        player.dx = 0
                    elif event.key == pygame.K_w:   
                        player.dy = 0
                    elif event.key == pygame.K_s:
                        player.dy = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            transp_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
                            transp_surf.set_alpha(150)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('일시정지', pygame.font.Font('NanumGothic.ttf', 60), screen, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, YELLOW)

    
def main_loop():
    action = 'game_screen'
    while action != 'quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            action = game_loop()

    pygame.quit()

main_loop()
