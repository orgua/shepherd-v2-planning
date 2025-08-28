# BeagleBone AI64 Eval

## TLDR

- same performance as RPi CM4
- feels outdated: despite huge heat sink not stable without active cooling or optimized airflow
- as a dev-platform hard to manage, with > 20'000 pages of documentation for the SOC
- feels overloaded: too many layers of complexity with 20 listed coprocessors
- software not ready - as [ptp still has issues](https://github.com/nes-lab/shepherd/blob/dev/software/test_timesync/Readme_D_analysis.md)

## Advantages

- dual-core 2GHz 64-bit Cortex A72 (instead 1x 1GHz Cortex A8 32-bit)
  - ArmV8, Neon, AArch64,
- 10x faster USB, GBE
- 6x 1 GHz Cortex-R5F MCUs
- 8x larger eMMC & RAM
- several other coprocessors, dsp and accelerators
- support for Time-sensitive Networks (TSN)
- NOTE: there might even be two PRUs hidden inside (not mentioned in general specs)
  - "two gigabit dual-core Programmable Real-Time Unit [...] (PRU_ICSSG)"
  - looks like R5FSS in [MCU Domain](https://docs.beagleboard.org/latest/_images/soc-block-diagram.svg)

## Info

- [Product Page](https://www.beagleboard.org/boards/beaglebone-ai-64)
- [GitRepo](https://git.beagleboard.org/beagleboard/beaglebone-ai-64/-/environments)
  - Schematics and Manual inside
- [Images](https://rcn-ee.com/rootfs/ubuntu-arm64-22.04-console-v5.10-ti/)
- [Headers-Pinouts](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/04-connectors-and-pinouts.html)
- [Forum](https://forum.beagleboard.org/tag/bbai64)
  - [how to overlay device tree](https://forum.beagleboard.org/t/how-to-overlay-device-tree-on-beaglebone-ai-64-board/35134)
  - [pru basics](https://forum.beagleboard.org/t/ai64-pru-basics-very/32288/8)
  - [pin_mux_table](https://forum.beagleboard.org/t/bbai-64-pinmux-spreedsheet/32418)
  - [Cortex R5 Example](https://forum.beagleboard.org/t/minimal-cortex-r5-example-on-bbai-64/32443)

## First steps - eval images

### Ubuntu 22.04.3

Comes with

- linux 5.10.168-ti-arm64-r111
- python 3.10.12

Steps

- update sw
- install kernel-headers
- use `P8.03` ⇾ `GPIO 1 20` or `GPIO0_20`
  - REG 0x00011C054
  - MODE 7 - GPIO0_20

```Shell
# Actuating P8.03
gpioset 1 20=1
gpioset 1 20=0
# SysFS-Way
sudo echo 320 >  /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio320/direction
sudo echo 1 > /sys/class/gpio/gpio320/value
```

SysFS-Derivation

```Shell
######## SYSFS-Approach #################
# following https://forum.beagleboard.org/t/ai-64-gpio-sysfs/32268

gpiodetect
# gpiochip0 [42110000.gpio] (84 lines)
# gpiochip1 [600000.gpio] (128 lines)
# gpiochip2 [601000.gpio] (36 lines)

gpiofind P8_03
# gpiochip1 20

ls -ltr /sys/class/gpio/gpiochip*
# /sys/class/gpio/gpiochip428 ⇾ ../../devices/platform/bus@100000/bus@100000:bus@28380000/42110000.gpio/gpio/gpiochip428
# /sys/class/gpio/gpiochip264 ⇾ ../../devices/platform/bus@100000/601000.gpio/gpio/gpiochip264
# /sys/class/gpio/gpiochip300 ⇾ ../../devices/platform/bus@100000/600000.gpio/gpio/gpiochip300

# P8_03 is on gpiochip1 ⇾ chip1 = 600000.gpio ⇾ 600000.gpio = /sys/class/gpio/gpiochip300
# P8_03 = 320 (value to export)
```

Looking for solutions presents a possible fix

```Shell
# problem: https://github.com/beagleboard/arm64-mainline-linux/issues/7
# FIX: https://forum.beagleboard.org/t/bb-ai64-gpio-basics/36032/6?u=alex_park
# Referenced File: https://github.com/beagleboard/BeagleBoard-DeviceTrees/blob/v5.10.x-ti-arm64/src/arm64/k3-j721e-beagleboneai64-bone-buses.dtsi
git clone https://github.com/beagleboard/BeagleBoard-DeviceTrees.git
cd BeagleBoard*
git checkout v5.10.x-ti-arm64
# ... (instead of default v5.10.x-ti-unified)
make all_arm64
sudo make install_arm64
# cp -v src/arm64/*.dtb /boot/dtbs/5.10.168-ti-arm64-r112/ti/
# NOTE: .dtsi-file gets not compiled directly, but is included by several .dts-files
sudo reboot
```

Watching the UART0-Output (J3 / Debug-Header) tells us that

  k3-j721e-beagleboneai64.dtb is loaded


```
[  461.349258] watchdog: watchdog0: watchdog did not stop!
[  461.819578] reboot: Restarting system

U-Boot SPL 2021.01-g3419da0b (Jan 13 2022 - 15:29:57 +0000)
Model: Texas Instruments K3 J721E SoC
Board: BBONEAI-64-B0- rev B0
SYSFW ABI: 3.1 (firmware rev 0x0015 '21.5.0--v2021.05 (Terrific Llam')
Trying to boot from MMC1
init_env from device 17 not supported!
Starting ATF on ARM64 core...

NOTICE:  BL31: v2.5(release):e0d9fdb
NOTICE:  BL31: Built : 20:08:51, Jan  7 2022

U-Boot SPL 2021.01-g3419da0b (Jan 13 2022 - 15:29:57 +0000)
Model: Texas Instruments K3 J721E SoC
Board: BBONEAI-64-B0- rev B0
SYSFW ABI: 3.1 (firmware rev 0x0015 '21.5.0--v2021.05 (Terrific Llam')
ti_i2c_eeprom_am6_parse_record: Ignoring record id 17
Trying to boot from MMC1


U-Boot 2021.01-g3419da0b (Jan 13 2022 - 15:29:57 +0000)

SoC:   J721E SR2.0
Model: Texas Instruments K3 J721E SoC
Board: BBONEAI-64-B0- rev B0
DRAM:  4 GiB
Flash: 0 Bytes
MMC:   sdhci@4f80000: 0, sdhci@4fb0000: 1
In:    serial@2800000
Out:   serial@2800000
Err:   serial@2800000
ti_i2c_eeprom_am6_parse_record: Ignoring record id 17
Net:   am65_cpsw_nuss_slave ethernet@46000000: K3 CPSW: nuss_ver: 0x6BA00101 cpsw_ver: 0x6BA80100 ale_ver: 0x00293904 Ports:1 mdio_freq:1000000
eth0: ethernet@46000000
Hit any key to stop autoboot:  2 \x08\x08\x08 1 \x08\x08\x08 0
board_name=[BBONEAI-64-B0-] ...
name_fdt=[k3-j721e-beagleboneai64.dtb] ...
i2c_write: error waiting for data ACK (status=0x116)
pca953x gpio@22: Error reading output register
switch to partitions #0, OK
mmc1 is current device
Scanning mmc 1:1...
Found /extlinux/extlinux.conf
Retrieving file: /extlinux/extlinux.conf
705 bytes read in 8 ms (85.9 KiB/s)
BeagleBone AI-64 microSD (extlinux.conf) Options
1:      BeagleBone AI-64 microSD Recovery
2:      BeagleBone AI-64 copy microSD to eMMC
3:      BeagleBone AI-64 microSD (default)
Enter choice: 3:        BeagleBone AI-64 microSD (default)
Retrieving file: /initrd.img
14089271 bytes read in 597 ms (22.5 MiB/s)
Retrieving file: /Image
29618688 bytes read in 1245 ms (22.7 MiB/s)
append: root=/dev/mmcblk1p2 ro rootfstype=ext4 rootwait net.ifnames=0 quiet
Retrieving file: /k3-j721e-beagleboneai64.dtb
226922 bytes read in 18 ms (12 MiB/s)
## Flattened Device Tree blob at 88000000
   Booting using the fdt blob at 0x88000000
   Loading Ramdisk to 8f290000, end 8ffffc37 ... OK
   Loading Device Tree to 000000008f255000, end 000000008f28f669 ... OK

Starting kernel ...

[    0.611800] debugfs: Directory '31010000.pat' with parent 'regmap' already present!
[    0.611991] debugfs: Directory '31011000.pat' with parent 'regmap' already present!
[    0.612108] debugfs: Directory '31012000.pat' with parent 'regmap' already present!
[    0.612238] debugfs: Directory '31013000.pat' with parent 'regmap' already present!
[    0.612370] debugfs: Directory '31014000.pat' with parent 'regmap' already present!
[    1.086487] am65-cpsw-nuss c000000.ethernet: /bus@100000/ethernet@c000000/ethernet-ports/port@1 error retrieving port phy: -19
[    2.983404] debugfs: Directory 'pd:27' with parent 'pm_genpd' already present!
[    2.990666] debugfs: Directory 'pd:26' with parent 'pm_genpd' already present!
[    2.999174] debugfs: Directory 'pd:242' with parent 'pm_genpd' already present!
[    3.006499] debugfs: Directory 'pd:241' with parent 'pm_genpd' already present!
[    3.013814] debugfs: Directory 'pd:240' with parent 'pm_genpd' already present!
[    3.021119] debugfs: Directory 'pd:239' with parent 'pm_genpd' already present!
rootfs: clean, 55075/1864960 files, 711499/7678203 blocks
[    7.772561] k3-dsp-rproc 4d80800000.dsp: configured DSP for remoteproc mode
[    7.846033] remoteproc remoteproc12: request_firmware failed: -2
[    7.858141] k3-dsp-rproc 4d81800000.dsp: configured DSP for remoteproc mode
[    7.887429] remoteproc remoteproc13: request_firmware failed: -2
[    7.921161] k3-dsp-rproc 64800000.dsp: configured DSP for remoteproc mode
[    7.928617] remoteproc remoteproc14: request_firmware failed: -2
[    8.035649] img_enc 4200000.video-encoder: vxe_enc_probe: using heap 1 for internal alloc
[    8.740113] platform 41000000.r5f: configured R5F for IPC-only mode
[    8.791180] platform 41000000.r5f: R5F core initialized in IPC-only mode
[    8.845789] platform 5c00000.r5f: configured R5F for remoteproc mode
[    8.919641] remoteproc remoteproc16: request_firmware failed: -2
[    8.926516] platform 5d00000.r5f: configured R5F for remoteproc mode
[    8.945917] remoteproc remoteproc17: request_firmware failed: -2
[    8.953501] platform 5e00000.r5f: configured R5F for remoteproc mode
[    8.968672] platform 5f00000.r5f: configured R5F for remoteproc mode
[    8.978684] remoteproc remoteproc19: request_firmware failed: -2
[    9.014579] remoteproc remoteproc18: request_firmware failed: -2
```

### Debian 12.2 with 5.10ti

various images panic during boot

### Debian 12.2 min kernel 6.1 ti

Comes with

- linux 6.1.46-ti-arm64-r13
- python 3.11.2

GPIO also NOT working. ⇾ try device-tree fix - 5.10-branch?

there are also images (mainline) with RT and kernel 6.6 / 6.7

### Debian 12.2 xfce kernel 6.6 rt

- 6.6.0-rt-arm64-k3-r13

SysFS-Derivation (changed here)

```Shell
######## SYSFS-Approach #################
# following https://forum.beagleboard.org/t/ai-64-gpio-sysfs/32268

gpiodetect
# gpiochip0 [42110000.gpio] (84 lines)
# gpiochip1 [600000.gpio] (128 lines)
# gpiochip2 [601000.gpio] (36 lines)

gpiofind P8_03
# gpiochip1 20

ls -ltr /sys/class/gpio/gpiochip*
# /sys/class/gpio/gpiochip724 ⇾ ../../devices/platform/bus@100000/601000.gpio/gpio/gpiochip724
# /sys/class/gpio/gpiochip512 ⇾ ../../devices/platform/bus@100000/bus@100000:bus@28380000/42110000.gpio/gpio/gpiochip512
# /sys/class/gpio/gpiochip596 ⇾ ../../devices/platform/bus@100000/600000.gpio/gpio/gpiochip596

# P8_03 is on gpiochip1 ⇾ chip1 = 600000.gpio ⇾ 600000.gpio = /sys/class/gpio/gpiochip596
# P8_03 = 616 (value to export)
```

```Shell
sudo echo 616 >  /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio616/direction
sudo echo 1 > /sys/class/gpio/gpio616/value
```

Does not work!

Shepherd-Kernel-Module now also configures MUX ⇾ GPIO works there, AFTER running once:

```Shell
gpioset 1 20=1
```

xfce or other service throws higher interrupts

```Shell
sudo apt purge alsa-utils btrfs-progs can-utils cloud-guest-utils
sudo apt purge firmware-atheros firmware-brcm80211 firmware-iwlwifi wireless-tools vim
sudo apt purge xfdesktop4
sudo apt purge bluetooth bluez gnome-system-tools mesa-utils-extra tightvncserver
sudo apt purge novnc xserver-xorg-video-fbdev libxfce4ui-utils xfce*
sudo apt purge xfconf xfwm4 qt5ct firefox-esr
sudo apt purge powervr-firmware mender-client nginx pastebinit pciutils bb-code-server bbb.io-xfce4-desktop docker*
sudo apt purge wireplumber* pipewire*
sudo apt purge plymouth*
sudo apt purge dnsmasq nginx* gnupg hexedit hostapd iw less libiio* wireguard*
sudo apt purge wpasupplicant wireless* ofono rfkill acpid libasound* eject

sudo apt purge linux-firmware cron

sudo apt autoremove
# minimal ubuntu stats: 2.4gb space, 116 MB ram
#                after: 1.4gb        107 MB
```

process-view is now much shorter, and ram-usage down to 90 MB.



### Debian bullseye XFCE image 2022-01-14 (on eMMC)

- 5.10.90-ti-arm64-r28 #1bullseye SMP PREEMPT Thu Jan 13 15:02:48 UTC 2022 aarch64 GNU/Linux
- Python 3.9.2

Gpioset and SYSFS work out-of-the-box!

### Debian-11.8-minimal-arm64-2023-12-03-4gb_510ti

- 5.10.168-ti-arm64-r112
- Python 3.9.2

Apply manual DT-Fix
Install gpiod (& htop)

```Shell
sudo apt install gpiod htop
```

Now both works

Additional Steps for PTP-Eval-Testrun:
- remove & update software (shown above)
- playbook bootstrap (add user jane, pwless access, root w/o pw)
- playbook setup_nw_mac_dhcp_id.yml
- install linuxptp, add service-cfg from shepherd

```shell
sudo apt install linuxptp ntpdate
git clone https://github.com/nes-lab/shepherd.git
cd shepherd
git checkout Kernel510
git pull
sudo cp shepherd/deploy/roles/ptp_host/files/* /etc/systemd/system/
# nano /etc/linuxptp/ptp4l.conf
# ⇾ switch "slaveOnly  1" to disable server-cap

sudo systemctl disable systemd-timesyncd
sudo systemctl stop systemd-timesyncd
# sudo systemctl stop gpsd.socket
# sudo systemctl stop chrony.service

sudo systemctl status phc2sys@eth0.service
sudo systemctl status ptp4l@eth0.service

sudo systemctl enable phc2sys@eth0.service
sudo systemctl enable ptp4l@eth0.service

# both helpful
sudo journalctl -u ptp4l@eth0.service -b -f
sudo journalctl -u phc2sys@eth0.service -b -f

# Semi-working config - same for server & clients
ExecStart=/usr/sbin/phc2sys -rr -w -s %I -E linreg
ExecStart=/usr/sbin/ptp4l -A -H -f /etc/linuxptp/ptp4l.conf -i %I
# NEW: /etc/linuxptp/ptp4l.conf ⇾ clock_servo linreg

# new for client
ExecStart=/usr/sbin/phc2sys -r -w -s %I -E linreg
sudo nano /etc/linuxptp/ptp4l.conf ⇾ slaveOnly 1, pi-servo

# new for server
ExecStart=/usr/sbin/phc2sys -a -rr -E linreg
sudo nano /etc/linuxptp/ptp4l.conf ⇾ slaveOnly 0, pi-servo
```

- install kernel module

```shell
uname --kernel-release
sudo apt install linux-headers-5.10.168-ti-arm64-r113
sudo systemctl set-default multi-user
sudo systemctl disable graphical.target
sudo systemctl stop graphical.target

cd shepherd/software/kernel-module/src/
cp pru_sync_control_ai64.c pru_sync_control.c
make
sudo make install
ls /lib/modules/5.10.168-ti-arm64-r113/extra/
sudo depmod -a
sudo modprobe -a shepherd
sudo nano /etc/modules +>> shepherd
```

- prepare a Traffic-generator

```Shell
#sudo apt install flowgrind
sudo apt install iperf3

iperf3 -s
iperf3 -b 100M -c sheep65
```

- activate passthrough of gpio

```
sudo gpioset 1 20=1
```

- debugging

```Shell
sudo systemctl restart phc2sys@eth0.service
sudo systemctl restart ptp4l@eth0.service
sudo journalctl -u phc2sys@eth0.service -b -f
sudo journalctl -u ptp4l@eth0.service -b -f
```


- PPS-Signal is now on P8_03
- GND is on P8_01 & P8_02


## Shepherd-Eval

Compiling and activating the Shepherd-KMod

```Shell
[  +0.000002] shprd.k: Benchmark high-res busy-wait Variants
[  +0.000103] shprd.k: ktime_get() = 2463 n / ~100us
[  +0.000102] shprd.k: ktime_get_real() = 2352 n / ~100us
[  +0.000102] shprd.k: ktime_get_ns() = 2463 n / ~100us
[  +0.000102] shprd.k: ktime_get_real_ns() = 2352 n / ~100us
[  +0.000102] shprd.k: ktime_get_raw() = 2061 n / ~100us
[  +0.000102] shprd.k: ktime_get_real_fast_ns() = 1960 n / ~100us
```

⇾ requesting kernel-time only takes ~40 ns, compared to 300 ns on BBB.
⇾ 100k loop-iterations take 400 us
⇾ same results for kernel 5.10ti and 6.6rt

Getting direct GPIO access for P8_03.

- Line is located in `gpiochip1 [600000.gpio] (128 lines)`
- SPRUIL1C tells us memory map: start @ 0x600000, end @ 0x6000FF, size 256 B
  - page 126
- pinout-guide speaks of: REG 0x11C054
  - memory maps shows: CTRL_MMR0_CFG0, start @ 0x100000, end @ 0x11FFFF, size 128 KB
  - registers1.pdf links REG to CTRLMMR_PADCONFIG21
  - this is the mux-register! writing 7 to MUXMODE bit[3:0] should enable gpio
- J721E_registers4.pdf shows direct gpio-access
  - set: bit 20 in 0x600018
  - clear: x60001C

Setting MuX-Register

1 0 0 0 0 0 1 00 0 0 1 0 1 000 00000 00 0111
⇾ compare with J721_registers1.pdf, page 1108
- set Mode 7, bit[3:0] = 7
- activate RX, bit[18] = 1
- Activate TX, bit[21] = 0


## observations

- system-heatsink is pretty toasty at idle (~55°C)
- iterates up to remoteproc19
- no RT-Kernel yet
