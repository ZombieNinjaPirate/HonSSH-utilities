#!/usr/bin/env python


"""Installs HonSSH, utilities and its dependencies. """


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
__date__ = '2015, Jan 17'
__version__ = '0.0.2'


import logging
import os
import shutil
import sys
import time


log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(
    logging.Formatter('%(asctime)s %(module)s[%(process)d]: %(msg)s', datefmt="%b %d %T")
    )
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


def checkenv():
    """Check the environment for missing modules and structures. Creates missing
    structures, calls sys.sexit(1) on missing modules. """
    logdir = '/var/log/honssh'
    daydir = '{0}/daily'.format(logdir)
    attdir = '{0}/attack'.format(logdir)
    appdir = '{0}/application'.format(logdir)

    if not os.path.isdir('kippo'):
        log.info('ModuleError: kippo')
        sys.exit(1)

    if not os.path.isdir('honssh'):
        log.info('ModuleError: honssh')
        sys.exit(1)

    if not os.path.isdir('hpfeeds'):
        log.info('ModuleError: hpfeeds')
        sys.exit(1)

    if not os.path.isdir(logdir):
        os.mkdir(logdir)
        log.info('Created directory: {0}'.format(logdir))

    if not os.path.isdir(attdir):
        os.mkdir(attdir)
        log.info('Created directory: {0}'.format(attdir))

    if not os.path.isdir(appdir):
        os.mkdir(appdir)
        log.info('Created directory: {0}'.format(appdir))

    if not os.path.isdir(daydir):
        os.mkdir(daydir)
        log.info('Created directory: {0}'.format(daydir))


def installmodules():
    """Checks the current environment and create directories as needed. We will assume
    that any existing modules here are outdated and that the user is applying a newer
    version thus, any existing modules will be delete and replaced. """
    moddir = '/usr/local/lib/python2.7/dist-packages'

    if os.path.isdir('{0}/{1}'.format(moddir, 'kippo')):
        log.info('Replacing {0}/{1} with the latest version'.format(moddir, 'kippo'))
        shutil.rmtree('{0}/{1}'.format(moddir, 'kippo'))
        shutil.copytree ('kippo', moddir)
        shutil.rmtree('{0}'.format('kippo'))
    elif not os.path.exists('{0}/{1}'.format(moddir, 'kippo')):
        shutil.copytree ('kippo', moddir)
        shutil.rmtree('{0}'.format('kippo'))
        log.info('Installed {0} in {1}'.format('kippo', moddir))

    if os.path.exists('{0}/{1}'.format(moddir, 'honssh')):
        log.info('Replacing {0}/{1} with the latest version'.format(moddir, 'honssh'))
        shutil.rmtree('{0}/{1}'.format(moddir, 'honssh'))
        shutil.copytree ('honssh', moddir)
        shutil.rmtree('{0}'.format('honssh'))
    elif not os.path.exists('{0}/{1}'.format(moddir, 'honssh')):
        shutil.copytree ('honssh', moddir)
        log.info('Installed {0} in {1}'.format('honssh', moddir))
        shutil.rmtree('{0}'.format('honssh'))

    if os.path.exists('{0}/{1}'.format(moddir, 'hpfeeds'):
        log.info('Replacing {0}/{1} with the latest version'.format(moddir, 'hpfeeds'))
        shutil.rmtree('{0}/{1}'.format(moddir, 'hpfeeds'))
        shutil.copytree ('hpfeeds', moddir)
        shutil.rmtree('{0}'.format('hpfeeds'))
    elif not os.path.exists('{0}/{1}'.format(moddir, 'hpfeeds'):
        shutil.copytree ('hpfeeds', moddir)
        log.info('Installed {0} in {1}'.format('hpfeeds', moddir))
        shutil.rmtree('{0}'.format('hpfeeds'))


def installcfg():
    """Installs configuration files. Verifies that the current directory contains the
    application critical files, will call sys.exit(1) if missing. Checks for
    non-application critical files, will throw warning is missing. Checks for existing
    configuration files in cfgdir, will rename existing ones before installing the new
    ones."""
    cfgdir = '/etc/honssh'
    mvtime = time.strftime('%y%m%d%H%M%S') 
    honcfg = '{0}/{1}'.format(cfgdir, 'honssh.cfg')
    hontac = '{0}/{1}'.format(cfgdir, 'honssh.tac')

    if not os.path.isfile('honssh.cfg'):
        log.info('CfgFileError: {0} was not found!'.format('honssh.cfg'))
        sys.exit(1)

    if not os.path.isfile('honssh.tac'):
        log.info('CfgFileError: {0} was not found!'.format('honssh.tac'))
        sys.exit(1)

    if not os.path.isfile('utils/honssh.sql'):
        log.info('CfgFileWarning: {0} appears to be missing'.format('utils/honssh.sql'))

    if not os.path.isfile('utils/playlog.py'):
        log.info('CfgFileWarning: {0} appears to be missing'.format('utils/playlog.py'))

    if not os.path.isfile('honsshctrl.sh'):
        log.info('CfgFileWarning: {0} appears to be missing'.format('honsshctrl.py'))

    if not os.path.isfile('honeydata.py'):
        log.info('CfgFileWarning: {0} appears to be missing'.format('honeydata.py'))

    if os.path.isfile('{0}'.format(honcfg))
        log.info('File {0} exists, creating backup...'.format(honcfg))
        os.rename('{0}'.format(honcfg), '{0}-{1}'.format(honcfg, mvtime))
        log.info('{0} was renamed to {0}-{1}'.format(honcfg, mvtime))
        log.info('Installing new version of {0}'.format(honcfg))
        os.rename('honssh.cfg', honcfg)
    elif not os.path.isfile('{0}'.format(honcfg))
        log.info('Installing {0}'.format(honcfg))
        os.rename('honssh.cfg', honcfg)

    if os.path.isfile('{0}'.format(hontac))
        log.info('File {0} exists, creating backup...'.format(hontac))
        os.rename('{0}'.format(hontac), '{0}-{1}'.format(hontac, mvtime))
        log.info('{0} was renamed to {0}-{1}'.format(hontac, mvtime))
        log.info('Installing new version of {0}'.format(hontac))
        os.rename('honssh.tac', hontac)
    elif not os.path.isfile('{0}'.format(hontac))
        log.info('Installing {0}'.format(hontac))
        os.rename('honssh.tac', hontac)


    # requirements
    # README

    # Generates the keys without any passphrase
    # id_rsa.pub
    # id_rsa
    ckeygen -t rsa -f id_rsa -q --no-passphrase

    # - Utility scripts
    if os.
    # playlog.py => playlog
    # honsshctrl.py => honsshctrl
    # honeydata.py (bzstats) => honsydata 


def installutils():
    """Installs the various utils. """
    utldir = '/usr/local/bin'

#
#   FUNCTION: Download and instal GeoLite2-City data base 
#

#
#   FUNCTION: Install dependencies
#
