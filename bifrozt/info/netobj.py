"""The funcitons in this module can be for extracting and fiding information about various
network related objects. """


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
__date__ = '2015, Feb 20'
__version__ = '0.0.2'


import sys
try:
    import geoip2.database
except ImportError, err:
    print 'MissingModule: sudo pip install {0}'.format(str(err).split()[-1])
    sys.exit(1)


def geodata(ipstr, dbpath):
    """Attempts to find as much information about the ipstr in the local database from 
    Maxmind. The search will return a dirctionary object with the following properties:

    KEY: ipstr
        VALUES:
            ISO: a two letter country code
            CN: name of the country
            RGN: region specific name
            CITY: name of the city
            ZIP: postal code
            LAT: latitude
            LONG: longitude

    If the ipstr was not found (malformed address or rfc1918) the KEY will contain the
    returned error message and all values will be set to None.
    If one or more of the VAULES was not populated (not found), their will contain a value
    of None.
    """
    geloc = {}
    loinfo = {}
    reload(sys)
    sys.setdefaultencoding("utf-8")

    try:
        readipdb = geoip2.database.Reader(dbpath)
    except IOError, dberr:
        print '{0}'.format(dberr)
        sys.exit(1)

    try:
        response = readipdb.city(ipstr)
        geloc[ipstr] = { 
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

