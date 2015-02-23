#!/usr/bin/env python


"""Extract data from various logs on Bifrozt. """


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
__date__ = '2014, May 15'
__version__ = '0.2.0'


import argparse
import os
import sys
from bifrozt.functions.honssh import bzha, bzhc, bzho, bzhp, bzhs, bzhu, daylog
from bifrozt.find.systemobj import readobj, fileobj
from bifrozt.IO.files import readfile, getdata


def parse_args():
    """Defines the command line arguments. """
    parser = argparse.ArgumentParser('Extract data from various logs on Bifrozt:')

    xtract = parser.add_argument_group('Log data options')
    data = xtract.add_mutually_exclusive_group(required=True)
    data.add_argument('-HA', 
                        dest='access', 
                        help='Valid login found', 
                        action='store_true'
                        )
    data.add_argument('-HC', 
                        dest='combos', 
                        help='Frequent combinations', 
                        action='store_true'
                        )
    data.add_argument('-HM', 
                        dest='malwre', 
                        help='Data about the captured malware', 
                        action='store_true'
                        )
    data.add_argument('-HO', 
                        dest='origin', 
                        help='Number of attacks/country', 
                        action='store_true'
                        )
    data.add_argument('-HP', 
                        dest='passwd', 
                        help='Most used passwords', 
                        action='store_true'
                        )
    data.add_argument('-HS', 
                        dest='source',
                        help='Connection/IP address', 
                        action='store_true'
                        )
    data.add_argument('-HU', 
                        dest='usrnam', 
                        help='Most tested user names', 
                        action='store_true'
                        )

    logd = parser.add_argument_group('Directories containing data')
    logs = logd.add_mutually_exclusive_group()
    logs.add_argument('-HL', 
                        dest='hondir', 
                        help='HonSSH log directory (default: /opt/honssh/logs)', 
                        default='/opt/honssh/logs',                        
                        nargs=1
                        )

    out = parser.add_argument_group('Output options')
    out.add_argument('-n', 
                        dest='number', 
                        help='Number of lines displayed (default: 50)',
                        type=int,
                        default=50
                        )
    out.add_argument('-o',
                        dest='file',
                        help='Output file',
                        type=argparse.FileType('w')
                        )

    args = parser.parse_args()

    return args


def process_args(args):
    """Process the command line arguments."""
    if args.access:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzha(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.combos:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzhc(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.origin:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzho(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.passwd:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzhp(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.source:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzhs(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.usrnam:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        bzhu(daylog(readfile(fileobj(args.hondir, '20*', os.getcwd()))), args.number)

    if args.malwre:
        if type(args.hondir) is list:
            args.hondir = args.hondir[0]
        readobj(args.hondir)
        for line in readfile(fileobj(args.hondir, 'download*', os.getcwd())):
            line = line.split(',')
            print 'Date:', line[0]
            print 'Attacker:', line[1]
            print 'Server:', line[2]
            print 'Size:', line[3]
            print 'MD5:', line[4]
            print 'Local:', line[5]
            print ''

def main():
    """Main function of bifrozt_stats. """
    args = parse_args()
    process_args(args)


if __name__ == '__main__':
    main()