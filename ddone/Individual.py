#-*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:29:43 2019

@author: Abhilash
"""
import numpy as np
import random
import os
import Configuration as config
from Update import Update

class Individual:
    
    global_src = config.global_src
    global_dst = config.global_dst
    lake_src = config.lake_src
    lake_dst = config.lake_dst
    veg_src = config.veg_src
    veg_dst = config.veg_dst
    vic_sim = config.vic_sim
    results_dst = config.results_dst
    n_veg = config.n_veg
    n_tiles = config.n_tiles # including a lake tile
    individual = []    
    fitness = 0
    dominationRank = 0
    dominatedChromosomes = []
#    global_lines = Update.global_lines 
#    with open(global_src, 'r') as global_file: 
#        for line in global_file: 
#            global_lines.append(line)     
    
    # collect all lines from lake param file 
#    lake_lines = Update.lake_lines
#    with open(lake_src, 'r') as lake_file: 
#        for line in lake_file: 
#            lake_lines.append(line)     
    
    # collect all lines from veg param file 
#    veg_lines = Update.veg_lines 
#    with open(veg_src, 'r') as veg_file: 
#        for line in veg_file: 
#            veg_lines.append(line)     
    
    # clean previous temp results
#    os.system('rm -f {}'.format(os.path.join(global_dst, '*')))
#    os.system('rm -f {}'.format(os.path.join(lake_dst, '*')))
#    os.system('rm -f {}'.format(os.path.join(veg_dst, '*')))
#    os.system('rm -rf {}'.format(os.path.join(results_dst, '*')))
        
            
    def generate_id(self):
        return random.random()
    
    
    def get_new_frac(self):
        return np.random.uniform(low=0.1, high=0.7)
    
    
    def get_new_LAI(self):
        return np.random.uniform()*10 
    
    def normalize_fracs(self,individual): 
        start_i = 1
        end_i = len(individual)-2
        total = sum(individual[start_i:end_i+1]) 
        
        for i in range(start_i, end_i): 
            individual[i] = individual[i]/total 
        individual[end_i] = 1-sum(individual[start_i:end_i]) 
    
        return individual
    
    def create_individual(self):
        # get an id for indv 
        id = self.generate_id() 
        #data = [self.get_new_frac(), self.get_new_LAI()] 
        fracs = [np.random.uniform() for f in range(self.n_tiles)] 
        veg_lake = random.randint(1, self.n_veg) 
        individual = [str(id)] + fracs[:] + [veg_lake]
        #random.shuffle(individual[1:])
        individual = self.normalize_fracs(individual)
        update = Update()
        # update global, lake parameters
        update.update_params(individual) 
    


        return individual

    def calc_fitness (self,individual):
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
        global_param_file = os.path.join(self.global_dst, '{}.txt'.format(individual[0]))
#        os.system('cat {}'.format(global_param_file))
        os.system('{} -g {}'.format(self.vic_sim, global_param_file)) 
    #	quit()
        # evaluate 
        results_file = open(os.path.join(self.results_dst, str(individual[0]), 'fluxes_48.1875_-120.6875.txt')) 
#	quit()
        results_dic = self.results_to_dic(results_file)
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
    
    def results_to_dic(self,results_file):
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
    
    
    
    
        
