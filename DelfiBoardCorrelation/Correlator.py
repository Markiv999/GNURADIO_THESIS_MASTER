# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:29:29 2023

@author: LocalAdmin
"""
import numpy as np
import matplotlib.pyplot as plt



def main(options=None):
    print("Correlator was Called")
    #regenerate header and demodsignals at correct sample rate and sps before correlation
    sps=int(250000/9600)
    plt.close('all')
    #DemodRemodSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DemodRemodSignals', dtype=np.complex64, sep='', offset=0) 
    
    ReceivedSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\ReceivedSignals3', dtype=np.complex64, sep='', offset=0) 
    
    SentSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\SentSignals5', dtype=np.complex64, sep='', offset=0) 
    
    DemodSignalSent=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\Demodsignalsent', dtype=np.float32, sep='', offset=0) 
    
    DemodSignalReceived=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DemodsignalReceived', dtype=np.float32, sep='', offset=0) 
    
    
    HeaderSignal=np.fromfile('D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DelfiPQHeader', dtype=np.float32, sep='', offset=0) 
    
    
    
    #DemodSignal= SentSignal
    skip=int(50*sps*8)
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
    skip=50*sps*8
    hold=24*sps*8
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
    
    
    #CorrelateHeaderSequence
    HeaderSignal=np.pad(HeaderSignal,(0,DemodSignalReceived.shape[0]-HeaderSignal.shape[0]))
    correlation_values_3 = np.fft.ifft(np.fft.fft(DemodSignalReceived) * np.conj(np.fft.fft(HeaderSignal)))
    delay_header= np.argmax(np.abs(correlation_values_3))
    
    
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
    
    print("Delay:"+delay)
    print("Demod_Delay:"+delay_demod)
    print("Header_Delay:"+delay_header)
    
    with open("Results.txt", "a") as att_file:
        att_file.write(str(delay_header)+"\n")