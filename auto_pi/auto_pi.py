#!/usr/bin/env python
# aptinstall.py

import apt
import subprocess
import time
import os

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

#sudo passwd
#root
#root
#su
#root
#cd ..
#cd ..

subprocess.call(['echo' ,'Running macro to prepare for install of system.'])
subprocess.call(['echo', '\n'])

subprocess.call(['echo' ,'     Creating directory kk_hacks...'])
subprocess.call(['mkdir', 'kk_hacks'])
os.chdir('/kk_hacks')
subprocess.call(['echo' ,'     Change Directory: ' + str(os.getcwd())])
subprocess.call(['echo' ,'     Creating directory monitoringPy_v1_00.'])
subprocess.call(['mkdir', 'monitoringPy_v1_00'])
#os.chdir('/kk_hacks/monitoringPy_v1_00')
#subprocess.call(['echo' ,'     Change Directoy: ' + str(os.getcwd())])
subprocess.call(['echo', '\n'])

'''
subprocess.call(['echo' ,'     Updating the operating system.'])
process(['sudo', 'apt-get', 'update', '-y'])
process(['sudo', 'apt-get', 'upgrade', '-y'])
process(['sudo', 'apt-get', 'dist-upgrade', '-y'])

subprocess.call(['echo' ,'     Installing git.'])
process(['sudo', 'apt-get', 'install', 'git', '-y'])

subprocess.call(['echo' ,'     Installing Python.'])
process(['sudo', 'apt-get', 'install', 'python3-dev', '-y'])

subprocess.call(['echo' ,'     Installing Python PIP.'])
process(['sudo', 'apt-get', 'install', 'python3-pip', '-y'])

subprocess.call(['echo', '     Installing GTK...'])
process(['sudo', 'apt-get', 'install', 'libgtk-3-dev', '-y'])

subprocess.call(['echo', '     Installing Glade...'])
process(['sudo', 'apt-get', 'install', 'glade', '-y'])

subprocess.call(['echo' ,'     Installing I2C Tool.'])
process(['sudo', 'apt-get', 'install', 'i2c-tools', '-y'])

subprocess.call(['echo' ,'     Installing smbus2.'])
#process(['sudo', 'pip', 'install', 'smbus2'])
process(['sudo', 'pip3', 'install', 'smbus2'])
# process(['sudo', 'apt-get', 'install', 'python-smbus'])
# process(['sudo', 'apt-get', 'install', 'python3-smbus'])

subprocess.call(['echo', '     Enabling RaspberryPi Peripherals'])
subprocess.call(['echo', '     Enabling VNC...'])
subprocess.call(['raspi-config', 'nonint', 'do_vnc', '0'])
subprocess.call(['echo', '     Enabling SPI...'])
subprocess.call(['raspi-config', 'nonint', 'do_spi', '0'])
subprocess.call(['echo', '     Enabling I2C...'])
subprocess.call(['raspi-config', 'nonint', 'do_i2c', '0'])
subprocess.call(['echo', '     Enabling Serial...'])
subprocess.call(['raspi-config', 'nonint', 'do_serial', '0'])
subprocess.call(['echo', '     Disable Overscan (Remove Display Border)...'])
subprocess.call(['raspi-config', 'nonint', 'do_overscan', '1'])
subprocess.call(['echo', '\n'])
'''

subprocess.call(['echo' ,'     Initilizing Git'])
subprocess.call(['git', 'init'])
subprocess.call(['echo' ,'     Setting user name, rpi.'])
process(['git', 'config', '--global', 'user.name', 'rpi'])
subprocess.call(['echo' ,'     Setting email address kriskizlyk@gmail.com'])
process(['git', 'config', '--global', 'user.name', 'kriskizlyk@gmail.com'])
subprocess.call(['echo' ,'     Adding remote git address.'])
process(['git', 'remote', 'add', 'origin', 'https://github.com/kriskizlyk/monitoringPy_v1_00 .'])
subprocess.call(['echo' ,'     Cloning Prcd oject'])
subprocess.call(['git', 'clone', 'https://github.com/kriskizlyk/monitoringPy_v1_00'])

subprocess.call(['echo', '\n'])
subprocess.call(['echo' ,'     Cleaning up install files.'])
process(['sudo', 'apt-get', 'clean'])
