"""Searches for network related objects. """


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


import geoip2.database
import sys
import re


def ipv4geo(ipv4_obj):
    """Given a IPv4 address the function will quesry the GeoLite2-City.mmdb database and
    return the ipv4_obj as a dictionary with as much info regarding its geo location as
    possible. """
    # Making sure we are using utf-8 as default encoding, eunicode can mess s**t up for us
    reload(sys)
    sys.setdefaultencoding("utf-8")
    readipdb = geoip2.database.Reader('/home/odin/Documents/PYTHON/BZ009/geoipdb/GeoLite2-City.mmdb')

    gelocd = {}
    gelocl = []

    for ipv4 in sorted(ipv4_obj):
        response = readipdb.city(ipv4)

        gelocd[ipv4] = { 
                        'ISO': response.country.iso_code, 
                        'CN': response.country.name,
                        'RGN': response.subdivisions.most_specific.name,
                        'CITY': response.city.name,
                        'ZIP': response.postal.code,
                        'LAT': response.location.latitude,
                        'LONG': response.location.longitude
                        }

        gelocl.append(gelocd)

    return gelocl


def ipv4match(ipv4_obj):
    """Checks the ipv4_obj, if the object is a string it will be converted to a list object.
    Itterate over the list elements and extract anything that matches the regex of a IPv4 address,
    if the extracted object is not present in the ipv4_list it will be appended to that list. The 
    ipv4_list is sorted and return as the ipv4_sort list. This function searche for an IPv4 address
    containig all four octets. """
    ipv4_list = []
    ipv4_sort = []

    if type(ipv4_obj) == str:
        ipv4_obj = ipv4_obj.split()

    for obj in ipv4_obj:
        #matches = re.findall(r"[\d,\w,\W,\S,\s](\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\w,\W,\S,\s,\n]", obj)
        #matches = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", obj)
        matches = re.match(r"[1-9]\d{1,2}\.\d{1,3}\.\d{1,3}\.\d{1,3}", obj)
        if matches:
            print matches
            if matches not in ipv4_list:
                ipv4_list.append(matches[0])

    for ipv4 in sorted(ipv4_list):
        ipv4_sort.append(ipv4)

    return ipv4_sort

