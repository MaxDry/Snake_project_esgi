import pygame
import datetime
import csv
import re

#Génère le snake sur la surface avec les rect()
def our_snake(snake_block, snake_list, color, window_surface):
    for x in snake_list:
        pygame.draw.rect(window_surface, color, [x[0], x[1], snake_block, snake_block])

def Your_score(score, window_surface, pos, color):
    text = pygame.font.SysFont("comicsansms", 35)

    value = text.render("Score : " + str(score), True, color)
    window_surface.blit(value, pos)

def display_text(data, window_surface, pos, color):
    text = pygame.font.SysFont("comicsansms", 35)

    value = text.render(data, True, color)
    window_surface.blit(value, pos)

def write_solo(isNotWritable, score, mode):
    if not isNotWritable:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")

        with open('results/solo.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, mode, score])

def addResult(data, mode, file):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    with open(file, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, mode, data])

def getResults(filename, mode = None):
    file = open(filename)
    reader = csv.reader(file)

    rows = []
    for row in reader:
        rows.append(row)

    if mode is None:
        return rows[::-1][0:20]
    else:
        return filterResultsByMode(rows, mode)

def filterResultsByMode(rows, mode):
    result = []
    for row in rows[::-1]:
        if row[1] == mode and len(result) < 20:
            result.append(row)

    return result

def displaySoloResults(file, mode, window_surface):
    soloResults = getResults(file, mode)

    text = pygame.font.SysFont("comicsansms", 18)
    value = text.render('                        SOLO                        ', True, 'red')
    window_surface.blit(value, [150, 170])
    text = pygame.font.SysFont("comicsansms", 14)
    value = text.render('----------------------------------------------', True, 'red')
    window_surface.blit(value, [150, 185])
    value = text.render('            Date             |     Mode    |   Score', True, 'red')
    window_surface.blit(value, [150, 200])
    value = text.render('----------------------------------------------', True, 'red')
    window_surface.blit(value, [150, 210])

    text = pygame.font.SysFont("comicsansms", 12)
    pos = 210
    for data in soloResults:
        pos += 15
        value = text.render(data[0] + '    |    ' + data[1] + '    |        ' + data[2], True, 'red')
        window_surface.blit(value, [150, pos])

def displayMultiResults(file, mode, window_surface):
    multiResults = getResults(file, mode)

    text = pygame.font.SysFont("comicsansms", 18)
    value = text.render('                         MULTI                        ', True, 'red')
    window_surface.blit(value, [830, 170])
    text = pygame.font.SysFont("comicsansms", 14)
    value = text.render('--------------------------------------------------', True, 'red')
    window_surface.blit(value, [830, 185])
    value = text.render('            Date              |     Mode   |     Gagnant', True, 'red')
    window_surface.blit(value, [830, 200])
    value = text.render('--------------------------------------------------', True, 'red')
    window_surface.blit(value, [830, 210])

    text = pygame.font.SysFont("comicsansms", 12)
    pos = 210
    for data in multiResults:
        pos += 15
        value = text.render(data[0] + '    |    ' + data[1] + '    |     ' + data[2], True, 'red')
        window_surface.blit(value, [830, pos])