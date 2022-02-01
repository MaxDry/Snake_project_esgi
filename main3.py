import pygame
import time
import random

from pygame import image
from pygame.transform import scale

pygame.init()

#Nom de la fenêtre
pygame.display.set_caption("Snake ESGI")

#Taille de la fenêtre
#Forcément des multiples de la taille du standard block sinon ça fonctionne pas !
window_width = 1280
window_height = 720
window_resolution = (window_width,window_height)

#Définition de la fenêtre de jeu
window_surface = pygame.display.set_mode(window_resolution)

window_image = pygame.image.load("wallpaper_snake.png").convert_alpha()
window_start = pygame.image.load("wallpaper_start.png").convert_alpha()
window_lose = pygame.image.load("wallpaper_lose.png").convert_alpha()
image_food = pygame.image.load("framboise.png").convert_alpha()
image_food = pygame.transform.scale(image_food, (40, 40)) 
food_image = image_food.get_rect()

#Buttons
start_btn_image = pygame.image.load('start_btn.png').convert_alpha()
restart_btn_image = pygame.image.load('restart_btn.png').convert_alpha()
exit_btn_image = pygame.image.load('exit_btn.png').convert_alpha()
solo_btn_image = pygame.image.load('solo.png').convert_alpha()
solo_btn_image = pygame.transform.scale(solo_btn_image, (200, 100))
multi_btn_image = pygame.image.load('limit.png').convert_alpha()
multi_btn_image = pygame.transform.scale(multi_btn_image, (200, 100))

#button class
class Button():
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.scaled = True

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False

        window_surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


start_button = Button(550, 350, start_btn_image, 0.8)
restart_button = Button(520, 350, restart_btn_image, 0.8)
exit_button = Button(565, 500, exit_btn_image, 0.8)
solo_button = Button(400, 350, solo_btn_image, 0.8)
multi_button = Button(700, 350, multi_btn_image, 0.8)

#Font des écritures de fin et du score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

snake_block = 40

#Colors
window_color=(143,151,121)
color_snake=(11, 102, 35)
color_snake2=(255,0,0)
red = (255, 0, 0)
white = (255, 255, 255)
game_start = False

modeWall = False

#Initialisation de clock pour utiliser tick() qui équivaut à un time.sleep()
clock = pygame.time.Clock()


#Génération message fin lorsque tu perds
def message(msg,color):
    mesg = font_style.render(msg, True, color)
    window_surface.blit(mesg, [window_width/6, window_height/3])

#Génère le snake sur la surface avec les rect()
def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(window_surface, color, [x[0], x[1], snake_block, snake_block])

def Your_score(score, position, color):
    value = score_font.render("Score : " + str(score), True, color)
    window_surface.blit(value, position)

def gameLoop():
    game_over = False
    game_close = False

    #Emplacement de départ
    x1 = window_width * 0.25
    y1 = window_height * 0.5

    # Emplacement de départ
    x2 = window_width * 0.75
    y2 = window_height * 0.5

    #Emplacement vers lequel le snake se dirige étant incrémenté dans le while
    x1_change = 0       
    y1_change = 0

    # Emplacement vers lequel le snake se dirige étant incrémenté dans le while
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

    #Logique du code
    while not game_over:
        #Effectue le traitement de tout ce while à chaque fois que le snake avance d'une case
        while game_close == True:
            #Affichage de la fenetre si tu as perdu
            window_surface.fill(white)
            window_surface.blit(window_lose, (0, 0))
            if restart_button.draw():
                gameLoop()
            if exit_button.draw():
                game_over = True
                game_close = False
            pygame.display.update()
            #Décision à prendre quand tu as perdu
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # 'Q' Fin du jeu
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    # 'C' Relance du jeu
                    if event.key == pygame.K_c:
                        gameLoop()
        #A chaque fois que j'appuie sur une touche il garde en mémoire la touche
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

                if event.key == pygame.K_q:
                    x2_change = -snake_block
                    y2_change = 0
                elif event.key == pygame.K_d:
                    x2_change = snake_block
                    y2_change = 0
                elif event.key == pygame.K_z:
                    y2_change = -snake_block
                    x2_change = 0
                elif event.key == pygame.K_s:
                    y2_change = snake_block
                    x2_change = 0

        
        # Si x1(prochaine case du snake en x) supérieur à la limite ou inférieur à 0 ou y1 [...] c'est perdu
        if modeWall:
            if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
                game_close = True
            if x2 >= window_width or x2 < 0 or y2 >= window_height or y2 < 0:
                game_close = True

        #Position de la prochaine case
        #ex : Position x actuel du snake est 150, j'appuie sur précedemment sur left donc 150 += -15 = 135
        x1 += x1_change
        y1 += y1_change

        x2 += x2_change
        y2 += y2_change

        if not modeWall:
            if x1 < 0:
                x1 = window_width - snake_block

            if x1 >= window_width:
                x1 = 0

            if y1 < 0:
                y1 = window_height - snake_block

            if y1 >= window_height:
                y1 = 0

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
        window_surface.blit(image_food, (foodx, foody))
        
        #Comme indiqué c'est la tête du serpent
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_Head2 = []
        snake_Head2.append(x2)
        snake_Head2.append(y2)

        #A chaque entrée dans le while j'inscris la position(snake_head) dans la snake_list
        snake_List.append(snake_Head)
        snake_List2.append(snake_Head2)

        #Sans ce if, le snake continuerait de grandir dès le début du jeu
        if len(snake_List) > Length_of_snake:
            #Dès que la snake_list append une case en trop elle se fait delete en fonction de la longueur du snake inscrite
            del snake_List[0]

        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        #Détermine si le snake se mord lui même
        #[:-1] Prend tous les éléments sauf le dernier(qui est la tête)
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for x in snake_List2[:-1]:
            if x == snake_Head2:
                game_close = True

        #Affichage du snake avec les rects
        our_snake(snake_block, snake_List, color_snake)
        our_snake(snake_block, snake_List2, color_snake2)
        Your_score(Length_of_snake - 1, [250, 0], color_snake)
        Your_score(Length_of_snake2 - 1, [800, 0], color_snake2)

        #On met à jour le plateau de tout ce qu'on a définit avant avec les rect(), les fill() etc..
        pygame.display.flip()

        #Si le snake percute de la bouffe alors on génère une autre bouffe et on agrandit le snake
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        if x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
            Length_of_snake2 += 1

        #Vitesse du snake
        if (Length_of_snake > 6 and Length_of_snake) <= 12 or (Length_of_snake2 > 6 and Length_of_snake2 <= 12):
            clock.tick(13)
        elif (Length_of_snake > 12 and Length_of_snake <= 18) or (Length_of_snake2 > 12 and Length_of_snake2 <= 18):
            clock.tick(16)
        elif (Length_of_snake > 18 and Length_of_snake <= 24) or (Length_of_snake2 > 18 and Length_of_snake2 <= 24):
            clock.tick(19)
        elif Length_of_snake > 24 or Length_of_snake2 > 24:
            clock.tick(22)
        else:
            clock.tick(10)

    pygame.quit()
    quit()

def setMode():
    while 1:
        window_surface.fill(white)
        window_surface.blit(window_image, (0, 0))

        if solo_button.draw():
            return True
        if multi_button.draw():
            return False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

#Launcher
while game_start == False:
    #Affichage de la fenetre de départ
    window_surface.fill(white)
    window_surface.blit(window_start, (0, 0))
    
    if start_button.draw():
        modeWall = setMode()
        gameLoop()
    if start_button.draw():
        modeWall = setMode()
        gameLoop()
    if exit_button.draw():
        break

    pygame.display.update()
    #Décision à prendre quand tu commences
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # 'C' Relance du jeu
            if event.key == pygame.K_c:
                gameLoop()
