# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:17:45 2019

@author: Abhilash
"""
import Configuration as config
import os

class Update:
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
            
    def update_lake_params(self,individual): 
        id = individual[0] 
    
        # create its lake param file 
        indv_file = open(os.path.join(self.lake_dst, '{}.txt'.format(id)), 'w') 
        for line in self.lake_lines:
            params = line.split()
            
            if len(params) == 7:
                params[1] = str(0) # th tile is for lake 
#            elif len(params) == 10:
                '''
                if individual[1] + 0.325892 > 1: # resize proportionally 
                    params[1] = str(individual[1]/(individual[1]+0.325892)) # frac 
                else: # last veg tile takes the rest 
                    params[1] = str(individual[1]) 
                '''
#                params[1] = str(individual[len(individual)-2]) # frac of lake  
            line = '  '.join(params) + '\n' 
            indv_file.write(line) 


    def update_veg_params(self,individual): 
#        id = individual[0] 
#        rest_params = ['0.10', '0.05', '1.00', 
#                '0.45', '5.00', '0.50'] # after veg class, tile frac 
#    
#        # create its lake param file 
#        indv_file = open(os.path.join(self.veg_dst, '{}.txt'.format(id)), 'w') 
#        for line in self.veg_lines:
#            params = line.split()
#            
#            if len(params) == 2:
#                params[1] = str(self.n_tiles)
#                layer_i = 1
#            elif layer_i == 1 and len(params) == 8:
#                params[1] = str(individual[1]) # frac 
#            elif layer_i == 1 and len(params) == 12:
#                params[0] = str(individual[2]) # LAI 
#                layer_i += 1    
#            line = '  '.join(params) + '\n' 
#            indv_file.write(line) 
#    
#                # write params for each tile
#            for i in range(self.n_tiles):
#                veg_class = i+1
#                if veg_class > self.n_veg:
#                    veg_class = individual[len(individual)-1]
#                frac = individual[1+i]
#                params = [str(veg_class), str(frac)] + rest_params 
#                line = '  '.join(params) + '\n' 
#                indv_file.write(line) 
        id = individual[0] 
    #    rest_params = ['0.10', '0.05', '1.00', 
    #            '0.45', '5.00', '0.50'] # after veg class, tile frac 
    
        # create its lake param file 
        indv_file = open(os.path.join(self.veg_dst, '{}.txt'.format(id)), 'w') 
        for line in self.veg_lines:
            #print(line)
            params = line.split()
            #print("params")
            #print(params)
            if len(params) == 2:
                params[1] = str(self.n_tiles)
                '''
                
                '''
#                line = '  '.join(params) + '\n' 
#                indv_file.write(line) 
            
                    
                # write params for each tile
#            else:
                
#                for i in range(self.n_tiles):
#             veg_class = i+1
#             if veg_class > self.n_veg:
#                   veg_class = individual[len(individual)-1]
#                frac = individual[1+i]
                   
#                    if len(params) == 8:
#                        params += [str(veg_class), str(frac)] # frac 
                    
            line = '  '.join(params) + '\n' 
                    
                    
                    
            indv_file.write(line) 
        
        
    def update_global_params(self,individual): 
        id = individual[0] 
    
        # create its global param file 
        indv_file = open(os.path.join(self.global_dst, '{}.txt'.format(id)), 'w') 
    
        # update refs to parameter files 
        for line in self.global_lines:
            # filter words of interest 
            if line.startswith('LAKES '):
                line = 'LAKES    {}\n'.format(os.path.join(self.lake_dst, '{}.txt'.format(id)))
            elif line.startswith('VEGPARAM '):
                line = 'VEGPARAM    {}\n'.format(os.path.join(self.veg_dst, '{}.txt'.format(id)))
            elif line.startswith('RESULT_DIR '):
                os.makedirs(os.path.join(self.results_dst, str(id)))
                line = 'RESULT_DIR    {}\n'.format(os.path.join(self.results_dst, str(id)))
    
            indv_file.write(line) 
            
    def update_params(self,individual):
        # global parameter files 
        self.update_global_params(individual) 
    
        # lake parameter files 
        self.update_lake_params(individual) 
    
        # veg parameter files 
        self.update_veg_params(individual) 
        
 