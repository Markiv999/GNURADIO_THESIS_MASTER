# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:29:29 2023

@author: LocalAdmin
"""
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x -1).bit_length()

#def main():
print("Correlator was Called")
#regenerate header and demodsignals at correct sample rate and sps before correlation
##All params to change when changing any parameter
bitrate=4800
sample_rate=250000
sps=int(sample_rate/bitrate)
#have 1 trial run, set this to the double the delay, 212027(2MHZ, 2400bps), 26635(250Khz,2400bps), 108624(1MHz,2400bps), 26635 for (250Khz,4800bps), 
#20000 for (250Khz,9600bps), 55000(1Mhz, 19200bps), 40000(1MHz, 76800bps), if not given or wrong set very high run once and configure based on first logical measurement. 
# with differential encoding 10000 for (250Khz,4800bps), 35000 fro 1200bps 250KHz, 3500 for 19200bps 250KHz  , 7000 for 500KHz, 38400bps
#trialrundelay=6000
max_delay_allowed=30000
min_delay=1000
#Currently, set by trial, 0.000003(2MHZ, 2400bps), 0.0015(250Khz,2400bps), 0.1(250KHz,9600bps)
#1(250KHz, 19200bps), 0.015(1Mhz, 19200bps) , 1.0(500KHz, 38400bps), 1.0(1MHz, 76800bps), 0.00020(250KHz, 1200bps)
#with differential encoding 0.0015 for 250Khz, 4800bps,  0.0015 for 250Khz, 2400bps , 0.00015 for 250KHz, 1200bps, 1 for 250KHz 19200 bps., 1 for 500KHz and 38400bps(sample rate doubles the sample amp but bit rate halves it so cancels out also oversampling seems to be needed for delfi to quickly receive the packet , )
cut_off_limit_correlation=0.0040
#important to ensure that two peaks dont compete with each other. Check the distance between peaks and select accordingly. (when hitting a single peak twice, it reflects as wrong readings in the middle of the delay values array, typically negative values)
#Also a slice length needs to be bigger than a single peak.
slice_length=30000  
#Peak breaker should be bigger than size of a peak, exists to avoid double and wrong inputs from a peak
delaypeakbreaker=20000

plt.close('all')
#DemodRemodSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DemodRemodSignals', dtype=np.complex64, sep='', offset=0) 

ReceivedSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\ReceivedSignals3', dtype=np.complex64, sep='', offset=0) 

SentSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\SentSignals5', dtype=np.complex64, sep='', offset=0) 

DemodSignalSent=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\Demodsignalsent', dtype=np.float32, sep='', offset=0) 

DemodSignalReceived=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DemodsignalReceived', dtype=np.float32, sep='', offset=0) 

HeaderSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DelfiPQHeader', dtype=np.float32, sep='', offset=0) 


"""
#DemodSignal= SentSignal
skip=int(300*sps*8)
hold=int(24*sps*8)
print(SentSignal.shape)
SentSignal=SentSignal[skip:skip+hold]
SentSignal=np.pad(SentSignal,(0,ReceivedSignal.shape[0]-SentSignal.shape[0]))

correlation_values = np.fft.ifft(np.fft.fft(ReceivedSignal) * np.conj(np.fft.fft(SentSignal)))

delay= np.argmax(np.abs(correlation_values)) 

#np.roll(SentSignal,delay)
#correlation_values_2 = np.fft.ifft(np.fft.fft(DemodRemodSignal) * np.conj(np.fft.fft(ReceivedSignal)))

#delay_2_3 = np.argmax(np.abs(correlation_values))



SentSignal2=np.roll(SentSignal,delay)
t = np.arange(0, SentSignal.shape[0], 1)
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, SentSignal2, t, ReceivedSignal)
axs[0].set_xlim(0,  SentSignal.shape[0])
axs[0].set_xlabel('Sample delay')
axs[0].set_ylabel('Sent Signal and Received Signal')
axs[0].grid(True)

cxy, f = axs[1].cohere(SentSignal2, ReceivedSignal, 256, 1. / 1)
axs[1].set_ylabel('Coherence')

fig.tight_layout()
plt.show()

plt.plot(SentSignal,ReceivedSignal,color="blue")
plt.show()
#delay=delay_1_2=delay_1_3-delay_2_3 



#Correlating Demodded Signal
print(DemodSignalSent.shape)
print(DemodSignalReceived.shape)

#Select only header and data from the demodulated signal
#skip=20*sps*8
#hold=24*sps*8
print(DemodSignalSent.shape)
DemodSignalSent=DemodSignalSent[skip:skip+hold]
#Pad for length of received signal and correlate
DemodSignalSent=np.pad(DemodSignalSent,(0,DemodSignalReceived.shape[0]-DemodSignalSent.shape[0]))
correlation_values_2 = np.fft.ifft(np.fft.fft(DemodSignalReceived) * np.conj(np.fft.fft(DemodSignalSent)))
delay_demod=delay= np.argmax(np.abs(correlation_values_2)) 

if correlation_values_2[delay_demod].real<0:
    DemodSignalReceived=-1*DemodSignalReceived


#Roll Sent Signal to length of delay and plto
DemodSignalSent2=np.roll(DemodSignalSent,delay_demod)
t = np.arange(0, DemodSignalSent.shape[0], 1)
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, DemodSignalSent2, t, DemodSignalReceived)
axs[0].set_xlim(0, DemodSignalSent.shape[0])
axs[0].set_xlabel('Sample delay')
axs[0].set_ylabel('Sent Signal and Received Signal Demodded')
axs[0].grid(True)
#Plot correaltion peaks between the two signals
cxy, f = axs[1].cohere(DemodSignalSent, DemodSignalReceived, 256, 1. / 1)
axs[1].set_ylabel('Coherence')

fig.tight_layout()
plt.show()

plt.plot(DemodSignalSent2,DemodSignalReceived,color="blue")
plt.show()

#Plot a more readable correlation plot
plt.figure(3)
plt.rcParams['interactive'] == True
plt.title("Line Graph")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
#plt.xlim((164400,164700))
plt.plot(np.abs(correlation_values_2), color="red")

plt.figure(4)
plt.rcParams['interactive'] == True
plt.title("Line Graph")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
#plt.xlim((164400,164700))
plt.plot(np.abs(HeaderSignal), color="red")
"""
#CorrelateHeaderSequence
# HeaderSignaltemp=HeaderSignal
# DemodSignalReceived=DemodSignalReceived[1:1000000]
HeaderSignal=np.pad(HeaderSignal,(0,DemodSignalReceived.shape[0]-HeaderSignal.shape[0]))
#Pad to next power to 2 to avoid cyclic convolution
HeaderSignal=np.pad(HeaderSignal, (0,(next_power_of_2(HeaderSignal.shape[0])-HeaderSignal.shape[0])) )
DemodSignalReceived=np.pad(DemodSignalReceived, (0,(next_power_of_2(DemodSignalReceived.shape[0])-DemodSignalReceived.shape[0])) )
correlation_values_3 = np.fft.ifft(np.fft.fft(DemodSignalReceived) * np.conj(np.fft.fft(HeaderSignal)))
 

delay_header= np.argmax(np.abs(correlation_values_3))

if correlation_values_3[delay_header].real<0:
    DemodSignalReceived=-1*DemodSignalReceived

plt.figure(5)
plt.rcParams['interactive'] == True
plt.title("Line Graph")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
#plt.xlim((164400,164700))
plt.plot(np.abs(correlation_values_3), color="red")


HeaderSignal=np.roll(HeaderSignal,delay_header)
t = np.arange(0, HeaderSignal.shape[0], 1)
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, HeaderSignal, t, DemodSignalReceived)
axs[0].set_xlim(0, HeaderSignal.shape[0])
axs[0].set_xlabel('Sample delay')
axs[0].set_ylabel('Sent Signal and Received Signal Demodded')
axs[0].grid(True)
#Plot correaltion peaks between the two signals
cxy, f = axs[1].cohere(HeaderSignal, DemodSignalReceived, 256, 1. / 1)
axs[1].set_ylabel('Coherence')

fig.tight_layout()
plt.show()

#print("Delay:"+str(delay))
#print("Demod_Delay:"+str(delay_demod))
print("Header_Delay:"+str(delay_header))

#Write Result to file
#with open("Results.txt", "a") as att_file:
#    att_file.write(str(delay_header)+"\n")
    
#Part of associate delay with Sent Signal
#Signal Length is sps*24*8 of data sandwiched between sps*50*8 of Pilot and sps*50*8 of tail
Signal_length=sps*24*8  
PT_length=sps*450*8
offset=Signal_length+2*PT_length
i=0
SentSignal_location=[]
#Find out location of Signal
while offset*i<SentSignal.shape[0]: 
    SentSignal_location.append((offset*i+PT_length))
    i=i+1

ReceivedSignal_Location=[]

#Slice Length to see how much of array to slice, smaller values have lesser chance of having multiple peaks within the same slice.
#If an unlucky event happens where the same peak is in two slices, then change the slice length

p=0
delay_peak_previous=0

#Find out location of Received Peaks from Correlation_values_3
while p+slice_length<correlation_values_3.shape[0]:
    correlation_array_slice=correlation_values_3[p:p+slice_length]
    delay_peak= np.argmax(np.abs(correlation_array_slice))    
   #Set peak as 0.0002 for 2million sample rate and 0.1 for 250000 sample rate
    if abs(correlation_array_slice[delay_peak])>cut_off_limit_correlation:
        
        if abs(p+delay_peak-delay_peak_previous)<delaypeakbreaker:    
            if correlation_values_3[delay_peak_previous]<correlation_values_3[delay_peak]:                           
                ReceivedSignal_Location[-1]=p+delay_peak
            p+=slice_length
            continue
        ReceivedSignal_Location.append(p+delay_peak)
        delay_peak_previous=p+delay_peak
    
    p+=slice_length
           

#Finally Iterate through every Sentsignal location and associate it with ReceivedSignal Location to find the delays
#Indices for both arrays, asynchronous because we want to detect missed packets using a max delay threshold.
j=0
k=0

delay_values=[]
for j in range(len(ReceivedSignal_Location)):
    while ReceivedSignal_Location[j]-SentSignal_location[j]>max_delay_allowed:
        del SentSignal_location[j]
    delay_values.append(ReceivedSignal_Location[j]-SentSignal_location[j])   
    print("identifier")
  
#Write Result to file
with open("Results.txt", "a") as att_file:
    for item in delay_values:
        att_file.write(str(item)+"\t")
    att_file.write(str(item)+"\n")


