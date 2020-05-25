# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:57:05 2019

@author: Abhilash
"""


import random
from pyeasyga import pyeasyga
import numpy as np
import os
from time import time

# setup seed data
#seed_data = [0, 1, 2, 3, 4, 5, 6, 7]
seed_data = [0.1, 0.9]
populationSize = 10 
generations = 5 
global_src = './classic/Stehekin/parameters/global_param.STEHE.txt'
global_dst = './tmp_global' 
lake_src = './classic/Stehekin/parameters/lakeparam.txt'
lake_dst = './tmp_lake' 
veg_src = './classic/Stehekin/parameters/Stehekin_vegparam.txt'
veg_dst = './tmp_veg' 
vic_sim = '/VIC/vic/drivers/classic/vic_classic.exe'
results_dst = './tmp_sim_results'
n_veg = 11
n_tiles = n_veg + 1 # including a lake tile

# collect all lines from global param file 
global_lines = [] 
with open(global_src, 'r') as global_file: 
    for line in global_file: 
        global_lines.append(line)     

# collect all lines from lake param file 
lake_lines = [] 
with open(lake_src, 'r') as lake_file: 
    for line in lake_file: 
        lake_lines.append(line)     

# collect all lines from veg param file 
veg_lines = [] 
with open(veg_src, 'r') as veg_file: 
    for line in veg_file: 
        veg_lines.append(line)     

# clean previous temp results
os.system('rm -f {}'.format(os.path.join(global_dst, '*')))
os.system('rm -f {}'.format(os.path.join(lake_dst, '*')))
os.system('rm -f {}'.format(os.path.join(veg_dst, '*')))
os.system('rm -rf {}'.format(os.path.join(results_dst, '*')))

def update_lake_params(individual): 
    id = individual[0] 

    # create its lake param file 
    indv_file = open(os.path.join(lake_dst, '{}.txt'.format(id)), 'w') 
    for line in lake_lines:
        params = line.split()
        
        if len(params) == 7:
            params[1] = str(n_tiles-1) # th tile is for lake 
        elif len(params) == 10:
            '''
            if individual[1] + 0.325892 > 1: # resize proportionally 
                params[1] = str(individual[1]/(individual[1]+0.325892)) # frac 
            else: # last veg tile takes the rest 
                params[1] = str(individual[1]) 
            '''
            params[1] = str(individual[len(individual)-2]) # frac of lake  
        line = '  '.join(params) + '\n' 
        indv_file.write(line) 


def update_veg_params(individual): 
    id = individual[0] 
    rest_params = ['0.10', '0.05', '1.00', 
            '0.45', '5.00', '0.50'] # after veg class, tile frac 

    # create its lake param file 
    indv_file = open(os.path.join(veg_dst, '{}.txt'.format(id)), 'w') 
    for line in veg_lines:
        params = line.split()
        
        if len(params) == 2:
            params[1] = str(n_tiles)
            '''
            layer_i = 1
            elif layer_i == 1 and len(params) == 8:
                params[1] = str(individual[1]) # frac 
            elif layer_i == 1 and len(params) == 12:
                params[0] = str(individual[2]) # LAI 
                layer_i += 1
            '''
            line = '  '.join(params) + '\n' 
            indv_file.write(line) 

            # write params for each tile
            for i in range(n_tiles):
                veg_class = i+1
                if veg_class > n_veg:
                    veg_class = individual[len(individual)-1]
                frac = individual[1+i]
                params = [str(veg_class), str(frac)] + rest_params 
                line = '  '.join(params) + '\n' 
                indv_file.write(line) 


def update_global_params(individual): 
    id = individual[0] 

    # create its global param file 
    indv_file = open(os.path.join(global_dst, '{}.txt'.format(id)), 'w') 

    # update refs to parameter files 
    for line in global_lines:
        # filter words of interest 
        if line.startswith('LAKES '):
            line = 'LAKES    {}\n'.format(os.path.join(lake_dst, '{}.txt'.format(id)))
        elif line.startswith('VEGPARAM '):
            line = 'VEGPARAM    {}\n'.format(os.path.join(veg_dst, '{}.txt'.format(id)))
        elif line.startswith('RESULT_DIR '):
            os.makedirs(os.path.join(results_dst, str(id)))
            line = 'RESULT_DIR    {}\n'.format(os.path.join(results_dst, str(id)))

        indv_file.write(line) 


def update_params(individual):
    # global parameter files 
    update_global_params(individual) 

    # lake parameter files 
    update_lake_params(individual) 

    # veg parameter files 
    update_veg_params(individual) 


def generate_id():
    return random.random()


def get_new_frac():
    return np.random.uniform(low=0.1, high=0.7)


def get_new_LAI():
    return np.random.uniform()*10 


def normalize_fracs(individual): 
    start_i = 1
    end_i = len(individual)-2
    total = sum(individual[start_i:end_i+1]) 
    
    for i in range(start_i, end_i): 
        individual[i] = individual[i]/total 
    individual[end_i] = 1-sum(individual[start_i:end_i]) 

    return individual


# define and set function to create a candidate solution representation
# [0] = id of individual
# [l-1] = veg type in lake 
# [1:l-2] = fractions of veg types
def create_individual():
    # get an id for indv 
    id = generate_id() 
    #data = [get_new_frac(), get_new_LAI()] 
    fracs = [np.random.uniform() for f in range(n_tiles)] 
    veg_lake = random.randint(1, n_veg) 
    individual = [str(id)] + fracs[:] + [veg_lake]
    #random.shuffle(individual[1:])
    individual = normalize_fracs(individual)

    # update global, lake parameters
    update_params(individual) 

    return individual

def calc_fitness (individual):
    '''
    collisions = 0
    for item in individual:
        item_index = individual.index(item)
        for elem in individual:
            elem_index = individual.index(elem)
            if item_index != elem_index:
                if item - (elem_index - item_index) == elem \
                    or (elem_index - item_index) + item == elem:
                    collisions += 1
    return collisions
    '''
    # run with the specific global param file 
    global_param_file = os.path.join(global_dst, '{}.txt'.format(individual[0]))
    os.system('{} -g {}'.format(vic_sim, global_param_file)) 

    # evaluate 
    results_file = open(os.path.join(results_dst, str(individual[0]), 'fluxes_48.1875_-120.6875.txt')) 
    results_dic = results_to_dic(results_file)
    surf_prec_list = results_dic['OUT_PREC'] 
    #surf_temp_list = results_dic['OUT_SURF_TEMP'] 
    #soil_temp_list = results_dic['OUT_SOIL_TEMP_0'] 
    soil_mst_list = results_dic['OUT_SOIL_MOIST_0'] 
    #runoff_list = results_dic['OUT_RUNOFF']

    #return np.mean(surf_temp_list) 
    #return np.var(surf_temp_list) 
    #return np.var(surf_prec_list) #np.power(np.power(individual[0],2) + np.power(individual[1],2) - 1, 2) 
    #return np.var(soil_temp_list) 
    #return np.mean(soil_temp_list) 
    #return np.var(runoff_list) 
    #return np.mean(surf_soil_temp_list) #np.power(np.power(individual[0],2) + np.power(individual[1],2) - 1, 2) 
    return np.var(soil_mst_list), np.var(surf_prec_list) 

def results_to_dic(results_file):
    d = dict()
    header = True
    header_list = []

    for line in results_file:
        line = line.strip()
        if '#' in line:
            continue
        elif header:
            header_list = line.split() 
            header = False
            for h in header_list:
                d[h] = list() 
            continue
        for (h,v) in zip(header_list, line.split()):
            d[h].append(float(v))
    return d


def create_population():
    populace = []
    
    for i in range(0, populationSize):
        populace.append(create_individual())
    
    return populace

def create_child_population(parent, fitness):
    populace = []
#    i=0
    while len(populace)<populationSize:
        for individual in crossover(binary_tournament_selection(parent, fitness),binary_tournament_selection(parent, fitness)):
            populace.append(mutate(individual))
#        i+=1
    return populace

        
        
        
def binary_tournament_selection(population, fitness):
    individual1 = population[random.randint(0, populationSize-1)]
    individual2 = population[random.randint(0, populationSize-1)]
    if(fitness[str(individual1[0])] > fitness[str(individual2[0])]):
        #print('true')
        #print(fitness[str(individual1[0])])
        #print(fitness[str(individual2[0])])
        return individual1
    else:
        #print('false')
        #print(fitness[str(individual2[0])])
        return individual2


    
def crossover(parent_1, parent_2):
    # crossover fractions 
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
    child_1 = normalize_fracs(child_1) 
    child_2 = normalize_fracs(child_2) 

    # update id and params 
    child_1[0] = generate_id()
    child_2[0] = generate_id()
    update_params(child_1)
    update_params(child_2)

    return child_1, child_2  

def mutate(individual):
    start_index = 1
    end_index = len(individual) - 2
    mutate_index = random.randrange(start_index, end_index)
    individual[mutate_index] = np.random.uniform()
    individual = normalize_fracs(individual) 

    # update id and params
    individual[0] = str(generate_id())
    update_params(individual)
    return individual

def combine_population(parent, child):
    populace = []
    populace = parent + child
    
    return populace

def initial_domination_rank(population):
    dominationRanks = {}
    for chromosome in population:
        dominationRanks[str(chromosome[0])]=0
    
    return dominationRanks

def fast_non_dominated_sort(population, dominationRanks, fitness):
    populace = {}
    
    singularFront = []
    previousFront = []
    nextFront = []
    paretoFront = {}
    dominatedChromosomes = {}
    
    #print(dominationRanks)
    for chromosome in population:

        
        populace[str(chromosome[0])] = 0
        dominatedChromosomes[str(chromosome[0])] = [0]
        
        for competitor in population:
            if(chromosome != competitor):
                if(dominates(chromosome, competitor, fitness)):
                    if competitor not in dominatedChromosomes[str(chromosome[0])]:
                        dominatedChromosomes[str(chromosome[0])].append(competitor)
                   
                    if 0 in dominatedChromosomes[str(chromosome[0])]:
                        dominatedChromosomes[str(chromosome[0])].remove(0)
                    
                elif(dominates(competitor, chromosome, fitness)):
                    ##print(dominationRanks)
                    ##print(population)
                    ##print(str(chromosome[0]))
                    dominationRanks[str(chromosome[0])] += 1
                    
        if (dominationRanks[str(chromosome[0])] == 0):
            singularFront.append(chromosome)
    paretoFront[1] = singularFront
    i = 1
    if i in paretoFront:
        previousFront = paretoFront[i]
    
    while (previousFront):
        #print(previousFront)
        for chromosome in previousFront:
            #print(str(chromosome[0]))
            for recessive in dominatedChromosomes[str(chromosome[0])]:
                
                if(dominationRanks[str(recessive[0])] != 0):
                    dominationRanks[str(recessive[0])] -= 1
                else:
                    
                    if recessive not in nextFront:                        
                        nextFront.append(recessive)
       
        if not nextFront and not is_dominated_chromosomes_empty(dominatedChromosomes, previousFront):
           
            minimumRank = -1
            for chromosome in previousFront:
                while(recessive_rank_greater_than_zero(dominatedChromosomes, dominationRanks, chromosome)):
                    for recessive in dominatedChromosomes[str(chromosome[0])]:
                        if(minimumRank == -1 or minimumRank > dominationRanks[str(recessive[0])]):
                            minimumRank = dominationRanks[str(recessive[0])]
            
            if(minimumRank != -1):
                
                for chromosome in previousFront:
                    while(recessive_rank_greater_than_zero(dominatedChromosomes, dominationRanks, chromosome)):
                        for recessive in dominatedChromosomes[str(chromosome[0])]:
                            if(dominationRanks[str(recessive[0])] != 0):
                                dominationRanks[str(recessive[0])] -= minimumRank
                            if(dominationRanks[str(recessive[0])] == 0):
                                if recessive not in nextFront:
                                    nextFront.append(recessive)
                
        
        if nextFront:
	    i += 1
            paretoFront[i] = nextFront
        else:
           
            break
        
        previousFront = nextFront
        
        nextFront.clear
        
          
    #print("singular")
    #print(previousFront)
    #print("return")
    #print(paretoFront)    
    ##print(dominatedChromosomes)
    return population, dominationRanks, dominatedChromosomes, paretoFront
def dominates(competitor1, competitor2, fitness):
    if(fitness[str(competitor1[0])]<fitness[str(competitor2[0])]):
        return True
    else:
        return False

def is_dominated_chromosomes_empty(dominatedChromosomes, front):
    for chromosome in front:
        if(str(chromosome[0]) in dominatedChromosomes):
            #print("true")
            return True
        
def recessive_rank_greater_than_zero(dominatedChromosomes, dominationRanks, chromosome):
    flag = True
    if(str(chromosome[0]) not in dominatedChromosomes):
        flag = False
    else:
        for recessive in dominatedChromosomes[str(chromosome[0])]:
            if(dominationRanks[str(recessive[0])] == 0):
                flag = False
    return flag

def crowding_distance_assignment(singularFront, population, fitness):
    i=0
    end = len(singularFront)-1
    
    singlePareto = {}
    paretoObject = {}
    #print(singularFront)
    for chromosome in singularFront:
        #print(chromosome)
        paretoObject[str(chromosome[0])] = 0
        singlePareto[i] = paretoObject
        i+=1
    #print(singlePareto)
    for objective in range(objectives):
        
        maxObjectiveValue = 0
        minObjectiveValue = 0
        #print("inside loop")
        #print("loop : " + str(objective))
        
        singlePareto = sort(singlePareto, objective, fitness)
        
        firstPareto = singlePareto[list(singlePareto.keys())[0]]
        firstPareto[list(firstPareto.keys())[0]] = 99999999999
        singlePareto[list(singlePareto.keys())[0]] = firstPareto
        #print(firstPareto)
        last = len(list(singlePareto.keys())) -1
        lastPareto = singlePareto[list(singlePareto.keys())[last]]
        lastPareto[list(lastPareto.keys())[0]] = 99999999999
        singlePareto[list(singlePareto.keys())[last]] = lastPareto
        #print("single")
        #print(singlePareto)
        for pareto in singlePareto:
            paretoObjective = []
            gene = []
            gene = get_chromosome(population, list(singlePareto[pareto].keys())[0])
            #for chromosome in population:
             #   if (str(chromosome[0]) == list(singlePareto[pareto].keys())[0]):
              #      gene = chromosome
            paretoObjective = fitness[str(gene[0])]
            if((maxObjectiveValue == 0) or (maxObjectiveValue < paretoObjective[objective])):
                maxObjectiveValue = paretoObjective[objective]
            if((minObjectiveValue == 0) or (minObjectiveValue > paretoObjective[objective])):
                minObjectiveValue = paretoObjective[objective]
            #print("pareto")
            #print(paretoObjective)
            #print(maxObjectiveValue)
            #print(minObjectiveValue)
            #print("hhhhhh" + str(list(singlePareto[pareto].values())[0]))
            
        for j in range(0, end):
            #print("yo hoo")
            pareto = singlePareto[list(singlePareto.keys())[j]]
            pareto[list(pareto.keys())[0]] = calculate_crowding_distance(population, singlePareto, j, objective, maxObjectiveValue, minObjectiveValue, fitness)
            singlePareto[list(singlePareto.keys())[j]] = pareto
    
    return singlePareto
            
        

def calculate_crowding_distance(population, singlePareto, presentIndex, objective, maxObjectiveValue, minObjectiveValue, fitness):
    
    previousChromosomeObjective = fitness[str(get_chromosome(population, list(singlePareto[presentIndex-1].keys())[0])[0])][objective]
    afterChromosomeObjective = fitness[str(get_chromosome(population, list(singlePareto[presentIndex+1].keys())[0])[0])][objective]
    return list(singlePareto[presentIndex].values())[0] + (previousChromosomeObjective - afterChromosomeObjective) / (maxObjectiveValue - minObjectiveValue)
            
        
def get_chromosome(population, index):
    for chromosome in population:
                if (str(chromosome[0]) == index):
                    return chromosome
        
def sort(singlePareto, objective, fitness):
    
    randomized_quick_sort(singlePareto, 0, len(singlePareto)-1, objective, fitness) 
    
    return singlePareto

def randomized_quick_sort(paretoArray, head, tail, objective, fitness):
    #print("check")
    #print(head)
    #print(tail)
    if (head <= tail):
        pivot = randomized_partition(paretoArray, head, tail, objective, fitness)
        
        randomized_quick_sort(paretoArray, head, pivot-1, objective, fitness)
        randomized_quick_sort(paretoArray, pivot+1, tail, objective, fitness)
        
def randomized_partition(paretoArray, head, tail, objective, fitness):
    rand = random.randint(head, tail)
    temporary = paretoArray[head]
    paretoArray[head] = paretoArray[rand]
    paretoArray[rand] = temporary
    
    return partition(paretoArray, head, tail, objective, fitness)

def partition(paretoArray, head, tail, objective, fitness):
    #print("part")
    pivot = paretoArray[tail]
    i = head -1
    for j in range(head, tail-1):
        paretoObjective = []
        #print("pareto")
        #print(paretoArray[j])
        paretoObjective = fitness[str(paretoArray[j][0])]
        pivotObjective = []
        pivotObjective = fitness[str(paretoArray[pivot][0])]
        if(paretoObjective[objective]<=pivotObjective[objective]):
            i+=1
            temporary = paretoArray[i]
            paretoArray[i] = paretoArray[j]
            paretoArray[j] = temporary
        
    temporary = paretoArray[i+1]
    paretoArray[i+1] = paretoArray[tail]
    paretoArray[tail] = temporary
    
    return (i+1)
        
def crowd_comparison_sort(singleFront, crowdingDistanceSorted, dominationRanks):
    index = -1
    sortedFront = {}
    presentParetoObject = {}
    competitor = {}
    
    crowdingDistanceSorted = [False]
    
    for i in range(0, len(singleFront)):
        presentParetoObject = singleFront[i]
        if(crowdingDistanceSorted[i] == False):
            for j in range(0, len(singleFront)):
                competitor = singleFront[j]
                if(crowdingDistanceSorted[j] == False):
                    dominationRank = dominationRanks[list(presentParetoObject.keys())[0]]
                    competingDominationRank = dominationRanks[list(competitor.keys())[0]]
                    crowdingDistance = list(presentParetoObject.values())[0]
                    competingCrowdingDistance = list(competitor.values())[0]
                    
                    if(i!=j):
                        if((dominationRank > competingDominationRank) or ((dominationRank == competingDominationRank) and crowdingDistance < competingCrowdingDistance)):
                            presentParetoObject = competitor
                    
            crowdingDistanceSorted[i] = True
            index+=1
            sortedFront[index] = presentParetoObject
    return sortedFront

start_time = time()                       
parent = []
parent = create_population()
child = []
##print(random.randint(0, populationSize-1))
#print("parent")
#print(parent)
fitness = {}
for chromosome in parent:
    fitness[str(chromosome[0])] = calc_fitness(chromosome)
child = create_child_population(parent, fitness)

for i in range(2, generations+1):
    
    combinedPopulation = []
    combinedPopulation = combine_population(parent, child)
    ##print(parent)
    ##print(child)
    ##print(combinedPopulation)
    #initial_domination_rank(combinedPopulation)
    fitness.clear()
    for chromosome in combinedPopulation:
        fitness[str(chromosome[0])] = calc_fitness(chromosome)
    dominationRanks = {}
    dominationRanks = initial_domination_rank(combinedPopulation)
    #print(dominationRanks)
    dominatedChromosomes = {}
    combinedPopulation, dominationRanks, dominatedChromosomes, rankedFronts = fast_non_dominated_sort(combinedPopulation, dominationRanks, fitness)  
    #print(rankedFronts)
    #print("kkk")
    
    nextChildPopulation = []
    childPopulace = []
    
    
    for j in range(1, len(rankedFronts) + 1):
        singularFront = rankedFronts[j]
        usableSpace = populationSize - len(childPopulace)
        
        if (singularFront and usableSpace > 0):
            #print("in here")
            if(usableSpace >= len(singularFront)):
                #print("more inner")
                for chromosome in singularFront:
                    childPopulace.append(chromosome)
            else:
                #print("i'm in here")
                singlePareto = {}
                singlePareto = crowding_distance_assignment(singularFront, combinedPopulation, fitness)
                crowdingDistanceSorted = []
                latestFront = {}
                latestFront = crowd_comparison_sort(singlePareto, crowdingDistanceSorted, dominationRanks)
                
                for k in range(0, usableSpace):
                    childPopulace.append(latestFront[k])
        else:
            break
        
    nextChildPopulation = childPopulace
        
    print("Parent")
    print(parent)
    print("childpopulace")
    print(childPopulace)
    print("Children")
    print(child)
    if (i < generations):
        parent = child
        #print(len(childPopulace))
        child = create_child_population(childPopulace, fitness)
#
end_time = time()
m = (end_time - start_time) // 60
s = (end_time - start_time) % 60
print('took {} minutes {} seconds'.format(m, s))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ALL DONE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 











