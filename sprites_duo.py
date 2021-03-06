# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 13:44:23 2018

@author: Kevin
"""

""" SPRITES SETTINGS """

import pygame as pg
from settings_duo import *
from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        self.spritesheet_idle = pg.image.load(filename).convert()
        self.spritesheet_jump = pg.image.load(filename).convert()
        self.spritesheet_run = pg.image.load(filename).convert()
        self.spritesheet_mob = pg.image.load(filename).convert()
    
    #on va chercher les images aux bonnes coordonnees
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #on reduit la taille des sprite
        #//2 pour ne pas avoir de decimaux pour les pixels
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
        


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        #on assigne un sprite au player avec les coordonnees de l image
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        #on veux spwan en bas a gauche de l ecran
        self.rect.center = (40, HEIGHT - 100)
        self.pos = (40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        #annimations
        self.standing_frames = [self.game.spritesheet_idle.get_image(5, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(131, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(257, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(383, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(5, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(131, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(257, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(383, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(509, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(509, 235, 116, 220)]
        for frame in self.standing_frames:
            #on enleve les contours
            frame.set_colorkey(WHITE)
            
        self.jump_frames = [self.game.spritesheet_jump.get_image(5, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(387, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(5, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(387, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(578, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(578, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(5, 509, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 509, 181, 242)]
        for frame in self.jump_frames:
            #on enleve les contours
            frame.set_colorkey(WHITE)

        self.walk_frames_r = [self.game.spritesheet_run.get_image(5, 5, 182, 229),
                              self.game.spritesheet_run.get_image(197, 5, 182, 229),     
                              self.game.spritesheet_run.get_image(389, 5, 182, 229),
                              self.game.spritesheet_run.get_image(5, 244, 182, 229),
                              self.game.spritesheet_run.get_image(197, 244, 182, 229),
                              self.game.spritesheet_run.get_image(389, 244, 182, 229),
                              self.game.spritesheet_run.get_image(581, 5, 182, 229),
                              self.game.spritesheet_run.get_image(581, 244, 182, 229),
                              self.game.spritesheet_run.get_image(5, 483, 182, 229),
                              self.game.spritesheet_run.get_image(197, 483, 182, 229),]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            #horizontal puis vertival flip
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))


    def jump(self):
        #on peux jump seulement si on est sur une platforme
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -=1
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    
    def update(self):
        self.animate()
        #acceleration variable + ajout de la gravitee
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        #constant crash avec le += et les vecteurs donc pas de += !!!
        #on applique la friction
        self.acc.x = self.acc.x + self.vel.x * PLAYER_FRICTION
        #on applique les équations de mouvements
        self.vel = self.vel + self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos = self.pos + self.vel + 0.5 * self.acc
        #le perso ne sort pas de l'écran et on fait en sorte que l animation soit correcte
        #le perso doit sortir completement de l ecran avant de passer de l autre cote
        if self.pos.x > WIDTH - 40:
            self.pos.x = WIDTH - 40
        if self.pos.x < 40:
            self.pos.x =  40 
        self.rect.midbottom = self.pos
        
    def animate(self):
        now = pg.time.get_ticks()
        #si il a un mouvement alors on est en train de marcher
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
        if self.walking:
            #plus c est petit plus c est rapide
            if now - self.last_update > 20:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        if self.jumping:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) \
				% len(self.jump_frames)
                bottom = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        if not self.jumping and not self.walking:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #ici on fait une collision avec un masque mais ça prend pas mal de ressource
        #en revanche il n y a pas bcp d ennemie donc ce n est pas un probleme
        #mais si l on veux garder un max de perf, on fait une boucle dans laquelle
        #on fait une rect collision et SI et suelement SI il y a une rect collision
        #alors on lance un check pour un mask collision. Dans ce cas la, on sauve bcp de ressources
        self.mask = pg.mask.from_surface(self.image)
        
    def shoot(self):
        bullets = pg.sprite.Group()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.groups.add(bullet)
        bullets.add(bullet)
        
class Player2(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        #on assigne un sprite au player avec les coordonnees de l image
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        #on veux spwan en bas a gauche de l ecran
        self.rect.center = (WIDTH - 40, HEIGHT - 100)
        self.pos = (WIDTH - 40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        #annimations
        self.standing_frames = [self.game.spritesheet_idle.get_image(5, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(131, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(257, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(383, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(5, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(131, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(257, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(383, 235, 116, 220),
                                self.game.spritesheet_idle.get_image(509, 5, 116, 220),
                                self.game.spritesheet_idle.get_image(509, 235, 116, 220)]
        for frame in self.standing_frames:
            #on enleve les contours
            frame.set_colorkey(WHITE)
            
        self.jump_frames = [self.game.spritesheet_jump.get_image(5, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(387, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(5, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(387, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(578, 5, 181, 242),
                           self.game.spritesheet_jump.get_image(578, 257, 181, 242),
                           self.game.spritesheet_jump.get_image(5, 509, 181, 242),
                           self.game.spritesheet_jump.get_image(196, 509, 181, 242)]
        for frame in self.jump_frames:
            #on enleve les contours
            frame.set_colorkey(WHITE)

        self.walk_frames_r = [self.game.spritesheet_run.get_image(5, 5, 182, 229),
                              self.game.spritesheet_run.get_image(197, 5, 182, 229),     
                              self.game.spritesheet_run.get_image(389, 5, 182, 229),
                              self.game.spritesheet_run.get_image(5, 244, 182, 229),
                              self.game.spritesheet_run.get_image(197, 244, 182, 229),
                              self.game.spritesheet_run.get_image(389, 244, 182, 229),
                              self.game.spritesheet_run.get_image(581, 5, 182, 229),
                              self.game.spritesheet_run.get_image(581, 244, 182, 229),
                              self.game.spritesheet_run.get_image(5, 483, 182, 229),
                              self.game.spritesheet_run.get_image(197, 483, 182, 229),]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            #horizontal puis vertival flip
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))


    def jump(self):
        #on peux jump seulement si on est sur une platforme
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -=1
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    
    def update(self):
        self.animate()
        #acceleration variable + ajout de la gravitee
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        #constant crash avec le += et les vecteurs donc pas de += !!!
        #on applique la friction
        self.acc.x = self.acc.x + self.vel.x * PLAYER_FRICTION
        #on applique les équations de mouvements
        self.vel = self.vel + self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos = self.pos + self.vel + 0.5 * self.acc
        #le perso ne sort pas de l'écran et on fait en sorte que l animation soit correcte
        #le perso doit sortir completement de l ecran avant de passer de l autre cote
        if self.pos.x > WIDTH - 40:
            self.pos.x = WIDTH - 40
        if self.pos.x < 40:
            self.pos.x =  40 

        self.rect.midbottom = self.pos
        
    def animate(self):
        now = pg.time.get_ticks()
        #si il a un mouvement alors on est en train de marcher
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
        if self.walking:
            #plus c est petit plus c est rapide
            if now - self.last_update > 20:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        if self.jumping:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) \
				% len(self.jump_frames)
                bottom = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        if not self.jumping and not self.walking:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #ici on fait une collision avec un masque mais ça prend pas mal de ressource
        #en revanche il n y a pas bcp d ennemie donc ce n est pas un probleme
        #mais si l on veux garder un max de perf, on fait une boucle dans laquelle
        #on fait une rect collision et SI et suelement SI il y a une rect collision
        #alors on lance un check pour un mask collision. Dans ce cas la, on sauve bcp de ressources
        self.mask = pg.mask.from_surface(self.image)
        
        
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        #choice importe de random
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
         
class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game   
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        
    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()