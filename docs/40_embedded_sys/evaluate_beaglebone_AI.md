# BeagleBone AI Eval

Update from 2024: the board was silently discontinued and vanished from earth, probably due to the various problems.

## Images

- Best Image: am57xx eMMC flasher ubuntu console, 2 GB, <https://elinux.org/BeagleBoardUbuntu#eMMC:_BeagleBoard-X15_and_BeagleBone_AI>
- Better Image: am57xx eMMC flasher debian iot, 4 GB, <https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Debian_Buster_IOT_Snapshot>
        - untested alternative: debian console, sub 1 GB
- Wrong Image: am57xx debian IoT am5729, 8 GB unpacked, <http://beagleboard.org/latest-images>

## Install

- "boot" button is gone, but image flashes automatically (LED Larson-Scanner, until finished with copy, then static)
- ubuntu 18.04.4-console-armhf-2020-03-12
  - **Warning**: CPU gets very hot, even whole PCB, 66 °C idle, 77 °C after apt upgrade
  - takes about 1.2 GB of the 15 GB eMMC
  - dmesg reports 24.59 BogoMIPS (BBG shows 995?!?)
  - uname: 4.19.94-ti-r36
  - dd if=/dev/zero of=./testfile bs=100M count=1 oflag=direct ⇾ 73 MB/s (x3.5 of BBG)
  - GBE works with Cat 5e, 5m
  - 2nd AI shows "sudo hexdump -C /dev/mmcblk1boot1" ⇾ .U3.BBONE-AI00A1 | 1933EMAI000015 ⇾ board 15
- ansible: bootstrap, install, setup_linux_configuration, _performance, _security
  - uname: 4.19.94-ti-r51
  - uname: 5.4.24-armv7-x20 ⇾ not booting

## Oddities

- some restarts are not coming back & there are random shutdowns
- cpu stays boiling hot, even with 99.6% idling, governor set to powersave, tested:
  - ubuntu 18.4.4 from elinux, with 4.19.94-r36 & r51
  - debian 10.4 iot from elinux, with 4.19.94-r41?
  - debian 10.4 console ⇾ does not even flash
  - debian 10.3 iot from bb.org with 4.19.94-r42
  - debian 9.12 console from elinux with 4.14.108-r134 stays at 50 deg ⇾ only one distro?!?
- ram only shows 578 MB ?!? it should be 1 Gig
  - DSP reserves 300 MB+
  - get ram back: <https://groups.google.com/g/beagleboard/c/-kDcIPsLCkc/m/xHyrFKepAgAJ>
- there is no device-tree overlay yet, just a big monolithic dts
- forum-post: it is easy to kill a cpu with wrong pin-inputs, <https://groups.google.com/forum/embed/?place=forum/beagleboard&showsearch=true&showpopout=true&showtabs=false&hideforumtitle=true&parenturl=http%3A%2F%2Fbeagleboard.org%2Fdiscuss#!category-topic/beagleboard/beaglebone-ai/fzwYWLDrQJw>
  - some pins are connected to two balls on the CPU, but io-use must be mutual exclusive
- PRU-Changes ⇾ ll /sys/class/remoteproc/ ⇾ remoteproc4 to remoteproc7
- addresses in RAM changed most likely as well

## Documentation

- nice pin-overview <https://docs.google.com/spreadsheets/d/1fE-AsDZvJ-bBwzNBj1_sPDrutvEvsmARqFwvbw_HkrE/edit#gid=1518010293>
- nice to distinguish BB-Models: cat /proc/device-tree/model ⇾ BeagleBoard.org BeagleBone AI
- device tree is raw, see <https://www.elinux.org/EBC_Exercise_41_Pin_Muxing_for_the_AI>
  - AI.dts <https://github.com/beagleboard/BeagleBoard-DeviceTrees/blob/v4.19.x-ti-overlays/src/arm/am5729-beagleboneai.dts>
  - overlays, general: <https://github.com/beagleboard/bb.org-overlays>
- AI survival guide: <https://www.element14.com/community/community/project14/visionthing/blog/2019/11/16/beagleboard-ai-brick-recovery-procedure>
- AI reference manual: <https://github.com/beagleboard/beaglebone-ai/wiki/System-Reference-Manual>
  - says that out rev A1 is prototype, even A1a is alpha pilot run
- show temp from internal sensors: watch /opt/scripts/device/x15/test_thermal.sh
- included Processors
  - 2x cortex a15
  - 2x C66 DSP, FP VLIW with openCL, TMS320C66x
  - 4x Cortex-M4
  - 4x PRU
  - 4x EVE, embedded vision engines
  - dual core powerVR SGX544 3d GPU
  - vivante GC320 2D graphics accelerator

## TODO

- save power
- turn off not needed processors,
- unload (lsmod) wifi, bt, media (videodev, v4l2), videobuf, vpdma, ti_csc
- apt: bb-node-red-installer
