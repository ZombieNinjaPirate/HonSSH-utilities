"""
NOTE: THIS MODULE HAS BEEN OBSOLETE. 
ALL FUNCTIONS MOVED TO: BZ.find.systemobj
"""


"""
Copyright (c) 2014, Are Hansen - Honeypot Development.

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
__date__ = '2014, Oct 18'
__version__ = '0.0.3'


import os
import sys
from os import R_OK, W_OK
from BZ.raising.exceptions import check_true, access_except


def is_found(fpath):
    """Verifies that the path exists. Will raise and exception and call sys.exit(1) 
    if False. """
    try:
        check_true(os.path.exists(fpath))
    except Exception as e:
        access_except('{0} {1} was not found!'.format(e, fpath))
        sys.exit(1)


def has_read(fpath):
    """Checks if the executing user has read access to the given path. Function will 
    return True if the executing user has read access to the path, the function will call 
    sys.exit(1) and give an error if False."""
    is_found(fpath)

    try:
        check_true(os.access(fpath, R_OK))
    except Exception as e:
        access_except('{0} Read permission on {1}!'.format(e, fpath))
        sys.exit(1)


def has_write(fpath):
    """Checks if the executing user has read access to the given path. Function will 
    return True if the executing user has read access to the path, the function will call 
    sys.exit(1) and give an error if False."""
    is_found(fpath)

    try:
        check_true(os.access(fpath, W_OK))
    except Exception as e:
        access_except('{0} Write permission on {1}!'.format(e, fpath))
        sys.exit(1)
