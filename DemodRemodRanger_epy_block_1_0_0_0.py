import numpy as np
from gnuradio import gr
import scipy as scipy

class CorrelationDelayEstimator(gr.decim_block):
    def __init__(self, vectorsize=18750, sample_rate=500000, max_delay=1000):
        gr.decim_block.__init__(
            self,
            name='CorrelationDelayEstimator',
            in_sig=[np.ubyte, np.ubyte],
            out_sig=[np.float32],
            decim=vectorsize
        )
        self.set_relative_rate(1.0/vectorsize)
        self.decimation = vectorsize
        self.vectorsize = vectorsize
        self.range_clock_signal = np.zeros(vectorsize, dtype=np.ubyte)
        self.sequential_signal = np.zeros(vectorsize, dtype=np.ubyte)
        self.i = 0
        self.j = 0
        self.counter = 0
        self.sample_rate = sample_rate
        self.correlation_values = np.zeros(vectorsize, dtype=np.ubyte)
        self.max_delay=max_delay

    def work(self, input_items, output_items):
        sequential_signal = input_items[0]
        range_clock_signal = input_items[1]
        num_samples = sequential_signal.shape[0]
        n=1
        # Process each sample in the input buffer
        for k in range(num_samples):
            if self.i < self.vectorsize/n:
                # Take the latest values from the buffer
                self.range_clock_signal[self.i] = range_clock_signal[k]
                self.sequential_signal[self.i] = sequential_signal[k]
                self.i += 1
            else:
                # Calculate delay
                #self.range_clock_signal=self.range_clock_signal[0 : self.vectorsize/n]
                #self.sequential_signal = self.sequential_signal[0 : self.vectorsize/n]
                self.correlation_values = np.fft.ifft(np.fft.fft(self.range_clock_signal) * np.conj(np.fft.fft(self.sequential_signal)))
                #self.correlation_values= scipy.signal.correlate(self.range_clock_signal, self.sequential_signal, mode='full', method='auto')
                self.sample_delay_count = np.argmax(np.abs(self.correlation_values))
               # self.sample_delay_count=np.argmax(np.correlate(self.range_clock_signal,self.sequential_signal))
                delay = self.vectorsize - self.sample_delay_count
                delay_in_micro_seconds = 10 ** 6 * delay / self.sample_rate
                #correlationfactor=self.correlation_values[self.sample_delay_count]/np.sum(np.abs(self.correlation_values))
                output_items[0][0] = delay
                #n=n*2
                #if n==16:
                #    n=1
                self.i = 0
        self.j = 0
        return num_samples // self.vectorsize
