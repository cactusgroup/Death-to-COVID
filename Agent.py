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
        
        status can be 0 through 6 for 'healthy', 'ignorant', 'contagious',
        'infected', 'low_severity', 'high_severity', and 'deceased'
        
        vaccinated can be 0 or False for unvaccinated, 1 for 1st dose, and 2.
        
        masked can be True for always, a random function polled on expose(),
        or False for never
        
        direction can be 1 through 8, for NW through W clockwise, that is,
        1 2 3
        8 x 4
        7 6 5, with x the agent's current position.
        
        ignorant_counter is used to count down the time that the Agent stays
        ignorant.
        
        contagious_counter is to count down the time that the Agent is contagious
        
        infected_counter is used to count down each segment that the Agent is
        infected but not contagious
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
        
        # check daily whether the infection continues, abates, or kills
        self.infected_counter = 4 * 24

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
                chance -= 0.81 * chance
            elif self.vaccinated == 2:
                chance -= 0.91 * chance
            
            # 70% reduction in risk of infection by wearing a mask for health
            # care workers.
            # There is a smaller reduction for people not wearing masks all the
            # time, but let's say it is the full 70% reduction while they are 
            # wearing the mask, and none while they are not.
            # https://pubmed.ncbi.nlm.nih.gov/33347937/
            if self.masked and not callable(self.masked):
                chance -= 0.7 * chance
            elif callable(self.masked):
                if self.masked():
                    chance -= 0.7 * chance
            
            # further 70% reduction in risk of infection if the infected person
            # is also wearing a mask
            if otherAgent.masked and not callable(otherAgent.masked):
                chance -= 0.7 * chance
            elif callable(otherAgent.masked):
                if otherAgent.masked():
                    chance -= 0.7 * chance
            
            if chance > 300:
                self.status = 1 # ignorant
    
    def update(self, sim_time):
        """
        healthy status can transition to ignorant status upon successful expose()
        
        So we start the update calls in ignorant, contagious, infected,
        low_severity, high_severity, or deceased statuses.
        
        sim_time is the current simulation time in the 15-minute time units
        """
        
        # ignorant
        if self.status == 1:
            self.ignorant_counter -= 1
            if self.ignorant_counter == 0:
                self.status = 2 # -> contagious
                self.ignorant_counter = 4 * 24 * 5
        # contagious
        elif self.status == 2:
            self.contagious_counter -= 1
            if self.contagious_counter == 0:
                self.status = 3 # -> infected
                self.contagious_counter = 4 * 24 * 10
        # infected
        elif self.status == 3:
            self.infected_counter -= 1
            if self.infected_counter == 0:
                chance = self.random.random() * 1000
                
                # set upper limits on chance of dying and staying infected
                deceasedUpper = 500
                infectedUpper = 800
                if self.vaccinated == 1:
                    deceasedUpper = 300
                    infectedUpper = 680
                elif self.vaccinated == 2:
                    deceasedUpper = 100
                    infectedUpper = 500
                    
                # deceased
                if chance < deceasedUpper:
                    self.status = 6
                # continue infected
                elif deceasedUpper < chance < infectedUpper:
                    self.infected_counter = 4 * 24
                # abate
                else:
                    self.status = 1
                    self.infected_counter = 4 * 24
        # low_severity
        elif self.status == 4:
            
        # high_severity
        elif self.status == 5:
            pass
        # deceased
        else:
            self.status = 6