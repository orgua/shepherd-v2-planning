## Install

git clone <https://github.com/RobertCNelson/omap-image-builder>
cd ./omap-image-builder
rm -rf ./git

For Debian based distros the prereqs are:

- m4
- debootstrap
- debootstick
- qemu-system-arm (+ many dependencies)
- chrootuid (?? probably not)
- bash-completion (convenience)
- git
- sbuild (just a guess)
- [buildroot-reqs](https://buildroot.org/downloads/manual/manual.html#requirement) (probably not needed)
- qemubuilder (+ many dependencies)
- qemu-user-static
- crossbuild-essential-armhf
- coreutils
- sbuild-qemu
- qemu-utils
- pbuilder
- cdebootstrap
- zstd
- schroot
- tree (definitely)

## Run Ubuntu 20.04 Focal

```Shell
./RootStock-NG.sh -c rcn-ee.net-console-ubuntu-focal-v5.10-ti-armhf

rm -rf ./ignore
cd deloy/ubu

sudo ./setup_sdcard.sh --img-2gb am335x-ubuntu-20.04.5-console-armhf-2023-03-14 --dtb beaglebone --distro-bootloader --enable-cape-universal --enable-uboot-disable-pru --enable-bypass-bootup-scripts

xz -v6 am335
#  ⇾ 4 MB/s, -v6 got ~8 MB/s
mv am ~/

# ⇾ should yield 318 M

sudo du -hc --max-depth=1 ./

scp service@141.76.39.100:/home/service/am335x-ubuntu-20.04.5-console-armhf-2023-03-11-2gb.img.xz /mnt/f/
```

## Run Ubuntu 22.04 Jammy

```Shell
nano ./configs/neslab-ubuntu-jammy-console-armhf.conf


./RootStock-NG.sh -c neslab-ubuntu-jammy-console-armhf


final name "shepherd-ubuntu-20.04.5-console-armhf-2023-03-10-2gb.img.xz"

scp service@141.76.39.100:/home/service/omap-image-builder/deploy/ubuntu-20.04.5-console-armhf-2023-03-10/ubuntu-20.04.5-console-armhf-2023-03-10-2gb-2gb.img.xz ./
```

## run Ubuntu 22.04 focal (frankenstein)

```text
./RootStock-NG.sh -c neslab-ubuntu-focal-console-v4.19-ti-armhf
# ⇾ does NOT work as used ubuntu image is determined by deb_codename
```

## slim down the ubuntu image

wireless - removable

```text
bluetooth
hostapd
iw
wpasupplicant

bb-wl18xx-firmware
bb-wlan-defaults
```

functionality not needed

```text
btrfs-progs
gnupg
hexedit
less            (⇾ nano)
pastebinit
vim

bb-bbai-firmware
bb-u-boot-am57xx-evm
sancloud-firmware
```

additionally unneeded (to test)

```text
linux-firmware      (+ comment-out "include_firmware")
libiio-utils        (industrial IO Subsystem)
cloud-guest-utils   (TODO, depends on fdisk, gdisk, python3)
wireguard-tools
```

switch to older kernel by default (focal)

```text
bbb.io-kernel-4.19-ti
linux-image-4.19.94-ti-r73
4.19.94-ti-r73
4.19-ti
cmem = 4.16.00.01
    ⇾ installs ti-cmem-{version}
    https://github.com/rcn-ee/ti-cmem
    https://github.com/rcn-ee/ipc-ludev
    TODO: 4.20.00.01 could still be ok?
```

add functionality

```text
zstd
```

result

```text
xz-v6   raw
323     1396        official repo
319 MB  1363 MB     home-build, unchanged   (50 MB ram usage)
150      578        without (1/2 of) above
147      571        apply above (except cloud-guest)
139      547        switch to 4.19           ⇾ works!
```

## switch apt to jammy (dirty)

base: latest 4.19 image

```Shell
sudo nano /etc/apt/sources.list

# - start with 580 mb used, 47 mb ram

# ⇾ replace focal with jammy on official repos
#    - ends with 760 mb used
#    - python 3.10.6

# ⇾ replace with lunar
#    - ends with 893 mb used, 41 mb ram
#    - python 3.11.1 & 3.10.9 ?

sudo do-release-upgrade -d

shepherd install
apt installs python3-numpy 1.24.2-1
# but pip install shepherd-package installs numpy again - with full compile
```

| Package                  | Version     |
|--------------------------|-------------|
| dbus-python              | 1.3.2       |
| decorator                | 5.1.1       |
| distlib                  | 0.3.6       |
| filelock                 | 3.9.0       |
| gevent                   | 22.10.2     |
| greenlet                 | 2.0.1       |
| h5py.-debian-h5py-serial | 3.7.0       |
| Mako                     | 1.2.4.dev0  |
| Markdown                 | 3.4.1       |
| markdown-it-py           | 2.1.0       |
| MarkupSafe               | 2.1.2       |
| mdurl                    | 0.1.2       |
| msgpack                  | 1.0.3       |
| netifaces                | 0.11.0      |
| numpy                    | 1.24.2      |
| olefile                  | 0.46        |
| Pillow                   | 9.4.0       |
| pip                      | 23.0.1      |
| platformdirs             | 3.0.0       |
| py                       | 1.11.0      |
| Pygments                 | 2.14.0      |
| PyGObject                | 3.43.1.dev0 |
| pymacaroons              | 0.13.0      |
| PyNaCl                   | 1.5.0       |
| python-apt               | 2.5.3       |
| PyYAML                   | 6.0         |
| pyzmq                    | 24.0.1      |
| rich                     | 13.3.1      |
| scipy                    | 1.10.1      |
| setuptools               | 67.6.0      |
| six                      | 1.16.0      |
| ubuntu-advantage-tools   | 8001        |
| virtualenv               | 20.20.0     |
| wheel                    | 0.38.4      |
| zope.event               | 4.4         |
| zope.interface           | 5.5.2       |
