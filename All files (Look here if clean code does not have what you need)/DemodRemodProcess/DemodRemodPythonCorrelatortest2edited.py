# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:32:04 2023

@author: LocalAdmin
"""

import numpy as np
from scipy import stats as st
import seaborn as sns

Interpolation=100
offsetvalue=0
sns.set_theme()
result_array=np.zeros((6,100))
for i in np.arange(1.0,101.0,1):  
    for j in range(0,1):
        countvalue=int(    8400*Interpolation   )
        #RecievedDemodRemodSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\CorrelatorresultsDemodRemodOnetimeRanger', dtype=np.float32, sep='', offset=0) 
        
        #SentDemodRemodSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\SentSignalandDemodRemodSignalInterpolated', dtype=np.float32, sep='', offset=0) 
        
        #SentReceivedSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\SentSignalandRecievedSignalInterpolated', dtype=np.float32, sep='', offset=0) 
        
        #Difference= SentDemodRemodSignalCorrelation[:30]-RecievedDemodRemodSignalCorrelation[:30]
        #Delay=84000-SentReceivedSignalCorrelation            
        
        DemodRemodSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\SimulationTESTDEMODREMOD\Signal3', dtype=np.complex64, count=countvalue, sep='', offset=8*(countvalue*(int(i)-1)+offsetvalue)) 
        
        ReceivedSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\SimulationTESTDEMODREMOD\Signal2', dtype=np.complex64,count=countvalue, sep='', offset=8*(countvalue*(int(i)-1)+offsetvalue)) 
        
        SentSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\SimulationTESTDEMODREMOD\Signal1', dtype=np.complex64, count=countvalue, sep='', offset=8*(countvalue*(int(i)-1)+offsetvalue)) 
        
        #DemodRemodSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\DemodRemoddedInterpolatedSignal', dtype=np.complex64, count=countvalue, sep='', offset=0) 
        
        #ReceivedSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\ReceivedInterpolatedSignal', dtype=np.complex64,count=countvalue, sep='', offset=0) 
        
        #SentSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\SentInterpolatedSignal', dtype=np.complex64, count=countvalue, sep='', offset=0) 
        
        correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignal) * np.conj(np.fft.fft(DemodRemodSignal)))
        delay_2_3 = np.argmax(np.abs(correlation_values))
              
        correlation_values_2 = np.fft.ifft(np.fft.fft(SentSignal) * np.conj(np.fft.fft(DemodRemodSignal)))
        delay_1_3 = np.argmax(np.abs(correlation_values_2))                                                                                                                         
        
        correlation_values_3 = np.fft.ifft(np.fft.fft(ReceivedSignal) * np.conj(np.fft.fft(SentSignal)))
        #This is the real delay seen.
        delay_1_2 = np.argmax(np.abs(correlation_values_3))                                
        
        
        #DemodRemodError
        delay_error=abs(delay_2_3-delay_1_3)-delay_1_2
        result_array[0,int((i-1))]=(countvalue/(250000))
        result_array[1+j,int((i-1))]=delay_error
        result_array[2,int((i-1))]=delay_1_3
        result_array[3,int((i-1))]=delay_2_3  
        result_array[4,int((i-1))]=delay_1_2
    
 

sns.lineplot(correlation_values_3)


