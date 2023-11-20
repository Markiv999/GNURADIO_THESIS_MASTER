# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:34:46 2023

@author: LocalAdmin
"""
import numpy as np
from scipy import stats as st
#Set initial Parameters, these values are used to ensure that only neccessary samples are correlated. Incorrect entry
#will degrade performance.
vectorsize=187500
sample_rate=2000000
starttime=9#secs

#noofarraysdelayed=starttime*sample_rate/vectorsize

Maxdelayallowed=750

#DerivedValuesPlusConstants
initial_offset=starttime*sample_rate
Allcorrelationvalues=np.zeros(1)
actualdelaycount=np.zeros(1)
counter_s=0
counter_f=0
overall_counter=0
flag=0
average=0
sum=0
baselinereset=0
previousdelay=0
#Choose Sent and Received Signal Files
sentvalues=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\Sequential Ranging Signal\\FinalSignal4', dtype=np.complex64, count=187500, sep='', offset=0)   
received=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\RangingSignals\\75KLengthSignal\\Switchtest32', dtype=np.complex64)

while flag==0:
    #receivedvalues=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\RangingSignals\\75KLengthSignal\\Switchtest10MHZ', dtype=np.complex64, count=187500, sep='', offset=2*187500*(overall_counter))
    #sentvalues=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\Sequential Ranging Signal\\FinalSignal4', dtype=np.complex64, count=187500, sep='', offset=0)   
    receivedvalues=received[initial_offset+overall_counter*187500:initial_offset+(overall_counter+1)*187500]
    
    
    
    
    overall_counter+=1
    if receivedvalues.shape[0]!=187500:
        flag=1
        continue
    
    #Correlate Arrrays to Obtain Delay
    correlation_values = np.fft.ifft(np.fft.fft(receivedvalues) * np.conj(np.fft.fft(sentvalues)))
    sample_delay_count = np.argmax(np.abs(correlation_values))
    delay = vectorsize - sample_delay_count
    #delay_in_micro_seconds = 10 ** 6 * delay / self.sample_rate
    Allcorrelationvalues=np.append(Allcorrelationvalues,delay)
    #Allows for baseline to change in case incorrect baseline was captured
    if delay==previousdelay:
        baselinereset+=1
        if baselinereset==10:
            baseline=delay
            baselinereset=0
    else:
        baselinereset=0
    
    if counter_s<=10:
        baseline=delay
    
    if abs(delay-baseline)>Maxdelayallowed:
        counter_f+=1
        
    else:        
        sum+=delay
        counter_s+=1
        average+=sum/counter_s
        if abs(delay-baseline)>5:
            actualdelaycount=np.append(actualdelaycount, abs(delay-baseline))
    previousdelay=delay
#Remove the artificial zero that was present initially
actualdelaycount=actualdelaycount[1:]
#Calculate Min and Max delay
maxdelay=np.max(actualdelaycount)
mindelay=np.min(actualdelaycount)

#find unique values in array along with their counts
MostRepeatingDelay=st.mode(actualdelaycount,keepdims=True)

MostRepeatingDelayCount=MostRepeatingDelay[1]
MostRepeatingDelay=MostRepeatingDelay[0]