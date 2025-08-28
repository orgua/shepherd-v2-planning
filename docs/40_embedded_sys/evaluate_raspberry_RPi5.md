# Raspberry RPi5

- Board is ~ 2.5x the performance of BB-AI64
- RPi4 & RPi5 have hardware-timestamping
- various RAM configurations (no eMMC anymore)

## Info

- [getting started](https://www.raspberrypi.com/documentation/computers/getting-started.html)
- [linux images](https://www.raspberrypi.com/software/operating-systems/)
  - Pi OS 64-bit lite available (~400 mb)
  - NOTE: while CM4 was tested with Kernel 6.1, the current version uses v6.6

## Eval

- Pi OS Lite, 64-bit, Kernel 6.6, debian 12 bookworm
    - flashed to uSD-Card with RPi Imager
    - **hostname: sheep50 - sheep52**
    - **user: jane, temppwd**
    - **enable ssh with pw**
- Powered via USB Type C & Power-Brick
- Platform is definitely hot to the touch, compared to CM4
  - cam shows 56..60 deg C for idle
  - new power converters seem to run hot also

Connect via

```shell

```

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
# take output & modify
sudo apt install linux-headers-6.6.20+rpt-rpi-2712
sudo apt install build-essential

sudo apt install iperf3 linuxptp ntpdate
```

Remove more overhead

```Shell
sudo nano /boot/firmware/config.txt

# change (includes commenting-out lines)
  # dtparam=audo=on
  camera_auto_detect=0
  display_auto_detect=0
  # dtoverlay=vc4-kms-v3d
  otg_mode=0
# add
  hdmi_blanking=2

# ram usage down to 72 mb with < 20 programs running
```

try to preserve power

```Shell
sudo nano /boot/firmware/config.txt

#dtoverlay=vc4-kms-v3d
max_framebuffers=0
dtoverlay=disable-wifi
dtoverlay=disable-bt
dtoverlay=disable-wifi-pi5
dtoverlay=disable-bt-pi5
# under-clocking, ref = 2400
#arm_freq=2200
# under-volting
over_voltage_delta=-10000
```

```Shell
nano /boot/firmware/cmdline.txt

maxcpus=2
```

reboot and compare to before

```shell
sudo reboot
```


### Comparison

```shell
> df -h
/dev/mmcblk0p2   29G  1.7G   26G   7% /
/dev/mmcblk0p2   29G  1.4G   26G   6% /

> top
204 MiB Ram Used, 145 Tasks
163 MiB Ram Used, 126 Tasks

> htop
118M Ram used, 24 Tasks
91M Mem used, 17 Tasks
```

### Testing gpio

- `raspi-gpio` used for CM4 is now deprecated
- `pinctrl` is recommended, interface is similar



- `pinctrl get` prints the state of all GPIO pins
- `pinctrl get X` prints the state of GPIO pin X
- `pinctrl set X op` sets GPIO pin X as an output
- `pinctrl set X dh` sets GPIO pin X to drive high
- `pinctrl set X dl` sets GPIO pin X to drive low

- going for GPIO21, last one on the connector
- J8-P40: GPIO21 (upper right corner)
- J8-P39: GND (lower right corner)

```Shell
sudo pinctrl
# 21: no    pd | -- // GPIO21 = none
# 121: ip    pd | lo // 2712_G21_FS/GPIO21 = input
sudo pinctrl set 21 op dl
sudo pinctrl set 21 op dl
```

It works!

### Determine Address of GPIO21 in Memory

```Shell
sudo gpiodetect
# gpiochip0 [gpio-brcmstb@107d508500] (32 lines)
# gpiochip1 [gpio-brcmstb@107d508520] (4 lines)
# gpiochip2 [gpio-brcmstb@107d517c00] (17 lines)
# gpiochip3 [gpio-brcmstb@107d517c20] (6 lines)
# gpiochip4 [pinctrl-rp1] (54 lines)

sudo gpiofind GPIO21
# gpiochip4 21

ls -ltr /sys/class/gpio/gpiochip*
# /sys/class/gpio/gpiochip571 -> ../../devices/platform/axi/1000120000.pcie/1f000d0000.gpio/gpio/gpiochip571
# /sys/class/gpio/gpiochip565 -> ../../devices/platform/soc/107d517c00.gpio/gpio/gpiochip565
# /sys/class/gpio/gpiochip548 -> ../../devices/platform/soc/107d517c00.gpio/gpio/gpiochip548
# /sys/class/gpio/gpiochip544 -> ../../devices/platform/soc/107d508500.gpio/gpio/gpiochip544
# /sys/class/gpio/gpiochip512 -> ../../devices/platform/soc/107d508500.gpio/gpio/gpiochip512

# by comparing raw addresses (4x 107d5###) we can guess that
# gpiochip4 = gpiochip571, x1000120000 or **0x1f000d0000**
```

BCM2712 + RP1
-> Datasheet for BCM not published yet, but
-> https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf

#### RP1

##### chapter 3.3 RIO

`RIO_OUT` -> Output drive
`RIO_OE` -> Output drive enable

##### Chapter 3.3.2

sys_rio0 @0x400e0000
normal rw           -> addr + 0x0000
atomic XOR on write -> addr + 0x1000
atomic bitmask set  -> addr + 0x2000
atomic bitmask clear-> addr + 0x3000

##### Kernel Module

https://github.com/raspberrypi/linux/blob/rpi-6.6.y/drivers/pinctrl/pinctrl-rp1.c
```c
#define RP1_RIO_OUT			0x00
#define RP1_RIO_OE			0x04
#define RP1_RIO_IN			0x08

struct rp1_pin_info {
	u8 num;
	u8 bank;
	u8 offset;
	u8 fsel;
	u8 irq_type;

	void __iomem *gpio;
	void __iomem *rio;
	void __iomem *inte;
	void __iomem *ints;
	void __iomem *pad;
};

static int rp1_get_dir(struct rp1_pin_info *pin)
{
	return !(readl(pin->rio + RP1_RIO_OE) & (1 << pin->offset)) ?
		RP1_DIR_INPUT : RP1_DIR_OUTPUT;
}
```

another approach is https://github.com/raspberrypi/utils/blob/master/pinctrl/gpiochip_rp1.c



### add Kernel Module

```shell
sudo apt install git
git clone https://github.com/nes-lab/shepherd
cd shepherd/software/kernel-module/src/
git checkout Kernel66RPi5

make
sudo make install
ls /lib/modules/6.6.20+rpt-rpi-2712/extra/
# module present

sudo depmod -a
sudo modprobe -a shepherd
sudo nano /etc/modules +>> shepherd
# to remove:
sudo modprobe -rf shepherd
```
