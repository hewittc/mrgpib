
from .. import device 
from gpib import GpibError
import sys

class TektronixTDS(device.Instrument):
    """Control Tektronix TDS Family Digitizing Oscilloscopes
    
    Supported: TDS 410, 420, 460, 520A, 524A, 540A, 544A, 620A, 640A, 644A, 684A, 744A, & 784A
    """

    def __init__(self, name = 'gpib0', pad = None, sad = 0, timeout = 13, send_eoi = 1, eos_mode = 0):
        super(TektronixTDS, self).__init__(name, pad, sad, timeout, send_eoi, eos_mode)

        self.supported_devices = ['410', '420', '460', '520A', '524A', '540A', '544A', 
                                  '620A', '640A', '644A', '684A', '744A', '784A']

        self.sources = ['CH1', 'CH2', 'CH3', 'CH4', 
                        'MATH1', 'MATH2', 'MATH3', 
                        'REF1', 'REF2', 'REF3', 'REF4']

        self.encodings = ['ASCIi', 
                          'RIBinary', 'RPBinary', 
                          'SRIbinary', 'SRPbinary']

    def get_identity(self):
        """Returns the digitizing oscilloscope identification code.
        
        Syntax: *IDN?
        """
        self.write('*IDN?')
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
        return self.read().strip()

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
        return self.read().strip()

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
        
    print("testing connection to '{name}'...\n".format(name=sys.argv[1]))

    try:
        tds = TektronixTDS(sys.argv[1])
        tds.clear()
        tds.set_data_encoding('SRIbinary')

        print("     identity: {idn}".format(idn=tds.get_identity()))
        print("  first point: {first}".format(first=tds.get_data_start()))
        print("   last point: {last}".format(last=tds.get_data_stop()))
        print("     encoding: {enc}".format(enc=tds.get_data_encoding()))
        print("     waveform: {wfm}".format(wfm=tds.get_waveform()))

        tds.clear()
    except GpibError as msg:
        tds.handle_error(msg)
    
    print("\ndone!")


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

