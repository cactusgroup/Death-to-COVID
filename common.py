# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:43:56 2021

@author: Joshua Chu
"""

import pygame
import pygame.freetype

import random
import pickle
import sys
import os

from tkinter import Tk
from tkinter.filedialog import askopenfile, asksaveasfile

sys.path.append(os.path.abspath('./help'))
from AgentsGen import generate_agents
from Constants import Status, Colors, Age
from Images import (old_healthy, old_ignorant, old_contagious, old_infected,
                    old_low_severity, old_high_severity, old_deceased,
                    young_healthy, young_ignorant, young_contagious,
                    young_infected, young_low_severity, young_high_severity,
                    young_deceased)

# Initialize library
pygame.init()
# Initialize game clock
clock = pygame.time.Clock()
# Initialize Tk graphics for file dialogs
Tk().withdraw()

# Constants
# screen dimensions
(W, H) = (500 + 3*20 + 300, 500 + 3*20 + 10)
# font for game text
GAME_FONT = pygame.freetype.SysFont("Times New Roman", 12, bold=True)

# Code
# Set up display
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('COVID Model')

# (sim_time, rate)
# masking
full_masking_rate = [(0, .2), (4*16*30, .4), (4*16*10*30, .82)]
part_masking_rate = [(0, .2)]
part_masking_percent = 0.8
# vaccinations
vaccinated_1stdose_old = [(0, .0),
                          (4*16*9*30 + 17*4*16, .0),
                          (4*16*12*30 + 5*4*16, .442-.213),
                          (4*16*13*30, .669-.432),
                          (4*16*16*30, .858-.790)]
vaccinated_fully_old = [(0, .0),
                        (4*16*9*30 + 17*4*16, .0),
                        (4*16*12*30 + 5*4*16, .213),
                        (4*16*13*30, .432),
                        (4*16*16*30, .790)]
vaccinated_1stdose_young = [(0, .0),
                            (4*16*9*30 + 17*4*16, .0),
                            (4*16*11*30 + 13*4*16, .1477),
                            (4*16*13*30, .337-.1729),
                            (4*16*16*30, .6946-.6266)]
vaccinated_fully_young = [(0, .0),
                          (4*16*9*30 + 17*4*16, .0),
                          (4*16*11*30 + 13*4*16, .0),
                          (4*16*13*30, .1729),
                          (4*16*16*30, .6266)]

# initialize all 2500 cell locations in grid
grid = { (i,j):None for i in range(50) for j in range(50) }

# Initialize agents (700 for NY, 762 for FL)
nOld = 229
nYoung = 471
assert nOld + nYoung == 700

# {(row, col): Agent}, 50x50 grid of agents
agents = generate_agents(nOld,nYoung,
                          
                          1,1,
                          
                          part_masking_rate[0][1]*nOld,
                          part_masking_rate[0][1]*nYoung,
                          part_masking_percent,
                          
                          full_masking_rate[0][1]*nOld,
                          full_masking_rate[0][1]*nYoung)
# {col: Agent}, 1x2 grid of hospital beds
hospital = {}
# {(row, col): Agent}, 30x30 grid of agents
quarantine = {}

# Draw functions
def draw_grids():
    # main grid
    # vertical lines
    left = 20
    top = 20
    right = 20
    bottom = 520
    for i in range(51):
        pygame.draw.line(surface=screen, color=Colors.black,
                         start_pos=(left, top), end_pos=(right, bottom))
        left += 10
        right += 10
        
    # horizontal lines
    left = 20
    top = 20
    right = 520
    bottom = 20
    for i in range(51):
        pygame.draw.line(surface=screen, color=Colors.black,
                         start_pos=(left, top), end_pos=(right, bottom))
        top += 10
        bottom += 10
        
    # quarantine label
    GAME_FONT.render_to(screen, (2*20 + 500, 20 + 8), "Quarantine",
                        Colors.black)
    
    # quarantine grid
    # vertical lines
    left = 540
    top = 40
    right = 540
    bottom = 340
    for i in range(31):
        pygame.draw.line(screen, Colors.black, (left, top), (right, bottom))
        left += 10
        right += 10
        
    # horizontal lines
    left = 540
    top = 40
    right = 840
    bottom = 40
    for i in range(31):
        pygame.draw.line(screen, Colors.black, (left, top), (right, bottom))
        top += 10
        bottom += 10
    
    # hospital label
    GAME_FONT.render_to(screen, (20, 20 + 500 + 8), "Hospital", Colors.black)
    
    # hospital grid
    # vertical lines
    left = 20
    top = 540
    right = 20
    bottom = 550
    for i in range(3):
        pygame.draw.line(screen, (0,0,0,1), (left, top), (right, bottom))
        left += 10
        right += 10
        
    # horizontal lines
    left = 20
    top = 540
    right = 40
    bottom = 540
    for i in range(2):
        pygame.draw.line(screen, (0,0,0,1), (left, top), (right, bottom))
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
            pygame.draw.rect(screen, Colors.dark_gray, (x,y,w,h))
        else:
            pygame.draw.rect(screen, Colors.light_gray, (x,y,w,h))
    else:
        pygame.draw.rect(screen, Colors.gray, (x,y,w,h))
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
    global agents
    result = []
    for x, y in [(loc[0]+i, loc[1]+j)
                  for i in (-1,0,1) for j in (-1,0,1)
                  if i != 0 or j != 0]:
        if type == 'cells' and (x, y) in grid and (x, y) not in agents:
            result.append((x, y))
        elif type == 'agents' and (x, y) in agents:
            result.append((x, y))
            
    agents[loc].random.shuffle(result)
    return result

def expose_agents():
    global agents
    # Expose
    for k, v in {k: v for k, v in agents.items()
                  if (v.status == Status.ignorant or
                      v.status == Status.contagious)}.items():
        exposees_ks = get_adjacent(k, 'agents')
        for k in exposees_ks:
            agents[k].expose(v)
            
def move_agents():
    global agents
    # Move if not deceased
    newAgents = {k: v for k, v in agents.items()}
    for k in agents:
        if agents[k].status != Status.deceased:
            cells = get_adjacent(k)
            for cell in cells:
                if cell not in newAgents:
                    newAgents[cell] = newAgents.pop(k)
                    break
    agents = newAgents

# Hospital functions
def check_hospital_calls():
    global agents, sim_time
    # Check for calls to the hospital
    delete_list = []
    for k in {k: v for k, v in agents.items()
              if (v.status == Status.contagious or
                  v.status == Status.infected)}:
        status = agents[k].status
        
        agents[k].status = Status.low_severity
        
        if not to_hospital(k, sim_time):
            agents[k].status = status
            break
        else:
            delete_list.append(k)
    for el in delete_list:
        del agents[el]

def check_discharges():
    global agents, hospital
    # Check for agents returning from the hospital
    delete_list = []
    for k in {k: v for k, v in hospital.items()
              if v.status == Status.healthy}:
        loc = (random.randint(0, 49), random.randint(0, 49))
        while loc in agents:
            loc = (random.randint(0, 49), random.randint(0, 49))
        agents[loc] = hospital[k]
        delete_list.append(k)
    for el in delete_list:
        del hospital[k]

def find_bed():
    """
    Checks for and returns an empty bed by column location or None if there is
    no bed available.

    Parameters
    ----------

    Returns
    -------
    integer (column index)
        Returns a column index that can be used to reserve a bed in the
        hospital, or None is there is no bed available.
        
    @author: Jason Mejia
    """
    global hospital
    if 0 in hospital and 1 in hospital:
        return None
    if 0 in hospital:
        return 1 # second column index
    if 1 in hospital:
        return 0 # first column index
    if len(hospital.items()) == 0:
        return 0 # first column index

hospitalized_old = 0
hospitalized_young = 0
hospitalized_m_old = []
hospitalized_m_young = []
def to_hospital(loc, sim_time):
    """
    Sends an agent specified by its grid location to an open bed in the
    hospital if there is an open bed; otherwise, does nothing to the agent.

    Parameters
    ----------
    loc : integer
        grid location of an agent.

    Returns
    -------
    Returns True if the agent was removed to a hospital bed, and False if
    nothing happened.
    
    @author: Jason Mejia
    """
    global hospitalized_old, hospitalized_young
    global hospitalized_m_old, hospitalized_m_young
    global agents, hospital
    
    if sim_time % (4*16*30) == 0 and sim_time != 0 or sim_time == 34559:
        hospitalized_m_old.append(hospitalized_old)
        hospitalized_m_young.append(hospitalized_young)
        hospitalized_old = hospitalized_young = 0
    
    bed = find_bed()
    if bed != None:
        hospital[bed] = agents[loc]
        
        if agents[loc].age == Age.old:
            hospitalized_old += 1
        elif agents[loc].age == Age.young:
            hospitalized_young += 1
        
        return True
    return False

# death function
deceased_old = 0
deceased_young = 0
deceased_m_old = []
deceased_m_young = []
def collect_deceased(sim_time):
    global deceased_old, deceased_young
    global deceased_m_old, deceased_m_young
    global agents, hospital
    
    if sim_time % (4*16*30) == 0 and sim_time != 0 or sim_time == 34559:
        deceased_m_old.append(deceased_old)
        deceased_m_young.append(deceased_young)
        deceased_old = deceased_young = 0
    
    agents_del_list = []
    for loc in {k: v for k, v in agents.items()
                if v.status == Status.deceased}:
        agents_del_list.append(loc)
        
        if (agents[loc].age == Age.old):
            deceased_old += 1
        elif (agents[loc].age == Age.young):
            deceased_young += 1
            
    for el in agents_del_list:
        del agents[el]
    
    hosp_del_list = []
    for col in {k: v for k, v in hospital.items()
                if v.status == Status.deceased}:
        hosp_del_list.append(col)
        
        if hospital[col].age == Age.old:
            deceased_old += 1
        elif hospital[col].age == Age.young:
            deceased_young += 1
            
    for el in hosp_del_list:
        del hospital[el]

# Game loop
speed = 'slow'
sim_time = 0
while True:
    # draw background
    screen.fill(Colors.bg_color)
    
    # Draw
    draw_grids()
    draw_agents()
    draw_hospital()
    
    # draw button graphics (animation control)
    make_button('Save', x=100)
    make_button('Load', x=200)
    make_button('Fast', x=300)
    make_button('Slow', x=400)
    
    # Process
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = event.pos
            if event.button == 1:
                if (100 < mouse[0] < 190 and 530 < mouse[1] < 550):
                    save()
                if (200 < mouse[0] < 290 and 530 < mouse[1] < 550):
                    load()
                if (300 < mouse[0] < 390 and 530 < mouse[1] < 550):
                    speed = 'fast'
                if (400 < mouse[0] < 490 and 530 < mouse[1] < 550):
                    speed = 'slow'
    
    expose_agents()
    move_agents()
    check_hospital_calls()
    check_discharges()
    collect_deceased(sim_time)

    # Update
    for k in agents:
        agents[k].update(sim_time)
    for k in hospital:
        hospital[k].update(sim_time)
                    
    # Finished Drawing
    pygame.display.flip()
    # update simulation time
    sim_time += 1
    if sim_time == 34560:
        break
    
    # Set Framerate
    if speed=='fast':
        clock.tick(30) # 18 minute simulation
    elif speed=='slow':
        clock.tick(1) # 9.6 hour simulation

months = {k: v for k, v in zip([0,1,2,3,4,5,6,7,8,9,10,11],
                               ['March', 'April', 'May',
                                'June', 'July', 'August',
                                'September', 'October', 'November',
                                'December', 'January', 'February'])}
print('           \t Hospitalizations \t Deaths')
print('           \t Old    Young     \t Old     Young')
for month in range(len(hospitalized_m_old)):
    print(f'{months[month % 12]} \t '
          f'{hospitalized_m_old[month] / (nOld + nYoung)*10**-5:4.2} ')
    
pygame.quit()