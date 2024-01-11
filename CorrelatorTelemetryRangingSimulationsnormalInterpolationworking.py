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
import matplotlib.pyplot as plt
from scipy import interpolate
import time
import scipy

sample_rate=2000000
bit_rate=20000
sps=int(sample_rate/bit_rate)
#IntegrationFactor=np.array([0.1,	0.5,	1,	10,	20,	50,	100, 500, 1000])
#delay_array=[]
#for i in IntegrationFactor:
Interpolation_Factor=1
IntegrationFactor=1
#Command Signal
#vectorsize=int(62*8*1*1*sps*Interpolation_Factor*IntegrationFactor)
#Sequential Signal
vectorsize=187500
Instrument_calibration=0*Interpolation_Factor
SentSignal=np.zeros(vectorsize)
delay_array=np.zeros([510,11])
demod_error=np.zeros([510,11])
i=0
def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

pad_to_length=next_power_of_2(vectorsize)
j=1
#sentsignallocation=("C:\GNU Radio Files\GFSKTestSentSignal"+str(j-1))
##print(sentsignallocation)
#sentsignallocation=("C:\GNU Radio Files\GFSKTestSentSignal"+str(j))
##print(sentsignallocation)
for j in range(1,2):
    sentsignallocation=("D:\\GNURADIO_THESIS_MASTER\\sentsignal1Usrptestinterpolated")
    Receivedsignallocation=("D:\\GNURADIO_THESIS_MASTER\\receivedsignal1Usrptest")
    #Demodsignallocation=("C:\GNU Radio Files\GFSKTestDR"+str(j))
    k=0
    i=0
    SentSignal=np.fromfile(sentsignallocation,count=vectorsize, dtype=np.complex64, sep='', offset=i*8) 
    while(SentSignal.shape[0]>=vectorsize):
         
        SentSignal=np.fromfile(sentsignallocation,count=vectorsize, dtype=np.complex64, sep='', offset=i*8) 
        #Pad to avoid circular convolution and to improve correlation speed
       
        if SentSignal.shape[0]<vectorsize:
            continue
        ReceivedSignal=np.fromfile(Receivedsignallocation,count=vectorsize, dtype=np.complex64, sep='', offset=i*8) 
        
        
        start = time.time()
        #print("hello")
        SentSignalpadded=np.pad(SentSignal,  (0,(2*SentSignal.shape[0]-SentSignal.shape[0])) )
        ReceivedSignalpadded=np.pad(ReceivedSignal, (0,(2*ReceivedSignal.shape[0]-ReceivedSignal.shape[0])) )
        end = time.time()
        print(end - start)
        
        #Demodsignal=np.fromfile(Demodsignallocation,count=vectorsize, dtype=np.complex64, sep='', offset=i*8) 
        #Demodsignalpadded=np.pad(Demodsignal, (0,(pad_to_length-Demodsignal.shape[0])) )
        
        #SentSignal=np.pad(SentSignal, (0,(ReceivedSignal.shape[0]-SentSignal.shape[0])) )
        #DemodRemodSignal=np.fromfile('D:\GNURADIO_THESIS_MASTER\DemodRemodProcess\RecievedDemodRemodSignalSimulation',count=SentSignal.shape[0], dtype=np.complex64, sep='', offset=0)  
        #SentSignal=np.pad(SentSignal, (0,-(SentSignal.shape[0]-ReceivedSignal.shape[0])) )
        #correlation_values = np.fft.ifft(np.fft.fft(SentSignal) * np.conj(np.fft.fft(DemodRemodSignal)))
        
       # delay_est = np.argmax(np.abs(correlation_values)) 
        
        #correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignal) * np.conj(np.fft.fft(SentSignal)))
        correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignalpadded) * np.conj(np.fft.fft(SentSignalpadded)))
        
        
        correlation_values=np.abs(correlation_values)
        
        
        delay_1 = np.argmax(correlation_values[1:vectorsize])

        
        #Interpolate to find the sub sample peak
        
        x_value_interp=np.array([0,1,2,3,4])
        array_to_interp=[correlation_values[delay_1-1],correlation_values[delay_1],correlation_values[delay_1+1], correlation_values[delay_1+2], correlation_values[delay_1+3]]
        y=interpolate.interp1d(x_value_interp, array_to_interp,'quadratic')
        #print(y)
        max_x = scipy.optimize.fminbound(lambda x: -y(x), 0, 4)

        #delay with quadratic interpolation
        #delay=delay_1-1+max_x
        #delay without interpolation
        delay=delay_1
        #demod_remod_error= abs(delay-delay_1_2)
        
        #delay=abs(delay_est)-abs(delay_demod_remod)
        
        delay_error=abs(0-abs(delay))-Instrument_calibration
    
        delay_array[k,j-1]=abs(delay_error)
        
        #demod_error[k,j-1]=abs(demod_remod_error)
        
        if k==1 and j<7:
            plt.figure(1)
            plt.rcParams['interactive'] == True
            plt.title("Sub Sample Delay Estimate Via Interpolation - Thesis ")
            plt.xlabel("Samples")
            #plt.ylabel("Y Axis")
            #plt.xlim((164400,164700))
            x=np.linspace(0,4,10000000)
            '''
            if j==1:
                plt.plot(x_value_interp,array_to_interp,'o',label='Initial Samples')
                plt.plot(max_x, y(max_x),'x',label='Max Correlation')
                plt.plot(x, y(x), '-',label='Quadratic Fit')
                plt.gca().legend('Points Used for Interpolation', 'Maximum Correlation Point')
                plt.legend(loc='best')
            else:
                plt.plot(x_value_interp,array_to_interp,'o')
                plt.plot(max_x, y(max_x),'x')
                plt.plot(x, y(x), '-')'''
            plt.plot(np.abs(correlation_values), color="red")
        
        k+=1
        i+=vectorsize
        print("Correlation",k,"is over")
    print("Run",j,"is over")   