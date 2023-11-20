# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:32:04 2023

@author: LocalAdmin
"""

import numpy as np
from scipy import stats as st
import seaborn as sns

Interpolation=1
offsetvalue=int(32)
sns.set_theme()
result_array=np.zeros((6,100))
for i in np.arange(1.0,30.0,1):    
    for j in range(0,1):
        countvalue=int(    8400*i*Interpolation   )
        #RecievedDemodRemodSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\CorrelatorresultsDemodRemodOnetimeRanger', dtype=np.float32, sep='', offset=0) 
        
        #SentDemodRemodSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\SentSignalandDemodRemodSignalInterpolated', dtype=np.float32, sep='', offset=0) 
        
        #SentReceivedSignalCorrelation=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationValues\SentSignalandRecievedSignalInterpolated', dtype=np.float32, sep='', offset=0) 
        
        #Difference= SentDemodRemodSignalCorrelation[:30]-RecievedDemodRemodSignalCorrelation[:30]
        #Delay=84000-SentReceivedSignalCorrelation            
        
        DemodRemodSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\DemodRemoddedInterpolatedSignal', dtype=np.complex64, count=countvalue, sep='', offset=offsetvalue) 
        
        ReceivedSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\ReceivedInterpolatedSignal', dtype=np.complex64,count=countvalue, sep='', offset=offsetvalue) 
        
        SentSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\SentInterpolatedSignal', dtype=np.complex64, count=countvalue, sep='', offset=offsetvalue) 
        
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
        result_array[0,int(2*(i-1))]=(countvalue/(250000))
        result_array[1+j,int(2*(i-1))]=delay_error
        result_array[2,int(2*(i-1))]=delay_1_3
        result_array[3,int(2*(i-1))]=delay_2_3  
        result_array[4,int(2*(i-1))]=delay_1_2
        
sns.relplot(
    data=result_array, kind="line", 
    facet_kws=dict(sharex=False),
)   


