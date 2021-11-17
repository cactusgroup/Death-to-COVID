# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:12:29 2021

@author: Joshua Chu
"""
class Sim1:
    # masking - incremental
    full_masking_rate = [.2, .2, .42]
    part_masking_rate = [.2]
    part_masking_percent = 0.8
    # vaccination - incremental
    vaccinated_1stdose_old = [.0, .0, .229, .008, -.169]
    vaccinated_fully_old = [.0, .0, .213, .219, .358]
    vaccinated_1stdose_young = [.0, .0, .1477, .0164, -.1321]
    vaccinated_fully_young = [.0, .0, .0, .1729, .4537]

    # hospitalized
    hospitalized_old = [19.15, 2.7, 2.77, 79.5, 18.0, 1.0]
    hospitalized_young = [3.9, 0.8, 1.1, 11.6, 5.8, 1.0]
    # deceased
    deceased_old = [331.88, 6.497, 6.65, 96.428, 29.25, 3.217]
    deceased_young = [8.760, 0.245, 0.15, 1.327, 0.97, 0.23]
    
    # number of agents
    nOld = 229
    nYoung = 471
    
    quarantine_count = 0.5*(nOld + nYoung)
    
class Sim2:
    # masking - incremental
    full_masking_rate = [1.0, .0, .0]
    part_masking_rate = [.0]
    part_masking_percent = 0.8
    # vaccination - incremental
    vaccinated_1stdose_old = [.0, .0, .229, .008, -.169]
    vaccinated_fully_old = [.0, .0, .213, .219, .358]
    vaccinated_1stdose_young = [.0, .0, .1477, .0164, -.1321]
    vaccinated_fully_young = [.0, .0, .0, .1729, .4537]

    # hospitalized
    hospitalized_old = [19.15, 2.7, 2.77, 79.5, 18.0, 1.0]
    hospitalized_young = [3.9, 0.8, 1.1, 11.6, 5.8, 1.0]
    # deceased
    deceased_old = [331.88, 6.497, 6.65, 96.428, 29.25, 3.217]
    deceased_young = [8.760, 0.245, 0.15, 1.327, 0.97, 0.23]
    
    # number of agents
    nOld = 229
    nYoung = 471
    
    quarantine_count = 0.5*(nOld + nYoung)

class Florida:
    # masking - incremental
    full_masking_rate = [.0, .1, .18]
    part_masking_rate = [.3]
    part_masking_percent = 0.6
    # vaccination - incremental
    vaccinated_1stdose_old = [.0, .0, .260, -.038, -.108]
    vaccinated_fully_old = [.0, .0, .313, .228, .244]
    vaccinated_1stdose_young = [.0, .0, .1616, -.029, -.049]
    vaccinated_fully_young = [.0, .0, .0, .1062, .3851]
    
    # hospitalized
    hospitalized_old = [.0, 2.21, 2.42, 8.52, 3.63, 1.978]
    hospitalized_young = [.0, .576, .71, 2.02, 1.568, 1.07]
    # deceased
    deceased_old = [17.989, 68.237, 19.517, 69.85, 19.978, 24.69]
    deceased_young = [.548, 2.08, .48, 1.416, .986, 2.13]
    
    # number of agents
    nOld = 281
    nYoung = 481
    
    quarantine_count = 0.3*(nOld + nYoung)

class NewYork:
    # masking - incremental
    full_masking_rate = [.8, .0, .0]
    part_masking_rate = [.2]
    part_masking_percent = 0.8
    # vaccination incremental
    vaccinated_1stdose_old = [.0, .0, .229, .008, -.169]
    vaccinated_fully_old = [.0, .0, .213, .219, .358]
    vaccinated_1stdose_young = [.0, .0, .1477, .0164, -.1321]
    vaccinated_fully_young = [.0, .0, .0, .1729, .4537]

    # hospitalized
    hospitalized_old = [19.15, 2.7, 2.77, 79.5, 18.0, 1.0]
    hospitalized_young = [3.9, 0.8, 1.1, 11.6, 5.8, 1.0]
    # deceased
    deceased_old = [331.88, 6.497, 6.65, 96.428, 29.25, 3.217]
    deceased_young = [8.760, 0.245, 0.15, 1.327, 0.97, 0.23]
    
    # number of agents
    nOld = 229
    nYoung = 471
    
    quarantine_count = 0.6*(nOld + nYoung)
    