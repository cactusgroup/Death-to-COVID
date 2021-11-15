#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:43:46 2021

@author: Joshua
"""

import random

from Constants import Age, Status, Vax

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
        
        infected_counter is used to count down each day that the Agent is
        infected but not contagious
        
        low_severity_counter is used to count down each day in a low-severity
        hospital room
        
        high_severity counter is used to count down each day in a high-severity
        hospital room
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
        
        # check daily to see if the low-severity hospitalization stays, worsens, or heals
        self.low_severity_counter = 4 * 24
        
        # check daily if the high-severity hospitalization stays, improves, or kills
        self.high_severity_counter = 4 * 24

    def expose(self, otherAgent):
        """
        expose this agent to COVID-19
        mask-wearing and vaccination determine whether this agent is infected
        """
        # if I am healthy and the other Agent is ignorant or contagious
        if self.status == Status.healthy and (otherAgent.status == Status.ignorant or
                                              otherAgent.status == Status.contagious):
            chance = self.random.random() * 1000
            print('[ Initial', chance)
            
            # 81% reduction in risk of infection by getting one dose
            # 91% reduction by getting two doses
            # https://www.cdc.gov/media/releases/2021/p0607-mrna-reduce-risks.html
            if self.vaccinated == Vax.first:
                chance -= 0.81 * chance
                print('first vax', chance)
            elif self.vaccinated == Vax.second:
                chance -= 0.91 * chance
                print('second vax', chance)
            
            # 70% reduction in risk of infection by wearing a mask for health
            # care workers.
            # There is a smaller reduction for people not wearing masks all the
            # time, but let's say it is the full 70% reduction while they are 
            # wearing the mask, and none while they are not.
            # https://pubmed.ncbi.nlm.nih.gov/33347937/
            if self.masked and not callable(self.masked):
                chance -= 0.7 * chance
                print('self masked', chance)
            elif callable(self.masked):
                if self.masked():
                    chance -= 0.7 * chance
                    print('self part masked', chance)
            
            # further 70% reduction in risk of infection if the infected person
            # is also wearing a mask
            if otherAgent.masked and not callable(otherAgent.masked):
                chance -= 0.7 * chance
                print('other masked', chance)
            elif callable(otherAgent.masked):
                if otherAgent.masked():
                    chance -= 0.7 * chance
                    print('other part masked', chance)
            
            print('Final', chance, ']')
            if chance > 950:
                print('-- infected', chance)
                self.status = Status.ignorant # ignorant
    
    def update(self, sim_time):
        """
        healthy status can transition to ignorant status upon successful expose()
        
        So we start the update calls in ignorant, contagious, infected,
        low_severity, high_severity, or deceased statuses.
        
        sim_time is the current simulation time in the 15-minute time units
        """
        
        # ignorant
        if self.status == Status.ignorant:
            """
            ignorant status always transitions to contagious status
            """
            self.ignorant_counter -= 1
            if self.ignorant_counter == 0:
                self.status = Status.contagious # -> contagious
                self.ignorant_counter = 4 * 24 * 5
        # contagious
        elif self.status == Status.contagious:
            """
            contagious status transitions to infected status,
            but a contagious agent is also symptomatic and may be placed in a
            hospital, outside of this update function
            """
            self.contagious_counter -= 1
            if self.contagious_counter == 0:
                self.status = Status.infected # -> infected
                self.contagious_counter = 4 * 24 * 10
        # infected
        elif self.status == Status.infected:
            """
            infected status branches into deceased, infected, or healthy
            statuses with probabilities that change if the agent is vaccinated.
            The deceased probability also changes depending on agent age,
            becoming 100x as high for old agents.
            https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html
            An infected agent is (maybe more) symptomatic, so they may also be
            placed in a hospital, outside of this update function.
            """
            self.infected_counter -= 1
            if self.infected_counter == 0:
                chance = self.random.random() * 1000
                
                # Set probabilities
                deceasedUpper = 5 if self.age == Age.young else 500
                infectedUpper = 800
                if self.vaccinated == Vax.first:
                    deceasedUpper = 2 if self.age == Age.young else 200
                    infectedUpper = 680
                elif self.vaccinated == Vax.second:
                    deceasedUpper = 1 if self.age == Age.young else 100
                    infectedUpper = 600
                
                # Transition
                # deceased
                if chance < deceasedUpper:
                    self.status = Status.deceased
                # continue infected
                elif deceasedUpper < chance < infectedUpper:
                    pass
                # abate
                else:
                    self.status = Status.healthy
                
                self.infected_counter = 4 * 24
        # low_severity
        elif self.status == Status.low_severity:
            """
            low_severity status comes from contagious and infected statuses
            from outside of this function. The agent will usually be young.
            low_severity status branches into low_severity, high_severity, and
            healthy, based on the results of a daily check-in.
            """
            self.low_severity_counter -= 1
            if self.low_severity_counter == 0:
                chance = self.random.random() * 1000
                
                # Set probabilities
                low_severityUpper = 600 if self.age == Age.young else 300
                high_severityUpper = 800 if self.age == Age.young else 800
                if self.vaccinated == Vax.first:
                    low_severityUpper = 500 if self.age == Age.young else 400
                    high_severityUpper = 700 if self.age == Age.young else 700
                elif self.vaccinated == Vax.second:
                    low_severityUpper = 450 if self.age == Age.young else 500
                    high_severityUpper = 600 if self.age == Age.young else 750
                
                # Transition
                # continue low_severity
                if chance < low_severityUpper:
                    pass
                # high_severity
                elif low_severityUpper < chance < high_severityUpper:
                    self.status = Status.high_severity
                # healthy
                else:
                    self.status = Status.healthy
                
                self.low_severity_counter = 4 * 24
        # high_severity
        elif self.status == Status.high_severity:
            """
            high_severity status comes from contagious and infected statuses
            from outside of this function. The agent will usually be old.
            high_severity status branches into high_severity, low_severity, and
            deceased, based on the results of a daily check-in.
            """
            self.high_severity_counter -= 1
            if self.high_severity_counter == 0:
                chance = self.random.random() * 1000
                
                # Set probabilities
                high_severityUpper = 300 if self.age == Age.young else 500
                low_severityUpper = 900 if self.age == Age.young else 800
                if self.vaccinated == Vax.first:
                    high_severityUpper = 250 if self.age == Age.young else 400
                    low_severityUpper = 950 if self.age == Age.young else 850
                elif self.vaccinated == Vax.second:
                    high_severityUpper = 200 if self.age == Age.young else 450
                    low_severityUpper = 950 if self.age == Age.young else 900
                
                # Transition
                # continue high_severity
                if chance < high_severityUpper:
                    pass
                # low_severity
                elif high_severityUpper < chance < low_severityUpper:
                    self.status = Status.low_severity
                # deceased
                else:
                    self.status = Status.deceased
                
                self.high_severity_counter = 4 * 24
        # deceased
        else:
            pass