# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:47:01 2019

@author: Abhilash
"""

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

generations = 5
populationSize = 10
objectives = 2