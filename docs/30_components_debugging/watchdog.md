# Watchdog

**TLDR**: dedicated external WD is important and is kept on cape.

## Advantages of dedicated WD

- nodes are in remote rooms, often without access
- Fallback if we can't control POE-Power of ports (most likely)
- with a WD the BB can shut down and be woken up periodically
- BB does not mind a wake-up-signal when already running
- routine: BB asks server for tasks, waits or goes to sleep again

## TPL5000 Watchdog behavior

- time-delay is configured via resistor (100ms to 2h)
- "wake" is triggered for 31 ms on timer-match
- system has to confirm wake by triggering "done"
- if "done" is not triggered before next "wake" a reset occurs

## Problem

- (minor problem) watchdog will issue a reset for 0.4s after 3.7s of power-on
- (severe) watchdog will issue a wake-signal every t_delay
  - initial tests were done with "broken" beaglebone that did not act on a wake-signal during runtime
- (severe) diode from VDD5v to SYS5v introduced a lot of noise to the system (power-management seemed to have tried to switch to sys-power
  - diode was added to allow operation from internal power
  - use

## BBB behavior on Shutdown

- 3V3 ⇾ 0V
- VDD5V        ⇾ 0V
- SYS5V ⇾ 1.16V
- PWR_BTN    ⇾ 3.74V
- nRES_BTN ⇾ 0.15V

## Beaglebone Pin-Schematic

- nSTART: BB_PCB has nothing discrete except switch to GND
- nRST: BB_PCB has 10k PU & 2.2 uF Buffer & switch to GND

## Solution

- use 3V3 as Pull-Down to only get affected by wake-signal when BB is powered off
- add a diode, otherwise the 3v3 get shorted by Power-Button
- the diode also protects against
- (decide)
  - use two diodes to get energy from ext5v and power-button
  - use only 1 diode to power from ext5v. so watchdog is disabled when usb-powered
