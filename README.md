mrgpib
======

It's Mr. GPIB! Connect test equipment to computer and control it remotely.

Tested with python 2.7.5, linux-gpib 3.2.20, National Instruments PCI-GPIB, and Tektronix TDS684A.

* [Linux-GPIB](http://linux-gpib.sourceforge.net/)

This is a work in progress...

```
% python -m devices.tektronix.tds tds684a
testing connection to 'tds684a'...

     identity: TEKTRONIX,TDS 684A,0,CF:91.1CT FV:v4.2e
  first point: 1
   last point: 500
     encoding: SRI
     waveform: :WFMP:BYT_N 1;BIT_N 8;ENC BIN;BN_F RI;BYT_O LSB;CH1:WFI "Ch1, DC coupling, 143.0mVolts/div, 20.00us/div, 15000 points, Sample mode";NR_P 500;PT_F Y;XUN "s";XIN 400.0E-9;XZE 300.0E-9;PT_O 3000;YUN "Volts";YMU 5.720E-3;YOF 500.0E-3;YZE 0.0E+0;:CURV #3500...

done!
```
