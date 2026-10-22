# Migration to Ubuntu 22.04

- starting-point is Ubuntu 20.04.04
- release: <https://rcn-ee.com/rootfs/ubuntu-armhf-22.04-console-v5.10-ti/> ⇾ bone ... console armhf
- kernel 5.10.168-ti-r72
- minimal image with 2.1 GB of free space
- software versions on 20.04
  - python 3.8.2
  - numpy 1.17.7 ?
  - skipy ?
  - h5py 2.10.0
- software version on 22.04
  - python 3.10.3 (significant speed boost)
  - numpy 1.21.5
  - skipy 1.7.1
  - h5py 3.6.0

## Install Steps

- mostly: <https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Flashing_eMMC>
- flashing to eMMC via user-button was not active by default ⇾ activated by changing line in /boot/uEnv.txt
- playbook bootstrap
- optional highly manual interlude ⇾ update to ubuntu 22.04 release::

```text
# this will leave you with newer package-versions
# h5py has a memory-leak in version <3.5 that prevents you from emulating > 4h in one go
[host] ansible-playbook deploy/setup_linux_configuration.yml
[sheep] sudo apt install update-manager-core
[sheep] sudo do-release-upgrade --devel-release --quiet --allow-third-party
[host] playbook setup_allow_ssh_from_pwless_host
[sheep] sudo nano /etc/sudoers ⇾ %sudo ALL=(ALL) NOPASSWD: ALL
[sheep] sudo nano /etc/apt/sources.list ⇾ reactivate rcn-repo
```

- ansible-playbook deploy/setup_linux_configuration.yml
- ansible-playbook deploy/deploy.yml
- changed branch on sheep: git stash, git pull, git checkout hw_v2.2
- playbook dev_rebuild_pru
- test: sudo shepherd-sheep -vvv run --config /etc/shepherd/config.yml
- add usb-thumbdrive

```Shell
sudo mount -t ext4 -o defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,noacl,nouser_xattr,users /dev/sda /var/shepherd/recordings
sudo mount /dev/sda /var/shepherd/recordings
# or add to /etc/fstab:
/dev/sda  /var/shepherd/recordings  ext4  defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,noacl,nouser_xattr,users,noauto  0  0

sudo umount -f -v /dev/sda

mount /dev/mmcblk0 /var/shepherd/recordings
sudo umount -f -v /dev/mmcblk0

safe image:
sudo dd if=/dev/mmcblk1 of=/var/shepherd/recordings/mmc_u224_k419_deployed.img
```

## Alternative to try: update python

<https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu/pool/main/p/python3.11/>

```Shell
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

or

```Shell
sudo add-apt-repository universe
sudo apt update
sudo apt install python3.10
```

## Modifications

- linuxptp switched to systemd service-templates ⇾ ptp-host playbook needs improvement
- test newest kernel 5.10.100 ⇾ expected trouble with memory interface to pru
  - will downgrade to 4.19 for now
- update apt-install-list against pip-list ⇾ fresh
  - 29_improve...rst is a good base for setup
- failed unittests
  cd /opt/shepherd/software/python-package/
  sudo python3 setup.py test --addopts "-vvv"

tests/test_sysfs_interface.py::test_calibration_settings[real_hardware] FAILED
tests/test_sysfs_interface.py::test_initial_calibration_settings[real_hardware] FAILED

### build kernel module with 5.4.106-r40

cd /opt/shepherd/software/kernel-module/src

```Shell
make -C /lib/modules/5.4.106-ti-r40/build M=/opt/shepherd/software/kernel-module/src modules
make[1]: Entering directory '/usr/src/linux-headers-5.4.106-ti-r40'
  CC [M]  /opt/shepherd/software/kernel-module/src/sync_ctrl.o
  CC [M]  /opt/shepherd/software/kernel-module/src/pru_comm.o
  CC [M]  /opt/shepherd/software/kernel-module/src/sysfs_interface.o
  CC [M]  /opt/shepherd/software/kernel-module/src/pru_mem_msg_sys.o
  CC [M]  /opt/shepherd/software/kernel-module/src/module_base.o
  LD [M]  /opt/shepherd/software/kernel-module/src/shepherd.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC [M]  /opt/shepherd/software/kernel-module/src/shepherd.mod.o
make[3]: *** No rule to make target 'arch/arm/kernel/module.lds', needed by '/opt/shepherd/software/kernel-module/src/shepherd.ko'.  Stop.
make[2]: *** [scripts/Makefile.modpost:95: __modpost] Error 2
make[1]: *** [Makefile:1648: modules] Error 2
make[1]: Leaving directory '/usr/src/linux-headers-5.4.106-ti-r40'
make: *** [Makefile:17: build] Error 2

- /lib/modules/5.4.106-ti-r40/build is the wrong folder
cd /usr/src/linux-headers-5.4.106-ti-r40/arch/arm/

https://github.com/beagleboard/linux/issues/263

uname -r
sudo apt install
linux-kernel-5.4.106-ti-r40
linux-headers-5.4.106-ti-r40
linux-libc-dev

sudo ntpdate -b -s -u pool.ntp.org

downgrade ⇾ https://rcn-ee.com/repos/ubuntu/pool/main/l/linux-upstream/
sudo apt install linux-image-5.4.70-ti-r22

      CC [M]  /opt/shepherd/software/kernel-module/src/pru_comm.o
    /tmp/ccp9lSUA.s: Assembler messages:
    /tmp/ccp9lSUA.s:43: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:231: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:301: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:341: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:367: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:407: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:448: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:464: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:517: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:531: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:583: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:599: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:658: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:674: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:733: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:749: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:802: Error: selected processor does not support `dsb ' in ARM mode
    /tmp/ccp9lSUA.s:816: Error: selected processor does not support `dsb st' in ARM mode
    /tmp/ccp9lSUA.s:861: Error: selected processor does not support `dsb ' in ARM mode
    make[2]: *** [scripts/Makefile.build:266: /opt/shepherd/software/kernel-module/src/pru_comm.o] Error 1
    make[1]: *** [Makefile:1732: /opt/shepherd/software/kernel-module/src] Error 2
    make[1]: Leaving directory '/usr/src/linux-headers-5.4.70-ti-r22'
    make: *** [Makefile:17: build] Error 2


sudo apt install linux-image-5.4.87-ti-r23
sudo apt install linux-headers-5.4.87-ti-r23
- same as .70

sudo apt install linux-image-5.4.52-ti-r17
sudo apt install linux-headers-5.4.52-ti-r17
- same as .70

switch back to 4.19.94-ti-r72' with script
⇾ works

sudo apt install linux-image-5.4.106-ti-r26
sudo apt install linux-headers-5.4.106-ti-r26
sudo apt install libpruio-modules-5.4.106-ti-r26
sudo apt install ti-sgx-ti335x-modules-5.4.106-ti-r26
- same as .70

sudo apt install linux-image-5.4.106-ti-r33
sudo apt install linux-headers-5.4.106-ti-r33
sudo apt install libpruio-modules-5.4.106-ti-r33
sudo apt install ti-sgx-ti335x-modules-5.4.106-ti-r33
- same as .70

sudo apt install linux-image-5.4.106-ti-r40 linux-headers-5.4.106-ti-r40 libpruio-modules-5.4.106-ti-r40 ti-sgx-ti335x-modules-5.4.106-ti-r40
- new 106 error

sudo apt install linux-image-5.4.106-ti-r36 linux-headers-5.4.106-ti-r36 libpruio-modules-5.4.106-ti-r36 ti-sgx-ti335x-modules-5.4.106-ti-r36
- same as .70

sudo apt install linux-image-5.4.106-ti-r39 linux-headers-5.4.106-ti-r39 libpruio-modules-5.4.106-ti-r39 ti-sgx-ti335x-modules-5.4.106-ti-r39
- new 106 error

sudo apt install linux-image-5.4.161-bone63 linux-headers-5.4.161-bone63 libpruio-modules-5.4.161-bone63
- new 106 error

sudo apt install linux-image-5.4.182-bone64 linux-headers-5.4.182-bone64 libpruio-modules-5.4.182-bone64
- new 106 error

sudo apt install linux-image-5.9.16-bone40 linux-headers-5.9.16-bone40 libpruio-modules-5.9.16-bone40
⇾ whole new can of worms (timespec and timespec_to_ns is unknown now)
```

Quickfix:

sudo apt install linux-headers-5.4.106-ti-r40

wget <https://raw.githubusercontent.com/torvalds/linux/master/scripts/module.lds.S> -O /usr/src/linux-headers-5.4.106-ti-r40/scripts/module.lds
sudo sed -i '$ d' /usr/src/linux-headers-5.4.106-ti-r40/scripts/module.lds

sudo nano /usr/src/linux-headers-5.4.106-ti-r40/scripts/Makefile.modpost

cd /opt/shepherd/software/kernel-module/src

also available:

- .87-ti-r23
- .93-ti-r24
- .93-ti-r25
- .106-ti-r26 to -r40
- .47-ti-r12
- .40-ti-r9

later:
5.10.106-ti-r41

- emulation loop is too slow - with active harvester it is not RT, without hrv it takes ~ 8.3 / 10 us
- current state, with[ns]:
  - read          580     420
  - calc_harv DIS 200     260, 740 en
  - calc_inp      940
  - spi_read      900
  - calc_out      1960
  - calc_cap      1500
  - calc_state    1000
  - spi_write     800
  - calc_end      200
  - kernelcom     140 or bufferswap 680 ⇾ now 800
- util-manager shows that ram-read can take from 420 to ~3000 ns
  - even with mean-util = 67 % max gets over 100 %
  - sharedmem-read shows 160 ns (includes entering fn)
  - solution: move expensive read to pru1

Transfer Speed per SSH, down 4.6 MB/s max

ssh -Q ciphers
scp -c aes128-ctr hans@10.0.0.9:/var/shepherd/recordings/
scp -c <aes128-gcm@openssh.com> hans@10.0.0.9:/var/shepherd/recordings/
