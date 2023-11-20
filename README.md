# GNURADIO_THESIS_MASTER
GNU radio files for thesis, repository still messy. 
For a starter, look inside Delfi Board Correlation folder. 

TransmissionTest2Final (+edited) .py is the file used for transmission and recording. Transformer.py is run for quadrature demodulation before correlation(grc(GNU Radio Companion) file of transformer is lost unfortunately). 
Any of the correlation files under Different Rate folder are reasonably upto date.

To run these files, install GNU Radio libs using radioconda (https://github.com/ryanvolz/radioconda), then use that environment with any compiler.
Note: Most of the code is configured for maximum visibility with SPYDER IDE (Holds a database of varaibles for access post run). However, the use of Matplotlib with the IDE seems to cause memory leaks which slow down the PC.

Encoder code is not uploaded here yet for safety reasons.

TODO for this repo:
Clean Up Work.
See if encoder code can be added.
