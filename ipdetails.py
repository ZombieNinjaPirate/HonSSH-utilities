#!/usr/bin/env python


"""Example using GeoLite2 database. """


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
__version__ = 'DEV-0.0.4'


import argparse
import datetime
import glob
import gzip
import os
import sys
import socket
import urllib
try:
    import geoip2.database
except ImportError, err:
    print '{0}'.format(err)
    print 'Resolution: sudo pip install geoip2'
    sys.exit(1)




def parse_args():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Get datailed data about a IP address')
    src = parser.add_argument_group('- Lookups')
    src.add_argument(
                    '-I', 
                    dest='ipadd',
                    help='One or more IP addresses separate by white space',
                    nargs='+',
                    type=str
                    )
    src.add_argument(
                    '-F',
                    dest='input',
                    help='File containing one IP address per line',
                    nargs='?',
                    type=argparse.FileType('r')
                    )

    mng = parser.add_argument_group('- Update')
    mng.add_argument(
                    '-U',
                    dest='update',
                    help='Downloads the loopup database from http://maxmind.com',
                    action='store_true'
                    )

    args = parser.parse_args()

    return args


def fetcmmdb():
    """Download the mmdb from Maxmind. """
    rfile = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
    lfile = '/tmp/GeoLite2-City.mmdb.gz'

    if os.geteuid() != 0:
        print 'PrivilegeError: You have to be root to update the database!'
        sys.exit(1)

    try:
        print 'Downloading database from http://maxmind.com now...'
        urllib.urlretrieve(rfile, lfile)
        print 'Database has been downloaded'
    except IOError, err:
        print '{0}'.format(err)
        sys.exit(1)

    return lfile


def extractgz(mmdbgz, mmdbp):
    """Extracts the CSV from the zip archive. """
    print 'Extracting database into /opt...'
    inngz = gzip.open(mmdbgz, 'rb')
    outgz = open(mmdbp, 'wb')
    outgz.write(inngz.read())
    inngz.close()
    outgz.close()
    print 'The database has been updated'


def dolookup(ipl, mmdb):
    reload(sys)
    sys.setdefaultencoding("utf-8")

    readipdb = geoip2.database.Reader(mmdb)

    geloc = {}
    loinfo = {}

    for ip in sorted(ipl):
        try:
            response = readipdb.city(ip.rstrip())

            geloc[ip] = { 
                        'ISO': response.country.iso_code, 
                        'CN': response.country.name,
                        'RGN': response.subdivisions.most_specific.name,
                        'CITY': response.city.name,
                        'ZIP': response.postal.code,
                        'LAT': response.location.latitude,
                        'LONG': response.location.longitude
                        }

            for ipadd, data in geloc.items():
                print 'IPv4 address:', ipadd
                if data['ISO']:
                    print '- {0:<12}{1}'.format('Code:', data['ISO'])

                if data['CN']:
                    print '- {0:<12}{1}'.format('Country:', data['CN'])

                if data['RGN']:
                    print '- {0:<12}{1}'.format('Region', data['RGN'])

                if data['CITY']:
                    print '- {0:<12}{1}'.format('City:', data['CITY'])

                if data['ZIP']:
                    print '- {0:<12}{1}'.format('Postal:', data['ZIP'])

                if data['LAT']:
                    print '- {0:<12}{1}'.format('Latitude:', data['LAT'])

                if data['LONG']:
                    print '- {0:<12}{1}'.format('Longitude:', data['LONG'])
                print ''
        except geoip2.errors.AddressNotFoundError, err:
            print err
            print ''


def check_args(args):
    mmdbp = '/opt/GeoLite2-City.mmdb'
    if args.ipadd:
        dolookup(args.ipadd, mmdbp)

    if args.input:
        dolookup(args.input, mmdbp)

    if args.update:
        dlgz = fetcmmdb()
        extractgz(dlgz, mmdbp)

    if not os.path.exists(mmdbp):
        print 'MissingDB: Unable to locate the IP lookup database'
        print 'Use the -U option to get the updated database from http://maxmind.com'
        sys.exit(1)


def main():
    """Main function. """
    args = parse_args()
    check_args(args)


if __name__ == '__main__':
    main()

