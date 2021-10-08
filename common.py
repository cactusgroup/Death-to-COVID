# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:43:56 2021

@author: Joshua
"""

import pygame

# constants
background_color = (255,255,255)
(W, H) = (500 + 2*20, 500 + 3*20 + 10)

# set up display
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('COVID Model')

def draw_grid():
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
    """I don't know how to do this."""
    
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
    
    # draw grid
    draw_grid()
    
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()