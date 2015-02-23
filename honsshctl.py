#!/usr/bin/env python


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

#
#   All the honssh utilities will read a configuration file in /etc/honssh/.utils.cfg
#   The configuration file contains
#   - path to honssh.cfg
#


__author__ = 'Are Hansen'
__date__ = '2015, Jan 17'
__version__ = 'DEV-0.0.2'


import argparse
import os
import sys
import subprocess
from bifrozt.calc.timeobj import modage
from bifrozt.functions import std


def parse_args():
    """Defines the command line arguments. """
    parser = argparse.ArgumentParser('Manage HonSSH and its environment')

    pctrl = parser.add_argument_group('Process control')
    pctrl.add_argument(
                      '-P', 
                      dest='pctrl', 
                      help='Manage the HonSSH process', 
                      choices=['kill', 'restart', 'start', 'status', 'stop']
                      )

    args = parser.parse_args()

    return args


def honssh_status(ppath):
    """Prints a short summary about the HonSSH status. """
    currpid = showpid(ppath)
    gettime = modage(ppath)

    print '\n   HonSSH status'
    print '==================='
    print 'Process ID:\t{0}'.format(currpid)
    print 'Run time:\t{0}\n'.format(gettime)


def showpid(ppath):
    """If honssh pid file is found it returns the pid from that file, if the pid file
    dont exist it will throw an error and halt execution."""
    pfile = []

    if os.path.isfile(ppath):
        with open(ppath, 'r') as lines:
            for line in lines.readlines():
                pfile.append(line)

    if not os.path.isfile(ppath):
        std.log.info('Unable to find {0}'.format(ppath))
        sys.exit(1)

    return pfile[0]


def stop_honssh():
    """Stop HonSSH. """
    currpid = showpid(hon_pid)
    SIGTERM = 'kill -15 {0}'.format(currpid)

    std.log.info('HonSSH is running with pid {0}. SIGTERM sent to {0}'.format(currpid))    
    subp = subprocess.Popen(SIGTERM, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    std.log.info('Waiting for return code of SIGTERM...')
    xcode = subp.wait()

    if xcode == 0:
        std.log.info('SIGTERM on {0} returned {1}'.format(currpid, xcode))

        if not os.path.isfile(hon_pid):
            std.log.info('{0} was cleanly removed'.format(hon_pid))

    if xcode != 0:
        std.log.info('SIGTERM was refused by {0}'.format(currpid))
        sys.exit(1)


def start_honssh():
    """Starting HonSSH."""
    if os.path.isfile(hon_pid):
       std.log.info(' - FAIL - pid file already exists ({0})'.format(hon_pid))
       sys.exit(0)

    # Changing to /opt/honssh
    os.chdir(app_dir)
    #
    #   Building HonSSH as a python package would install it in PYPATH and would resolve
    #   the issues with PATH.
    #
    ini = 'twistd -y {0} -l {1} --pidfile {2}'.format(hon_tac, hon_log, hon_pid)
    std.log.info('Initializing HonSSH and requesting the system to assign us a pid')
    subp = subprocess.Popen(ini, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    std.log.info('Received pid from the system, waiting for startup to complete...')
    xcode = subp.wait()
    
    if xcode == 0:
        std.log.info('HonSSH has completed startup and is running with pid {0}'.format(showpid(hon_pid)))

    if xcode != 0:
        std.log.info('HonSSH failed to start. Exit code {0}'.format(xcode))
        sys.exit(0)


def process_args(args):
    """Process the command line arguments."""
    if args.pctrl == 'restart':
        stop_honssh()
        sleep(3)
        start_honssh()

    if args.pctrl == 'start':
        start_honssh()

    if args.pctrl == 'stop':
        stop_honssh()

    if args.pctrl == 'status':
        #print 'NOT IMPLMENTED YET'
        honssh_status('/var/run/honssh.pid')
        #
        #   If pid file exists
        #   - show the current pid
        #   - show time pid was created
        #   - show how long the process has been running

    if args.pctrl == 'kill':
        print 'NOT IMPLMENTED YET'
        #
        #   The kill function will ba called from stop_honssh in the event of SIGTERM (15)
        #   returning non-zero exit. kill_honssh will then
        #   issue a second SIGTERM
        #       if SIGTERM fails again: 
        #           issue SIGHUP (1) and remove pid file on exit 0
        #           if SIGHUP fails:
        #               issue SIGKILL (9) and remove pid file on exit 0
        #                   if SIGKILL returns non-zero:
        #                       wait 2 seconds
        #                       retry SIGKILL for a maximum of 10 times

    if args.pctrl == 'status':
        print 'NOT IMPLMENTED YET'



def main():
    """Main function of bifrozt_stats. """
    #
    #   This will be moved to a separate function that modifies the environment to addheres
    #   with a more common Linux system layout.
    #
    """
    if not os.path.isdir(app_dir):
        std.log.info('{0} does not exist. Creating directory structure now...'.format(log_dir))
        os.makedirs('{0}/HonSSH/application'.format(log_dir))
        std.log.info('Created directory: {0}/HonSSH/application'.format(log_dir))
        os.makedirs('{0}/HonSSH/daily'.format(log_dir))
        std.log.info('Created directory: {0}/HonSSH/daily'.format(log_dir))
        os.makedirs('{0}/HonSSH/sessions'.format(log_dir))
        std.log.info('Created directory: {0}/HonSSH/sessions'.format(log_dir))
        os.makedirs('{0}/HonSSH/utilities'.format(log_dir))
        std.log.info('Created directory: {0}/HonSSH/utilities'.format(log_dir))
    """
    args = parse_args()
    process_args(args)


if __name__ == '__main__':
    app_dir = '/etc/honssh'
    log_dir = '/var/log/honssh'
    hon_pid = '/var/run/honssh.pid'
    hon_tac = '{0}/honssh.tac'.format(app_dir)
    hon_log = '{0}/application/honssh.log'.format(log_dir)
    main()
