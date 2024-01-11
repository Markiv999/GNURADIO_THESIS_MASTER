# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:12:36 2023

@author: LocalAdmin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:29:29 2023

@author: LocalAdmin
"""
import numpy as np
sps=208
IntegrationFactor=np.array([0.1,	0.5,	1,	10,	20,	50,	100, 500, 1000])
delay_array=[]
for i in IntegrationFactor:
    vectorsize=int(28*i*sps)
    
    SentSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\SentSignalSimulations',count=vectorsize, dtype=np.complex64, sep='', offset=0) 
    
    ReceivedSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\RecievedSignalSimulation',count=SentSignal.shape[0], dtype=np.complex64, sep='', offset=0) 
    
    DemodRemodSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\RecievedDemodRemodSignalSimulation',count=SentSignal.shape[0], dtype=np.complex64, sep='', offset=0)  
    
    correlation_values = np.fft.ifft(np.fft.fft(SentSignal) * np.conj(np.fft.fft(DemodRemodSignal)))
    
    delay_est = np.argmax(np.abs(correlation_values)) 
    
    correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignal) * np.conj(np.fft.fft(DemodRemodSignal)))
    
    delay_demod_remod = np.argmax(np.abs(correlation_values)) 
    
    delay=abs(delay_est)-abs(delay_demod_remod)
    
    delay_error=50-abs(delay)
    
    delay_array.append(delay_error)