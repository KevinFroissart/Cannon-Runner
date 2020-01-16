# -*- coding: utf-8 -*-

"""
Created on Tue Mar 27 11:59:29 2018

@author: matteo.devita
"""

import pygame
from pygame.locals import *
from settings_menu import *
from time import sleep
from os import path


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(path.join(path.dirname(__file__), 'snd'), 'Bats In The Belfry.ogg'))
pygame.mixer.music.play(-1)

#import de l'icone et du titre de la fenetre depuis le fichier constantes
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
pygame.display.set_caption(titre_fenetre)

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((window_width, window_height))

#Chargement et collage du fond
fond = pygame.image.load(bg_flou).convert()
fond = pygame.transform.scale(fond, (window_width, window_height))
fenetre.blit(fond, (0,0))


   
#Chargement et collage du logo
   
logo = pygame.image.load(image_logo).convert_alpha()

#récup dim logo
logo_width = logo.get_width()
logo_height = logo.get_height()

#collage du logo
fenetre.blit(logo, (window_width/2 - 250, window_height/2 - logo_height/1.2))


#tant que le logo n'a pas une dimension nulle
while (logo_width > 0 and logo_height > 0):
    #si le logo est égale aux dim de base, on attend 2 secondes    
    if logo_width == logo_initial_width and logo_height == logo_initial_height:
        pygame.display.flip()    
        sleep(2)
    #a chaque tour de boucle, on réduit les dim du logo de 5px, puis on recolle le fond et on actualise
    logo = pygame.transform.scale(logo, (logo_width - 5, logo_height - 5))
    
    
    fenetre.blit(fond, (0,0))
    fenetre.blit(logo, ((window_width/2 - logo_width/2), (window_height/2 - logo_height/1.2)))

    pygame.display.flip()
    
    
    sleep(0.01)
    
    #on récupère à chaque tour les nouvelles dim du logo qu'on stocke dans logo_width et logo_height
    logo_width = logo.get_width()
    logo_height = logo.get_height()
    
    #pour pouvoir quitter
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

#on initialise les polices
pygame.font.init()

#on créer une police Comic Sans MS de taille 80
font = pygame.font.SysFont('Comic Sans MS', 80)

#on créer un texte d'entrer qu'on ajoute dans la police et on récupère la largeur
text_space = 'Press SPACE to play' 
text_space_surface = font.render(text_space, True, (211, 211, 211))
text_space_surface_width = text_space_surface.get_width()

#on stocke ces 2 textes pour les options de fullscreen et window plus tard
text_fullscreen = "You already are in fullscreen mode"
text_windowed = "You already are in windowed mode"

#on ajoute ces deux texxtes dans des polices et on récupère es dimensions
text_fullscreen_surface        = font.render(text_fullscreen, True, (0,0,0))
text_fullscreen_surface_width  = text_fullscreen_surface.get_width()
text_fullscreen_surface_height = text_fullscreen_surface.get_height()

text_windowed_surface          = font.render(text_windowed, True, (0,0,0))
text_windowed_surface_width    = text_windowed_surface.get_width()
text_windowed_surface_height   = text_windowed_surface.get_height()

#pareil pour afficher settings quand on est dans le menu setings
text_settings                  = "settings"
text_settings_surface          = font.render(text_settings, True, (0,0,0))
text_settings_surface_width    = text_settings_surface.get_width()
text_settings_surface_height   = text_settings_surface.get_height()


#menu de type 1
menu_state = 1

while menu_state == 1:
        #on fait clignotez "press SPACE to play" avec un intervalle de 0.2s
        fenetre.blit(text_space_surface, (window_width/2 - text_space_surface_width/2, window_height/2))
        pygame.display.flip()
        sleep(0.2)
        fenetre.blit(fond, (0,0))
        pygame.display.flip()
        sleep(0.2)        
        #boucle pour permmetre de quiter le jeu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                menu_state = 2
    
#on charge une image uniquemetn noir    
black_rect = pygame.image.load(bg_black).convert()    
#tant que i <=300 on affiche le rectangle noir avec une valeur assombrie de +1 à chaque fois
for i in range(300):
    i += 1
    black_rect.set_alpha(1)
    fenetre.blit(black_rect, (0,0))    
    pygame.display.flip()      
    sleep(0.005)
    #menu de typer 2
    menu_state = 2
    #boucle pour quitter le jeu
    for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()

#on charge le perso vert (celui tourner vers la gaucge) et les deux persos violets dans les 2 sens 
perso_violet        = pygame.image.load(p_violet).convert_alpha()
perso_vert          = pygame.image.load(p_vert).convert_alpha()
perso_violet_2      = pygame.image.load(p_violet2).convert_alpha()

#on récupère largeur et hauteur du perso violet
perso_violet_width  = perso_violet.get_width()
perso_violet_height = perso_violet.get_height()


#on récupère largeur et hauteur du perso vert
perso_vert_width    = perso_vert.get_width()
perso_vert_height   = perso_vert.get_height()

#on fait réafficher le fond et on actualise
fenetre.blit(fond, (0,0))   
pygame.display.flip()
sleep(1) #petite pause

#les changed point représente les points haut gauche sur l'axe des abcsisses de chaque image qui font changer de valeur au cours de l'animation (voir lignes 213 et 229)
perso_violet_changed_point = - perso_violet_width 
perso_vert_changed_point   = window_width



#menu de type 3
menu_state = 3


#on charge les images qui affichent 1 player et 2 players, on récupère leur dimensions et on intialise un changed point, qui lui sera sur l'axe des ordonnées (toujours le point haut gauche)
one_player_image               = pygame.image.load(player_1).convert_alpha()
one_player_image               = pygame.transform.scale(one_player_image, (window_width/3, window_height/15))
one_player_image_width         = one_player_image.get_width()
one_player_image_height        = one_player_image.get_height()
one_player_image_changed_point = - one_player_image_height

two_player_image               = pygame.image.load(player_2).convert_alpha()
two_player_image               = pygame.transform.scale(two_player_image, (window_width/3, window_height/15))
two_player_image_width         = two_player_image.get_width()
two_player_image_height        = two_player_image.get_height()
two_player_image_changed_point = window_height

#on recharge le logo
logo        = pygame.image.load(image_logo2).convert_alpha()
logo_width  = logo.get_width()
logo_height = logo.get_height()





#on choisit cette condition car c'est l'animation la plus longue parmis toute : afin que les autres aient le temps de s'effectuer aussi
while (one_player_image_changed_point < window_height/1.75):
    
    
    
    #si les valeurs de changed point dépasse de là où on voudrait qu'elles s'arrêtent, on les repositionnent au bon endroit
    if perso_violet_changed_point >= 0:
        perso_violet_changed_point = 0
    if perso_vert_changed_point <= window_width - perso_vert_width:
        perso_vert_changed_point = window_width - perso_vert_width
    if two_player_image_changed_point <= window_height/2 + window_height/5:
        two_player_image_changed_point = window_height/2 + window_height/5
    
    #on charge chaque éléments avec les valeurzs de changed_point cortrespondantes
    fenetre.blit(fond, (0,0))
    fenetre.blit(logo, (window_width/2 - logo_width/2, window_height/2 - window_height / 2.75))    
    
    fenetre.blit(perso_violet, (perso_violet_changed_point, window_height/2 - perso_violet_height/2))
    
    
    fenetre.blit(perso_violet_2, (perso_vert_changed_point - window_height/25, window_height/2 - perso_violet_height/2))
    fenetre.blit(perso_vert, (perso_vert_changed_point, window_height/2 - perso_vert_height/2))
    
    
    fenetre.blit(one_player_image, (window_width/2 - one_player_image_width/2, one_player_image_changed_point))
    fenetre.blit(two_player_image, (window_width/2 - one_player_image_width/2, two_player_image_changed_point))
    
    sleep(0.001)
    
    #on incrémente les valeurs des changed_point de + 1 ou - 1 selon les cas
    perso_violet_changed_point += 1
    perso_vert_changed_point -= 1
    one_player_image_changed_point += 1
    two_player_image_changed_point -= 1
    pygame.display.flip()
    
    #boucle pour pouvoir quitter
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()



#menu de type 4
menu_state = 4


#rotate_angle est la variable qi gère l'angle d'inclinaison du logo
rotate_angle = 1

#on charge et affiche l'image de roue des options et on récupère ses dimensions
option_wheel_image        = pygame.image.load(option).convert_alpha()
option_wheel_image        = pygame.transform.scale(option_wheel_image, (window_width/18, window_height/14))
option_wheel_image_width  = option_wheel_image.get_width()
option_wheel_image_height = option_wheel_image.get_height()

#boucle étape 4 et tant que l'angle de rotation du logo < 5
while menu_state == 4 and rotate_angle <= 5:
    
    #on affiche chaques éléments et on fait tourner le logo de +1 degré à chaque tour de boucle
    logo = pygame.transform.rotate(logo, (rotate_angle))
    fenetre.blit(logo, (window_width/2 - logo_width/2, window_height/2 - window_height / 2.75))
    
    fenetre.blit(fond, (0,0))
    fenetre.blit(logo, (window_width/2 - logo_width/2, window_height/2 - window_height / 2.75))    
    
    
    fenetre.blit(perso_violet, (perso_violet_changed_point, window_height/2 - perso_violet_height/2))
    
    
    fenetre.blit(perso_violet_2, (perso_vert_changed_point - window_width/25, window_height/2 - perso_violet_height/2))
    fenetre.blit(perso_vert, (perso_vert_changed_point, window_height/2 - perso_vert_height/2))
    
    
    fenetre.blit(one_player_image, (window_width/2 - one_player_image_width/2, one_player_image_changed_point))
    fenetre.blit(two_player_image, (window_width/2 - one_player_image_width/2, two_player_image_changed_point))    
    
    
    fenetre.blit(option_wheel_image, (window_width/32, window_height/24))
    
    pygame.display.flip()
    sleep(0.01)
    rotate_angle += 1
    
    #boucle pour pouvoir quitter
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()
        if event.type == KEYDOWN and key.event == K_q:
            pygame.quit()


#menu de type 5
menu_state = 5

#on charge les persos violet dans les 2 sens et le perso vert
perso_violet_3 = pygame.image.load(p_violet3).convert_alpha()
perso_violet_4 = pygame.image.load(p_violet4).convert_alpha()
perso_vert_3   = pygame.image.load(p_vert3).convert_alpha()


#on charge les mêmes images mais entourés d'un trait blanc
one_player_image_outline = pygame.image.load(player_1_outline).convert_alpha()
one_player_image_outline = pygame.transform.scale(one_player_image_outline, (window_width/3, window_height/15))

two_player_image_outline = pygame.image.load(player_2_outline).convert_alpha()
two_player_image_outline = pygame.transform.scale(two_player_image_outline, (window_width/3, window_height/15))


#on charge l'image roue d'option et la même image entourée
option_wheel_image_outline = pygame.image.load(option_outline).convert_alpha()
option_wheel_image_outline = pygame.transform.scale(option_wheel_image_outline, (window_width/18, window_height/14))






#on charge toutes les images du menu options et on récupère les dimensions on change aussi les dimension avec pygame.transform.scale()
fullscreen_image = pygame.image.load(grand_blanc).convert_alpha()
fullscreen_image = pygame.transform.scale(fullscreen_image, (window_width/17, window_height/7))

fullscreen_image_width = fullscreen_image.get_width()
fullscreen_image_height = fullscreen_image.get_height()

fullscreen_image_outline = pygame.image.load(grand_blanc_outline).convert_alpha()
fullscreen_image_outline = pygame.transform.scale(fullscreen_image_outline, (window_width/17, window_height/7))

windowed_image = pygame.image.load(grand_blanc).convert_alpha()
windowed_image = pygame.transform.scale(windowed_image, (window_width/17, window_height/7))

windowed_image_width = windowed_image.get_width()
windowed_image_height = windowed_image.get_height()


windowed_image_outline = pygame.image.load(petit_blanc_outline).convert_alpha()
windowed_image_outline = pygame.transform.scale(windowed_image_outline, (window_width/17, window_height/7))

#fullscreen_mode à l'état faux --> mode fenetré
fullscreen_mode = False



sound_on_image = pygame.image.load(sound_on).convert_alpha()
sound_on_image = pygame.transform.scale(sound_on_image, (window_width/21, window_height/12))
sound_on_image_width = sound_on_image.get_width()
sound_on_image_height = sound_on_image.get_height()

sound_on_image_outline = pygame.image.load(sound_on_outline).convert_alpha()
sound_on_image_outline = pygame.transform.scale(sound_on_image_outline, (window_width/21, window_height/12))



sound_off_image = pygame.image.load(sound_off).convert_alpha()
sound_off_image = pygame.transform.scale(sound_off_image, (window_width/21, window_height/12))
sound_off_image_width = sound_off_image.get_width()
sound_off_image_height = sound_off_image.get_height()

sound_off_image_outline = pygame.image.load(sound_off_outline).convert_alpha()
sound_off_image_outline = pygame.transform.scale(sound_off_image_outline, (window_width/21, window_height/12))

sound_more_image = pygame.image.load(sound_more).convert_alpha()
sound_more_image = pygame.transform.scale(sound_more_image, (window_width/21, window_height/12))
sound_more_image_width = sound_more_image.get_width()
sound_more_image_height = sound_more_image.get_height()

sound_more_image_outline = pygame.image.load(sound_more_outline).convert_alpha()
sound_more_image_outline = pygame.transform.scale(sound_more_image_outline, (window_width/21, window_height/12))


sound_less_image = pygame.image.load(sound_less).convert_alpha()
sound_less_image = pygame.transform.scale(sound_less_image, (window_width/21, window_height/12))
sound_less_image_width = sound_less_image.get_width()
sound_less_image_height = sound_less_image.get_height()

sound_less_image_outline = pygame.image.load(sound_less_outline).convert_alpha()
sound_less_image_outline = pygame.transform.scale(sound_less_image_outline, (window_width/21, window_height/12))

back_image = pygame.image.load(back).convert_alpha()
back_image = pygame.transform.scale(back_image, (300, 100))
back_image_width = back_image.get_width()
back_image_height = back_image.get_height()


back_image_outline = pygame.image.load(back_outline).convert_alpha()
back_image_outline = pygame.transform.scale(back_image_outline, (300, 100))

#boucle menu de type 5
while menu_state == 5:
    
    #boucle pour pouvoir quitter
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEMOTION:
            
            
            
            #si souris sur option wheel image, on charge l'image outline
            if (window_width/32 < event.pos[0] < window_width/32 + option_wheel_image_width) and (window_height/24 < event.pos[1] < window_height/24 + option_wheel_image_height):
                fenetre.blit(option_wheel_image_outline,(window_width/32, window_height/24))
                pygame.display.flip()
                
            #souris sur perso violet, on charge l'image outline
            if (perso_violet_width > event.pos[0] > 0) and (window_height/2 + perso_violet_height/2 > event.pos[1] > window_height/2 - perso_violet_height/2):
                
                fenetre.blit(perso_violet_3, (perso_violet_changed_point, window_height/2 - perso_violet_height/2))
                fenetre.blit(one_player_image_outline, (window_width/2 - one_player_image_width/2, one_player_image_changed_point))                                
                pygame.display.flip()
                
            #souris sur texte 1 player, on charge l'image outline
            if (window_width/2 + one_player_image_width/2 > event.pos[0] > window_width/2 - one_player_image_width/2) and (one_player_image_changed_point + one_player_image_height > event.pos[1] > one_player_image_changed_point):
                fenetre.blit(perso_violet_3, (perso_violet_changed_point, window_height/2 - perso_violet_height/2))
                fenetre.blit(one_player_image_outline, (window_width/2 - one_player_image_width/2, one_player_image_changed_point))                                
                pygame.display.flip()
            
            
            #souris sur perso vert, on charge l'image outline
            if (perso_vert_changed_point - window_width/25 < event.pos[0] < window_width) and (window_height/2 + perso_violet_height/2 > event.pos[1] > window_height/2 - perso_violet_height/2):
                
                fenetre.blit(perso_violet_4, (perso_vert_changed_point - window_height/25, window_height/2 - perso_violet_height/2))
                fenetre.blit(perso_vert_3, (perso_vert_changed_point, window_height/2 - perso_vert_height/2))
                fenetre.blit(two_player_image_outline, (window_width/2 - two_player_image_width/2, two_player_image_changed_point))
                pygame.display.flip()
            
            #souris sur texte 2 player, on charge l'image outline
            if (window_width/2 + two_player_image_width/2 > event.pos[0] > window_width/2 - two_player_image_width/2) and (two_player_image_changed_point + two_player_image_height > event.pos[1] > two_player_image_changed_point):
                fenetre.blit(perso_violet_4, (perso_vert_changed_point - window_height/25, window_height/2 - perso_violet_height/2))
                fenetre.blit(perso_vert_3, (perso_vert_changed_point, window_height/2 - perso_vert_height/2))
                fenetre.blit(two_player_image_outline, (window_width/2 - two_player_image_width/2, two_player_image_changed_point))
                pygame.display.flip()
                
                
        #si clique souris
        if event.type == MOUSEBUTTONDOWN:
            
                #si soursi clique gauche sur perso violet  
                if (perso_violet_width > event.pos[0] > 0) and (window_height/2 + perso_violet_height/2 > event.pos[1] > window_height/2 - perso_violet_height/2):
                    player_1_state = True                    
                    if event.button == 1:
                        while player_1_state == True:
                            from solo import *
                            
               #si soursi clique gauche sur perso 1 player   
                if (window_width/2 + one_player_image_width/2 > event.pos[0] > window_width/2 - one_player_image_width/2) and (one_player_image_changed_point + one_player_image_height > event.pos[1] > one_player_image_changed_point):
                    player_1_state = True                    
                    if event.button == 1:
                        while player_1_state == True:
                            from solo import *


                            
                #si soursi clique gauche sur perso vert et violet
                if (perso_vert_changed_point - window_width/25 < event.pos[0] < window_width) and (window_height/2 + perso_violet_height/2 > event.pos[1] > window_height/2 - perso_violet_height/2):
                    player_2_state = True                    
                    if event.button == 1:
                        while player_1_state == True:
                            from duo import *
                            
                #si soursi clique gauche sur 2 players 
                if (window_width/2 + two_player_image_width/2 > event.pos[0] > window_width/2 - two_player_image_width/2) and (two_player_image_changed_point + two_player_image_height > event.pos[1] > two_player_image_changed_point):
                    player_2_state = True                    
                    if event.button == 1:
                        while player_2_state == True:
                            from duo import *
                  
                #si souris clique sur option wheel image, option_state à l'état True      
                if (window_width/32 < event.pos[0] < window_width/32 + option_wheel_image_width) and (window_height/24 < event.pos[1] < window_height/24 + option_wheel_image_height):
                    option_state = True
                    #tant que option_state à l'état True, on affiche le menu des options
                    while option_state == True:
                        #boucle pour pouvoir quitter
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                            if event.type == MOUSEMOTION:
                                #si souris sur image u, on charge image outline
                                if (window_width/3 < event.pos[0] < window_width/3 + fullscreen_image_width) and (window_height/4 < event.pos[1] < window_height/4 + fullscreen_image_height):
                                    fenetre.blit(fullscreen_image_outline, (window_width/3, window_height/4))                                    
                                    pygame.display.flip()
                                    #si souris sur image windowed, on charge image outline
                                if (window_width - window_width/3 < event.pos[0] < window_width - window_width/3 + windowed_image_width) and (window_height/4 < event.pos[1] < window_height/4 + windowed_image_height):
                                    fenetre.blit(windowed_image_outline, (window_width - window_width/3, window_height/4))
                                    pygame.display.flip()
                                    #si souris sur image sound on, on charge image outline
                                if (window_width - window_width/5 < event.pos[0] < window_width - window_width/5 + sound_off_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_off_image_height):
                                    fenetre.blit(sound_off_image_outline, (window_width - window_width/5, window_height/2))
                                    pygame.display.flip()
                                
                                #si souris sur image sound off, on charge image outline
                                if (window_width/5 < event.pos[0] < window_width/5 + sound_on_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_on_image_height):
                                    fenetre.blit(sound_on_image_outline, (window_width/5, window_height/2))
                                    pygame.display.flip()
                                
                                #si souris sur image sound more, on charge image outline
                                if (window_width/3 < event.pos[0] < window_width/3 + sound_less_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_less_image_height)                                :
                                    fenetre.blit(sound_more_image_outline, (window_width/3, window_height/2))
                                    pygame.display.flip()
                                
                                #si souris sur image sound less, on charge image outline
                                if (window_width - window_width/3 < event.pos[0] < window_width - window_width/3 + sound_more_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_more_image_height)                                :
                                    fenetre.blit(sound_less_image_outline, (window_width - window_width/3, window_height/2))
                                    pygame.display.flip()
                                    
                                #si souris sur image back, on charge image outline
                                if (window_width/25 < event.pos[0] < window_width/25 + back_image_width) and (window_height/1.2 < event.pos[1] < window_height/1.2 + back_image_height):
                                    fenetre.blit(back_image_outline, (window_width/25, window_height/1.2))
                                    pygame.display.flip()
                                
                            #si cliques souris
                            if event.type == MOUSEBUTTONDOWN:
                                #si clique gauche sur image fullscreen
                                if (window_width/3 < event.pos[0] < window_width/3 + fullscreen_image_width) and (window_height/4 < event.pos[1] < window_height/4 + fullscreen_image_height):
                                    if event.button == 1:
                                        #si on est déjà en fullscreen, on affiche un texte qui indique qu'on est déjà en fullscreen                                        
                                        if fullscreen_mode == True:
                                            fenetre.blit(fond, (0,0))
                                            fenetre.blit(text_fullscreen_surface, (window_width/2 - text_fullscreen_surface_width/2, window_height/2 - text_fullscreen_surface_height))                                           
                                            pygame.display.flip()
                                            sleep(2)
                                            quit
                                        #si on est pas déjà en fullscreen alors on met en fullscreen
                                        if fullscreen_mode == False:
                                            fenetre = pygame.display.set_mode((window_width, window_height), FULLSCREEN)
                                            fullscreen_mode = True
                                #si clique gauche sur image windowed
                                if (window_width - window_width/3 < event.pos[0] < window_width - window_width/3 + windowed_image_width) and (window_height/4 < event.pos[1] < window_height/4 + windowed_image_height):
                                    if event.button == 1:
                                        #si on est déjà en mode fenetrée, on affiche un texte qui indique qu'on est déjà en mode fenetrée                                        
                                        if fullscreen_mode == False:
                                            fenetre.blit(fond, (0,0))
                                            fenetre.blit(text_windowed_surface, (window_width/2 - text_windowed_surface_width/2, window_height/2 - text_windowed_surface_height))                                           
                                            pygame.display.flip()
                                            sleep(2)
                                        #si on est pas déjà en mode fenetrée, alors on met en mode fenetrée
                                        if fullscreen_mode == True:                                    
                                            fenetre = pygame.display.set_mode((window_width, window_height))
                                            fullscreen_mode = False
                                #si clique gauce sur image sound more
                                if (window_width/3 < event.pos[0] < window_width/3 + sound_less_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_less_image_height)                                :
                                    print("sound more")
                                    
                                 #si clique gauche sur image sound less
                                if (window_width - window_width/3 < event.pos[0] < window_width - window_width/3 + sound_more_image_width) and (window_height/2 < event.pos[1] < window_height/2 + sound_more_image_height)                                :
                                    print("sound less")
                                
                                 #si clique gauche sur image back
                                if (window_width/25 < event.pos[0] < window_width/25 + back_image_width) and (window_height/1.2 < event.pos[1] < window_height/1.2 + back_image_height):
                                    option_state = False
                                    
                                
                                                                                       
                        """
                        !!! Rajouter option augmenter et diminuer le son !!!            
                        """
                        
                        #quand on sort du menu option, option_state = False et on réaffiche les éléments du menu normal
                        fenetre.blit(fond, (0,0))
                        fenetre.blit(fullscreen_image, (window_width/3, window_height/4))
                        fenetre.blit(windowed_image, (window_width - window_width/3, window_height/4))
                        
                        fenetre.blit(sound_on_image, (window_width/5, window_height/2))
                        fenetre.blit(sound_off_image, (window_width - window_width/5, window_height/2))
                        
                        fenetre.blit(sound_more_image, (window_width/3, window_height/2))
                        fenetre.blit(sound_less_image, (window_width - window_width/3, window_height/2))
                        
                        fenetre.blit(text_settings_surface, (window_width/2 - text_settings_surface_width/2, window_height/100))
                        
                        fenetre.blit(back_image, (window_width/25, window_height/1.2))
                        pygame.display.flip()
                    
                
                    
                            
                
                                  
         #à chaque tour de la boucle du menu, on réaffiche les éléments ( = acutalisation)
        fenetre.blit(fond, (0,0))
        fenetre.blit(logo, (window_width/2 - logo_width/2, window_height/2 - window_height / 2.75))
        
        
        fenetre.blit(perso_violet, (perso_violet_changed_point, window_height/2 - perso_violet_height/2))
        
        
        fenetre.blit(perso_violet_2, (perso_vert_changed_point - window_height/25, window_height/2 - perso_violet_height/2))
        fenetre.blit(perso_vert, (perso_vert_changed_point, window_height/2 - perso_vert_height/2))
        
        
        fenetre.blit(one_player_image, (window_width/2 - one_player_image_width/2, one_player_image_changed_point))
        fenetre.blit(two_player_image, (window_width/2 - one_player_image_width/2, two_player_image_changed_point))
        
        fenetre.blit(option_wheel_image, (window_width/32, window_height/24))
        

        
        pygame.display.flip()
    
    
        

            




#BOUCLE INFINIE
continuer = 1
while continuer:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
            
pygame.quit()            