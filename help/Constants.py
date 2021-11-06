# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:22:09 2021

@author: Joshua Chu
"""

# Agent parameters
class Age:
    old = 0
    young = 1

class Status:
    healthy = 0
    ignorant = 1
    contagious = 2
    infected = 3
    low_severity = 4
    high_severity = 5
    deceased = 6

class Vax:
    non_vax = 0
    first = 1
    second = 2
    
class Colors:
    bg_color = (255,255,255)
    black = (0,0,0)
    gray = (128,128,128)
    light_gray = (144,144,144)
    dark_gray = (110,110,110)
    
class ImgPaths:
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
    
    old_healthy = path['old_healthy']
    old_ignorant = path['old_ignorant']
    old_contagious = path['old_contagious']
    old_infected = path["old_infected"]
    old_low_severity = path['old_low_severity']
    old_high_severity = path['old_high_severity']
    old_deceased = path["old_deceased"]

    young_healthy = path["young_healthy"]
    young_ignorant = path["young_ignorant"]
    young_contagious = path["young_contagious"]
    young_infected = path["young_infected"]
    young_low_severity = path['young_low_severity']
    young_high_severity = path['young_high_severity']
    young_deceased = path["young_deceased"]
