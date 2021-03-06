# Copyright (C) 2014 Christopher Hewitt
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from .. import device 
from gpib import GpibError
import numpy
import sys

class TektronixTDS(device.Instrument):
    """Control Tektronix TDS Family Digitizing Oscilloscopes
    
    Supported: TDS 410, 420, 460, 520A, 524A, 540A, 544A, 620A, 640A, 644A, 684A, 744A, & 784A
    """

    def __init__(self, name = 'gpib0', pad = None, sad = 0, timeout = 13, send_eoi = 1, eos_mode = 0):
        super(TektronixTDS, self).__init__(name, pad, sad, timeout, send_eoi, eos_mode)

        self.supported_devices = ['410', '420', '460', '520A', '524A', '540A', '544A', 
                                  '620A', '640A', '644A', '684A', '744A', '784A']

        self.sources =           ['CH1', 'CH2', 'CH3', 'CH4', 
                                  'MATH1', 'MATH2', 'MATH3', 
                                  'REF1', 'REF2', 'REF3', 'REF4']

        self.encodings =         ['ASCIi', 
                                  'RIBinary', 'RPBinary', 
                                  'SRIbinary', 'SRPbinary']

        self.hardcopy_formats =  ['BMP', 'BMPCOLOR', 'DESKJet', 'DPU411', 'DPU412', 
                                  'EPSCOLImg', 'EPSColor', 'EPSImage', 'EPSMono', 'EPSOn', 
                                  'HPGl', 'INTERLeaf', 'LASERJet', 'PCX', 'PCXCOLOR', 
                                  'RLE', 'THInkjet', 'TIFf']

    def get_identity(self):
        """Returns the digitizing oscilloscope identification code.
        
        Syntax: *IDN?
        """
        self.write('*IDN?')
        return self.read().strip()

    def set_wait(self):
        """(Wait) Prevents the digitizing oscilloscope from executing further commands or
        queries until all pending operations finish. This command allows you to
        synchronize the operation of the digitizing oscilloscope with your application
        program.

        Syntax: *WAI
        """
        self.write('*WAI')

    def get_busy(self):
        """Returns the status of the digitizing oscilloscope. This command allows you to
        synchronize the operation of the digitizing oscilloscope with your application
        program.

        Syntax: BUSY?
        """
        self.write('BUSY?')
        bsy = self.read()
        return '1' in bsy

    def get_identity(self):
        """Returns the digitizing oscilloscope identification code.
        
        Syntax: *IDN?
        """
        self.write('*IDN?')
        return self.read().strip()

    def set_hardcopy_format(self, fmt):
        """Selects the output data format for hardcopies. This is equivalent to setting
        Format in the Hardcopy menu.
        
        Syntax: HARDCopy:FORMat { BMP | BMPCOLOR (TDS 5XXA, 6XXA, & 7XXA series
        only) | DESKJet | DPU411 | DPU412 | EPSCOLImg (TDS 5XXA, 6XXA,
        744 series only) | EPSColor | EPSImage | EPSMono | EPSOn | HPGl |
        INTERLeaf | LASERJet | PCX | PCXCOLOR (TDS 5XXA, 6XXA, & 7XXA
        series only) | RLE (TDS 5XXA, 6XXA, & 7XXA series only) | THInkjet |
        TIFf }
        """
        if fmt in self.hardcopy_formats:
            self.write('HARDCopy:FORMat {fmt}'.format(fmt=fmt))

    def get_hardcopy_format(self):
        """Queries the output data format for hardcopies.
        
        Syntax: HARDCopy:FORMat?
        """
        self.write('HARDCopy:FORMat?')
        return self.read().strip()

    def set_hardcopy(self, cmd):
        """Sends a copy of the screen display followed by an EOI to the port specified by
        HARDCopy:PORT. The format and layout of the output is specified with the
        HARDCopy:FORMat and HARDCopy:LAYout commands. This command is
        equivalent to pressing the front-panel HARDCOPY button.

        Syntax: HARDCopy { ABOrt | CLEARSpool | STARt }
        """
        if cmd in ['ABOrt', 'CLEARSpool', 'STARt']:
            self.write('HARDCopy {cmd}'.format(cmd=cmd))
            if cmd is 'STARt':
                while self.get_busy():
                    pass

    def get_hardcopy(self):
        """Query returns format, layout, and port information.

        Syntax: HARDCopy?
        """
        self.write('HARDCopy?')
        return self.read().strip()

    def set_data_source(self, wfm):
        """Sets the location of the waveform data that is transferred from the
        instrument by the CURVe? query. The source data is always transferred in a
        predefined order regardless of the order they are specified using this command.
        The predefined order is CH1 through CH4, MATH1 through MATH3, then
        REF1 through REF4.
        
        Syntax: DATa:SOUrce <wfm>[<Comma><wfm>]...
        """
        if wfm in self.sources:
            self.write('DATa:SOUrce {waveform}'.format(waveform=wfm))

    def get_data_source(self, wfm):
        """Queries the location of the waveform data that is transferred from the
        instrument by the CURVe? query.
        
        Syntax: DATa:SOUrce?
        """
        self.write('DATa:SOUrce?')
        return self.read().strip()

    def set_data_encoding(self, enc):
        """Sets the format of the waveform data. This command is equivalent to
        setting WFMPre:ENCdg, WFMPre:BN_Fmt, and WFMPre:BYT_Or as shown
        in Table 2–26. Setting the DATa:ENCdg value causes the corresponding
        WFMPre values to be updated and vice versa.

        Syntax: DATa:ENCdg { ASCIi | RIBinary | RPBinary | SRIbinary | SRPbinary }
        """
        if enc in self.encodings:
            self.write('DATa:ENCdg {encoding}'.format(encoding=enc))

    def get_data_encoding(self):
        """Queries the format of the waveform data.

        Syntax: DATa:ENCdg?
        """
        self.write('DATa:ENCdg?')
        return self.read().strip()

    def set_data_start(self, start):
        """Sets the starting data point for waveform transfer. This command
        allows for the transfer of partial waveforms to and from the digitizing oscillo-
        scope.

        Syntax: DATa:STARt <NR1>
        """
        self.write('DATa:STARt {start}'.format(start=start))

    def get_data_start(self):
        """Sets the starting data point for waveform transfer.

        Syntax: DATa:STARt?
        """
        self.write('DATa:STARt?')
        return int(self.read())

    def set_data_stop(self, stop):
        """Sets the last data point that will be transferred when using the
        CURVe? query. This allows the transfer of partial waveforms to the controller.

        When using the CURVe command, the digitizing oscilloscope will stop reading
        data when there is no more data to read or when the specified record length has
        been reached so this command will be ignored.

        Syntax: DATa:STOP <NR1>
        """
        self.write('DATa:STOP {stop}'.format(stop=stop))

    def get_data_stop(self):
        """Queries the last data point that will be transferred when using the
        CURVe? query.

        Syntax: DATa:STOP?
        """
        self.write('DATa:STOP?')
        return int(self.read())

    def set_data_width(self, width):
        """Sets the number of bytes per data point in the waveform transferred using the
        CURVe command.

        Syntax: DATa:WIDth <NR1>
        """
        if width in (1, 2):
            self.write('DATa:WIDth {width}'.format(width=width))

    def get_data_width(self):
        """Queries the number of bytes per data point in the waveform transferred using the
        CURVe command.

        Syntax: DATa:WIDth?
        """
        self.write('DATa:WIDth?')
        return int(self.read())

    def get_curve(self):
        enc = self.get_data_encoding()
        width = self.get_data_width()

        self.write('CURVe?')
        if 'ASCI' in enc:
            """Just an ASCII string with terminating newline"""
            crv = ""
            while 1:
                buf = self.read()
                crv += buf
                if '\n' in buf:
                    break
            return crv.strip()
        else:
            """Header and binary sequence with terminating newline"""
            self.read(1)
            x = int(self.read(1))
            y = int(self.read(x))
            buff = self.read((y * width) + 1)
            dtype = ''

            if 'SRP' in enc:
                """Unsigned integer, least significant bit first"""
                dtype = '<u{width}'.format(width=width)
            elif 'SRI' in enc:
                """Signed integer, least significant bit first"""
                dtype = '<i{width}'.format(width=width)
            elif 'RPB' in enc:
                """Unsigned integer, most significant bit first"""
                dtype = '>u{width}'.format(width=width)
            elif 'RIB' in enc:
                """Signed integer, most significant bit first"""
                dtype = '>i{width}'.format(width=width)

            crv = numpy.ndarray((y,), buffer=buff, dtype=dtype)
            return crv

    def get_waveform(self):
        """Returns WFMPre? and CURVe? data for the waveform or waveforms as
        specified by the DATa:SOUrce command. This command is equivalent to
        sending WFMPre?; CURVe?

        Syntax: WAVFrm?
        """
        self.write('WAVFrm?')
        return self.read().strip()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python -m devices.tektronix.tds <devicename>")
        sys.exit(1)
        
    try:
        print("testing connection to '{name}'...\n".format(name=sys.argv[1]))
        tds = TektronixTDS(sys.argv[1])
        tds.clear()
        tds.set_data_encoding('RIBinary')
        tds.set_data_stop('15000')
        tds.set_hardcopy_format('BMPCOLOR')
        print("     identity: {idn}"  .format(idn=tds.get_identity()))
        print("  first point: {first}".format(first=tds.get_data_start()))
        print("   last point: {last}" .format(last=tds.get_data_stop()))
        print("     encoding: {enc}"  .format(enc=tds.get_data_encoding()))
        print("       format: {fmt}"  .format(fmt=tds.get_hardcopy_format()))
        print("        curve: {crv}"  .format(crv=tds.get_curve()))
        #tds.set_hardcopy('STARt')
        tds.clear()
        print("\ndone!")

        import matplotlib.pyplot as plt
        import matplotlib.animation as ani
        fig, ax = plt.subplots()
        line, = ax.plot(tds.get_curve())
        plt.ylabel('Voltage')
        plt.xlabel('Time')

        def update(data):
            line.set_ydata(data)
            return line,

        def data_gen():
            while True: yield tds.get_curve()

        anim = ani.FuncAnimation(fig, update, data_gen, interval=10)
        plt.show()
    except GpibError as msg:
        device.handle_error(msg)


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

