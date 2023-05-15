from turtle import delay
import numpy as np
from gnuradio import gr

class CorrelationDelayEstimator(gr.sync_block):
    def __init__(self, vectorsize=18750, sample_rate=500000, delayinitial=0):
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
        self.j = 0
        self.delayiterator=0
        self.sample_rate = sample_rate
        self.correlation_values = np.zeros(vectorsize, dtype=np.complex64)
        self.delayinitial=delayinitial

    def work(self, input_items, output_items):
        sequential_signal = input_items[0][:]
        range_clock_signal = input_items[1][:]
        num_samples = sequential_signal.shape[0]
        #print(num_samples)
        
       #while there are still values in the buffer
        while self.j < num_samples:
            if self.i < self.vectorsize:
                #Take the latest values from the buffer
                self.range_clock_signal[self.i] = range_clock_signal[self.j]
                self.sequential_signal[self.i] = sequential_signal[self.j]
                #output_items[0][self.j] = 0
                self.i += 1
                self.j += 1            
                continue
            #
            self.delayiterator+=1
            output_items[0][0] = self.delayiterator
            
            # calculate delay, then return to the while loop
            self.correlation_values = np.fft.ifft(np.fft.fft(self.range_clock_signal) * np.conj(np.fft.fft(self.sequential_signal)))
            self.sample_delay_count = np.argmax(np.abs(self.correlation_values))
            delay = self.vectorsize - self.sample_delay_count
            delay_in_micro_seconds = 10 ** 6 * delay / self.sample_rate
            self.delayinitial=10000
            
            self.i = 0
            print(delay)

        self.j = 0
        return 1