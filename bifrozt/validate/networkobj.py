"""This module contain functions that can be used to validate different types of network related
objects such as MAC and IPv4 addresses. """


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
__date__ = '2014, Oct 11'
__version__ = '0.0.1'


import ipaddr
import re


def check_mac(macadd):
    """Check for valid MAC address. """
    while True:
        if not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macadd.lower()):
            print 'MAC address "{0}" is not valid!'.format(macadd)
            macadd = raw_input('- MAC: ')

        if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macadd.lower()):
            break

    return macadd


def check_ipv4(ipv4):
    """Checks for valid ipv4 addresses. """
    while True:
        try:
            ip = ipaddr.ip_address(ipv4)
            break
        except ValueError:
            print '[!] - IPv4 {0} is not valid!'.format(ipv4)
            ipv4 = raw_input('Enter a valid IPv4: ')

    return ipv4
