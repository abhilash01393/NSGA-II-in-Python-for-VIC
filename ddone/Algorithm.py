##from Individual import Individual
##
##
##
##pop = []
##for i in range(10):
##    gene = Individual()
##    gene.individual = gene.create_individual()
##    gene.fitness = gene.calc_fitness(gene.individual)
##    pop.append(gene)
##
##for chromosome in pop:
##    print(chromosome.individual)
##    print(chromosome.fitness)
##    
#
#
##for chromosome in population.populace:     
##	print(chromosome.individual) 
#
##print(child.populace)
##for chromosome in child.populace:
##	print(chromosome.individual)
#  
#
##for chromosome in combinedPopulation.populace:
##    dc = chromosome.dominatedChromosomes
##    for individual in dc:
##       print(chromosome.dominationRank)
#
##paretoFront = service.fast_non_dominated_sort(combinedPopulation)
##for chromosome in paretoFront.values()[0]:
##    print(chromosome.individual)
#
#from Synthesis import Synthesis
#from Service import Service
#
#service = Service()
#synth = Synthesis()
#
#parent = synth.synthesize_population()
#child = synth.create_child_population(parent)
#print("Children")
#combinedPopulation = service.combine_population(parent, child)
#paretoFront = service.fast_non_dominated_sort(combinedPopulation)


from Service import Service
from Synthesis import Synthesis
import Configuration as config
from Population import Population
from time import time
import os


global_src = config.global_src
global_dst = config.global_dst
lake_src = config.lake_src
lake_dst = config.lake_dst
veg_src = config.veg_src
veg_dst = config.veg_dst
vic_sim = config.vic_sim
results_dst = config.results_dst

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
start_time = time()      
service = Service()
synthesis = Synthesis()

parent = synthesis.synthesize_population()
child = synthesis.create_child_population(parent)

for i in range(2, config.generations+1):
    rankedFronts = service.fast_non_dominated_sort(service.combine_population(parent, child))
    nextChildPopulation = Population()
    childPopulace = []
    
    for j in range(1, len(rankedFronts)+1):
        singularFront = []
        singularFront = rankedFronts[j]
        
        usableSpace = config.populationSize - len(childPopulace)
        
        if singularFront != [] and usableSpace > 0:
            if usableSpace >= len(singularFront):
                for chromosome in singularFront:
                    childPopulace.append(chromosome)
            else:
                latestFront = []
                latestFront = service.crowd_comparison_sort(service.crowding_distance_assignment(singularFront))
                
                for k in range(0,usableSpace):
                    childPopulace.append(latestFront[k].chromosome)
        else:
            break
    nextChildPopulation.populace = childPopulace
    
    if i<config.generations:
        parent = child
        child = synthesis.create_child_population(nextChildPopulation)
    else:
	for chromosome in child.populace:
		print(chromosome.individual[0])

end_time = time()
m = (end_time - start_time) // 60
s = (end_time - start_time) % 60
print('took {} minutes {} seconds'.format(m, s))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ALL DONE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 



        
