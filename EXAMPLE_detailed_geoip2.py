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
__version__ = 'DEV-0.0.3'

import sys
import geoip2.database


def main():
    ipl = sys.argv[1:]

    reload(sys)
    sys.setdefaultencoding("utf-8")

    readipdb = geoip2.database.Reader('/PATH/TO/YOUR/GeoLite2-City.mmdb')

    geloc = {}
    loinfo = {}

    for ip in sorted(ipl):
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

if __name__ == "__main__":
    main()
