#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:43:46 2021

@author: Joshua
"""

import random

class Agent: 
    def __init__(self, age, status, vaccinated, masked, direction):
        """
        age can be 0 or 1 for 'old' or 'young'
        
        status can be 0 through 4 for 'healthy', 'ignorant', 'contagious',
        'infected', and 'deceased'
        
        vaccinated can be 0 or False for unvaccinated, 1 for 1st dose, and 2.
        
        masked can be True for always, a random function polled on expose(),
        or False for never
        
        direction can be 1 through 8, for NW through W clockwise, that is,
        1 2 3
        8 x 4
        7 6 5, with x the agent's current position.
        
        ignorant_counter is used to count down the time that the Agent stays
        ignorant.
        
        contagious_counter is to count down the tme that the Agent is contagious
        """
        self.age = age
        self.status = status
        self.vaccinated = vaccinated
        self.masked = masked
        self.direction = direction
        
        self.random = random.Random(random.random())
        
        # https://medical.mit.edu/covid-19-updates/2020/10/exposed-to-covid-19-how-soon-contagious
        # most people who become ill develop symptons b/t 5 and 6 days after exposure
        self.ignorant_counter = 4 * 24 * 5
        
        # https://medical.mit.edu/covid-19-updates/2020/11/recovery-covid-19-how-long-someone-contagious
        # remain isolated at least 10 days from onset of symptoms
        self.contagious_counter = 4 * 24 * 10

    def expose(self, otherAgent):
        """
        expose this agent to COVID-19
        mask-wearing and vaccination determine whether this agent is infected
        """
        
        # if I am healthy and the other Agent is ignorant or contagious
        if self.status == 0 and (otherAgent.status == 1 or
                                 otherAgent.status == 2):
            chance = self.random.random() * 1000
            
            # 81% reduction in risk of infection by getting one dose
            # 91% reduction by getting two doses
            # https://www.cdc.gov/media/releases/2021/p0607-mrna-reduce-risks.html
            if self.vaccinated == 1:
                if chance > 500:
                    chance -= 0.91 * (chance - 500)
            elif self.vaccinated == 2:
                if chance > 500:
                    chance -= 0.81 * (chance - 500)
            
            # 70% reduction in risk of infection by wearing a mask for health
            # care workers.
            # There is a smaller reduction for people not wearing masks all the
            # time, but let's say it is the full 70% reduction while they are 
            # wearing the mask, and none while they are not.
            # https://pubmed.ncbi.nlm.nih.gov/33347937/
            if self.masked and not callable(self.masked):
                if chance > 500:
                    chance -= 0.7 * (chance - 500)
            elif callable(self.masked):
                if self.masked() and chance > 500:
                    chance -= 0.7 * (chance - 500)
            
            # further 70% reduction in risk of infection if the infected person
            # is also wearing a mask
            if otherAgent.masked and not callable(otherAgent.masked):
                if chance > 500:
                    chance -= 0.7 * (chance - 500)
            elif callable(otherAgent.masked):
                if otherAgent.masked() and chance > 500:
                    chance -= 0.7 * (chance - 500)
            
            if chance > 500:
                self.status = 1 # ignorant
    
    def update():
        """
        healthy status can transition to ignorant status upon successful expose()
        
        So we start the update calls in ignorant, contagious, infected,
        low_severity, high_severity, or deceased statuses.
        """
        
        if self.status == 1: # ignorant
            self.ignorant_counter -= 1
            if self.ignorant_counter == 0:
                