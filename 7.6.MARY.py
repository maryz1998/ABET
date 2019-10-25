#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gnuradio import gr
from gnuradio import analog
from gnuradio import blocks
from gnuradio import qtgui 
from gnuradio.filter import firdes
from gnuradio import audio 
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, sip
import tres as SUMA
import VECTOR5 as vector
import Vectoraverage as Vectoraverage

class flujograma(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        # Nuestras variables especificas
        muestreo=48000
        T=1./muestreo
        f=1000
        N=128
        s=blocks.wavfile_source('/media/mary/F000-ED40/comunicaciones2/Lab4/liberias/Mary.wav', True)
        nse=analog.noise_source_f(analog.GR_GAUSSIAN,0.001)
        add=SUMA.SUMA_cc()
        snk=qtgui.time_sink_f(
           512,
           muestreo,
           'señal Promediada',
           1
       )
        str2vec=blocks.stream_to_vector(gr.sizeof_float*1,N)
        e_fft=vector.vector_fft_ff(N,T)
        average=Vectoraverage.vector_average_hob(N,100)
        vsnk=qtgui.vector_sink_f(
           N,
           -muestreo/2.,
           muestreo/N,
           'frecuencia',
           'Magnitud',
           'FT en Magnitud de la Voz de Mary',
           1
       )
        vsnk.enable_autoscale(True)
        self.connect(s,(add,0))
        self.connect(nse,(add,1))
        self.connect(add,snk)
        self.connect(add,str2vec,e_fft,average,vsnk)
     
        #para graficar
        pyobj=sip.wrapinstance(vsnk.pyqwidget(),QtWidgets.QWidget)
        pyobj.show()

#Clase principal

def main():
    qapp=QtWidgets.QApplication(sys.argv)
    simulador_de_la_envolvente_compleja=flujograma()
    simulador_de_la_envolvente_compleja.start()
    qapp.exec_()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
