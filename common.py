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

# constants
background_color = (255,255,255)
(W, H) = (500 + 2*20, 500 + 3*20 + 10)
GAME_FONT = pygame.freetype.SysFont("Times New Roman", 12, bold=True)

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
                                              lambda (): return random.random(),
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

while True:
    # draw background
    screen.fill(background_color)
    
    # draw grids
    draw_grids()
    
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()