#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:43:46 2021

@author: Joshua
"""

import random

class Agent: 
    def __init__(self, vaccinated, masked):
        """
        vaccinated can be 0 or False for unvaccinated, 1 for 1st dose, and 2.
        
        masked can be True for always, a random function polled on expose(),
        or False for never
        """
        self.vaccinated = vaccinated
        self.masked = masked
        self.random = random.Random(random.random())

    def expose(self):
        """
        expose this agent to COVID-19
        mask-wearing and vaccination determine whether this agent is infected
        """
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
        # time, but it is unknown how much smaller the reduction is.
        # https://pubmed.ncbi.nlm.nih.gov/33347937/
        if self.masked and not callable(self.masked):
            if chance > 500:
                chance -= 0.7 * (chance - 500)
        elif callable(self.masked):
            if self.masked() and chance > 500:
                chance -= 0.5 * (chance - 500)