# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:43:56 2021

@author: Joshua
"""

import pygame

# constants
background_color = (255,255,255)
(width, height) = (500 + 2*20, 500 + 3*20 )

# set up display
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('COVID Model')
screen.fill(background_color)

#
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()