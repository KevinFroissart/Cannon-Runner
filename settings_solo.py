# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 13:00:58 2018

@author: Kevin
"""

""" GAME OPTIONS """

#options de la fenetre
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Cannon Runner"
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
SPRITESHEET_IDLE = "spritesheet_idle.png"
SPRITESHEET_JUMP = "spritesheet_jump.png"
SPRITESHEET_RUN = "spritesheet_run.png"
SPRITESHEET_MOB = "mob2.png"
SPRITESHEET_POW = "pow.png"

#couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 33, 0)
GREEN = (0, 255, 0)
BLUE = (38, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

#options player
PLAYER_ACC = 0.65
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
#platformes
PLATFORM_LIST = [(0, HEIGHT -60),
                 (WIDTH / 2 -50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]
                 
#options jeu
BOOST_POWER = 60
POW_SPAWN = 4
MOB_FREQ = 5000 #5s
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0