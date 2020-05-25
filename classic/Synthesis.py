# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:50:15 2019

@author: Abhilash
"""

import random
from Population import Population
import Configuration as config
from Individual import Individual
import numpy as np

class Synthesis:
    
    def synthesize_population(self):
        population = Population()
        populace = []
        
        for i in range(0, config.populationSize):
            gene = Individual()
            gene.individual = gene.create_individual()
            gene.fitness = gene.calc_fitness(gene.individual)
            populace.append(gene)
        
        population.populace = populace
        return population
    
    def create_child_population(self, parent):
        child = Population()
        populace = []
        
        while (len(populace) < config.populationSize):
            for individual in self.crossover(self.binary_tournament_selection(parent),self.binary_tournament_selection(parent)):
                populace.append(self.mutate(individual))
                
        child.populace = populace
        
        return child

    def crossover(self,individual1, individual2):
        # crossover fractions
        parent_1 = individual1.individual
        parent_2 = individual2.individual
        chromosome = Individual()
        start_index = 1
        end_index = len(parent_1)-2
        crossover_index = random.randrange(start_index, end_index+1)
        child_1a = parent_1[crossover_index:]
        child_1b = parent_2[:crossover_index] 
        child_1 = child_1b + child_1a
    
        child_2a = parent_2[crossover_index:]
        child_2b = parent_1[:crossover_index] 
        child_2 = child_2b + child_2a
    
        # crossover lake's veg type
        if np.random.uniform() > 0.5: 
            tmp = child_1[len(child_1)-1]
            child_1[len(child_1)-1] = child_2[len(child_2)-1]
            child_2[len(child_2)-1] = tmp 
    
        # normalize fractions 
        child_1 = chromosome.normalize_fracs(child_1) 
        child_2 = chromosome.normalize_fracs(child_2) 
    
        # update id and params 
        child_1[0] = chromosome.generate_id()
        child_2[0] = chromosome.generate_id()
        chromosome.update_params(child_1)
        chromosome.update_params(child_2)
        child1 = Individual()
        child2 = Individual()
        
        child1.individual = child_1
        child2.individual = child_2
        
        child1.fitness = chromosome.calc_fitness(child_1)
        child2.fitness = chromosome.calc_fitness(child_2)
        return child1, child2  
    
    def mutate(self,child_1):
        chromosome = Individual()
        individual = child_1.individual
        start_index = 1
        end_index = len(individual) - 2
        mutate_index = random.randrange(start_index, end_index)
        individual[mutate_index] = np.random.uniform()
        individual = chromosome.normalize_fracs(individual) 
    
        # update id and params
        individual[0] = str(chromosome.generate_id())
        chromosome.update_params(individual)
        child = Individual()
        child.individual = individual
        child.fitness = chromosome.calc_fitness(individual)
        return child
    
    def binary_tournament_selection(self, population):
        individual1 = population.populace[random.randint(0, config.populationSize-1)]
        individual2 = population.populace[random.randint(0, config.populationSize-1)]
        if(individual1.fitness > individual2.fitness):
            #print('true')
            #print(fitness[str(individual1[0])])
            #print(fitness[str(individual2[0])])
            return individual1
        else:
            #print('false')
            #print(fitness[str(individual2[0])])
            return individual2