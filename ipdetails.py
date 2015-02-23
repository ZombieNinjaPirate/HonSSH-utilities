#!/usr/bin/env python


"""Uses Maxminds database to gather detailed infomation about a IP address. """


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
__date__ = '2015, Jan 17'
__version__ = '0.0.9'


import argparse
import os
import sys
from bifrozt.IO.archives import xtrctgz
from bifrozt.info.netobj import geodata
from bifrozt.info.retmsgs import geodb
from bifrozt.network.DL import dlwww


def parse_args():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Get datailed data about a IP address')
    src = parser.add_argument_group('- Lookups')
    src.add_argument(
                    '-i', 
                    dest='ipadd',
                    help='One or more IP addresses separate by white space',
                    nargs='+',
                    type=str
                    )
    src.add_argument(
                    '-f',
                    dest='input',
                    help='File containing one IP address per line',
                    nargs='?',
                    type=argparse.FileType('r')
                    )
    mng = parser.add_argument_group('- Update')
    mng.add_argument(
                    '-U',
                    dest='update',
                    help='Update database from http://maxmind.com (run as root)',
                    action='store_true'
                    )

    args = parser.parse_args()

    return args


def checkip(ipl, mmdb):
    """Itterate over the list of ip addresses and print what ever details we found in the 
    database. """
    for ip in sorted(ipl):

        ipdict = geodata(ip.rstrip(), mmdb)

        for ipadd, data in ipdict.items():
            print '{0:<12}{1}'.format('Source:', ipadd).rstrip()

            if data['ISO']:
                print '{0:<12}{1}'.format('Code:', data['ISO'])
            
            if data['CN']:
                print '{0:<12}{1}'.format('Country:', data['CN'])
            
            if data['RGN']:
                print '{0:<12}{1}'.format('Region', data['RGN'])
            
            if data['CITY']:
                print '{0:<12}{1}'.format('City:', data['CITY'])
            
            if data['ZIP']:
                print '{0:<12}{1}'.format('Postal:', data['ZIP'])
            
            if data['LAT']:
                print '{0:<12}{1}'.format('Latitude:', data['LAT'])
            
            if data['LONG']:
                print '{0:<12}{1}'.format('Longitude:', data['LONG'])
            
            print ''


def check_args(args):
    """Runs some basic environment checks before parsing the arguments."""        
    mmdbp = '/etc/GeoIPdb/GeoLite2-City.mmdb'
    scrpt = sys.argv[0].split('/')[-1]

    if len(sys.argv) == 1:
        print 'Usage: {0} -h'.format(scrpt)
        sys.exit(1)

    if args.ipadd:
        mmdbp = geodb(mmdbp)
        checkip(args.ipadd, mmdbp)

    if args.input:
        mmdbp = geodb(mmdbp)
        checkip(args.input, mmdbp)

    if args.update:
        if os.geteuid() != 0:
            print 'PrivilegeError: You have to be root to update the database!'
            sys.exit(1)

        rfgz = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
        lfgz = '/tmp/GeoLite2-City.mmdb.gz'

        print 'Downloading database from maxmind.com, this might take a while...'
        dlgz = dlwww(rfgz, lfgz)

        dbdri = '/'.join(mmdbp.split('/')[:-1])
        print 'Extracting database into {0}...'.format(dbdri)

        xtrctgz(dlgz, mmdbp)


def main():
    """Main function. """
    args = parse_args()
    check_args(args)


if __name__ == '__main__':
    main()


