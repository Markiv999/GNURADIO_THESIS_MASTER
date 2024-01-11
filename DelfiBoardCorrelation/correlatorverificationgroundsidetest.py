# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 10:39:17 2023

@author: LocalAdmin
"""

import numpy as np
import matplotlib.pyplot as plt
def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x -1).bit_length()

sample_rate=2000000
bit_rate=20000
interpolation=1
sps=int(sample_rate/bit_rate)
vectorsize=64*sps*8*interpolation
i=0
SentSignal=np.zeros(vectorsize)
k=0
delay_array=np.zeros([101,1])
while(SentSignal.shape[0]>=vectorsize):
    ReceivedSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\receivedsignal1Usrptest',count=vectorsize ,dtype=np.complex64, sep='', offset=i*8) 
    
    SentSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\sentsignal1Usrptest',count=vectorsize, dtype=np.complex64, sep='', offset=i*8) 
    
    ReceivedSignalpadded=np.pad(ReceivedSignal, (0,(2*(ReceivedSignal.shape[0])-ReceivedSignal.shape[0])) )
    SentSignalpadded=np.pad(SentSignal, (0,(2*(SentSignal.shape[0])-SentSignal.shape[0])) )
    
    
    correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignalpadded) * np.conj(np.fft.fft(SentSignalpadded)))
    delay= np.argmax(np.abs(correlation_values)) 
    delay_array[k]=delay
    k+=1
    i+=vectorsize
    print("Correlation",k,"is over delay:",delay)
    if k==1000:
        plt.figure(5)
        plt.rcParams['interactive'] == True
        plt.title("Line Graph")
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        #plt.xlim((164400,164700))
        plt.plot(np.abs(correlation_values), color="red")