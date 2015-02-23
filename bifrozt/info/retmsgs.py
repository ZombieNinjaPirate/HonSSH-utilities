"""The funcitons in this module can be for checking various states of various 
environmental objects. Depending on their states they will return a warning or error 
message to the user and halt any further execution. If the state of the checked obects 
dont generate warning or error messages, that object will be returned from the called 
function. """


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
__version__ = '0.0.1'


import os
import sys
from bifrozt.calc.timeobj import modage


def geodb(dbpath):
    """Check the age of the database, if the database was modified more than 30 days ago, 
    inform the user that it should be updated. """
    if not os.path.exists(dbpath):
        print 'DatabaseError: Unable to locate the IP lookup database'
        print 'Use the -U option to get the updated database from http://maxmind.com'
        sys.exit(1)

    mtime = modage(dbpath)

    if 'days' in str(mtime).split(',')[0]:
        
        nrday = int(str(mtime).split(',')[0].split()[0])

        if nrday > 29:
            print '\n=================================================================='
            print 'UpdateNotification: Maxmind updates the GeoLite database the first'
            print 'Thursday of the month. Update your database using -U'
            print '==================================================================\n'

    return dbpath
