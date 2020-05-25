# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:19:47 2019

@author: Abhilash
"""

import Configuration as config
from Individual import Individual
from ParetoObject import ParetoObject
from Population import Population
import numpy as np
import random

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
                if(competitor != chromosome):
                    if(self.dominates(chromosome, competitor)):
                        if competitor not in chromosome.dominatedChromosomes:
                            chromosome.dominatedChromosomes.append(competitor)
                    elif(self.dominates(competitor, chromosome)):
                        chromosome.dominationRank += 1
            
            if(chromosome.dominationRank == 0):
                singularFront.append(chromosome)
                
        paretoFront[1] = singularFront
        
        i = 1
        
        previousFront = paretoFront[i]
        nextFront = []
        
        while(previousFront != []):
            for chromosome in previousFront:
                for recessive in chromosome.dominatedChromosomes:
                    if(recessive.dominationRank != 0):
                        recessive.dominationRank -= 1
                    if(recessive.dominationRank == 0):
                        if(recessive not in nextFront):
                            nextFront.append(recessive)
            if(nextFront == [] and self.is_dominated_chromosomes_empty(previousFront) == False):
                minimumRank = -1
                for chromosome in previousFront:
                    while(self.recessive_rank_greater_than_zero(chromosome) == True):
                        for recessive in chromosome.dominatedChromosomes:
                            if(minimumRank == -1 or minimumRank > recessive.dominationRank):
                                minimumRank = recessive.dominationRank
                if minimumRank != -1:
                    for chromosome in previousFront:
                        while(self.recessive_rank_greater_than_zero(chromosome) == True):
                            for recessive in chromosome.dominatedChromosomes:
                                if recessive.dominationRank != 0:
                                    recessive.dominationRank -= minimumRank
                                if recessive.dominationRank == 0:
                                    if recessive not in nextFront:
                                        nextFront.append(recessive)
                                        
            if nextFront != []:
                i += 1
                paretoFront[i] = nextFront
            else:
                break
            previousFront = nextFront
            del nextFront[:]
            
        return paretoFront
                
    def dominates(self,competitor1, competitor2):
        flag = None
        for i in range(config.objectives):
            if competitor1.fitness[i] < competitor2.fitness[i]:
                flag = True
            else:
                flag = False
            
        if flag == False:
            return False
        
        for i in range(config.objectives):
            if competitor1.fitness[i] > competitor2.fitness[i]:
                flag = True
                break
            else:
                flag = False
                
        return flag
        
        
    def is_dominated_chromosomes_empty(self, front):
        flag = False
        for chromosome in front:
            if(chromosome.dominatedChromosomes != []):
                flag = True
                break
        return flag
        
    def recessive_rank_greater_than_zero(self, chromosome):
        flag = False
        if(chromosome.dominatedChromosomes == []):
            return False
        for recessive in chromosome.dominatedChromosomes:
            if(recessive.dominationRank == 0):
                flag = True
                break
        return flag
    
    def crowding_distance_assignment(self, singularFront):
        i=0
        end = len(singularFront) - 1
        maxObjectiveValue = None
        minObjectiveValue = None
        objectives = config.objectives
        singlePareto = []
        
#	print(singularFront)
        for chromosome in singularFront:
            paretoObject = ParetoObject(chromosome, 0)
#	    print(i)
            singlePareto.append(paretoObject)
            i += 1
            
        for objective in range(objectives):
            maxObjectiveValue = None
            minObjectiveValue = None
            singlePareto = self.sort(singlePareto, objective)
            
            singlePareto[0].crowdingDistance = 9999999
            singlePareto[end].crowdingDistance = 9999999
            
            for paretoObject in singlePareto:
                if maxObjectiveValue == None or maxObjectiveValue < paretoObject.chromosome.fitness[objective]:
                    maxObjectiveValue = paretoObject.chromosome.fitness[objective]
                if minObjectiveValue == None or minObjectiveValue > paretoObject.chromosome.fitness[objective]:
                    minObjectiveValue = paretoObject.chromosome.fitness[objective] 
                    
            for i in range(2, end):
                singlePareto[i].crowdingDistance = self.calc_crowding_distance(singlePareto, i, objective, maxObjectiveValue, minObjectiveValue)
                
        return singlePareto
    
            
    def sort(self, singlePareto, objective):
        paretoArray = np.asarray(singlePareto)
        
        self.randomized_quick_sort(paretoArray, 0, len(paretoArray)-1, objective)
        
        return paretoArray.tolist()
    
    def randomized_quick_sort(self, paretoArray, head, tail, objective):
        if head<tail:
            pivot = self.randomized_partition(paretoArray, head, tail, objective)
            
            self.randomized_quick_sort(paretoArray, head, pivot-1, objective)
            self.randomized_quick_sort(paretoArray, pivot+1, tail, objective)
            
    def randomized_partition(self, paretoArray, head, tail, objective):
        rand = random.randint(head, tail)
        temporary = ParetoObject()
        
        temporary = paretoArray[head]
        paretoArray[head] = paretoArray[rand]
        paretoArray[rand] = temporary
        
        return self.partition(paretoArray, head, tail, objective)
    
    def partition(self, paretoArray, head, tail, objective):
         pivot = ParetoObject()
         pivot = paretoArray[tail]
         i = head -1
         
         for j in range(head, tail):
             if paretoArray[j].chromosome.fitness[objective] <= pivot.chromosome.fitness[objective]:
                 i += 1
                 temporary = ParetoObject()
        
                 temporary = paretoArray[i]
                 paretoArray[i] = paretoArray[j]
                 paretoArray[j] = temporary
        
         temporary = ParetoObject()
        
         temporary = paretoArray[i+1]
         paretoArray[i+1] = paretoArray[tail]
         paretoArray[tail] = temporary
        
         return i+1
    
    def calc_crowding_distance(self, singlePareto, presentIndex, objective, maxObjectiveValue, minObjectiveValue):
        return singlePareto[presentIndex].crowdingDistance + ((singlePareto[presentIndex+1].chromosome.fitness[objective] - singlePareto[presentIndex-1].chromosome.fitness[objective]) / (maxObjectiveValue - minObjectiveValue))
    
    def crowd_comparison_sort(self, singleFront):
        index = -1
        sortedFront = []
        presentParetoObject = ParetoObject()
        competitor = ParetoObject()
        
        for paretoObject in singleFront:
            paretoObject.crowdingDistanceSorted = False
        
        for i in range(0, len(singleFront)):
            presentParetoObject = singleFront[i]
            if presentParetoObject.crowdingDistanceSorted == False:
                for j in range(0, len(singleFront)):
                    competitor = singleFront[j]
                    if competitor.crowdingDistanceSorted == False:
                        dominationRank = presentParetoObject.chromosome.dominationRank
                        competingDominationRank = competitor.chromosome.dominationRank
                        crowdingDistance = presentParetoObject.crowdingDistance
                        competingCrowdingDistance = competitor.crowdingDistance
                        
                        if i!=j:
                            if dominationRank > competingDominationRank or (dominationRank == competingDominationRank and crowdingDistance < competingCrowdingDistance):
                                presentParetoObject = competitor
                
                presentParetoObject.crowdingDistanceSorted = True
                index += 1
                sortedFront.append(presentParetoObject)
        return sortedFront
    
