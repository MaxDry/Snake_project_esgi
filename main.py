import pygame
import time
import random
import sys
import time
import csv
from Button import Button
from Services import our_snake, Your_score, display_text, addResult, displaySoloResults, displayMultiResults
from pygame import image
from tabulate import tabulate
from pygame.transform import scale

pygame.init()

#Nom de la fenêtre
pygame.display.set_caption("Snake ESGI")

#---------------------------------------------- VARIABLES ---------------------------------------------

#Taille de la fenêtre
#Forcément des multiples de la taille du standard block sinon ça fonctionne pas !
window_width = 1280
window_height = 720
window_resolution = (window_width,window_height)

#Définition de la fenêtre de jeu
window_surface = pygame.display.set_mode(window_resolution)

window_image = pygame.image.load("./img/wallpaper_snake.png").convert_alpha()
window_start = pygame.image.load("./img/wallpaper_start.png").convert_alpha()
window_lose = pygame.image.load("./img/wallpaper_lose.png").convert_alpha()
image_food = pygame.image.load("./img/framboise.png").convert_alpha()
image_food = pygame.transform.scale(image_food, (40, 40))

image_food2 = pygame.image.load("./img/framboiseGreen.png").convert_alpha()
image_food2 = pygame.transform.scale(image_food2, (40, 40))

image_food3 = pygame.image.load("./img/framboiseBlue.png").convert_alpha()
image_food3 = pygame.transform.scale(image_food3, (40, 40))

image_food4 = pygame.image.load("./img/framboiseBlack.png").convert_alpha()
image_food4 = pygame.transform.scale(image_food4, (40, 40))

image_food5 = pygame.image.load("./img/framboiseYellow.png").convert_alpha()
image_food5 = pygame.transform.scale(image_food5, (40, 40))

#Buttons
solo_btn_image = pygame.image.load('./img/solo.png').convert_alpha()
multi_btn_image = pygame.image.load('./img/multi.png').convert_alpha()
restart_btn_image = pygame.image.load('./img/restart.png').convert_alpha()
exit_btn_image = pygame.image.load('./img/exit.png').convert_alpha()
back_btn_image = pygame.image.load('./img/back.png').convert_alpha()
classic_btn_image = pygame.image.load('./img/classic.png').convert_alpha()
no_wall_btn_image = pygame.image.load('./img/no_wall.png').convert_alpha()
no_limit_btn_image = pygame.image.load('./img/no_limit.png').convert_alpha()
classement_btn_image = pygame.image.load('./img/classement.png').convert_alpha()
all_btn_image = pygame.image.load('./img/all.png').convert_alpha()


solo_button = Button(650, 250, solo_btn_image, 0.8)
multi_button = Button(650, 400, multi_btn_image, 0.8)
restart_button = Button(300, 550, restart_btn_image, 0.8)
exit_button = Button(650, 550, exit_btn_image, 0.8)
back_button = Button(650, 550, back_btn_image, 0.8)
classic_button = Button(300, 300, classic_btn_image, 0.8)
no_wall_button = Button(650, 300, no_wall_btn_image, 0.8)
no_limit_button = Button(1000, 300, no_limit_btn_image, 0.8)
classement_button = Button(190, 60, classement_btn_image, 0.8)
filter_all_button = Button(360, 50, all_btn_image, 0.4)
filter_classic_button = Button(540, 50, classic_btn_image, 0.4)
filter_no_wall_button = Button(740, 50, no_wall_btn_image, 0.4)
filter_no_limit_button = Button(940, 50, no_limit_btn_image, 0.4)

#Font des écritures de fin et du score
font_style = pygame.font.SysFont("bahnschrift", 25)

snake_block = 40

#Colors
window_color=(143,151,121)
color_snake=(11, 102, 35)
color_snake2=(255,0,0)
color_timer=(0,0,0)
red = (255, 0, 0)
white = (255, 255, 255)
game_start = False

#Initialisation de clock pour utiliser tick() qui équivaut à un time.sleep()
clock = pygame.time.Clock()

#---------------------------------------------- FIN - VARIABLES ---------------------------------------------

#---------------------------------------------- JEU ---------------------------------------------

def gameLoop(isMulti, mode):
    game_over = False
    game_close = False

    dataResult = None
    lastDataResult = None

    #Emplacement de départ
    x1 = window_width * 0.75
    y1 = window_height * 0.5

    x2 = window_width * 0.25
    y2 = window_height * 0.5

    #Emplacement vers lequel le snake se dirige étant incrémenté dans le while
    x1_change = 0
    y1_change = 0

    x2_change = 0
    y2_change = 0

    snake_List = []
    snake_List2 = []
    Length_of_snake = 1
    Length_of_snake2 = 1

    #Génération de la bouffe
    # round() arrondit au supérieur ou infèrieur (exemple : round(4.80) = 5)
    # randrange() prend deux nombres et te génère un nombre aléatoire entre les deux
    # Imaginons random.randrange() génère 268, divisé par 15 = 17,866.
    # round() arrondit à 18 puis on multiplie par 15 = 270
    # La position est donc un multiple de 15, notre serpent peut le manger
    foodx = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
    food = 1

    speed = 0

    if mode == 'no_limit':
        startTimer = time.time()
        counter = 0
    #Logique du code
    while not game_over:
        if mode == 'no_limit':
            counter = round(time.time() - startTimer)

            if time.time() - startTimer >= 60:
                if isMulti:
                    if Length_of_snake > Length_of_snake2:
                        dataResult = 'Joueur 2'
                    elif Length_of_snake < Length_of_snake2:
                        dataResult = 'Joueur 1'
                    else:
                        dataResult = 'Joueur 1 & Joueur 2'
                else:
                    dataResult = Length_of_snake - 1
                game_close = True
        #Effectue le traitement de tout ce while à chaque fois que le snake avance d'une case
        while game_close == True:
            if dataResult != None:
                lastDataResult = dataResult

            #Affichage de la fenetre si tu as perdu
            mouse_pos = pygame.mouse.get_pos()

            window_surface.fill(white)
            window_surface.blit(window_lose, (0, 0))

            if lastDataResult != None:
                text = pygame.font.SysFont("comicsansms", 30)
                value = text.render('SCORE : ' + str(lastDataResult) if str(lastDataResult).isdigit() else 'GAGNANT : ' + lastDataResult, True, 'white')
                window_surface.blit(value, [50, 50])

            if dataResult != None:
                if mode == 'classic':
                    dataMode = 'Classic'
                elif mode == 'no_wall':
                    dataMode = 'No wall'
                else:
                    dataMode = 'No limit'

                addResult(dataResult, dataMode, 'results/multi.csv' if isMulti else 'results/solo.csv')
                dataResult = None

            for button in [restart_button, back_button]:
                button.update(window_surface)

            # Décision à prendre quand tu commences
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.checkForInput(mouse_pos):
                        gameLoop(isMulti, mode)
                    if back_button.checkForInput(mouse_pos):
                        x1 = window_width * 0.75
                        y1 = window_height * 0.5
                        x2 = window_width * 0.25
                        y2 = window_height * 0.5
                        x1_change = 0
                        y1_change = 0
                        x2_change = 0
                        y2_change = 0
                        snake_List = []
                        snake_List2 = []
                        Length_of_snake = 1
                        Length_of_snake2 = 1

                        game_over = True
                        game_close = False

            pygame.display.update()
        #A chaque fois que j'appuie sur une touche il garde en mémoire la touche
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change == snake_block and mode != 'no_limit':
                        if isMulti:
                            dataResult = 'Joueur 1'
                        else:
                            dataResult = Length_of_snake - 1
                        game_close = True
                    else:
                        x1_change = -snake_block
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change == -snake_block and mode != 'no_limit':
                        if isMulti:
                            dataResult = 'Joueur 1'
                        else:
                            dataResult = Length_of_snake - 1
                        game_close = True
                    else:
                        x1_change = snake_block
                        y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change == snake_block and mode != 'no_limit':
                        if isMulti:
                            dataResult = 'Joueur 1'
                        else:
                            dataResult = Length_of_snake - 1
                        game_close = True
                    else:
                        y1_change = -snake_block
                        x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change == -snake_block and mode != 'no_limit':
                        if isMulti:
                            dataResult = 'Joueur 1'
                        else:
                            dataResult = Length_of_snake - 1
                        game_close = True
                    else:
                        y1_change = snake_block
                        x1_change = 0

                if isMulti:
                    if event.key == pygame.K_q:
                        if x2_change == snake_block and mode != 'no_limit':
                            dataResult = 'Joueur 2'
                            game_close = True
                        else:
                            x2_change = -snake_block
                            y2_change = 0
                    elif event.key == pygame.K_d:
                        if x2_change == -snake_block and mode != 'no_limit':
                            dataResult = 'Joueur 2'
                            game_close = True
                        else:
                            x2_change = snake_block
                            y2_change = 0
                    elif event.key == pygame.K_z:
                        if y2_change == snake_block and mode != 'no_limit':
                            dataResult = 'Joueur 2'
                            game_close = True
                        else:
                            y2_change = -snake_block
                            x2_change = 0
                    elif event.key == pygame.K_s:
                        if y2_change == -snake_block and mode != 'no_limit':
                            dataResult = 'Joueur 2'
                            game_close = True
                        else:
                            y2_change = snake_block
                            x2_change = 0

        # Si x1(prochaine case du snake en x) supérieur à la limite ou inférieur à 0 ou y1 [...] c'est perdu
        if mode == 'classic':
            if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
                if isMulti:
                    dataResult = 'Joueur 1'
                else:
                    dataResult = Length_of_snake - 1
                game_close = True
            if isMulti and (x2 >= window_width or x2 < 0 or y2 >= window_height or y2 < 0):
                dataResult = 'Joueur 2'
                game_close = True

        #Position de la prochaine case
        #ex : Position x actuel du snake est 150, j'appuie sur précedemment sur left donc 150 += -15 = 135
        x1 += x1_change
        y1 += y1_change

        if isMulti:
            x2 += x2_change
            y2 += y2_change

        # Modification de la position lorsqu'un mur est traversé
        if mode != 'classic':
            if x1 < 0:
                x1 = window_width - snake_block
            if x1 >= window_width:
                x1 = 0
            if y1 < 0:
                y1 = window_height - snake_block
            if y1 >= window_height:
                y1 = 0

            if isMulti:
                if x2 < 0:
                    x2 = window_width - snake_block
                if x2 >= window_width:
                    x2 = 0
                if y2 < 0:
                    y2 = window_height - snake_block
                if y2 >= window_height:
                    y2 = 0

        #Je redéfinis la couleur entière de la surface sinon l'ancienne position du snake reste verte
        window_surface.fill(window_color)
        window_surface.blit(window_image, (0, 0))

        #rect(surface, couleur, [posX, posY, sizeX, sizeY]) définit un rectangle qui est ici la bouffe
        #pygame.draw.rect(window_surface, window_color, [foodx, foody, snake_block, snake_block])

        if food == 2:
            window_surface.blit(image_food2, (foodx, foody))
        elif food == 3:
            window_surface.blit(image_food3, (foodx, foody))
        elif food == 4:
            window_surface.blit(image_food4, (foodx, foody))
        else:
            window_surface.blit(image_food, (foodx, foody))

        #Comme indiqué c'est la tête du serpent
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        if isMulti:
            snake_Head2 = []
            snake_Head2.append(x2)
            snake_Head2.append(y2)

        #A chaque entrée dans le while j'inscris la position(snake_head) dans la snake_list
        snake_List.append(snake_Head)
        if isMulti:
            snake_List2.append(snake_Head2)

        #Sans ce if, le snake continuerait de grandir dès le début du jeu
        if len(snake_List) > Length_of_snake:
            #Dès que la snake_list append une case en trop elle se fait delete en fonction de la longueur du snake inscrite
            del snake_List[0]

        if isMulti and len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        #Détermine si le snake se mord lui même
        #[:-1] Prend tous les éléments sauf le dernier(qui est la tête)
        if mode != 'no_limit':
            if isMulti and snake_Head == snake_Head2:
                dataResult = 'Joueur 1 & Joueur 2'
                game_close = True

            for x in snake_List[:-1]:
                if x == snake_Head:
                    if isMulti:
                        dataResult = 'Joueur 1'
                    else:
                        dataResult = Length_of_snake - 1
                    game_close = True
                if isMulti and x == snake_Head2:
                    dataResult = 'Joueur 2'
                    game_close = True

            if isMulti:
                for x in snake_List2[:-1]:
                    if x == snake_Head2:
                        dataResult = 'Joueur 2'
                        game_close = True
                    if x == snake_Head:
                        dataResult = 'Joueur 1'
                        game_close = True

        #Affichage du snake avec les rects

        if mode == 'no_limit':
            display_text(str(60 - counter), window_surface, [20, 20], color_timer)

        if isMulti:
            our_snake(snake_block, snake_List, color_snake, window_surface)
            Your_score(Length_of_snake - 1, window_surface, [800, 0], color_snake)
            our_snake(snake_block, snake_List2, color_snake2, window_surface)
            Your_score(Length_of_snake2 - 1, window_surface, [250, 0], color_snake2)
        else:
            our_snake(snake_block, snake_List, color_snake, window_surface)
            Your_score(Length_of_snake - 1, window_surface, [550, 0], color_snake)

        #On met à jour le plateau de tout ce qu'on a définit avant avec les rect(), les fill() etc..
        pygame.display.flip()

        #Si le snake percute de la bouffe alors on génère une autre bouffe et on agrandit le snake
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block

            if food == 1:
                speed = 0
                Length_of_snake += 1
            elif food == 2:
                Length_of_snake += 1
                speed = 10
            elif food == 3:
                speed = 0
                Length_of_snake += 2
            elif food == 4:
                speed = 0
                if Length_of_snake > 1:
                    Length_of_snake -= 1
                    del snake_List[0]

            food = random.randrange(1, 5)

        elif isMulti and x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block

            if food == 1:
                speed = 0
                Length_of_snake2 += 1
            elif food == 2:
                Length_of_snake2 += 1
                speed = 10
            elif food == 3:
                speed = 0
                Length_of_snake2 += 2
            elif food == 4:
                speed = 0
                if Length_of_snake2 > 1:
                    Length_of_snake2 -= 1
                    del snake_List[0]

            food = random.randrange(1, 5)

        #Vitesse du snake
        if isMulti:
            if (Length_of_snake > 6 and Length_of_snake <= 12) or (Length_of_snake2 > 6 and Length_of_snake2 <= 12):
                clock.tick(speed + 13)
            elif (Length_of_snake > 12 and Length_of_snake <= 18) or (Length_of_snake2 > 12 and Length_of_snake2 <= 18):
                clock.tick(speed + 16)
            elif (Length_of_snake > 18 and Length_of_snake <= 24) or (Length_of_snake2 > 18 and Length_of_snake2 <= 24):
                clock.tick(speed + 19)
            elif Length_of_snake > 24 or Length_of_snake2 > 24:
                clock.tick(speed + 22)
            else:
                clock.tick(speed + 10)
        else:
            if Length_of_snake > 6 and Length_of_snake <= 12:
                clock.tick(speed + 13)
            elif Length_of_snake > 12 and Length_of_snake <= 18 :
                clock.tick(speed + 16)
            elif Length_of_snake > 18 and Length_of_snake <= 24:
                clock.tick(speed + 19)
            elif Length_of_snake > 24:
                clock.tick(speed + 22)
            else:
                clock.tick(speed + 10)

    launcher()

#---------------------------------------------- FIN - JEU ---------------------------------------------



#---------------------------------------------- LANCEMENT ---------------------------------------------
def displayRanking(mode = None):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        window_surface.fill(white)
        window_surface.blit(window_image, (0, 0))

        displaySoloResults('results/solo.csv', mode, window_surface)
        displayMultiResults('results/multi.csv', mode, window_surface)

        for button in [back_button, filter_classic_button, filter_no_wall_button, filter_no_limit_button, filter_all_button]:
            button.update(window_surface)

        # Décision à prendre quand tu commences
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if filter_all_button.checkForInput(mouse_pos):
                    return displayRanking()
                if filter_classic_button.checkForInput(mouse_pos):
                    return displayRanking('Classic')
                if filter_no_wall_button.checkForInput(mouse_pos):
                    return displayRanking('No wall')
                if filter_no_limit_button.checkForInput(mouse_pos):
                    return displayRanking('No limit')
                if back_button.checkForInput(mouse_pos):
                    return False

        pygame.display.update()

def setMode():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        window_surface.fill(white)
        window_surface.blit(window_image, (0, 0))

        for button in [classic_button, no_wall_button, no_limit_button, back_button]:
            button.update(window_surface)

        # Décision à prendre quand tu commences
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if classic_button.checkForInput(mouse_pos):
                    return 'classic'
                if no_wall_button.checkForInput(mouse_pos):
                    return 'no_wall'
                if no_limit_button.checkForInput(mouse_pos):
                    return 'no_limit'
                if back_button.checkForInput(mouse_pos):
                    return False

        pygame.display.update()

def launcher():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        #Affichage de la fenetre de départ
        window_surface.fill(white)
        window_surface.blit(window_start, (0, 0))

        for button in [solo_button, multi_button, exit_button, classement_button]:
            button.update(window_surface)

        #Décision à prendre quand tu commences
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo_button.checkForInput(mouse_pos):
                    mode = setMode()
                    if mode != False:
                        gameLoop(False, mode)
                if multi_button.checkForInput(mouse_pos):
                    mode = setMode()
                    if mode != False:
                        gameLoop(True, mode)
                if exit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if classement_button.checkForInput(mouse_pos):
                    displayRanking()

        pygame.display.update()

#---------------------------------------------- FIN - LANCEMENT ---------------------------------------------

launcher()
