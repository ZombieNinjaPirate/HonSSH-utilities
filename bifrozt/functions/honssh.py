"""All of these functions are used to interact with the HonSSH process and the data it 
collects. """


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
__date__ = '2014, Dec 9'
__version__ = '0.0.7'


import os
import re
import sys
import operator
from bifrozt.IO.files import readfile, getdata
from bifrozt.info.netobj import geodata
from bifrozt.objects.lists import element


def daylog(dlist):
    """Expects the dlist to consist of data from HonSSH daily logs. It will extract all
    lines where the attacker has completed the authentication process. The entire line
    will be converted from a string to a tuple. This tuple is appended to the authlist and
    returned from the function.

                        Contents of the authlist

    Date/time stamp         authlist[0][0]      2015-01-17 00:07:39
    Country code            authlist[0][1]      KR
    IPv4 address            authlist[0][2]      123.45.67.89
    Username                authlist[0][3]      root
    Password                authlist[0][4]      P@ssw0rD
    Success code            authlist[0][5]      0,1
    """
    authlist = []

    for data in dlist:
        lenlog = data.split(',')

        if len(lenlog) > 3:
            patrn = r'^([^,]*),([^,]*),([^,]*),([^,]*),(.*),(\d+)\s*$'
            strng = str(data)
            match = re.match(patrn, strng)
            authlist.append(match.groups())
    
    return authlist


def bzha(hlog, nline):
    """Show who got access, what time, from what country, which IPv4 and using what 
    credentials. """
    gotroot = []

    for data in hlog:
        if len(data) == 6 and data[-1] == '1':
            gotroot.append('{0} {1} {2} {3}/{4}'.format(data[0], data[2], data[1], data[3], data[4]))

    if len(gotroot) == 0:
        print 'No valid login has been found yet'
        sys.exit(1)

    print '       Date       Time       Source      Origin   Login'
    print '================================================================='

    for got in sorted(gotroot[:nline]):
        got = got.split()
        print '{0:>14}  {1}  {2:<15}  {3}   {4}'.format(got[0], got[1], got[2], got[3], got[4])


def bzhc(hlog, nline):
    """Decending list of the most fequently used combinations. """
    combina = []

    for data in hlog:
        if len(data) == 6:
            combina.append('{0}/{1}'.format(data[3], data[4]))

    topcombo = element(combina)

    if len(topcombo) == 0:
        print 'No login attempts registered so far.'
        sys.exit(1)

    print '  Attempts  Combinations'
    print ' =========  ======================'

    for top in topcombo[:nline]:
        print '{0:>10}{1:>2}{2}'.format(top[1], '', top[0])


def bzho(hlog, nline):
    """Decending list of connections per country. """
    mmdbp = '/etc/GeoIPdb/GeoLite2-City.mmdb'
    olist = []

    for data in hlog:
            olist.append(data[1])

    origin = element(olist)

    print '  Attempts  Country of origin'
    print ' =========  ======================'

    for org in origin[:nline]:
        print '{0:>10}{1:>2}{2}'.format(org[1], '', org[0])


def bzhp(hlog, nline):
    """Decending list of used passwords. """
    plist = []

    for data in hlog:
            plist.append(data[4])

    passwd = element(plist)

    print '  Attempts  Password'
    print ' =========  ======================'

    for pwd in passwd[:nline]:
        print '{0:>10}{1:>2}{2}'.format(pwd[1], '', pwd[0])


def bzhs(hlog, nline):
    """Decending list of attacks per source IPv4 address. """
    slist = []

    for data in hlog:
        ndata = '{0} {1}'.format(data[2], data[1])
        slist.append(ndata)

    source = element(slist)

    print '  Attempts  Source           Origin country'
    print ' =========  ===============  ================='

    for src in source[:nline]:
        src1 = src[0].split(' ')[0]
        src2 = src[0].split(' ')[1]
        print '{0:>10}  {1:<16} {2}'.format(src[1], src1, src2)


def bzhu(hlog, nline):
    """Decending list of tried user names. """
    ulist = []

    for data in hlog:
            ulist.append(data[3])

    users = element(ulist)

    print '  Attempts  User name'
    print ' =========  ======================'

    for usr in users[:nline]:
        print '{0:>10}{1:>2}{2}'.format(usr[1], '', usr[0])
