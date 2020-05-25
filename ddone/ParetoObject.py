# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:38:09 2019

@author: Abhilash
"""
from Individual import Individual
class ParetoObject:
    chromosome = Individual()
    crowdingDistance = -1
    crowdingDistanceSorted = False
    
    def __init__(self, chromosome = None, crowdingDistance = None):
        self.chromosome = chromosome
        self.crowdingDistance = crowdingDistance