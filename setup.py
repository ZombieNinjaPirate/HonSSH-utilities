#!/usr/bin/env python


"""Installs HonSSH, utilities and its dependencies. """


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
__date__ = '2015, Jan 17'
__version__ = 'DEV-0.0.4'


import gzip
import logging
import os
import shutil
import sys
import subprocess
import socket
import urllib
import time


log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(
    logging.Formatter('%(asctime)s %(module)s[%(process)d]: %(msg)s', datefmt="%b %d %T")
    )
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


# Path to the modules inside the HonSSH main 
reqdir = {
         'modules/honssh': '/usr/local/lib/python2.7/dist-packages/honssh', 
         'modules/hpfeeds': '/usr/local/lib/python2.7/dist-packages/hpfeeds', 
         'modules/kippo': '/usr/local/lib/python2.7/dist-packages/kippo' 
         }

reqfil = {
         'conf/honssh.cfg': '/etc/honssh/honssh.cfg',
         'conf/honssh.tac': '/etc/honssh/honssh.tac', 
         'conf/users.cfg': '/etc/honssh/users.cfg', 
         'utils/honsshctrl.sh': '/usr/local/bin/honsshctrl.sh', 
         'utils/honssh.sql': '/etc/honssh/honssh.sql', 
         'utils/playlog.py': '/usr/local/bin/playlog.py' 
         }

reqdst = [
         '/usr/local/lib/python2.7/dist-packages', 
         '/usr/local/bin', 
         '/etc/honssh', 
         '/etc/bifrozt/ipdb', 
         '/var/log/honssh', 
         '/var/log/honssh/daily', 
         '/var/log/honssh/application',
         '/var/log/honssh/attackers' 
         ]


reqdep = [ 'geoip2', 'MySQLdb', 'twisted' ]

reserr = [ 'sudo pip install geoip2', 'sudo apt-get install python-mysqldb', 
           'sudo pip install twisted' ]


def checkenv():
    log.info('Checking the installation environment...')
    for okdir in reqdir:
        if not os.path.isdir(okdir):
            log.info('DirError: {0} was not found!'.format(okdir))
            sys.exit(1)
        if os.path.isdir(okdir):
            log.info('DirOkay: {0}'.format(okdir))

    for okfil in reqfil:
        if not os.path.isfile(okfil):
            log.info('FileError: {0} was not found!'.format(okfil))
            sys.exit(1)
        if os.path.isfile(okfil):
            log.info('FileOkay: {0}'.format(okfil))

    for okdst in reqdst:
        if not os.path.isdir(okdst):
            os.makedirs(okdst)
            log.info('DstWarn: {0} was not found, created {0}'.format(okdst))
        if os.path.isdir(okdst):
            log.info('DstOkay: {0}'.format(okdst))

    log.info('Checking dependencies...')

    header = 35 * '='

    for dep in reqdep:
        try:
            __import__(dep)
            log.info('DependencyOkay: {0} is already installed'.format(dep))
        except ImportError, err:
            log.info('DependencyError: {0} does not exist'.format(dep))
            log.info('{0} DEPENDENCY ERROR {0}'.format(header))
            log.info('There are missing dependencies. Resolve them with these commands:')
            for res in reserr:
                log.info('{0}'.format(res))
            log.info('{0} DEPENDENCY ERROR {0}'.format(header))
            sys.exit(1)


def installmodules():
    log.info('Installing software components...')

    for mod,dst in reqdir.items():
        if not os.path.isdir(dst):
            log.info('Installing {0} in {1}'.format(mod.split('/')[-1], dst))
            shutil.copytree(mod, dst)
        elif os.path.isdir(dst):
            log.info('Replacing {0} with the latest version'.format(dst))
            shutil.rmtree(dst)
            shutil.copytree(mod, dst)

    for fil,loc in reqfil.items():
        if not os.path.isfile(loc):
            log.info('Installing {0} in {1}'.format(fil.split('/')[-1], loc))
            shutil.copyfile(fil, loc)
        elif os.path.isfile(loc):
            # Lets see if the existing file is a confgiration file
            if loc.split('/')[-1][-4:] == '.cfg':
                # If it is, create a backup before installing a clean one.
                log.info('Existing config file discovered: {0}'.format(loc))
                bktime = time.strftime('%y%m%d%H%M%S')
                bakfil = '{0}.{1}'.format(loc, bktime)
                log.info('Backup of {0} created as {1}'.format(loc, bakfil))
                os.rename(loc, bakfil)
                log.info('Installing new version of {0}'.format(loc))
                shutil.copyfile(fil, loc)


def fetcmmdb():
    """Download the mmdb from Maxmind. """
    rfile = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
    lfile = '/tmp/GeoLite2-City.mmdb.gz'

    if not os.path.isdir('/etc/bifrozt'):
        try:
            os.mkdir('/etc/bifrozt')
        except OSError, mkerr:
            log.info('{0}'.format(mkerr))
            sys.exit(1)

    try:
        log.info('Downloading GeoLite2 database from http://maxmind.com into /tmp')
        log.info('This might take up to a few minutes depending on your connection...')
        urllib.urlretrieve(rfile, lfile)
        log.info('Download of GeoLite2 database completed')
    except IOError, err:
        log.info('{0}'.format(err))
        sys.exit(1)

    return lfile


def extractgz(mmbgz, mmdbp):
    """Extracts the CSV from the zip archive. """
    if os.path.isfile(mmdbp):
        log.info('An older version of {0} exists'.format(mmdbp))
        log.info('Removing {0} now'.format(mmdbp))
        os.remove(mmdbp)
        log.info('{0} was removed'.format(mmdbp))

    log.info('Extracting latest version of GeoLite2 database to {0}'.format(mmdbp))

    inngz = gzip.open(mmbgz, 'rb')
    outgz = open(mmdbp, 'wb')
    outgz.write(inngz.read())
    inngz.close()
    outgz.close()
    log.info('The latest version of GeoLite2 database has been installed'.format(mmdbp))


def main():
    """Main...doing main stuff. """
    checkenv()
    installmodules()

    mmdbp = '/etc/bifrozt/ipdb/GeoLite2-City.mmdb'
    mmbgz = fetcmmdb()
    extractgz(mmbgz, mmdbp)


if __name__ == "__main__":
    main()

