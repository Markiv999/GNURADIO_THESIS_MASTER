import numpy as np
from gnuradio import gr
import scipy as sp

class CorrelationDelayEstimator(gr.sync_block):
    def __init__(self, vectorsize=18750,sample_rate=50000):
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
       # self.j=0
        self.max = 0
        self.sample_delay_count = 0
        self.correlation_values = np.zeros(vectorsize, dtype=np.complex64)
        self.sample_rate=sample_rate

    def work(self, input_items, output_items):
        #build from ground up
        sequential_signal = input_items[0][0]
        range_clock_signal = input_items[1][0]
       # self.j+=1
       # print(self.j)
    
        if self.i < self.vectorsize:
            self.range_clock_signal[self.i] = range_clock_signal
            self.sequential_signal[self.i] = sequential_signal
            self.i += 1
            output_items[0][0] = 0
            #Gnu radio automatically takes output items as output, we just need to specify return length
            return 1
        
        self.correlation_values = np.fft.ifft(np.fft.fft(self.range_clock_signal) * np.conj(np.fft.fft(self.sequential_signal)))
         #self.max = np.amax(np.abs(self.correlation_values))
        self.sample_delay_count = np.argmax(np.abs(self.correlation_values))
        delay=self.vectorsize - self.sample_delay_count
       # delay_in_micro_seconds= 10**6 * delay/self.sample_rate
        output_items[0][0] = delay
        print(self.i)
        self.i=0
        
        print(delay)
       # output_items[0][:] = delay_in_micro_seconds
       #Gnu radio automatically takes output items as output, we just need to specify return length
        return 1 
