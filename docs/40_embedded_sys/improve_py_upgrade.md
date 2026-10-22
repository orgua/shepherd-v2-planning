# Python Upgrade

Update 2024-01: Ubuntu 22.04 Images from [rcn-ee](https://rcn-ee.com/rootfs/) are fine. Python 3.10 brings a Load-Reduction.

## Problem

- storing to USB causes trouble
- high counts of GPIO-Edges cause trouble (heavy load)
- emulation causes already ~ 80 % cpu-load
- newer libs would probably bring lots of improvements (some like h5py seem essential), but upgrading fails due to scipy / numpy build trouble
- linux-images were updated 2020-04

## Current State (2020)

- BBone with Ubuntu 18.04.44, image from 2020-03, linux-image-4.19.94-ti-r36
- Python 3.6
  - scipy 0.19.1      ⇾ (1.7.0)
  - numpy 1.13.3      ⇾ 1.19.5 (1.21.1)
  - h5py 2.7.1        ⇾ 3.1 (3.3)
  - setuptools 39.x,  ⇾ 57.4.0
  - pip 9.x           ⇾ 21.2.1
- python 3.9.5 (ubuntu 21.04/hirsute)
  - scipy 1.6.0
  - numpy 1.19.5
  - h5py 2.10.0
  - pip 20.3.4
  - setuptools 52.0.0
- manual update (brings solvable libcblas-trouble)
  - setuptools 57.4.0
  - pip 21.2.1
  - numpy 1.21.2
  - scipy 1.7.0
  - h5py 3.4.0
- Kai reports that h5py v3.1 works with current shepherd-sw
- I report that code is working after bringing libs to newest version

## Upgrading Ubuntu

Tutorial: <https://www.howtogeek.com/351360/how-to-upgrade-to-the-latest-version-of-ubuntu/>

```Shell
sudo apt install update-manager-core

# switch to normal
sudo nano /etc/update-manager/release-upgrades ⇾ normal

# show current Version
do-release-upgrade -V

# show available Version
do-release-upgrade -c

# Update, Needs currently 1353 MB of Space for Focal, so clean up current system
sudo rm -rf /var/log/*
do-release-upgrade --allow-third-party
# TODO: does not run without interaction
# ⇾ brings python3.8.10 and gcc9.3/10 and kernel 5.4.24?
# wants to install linux-image-5.4.24-armv7-x20, check uEnv.txt ⇾ is fine, 4.19 stays default
sudo apt remove linux-headers-5.4.* linux-image-5.4.*
sudo rm -rf /boot/initrd*
sudo apt autoremove
sudo apt clean
# from 1.8 GB free down to 1.5 GB for ubuntu 20.04.34/focal

# rinse and repeat to get ubuntu 21.04/hirsute, python 3.9.5, gcc 10.3
do-release-upgrade --allow-third-party --quiet
# still does not run quiet, but is done faster
# from 1.5 GB free down to 1.3 GB for ubuntu 21.04.13/hirsute

# cleanup
ansible-playbook deploy/setup_linux_configuration.yml
ansible-playbook deploy/setup_linux_performance.yml
ansible-playbook deploy/setup_linux_security.yml

# TODO: there is gcc-7/9/10 installed

# clean python packages, avoid sudo on fresh images!!
sudo /usr/bin/python3 -m pip install --upgrade pip
sudo /usr/bin/python3 -m pip uninstall click click-config-file numpy python-periphery scipy zerorpc invoke h5py psutil pyserial -y


# some packages where installed via distutils: PyYAML pyzmq pyxdg
sudo apt remove python3-yaml python3-xdg python3-zmq
sudo apt remove python3-six python3-gevent python3-keyring* python3-numpy python3-secretstorage
sudo apt remove python3-gi
sudo apt autoremove
sudo apt clean

sudo /usr/bin/python3 -m pip uninstall Adafruit-BBIO Pillow six asn1crypto cryptography decorator -y
sudo /usr/bin/python3 -m pip uninstall idna keyring keyring.alt olefile gevent  SecretStorage -y
/usr/bin/python3 -m pip list --outdated
sudo /usr/bin/python3 -m pip install --upgrade wheel virtualenv setuptools

# packages install again
sudo apt install python3-yaml python3-xdg python3-zmq
sudo apt install python3-gevent python3-numpy python3-secretstorage
sudo apt install python3-gi
# new packages per apt
sudo apt install python3-scipy
sudo apt install python3-h5py

# try to further update, TODO: not the best idea
/usr/bin/python3 -m pip install --help
/usr/bin/python3 -m pip install --upgrade --only-binary :all: setuptools pip virtualenv wheel
/usr/bin/python3 -m pip install --upgrade --only-binary :all: six cryptography distlib distro gevent Pillow pyzmq
/usr/bin/python3 -m pip install --upgrade --only-binary :all: numpy
/usr/bin/python3 -m pip install --upgrade --only-binary :all: scipy
/usr/bin/python3 -m pip install --upgrade --only-binary :all: h5py
# update not working with pip: pyYAML, xdg

# trouble with numpy ⇾ libcblas.so.3: cannot open shared object file: No such file or directory
sudo apt install libopenblas-dev libblas-test
# ⇾ does not fix error
sudo /usr/bin/python3 -m pip uninstall numpy scipy h5py
sudo /usr/bin/python3 -m pip uninstall cryptography pyzmq
sudo /usr/bin/python3 -m pip uninstall six pillow
#
sudo apt remove  python3-numpy python3-h5py python3-scipy python3-h5py-serial python3-zmq python3-six python3-cryptography
sudo apt install python3-numpy python3-h5py python3-scipy python3-h5py-serial python3-zmq python3-six python3-cryptography
```

Alternative ⇾ fresh test-images, debian only: <https://rcn-ee.com/rootfs/bb.org/testing/2021-07-26/buster-console/>

BBone PIP-Transactions can take forever, speedup by not installing from sources::

```text
[sudo] /usr/bin/python3 -m pip install --upgrade wheel packetname
```

## Alternative to manual updating Distro

- build or use fresher image
- <https://forum.digikey.com/t/debian-getting-started-with-the-beaglebone-black/12967#BeagleBoneBlack-Ubuntu20.04LTS>

## New Packets

WIP

```Shell
sudo apt install python3-msgpack-numpy
```

## Experiment with Upgrade

- current config
  - python 3.9.5
  - ubuntu 21.04/hirsute
- shepherd.code is still functional with major updates of pypackets
- Trouble
  - some timejumps during recording detected (in 10s window)
  - flushing and closing hdf5 file seems to hang at the end, some load
  - a litte deprecation-warning for str-compares with "is"
  - gevent.signal() is ancient ⇾ gevent.signal_handler()
- `sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml`
  - ~ 57 % cpu-load for recording, 118 MB Ram (85 MB before)
- EMU: `sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml`
  - ~ 77 % cpu-load for emulation, 127 MB Ram (85 MB before) (verbose=3)
  - only 63 to 68 % with verbose <= 2

```Shell
sudo mount -t exfat /dev/mmcblk0p1 /var/shepherd/recordings2
# ⇾ TODO: fails after update despite installing all 3 extfat-packages in apt

sudo nano /etc/shepherd/example_config_emulation.yml

  command: emulate
  parameters:
    #input_path: /var/shepherd/recordings2/indoor_solar/sheep4/office_sd.h5
    input_path: /var/shepherd/recordings/test_rec.h5
    output_path: /var/shepherd/recordings/test_emu.h5
    virtsource:
    force_overwrite: true
    no_calib: false
    enable_io: true
    io_sel_target_a: true
    pwr_sel_target_a: true
    aux_voltage: 3.3
    uart_baudrate: 9600
  verbose: 3

sudo nano /etc/shepherd/config.yml

  command: record
  verbose: 3
  parameters:
    output_path: /var/shepherd/recordings/test_rec.h5
    mode: harvesting
    duration: 60.0
    force_overwrite: true
    no_calib: true
```

## Server PipEnv Updates

useful commands::

```text
pip3 install pipenv
# or
pipenv --rm
pip3 install --upgrade pipenv setuptools virtualenv pip six certifi distlib

pipenv install --deploy

pipenv update --keep-outdated packet
pipenv uninstall ansible ansible-base ansible-core --skip-lock
pipenv graph
pipenv check
pipenv lock --clear

pipenv shell
exit
```
