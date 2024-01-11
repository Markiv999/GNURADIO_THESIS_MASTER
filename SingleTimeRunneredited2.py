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
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip
import numpy as np



class SingleTimeRunner(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "SingleTimeRunner")

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
        self.variable_qtgui_range_0 = variable_qtgui_range_0 = 0
        self.sps = sps = 300
        self.samp_rate = samp_rate = 250000

        ##################################################
        # Blocks
        ##################################################

        self._variable_qtgui_range_0_range = Range(0, 15000, 1, 0, 200)
        self._variable_qtgui_range_0_win = RangeWidget(self._variable_qtgui_range_0_range, self.set_variable_qtgui_range_0, "'variable_qtgui_range_0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._variable_qtgui_range_0_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "type=b200")),
            uhd.stream_args(
                cpu_format="fc32",
                otw_format="sc16",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # Set the time to GPS time on next PPS
        # get_mboard_sensor("gps_time") returns just after the PPS edge,
        # thus add one second and set the time on the next PPS
        self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec(self.uhd_usrp_source_0.get_mboard_sensor("gps_time").to_int() + 1.0))
        # Sleep 1 second to ensure next PPS has come
        time.sleep(1)

        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(145e6, 5e6), 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_gain(60, 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(('', "type=b200")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        # Set the time to GPS time on next PPS
        # get_mboard_sensor("gps_time") returns just after the PPS edge,
        # thus add one second and set the time on the next PPS
        self.uhd_usrp_sink_0_0.set_time_next_pps(uhd.time_spec(self.uhd_usrp_sink_0_0.get_mboard_sensor("gps_time").to_int() + 1.0))
        # Sleep 1 second to ensure next PPS has come
        time.sleep(1)

        self.uhd_usrp_sink_0_0.set_center_freq(uhd.tune_request(145e6, 5e6), 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0_0.set_gain(50, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        
        self.uhd_usrp_sink_0_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_sink_0_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_time_source('gpsdo', 0)
        print(self.uhd_usrp_sink_0_0.get_mboard_sensor("gps_locked",0)) 
        print(np.float64(self.uhd_usrp_sink_0_0.get_time_last_pps().get_real_secs()))
        gpstime=self.uhd_usrp_source_0.get_mboard_sensor("gps_time").to_int() + 1.0
        print(np.float64(gpstime))
        starttime=gpstime+ 5
        #sync to PPS for usrp source and sink
        self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec(gpstime))
        self.uhd_usrp_sink_0_0.set_time_next_pps(uhd.time_spec(gpstime))
        #Set start time for usrp source and sinkv
        self.uhd_usrp_source_0.set_start_time(uhd.time_spec(starttime))
        self.uhd_usrp_sink_0_0.set_start_time(uhd.time_spec(starttime))
        # Sleep 1 second to ensure next PPS has come
        time.sleep(1)
        print(self.uhd_usrp_sink_0_0.get_mboard_sensor("gps_locked",0))
        print(np.float64(self.uhd_usrp_sink_0_0.get_time_last_pps().get_real_secs()))
        print(np.float64(gpstime))
        
        
        
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=sps,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,log=False)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=sps,
            sensitivity=1.0,
            bt=0.5,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b((0x0B ,0xF1 ,0xC4 ,0x1A ,0x17 ,0x17 ,0x3E ,0x51 ,0x2C ,0x93 ,0x0F ,0xD0 ,0x2C ,0x43 ,0x84 ,0xB0 ,0xDF ,0x04 ,0x4A ,0x99 ,0x26 ,0x0B ,0xDE ,0x92 ,0xAB ,0xC7 ,0x69 ,0x15), True, 1, [])
        self.blocks_unpack_k_bits_bb_1_1 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
       #self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, (samp_rate*5))
        #self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, (samp_rate*5))
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_head_0_0_0 = blocks.head(gr.sizeof_char*1, (28*100*15))
        self.blocks_head_0_0 = blocks.head(gr.sizeof_gr_complex*1, (sps*28*100*15))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, (sps*28*100*15))
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_gr_complex*1, 'D:\\GNURADIO_THESIS_MASTER\\DemodRemodProcess\\RecievedSignal', False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, 'D:\\GNURADIO_THESIS_MASTER\\DemodRemodProcess\\DemoddedSignal', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'D:\\GNURADIO_THESIS_MASTER\\DemodRemodProcess\\SentSignal', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_2 = blocks.delay(gr.sizeof_gr_complex*1, variable_qtgui_range_0)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 0)
        self.analog_agc_xx_0 = analog.agc_cc((1e-3), 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_head_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_delay_2, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_head_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.blocks_head_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_head_0_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_gfsk_mod_0, 0))
        #self.connect((self.blocks_skiphead_0, 0), (self.blocks_head_0_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_gmsk_demod_0, 0))
        #self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_unpack_k_bits_bb_1_1, 0))
        self.connect((self.blocks_unpack_k_bits_bb_1_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.blocks_delay_2, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.blocks_head_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blocks_head_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SingleTimeRunner")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_range_0(self):
        return self.variable_qtgui_range_0

    def set_variable_qtgui_range_0(self, variable_qtgui_range_0):
        self.variable_qtgui_range_0 = variable_qtgui_range_0
        self.blocks_delay_2.set_dly(int(self.variable_qtgui_range_0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_head_0.set_length((self.sps*28*10))
        self.blocks_head_0_0.set_length((self.sps*28*10))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)




def main(top_block_cls=SingleTimeRunner, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()
    
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        #qapp.exit()
        Qt.QApplication.quit()
        qapp.closeAllWindows()
        #import Remodder
        #Remodder.main()
        tb.stop()
        tb.wait()
     
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(30000)
    timer.setSingleShot(True)
    #timer.timeout.connect()
    

    qapp.exec_()

if __name__ == '__main__':
    main()
