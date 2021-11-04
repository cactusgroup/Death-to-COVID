# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:43:56 2021

@author: Joshua
"""

import pygame
import pygame.freetype

import random

from tkinter import Tk
from tkinter.filedialog import askopenfile, asksaveasfile

import pickle

from Agent import Agent
from status_constants import AGE, STATUS


# Initialize library
pygame.init()
# Initialize game clock
clock = pygame.time.Clock()
# Initialize Tk graphics for file dialogs
Tk().withdraw()

# Constants
# colors
BACKGROUND_COLOR = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
light_gray = (144,144,144)
dark_gray = (110,110,110)

# screen dimensions
(W, H) = (500 + 2*20, 500 + 3*20 + 10)

# font for game text
GAME_FONT = pygame.freetype.SysFont("Times New Roman", 12, bold=True)

# images
path = {i : './img/' + i + '.png' for i in [
    'old_healthy',
    'old_ignorant',
    'old_contagious',
    'old_infected',
    'old_low_severity',
    'old_high_severity',
    'old_deceased',
    
    'young_healthy',
    'young_ignorant',
    'young_contagious',
    'young_infected',
    'young_low_severity',
    'young_high_severity',
    'young_deceased']}

old_healthy = pygame.image.load(path['old_healthy'])
old_ignorant = pygame.image.load(path['old_ignorant'])
old_contagious = pygame.image.load(path['old_contagious'])
old_infected = pygame.image.load(path["old_infected"])
old_low_severity = pygame.image.load(path['old_low_severity'])
old_high_severity = pygame.image.load(path['old_high_severity'])
old_deceased = pygame.image.load(path["old_deceased"])

young_healthy = pygame.image.load(path["young_healthy"])
young_ignorant = pygame.image.load(path["young_ignorant"])
young_contagious = pygame.image.load(path["young_contagious"])
young_infected = pygame.image.load(path["young_infected"])
young_low_severity = pygame.image.load(path['young_low_severity'])
young_high_severity = pygame.image.load(path['young_high_severity'])
young_deceased = pygame.image.load(path["young_deceased"])

# Code
# Set up display
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('COVID Model')

# initialize all 2500 cell locations in grid
grid = { (i,j):None for i in range(50) for j in range(50) }

# Initialize agents (700 for NY, 762 for FL)
NUM_OLD = 229
NUM_YOUNG = 471
agents = {} # {(row, col): Agent}
hospital = {} # {col: Agent}

# old
for i in range(NUM_OLD):
    loc = (random.randint(0, 49), random.randint(0, 49))
    while loc in agents:
        loc = (random.randint(0, 49), random.randint(0, 49))
    agents[loc] = Agent(age=AGE['old'],
                        status=STATUS['healthy'],
                        vaccinated=0,
                        masked=False,
                        direction=random.randint(1,8))

# young
for i in range(NUM_YOUNG):
    loc = (random.randint(0, 49), random.randint(0, 49))
    while loc in agents:
        loc = (random.randint(0, 49), random.randint(0, 49))
    agents[loc] = Agent(age=AGE['young'],
                        status=STATUS['healthy'],
                        vaccinated=0,
                        masked=False,
                        direction=random.randint(1,8))

# ignorant
old = 0; young = 0
while old < 1 or young < 1:
    k, v = random.choice([(k, v) for k, v in agents.items()])
    if (v.age == AGE['old'] and old < 1):
        v.status = STATUS['ignorant']
        old = 1
    elif (v.age == AGE['young'] and young < 1):
        v.status = STATUS['ignorant']
        young = 1

# partially-masking
def masked():
    return random.random() < 0.35

old = 0; young = 0
while old < 35 or young < 95:
    k, v = random.choice([(k, v) for k, v in agents.items()])
    if (v.age == AGE['old'] and old < 35):
        v.masked = masked
        old += 1
    elif (v.age == AGE['young'] and young < 95):
        v.masked = masked
        young += 1

# Draw functions
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
    GAME_FONT.render_to(screen, (20, 20 + 500 + 8), "Hospital", (0,0,0))
    
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
    images = [[old_healthy, old_ignorant, old_contagious, old_infected,
               old_low_severity, old_high_severity, old_deceased],
              [young_healthy, young_ignorant, young_contagious,
               young_infected, young_low_severity, young_high_severity,
               young_deceased]]
    img = ''
    for loc, agent in agents.items():
        img = images[agent.age][agent.status]
        screen.blit(img, (20 + loc[0]*10, 20 + loc[1]*10))

def draw_hospital():
    images = [[old_healthy, old_ignorant, old_contagious, old_infected,
               old_low_severity, old_high_severity, old_deceased],
              [young_healthy, young_ignorant, young_contagious,
               young_infected, young_low_severity, young_high_severity,
               young_deceased]]
    img = ''
    for col, agent in hospital.items():
        img = images[agent.age][agent.status]
        screen.blit(img, (20 + col*10, 20 + 500 + 20))

# Animation control functions
def make_button(msg, x):
    y = 20 + 500 + 10
    w = 90
    h = 20
    # mouse[0] = x coordinate
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, dark_gray, (x,y,w,h))
        else:
            pygame.draw.rect(screen, light_gray, (x,y,w,h))
    else:
        pygame.draw.rect(screen, gray, (x,y,w,h))
    surf, bounds = GAME_FONT.render(msg, fgcolor=(0,0,0))
    bounds.center = (x + w/2, y + h/2)
    screen.blit(surf, bounds);

def save():
    file = asksaveasfile('wb')
    pickle.dump((agents,hospital), file)
    file.close()
    
def load():
    global agents, hospital
    file = askopenfile('rb')
    agents, hospital = pickle.load(file)
    file.close()
    
# Move and Expose
def get_adjacent(loc, type='cells'):
    result = []
    for x, y in [(loc[0]+i, loc[1]+j)
                 for i in (-1,0,1) for j in (-1,0,1)
                 if i != 0 or j != 0]:
        if type == 'cells' and (x, y) in grid and (x, y) not in agents:
            result.append((x, y))
        elif type == 'agents' and (x, y) in agents:
            result.append((x, y))
            
    random.shuffle(result)
    return result

# def cell_direction(loc, cellLoc):
#     x1, y1 = loc
#     x2, y2 = cellLoc
    
#     if x2 == x1:
#         if y2 < y1:
#             return 2
#         if y2 > y1:
#             return 6
#     if y2 == y1:
#         if x2 < x1:
#             return 8
#         if x2 > x1:
#             return 4
#     if x2 > x1 and y2 > y1:
#         return 5
#     if x2 < x1 and y2 < y1:
#         return 1
#     if x2 > x1 and y2 < y1:
#         return 3
#     if x2 < x1 and y2 > y1:
#         return 7

# Game loop
speed = 'slow'
sim_time = 0
while True:
    # draw background
    screen.fill(BACKGROUND_COLOR)
    
    # Draw
    # draw grids
    draw_grids()
    # draw agents (on main grid)
    draw_agents()
    # draw hospital
    draw_hospital()
    
    # draw button graphics (animation control)
    # Save    
    make_button('Save', x=100)
    # Load
    make_button('Load', x=200)
    # Fast
    make_button('Fast', x=300)
    # Slow
    make_button('Slow', x=400)
    
    # Process
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = event.pos
            if event.button == 1:
                # Save
                if (100 < mouse[0] < 190 and 530 < mouse[1] < 550):
                    save()
                # Load
                if (200 < mouse[0] < 290 and 530 < mouse[1] < 550):
                    load()
                # Fast
                if (300 < mouse[0] < 390 and 530 < mouse[1] < 550):
                    speed = 'fast'
                # Slow
                if (400 < mouse[0] < 490 and 530 < mouse[1] < 550):
                    speed = 'slow'
    
    # Expose
    for k, v in {k: v for k, v in agents.items()
                 if (v.status == STATUS['ignorant'] or
                     v.status == STATUS['contagious'])}.items():
        exposees_ks = get_adjacent(k, 'agents')
        for k in exposees_ks:
            agents[k].expose(v)
    
    # Move
    newAgents = {k: v for k, v in agents.items()}
    for k in agents:
        cells = get_adjacent(k)
        for cell in cells:
            if cell not in newAgents:
                newAgents[cell] = newAgents.pop(k)
                break
    
    # Update
    for k in agents:
        agents[k].update(sim_time)
                    
    agents = newAgents
    
    # Finished Drawing
    pygame.display.flip()
    # update simulation time
    sim_time += 1
    
    # Set Framerate
    if speed=='fast':
        clock.tick(30) # 18 minute simulation
    elif speed=='slow':
        clock.tick(1) # 9.6 hour simulation
        
        