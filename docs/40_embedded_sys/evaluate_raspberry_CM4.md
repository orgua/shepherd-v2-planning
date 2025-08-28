# Raspberry CM4

- Board is similar to BB-AI64 regarding performance
- RPi4 & RPi5 have hardware-timestamping
- various RAM and eMMC configurations


## Info

- [first step](https://www.raspberrypi.com/documentation/computers/compute-module.html#setting-up-the-cmio-board)
- [linux images](https://www.raspberrypi.com/software/operating-systems/)
  - Pi OS 64-bit lite available

## Eval

- Pi OS Lite, 64-bit, Kernel 6.1, debian 12 bookworm
    - flashed directly to eMMC (see first steps): add jumper to disable eMMC-Boot, run rpiboot-program and then imager
    - **hostname: sheep40 - sheep42**
    - **user: jane, temppwd**
    - **enable ssh with pw**
- Barrel-Connector can take 7.5 to 28V (if no PCIe is used)
- at rest system draws 136mA @ 10V
  - with disabled BT & WIFI, 122mA @ 10V (J3 - short all 3 Pins)
- Platform seems a lot more up to date than the BB-AI64
  - cpu survives without cooling and is only slightly warm
  - BB-AI64 has a big heatsink and dies if it is places upside down for some minutes



### Update System and remove not needed services

- xfce or other service throws higher interrupts

```Shell
# mostly copied from ai64-notes
sudo apt purge alsa-utils btrfs-progs can-utils cloud-guest-utils
sudo apt purge firmware-atheros firmware-brcm80211 firmware-iwlwifi wireless-tools vim
sudo apt purge xfdesktop4
sudo apt purge bluetooth bluez gnome-system-tools mesa-utils-extra tightvncserver
sudo apt purge novnc xserver-xorg-video-fbdev libxfce4ui-utils xfce*
sudo apt purge xfconf xfwm4 qt5ct firefox-esr
sudo apt purge mender-client nginx pastebinit pciutils docker*
sudo apt purge wireplumber* pipewire*
sudo apt purge plymouth*
sudo apt purge dnsmasq nginx* gnupg hexedit hostapd iw less libiio* wireguard*
sudo apt purge wpasupplicant wireless* ofono rfkill acpid libasound* eject

sudo apt purge cron

sudo apt autoremove
# then update and full-upgrade
sudo apt update
sudo apt full-upgrade

sudo systemctl disable systemd-timesyncd
sudo systemctl stop systemd-timesyncd

sudo systemctl set-default multi-user
sudo systemctl disable graphical.target
sudo systemctl stop graphical.target

# remaining: ModemManager
sudo systemctl disable ModemManager
sudo systemctl stop ModemManager

# RPI-specific
sudo dpkg -l
sudo apt purge vim* systemd-timesyncd rpicam* modemmanager firmware-realtek firmware-misc-non* bluez*
sudo apt purge mkvtoolnix gdb iso-codes libqt5core5a
sudo apt purge linux-image-6.1.0-rpi7-rpi-2712
sudo apt purge exfatprogs firmware-libertas
sudo apt autoremove

# already installed
uname --kernel-release
sudo apt install linux-headers-6.1.0-rpi7-rpi-v8
sudo apt install build-essential

# minimal ubuntu stats: 1.8gb space, 90 MB ram
#                after: 1.5gb        65 MB

sudo apt install iperf3 linuxptp ntpdate
```

Remove more overhead

```Shell
# sudo nano /boot/config.txt
sudo nano /boot/firmware/config.txt

# change (includes commenting-out lines)
  # dtparam=audo=off
  camera_auto_detect=0
  display_auto_detect=0
  # dtoverlay=vc4-kms-v3d
  otg_mode=0
# add
  hdmi_blanking=2

# ram usage down to 72 mb with < 20 programs running
```

### Testing gpio

- `raspi-gpio get` prints the state of all GPIO pins
- `raspi-gpio get X` prints the state of GPIO pin X
- `raspi-gpio set X op` sets GPIO pin X as an output
- `raspi-gpio set X dh` sets GPIO pin X to drive high
- `raspi-gpio set X dl` sets GPIO pin X to drive low

- going for GPIO21, last one on the connector
- J8-P40: GPIO21 (upper right corner)
- J8-P39: GND (lower right corner)

```Shell
sudo raspi-gpio set 21 op dh
sudo raspi-gpio set 21 op dl
```

It works!

### Determine Address of GPIO21 in Memory

```Shell
sudo gpiodetect
# gpiochip0 [pinctrl-bcm2711] (58 lines)
# gpiochip1 [raspberrypi-exp-gpio] (8 lines)

sudo gpiofind GPIO21
# gpiochip0 21

ls -ltr /sys/class/gpio/gpiochip*
# /sys/class/gpio/gpiochip504 ⇾ ../../devices/platform/soc/soc:firmware/soc:firmware:gpio/gpio/gpiochip504
# /sys/class/gpio/gpiochip0 ⇾ ../../devices/platform/soc/fe200000.gpio/gpio/gpiochip0

# ⇾ hints @ something like 0x200000
```

(BCM2711-datasheet](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf)

- 32-bit registers
- gpio register base address 0x7e200000

```
# set gpio21 to output
GPFSEL2[5:3] = 001
# 0x7e200000 + 0x8

GPSET0[21] = 1   # set High
# 0x7e200000+0x1c
GPCLR0[21] = 1   # set Low (clear)
# 0x7e200000+0x28
GPLEV0[21]       # read value
# 0x7e200000+0x34
```

**IMPORTANT NOTE**: GPIO is really at 0xfe200000. Datasheet for the BCM2711 shows 2-stage remapping on page 5


### add Kernel Module

```shell
sudo apt install git
git clone https://github.com/nes-lab/shepherd
cd shepherd/software/kernel-module/src/
git checkout Kernel61RPi

make
sudo make install
ls /lib/modules/6.1.0-rpi7-rpi-v8/extra/

sudo depmod -a
sudo modprobe -a shepherd
sudo nano /etc/modules +>> shepherd
# to remove:
sudo modprobe -rf shepherd
```

### Benchmark

```Shell
[  176.137036] shprd.k: Benchmark high-res busy-wait Variants
[  176.137154] shprd.k: ktime_get() = 713 n / ~100us
[  176.137273] shprd.k: ktime_get_real() = 689 n / ~100us
[  176.137392] shprd.k: ktime_get_ns() = 713 n / ~100us
[  176.137510] shprd.k: ktime_get_real_ns() = 689 n / ~100us
[  176.137629] shprd.k: ktime_get_raw() = 722 n / ~100us
[  176.137747] shprd.k: ktime_get_real_fast_ns() = 777 n / ~100us
[  176.139146] shprd.k: 100000-increment-Loops ⇾ measure-time
[  176.139173] shprd.k: hres-mode: 1
[  176.139191] shprd.k: timer.is_rel = 0
[  176.139208] shprd.k: timer.is_soft = 0
[  176.139224] shprd.k: timer.is_hard = 1
```

- requesting kernel-time with ktime_get_real() takes 145 ns (lowest freq-step)
  - overclocked in performance-mode: 41 ns
- Reference: old BBB takes 300 ns, BB-AI64 takes ~ 40 ns
- NOTE: its the same core as the AI64, is there a powersaving or
⇾ unmodded rpi has 1040 n

### Performance-Improvements

Overclock (eval)

```Shell
sudo nano /boot/config.txt
  over_voltage=6
  ##arm_freq=2140  # 2 GHz is already 33% faster
  arm_freq=2000
```

Check & change governor

```Shell
sudo apt install cpufrequtils
cpufreq-info
sudo cpufreq-set --governor performance
sudo cpufreq-set --governor ondemand
```

120 mA Baseline 1500 MHz
155 mA Overclock 2150 MHz
200 mA Performance mode

```Shell
[  436.756285] shprd.k: ktime_get() = 2546 n / ~100us
[  436.756390] shprd.k: ktime_get_real() = 2458 n / ~100us
[  436.756496] shprd.k: ktime_get_ns() = 2547 n / ~100us
[  436.756601] shprd.k: ktime_get_real_ns() = 2459 n / ~100us
[  436.756707] shprd.k: ktime_get_raw() = 2577 n / ~100us
[  436.756812] shprd.k: ktime_get_real_fast_ns() = 2778 n / ~100us
```

Final-Setting:
- 2000 MHz in `/boot/config.txt`
- Performance-Gov in `/etc/default/cpufr` added to ptp-service

### Eval Sync

Configured PTP4L and Phc2sys like shown in AI64.md, changes from that:

- ptp prio reduced from 99 to 80
- phc prio reduced from x to 70
- set governor to performance in phc-service ExecStartPre `-/usr/bin/cpufreq-set --governor performance`
- ptp4l.conf
  - # run time options
  - tx_timestamp_timeout  1 ⇾ 10
  -
  - # servo options
  - pi_proportional_exponent -0.3 ⇾ ~~-0.5~~
  - pi_integral_exponent 0.4 ⇾ ~~0.2~~ made it faster? 0.4 worked better / slower
    - sync between clients was never that stable (007 ... 1u2)
  - # default interface options
  - delay_filter_length 10 ⇾ 100
- phc2sys
  - P kp 0.7 ⇾ 0.2
  - I Ki 0.3 ⇾ 0.1
