"""This module is only used by the BZ_search script. """

"""
Copyright (c) 2014, Are Hansen - Honeypot Development

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
__version__ = '0.0.2'


import argparse
import sys
import time
from bifrozt.find.systemobj import locate_file
from bifrozt.IO.files import read_data, get_data, write_data
from bifrozt.find.stringobj import grep_nocase, grep_case
from bifrozt.validate.access import has_read, has_write, is_found


def parse_args():
    """Command line options for search script. """
    parser = argparse.ArgumentParser(description='''Search for the precense of a string in
                                     files.''')

    floc = parser.add_argument_group('- File location.')
    floc.add_argument('-D', dest='directory', help='''Path to directory in which the
                      file(s) exists.''', required=True, nargs=1, type=str)
    
    fname = parser.add_argument_group('- File name(s).')
    fname.add_argument('-F', dest='filenanme', help='Name or partial name of the file(s).', 
                       required=True, nargs=1, type=str)

    searchquery = parser.add_argument_group('- Search string.')
    query = searchquery.add_mutually_exclusive_group()
    query.add_argument('-SI', dest='ignore_case', help='String search. Ignore case',
                       nargs=1, type=str)
    query.add_argument('-SC', dest='follow_case', help='String search. Case sensitive.', 
                       nargs=1, type=str)

    output = parser.add_argument_group('- Output')
    output.add_argument('-W', dest='outpath', help='''Writes result to text file at the
                        given path.''', type=str)

    args = parser.parse_args()
        
    return args


def check_args(args):
    """Process the command line arguments. """
    if not args.ignore_case and not args.follow_case:
        print '[ERROR] - You MUST define either -FC or -IC'
        sys.exit(1)

    has_read(args.directory[0])

    if args.outpath:
        is_found(args.outpath)

    if args.ignore_case:
        if args.outpath:
            has_write(args.outpath)
            argt = args.directory[0], args.filenanme[0], args.ignore_case[0], args.outpath
        
        if not args.outpath:
            argt = args.directory[0], args.filenanme[0], args.ignore_case[0]

        search_nocase(argt)

    if args.follow_case:
        if args.outpath:
            has_write(args.outpath)
            argt = args.directory[0], args.filenanme[0], args.follow_case[0], args.outpath
        
        if not args.outpath:
            argt = args.directory[0], args.filenanme[0], args.follow_case[0]

        search_case(argt)


def search_nocase(argt):
    """Preforms a non-case sensitive search and prints the results to stdout. """
    if len(argt) == 3:
        finput = locate_file(argt[0], argt[1])
        dinput = read_data(finput)
        doutput = get_data(dinput)
        dsearch = grep_nocase(doutput, argt[2])

        for data in dsearch:
            print data

    if len(argt) == 4:
        fname = '{0}/{1}_Search.log'.format(argt[3], time.strftime("%Y%m%d_%H%M%S"))
        finput = locate_file(argt[0], argt[1])
        dinput = read_data(finput)
        doutput = get_data(dinput)
        dsearch = grep_nocase(doutput, argt[2])
        write_data(dsearch, fname)
        is_found(fname)


def search_case(argt):
    """Preforms a case sensitive search and prints the results to stdout. """
    if len(argt) == 3:
        finput = locate_file(argt[0], argt[1])
        dinput = read_data(finput)
        doutput = get_data(dinput)
        dsearch = grep_case(doutput, argt[2])

        for data in dsearch:
            print data

    if len(argt) == 4:
        fname = '{0}/{1}_Search.log'.format(argt[3], time.strftime("%Y%m%d_%H%M%S"))
        finput = locate_file(argt[0], argt[1])
        dinput = read_data(finput)
        doutput = get_data(dinput)
        dsearch = grep_case(doutput, argt[2])
        write_data(dsearch, fname)
        is_found(fname)