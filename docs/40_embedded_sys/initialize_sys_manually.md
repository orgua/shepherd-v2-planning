# Install custom Shepherd-Code and check install, prior to release



## Install on System

```Shell
sudo git clone https://github.com/nes-lab/shepherd
cd /shepherd
pip install --upgrade ansible
ansible-playbook ./deploy/deploy.yml
```

## Useful on a fresh system

```Shell
sudo chown -R user /opt/shepherd
sudo passwd user
cp /opt/shepherd/software/meta-package/example_config_harvest.yml /etc/shepherd/config.yml
sudo shepherd-sheep -vvv run --config /etc/shepherd/config.yml

cd /opt/shepherd/software/python-package/
sudo python3 setup.py test --addopts "-vvv"
# bump2version --tag patch # ⇾ just hand in PR or hash

# test code on live system
sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml

⇾ done in unit-tests now
sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_harvester.yml
sudo shepherd-sheep -vv run --config /opt/shepherd/software/meta-package/example_config_harvester.yml
sudo shepherd-sheep -vv run --config /opt/shepherd/software/meta-package/example_config_emulator.yml
sudo shepherd-sheep -vv run --config /opt/shepherd/software/python-package/tests/example_config_harvester.yml
sudo shepherd-sheep -vv run --config /opt/shepherd/software/python-package/tests/example_config_emulator.yml


# test suite in /opt/shepherd/software/python-package
cd /opt/shepherd/software/python-package/
sudo python3 setup.py test --addopts "-vv"
dmesg -wH

# allow connection per GUI from remote:
sudo shepherd-sheep rpc

# helpful when build-system was used with sudo
sudo chown -R user ./
```

## Check Components (on sheep)

```Shell
# DT-Overlay: there should be an BB-SHPRD-... ⇾ overlay is active
ll /proc/device-tree/chosen/overlays/

# Custom-Services: should show 3x shepherd entries, only shepherd-launcher.service enabled, also: shepherd-rpc, shepherd
systemctl list-unit-files | grep shep

# Timesync-Services: both should be active and running
systemctl | grep ptp
systemctl | grep phc

# PRUs: two pru-rproc available and probed successfully
dmesg | grep pru

# PRUs: should show remoteproc1 and 2
ll /sys/class/remoteproc/

# KernelModule: it should probably be active - but isn't (sudo modprobe shepherd)
lsmod | grep shep

# KernelModule: should talk "shprd: found device", "found PRU0/1", "PRUs started"
dmesg | grep shp

# KernelModule: ``state`` should exist
ll /sys/shepherd/

# Shepherd program: >
cp /opt/shepherd/software/meta-package/example_config_harvest.yml /etc/shepherd/config.yml
shepherd-sheep -vv run --config /etc/shepherd/config.yml
    ⇾ error, no /sys/shepherd/state
        there is /sys/module/shepherd, without "state"
```

## Debug (on sheep)

```Shell
# KModule autoload in
sudo nano /etc/modules
/lib/modules/$(KVERSION)/extra/shepherd.ko

# manual load fw into pru
/sys/class/remoteproc/remoteprocX/firmware      ⇾ fw-name in lib/firmware/ usually am335x_pru0-shepherd-fw
echo "start" > /sys/class/remoteproc/remoteprocX/state
```

## Test new vSource-Emulator

```
sudo apt install --reinstall exfat-fuse exfat-utils
mkdir /var/shepherd/recordings2
chmod -Rf 777 /var/shepherd/recordings2

sudo mount -t exfat /dev/mmcblk0p1 /var/shepherd/recordings2
# configure the config.yml to point to wanted tracefile:
#   input_path: /var/shepherd/recordings2/indoor_solar/sheep4/office_sd.h5

sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
# cap-voltage is on second target-voltage-pin, bat-ok is on P8-29, CS_ADC_EMU is P9-42

cat /sys/shepherd/

sudo umount /var/shepherd/recordings
```

## Programming Target

**DEPRECATED** - use https://github.com/nes-lab/shepherd-targets

Compile a demo 'https://github.com/geissdoerfer/shepherd-nrf52-demo'

```Shell
sudo apt install gcc-arm-none-eabi
sudo find / -iname arm-none-eabi-gcc

export GNU_INSTALL_ROOT=/usr/bin/
export SDK_ROOT=/home/hans/Downloads/NordicSDK/
make all
```

Prepare target with default: 3V for target 1, with gpio-pass

```Shell
sudo shepherd-sheep -vv target-power --voltage 2.8
```

- installed and configured modded version of openOCD (new playbook)
- fixed cli for 'target-power' and extended herd-tool accordingly

### Herd-steps

```
shepherd-herd target
shepherd-herd start-openocd
shepherd-herd target flash build.hex

program /tmp/target_image.bin verify reset
```

### Start by hand

```
# installed in /etc/systemd/system/
sudo systemctl start shepherd-openocd.service

# cfgs in /usr/share/openocd/scripts/interface/
sudo /usr/bin/openocd -c "bindto 0.0.0.0" -f interface/beaglebone.cfg -f interface/shepherd.cfg -c "transport select swd" -f target/nrf52.cfg
sudo /usr/bin/openocd -d -c "bindto 0.0.0.0" -f interface/beaglebone.cfg -f interface/shepherd.cfg -c "transport select swd" -f target/nrf52.cfg
sudo /usr/bin/openocd -d -f interface/beaglebone.cfg -f interface/shepherd.cfg -c "transport select swd;telnet_port pipe;log_output /dev/null" -f target/nrf52.cfg

# check if it runs:
sudo netstat -apn | grep LISTEN
```

Success!! When Target is directly connected

```
shepherd-herd target flash build.hex
```

Flashed "powered" demo with 9600-baud serial and proper pin-config!

## UART to Target

- Image sets baudrate to 9600
- pins had to be disabled in device-tree P9-24/26
- uEnv.txt had to load uart1

```Shell
sudo stty -F /dev/ttyS1 9600
sudo cat /dev/ttyS1
```

Spits out text by manually triggering pins:

```
1 triggered

  is outside of range of supported pins (7)
```

## Tests for preparing software-release

- use a fresh ubuntu lts host and newest fresh ubuntu image for BB
- follow install instructions (install ansible, bootstrap, deploy)
- let pytests run
