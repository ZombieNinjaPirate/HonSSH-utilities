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
__version__ = 'DEV-0.0.5'


try:
    import argparse
    import datetime
    import glob
    import gzip
    import os
    import sys
    import socket
    import urllib
    import geoip2.database
except ImportError, err:
    print 'MissingModule: sudo pip install {0}'.format(str(err).split()[-1])
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
                    help='Update database from http://maxmind.com (run as root)',
                    action='store_true'
                    )

    args = parser.parse_args()

    return args


def fetcmmdb(mmdbp):
    """Download the mmdb from Maxmind. """
    rfile = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
    lfile = '/tmp/GeoLite2-City.mmdb.gz'

    if not os.path.isdir('/etc/bifrozt'):
        try:
            os.mkdir('/etc/bifrozt')
        except OSError, mkerr:
            print '{0}'.format(mkerr)
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

    if os.geteuid() != 0:
        print 'PrivilegeError: You have to be root to update the database!'
        sys.exit(1)

    inngz = gzip.open(mmdbgz, 'rb')
    outgz = open(mmdbp, 'wb')
    outgz.write(inngz.read())
    inngz.close()
    outgz.close()
    print 'The database in {0} has been updated'.format(mmdbp)


def checkdb(mmdbp):
    """Check the age of the database, if the database was modified more than 30 days ago, 
    inform the user that it should be updated. """
    if not os.path.exists(mmdbp):
        print 'MissingDB: Unable to locate the IP lookup database'
        print 'Use the -U option to get the updated database from http://maxmind.com'
        sys.exit(1)

    moddb = datetime.datetime.fromtimestamp(os.path.getmtime(mmdbp))
    today = datetime.datetime.now()
    mtime = today - moddb

    if 'days' in str(mtime).split(',')[0]:
        nrday = int(str(mtime).split(',')[0].split()[0])

        if nrday > 29:
            print '\n=================================================================='
            print 'UpdateNotification: Maxmind updates the GeoLite database the first'
            print 'Thursday of the month. Update your database using -U'
            print '==================================================================\n'


def dolookup(ipl, mmdb):
    """The function receives a list object containing one or more IP addresses, looks 
    them up in the Maxmind database and outputs the results. """
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
                print 'IPv4 address: {0}'.format(ipadd).rstrip()

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
        except geoip2.errors.AddressNotFoundError, err:
            print err
            print ''


def check_args(args):
    """Runs some basic environment checks before parsing the arguments."""        
    mmdbp = '/etc/bifrozt/GeoLite2-City.mmdb'
    scrpt = sys.argv[0].split('/')[-1]

    if len(sys.argv) == 1:
        print 'Usage: {0} -h'.format(scrpt)
        sys.exit(1)
    
    if args.ipadd:
        checkdb(mmdbp)
        dolookup(args.ipadd, mmdbp)

    if args.input:
        checkdb(mmdbp)
        dolookup(args.input, mmdbp)

    if args.update:
        dlgz = fetcmmdb(mmdbp)
        extractgz(dlgz, mmdbp)


def main():
    """Main function. """
    args = parse_args()
    check_args(args)


if __name__ == '__main__':
    main()

