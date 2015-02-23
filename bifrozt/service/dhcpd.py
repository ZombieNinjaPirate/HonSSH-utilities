"""This module contain functions that can be used for management of the Bifrozt DHCPD server. """


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
__date__ = '2014, Oct 12'
__version__ = '0.0.1'


import ipaddress
import sys


def dhcpd_info():
   """Prints the DHCPD header information. """
   print(''' 
         Bifrozt DHCPD server configuration
    ============================================

    Before you begin, make sure you have:
    - network name              - network CIDR
    - network range             - domain name
    - honeypot MAC address      - honeypot IPv4 

    The IPv4 addresses must be in compliance with 
    RFC 1918. That means the network must be 
    within one of the following IPv4 blocks:

                10.0.0.0/8
                172.16.0.0/16
                192.168.0.0/16
   ''')


def dhcpd_network():
    """Gets the network address from the user. """
    while True:
        print('Enter the network name for your IPv4 network.')
        Network = input('Network: ')

        rfc_10 = '10.{0}'.format(Network.split('.')[1])

        rfc1918_list = [ rfc_10, '192.168', '172.16' ]

        try:
            str(ipaddress.IPv4Address(Network))
        except ipaddress.AddressValueError:
            print('ERROR: {0} dont appear to be a valid IPv4 address!'.format(Network))
            print('Enter the network name for your IPv4 network.')
            Network = input('Network: ')     

        if '.'.join(Network.split('.')[0:2]) not in rfc1918_list:
            print('ERROR: {0} dont appear to be a valid RFC 1918 address!'.format(Network))
            print('Enter the network name for your IPv4 network.')
            Network = input('Network: ')     

        break

    return Network


def dhcpd_netmask(ipnet):
    """When given a network address as an arguemnt and a CIDR from the user, this function
    will then process the information and return:

    - Network address
    - Default gateway
    - First IPv4 address in the network
    - Last IPv4 address in the network
    - The broaccast address of the network
    - The subnet mask of the network
    - CIDR

    This is returned as a list object. """
    while True:
        print('Enter the CIDR of your IPv4 network.')
        CIDR = input('CIDR: ')

        try:
            net4 = ipaddress.IPv4Interface('{0}/{1}'.format(ipnet, CIDR))
            sbnet = str(net4.netmask)
        except ipaddress.NetmaskValueError:
            print('ERROR: {0} dont appear to be a valid CIDR!'.format(CIDR))
            print('Enter the CIDR of your IPv4 network.')
            CIDR = input('CIDR: ')

        break

    bcast = str(ipaddress.IPv4Network('{0}/{1}'.format(ipnet, CIDR), strict=False).broadcast_address)
    fipv4 = str(list(ipaddress.IPv4Network('{0}/{1}'.format(ipnet, CIDR), strict=False).hosts())[1])
    lipv4 = str(list(ipaddress.IPv4Network('{0}/{1}'.format(ipnet, CIDR), strict=False).hosts())[-1])
    defgw = str(list(ipaddress.IPv4Network('{0}/{1}'.format(ipnet, CIDR), strict=False).hosts())[0])

    # network_list: network, defaultgateway, firstIPv4, lastIPv4, broadcast, subnetmask, CIDR 
    dhcpd_obj = [ ipnet, defgw, fipv4, lipv4, bcast, sbnet ]

    return dhcpd_obj


def dhcpd_dns(dhcpd_obj_list):
    """Get the domain name servers and domain name. """
    # Holds the DNS server(s).
    dns_list = []

    while True:
        validation = ''

        print('Enter the DNS servers for your network (space separated).')
        dnssrvs = input('DNS server(s): ')
        dns_test = dnssrvs.split(' ')
        
        print('DEBUG:', dns_list)
        
        # Itterate over the DNS servers
        for dns in dns_test:
            try:
                # If the DNS server address(es) are valid
                str(ipaddress.IPv4Address(dns))
                # append them to the dns_list.
                print('DEBUG: verified DNS', dns)
                dns_list.append(dns)
            except ipaddress.AddressValueError:
                # Print an error if any of the DNS server address(es) fails the check
                print('ERROR: {0} dont appear to be a valid IPv4 address!'.format(dns))
                # and reset the dns_list
                dns_test = []
                dns_list = []

            if len(dns_list) == len(dns_test):
                validation = 'checked'
        
        if validation == 'checked':
            break

    print(dns_list)
    # Append the dns_list to the dhcpd_obj_list

def dhcpd_static(dhcpd_obj_list):
    """Get MAC address and IP address of the honeypot and append them to the dhcpd_obj_list. Get the
    user to define a dhcp range. Check for confilcts with the dhcp range and the static IPv4 hosts.
    Append the new values to the dhcpd_obj_list and return the updated list from the function. """
    print('INACTIVE: Honeypot MAC and IPv4 address')


def dhcpd_conf(datal):
    """Use the elements in the datal to generate the declarations for the final dhcpd.conf 
    file. All the declarations are appended to the dhcpd_file list and returned from the function. 
    """
    dhcpd_file = []

    dhcpd_file.append('authoritative;')
    dhcpd_file.append('ddns-update-style none;')
    dhcpd_file.append('log-facility local7;')
    dhcpd_file.append('default-lease-time 600;')
    dhcpd_file.append('max-lease-time 7200;')
    dhcpd_file.append(' ')
    dhcpd_file.append('subnet {0} netmask {1} {2}'.format(datal[0], datal[5], '{'))
    dhcpd_file.append('    option domain-name "{0}";'.format('DOMAIN_NAME'))
    dhcpd_file.append('    option domain-name-servers {0};'.format('DNS_SERVERS'))
    dhcpd_file.append('    option subnet-mask {0};'.format(datal[5]))
    dhcpd_file.append('    option broadcast-address {0};'.format(datal[1]))
    dhcpd_file.append('    option routers {0};'.format(datal[4]))
    dhcpd_file.append('    range {0} {1};'.format(datal[2], datal[3]))
    dhcpd_file.append(' ')
    dhcpd_file.append('    host {0}.{1} {2}'.format('HOSTNAME', 'DOMAIN_NAME', '{'))
    dhcpd_file.append('        hardware ethernet {0};'.format('MAC_ADDRESS'))
    dhcpd_file.append('        fixed-address {0};'.format('STATIC_IP_ADDRESS'))
    dhcpd_file.append('    {0}'.format('}'))
    dhcpd_file.append('{0}'.format('}'))

    return dhcpd_file
