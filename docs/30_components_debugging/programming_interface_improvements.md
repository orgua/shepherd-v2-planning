# Programming Interface to Target

**TLDR**: 4 programming pins to target are a good choice. enables JTAG or two MCU with SBW / SWD.

## OpenOCD and Patches from Kai

- latest patch / fix: OpenOCD seems to poll when still active after programming ⇾ higher IO-Traffic
- bring OpenOCD-Patches to mainline
- Comments for PatchSet before merging: https://review.openocd.org/c/openocd/+/4671
- full repo: https://sourceforge.net/p/openocd/code/ci/master/tree/

## Solutions for wider variety of Targets

- Idea
    - currently only SWD-Compatible ICs are supported (nRF)
    - support more than 1 IC on the target-board would be preferred (ie. msp-storage + nRF-radio)
- IC-Variety: nRF52 (DFU / USB, SWD), STM32L4 (SWD), MSP430 / 432 & CC430 (JTAG, Serial, USB, Spy-By-Wire)
- Programming-Standards
    - SWD
        + already working with OpenOCD on BBG via bitbanging
        - PRU of BBG as Programmer already exists - https://beagleboard.org/p/gniibe/bbg-swd-93bcea
    - SpyBiWire (SBW)
        + TI offers code for using MSP430 as a Programmer
        + basically JTAG with a different PHY, Main talks on ClkHigh, Client on ClkLow
        - timing constraints probably make bitbanging in Linux impossible (<= 7us clk-cycle)
        - ⇾ most efficient way would be to use PRU + custom abstraction layer to run MSP-Code ⇾ PRU needs to access GPIO-Unit of System
    - JTAG
        - 4 Wire Version preferred to keep wiring to a minimal
        - would come for free when 2x2 Programming pins go to each target
        - should also be possible to bitbang via OpenOCD, https://forum.43oh.com/topic/10035-4-wire-jtag-with-mspdebug-and-raspberry-pi-gpio/
- Implementation Variants
    - (as before) Two Lines to Target
        - target-board is responsible for solution
        - analog switch on target-pcb for programming lines, controlled by one of the gpio (should be exclusive)
    - SYS ⇾ 2x2 Lines to Target
        - mostly software-defined and very versatile
        - would allow JTAG & SWD via OpenOCD and SBW via custom PRU-Code
    - SYS ⇾ UART ⇾ intermediate uC ⇾ 2x2 Lines to Target
        - firmware could just be dumped by UART
        - Needs the most custom Code & Debugging would be hard to achieve

## TargetConnector-Modifications for HW v2.3 (Proposal)

- make programming pins officially exclusive for programming ⇾ no logging via PRU
- add second pair of programming pins to target
- extend GPIO count from 7 to 9 (now free on pru) also counting the uart-pins (that could also work as GPIO)
- concrete changes
    - connector grows from 2x7 Pins to 2x9 Pins
    - connector needs to shrink to RM2.0 or lower
    - additional BOM: two analog-switches and some resistors needed
- space constraints on board get serious! ⇾ Solutions
    - make board some mm wider
    - use SMD-Header to BB
    - more expensive manufacturing with smaller vias

## PRU-Programmer-Framework

### python frontend

Sheep supports new command ``shepherd-sheep programmer``

- example: ``sudo shepherd-sheep -vv programmer -p sbw ./build.hex``
- program enables shepherd-cape, io, target-port, desired voltage
- copies fw to ram
- configures programmer-struct

### Sysfs-Api

Files in `/sys/shepherd/programmer/`

Should be written after filling ram area with firmware - specially the state-attribute.

| File           | Description                                                                                                           |
|----------------|-----------------------------------------------------------------------------------------------------------------------|
| `./state`      | write "start" or "stop" and get current states ("idle", "running", [..], "error") ⇾ **write at last!**                |
| `./protocol`   | write swd, sbw or jtag                                                                                                |
| `./datarate`   | in baud, currently limited in kernel-module to 10 MBaud                                                               |
| `./datasize`   | in byte                                                                                                               |
| `./pin_%name%` | pin_tck (clock), data in (pin_tdio), data out (pin_tdo), mode (pin_tms), currently limited to 10'000 in kernel-module |


## PRU0

Includes programmer.c and jumps into programmer()-fn when "state" != IDLE or ERROR. The current demo checks firmware-struct, tinkers with the ctrl-struct and flashes the LED of the external button

## TODO

- implement variable pin-choice (4 banks á 32 pins ⇾ 128 n)
- plausibility-check of programmer-struct in kernel-module / sysFS before allowing "start"
- firmware-size is probably more useful in sysfs
- generalize concept, ideas documented [here](https://github.com/nes-lab/shepherd/issues/23)
