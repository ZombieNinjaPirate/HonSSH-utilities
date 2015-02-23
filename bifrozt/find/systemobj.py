"""The functions can be used to locate and interact with various system objects. """


"""
Copyright (c) 2015, Are Hansen - Honeypot Development

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
__date__ = '2014, Oct 11'
__version__ = '0.0.5'


import glob
import sys
import os
from os import R_OK, W_OK
from bifrozt.raising.exceptions import check_true, access_except


def findobj(fpath):
    """Verifies that the path exists. Will raise and exception and call sys.exit(1) 
    if False. """
    try:
        check_true(os.path.exists(fpath))
    except Exception as e:
        access_except('{0} {1} was not found!'.format(e, fpath))
        sys.exit(1)

    return fpath


def readobj(fpath):
    """Checks if the executing user has read access to the given path. Function will 
    return True if the executing user has read access to the path, the function will call 
    sys.exit(1) and give an error if False."""
    findobj(fpath)

    try:
        check_true(os.access(fpath, R_OK))
    except Exception as e:
        access_except('{0} Read permission on {1}!'.format(e, fpath))
        sys.exit(1)

    return fpath


def writeobj(fpath):
    """Checks if the executing user has read access to the given path. Function will 
    return True if the executing user has read access to the path, the function will call 
    sys.exit(1) and give an error if False."""
    findobj(fpath)

    try:
        check_true(os.access(fpath, W_OK))
    except Exception as e:
        access_except('{0} Write permission on {1}!'.format(e, fpath))
        sys.exit(1)

    return fpath


def fileobj(fpath, fname, wdir):
    """Looks for a file object on a system that corresponds with the fname within the
    fpath after changing directory to fpath. The fname can contain wildcard (*) to expand
    the file object name. Any file object matching the expanded fname will be appended to
    the flist. The function will then change back to the original working directory, the 
    flist will be returned only if it contains at least one file. If the flist contains
    zero files it will display an error message before stopping execution. """
    flist = []

    os.chdir(fpath)
    for files in glob.glob('{0}'.format(fname)):
        flist.append('{0}/{1}'.format(fpath, files))

    os.chdir(wdir)

    if len(flist) == 0:
        print '[NOTICE]: No log files found in {0}'.format(fpath)
        sys.exit(1)

    return flist

