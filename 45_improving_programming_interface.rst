Programming Interface to Target
===============================

OpenOCD and Patches from Kai
----------------------------
- latest patch / fix: OpenOCD seems to poll when still active after programming -> higher IO-Traffic
- bring OpenOCD-Patches to mainline
- Comments for PatchSet before merging: https://review.openocd.org/c/openocd/+/4671
- full repo: https://sourceforge.net/p/openocd/code/ci/master/tree/


Solutions for wider variety of Targets
--------------------------------------
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
        - -> most efficient way would be to use PRU + custom abstraction layer to run MSP-Code -> PRU needs to access GPIO-Unit of System
    - JTAG
        - 4 Wire Version preferred to keep wiring to a minimal
        - would come for free when 2x2 Programming pins go to each target
        - should also be possible to bitbang via OpenOCD, https://forum.43oh.com/topic/10035-4-wire-jtag-with-mspdebug-and-raspberry-pi-gpio/
- Implementation Variants
    - (as before) Two Lines to Target
        - target-board is responsible for solution
        - analog switch on target-pcb for programming lines, controlled by one of the gpio (should be exclusive)
    - SYS -> 2x2 Lines to Target
        - mostly software-defined and very versatile
        - would allow JTAG & SWD via OpenOCD and SBW via custom PRU-Code
    - SYS -> UART -> intermediate uC -> 2x2 Lines to Target
        - firmware could just be dumped by UART
        - Needs the most custom Code & Debugging would be hard to achieve

TargetConnector-Modifications for HW v2.3 (Proposal)
----------------------------------------------------
- make programming pins officially exclusive for programming -> no logging via PRU
- add second pair of programming pins to target
- extend GPIO count from 7 to 9 (now free on pru) also counting the uart-pins (that could also work as GPIO)
- concrete changes
    - connector grows from 2x7 Pins to 2x9 Pins
    - connector needs to shrink to RM2.0 or lower
    - additional BOM: two analog-switches and some resistors needed
- space constraints on board get serious! -> Solutions
    - make board some mm wider
    - use SMD-Header to BB
    - more expensive manufacturing with smaller vias


