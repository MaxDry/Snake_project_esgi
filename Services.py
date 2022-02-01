import pygame

#Génère le snake sur la surface avec les rect()
def our_snake(snake_block, snake_list, color, window_surface):
    for x in snake_list:
        pygame.draw.rect(window_surface, color, [x[0], x[1], snake_block, snake_block])

def Your_score(score, window_surface, pos, color):
    score_font = pygame.font.SysFont("comicsansms", 35)

    value = score_font.render("Score : " + str(score), True, color)
    window_surface.blit(value, pos)
