# TimeSync Revisit 2023

There are currently three problems with synchronization:

- (1) PTP seems to miss-align the clock from time to time when cpu is under load (rings for 10-20 seconds)
- (2) kernelspace hr-timer are not that precise ⇾ can overshoot 20++ usec
- (3) sync-loop between kernel and PRU is oscillating (~ 0.2 Hz, +- 400 nsec)

Context:

- problem 2 & 3 are minor when using shepherd as designed
- problem 2 is noticeable when generating a gpio-edge in kernel

## How to analyze

A logic analyzer that observes the gpio-output plus a some [python code](https://github.com/nes-lab/shepherd/tree/dev/software/test_timesync) allow to analyze performance.

## Fixes for Problem 1 - PTP under load

- switch to RT-Kernel ⇾ downside: higher load, up to 20 % for shepherd
- give PTP & phc2sys higher prio

observations:

- switch is primary factor of quality

### Check HW-Timestamping

as suggested [here](https://forum.beagleboard.org/t/beaglebone-black-hardware-timestamping-with-5-10-ti-rt-kernel-using-omap-image-builder/31031/11)

```Shell
sudo apt install ethtool
uname -r
# 4.19.94-ti-rt-r74
ethtool -T eth0
#
Time stamping parameters for eth0:
Capabilities:
        hardware-transmit     (SOF_TIMESTAMPING_TX_HARDWARE)
        software-transmit     (SOF_TIMESTAMPING_TX_SOFTWARE)
        hardware-receive      (SOF_TIMESTAMPING_RX_HARDWARE)
        software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)
        software-system-clock (SOF_TIMESTAMPING_SOFTWARE)
        hardware-raw-clock    (SOF_TIMESTAMPING_RAW_HARDWARE)
PTP Hardware Clock: 0
Hardware Transmit Timestamp Modes:
        off                   (HWTSTAMP_TX_OFF)
        on                    (HWTSTAMP_TX_ON)
Hardware Receive Filter Modes:
        none                  (HWTSTAMP_FILTER_NONE)
        ptpv1-l4-event        (HWTSTAMP_FILTER_PTP_V1_L4_EVENT)
        ptpv2-event           (HWTSTAMP_FILTER_PTP_V2_EVENT)
```

TODO: should be verified in general from time to time!

## Fixes for Problem 2 - Kernel HR-Timer

- add busy-wait to trigger gpio exactly (preemt disabled)
  - Observations: longer busy-waits also decrease sync-performance
  - optimization: disable busy-wait, analyze jitter (currently 35us for 99%-quantile)
- lowest bound: getting time (like `ktime_get_real()`) can take 300ns on BBone
  - added a benchmark in sync_init()
- add finer loop-counter-busy-wait
  - BIG FAIL - did not improve performance, but even increased jitter
- upgrade Kernel to 5.10 (from 4.19)
  - FAIL - made reliability of hrtimer much worse
  - HRTIMER_MODE_ABS shows missing gpio-edges during operation
  - UNSOLVED MYSTERY:
    - switching back to 4.19 still shows higher jitter (but it should be minimal)
    - also: PINNED & HARD are available, but shouldn't (ti-rt-mod)
    - full kModule with _ABS (confirmed soft) has too good performance
- tune hrtimer
  - hres-mode already active
  - least jitter (best first): HRTIMER_MODE_ABS_HARD, HRTIMER_MODE_ABS_PINNED_HARD, HRTIMER_MODE_ABS

TODO:
- change prio of kernel module?

```shell
make
sudo make install
sudo shepherd-sheep fix
sudo shepherd-sheep pru sync
sudo systemctl restart ptp4l@eth0
```

```Shell
# Downgrade Kernel
/opt/scripts/tools/update_kernel.sh --lts-4_19
# linux-image-4.19.94-ti-rt-r74
ll /lib/modules/4.19.94-ti-rt-r74/extra/
# 56936 bytes

# update Kernel
/opt/scripts/tools/update_kernel.sh --lts-5_10
# linux-image-5.10.168-ti-rt-r73
sudo apt install linux-headers-5.10.168-ti-rt-r73
# additional changes
sudo systemctl stop shepherd-launcher
nano /boot/uEnv.txt ⇾ disable uboot_overlay_pru= & dtb_overlay=
  uboot_overlay_pru=AM335X-PRU-UIO-00A0.dtbo
  enable_uboot_cape_universal=1
sudo nano /etc/modprobe.d/pruss-blacklist.conf
    # following https://catch22eu.github.io/website/beaglebone/beaglebone-pru-uio/
    # regarding newer sources this is NOT needed
    blacklist pruss
    blacklist pruss_intc
    blacklist pru-rproc

ll /lib/modules/5.10.168-ti-rt-r73/extra/
# 12460 bytes
sudo depmod -a
sudo modprobe -a shepherd
sudo lsmod
sudo modprobe -rf shepherd
```

```shell
# gpio-allocation via device-tree is still broken
sudo su
echo 22 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio22/direction
# now activate kernel module
# when other device trees are active we have to switch to available pin P8_17 (gpio27)
```

Current default Kernel 5.10 RT is much worse at triggering hrtimer

```Shell
                                         name  mean [ns]  q99:1 [ns]  minmax [ns]
37    014_improved_40us_busy_ch0_rising_100ms   11103814         588          692
39   015_kernel510RT_noBusyW_ch0_rising_100ms     495782      941801     99765808
40         016_mode-ABS_HARD_ch0_rising_100ms      -6688      199102       236904
41  017_mode-ABS_PINNED_HARD_ch0_rising_100ms      -6672      215903       238118
42             018_busyW_40u_ch0_rising_100ms      -6687      173760       175886

```

Higher System-Load - Update Python
⇾ does not work (missing libs brought by apt & 3.12 internals crashing)

```Shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
sudo apt install python3.12-distutils, python3.12-dev
python3.12 -m pip install --upgrade pip
sudo update-alternatives --config python3
```

## Fixes for Problem 3 - PRU-sync

TODO

- redesign sync-loop to avoid shortcomings of the system
- bb ai 64 already supports hardware timestamping (ubuntu 22.04, kernel 5.10.168-ti-arm64-r112 ti)
- ptp4l:
  - switch to newer clock servo (linreg instead of pi), [link](https://medium.com/inatech/sync-your-clocks-better-ptp-settings-on-raspberry-pi-37a9a54e4802)
  - ptp4l -i eth0 [--masterOnly 1] -m --tx_timestamp_timeout 200
  - [fedora-guide](https://docs.fedoraproject.org/en-US/fedora/latest/system-administrators-guide/servers/Configuring_PTP_Using_ptp4l/)
  - [redhat-guide](https://www.redhat.com/en/blog/combining-ptp-ntp-get-best-both-worlds)

### Use Kmodule to generate PPS-Signal

Resources:

- https://stackoverflow.com/questions/44930443/how-are-the-steps-to-access-gpios-in-linux-kernel-modules
- http://elinux.org/images/9/9b/GPIO_for_Engineers_and_Makers.pdf
  - `/sys/bus/gpio/devices/gpiochip2`
  - `/sys/bus/gpio/devices/gpiochip2/gpio/gpio65/value`
- https://github.com/jsln/pps-gen-gpio

Solution: write directly to registers

This produced 2 two branches

- [Kernel510](https://github.com/nes-lab/shepherd/tree/Kernel510/software/kernel-module/src): allows direct gpio-access for BBone Black & AI64
- [Kernel61RPi](https://github.com/nes-lab/shepherd/tree/Kernel61RPi/software/kernel-module/src): same for Raspberry PI CM4

## Eval for new platforms

TLDR: A dedicated Software-Analysis and Tutorial is located here: https://github.com/nes-lab/shepherd/tree/dev/software/test_timesync

- there is a [ptp-hat for raspberry](https://hackaday.com/2021/08/16/new-part-day-raspberry-pi-hat-for-ieee1588-precision-time-protocol/) now
- `ethtool -T eth0` shows BB AI 64 is already capable (per software)
- rpi3 still only software timestamping
- Raspberry CM4 and RPI5 should also support hardware timestamping, [link](https://forums.raspberrypi.com/viewtopic.php?t=358275)
  - [two CM4 within 15ns](https://www.jeffgeerling.com/blog/2022/ptp-and-ieee-1588-hardware-timestamping-on-raspberry-pi-cm4)
  - CM4 has quad-core Cortex-A72 ArmV8 64bit @ 1.5GHz (BB AI 64 has dual A72 @ 2 GHz) ⇾ only 28 GPIO though

## Implemented Changes

- every 2 mins clock jumps away on ptp-client (ringing for 10-20s, < 300us)
  - solution: still active sync-services
- box-plot of channel-diffs
- CLI
- improve kMod
    - 30 us capture does not suffice!
    - first non-busy-wait (100us) ⇾ shorter busy-wait (10) ⇾ loop-count (<1)
    - retest timing-performance
    - make
- reduce load (py) - read from PRU
    - sharedMem.read_buffer(): np.frombuffer() ⇾ DataBuffer(voltage, current)
    - shpIO.get_buffer(): buf ⇾ buf
    - ShpEmu.run(): buf ⇾ writer.write_buffer(buf)
    - writer.write_buffer(): add parts of buf to group[]
- name threads & change their prio?
- code from pps-kernel-module
- update kernel and try reduced module

hrv mppt_opt 200s
    54 - 60% cpu load (RT)
    44 - 47%        (r73)
emu (gpio, uart, logg off)
sudo shepherd-sheep run /etc/shepherd/config.yaml
    100% and lots of errors (RT)
    55 - 59 % (r73)
    66 - 71 % (RT) + 5-8 for SYSMon
