import numpy as np
from gnuradio import gr

class CorrelationDelayEstimator(gr.decim_block):
    def __init__(self, vectorsize=18750, sample_rate=500000):
        gr.decim_block.__init__(
            self,
            name='CorrelationDelayEstimator',
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32],
            decim=vectorsize
        )
        self.set_relative_rate(1.0/vectorsize)
        self.decimation = vectorsize
        self.vectorsize = vectorsize
        self.range_clock_signal = np.zeros(vectorsize, dtype=np.complex64)
        self.sequential_signal = np.zeros(vectorsize, dtype=np.complex64)
        self.i = 0
        self.j = 0
        self.counter = 0
        self.sample_rate = sample_rate
        self.correlation_values = np.zeros(vectorsize, dtype=np.complex64)

    def work(self, input_items, output_items):
        sequential_signal = input_items[0]
        range_clock_signal = input_items[1]
        num_samples = sequential_signal.shape[0]
        
        # Process each sample in the input buffer
        for k in range(num_samples):
            if self.i < self.vectorsize:
                # Take the latest values from the buffer
                self.range_clock_signal[self.i] = range_clock_signal[k]
                self.sequential_signal[self.i] = sequential_signal[k]
                self.i += 1
            else:
                # Calculate delay
                self.correlation_values = np.fft.ifft(np.fft.fft(self.range_clock_signal) * np.conj(np.fft.fft(self.sequential_signal)))
                self.sample_delay_count = np.argmax(np.abs(self.correlation_values))
                delay = self.vectorsize - self.sample_delay_count
                delay_in_micro_seconds = 10 ** 6 * delay / self.sample_rate

                output_items[0][0] = delay
                self.i = 0
                print(delay)

        self.j = 0
        return num_samples // self.vectorsize
