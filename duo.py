# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 12:59:05 2018

@author: Kevin
"""

""" GAME MAIN CODE """

#on importe les differents modules necessaire au fonctionement du jeu
#ainsi que les morceaux de code exterieur a celui ci
import pygame as pg
import random
from settings_duo import *
from sprites_duo import *
from os import path
#pour pouvoir enregistrer les scores

class Game:
    def __init__(self):
        #initialize game window, etc
        
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        icon = pg.image.load(path.join(path.join(path.dirname(__file__), 'pic_main_menu'), 'logo.png'))
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.running = True 
        #si la police n'existe pas sur le pc, pygame en trouve une qui y resemble
        self.font_name = pg.font.match_font(FONT_NAME)
        #on recupere les scores        
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        #on ouvre le fichier et on peux lire et ecrir des infos 'r+' et creer le ficher si il n existe pas
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            #si il y a un ficher on lit les infos sinon HS = 0
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet_idle = Spritesheet(path.join(img_dir, SPRITESHEET_IDLE))
        self.spritesheet_jump = Spritesheet(path.join(img_dir, SPRITESHEET_JUMP))
        self.spritesheet_run = Spritesheet(path.join(img_dir, SPRITESHEET_RUN))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        #on ajoute le son
        self.sound_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jump_sound.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.sound_dir, 'boost_sound.wav'))
                
    def new(self):
        self.score = 0
        #on utilise layeredupdate pour pouvoir definir l ordre de passage dans le plan des sprites
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bullets = pg.sprite.Group()


        #on prend tte les platformes de la liste grace a *plat et on les ajoute aux sprites
        for plat in PLATFORM_LIST:
            Platform(self, *plat)   
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.sound_dir, 'On Tiptoe.ogg'))
        for i in range(10):
            c = Cloud(self)
			#hauteur a partir de laquelle les nuages apparaissent
            c.rect.y += 500
        self.run()

    def run(self):
        # Game Loop
        #-1 = repeter a l infini
        pg.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            #print self.clock
        #fondu
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()
        #on cherche a faire spawn les mobs a un certain temps donne entre 4000 et 6000ms
        now = pg.time.get_ticks()
        #collision entre les sprite, false donc la collision ne detruit pas le sprite
        #on reset la position si le joueur touhe la platforme SEULEMENT si il tombe
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    #on doit atteindre au moins la moitie de la plateforme pour passer au dessus
                    if hit.rect.bottom > lowest.rect.centery:
                        lowest = hit
                #on ameliore la collision avec les plateforme de maniere a tomber si on depasse de moitie
				#and / pour passer a la ligne
                if self.player.pos.x < lowest.rect.right + 5 and \
                   self.player.pos.x > lowest.rect.left - 5:
                    if self.player.pos.y < lowest.rect.bottom:
                        #collision ente le midbottom et le top
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        if self.player2.vel.y > 0:
            hits2 = pg.sprite.spritecollide(self.player2, self.platforms, False)
            if hits2:
                lowest2 = hits2[0]
                for hit2 in hits2:
                    #on doit atteindre au moins la moitie de la plateforme pour passer au dessus
                    if hit2.rect.bottom > lowest2.rect.centery:
                        lowest2 = hit2
                #on ameliore la collision avec les plateforme de maniere a tomber si on depasse de moitie
				#and / pour passer a la ligne
                if self.player2.pos.x < lowest2.rect.right + 5 and \
                   self.player2.pos.x > lowest2.rect.left - 5:
                    if self.player2.pos.y < lowest2.rect.bottom:
                        #collision ente le midbottom et le top
                        self.player2.pos.y = lowest2.rect.top
                        self.player2.vel.y = 0
                        self.player2.jumping = False
                
        if random.randrange(100) < 75:
            Cloud(self)
            

        #si on tombe + petite annimation (ecran qui tombe avec nous)                 
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if self.player2.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player2.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        #on fait spawn de nouvelles plateformes
        #si taille du groupe plat < 6 on fait spawn
        while len(self.platforms) < 8:            
            width = random.randrange(50, 150)
            Platform(self, random.randrange(0, WIDTH - width - 60),
                     random.randrange(-75, -30))
        if self.player.vel.x > 0:
            hits_1 = pg.sprite.spritecollide(self.player2, self.bullets, True)
            if hits_1:
                lowest = hits_1[0]
                for hit_1 in hits_1:
                    self.player2.pos.x += SHURI_HIT
        if self.player.vel.x < 0:
            hits_2 = pg.sprite.spritecollide(self.player2, self.bullets, True)
            if hits_2:
                lowest = hits_2[0]
                for hit_2 in hits_2:
                    self.player2.pos.x -= SHURI_HIT
        if self.player2.vel.x > 0:
            hits_3 = pg.sprite.spritecollide(self.player, self.bullets, True)
            if hits_3:
                lowest = hits_3[0]
                for hit_3 in hits_3:
                    self.player.pos.x += SHURI_HIT
        if self.player2.vel.x < 0:
            hits_4 = pg.sprite.spritecollide(self.player, self.bullets, True)
            if hits_4:
                lowest = hits_4[0]
                for hit_4 in hits_4:
                    self.player.pos.x -= SHURI_HIT
                               
                         
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.player.jump_cut()
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player2.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player2.jump_cut()
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.player.shoot()
                    


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        #le perso reste toujours devant les plateformes
        self.draw_text(str(self.score), 22, WHITE,WIDTH / 2, 15)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir, 'TheOrphanage.ogg'))
        pg.mixer.music.play(-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Bougez avec Z Q S D, tirez avec F", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Appuyez sur une touche pour jouer", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Meilleur Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                #si on appuye sur une touche wait devient false
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        #game over screen + si on running ne tourne plus alors on ne montre pas l ecran
        #de maniere a pouvoir quitter le jeu
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.sound_dir, 'Introspection.ogg'))
        pg.mixer.music.play(-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " +str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Touchez une touche pour jouer", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NOUVEAU SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 +40)
            with open(path.join(self.dir, HS_FILE), 'r+') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Meilleur Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 +40)
        pg.display.flip()
        self.wait_for_key()

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()