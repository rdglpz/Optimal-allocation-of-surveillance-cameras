#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 11:48:03 2023

@author: rodrigo
"""


import os
import sys  


import numpy as np



root = os.getcwd() + "/.."
sys.path.insert(0, root)
import src.camera_allocation_functions as aptitude

import pandas as pd

import rasterio

def main():
    

    
    fp2 = '../data/processed/aguascalientes/01_densidad_delitos_sobre_calle_1998'
    crime_density = rasterio.open(fp2)

    
    fp3 = '../data/processed/aguascalientes/02_manzanas_raster_binary'
    blocks = rasterio.open(fp3)
    
    #correction
    S = blocks.read(1)
    S[S==255] = 0
    
    CD = crime_density.read(1)
    
#    W = walls.read(1)
    
    L = 50
    
    
    
    df = pd.DataFrame(data = {"visibility coefficient": [0], "area": [0],"i": [0], "j": [0]})
    
    c = 0
    
    K = aptitude.gkern(L*2 + 1, 2)
    
    for i in range(L, S.shape[0]-L):
        for j in range(L, S.shape[1]-L):
            
            si = (i, j)
            
            S_sub = np.copy(S[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])
            
            CD_sub = np.copy(CD[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])
            
            #if si is street with some crime then compute isovista:
            if S[si]==0 and CD[si]>0:
                
                isovist = aptitude.isovista(S_sub)
                
                area = np.sum(isovist)
            
                p = np.sum(CD_sub*K*isovist)
                
                #agregar a dataframe lista con y,j,p
                newData = pd.DataFrame({"visibility coefficient": [p], "area": [area], "i": [i], "j": [j]})
                
                df = pd.concat([df, newData], ignore_index=True)
                        
            c = c +1
            
            if c%100000==0:
                print(c)
                
                
    df.to_csv("../data/processed/fitness_positions.csv")
    
    

if __name__ == "__main__":
    
    main()
    