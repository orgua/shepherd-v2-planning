# Linux Improvements

## Ansible-playbooks

### Bootstrap

- "Set authorized key from local file" ⇾ script stops, no ssh pub key generated before trying to access it, on host!
  - give better error message
  - fix: ssh-keygen
- why "ansible_become_password", what is the meaning? script sets no pw when creating new user
- user should add (maybe)
  - `generate_ssh_key: yes`
  - `state: present`

### General

- playbook workflow - why "changed", and not all "ok"
- when is deploy needed? ⇾ better document all scripts
- accelerate ansible: allow pipelining in `ansible.cfg`` with `pipelining = True` in SSH-Section
- can bash-out be saved to file?
- how do we see if install is fine? ⇾ `journalctl -u shepherd`
- image could be run virtually

playbook args:

- `-v` ⇾ stdout
- `--check` ⇾ dry run

Improve Speed of SSH and Ansible by tuning local `~/.ssh/config`

```text
Host *
    AddressFamily inet
    Protocol 2
    Compression no
    ServerAliveInterval 60
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 6000
```

## System Status Feedback

BBB Leds

- USER0 is the heartbeat indicator from the Linux kernel.
- USER1 turns on when the SD card is being accessed
- USER2 is an activity indicator. It turns on when the kernel is not in the idle loop.
- USER3 turns on when the onboard eMMC is being accessed.

BBB Readme

- up-to-date system information <https://elinux.org/Beagleboard:BeagleBoneBlack_Debian>
  - updating kernel
  - new device tree interface
- improve system and boot performance: <https://embexus.com/2017/05/16/embedded-linux-fast-boot-techniques/>
- official boot optimization: <https://processors.wiki.ti.com/index.php/Sitara_Linux_Training:_Boot_Time_Reduction>

## System Evaluation

System-Info

- Ubuntu 18.04, bionic
- official image from 2020-03-12
- Beaglebone Green

### Storage Information

```Shell
# reference: https://learn.sparkfun.com/tutorials/single-board-computer-benchmarks
    BBB-revC, write 10 MB/s, read 27 MB/s

sudo blockdev --getbsz /dev/mmcblk1p1
    blocksize on eMMC and uSD is 4096 byte

sudo cat /sys/kernel/debug/mmc1/ios | grep "bus width"
    ⇾ should be 8 bits for mmc1/eMMC and 4 bits for mmc0/uSD
    # https://groups.google.com/forum/m/#!topic/beagleboard/fOGeXCub9OY
```

### Storage Benchmark

```Shell
dd if=/dev/zero of=./testfile bs=4096 count=40000 oflag=direct
# eMMC-w  5.6 MB/s, sda-w  5.6 MB/s, uSD-w  2.3 MB/s
dd if=/dev/zero of=./testfile bs=100M count=1 oflag=direct
# eMMC-w 21.1 MB/s, sda-w 26.0 MB/s, uSD-w 17.7 MB/s
dd if=/dev/zero of=./testfile bs=100M count=1
# eMMC-w 55.4 MB/s, sda-w 26.2 MB/s, uSD-w 39.3 MB/s
```

- explanation: uSD is a samsung evo plus 128 GB, sda is same uSD with a fast card reader via usb
- note: sd is only in 4bit-bus-mode
- learning: external USB seems to be the better choice for data storage,

### Find the biggest space waster

```Shell
sudo du -s /* | sort -n
    450 MB /lib ⇾ /firmware ⇾ intel 22 MB, netronome 24 MB, liquidio 24 MB, amdgpu 31 MB
    912 MB /usr
    190 MB /var

dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n
# better (part of debian-goodies):
dpigs -n20

# TODO 2021-07: /var/log/* has grown over time (> 500 mb)
sudo rm -rf /var/log/*

# TODO 2021-07: space-waster is now /usr/lib/firmware, 143 MB netronome, 48 MB qcom, 45 MB amd, 35 MB intel, 35 MB mellanox, 25 MB liquidio
# further removable: mrvl, ath1*, nvidia, radeon, iwlwifi*

# ⇾ collected in playbook dev_cleanup.yml
```

### Switch dynamically between cpu-governors

```Shell
sudo apt install cpufrequtils
cpufreq-info
sudo cpufreq-set --governor powersave
    ⇾ when idling
sudo cpufreq-set --governor performance
    ⇾ when preparing or during measurement
    hardcoded in /etc/init.d/cpufrequtils
    GOVERNOR, MAX_SPEED, MIN_SPEED
```

### CPU-Info

```Shell
cat /proc/cpuinfo | grep BogoMIPS
dmesg | grep Bogo # better
```

## Implemented System improvements

**Note:** most of these are already implemented in ansible playbooks.

### Downgrade kernel (deprecated & not correct way)

```Shell
sudo apt install linux-image-4.14.108-ti-r136, linux-headers-...
# currently installed 4.19.94-ti-r36
# ⇾ rt-kernel is possible, but A: not needed, B: bad for performance
# last updated bb-cape-overlays
sudo apt list --installed | grep linux- # ⇾ remove other
```

### Up- & Downgrade Kernel

```Shell
cd /opt/scripts/tools/
sudo git pull
sudo ./update_kernel.sh --lts-5_4
# ⇾ warning: does not work for BBB yet, just update to latest 4.19 release by omitting --lts..
sudo reboot

sudo apt-get install linux-headers-`uname -r`
```

### Update Bootloader

```Shell
sudo /opt/scripts/tools/developers/update_bootloader.sh
reboot
```

### SSHd improvement

```Shell
sudo nano /etc/ssh/sshd_config
    UseDNS no         # ⇾ disable dns lookup on server side
    Compression no    # ⇾ default is "delayed" (yes) after login

# Client side: use ipv4, one single tcp-connection (controlMaster auto) on Client-side
```

### SCP Improvement

```text
# Idea: handshake is secure and fully encrypted, after that the encryption could be lowered, maybe even with fast crypto-module-support
# switching crypto cipher ⇾ man ssh_config shows for local ``~/.ssh/config``, global ``/etc/ssh/ssh_config`` and ``sshd_config``

Specifies the ciphers allowed and their order of preference.  Multiple ciphers must be comma-separated.  If the specified list begins with a
‘+’ character, then the specified ciphers will be appended to the default set instead of replacing them.  If the specified list begins with a
‘-’ character, then the specified ciphers (including wildcards) will be removed from the default set instead of replacing them.  If the spec‐
ified list begins with a ‘^’ character, then the specified ciphers will be placed at the head of the default set.

The supported ciphers are:
    3des-cbc, aes128-cbc, aes192-cbc, aes256-cbc, aes128-ctr, aes192-ctr, aes256-ctr
    aes128-gcm@openssh.com, aes256-gcm@openssh.com, chacha20-poly1305@openssh.com

The default is:
    chacha20-poly1305@openssh.com, aes128-ctr, aes192-ctr, aes256-ctr,
    aes128-gcm@openssh.com,aes256-gcm@openssh.com

The list of available ciphers may also be obtained using "ssh -Q cipher".

OpenSSH 7.3 are:
    3des-cbc, aes128-cbc, aes192-cbc, aes256-cbc, aes128-ctr, aes192-ctr,
    aes256-ctr, aes128-gcm@openssh.com, aes256-gcm@openssh.com, arcfour,
    arcfour128, arcfour256, blowfish-cbc, cast128-cbc, chacha20-poly1305@openssh.com.
```

### Switch to proper timezone - 2h behind

```Shell
sudo dpkg-reconfigure tzdata
sudo nano /etc/timezone
# ⇾ one line "Europe/Berlin", alternative to "reconfigure"
```

### Software cleanup

```Shell
sudo apt list --installed
sudo apt -y remove ...
sudo apt autoremove

    alsa-utils
    dnsmasq
    dnsmasq-base
    nginx &-common &-core
    can-utils
    rfkill

    linux-headers-4.15.0*
    linux-image-5.4.24

    wireless-regdb -tools
    wpasupplicant
    ofono
```

Ansible-Hard.To.Get.packets

```Shell
sudo apt remove linux-image-4.19.94-ti-r36
# dpkg shows a kernel, that isn't in apt...
# dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n
sudo dpkg -P linux-image-5.4.24-armv7-x20
```

⇾ down to 1.4 GB MMC & <41 MB RAM usage (with shepherd)

More packages to remove

```Shell
sudo apt -y remove

    gcc-pru
    gdb-dbg
    gdb
    cmake
    btrfs-progs
    bluez
    alsa
```

### Disable Devices

```Shell
sudo nano /boot/uEnv.txt

    disable_uboot_overlay_video=1
    disable_uboot_overlay_audio=1
    disable_uboot_overlay_wireless=1
    disable_uboot_overlay_adc=1
```

### Switch to Ubuntu 20.04

(bionic to focal)

```Shell
# pro: brings fresh gcc 10, python 3.8, sshd 8.2,
sudo apt update && sudo apt upgrade
sudo reboot
sudo apt install update-manager-core
sudo do-release-upgrade -d
sudo reboot
# Some third party entries in your sources.list were disabled.
# new unwanted sw: libasound* alsa* ubuntu-release-upgrader* update-manager* ti-sgx* iw gfortran* eject
sudo apt-get remove '^namestart.*'
# general things to look out for gfx, rf, wifi, wlan, sound, alsa
```

### Shorten Boot-Time

```Shell
sudo rm /boot/initrd.img-*
# file is not needed and is putting a 20s wait on kernel
```

## Further actions

- nix, <https://nixos.org/> seems to be the better ansible (only future reference)
- is active cooling improving the performance? IC is only warm to the touch, so no
- look at ``dmesg`` for oddities
  - console on ttyO0, 115200n8, ttyS0 ⇾ see security concept
  - spectre v2 ⇾ not needed mitigation, cost performance
  - redundant drivers enabled: CAN driver, ALSA, Bluetooth ⇾ uninstalled
  - unusual timer-jump, mounting mmc takes 20-25s each ⇾ ext4-mount takes forever
    [    1.122421] Freeing unused kernel memory: 1024K
    [ 18.463305] EXT4-fs (mmcblk1p1): mounted filesystem with ordered data mode. Opts: (null)
- ``systemd-analyze blame`` shows:
  - v4.14: 39.936s dev-mmcblk1p1.device
  - v4.19: 53.286s dev-mmcblk1p1.device, 29.013s generic-board-startup.service
- look at power consumption
- BBB has a crypto engine, but is it used by openSSL! This site has a benchmark: <https://datko.net/2013/10/03/howto_crypto_beaglebone_black/>
- switch to more SD friendly filesystem, F2FS, YAFFS2
- benchmark cpu BOINC
- switch from ``-ti-kernel`` to ``-bone``?
  - see <https://groups.google.com/forum/#!topic/beagleboard/sAefubfDqco>
  - ``-bone`` is from Robert Nelson, mainly for BB and BBB, PRU with UIO
  - ``-ti-kernel`` is for all TI CPUs, PRU with remoteproc
  - ``-xenomai`` is dual kernel, realtime, 40 us
  - ``-rt`` uses preemt features to reduce latency to about 100 us

### Unnecessary kernel modules

`lsmod` shows

- wkup_m3_ipc               ⇾ Cortex M3 Co-Processor, misbehaving in dmesg, loaded to early
- virtio, virtio-ring       ⇾ IO-Virtualization in KVM
- uio, uio_pdrv_genirq      ⇾ should be user-space IO
- u_serial, usb_f_acm       ⇾ serial emulation on USB
- sch_fq_codel              ⇾ Fair Queue controlled delay
- libcomposite              ⇾ usb HID and massstorage
