# Boot Pin Interference

**TLDR**: cut connection to these pins per default.

## Problem

- shepherd-pcb stops beaglebone from booting
- startup behavior is determined by 16 pins, which are on P8 Pin 31 to 46
- only the first 6 and last 2 are important
- last two are not used by shepherd

## BOOT-Pins (from BB-Green-Schematic)

- to boot from internal MMC1 the bits from BOOT[4:0] must be 0b11100
- the high pins are held high for the first ~7 sec
- schematic shows that pins are Pulled up or down with 100k

## Changes through Shepherd PCB

- Boot-pins have 1k input Resistance and are then pulled up to 3V3 with 100k
- even with floating 3v3 the board won't boot
- each boot pin is also connected to another Beaglebone-Pin

Pin-Info

| name  | pin   | PRU1 | state | 2.pin | function | LinuxGPIO   | State | Note                             |
|-------|-------|------|-------|-------|----------|-------------|-------|----------------------------------|
| BOOT0 | P8-45 | 0    | LOW   | P8-14 | gpio0    | 26          | LOW   |                                  |
| BOOT1 | P8-46 | 1    | LOW   | P8-17 | gpio1    | 27          | LOW   |                                  |
| BOOT2 | P8-43 | 2    | HIGH  | P8-16 | gpio2    | 46          | LOW   | drive with 2k against bootconfig |
| BOOT3 | P8-44 | 3    | HIGH  | P8-15 | gpio3    | 47          | LOW   | drive with 2k against bootconfig |
| BOOT4 | P8-41 | 4    | HIGH  | P9-24 | uart-tx  | 15/uart1_tx | HIGH  |                                  |
| BOOT5 | P8-42 | 5    | HIGH  | p9-26 | uart-rx  | 14/uart1_rx | HIGH  |                                  |
| BOOT6 | P8-39 | 6    | LOW   | p9-17 | swd_clk  | 5/i2c1_scl  | HIGH  | boot: don't care                 |
| BOOT7 | P8-40 | 7    | LOW   | p9-18 | swd_io   | 4/i2c1_sda  | HIGH  | boot: don't care                 |
| batOK | P8-27 | 8    | LOW   |       |          |             |       |                                  |
| gpio4 | P8-28 | 9    | LOW   |       |          |             |       |                                  |

## Test & Improve

- 1k input resistance is fine
- shepherd PCB alone shows
  - (fresh PCB) pin 41-46 has 110k to GND, 101k to 3v3 ⇾ maybe still a short
  - (test PCB) pin 41-46 has open connection to GND, 101k to 3v3
- with BB connected
  - pin 41-44 show 44k to GND, 42k to 3v3
  - pin 45/46 show 106k to GND, 100k to 3v3
- previous 1.x hw-revision shows diodes to these pins, but this seems sub-optimal. makes pins to input-only, but only fast-switching for rising-edges
- shepherd-enable (p8-13) stays low during boot ⇾ perfect to disconnect board from power
- behavior of secondary pins (see table above)
  - BOOT[0:3] stay low
  - BOOT[4] stays high
  - BOOT[5:7] high during boot (7.7) on sys with shepherd installed, stays high on fresh sys
- disabling uart1 and i2c1 brings:
  - BOOT[0:3] stay low
  - BOOT[4:5] stays high
  - BOOT[6:7] high during boot (7.7), then low
- add uart1-pins to shepherd dts (and set p9-17 to also input pin)
  - BOOT[0:3] stay low
  - BOOT[4:7] high during boot (7.7), then low
- booting with shepherd works with
  - P8-44/45 disconnected, OR
  - P8-15/16 disconnected, OR
  - switching P8-15/16 (LOW) with P9-17/18 (HIGH) works!

## Changes to System

- i2c1 is only for target-pin-header and can be disabled by default (needed for target-programmer later)
- uart1 is disabled for now (to access pins in linux)
- switch Boot[2:3] with other PRU-Pins that are high during boot
  - OR disconnect pins when disabled
  - switch P8-15/16 (LOW) with P9-17/18 (HIGH)
- increase resistance of pru-pins, 10k should be fine, when only input
- bat_ok can be at the end (of PRU-Pins), because it is write-only

HW-Tests

```text
sudo shepherd-sheep -vvv demo-functions
```
