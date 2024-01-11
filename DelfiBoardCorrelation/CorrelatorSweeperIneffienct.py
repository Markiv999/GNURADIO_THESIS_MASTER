# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:29:29 2023

@author: LocalAdmin
"""
import numpy as np

ReceivedSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationwithDelfiBoard\ReceivedSignals', dtype=np.complex64, sep='', offset=0) 

SentSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\CorrelationwithDelfiBoard\SentSignals', dtype=np.complex64, sep='', offset=0) 
maxvalue=0
sizeofsignal=SentSignal.shape[0]
for  in range(ReceivedSignal.shape[0]-sizeofsignal):
    TempSignal=ReceivedSignal[i:i+sizeofsignal]
    correlation_values = np.fft.ifft(np.fft.fft(TempSignal) * np.conj(np.fft.fft(SentSignal)))
    temp=np.max(np.abs(correlation_values)) 
    if temp>maxvalue:
        maxvalue=temp 
        delay = np.argmax(np.abs(correlation_values))+i