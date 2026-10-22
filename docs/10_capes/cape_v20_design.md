# Cape v2.0 - PCB Changes

## General rule for assembly-drawings

- origin orientation
  - keepout
  - assembly notes (mech15)
- designator
  - keepout
  - top designator (mech 2?)
- Copper / Silk
  - L1 Pads / Via
  - Keepout
  - Top Overlay
⇾ print in Color

## Implemented Changes v2.0r0

- 4 Layer! Planes for Sig, GND, A5V, (3V3)
- decide Manufacturer, EC, Aisler, Betalayout
- add design rules
- add layer stackup
- add default vias
- divide in groups / rooms
- optimize surroundings of ICs
- change vias of pson50, dfn-10 (by lt3487 spec)
- move lvlchangers to the left
- change pads of pinheaders in inner layers
- thermal pad of switch unused? yes, no word of use in datasheet
- increase restring / holesize, sheph seems to have 0.15mm holes?, target 0.075 ring

## Implemented Changes v2.0r1

- Beaglebone
- Emulator
  - DAC
    - previous: **DAC8562SDGSR**, mouser 595-DAC8562SDGSR
      - 50 MHz SPI, 7-10 us Settling, 1-4 mV Zero-Scale-Error, 40 mA Short-Circuit-Current,
    - constraints: >= 16 bit, SMD, 2 CH, not maxim, v-range ~2.5...5.5 V, short settling time
      - this could also be low-res and slow for only bq-output-sim, but it would benefit to also tap in cap-voltage directly
      - <https://www.mouser.de/Semiconductors/Data-Converter-ICs/Digital-to-Analog-Converters-DAC/_/N-4c44d?P=1z0w8k6Z1z0w2wwZ1z0w2wvZ1z0w2wtZ1z0z7ptZ1yz5pwlZ1yzmm10Z1yzml2aZ1yzmm18Z1yzmlprZ1yzmm0yZ1yzmm13Z1yzmlr9Z1yzmlh1Z1yzmlwtZ1yzmm16Z1yzmm0zZ1yyh4l4Z1z0zls6Z1yzxao2&Ns=Pricing%7c0>
    - replacement: AD5663ARMZ-REEL7, mouser 584-AD5663ARMZ-R7
      - 50 MHz SPI, 4 us Settling, Zero-Scale-Error<1mV, 30mA Shor-Circuit-Current, needs voltage reference, WATCH OUT - there are versions with midpoint-start
    - replacement: DAC8830, 1-CH, 50 MHz, 16bit, 10nV/sqrtHz, 1us Settling,
    - replacement: AD5545B, 2-CH, 50
  - OpAmp for V-BUF 2CH?
    - previous: **OPA2388IDGKT**, digikey 296-50277-2-ND
      - 30-60 mA perm, 5 V/us, 7 nV / sqrtHz, 0.25 uV Offset,
    - constraints: opAmp, 3CH, supply ~ 3-5 V, Rail2Rail
      - <https://www.mouser.de/Semiconductors/Integrated-Circuits-ICs/Amplifier-ICs/Operational-Amplifiers-Op-Amps/_/N-6j73m?P=1yzxao0Z1yzmm18Z1yzmm0xZ1yzmm13Z1yzmm14&Ns=Pricing|0>
    - replacement: AD8606ARMZ-REEL, mouser 584-AD8606ARMZ-R
      - 2CH, 80 mA, 5 V/us, 8 nV/sqrtHz, 20 uV Input Offset,
  - shunt-Resistor
    - nRF52 takes 9 mA @ 4dBm, 16 mA @ 8 dBm for ~ 200 us, rest is below 2 mA,
    - previous: 2 Ohm 1% ⇾ 16 mA => 32 mV, would mean 1% Voltage drop at 3V3, less would be better
    - current sensors are no alternative, too expensive, not enough resolution
    - replacement: 1 Ohm 0.1% ⇾ 1:1 mA:mA, 0603 or 1206
      - **RT1206BRD071RL**, mouser 603-RT1206BRD071RL
  - OP-Amp for Shunt
    - previous: AD8422BRMZ in combination with LM27762DSSR
    - constraints: 1 CH, > 2 MHz Gain-BW-Product, Supply ~ 2-5 V, >75 dB CMRR, Low input offset voltage
    - replacement: **INA331AIDGKR**, mouser 595-INA331AIDGKR, in combination with **LM7705** (-0.23V) on V-, mouser 926-LM7705MMX/NOPB
      - ref: <https://e2e.ti.com/support/amplifiers/f/14/t/700003>
    - proper replacement: ad8429B
      - <https://tools.analog.com/en/diamond/#difL=0&difR=0.05&difSl=0&gain=100&l=0&pr=AD8429&r=5&sl=0&tab=1&ty=2&vn=-8&vp=9&vr=0>
      - <https://training.ti.com/system/files/docs/1312%20-%20Noise%202%20-%20slides.pdf>
  - ADC 2CH
    - previous: ADS8694TSSOP38 4 CH
      - 18 bit, 4 CH, two V-Rails for A&D, 500 kSPS, 18 MHz SPI, variable LPF, 1175 ns Acq & 825 ns Conv.
    - constraints: 2CH, 18-24 Bit, SMD, >100 kSPS
    - replacement: **ADS8691**, 1CH 1 MSPS 8€, ADS8695 1CH 500kSPS 9€, ADS8699 1CH 100kSPS 6€, Acq 335/1000/5000ns, Conv 665/1000/5000ns
  - analog switch ⇾ is there a way to power the offline target? Switch up supplies
    - previous: TMUX1101DCK, 4 Ohm, 1 SPST SinglePole-SingleThrow
    - constraints: 2 Ch, legs, supply >= 5, rdson <= 500 mOhm,
    - replacement: **NLAS4684MR2G**, mouser 863-NLAS4684MR2G, 2CH, 300 mA Conti, 500 mOhm rds
  - Target-Port-IO (GPIO, SPI, I2C, UART, SWD/JTAG, BAT_OK PRU) ⇾ Q: is HS-GPIO enough? rest is userspace-logged
- debug to target
  - voltage-level-translator,
    - previous1: TXB0304RUTR BiDir, autosense, min 3mA input drive current, 4 CH, >40 Mbps
    - previous2: SN74LV4T125PWR UniDir
    - constraints: 1 Mbps, high channelcount, autosensing, 2-5V, HighZ-Mode
    - replacement: **NXS0108PWJ**, mouser 771-NXS0108PWJ, 50 Mbps, BiDir, Autosense, open drain, 8 Bit, NXB-Version: 2mA input drive req.
      - ⇾ WARNING: expected 18.01.2021, **nxs0101** already in stock, nxs0102 in may
- target-port ⇾ default pin-header, maybe smaller version of it
- suppply for second target ⇾ 2. CH of DAC + Buffer
- status-Leds
  - green 575nm, 0603, 60mcd 2V@20mA, 150060VS55040, mouser 710-150060VS55040
  - blue 470nm, 0603, 80 mcd 3.2V@60mA, 150060BS55040, mouser 710-150060BS55040
  - red 645nm, 0603, 70 mcd, 2V@20mA, 150060SS55040, mouser 710-150060SS55040
  - orange 605nm, 0603, 100 mcd, 2.2V@20mA,
- LEDs for current active (and powered) Target
- multipurpose nChannel MosFet
  - constraints: <50mOhm, smd, n-CHannel, VGS <=700mV
  - sot-323-3: DMN2058UW-7, mouser 621-DMN2058UW-7
- i2c-storage, prev: CAT24C256WI-GT3
- Cage
- Part Properties:
  - price (for ten), manufacturer, manufacturer id, shop 1, shop 1 ID, ...
  - special properties: max voltage, power, current, size / package, color, forward Voltage
- extra information (i2c-adress, spi-speed, ) directly in schematic
- power-recording-stage
  - DAC DAC80501ZDGSR
  - OPAmp OPA388ID, pin-compatible with LTC2050HV
  - nMOS SI2374DS, test with BSH103
  - ShuntOPAmp Ina190A1IDCKR
- power in via vdd_5v (P5/6) ⇾ Test shows: BB does not power up via sys_5v
- reboot / boot via Pin-Toggle (Shutdown via command), we should trigger both (RESn⇾PD,PWR⇾PD), Test shows: Reset works while PWR is in PD
- add 256 GB USB-Stick
- switch to smaller IC-Packages and 0402
- order / add GPS
- is the gps capable of alarm (wake up sys)
- our 5V analog should be stabilized more! Add A5V with 2 Stage Bead, or real coil
- add footprint for layer-windows
- add footprint for shepherd-logo
- give INA190 a negative supply (>1mV would be enough) on GND-pin, ref stays on common gnd, extra decouple
- Debug-Pins with Ground
- extend harvest-Port, add option to measure VSense, and output VCap (V_A of Emulator)
- it would be wise to detach a5v even further from 5V, with a low-drop diode
- EMI-guard SPI, currentlimit at pinheader, terminate at ICs, 33 Ohms close to cpu recommended (avoid reflections)
- add alarm-feature, something SPI-programmable, that can act like a watchdog, with at least max 1-4h windows
- check against shepherd v1.5
- don't shut down individual Emu / Rec - Parts (delete or just disable all at once) ⇾ done by Pwr-control
- Harvester needs second channel ADC with very low input current, 1MOhm is too low
- manual button with LED ⇾ connector S4B-ZR-SM4A-TF, P1 3V3, P2 LED ODrain, P3 SenseButton with PU, P4-6 GND
- add ultra low noise LDO to A5V, and possibly a boost-converter upfront
- find better level translator, less current (best if near 0)
- reprocessed 11_concept.file
- switched Ina190 for AD8421
- added boost/Inverter for proper voltage rail
- add target port (comparator-include?) System will be a nRF52840 and most likely a MSP430
  - try to make it compatible with breadboard / dev-Kit
  - is spy-by-wire physically compatible with swd ⇾ it is, TClock is uni-dir, TDIO is bi-dir
- replace 100nF/16, 1uF/16, 10uF/16
- BOM, more precise alternative - BB uses 32.768 kHz osci MC-306 (20 ppm, 8x3.8mm) or similar, package says 327A5M
  - alternative: 5 ppm, 12.5pF, 50 kOhm, <https://www.mouser.de/ProductDetail/Citizen-FineDevice/CM200C32768HZFT?qs=rkhjVJ6%2F3ELrGt3qchcVtQ%3D%3D>
  - BB also uses 24.576 MHz
- check output limits of opax388 and DAC
- compare lowNoise LDO to LM27762
- 750 kOhm 1%, 667-ERJ-2RKF7503X, 5 + 32
- connect BB-Pins, 500 Ohm to input pins that could be driven from both sides
- complete ERC
- 1uF/16V is still 0603, change to 0402, there are 34x (incl. Recorder)
- redistribute capacitors
- replace coil with smaller one, check recommended direction
- add 1kR & 100R high precision for current measurement, EMU
- order digikey (extBut, samtec), mouser, csv
- add footprint for quality-control-panel
- BB Pinheader Cape-Design Stays ⇾ possible alternaltive Producer is Samtech, design is now divided
- add production-constraints
- update BOM
- v2r1 ordered

## Implemented Changes v2.0r2

- silkscreen - 10k array are 1k
- 3d-Step: shield transparent for better view below
- silk. "P3" designator is below component
- pads of 0402 bigger, 1.2x1.2 as min area for pads? paste 0.8x0.8? got some tombstones on current revision
  - half a pad distance to neighbour (keepout)
- improve connection betwenn pads (esp. 0402)
- feducial seems massive, shrink it?
- SPI-CS with at least 33R to lower chance of interference
- R for BatteryGood is wrong (handled by PRU), should it also be routed to userspace?
- TC7WH-Footprint is to large
- HC2G-comment (Name) is wrong / twisted
- DAC pads could be longer, reach more under the IC
- MP32 has no dot on package, just [ABC], lower left is pin1
- NSR (or all diodes) could get a line on the 3d-file (current dot is confusing, because the actual package has line and dot)
- the orange led is red! ... bad UI for general blinking
- describe gain of OP-Amp in schematic
- 100R, accuracy is missing in description / constraints
- Silk for L9/L10
- essential silk-numbers on headers can be bigger/bold, a bit more distance from header
- rename rec to harvest, port on pcb more obvious
- harvest dAC ch-b - drain power source OK?
- improve marking on Voltages, maybe with an arrow
- reverse diode of mosfet is too weak - already destroyed the reverse polarity protection
- some popular Flag-Markers on backside for pinheader
- Pin1 dot should be a shallow/sharp triangle, pointing in the right direction (less confusing in dense layouts)
- transistor-footprint is not conform to datasheet, it is slighly bigger and just misses the pads?!?
- u13 thermal to wide, reduce a bit to avoid shorts (u15 has same possible weakness)
- rework als Pin-Descriptions (already mentioned)
- round and divided (big) paste pads
- add general power-led when shepherd is on? maybe on 6V line
- switch to thinner stencil, bigger pads (paste is good for it)
- header-row on target has paste, it should not
- Font/Writing in copper is unreadable on target (slighly below spec)
- add layer for manual / pick'and'place descriptions (m15, m?)
- qr code is not readable, blurred, reduce size of "pixel"
- warning for harvest V_sense ⇾ Voltage floats if not connected and will most likely show V-Max in this state
- ADC nRST should not get A5V, only 3.3, also there is no need for a resistor-switch
- Connector for external switch was copied from old schematic, but this one had inversed pin-numbering on connector, different from datasheet
- Testpoint on RVS-Pin of
- protect GND better around Pinheaders
- U25A, Inputs are switched
- diode between both 5V-lines should be two diodes that feed the watchdog
- 3V3 should also be switched - maybe even the 5V0 in, so the PU that hinder bootup are meaningless
- vias came back only weak tainted (make it less severe if that happens), mainly for target pcb
- more distance to gnd-plane (soldering is hard, even with thermals
- TEST Watchdog, make compatible with BB
- TEST GPIO to and from target
- same orientation for transistors
- switch p8-27 and 29 (batOK / GPIO4) for cleaner readout
- switch p8-43/44 with p8-39/40 for proper boot
- TEST boot with all pins except 3v3 & 5V
- but make sure that shepherd-EN (p8-13) stays low during boot
- switching main power to both targets shows, that the routes seem to have different current-readings for the same load! odd
- 1k for LEDs
- check surroundings of mosfets, size has changed
- mosfet of watchdog-wake could be tied to 3V3 with additional 1k resistor or diode (so that button stays usable)
  - 100k PD for wd-pin (or keep 10k)
  - 3V3 goes low on powerdown, so watchdog can enable (pull low wake) BB again,
  - polling has no effect during normal operation
  - TEST if 1k is enough to pull line low to enable ⇾ it is
- add open source hardware logo?

## Schematic Changes - Open

- prepare calibration
- ordered not enough 15uH Coils, need 30 more
- check remainder of BOM for emu-only assembly
- shepV1 had a user-space led, which is still there, same pin, but pru-controlled, was it the same in v1?
- explain schematics,

## Part Changes

Note: after Mouser-Order - NOW already ordered

- DAC 100nF ⇾ 1uF
- Boost 10uF ⇾ 10uF (inv)
- Inv +47uF
- Rec 2x 10k 0603 ⇾ 0402
- All 34x 1uF/16V/0603 ⇾ 1uF/25V/0402
- final Shield, cover & frame
- all 4x 15uH/4mm ⇾ 15uH/3mm
- parts of nRF-Target

## Schematic Changes Postponed

- internal calibration? with 2 switches and 1 calibration-linear-power-supply
- OP-Amp, bias Subtractor: LMP7701MF, not needed now
- sync to pps ⇾ external pcb
- usb-socket is impossible to hand-solder right now
- (maybe) add PU to watchdog outputs
- separate PCBs for PPS-Source, Recorder, Emulator

### Open Issues

- only 5 diodes of type PMEG in order?
- change 100 uF to 47u? one less component
- Testpad should be square for GND, half-circle for Signal or similar
- r3 (dac, emu)
- proper naming for TP if there is space
- TPs should have bigger hole, so probes stick
- oscillating opAmp should be outside of cage
- allow install of a big cap on A5V or 5V, 5v5 1F is cheap
- add longer pinheader for p8/p9 23-46
