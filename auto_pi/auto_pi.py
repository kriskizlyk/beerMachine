#!/usr/bin/env python
# aptinstall.py

import apt
import subprocess
import time

def process(*args):
    string = str(*args)
    subprocess.call(['echo', '     ', string])
    p = subprocess.Popen(*args)
    while(1):
        if (p.poll() == 0):
            break;
    time.sleep(0.1)
    subprocess.call(['echo', '\n'])

def process_hide(*args):
    p = subprocess.Popen(*args, stdout=subprocess.PIPE)
    while(1):
        if (p.poll() == 0):
            break;

process(['clear'])

subprocess.call(['cd', '..', '&&', 'cd', '..'])
subprocess.call(['sudo', 'chown', '-R', 'pi', '/'])
subprocess.call(['mkdir', 'kk_hacks'])

subprocess.call(['echo' ,'     Running macro to prepare for install of system.'])
subprocess.call(['echo' ,'     Updating the operating system.'])
process(['sudo', 'apt-get', 'update'])
process(['sudo', 'apt-get', 'upgrade'])
process(['sudo', 'apt-get', 'dist-upgrade'])

subprocess.call(['echo' ,'     Installing git.'])
#process(['sudo', 'apt-get', 'install', 'python-dev'])
process(['sudo', 'apt-get', 'install', 'git', '-y'])

subprocess.call(['echo' ,'     Installing Python.'])
#process(['sudo', 'apt-get', 'install', 'python-dev'])
process(['sudo', 'apt-get', 'install', 'python3-dev', '-y'])

subprocess.call(['echo' ,'     Installing Python PIP.'])
#process(['sudo', 'apt-get', 'install', 'python-pip'])
process(['sudo', 'apt-get', 'install', 'python3-pip', '-y'])

subprocess.call(['echo', '     Installing GTK...'])
process(['sudo', 'apt-get', 'install', 'libgtk-3-dev', '-y'])

subprocess.call(['echo', '     Installing Glade...'])
process(['sudo', 'apt-get', 'install', 'glade', '-y'])

subprocess.call(['echo' ,'     Installing I2C Tool.'])
process(['sudo', 'apt-get', 'install', 'i2c-tools', '-y'])

subprocess.call(['echo' ,'     Installing smbus2.'])
process(['sudo', 'pip', 'install', 'smbus2', '-y'])
# process(['sudo', 'apt-get', 'install', 'python-smbus'])
# process(['sudo', 'apt-get', 'install', 'python3-smbus'])

subprocess.call(['echo' ,'     Cleaning up install files.'])
process(['sudo', 'apt-get', 'clean'])

subprocess.call(['echo' ,'     Consider the following, if required.'])
subprocess.call(['echo' ,'     git config --global user.name "Your Name"'])
subprocess.call(['echo' ,'     git config --global user.email email@example.com '])
