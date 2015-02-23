"""The functions can be used for locating strings. """


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
__date__ = '2014, Oct 18'
__version__ = '0.0.1'


import re


def pgrepnc(dlist, strobj):
    """Works in a similar way as the UNIX grep tool. It will itterate over the dlist
    looking for anything matching the strobj"""
    slist = []

    search_str = r"\b(?=\w){0}\b(?!\w)".format(re.escape(strobj))

    for data in dlist:
        if re.search(search_str, data, re.IGNORECASE):
            slist.append(data)

    return sorted(slist)


def grep_case(dlist, strobj):
    """Works in a similar was as the UNIX grep tool. It will inspect every data object in the dlist 
    looking for the string pattern. If the inspected data contains the requested sting pattern it 
    will be appended to the slist and retunned from the function. """
    slist = []

    search_str = r"\b(?=\w){0}\b(?!\w)".format(re.escape(strobj))

    for data in dlist:
        if re.search(search_str, data):
            slist.append(data)

    return sorted(slist)
