#from Individual import Individual
#
#
#
#pop = []
#for i in range(10):
#    gene = Individual()
#    gene.individual = gene.create_individual()
#    gene.fitness = gene.calc_fitness(gene.individual)
#    pop.append(gene)
#
#for chromosome in pop:
#    print(chromosome.individual)
#    print(chromosome.fitness)
#    

from Synthesis import Synthesis
from Service import Service

service = Service()
synth = Synthesis()

parent = synth.synthesize_population()
#for chromosome in population.populace:     
#	print(chromosome.individual) 
child = synth.create_child_population(parent)
print("Children")
#print(child.populace)
#for chromosome in child.populace:
#	print(chromosome.individual)
  
combinedPopulation = service.combine_population(parent, child)
paretoFront = service.fast_non_dominated_sort(combinedPopulation)
#for chromosome in combinedPopulation.populace:
#    dc = chromosome.dominatedChromosomes
#    for individual in dc:
#       print(chromosome.dominationRank)

#paretoFront = service.fast_non_dominated_sort(combinedPopulation)
#for chromosome in paretoFront.values()[0]:
#    print(chromosome.individual)

