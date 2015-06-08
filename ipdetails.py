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
__version__ = '0.0.6'


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


def fetcmmdb(mmdbp):
    """Download the mmdb from Maxmind. """
    rfile = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
    lfile = '/tmp/GeoLite2-City.mmdb.gz'
    dbdri = '/'.join(mmdbp.split('/')[:-1])

    if not os.path.isdir(dbdri):
        try:
            os.mkdir(dbdri)
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
    dbdri = '/'.join(mmdbp.split('/')[:-1])
    print 'Extracting database into {0}...'.format(dbdri)

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
        print 'DatabaseError: Unable to locate the IP lookup database'
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



def checkip(ipl, mmdb):
    """Itterate over the list of ip addresses and print what ever details we found in the 
    database. """
    for ip in sorted(ipl):

        ipdict = dolookup(ip.rstrip(), mmdb)

        for ipadd, data in ipdict.items():
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


def dolookup(ip, mmdb):
    """The function receives a string object that should be in the form of a IP addresses, 
    looks it up in the Maxmind database and returns the result as a dictionary. """
    geloc = {}
    loinfo = {}
    reload(sys)
    sys.setdefaultencoding("utf-8")
    readipdb = geoip2.database.Reader(mmdb)

    try:
        response = readipdb.city(ip)
        geloc[ip] = { 
                    'ISO': response.country.iso_code, 
                    'CN': response.country.name,
                    'RGN': response.subdivisions.most_specific.name,
                    'CITY': response.city.name,
                    'ZIP': response.postal.code,
                    'LAT': response.location.latitude,
                    'LONG': response.location.longitude
                    }
    except geoip2.errors.AddressNotFoundError, err:
        geloc[err] = {
                    'ISO': None, 
                    'CN': None,
                    'RGN': None,
                    'CITY': None,
                    'ZIP': None,
                    'LAT': None,
                    'LONG': None
                    }
    except ValueError, err:
        geloc[err] = {
                    'ISO': None, 
                    'CN': None,
                    'RGN': None,
                    'CITY': None,
                    'ZIP': None,
                    'LAT': None,
                    'LONG': None
                    }

    return geloc


def check_args(args):
    """Runs some basic environment checks before parsing the arguments."""        
    mmdbp = '/etc/GeoIPdb/GeoLite2-City.mmdb'
    scrpt = sys.argv[0].split('/')[-1]

    if len(sys.argv) == 1:
        print 'Usage: {0} -h'.format(scrpt)
        sys.exit(1)
    
    if args.ipadd:
        checkdb(mmdbp)
        checkip(args.ipadd, mmdbp)

    if args.input:
        checkdb(mmdbp)
        checkip(args.input, mmdbp)

    if args.update:
        dlgz = fetcmmdb(mmdbp)
        extractgz(dlgz, mmdbp)


def main():
    """Main function. """
    args = parse_args()
    check_args(args)


if __name__ == '__main__':
    main()

