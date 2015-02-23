"""The functions can be used for basic SFTP actions. """

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
__date__ = '2014, Oct 18'
__version__ = '0.0.1'


import paramiko
import socket
import sys


def passwd_upload(rhost, rport, rusr, rpass, lfile, rfile):
    """This function expects to be given a user name (rusr) and password (rpass) thats valid on the 
    remote host (rhost) together with the port on which the SFTP server is running on (rport). It 
    will then upload a file from the local machine (lpath) to the remote machine, the destination
    on the remote machine has to be declared using the full path. The full path should also include
    the file name on the remote machine (rfile). The function will call sys.exit(1) on failure and
    return the name of the remote file upon sucsess. """
    try:
        transport = paramiko.Transport((rhost, rport))
        transport.connect(username=rusr, password=rpass)
    except socket.error, e:
        print 'ERR socket error:', e
        sys.exit(1)
    except paramiko.SSHException, e:
        print 'ERR paramiko exception:', e
        sys.exit(1)

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.put(lfile, rfile)
    except IOError, e:
        print 'ERR IOerror:', e
        sys.exit(1)

    sftp.close()
    transport.close()

    return rfile