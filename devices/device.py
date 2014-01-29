
import gpib
import sys

class Instrument(object):
    def __init__(self, name='gpib0', pad=None, sad=0, timeout=13, send_eoi=1, eos_mode=0):
        self._own = False
        try:
            if isinstance(name, basestring):
                self.id = gpib.find(name)
                self._own = True
            elif pad is None:
                self.id = name
            else:
                self.id = gpib.dev(name, pad, sad, timeout, send_eoi, eos_mode)
                self._own = True
        except gpib.GpibError as msg:
            print("error: could not open device ({name})".format(name=name))
            print("libgpib: {msg}".format(msg=msg))
            sys.exit(1)

    def __del__(self):
        if self._own:
            gpib.close(self.id)

    def clear(self):
        gpib.clear(self.id)

    def read(self, len=512):
        self.res = gpib.read(self.id, len)
        return self.res

    def write(self, str):
        gpib.write(self.id, str)

def handle_error(msg):
    print("error: executing command failed")
    print("libgpib: {msg}".format(msg=msg))
    sys.exit(1)


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

