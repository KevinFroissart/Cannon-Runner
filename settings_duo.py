# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 13:00:58 2018

@author: Kevin
"""

""" GAME OPTIONS """

#options de la fenetre
WIDTH = 1280
HEIGHT = 720
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
                 (WIDTH -80, HEIGHT -60),
                 (WIDTH / 4 +10, HEIGHT * 3 / 4 + 60),
                 (WIDTH * 3 / 4 -10, HEIGHT  * 3 / 4 - 70),
                 (WIDTH/2, HEIGHT/2 -60),
                 (WIDTH /4 + 20, HEIGHT/4),
                 (WIDTH * (3 / 4) + 10 , HEIGHT/4),
                 (WIDTH/4 -10, HEIGHT/2),
                 (WIDTH * 3/4 + 20, HEIGHT/4),
                 (WIDTH/4 - 300, HEIGHT/2 + 50 ),
                 (WIDTH * 3/4 + 60, HEIGHT * 3/4 + 80),
                 (WIDTH * 3/4 - 200, HEIGHT *3/4),
                 (WIDTH/2 - 100, HEIGHT* 3/4 - 150)
                 ]
                 
                 
                 
#options jeu

SHURI_HIT = 20
BOOST_POWER = 60
POW_SPAWN = 4
MOB_FREQ = 5000 #5s
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0