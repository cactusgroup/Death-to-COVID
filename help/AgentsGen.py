# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:35:32 2021

@author: Joshua Chu
"""
import random

from Agent import Agent
from Constants import Age, Status

def generate_agents(nOld, nYoung, nIgnorantOld, nIgnorantYoung,
                    nPartMaskedOld, nPartMaskedYoung, partMaskedPercent,
                    nFullMaskedOld, nFullMaskedYoung):
    """
    Parameters
    ----------
    nOld : integer
        Number of old people in this community.
    nYoung : integer
        Number of young people in this community.
    nIgnorantOld : integer
        Number of infected old people who don't know they're infected.
    nIgnorantYoung : integer
        Number of infected young people who don't know they're infected.
    nPartMaskedOld : integer
        Number of partially-masking old people.
    nPartMaskedYoung : integer
        Number of partially-masking young people.
    partMaskedPercent : float
        Percentage expressed as a decimal that partially-masked people are
        masked.
    nFullMaskedOld : integer
        Number of fully-masked old people.
    nFullMaskedYoung : integer
        Number of fully-masked young people.

    Returns
    -------
    dict
        Returns a dict of agents, representing the community.

    """
    agents = {}
    
    # old
    for i in range(nOld):
        loc = (random.randint(0, 49), random.randint(0, 49))
        while loc in agents:
            loc = (random.randint(0, 49), random.randint(0, 49))
        agents[loc] = Agent(age=Age.old,
                            status=Status.healthy,
                            vaccinated=0,
                            masked=False,
                            direction=random.randint(1,8))
    
    
    # young
    for i in range(nYoung):
        loc = (random.randint(0, 49), random.randint(0, 49))
        while loc in agents:
            loc = (random.randint(0, 49), random.randint(0, 49))
        agents[loc] = Agent(age=Age.young,
                            status=Status.healthy,
                            vaccinated=0,
                            masked=False,
                            direction=random.randint(1,8))
    
    
    # ignorant
    old = 0; young = 0
    while old < nIgnorantOld:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.old):
            v.status = Status.ignorant
            old = 1
    while young < nIgnorantYoung:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.young):
            v.status = Status.ignorant
            young = 1
    
    
    # partially-masking
    def masked():
        return random.random() < partMaskedPercent
    
    old = 0; young = 0
    while old < nPartMaskedOld:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.old):
            v.masked = masked
            old += 1
    while young < nPartMaskedYoung:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.young):
            v.masked = masked
            young += 1
            
    # fully=masking
    old = 0; young = 0
    while old < nPartMaskedOld:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.old and v.masked != masked):
            v.masked = True
            old += 1
    while young < nPartMaskedYoung:
        k, v = random.choice([(k, v) for k, v in agents.items()])
        if (v.age == Age.young and v.masked != masked):
            v.masked = True
            young += 1
    
    return agents