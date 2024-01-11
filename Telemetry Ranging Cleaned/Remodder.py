#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.6.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import time
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



class Transofrmer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Transofrmer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        #%% Set Correct Samp Rate/Bit Rate
        self.samp_rate = samp_rate = 500000
        self.bitrate = bitrate = 9600
        self.sps = sps = int(samp_rate/bitrate)

        ##################################################
        # Blocks
        ##################################################

        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (5000*4),  #previously 5000*8
                (2500*4),  #previously 2500*8
                window.WIN_HAMMING,
                6.76))
        self.digital_gfsk_mod_2 = digital.gfsk_mod(
            samples_per_symbol=sps,
            sensitivity=(2*3.14/sps),
            bt=0.5,
            verbose=False,
            log=False,
            do_unpack=True)
        
        #%% Set Marker to Correlate for Here


        #Header without Scrambling
        #self.blocks_vector_source_x_0 = blocks.vector_source_b((11, 108, 251, 51, 123, 75, 80, 180, 187, 116, 219, 83, 44, 81, 213, 95), False, 1, [])
        
        #Attach Sink Marker [173, 173, 173, 173, 173, 173, 173, 173, 173, 173]  ,[ 173, 45, 210, 146, 109, 18, 18, 178, 77, 93]
        self.blocks_vector_source_x_0 = blocks.vector_source_b((85, 85, 85, 85), False, 1, [])
        #self.blocks_vector_source_x_0 = blocks.vector_source_b((33,34,35,36,37,38,39,40,41,48), False, 1, [])
        #Header with Scrambling (pilot sequence also included to allow go beyond scrambler memory)
        #self.blocks_vector_source_x_0 = blocks.vector_source_b((11, 241, 196, 26, 93, 86, 5, 53, 175, 62, 218, 140, 59, 123, 84, 246, 27, 228, 77, 72, 6, 183, 108, 225, 252, 219, 156, 159, 67, 48, 182, 63, 235, 79, 107, 241, 244, 25, 69, 102, 10, 45, 89, 61, 193, 188, 5, 224, 162, 4, 143, 180, 66, 96, 249, 193, 30, 15, 145, 0, 38, 124, 138, 8, 27, 123, 68, 247, 19, 244, 72, 64, 94, 219, 60, 32, 168, 137, 216, 21, 233, 224, 197, 183, 125, 39, 72, 75, 243, 52, 224, 116, 137, 140, 34, 250, 192, 47, 156, 16, 241, 249, 153, 155, 171, 137, 147, 163, 13, 31, 169, 139, 178, 128, 15, 190, 2, 193, 211, 131, 47, 13, 153, 161, 168, 52, 169, 174, 48, 202, 234, 53, 34, 219, 184, 26, 217, 20, 82, 132, 69, 141, 94, 191, 151, 8, 145, 173, 172, 242, 231, 169, 247, 181, 126, 115, 166, 253, 66, 84, 122, 147, 106, 129, 227, 160, 53, 45, 182, 179, 78, 147, 176, 140, 46, 122, 14, 99, 31, 254, 142, 233, 87, 31, 36, 131, 36, 141, 46, 7, 115, 184, 6, 232, 194, 179, 14, 226, 77, 249, 42, 192, 19, 193, 203, 2, 171, 85, 30, 5, 145, 165, 44, 126, 175, 43, 91, 222, 238, 255, 102, 119, 42, 183, 192, 217, 19, 3, 71, 75, 41, 233, 244, 149, 77, 224, 134, 6, 221, 144, 73, 50, 73, 67, 68, 6, 230, 161, 157, 253, 190, 110, 125, 91, 207, 189, 207, 172, 55, 181, 158, 125, 214, 29, 116, 39, 6, 157, 20, 97, 50, 221, 74, 68, 255, 147, 120, 0, 194, 242, 176, 172, 172, 98, 110, 233, 39, 24, 28, 243, 63, 180, 154, 109, 21, 25, 37, 224, 50, 13, 205, 73, 54, 251, 112, 126, 16, 149, 69, 149, 223, 59, 207, 143, 53, 148, 61, 119, 55, 54, 22, 4, 149, 181, 239, 122, 254, 236, 111, 78, 61, 186, 59, 128, 91, 59, 96, 213, 67, 192, 99, 24, 254, 253, 110, 86, 172, 191, 99, 87, 122, 34, 225, 193, 146, 7, 29, 225, 84, 41, 108, 54, 218, 61, 138, 77, 69, 94, 36, 227, 118, 230, 43, 239, 85, 252, 11, 192, 71, 26, 172, 217, 101, 4, 28, 61, 51, 51, 84, 82, 17, 246, 233, 107, 28, 250, 191, 40, 83, 239, 233, 247, 149, 124, 99, 134, 247, 82, 240, 120, 129, 74, 160, 156, 93, 71, 126, 96, 246, 116, 88, 244, 135, 158, 233, 143, 198, 155, 116, 4, 4, 188, 183, 107, 211, 246, 40, 103, 108, 187, 131, 27, 14, 195, 149, 166, 110, 75), False, 1, [])

        #11, 241, 196, 26, 93, 86, 5, 53, 175, 62, 218, 140, 59, 123, 84, 246, 27, 228, 77, 72, 12, 218, 53, 48, 183, 109, 211, 149, 46, 102, 143, 165, 67, 120, 104, 196, 70, 216, 176, 25, 167, 104, 91, 207, 111, 239, 183, 242, 90, 34, 123, 165, 131, 70, 113, 112, 128, 251, 11, 70, 21, 110, 143, 241, 146, 65, 19, 207, 75, 237, 229, 214, 81, 112, 193, 74, 138, 243, 20, 182, 63, 198, 29, 124, 39, 130, 149, 22, 229, 27, 221, 206, 204, 245, 87, 209, 40, 4, 234, 178, 32, 133, 230, 226, 99, 169, 245, 181, 95, 113, 166, 92, 72, 20, 91, 177, 98, 93, 144, 59, 79, 29, 249, 26, 41, 164, 170, 52, 37, 246, 103, 61, 190, 187, 202, 31, 186, 10, 131, 83, 138, 111, 157, 48, 227, 104, 185, 193, 62, 13, 129, 32, 44, 108, 46, 10, 9, 91, 111, 229, 183, 87, 80, 32, 84, 235, 154, 50, 144, 206, 186, 114, 4, 231, 178, 246, 8, 229, 116, 219, 9, 35, 226, 60, 214, 31, 142, 67, 140, 82, 71, 134, 127, 8, 28, 171, 238, 75, 237, 101, 222, 17, 240, 233, 8, 26, 251, 92, 54, 147, 140, 143, 240, 70, 2, 189, 212, 125, 83, 21, 102, 34, 47, 205, 21, 201, 40, 136, 226, 52, 172, 174, 98, 79, 235, 39, 185, 22, 179, 30, 150, 152, 220, 63, 83, 20, 102, 50, 164, 160, 28, 157, 67, 46, 60, 63, 153, 109, 126, 205, 128, 16, 235, 166, 49, 78, 242, 182, 172, 207, 100, 111, 10, 57, 216, 127, 149, 56, 103, 228, 179, 71, 147, 36, 5, 44, 174, 162, 67, 139, 231, 133, 117, 107, 18, 250, 88, 38, 80, 136, 222, 55, 114, 146, 110, 145, 32, 164, 100, 234, 130, 35, 157, 214, 231, 22, 6, 39, 229, 217, 0, 55, 199, 236, 185, 145, 22, 119, 198, 231, 115, 250, 120, 164, 72, 232, 84, 15, 148, 0, 116, 249, 139, 26, 138, 219, 22, 34, 23, 206, 137, 241, 37, 20, 61, 55, 51, 22, 86, 16, 180, 253, 235, 94, 190, 186, 74, 7, 123, 138, 251, 148, 58, 119, 68, 177, 23, 183, 14, 85, 150, 224, 161, 182, 207, 3, 56, 249, 87, 98, 249, 50, 60, 20, 245, 229, 218, 81, 182, 205, 73, 76, 206, 148, 112, 243, 201, 187, 129, 155, 39, 129, 21, 47, 38, 155, 4, 3, 60, 204, 172, 82, 109, 241, 23, 23, 4, 5, 60, 175, 170, 83, 142, 239, 215, 116, 98, 2, 239, 209, 116, 1, 4, 238, 50, 106, 203, 10, 209, 228, 242, 9, 246, 208, 210, 238, 99, 61, 209, 237, 220, 139, 216, 6, 146, 148, 158, 253, 94, 85, 180, 143, 108, 79, 140, 33, 250, 241, 172, 156, 225, 126, 153, 168, 40, 168, 96, 44, 204, 36, 90, 169, 121, 61, 209, 189, 13, 240, 167, 12, 221, 181, 75, 112, 236, 72, 76, 94, 29, 48, 35, 100, 211, 108, 91, 191, 18, 154, 15, 166, 185, 51, 235, 11, 150, 146, 136, 193, 54, 141, 13, 104, 174, 192, 69, 154, 133, 155, 229, 141, 84, 237, 26, 89, 214, 79, 113, 46, 84, 140, 156, 113, 119, 209, 56, 5, 226, 162, 37, 141, 180, 227, 106, 185, 224, 60, 13, 32, 42, 108, 77, 12, 8, 184, 113, 37, 212, 49, 93, 158, 115, 228, 131, 14, 222, 33, 201, 135, 88, 26, 254, 12, 181, 109, 242, 151, 46, 199, 133, 229, 98, 90, 106, 117, 108, 146, 129, 159, 167, 203, 81, 174, 76, 205, 20, 73, 48, 73, 98, 76, 107, 30, 122, 150, 106, 211, 102, 161, 39, 188, 22, 225, 155, 151, 138, 77, 159, 1, 193, 98, 8, 111, 124, 62, 137, 100, 214, 51, 140, 149, 160, 91, 145, 31, 253, 220, 240, 143, 90, 18
        
        #%% Dont Touch
        
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate*10) if "auto" == "time" else int(0.1), 1) )
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_gr_complex*1, 'D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\ReceivedSignals3', False, 0, 0)
        self.blocks_file_source_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'D:\\\\GNURADIO_THESIS_MASTER\\\\CorrelationwithDelfiBoard\\\\SentSignals5', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_1_0_0 = blocks.file_sink(gr.sizeof_float*1, 'D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DelfiPQHeader', False)
        self.blocks_file_sink_0_1_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_0 = blocks.file_sink(gr.sizeof_float*1, 'D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\DemodsignalReceived', False)
        self.blocks_file_sink_0_1_0.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_float*1, 'D:\\GNURADIO_THESIS_MASTER\\CorrelationwithDelfiBoard\\Demodsignalsent', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)


        #%% Change if you know better demod parameters
        self.analog_quadrature_demod_cf_0_1 = analog.quadrature_demod_cf(((3.14/2)/(sps)))
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(((3.14/2)/(sps)))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(((3.14/2)/(sps)))


        ##################################################
        # Connections
        ##################################################
        #%% Only touch if you know what you are doing.
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.blocks_file_sink_0_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_1, 0), (self.blocks_file_sink_0_1_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_file_source_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_gfsk_mod_2, 0))
        self.connect((self.digital_gfsk_mod_2, 0), (self.analog_quadrature_demod_cf_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Transofrmer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate/self.bitrate))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (5000*8), (2500*8), window.WIN_HAMMING, 6.76))

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate
        self.set_sps(int(self.samp_rate/self.bitrate))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.analog_quadrature_demod_cf_0.set_gain(((3.14/2)/(self.sps)))
        self.analog_quadrature_demod_cf_0_0.set_gain(((3.14/2)/(self.sps)))
        self.analog_quadrature_demod_cf_0_1.set_gain(((3.14/2)/(self.sps)))




def main(top_block_cls=Transofrmer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()
    print("Transformer Program was Called")
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()
        tb.close()
        Qt.QApplication.closeAllWindows()
        print("Transformer is Over")
        
        

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(15000)
    timer.timeout.connect(sig_handler)
    time.sleep(15)
    qapp.exec_()

if __name__ == '__main__':
    main()
