# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:19:47 2019

@author: Abhilash
"""

import Configuration as config
from Individual import Individual
from ParetoObject import ParetoObject
from Population import Population

class Service:
    
    def combine_population(self, parent, child):
        combinedPopulation = Population()
        combinedPopulace = []
        for chromosome in parent.populace:
            combinedPopulace.append(chromosome)
        for chromosome in child.populace:
            combinedPopulace.append(chromosome)
        
        combinedPopulation.populace = combinedPopulace
        return combinedPopulation
    
    def fast_non_dominated_sort(self,population):
        paretoFront = {}
        singularFront = []
        populace = population.populace
        
        for chromosome in populace:
            chromosome.dominationRank = 0
            chromosome.dominatedChromosomes = []
            
            for competitor in populace:
                if(chromosome != competitor):
                    if(self.dominates(chromosome, competitor)):
                        if competitor not in chromosome.dominatedChromosomes:
                            chromosome.dominatedChromosomes.append(competitor)
                    elif(self.dominates(competitor, chromosome)):
                        chromosome.dominationRank += 1
            
            if(chromosome.dominationRank == 0):
                singularFront.append(chromosome)
                
        paretoFront[1] = singularFront
    
        return paretoFront
                
    def dominates(self,competitor1, competitor2):
        flag = False
        for i in range(config.objectives):
            if(competitor1.fitness[i] < competitor2.fitness[i]):
                flag = False
            elif competitor1.fitness[i] > competitor2.fitness[i]:
                flag = True
                break
            
        return flag
        
        
        