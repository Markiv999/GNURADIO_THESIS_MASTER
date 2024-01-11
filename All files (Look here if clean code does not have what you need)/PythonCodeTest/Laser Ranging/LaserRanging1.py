# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:48:32 2023

@author: vikra
"""
from scipy import constants
import numpy as np
import pandas as pd


df = pd.read_csv(r'C:\Temporary\Newfile10.csv')
#print(df)
#print(df.loc[0])

Array=df.to_numpy()

Transmitted_Signal=np.zeros(Array.shape[0])
Recieved_Signal=np.zeros(Array.shape[0])
Transmitted_Signal=Array[1:,1]
Recieved_Signal=Array[1:,2]

correlation_values = np.fft.ifft(np.fft.fft(Transmitted_Signal) * np.conj(np.fft.fft(Recieved_Signal)))
sample_delay_count = np.argmax(np.abs(correlation_values))
delay = sample_delay_count*20
Range=delay * constants.c * 10**(-9)
print(Range )            

        
            
           
