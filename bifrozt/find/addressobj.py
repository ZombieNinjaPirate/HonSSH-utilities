"""The functions included in this module can be called to extract strings that matches 
some type of destinations adderss such as email, url and file shares like SMB and FTP. """


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


__author__ = 'Are Hansen'
__date__ = '2014, July 25'
__version__ = 'DEV-0.0.2'


import sys
import re


def email_match(email_obj):
    """Checks the email_obj, if the object is a string it will be converted to a list object.
    Itterate over the list elements and extract anything that matches the format of an email address
    and append that object to the email_list if its not present. The email_list is sorted and return
    returned as email_sort. """
    email_list = []
    email_sort = []

    if type(email_obj) == str:
        email_obj = email_obj.split()

    for obj in email_obj:
        matches = re.findall(r'[\w.-]+@[\w.-]+\.[\w.-]+', obj)
        if matches:
            if matches[0] not in email_list:
                user_list.append(matches[0])

    for user in sorted(user_list):
        print user


def url_match(url_obj):
    """Check the url_obj, if the object is a string it will be converted to a list object. Itterate
    over the list elements and extract anything that matches the format of any URL type and append
    that object to the url_list if not already present. The url_list is sorted and returned as
    url_sort. """
    url_list = []
    url_sort = []

    if type(url_obj) == str:
        url_obj = url_obj.split()

    for obj in url_obj:
        matches = re.findall(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))', obj)
        if matches:
            if matches[0] not in url_list:
                url_list.append(matches[0])

    for url in sorted(url_list):
        url_sort.append(url[0])
