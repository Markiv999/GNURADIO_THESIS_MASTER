import numpy as np
from gnuradio import gr
import scipy as sp

class CorrelationDelayEstimator(gr.sync_block):
    def __init__(self, vectorsize=18750,sample_rate=500000):
        gr.sync_block.__init__(
            self,
            name='CorrelationDelayEstimator',
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32]
        )
        self.vectorsize = vectorsize
        self.range_clock_signal = np.zeros(vectorsize, dtype=np.complex64)
        self.sequential_signal = np.zeros(vectorsize, dtype=np.complex64)
        self.i = 0
        self.j=0
        self.max = 0
        self.sample_delay_count = 0
        self.correlation_values = np.zeros(vectorsize, dtype=np.complex64)
        self.sample_rate=sample_rate

    def work(self, input_items, output_items):
        #build from ground up
        sequential_signal = input_items[0][:]
        range_clock_signal = input_items[1][:]
        #print(sequential_signal.size)
        #print("yay")
        #print(range_clock_signal.size)
       # self.j+=1
       # print(self.j)
        while self.j<sequential_signal.size:
            if self.i < self.vectorsize:
                self.range_clock_signal[self.i] = range_clock_signal[self.j]
                self.sequential_signal[self.i] = sequential_signal[self.j]
                self.i += 1
                output_items[0][0] = 0
                self.j+=1
                continue
            #Gnu radio automatically takes output items as output, we just need to specify return length
            #Block to calculate Delay 
            self.correlation_values = np.fft.ifft(np.fft.fft(self.range_clock_signal) * np.conj(np.fft.fft(self.sequential_signal)))
            
            self.sample_delay_count = np.argmax(np.abs(self.correlation_values))
            #print(np.amax(self.correlation_values))
            delay=self.vectorsize - self.sample_delay_count
            #Delay_in_micro_seconds= 10**6 * delay/self.sample_rate
            output_items[0][0] = delay
            

            #Print Statements to diagnose
            #print(self.i)
            print(delay)
            #Reset variables
            self.i=0
        
        self.j=0
       # output_items[0][:] = delay_in_micro_seconds
       #Gnu radio automatically takes output items as output, we just need to specify return length
        return 1
