# Concept nRF52 Target with FRAM

Design is based on Squeeze

## Assumptions

### Things to cut away

- power supply - complete block
- i2c routed to connector (i2c to RTC left)
- INT to max-IC
- all 7 pwr-supply signals to connector
- energy management - first in parts, then completely
- RTC-PWR-Switch ⇾ is a bad Idea, as we have no way to initially power MCUs (even during programming)
- shared pwr-IO (mostly to management) ⇾ enough shared pins already

### Things to keep

- RTC
- programming-pins
- shared spi, i2c, max-int, rtc-int

### Things to change

- Shp_Bat_OK should go to some gpio (=9)
- add current-protection between shared io-pins ⇾ all ICs (levelchanger, RTC, MSP, nRF) are comfortable with >10 mA drain/source so we limit at 8-10mA for ~4V max (~500 Ohm) which results in **240 Ohm for each connection of a star-topology**
- some more debug LEDs
- RTC gets more "battery", + 100 uF
- capacity on MSP_SBW_IO is ref-design (probably debounce for RST) ⇾ set DNP
- GPIO-Pins to cape-Port, special functions bound by MSP

   - 0:1 are UART
   - 0:3 are SPI (with target as Controller)
   - 9 signals BAT-OK from Shepherd
   - 10 is missing (is now LED)

## Misc Questions

- open source OK
- do some of D0:D10 have hidden dedicated functionality? 11 Pins to 9+1 ShpPins have to be mapped somehow. D2:3 seems to be A_In, D0:1 are uart?

   - one of D0:10 influences RF ⇾ D6 is LF-IO, P1.03
   - there are 6x free HS pins, why are they not used? space constraints?
   - NFC pins are special care (pwrgd H0)
   - really just put CLK on nRESET of nRF-Module? should be ok after reprogramming

- to clear up

   - MSP has a lot of compromises because of smaller package
   - MSP GPIO 0/1 is UART (This will be routed to SHP-GPIO 7&8)

    - bauteile sichten (BGA, QFN), advantages QFN
  + simpler design and footprint
	- pin-def incompatible to squeece
	+ already locally in stock
	+ if our qfn stock runs out we could switch to BGA without changing pin-def
	- QFN (-1IRGZT) = 7.80€@100n; BGA (-IZVW) = 9.42€@100n

 + msp reset C ⇾ DNP
 + CoPi
 + spannungsbegreuntzung diode checken
 + PWR-LED mit Mosfet + only 220 R ? as much current as possible

⇾ implemented for v1.0, https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.0

## Changes after v1.0 / Bugfixes

- marking of module footprint is irritating ⇾ copper crosses more inwards
- name LEDs!
- C7 is 0604? use same as C2
- make longer and all parts on one side? ⇾ NO

⇾ implemented for v1.1, https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.1

## Hardware-Tests

see readme.md in targets/hardware-folder
https://github.com/nes-lab/shepherd-targets/tree/main/hardware
