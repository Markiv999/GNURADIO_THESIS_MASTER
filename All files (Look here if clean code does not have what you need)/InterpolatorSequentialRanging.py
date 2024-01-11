#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: LocalAdmin
# GNU Radio version: 3.10.6.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class InterpolatorSequentialRanging(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "InterpolatorSequentialRanging")

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
        self.samp_rate = samp_rate = 2000000
        self.Interpolation = Interpolation = 10
        self.samp_rate_interpolated = samp_rate_interpolated = samp_rate*Interpolation
        self.vectorsize = vectorsize = 1875000*5
        self.lowPassTaps = lowPassTaps = firdes.low_pass(1.0, samp_rate_interpolated, samp_rate_interpolated/(Interpolation*2),samp_rate_interpolated/(Interpolation*4), window.WIN_HAMMING, 6.76)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
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
        self.interp_fir_filter_xxx_0_0_0 = filter.interp_fir_filter_ccc(Interpolation, lowPassTaps)
        self.interp_fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccc(Interpolation, lowPassTaps)
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_head_3_0_1_1 = blocks.head(gr.sizeof_gr_complex*1, (vectorsize*Interpolation))
        self.blocks_head_3_0_1 = blocks.head(gr.sizeof_gr_complex*1, (vectorsize*Interpolation))
        self.blocks_head_3_0_0 = blocks.head(gr.sizeof_gr_complex*1, vectorsize)
        self.blocks_head_3_0 = blocks.head(gr.sizeof_gr_complex*1, vectorsize)
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'D:\\GNURadioThesisReportData\\ReceviedSignal1', True, 0, 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'D:\\GNURadioThesisReportData\\SentSignal1', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'D:\\GNURadioThesisReportData\\ReceviedSignalInterpolated1', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'D:\\GNURadioThesisReportData\\SentSignalInterpolated1', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_head_3_0, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_head_3_0_0, 0), (self.interp_fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_head_3_0_1, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_head_3_0_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_head_3_0_1_1, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_head_3_0_1_1, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_head_3_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_head_3_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_head_3_0_1_1, 0))
        self.connect((self.interp_fir_filter_xxx_0_0_0, 0), (self.blocks_head_3_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "InterpolatorSequentialRanging")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_interpolated(self.samp_rate*self.Interpolation)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_Interpolation(self):
        return self.Interpolation

    def set_Interpolation(self, Interpolation):
        self.Interpolation = Interpolation
        self.set_lowPassTaps(firdes.low_pass(1.0, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.Interpolation*2), self.samp_rate_interpolated/(self.Interpolation*4), window.WIN_HAMMING, 6.76))
        self.set_samp_rate_interpolated(self.samp_rate*self.Interpolation)
        self.blocks_head_3_0_1.set_length((self.vectorsize*self.Interpolation))
        self.blocks_head_3_0_1_1.set_length((self.vectorsize*self.Interpolation))

    def get_samp_rate_interpolated(self):
        return self.samp_rate_interpolated

    def set_samp_rate_interpolated(self, samp_rate_interpolated):
        self.samp_rate_interpolated = samp_rate_interpolated
        self.set_lowPassTaps(firdes.low_pass(1.0, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.Interpolation*2), self.samp_rate_interpolated/(self.Interpolation*4), window.WIN_HAMMING, 6.76))

    def get_vectorsize(self):
        return self.vectorsize

    def set_vectorsize(self, vectorsize):
        self.vectorsize = vectorsize
        self.blocks_head_3_0.set_length(self.vectorsize)
        self.blocks_head_3_0_0.set_length(self.vectorsize)
        self.blocks_head_3_0_1.set_length((self.vectorsize*self.Interpolation))
        self.blocks_head_3_0_1_1.set_length((self.vectorsize*self.Interpolation))

    def get_lowPassTaps(self):
        return self.lowPassTaps

    def set_lowPassTaps(self, lowPassTaps):
        self.lowPassTaps = lowPassTaps
        self.interp_fir_filter_xxx_0_0.set_taps(self.lowPassTaps)
        self.interp_fir_filter_xxx_0_0_0.set_taps(self.lowPassTaps)




def main(top_block_cls=InterpolatorSequentialRanging, options=None):

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

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
