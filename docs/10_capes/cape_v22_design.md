# Cape v2.2 - PCB Changes

## Implemented Changes

- INFO for v2.1r0:
  - first 4 Target-Boards has green LED1 (down) and red LED2 (up)
  - Vanilla Shepherd v2.1 Cape stopped BB from booting and even putting it on while running failed (p8 41-44)
  - removed watchdogpins (pwrOn&reset) allowed to put cape on while running (still not while booting)
- L3V-TestPosition is bad, easy to produce shorts with neighbour
- update expected voltage levels in schematic
- label for pwr-led
- AB-label of target bigger
- P7/P8 seems wrong name for big pinheaders
- testpoints without paste, and small hole in copper to lock a probe ⇾ just less paste
- is there a way for cage-selfalignment? ⇾ negative solder mask exp
- remove layerwindows and make number bigger
- describe external powering better in schematic
- pin1 markings should be bigger
- emulationBug! - Critical
  - solutionA - MinimalEffort: Swap FbB- with RailA-Trace
    - FbB ⇾ rotate R1/10k clockwise and attach it to middle pad
    - RailA ⇾ cut Trace between R9 and Via
    - connect enamel from R9 to (now) free Pad of R1 ⇾ this routes RailA to Switch
    - connect enamel from TP1-Pad to rotated R1 ⇾ this routes FbB to Switch
  - solutionB - clean: rewire output of AnalogSwitch
- silk: vCap is now V_SimBuf
- schem: recorder gain is now just 10
- more Metal for cooling the recorder-Path
- Rail-LED is twisted! ⇾ No its not
- add 2x23 to BOM SSQ-123-03-G-D , digikey SAM1196-23-ND
- VHarv lowpass is 160 kHz not 16 kHz as shown
- change all lowpasses to 160 kHz
- emulator should go back to 1 Ohm Shunt, 100 Ohms for InAmp for 100:1 Amp ⇾ now 2R & 1:50
- Switch Ext-Pwr Pins (instincts are strong for edge-pin to be GND) and don't forget Silkscreens!
- EEPROM needs to be always powered (BB 3V3)
- reduce V_IO_BUF OPAmp-Resistor to 10 Ohms
- a little bit bigger 0402-pads, they get loose quiet fast
- level-change performance is still bad! maybe add 1k back?
  - add back 1 kOhm as series resistor for LSF0801. maybe a bit lower because edges are a bit slow (1 us)
- put a note in schematic for WD
  - BB_START has 5V Level when BB is on, gets pulled to 3V3 when WD does its routine because schematic uses BB3V on it. but that seems ok!
- get target A/B/1/2 straight. it is target 1/2 from now on! ⇾ Skip it
- C over Shunt is sometimes contraproductive (100 nF || 2 Ohm produce 1 MHz oscillation without any load but 100 nF buffer, 1uF/0uF is fine)
- provide more help with switching to external pwr, switch? backside would be good
  - switch + jumper?
- add 74HC4066 and OPA189 to consumer-list, build a low-pwr Overview
- optimize shepherd-EN (unlink rec/emu?`, better buffering?)
- hw may be glitching BB - caps are getting big, voltage drop also ⇾ critical!
  - maybe add lowpass to en-pin of regulators or limit power
  - TEST: run unittests 2-5x, often bb hangs itself somewhere between 47...80%
  - scope shows:
    - AC: 600mV dip on shepherd-enable, 3x 200mV stages, lowest point 600 us after start, then fast recovery to -300mV, slow after (quickshot 1-2)
    - DC: 800 - 1100 mV Dip, but the first one (after a break of some minutes) is more severe
  - another hang: converters did not start as planned, only 6V is up, L3V3 is at 2V, the others well below that
  - mitigations: 1mF/16V Cap on 5VBB reduces voltage drops to ~ 200mV (max 300), in a 5 ms Windows (quickshot 4)
- Add Cap
- run through hw_performance_v2.1r0 for final cross-check
- allow to turn off ADCs (not that important for EMU-only)
- maybe add 2nd Switch for PRU-Ports, or lower resistors to <= 100 Ohm (speed-improvement)
- around switch-IC, avoid solder bridges per design even more ⇾ space out vias, reduce solder mask expansion

## Additional Parts

Note: numbers for one Unit, refs are Mouser-Numbers

- 2 Ohm precision shunt: 603-RT1206CRD072RL
- 2 Ohm shunt: 667-ERJ-2GEJ2R0X
- more 1k 0402 (2xRec, 2xEmu, 10x LvlChg)
- 210R InAmp-Gain-Setter: 603-RT0402BRD07210RL
- 1mF, 6V3, 647-UVR0J102MPD1TD (D8mm,L11mm,3.5mm Spacing)
- analog switch, 2x 771-HC4066BQ115
- 4x 963-NR3015T1R5N
- LSF dev-kit

## Open Issues

- feducials could be removed - panel has plenty
- more pinnumbers on big headers
- test changed recorder
- is harvest-LED working? YES, but only with higher currents
  - var1: bind to vsim to allow more refined feedback
  - var2: 3x 2.0V Leds from adc-input to -6V (with resistor, should always light up)
  - var3: v-to-i converter
- switch to TI Version of LSF0801 ⇾ out of stock till feb.22
- optimize LSF for 1 MBaud (see
- WDog is still not triggering nSTART (pulse too short)
- HC2G04 still has wrong comment
- wrongly linked in schematic
  - C53 L3V is part of recorder, but should be open domain
  - C48 is recorder, but should be emu
  - C24 is open domain, but should be recoder
- has DAC also pin to disable?
