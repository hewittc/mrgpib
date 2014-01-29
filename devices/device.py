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

