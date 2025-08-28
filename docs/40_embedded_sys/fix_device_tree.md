# Fix Shepherd Device Tree Drivers

Original DT-Driver from shp v1 fails to work with 4.19 or newer.

## Device Tree Versions

- v4.14.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/4a9c0a652f58090491319d27dac4bf76da7d6086
- v4.19.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/af07ef77cc6f8f94568a4c238cc6d41fb8c81931
- v5.4.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/26b4c9fea3ff919835ba27393d5781ca4dd0923f
- overlays: https://github.com/RobertCNelson/bb.org-overlays/tree/master/src/arm

## Changes to reference DT-overlays

- compatible with v4.14.x: "ti,beaglebone", "ti,beaglebone-black"
- newer dts files only speak of "ti,am335x-bone-black", "ti,am335x-bone-green", "ti,am335x-bone", "ti,am33xx"
- pinctrl-single,pins
    - shprd:    0x034 0x06  /* P8.11, pr1_pru0_pru_r30_15 */
    - bbuniv:   AM33XX_IOPAD(0x0834, PIN_OUTPUT | INPUT_EN | MUX_MODE6)
- exclusive-use seems fine
- target pruss overlay ⇾ fine
- overlay is not announcing itself in fragment@0

## Shepherd Firmware

- ``make && sudo make install`` in device-tree sub-folder
- install in ``/lib/firmware/``
- check status in ``/proc/device-tree/chosen/overlays/``
    - or via: ``sudo /opt/scripts/tools/version.sh | grep UBOOT``

### Workflow

```Shell
cd ~/
git clone https://github.com/nes-lab/shepherd
cd shepherd/software/firmware/device-tree
make && sudo make install
# add to /boot/uEnv.txt
# check after reboot if loaded
sudo /opt/scripts/tools/version.sh | grep UBOOT
```

### Backup Image

```Shell
sudo mount /dev/sda1 /media
sudo dd if=/dev/mmcblk1 of=/media/mmc_s0_v4.19.94_bootstrap_apt.img
sudo umount /media

# alternative to local sd-card
sudo dd if=/dev/mmcblk1 of=/dev/mmcblk0
```

### Delete Kernel-Image on MMC

```Shell
sudo mount /dev/mmcblk1p1 /media
cd /media/lib/modules/.../extra
sudo rm shepherd.ko

# better way: do not load module on startup
sudo nano /etc/modules
```
