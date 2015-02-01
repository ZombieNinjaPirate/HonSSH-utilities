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
__version__ = 'DEV-0.0.3'


import apt
import gzip
import logging
import os
import pip
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
         'modules/honssh': '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/lib/python2.7/dist-packages/honssh', 
         'modules/hpfeeds': '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/lib/python2.7/dist-packages/hpfeeds', 
         'modules/kippo': '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/lib/python2.7/dist-packages/kippo' 
         }

reqfil = {
         'conf/honssh.cfg': '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/honssh/honssh.cfg',
         'conf/honssh.tac': '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/honssh/honssh.tac', 
         'conf/users.cfg': '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/honssh/users.cfg', 
         'utils/honsshctrl.sh': '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/bin/honsshctrl', 
         'utils/honssh.sql': '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/honssh/honssh.sql', 
         'utils/playlog.py': '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/bin/playlog' 
         }

reqdst = [
         '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/lib/python2.7/dist-packages', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/usr/local/bin', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/honssh', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/bifrozt/ipdb', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/var/log/honssh', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/var/log/honssh/daily', 
         '/home/odin/Documents/PYTHON/BZ009/TESTING/var/log/honssh/application',
         '/home/odin/Documents/PYTHON/BZ009/TESTING/var/log/honssh/attackers' 
         ]


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


def checkdeps():
    reqdep = [ 'geoip2', 'MySQLdb', 'twisted' ]

    log.info('Checking for missing dependencies')

    for dep in reqdep:


def pip_install(py_pkg):
    """Check for missing Python dependencies and installs them if needed. """
    pfreeze = 'pip freeze'

    log.info('Lookung for {0}'.format(py_pkg))
    subp = subprocess.Popen(pfreeze, shell=True, stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)
    xit = subp.wait()

    if xit != 0:
        for err in subp.stderr:
            log.info('ERROR: {0}'.format(err))
        sys.exit(1)

    if xit == 0:
        for out in subp.stdout:
            if py_pkg in out:
                log.info('Dependency for {0} is met'.format(py_pkg))
            else:
                pinstall = 'pip install {0}'.format(py_pkg)
                log.info('Failed dependency for {0}. Installing {0} now'.format(py_pkg))
                subp = subprocess.Popen(pfreeze, shell=True, stdout=subprocess.PIPE, 
                                        stderr=subprocess.STDOUT)

                ixit = subp.wait()

                if ixit == 0:
                    log.info('Installation of {0}')

def apt_install(pkg_name):
    """Install package using apt-get. """
    pkg_name = 'python-mysqldb'
    cache = apt.cache.Cache()

    if cache.update():
        pkg = cache[pkg_name]

    if pkg.is_installed:
        print '{0} has already been installed on this system'.format(pkg_name)
    else:
        pkg.mark_install()


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
            # Set permissions on executables
            if fil.split('/')[-1][-3:] == '.py' or fil.split('/')[-1][-3:] == '.sh':
                log.info('Making {0} executable'.format(loc))


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

    mmdbp = '/home/odin/Documents/PYTHON/BZ009/TESTING/etc/bifrozt/ipdb/GeoLite2-City.mmdb'
    #mmbgz = fetcmmdb()
    #extractgz(mmbgz, mmdbp)


if __name__ == "__main__":
    main()

