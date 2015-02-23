"""The functions can be used for running commands on a remote host using SSH. """

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


def pki_ssh_exec(rhost, ruser, cmd_list):
    """Connectcts as ruser on rhost, using public/private key authentication, while itterating over
    the cmd_list and executing the commands therein. This function will execute one command per 
    connection. The resulting output is stored in a dictionary were the commad is the key and the
    list object, containing the output of the executed commands, becomes the value. This dictionary
    is returned after the function completes its execution. """
    cmd_dict = {}

    for cmd in cmd_list:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(rhost, username=ruser)
        except paramiko.AuthenticationException:
            print('ERROR: Authentication as {0}@{1} failed.'.format(ruser, rhost))
            ssh.close()
            sys.exit(1)
        except socket.error:
            print('ERROR: Connection to {0} failed.'.format(rhost))
            ssh.close()
            sys.exit(1)

        stdin, stdout, stderr = ssh.exec_command(cmd)
        cmd_output = stdout.readlines()
        ssh.close()

        cmd_dict[cmd] = cmd_output

    return cmd_dict