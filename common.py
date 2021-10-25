# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:43:56 2021

@author: Joshua
"""

import pygame
import pygame.freetype
import random
from Agent import *

# initialize library
pygame.init()

# initialize game clock
clock = pygame.time.Clock()

# constants
BACKGROUND_COLOR = (255,255,255)
(W, H) = (500 + 2*20, 500 + 3*20 + 10)
GAME_FONT = pygame.freetype.SysFont("Times New Roman", 12, bold=True)

old_healthy = pygame.image.load("./img/old_healthy.png")
old_ignorant = pygame.image.load("./img/old_ignorant.png")
old_contagious = pygame.image.load("./img/old_contagious.png")
old_infected = pygame.image.load("./img/old_infected.png")
old_deceased = pygame.image.load("./img/old_deceased.png")

young_healthy = pygame.image.load("./img/young_healthy.png")
young_ignorant = pygame.image.load("./img/young_ignorant.png")
young_contagious = pygame.image.load("./img/young_contagious.png")
young_infected = pygame.image.load("./img/young_infected.png")
young_deceased = pygame.image.load("./img/young_deceased.png")

# set up display
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('COVID Model')

# initialize all 2500 cell locations in grid
grid = { (i,j):None for i in range(50) for j in range(50) }

# initialize agents (700 for NY, 762 for FL)
NUM_AGENTS = 500
agents = {}

for i in range(NUM_AGENTS): # this will break into multiple for loops
    loc = (random.randint(0, 49), random.randint(0, 49))
    while loc in agents:
        loc = (random.randint(0, 49), random.randint(0, 49))
    agents[loc] = Agent(age=random.randint(0,1),
                        status=random.randint(0,4),
                        vaccinated=random.randint(0,2),
                        masked=random.choice([True,
                                              lambda: random.random(),
                                              False]),
                        direction=random.randint(1,8))

def draw_grids():
    # main grid
    # vertical lines
    left = 20
    top = 20
    right = 20
    bottom = 520
    for i in range(51):
        pygame.draw.line(surface=screen, color=(0,0,0,1),
                         start_pos=(left, top), end_pos=(right, bottom))
        left += 10
        right += 10
        
    # horizontal lines
    left = 20
    top = 20
    right = 520
    bottom = 20
    for i in range(51):
        pygame.draw.line(surface=screen, color=(0,0,0,1),
                         start_pos=(left, top), end_pos=(right, bottom))
        top += 10
        bottom += 10
        
    # Hospital label
    GAME_FONT.render_to(screen, (20, 530 - 2), "Hospital", (0,0,0))
    
    # hospital grid
    # vertical lines
    left = 20
    top = 540
    right = 20
    bottom = 550
    for i in range(3):
        pygame.draw.line(screen, (0,0,0,1),
                         (left, top), (right, bottom))
        left += 10
        right += 10
        
    # horizontal lines
    left = 20
    top = 540
    right = 40
    bottom = 540
    for i in range(2):
        pygame.draw.line(screen, (0,0,0,1),
                         (left, top), (right, bottom))
        top += 10
        bottom += 10

def draw_agents():
    img = ''
    for loc in agents:
        if (agents[loc].age == 0): # old
            if (agents[loc].status == 0): # healthy
                img = old_healthy
            elif (agents[loc].status == 1): # ignorant
                img = old_ignorant
            elif (agents[loc].status == 2): # contagious
                img = old_contagious
            elif (agents[loc].status == 3): # infected
                img = old_infected
            elif (agents[loc].status == 4): # deceased
                img = old_deceased
        elif (agents[loc].age == 1): # young
            if (agents[loc].status == 0): # healthy
                img = young_healthy
            elif (agents[loc].status == 1): # ignorant
                img = young_ignorant
            elif (agents[loc].status == 2): # contagious
                img = young_contagious
            elif (agents[loc].status == 3): # infected
                img = young_infected
            elif (agents[loc].status == 4): # deceased
                img = young_deceased
        
        screen.blit(img, (20 + loc[0]*10, 20 + loc[1]*10))

while True:
    # draw background
    screen.fill(BACKGROUND_COLOR)
    
    # draw grids
    draw_grids()
    
    draw_agents()
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    clock.tick(30)