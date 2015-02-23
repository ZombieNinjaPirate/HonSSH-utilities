"""The funcitons in this module can be for manipulating various archive types. """


"""
Copyright (c) 2015, Are Hansen - Honeypot Development.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND AN
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


__author__ = 'Are Hansen'
__date__ = '2015, Feb 4'
__version__ = '0.0.2'


import os
import gzip


def xtrctgz(pathgz, xtrcpath):
    """Extract the compressed gz arghive (pathgz) into its uncompressed path (xtrcpath).
    If the location leading up to the xtrcpath dont exists it will be created, given that
    the EUID allows it to be. The xtrcpath is returned when the function completes. """
    ucgzl = '/'.join(xtrcpath.split('/')[:-1])

    print ucgzl
    if not os.path.isdir(ucgzl):
        try:
            os.mkdir(ucgzl)
        except OSError, mkerr:
            print '{0}'.format(mkerr)
            sys.exit(1)

    inngz = gzip.open(pathgz, 'rb')
    outgz = open(xtrcpath, 'wb')
    outgz.write(inngz.read())
    inngz.close()
    outgz.close()

    return xtrcpath
