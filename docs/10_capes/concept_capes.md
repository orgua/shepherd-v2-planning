# Cape Concept

This is mostly a documentation of changes in comparison to v1.x

## Computing Power and Accuracy Constraints - a pro and contra

- Beaglebone Green
  - pro: 40 €, HW-Timestamping, 2 real time Cores, awesome support and community, stable and fairly low energy consumption
  - con: fairly old CPU, 100 MBit Ethernet, RTUs could be to slow for the requirements, storage is slow, encrypted network traffic is slow (< 50 MBit)
  - biggest challenges:
    - pre and post data-transfer
    - high speed emulation in PRUs with the slow L3-Access, inflexible GPIO, missing FPU and int-division
- Beaglebone AI
  - pro: same as BBG, GBE, faster CPU, 4 Real time Cores
  - con: 3x Price of BBG, still the same PRU IP with its limitations
  - unknown: faster storage, faster network traffic
- Zynq 7020
  - pro: similar price as BBAI, 1 GBE, FPGA in same Package, hw-timestamping
  - con: xilinx-toolchain, documentation is overwhelming, community small, long dev-cycle
  - <https://shop.trenz-electronic.de/de/30195-MYC-C7Z020-CPU-Modul-mit-XC7Z020-2CLG400I-industrieller-Temperaturbereich?c=238>
- embedded AMD-Platform (v2000)
  - pro: compute-power, relatively cheap (>= 200€), fast ethernet, x86-64
  - con: real-time not out of the box, low gpio-count
- PRU replacement or extension
  - CPLD would be overkill
  - Teensy 4 ⇾ lots of iO, SPI with DMA, interrupts for everything, FPU, 600 MHz, proper [toolchain](https://www.pjrc.com/store/teensy40.html)
  - FPGA in between embedded CPU and Shepherd
    - some lattice even have a open source toolchain
    - FPGA could be transparent if not needed
  - argument to keep everything as is for now: "in between" could be added later by sandwiching PCBs

## Shepherd-Cape

- add fixed & robust power-connector and possibility to switch system on/off, reverse-polarity-detection
- external (SMA) connector for PPS (in addition to Link from GPS), possible switch / level-changer ⇾ record via PRU
- power stage:
  - remove / untie EH-recording (and mppt-conv) ⇾ recorder can stay on pcb or be even modularized
  - EH-recording after Converter not absolutely needed
  - current load solution seem a bit overkill and brings non-linearity with the LEDs
  - simplify "emulator" power-stage with virtual Converter
- easier (dis)assembly by reducing / removing pin-header-forwarding (only take what is needed)
  - reduce or bundle pins to shepherd (or another way to make disassembly easier) ⇾ used pins don't have to be forwarded
  - using a pointy thin rod that can get between pin-rows helps to non-destructive get cape off
- compatibility with and optimization for beagle AI (dedicated concept-file)
- addressable i2c - flash storage for calibration and distinction
  - all flashes can share same bus, shepherd gets first address, target second, ...

## Energy-Recorder/Emulator

- easiest case: replay / emulation could "just" rely on voltage-DAC and target-current-draw measurement?
- current implementation: recording with U/I before DC-Conv, emulation with U/I meas. after DC-Conv
- if recorder stays: converter could be modular, interface would offer shunt_in (V_sIn, V_sOut) and V_cOut Converter output, and some control pins
  - is the DAC for voltage reference really needed? LDO enough?

## Capelet - System

- get rid of pin-headers for b2b / mezzanine - interconnect ⇾ molex, flex cable, hirose ...
- support for addressable i2c-flash for distinction and configuration
- maybe rotate capelets, so they stick orthogonal on shepherd (would benefit antenna)

## Capelet - GPS

- look for similar gps-module with external antenna support (currently ublox SAM M8Q) ⇾ ublox Neo M8Q, same but with external antenna, 30-60 ns accuracy
- backup power (LiPo / Supercap)
- there are special timing modules
  - uBlox ZED-F9T (~ 140 €, < 5ns clear sky)
  - uBlox LEA-M8F (~60 €, < 20 ns clear sky)
  - uBlox LEA/NEO-M8T (~50 €, < 20 ns clear sky) ⇾ already in inventory
  - trimble also offers precise timing gps modules
- preferred solution: module without antenna and sma-port, smd-antenna on same pcb with sma-port, short interconnect or remote antenna
- PPS currently on Timer4 P8_7, GPS on UART2

## Target Port

- allow a second target ⇾ switch inputs and power (could also lead to a third if space is available)
- try to keep power (constant) for the not connected target, so it can run independently
- allow different targets (probably limited by software) even fpga or other untypical combinations
- handling with standardized data interfaces:
  - maximize gpio-count between beagle and target, parallel usage also for programmer-pins and uart if possible / needed (and spi if feasible)
  - host-cpu should offer SWD, JTAG, GPIO, SPI, UART to target (unified pins), PRU is recorder and power-supply-emulator (if PRU cant access host gpio periphery)
  - reasons: PRU is very static (pin-dir is predefined), python needs access to all pins
- target could also use i2c-bus to enable eprom-storage for config- and ID-Data
- fast level-changer for >= 1 Mbps UART (BB-Uart max is 3.7 Mbps)
- bidirectional gpio-connection, tri-state (input, output, disconnected)
  - perfect if also flexible muxer included
  - make gpio-connections to target switchable if possible ⇾ no transfer of energy (if needed)
  - possible usb-interface (has to be cable based, beagle does not offer usb on pin-header)
- if there is low cost one, make power-connection switchable (for on-off-pattern if power-emulation does not work)
- if usb to target (via cable), then make it off-switchable
- routing of v_in_SHT+/- can be removed - it was never used and is a big noise-source for ADC
- low prio: rf attenuator and connector for antenna ⇾ depending on target capabilities

## Beaglebone timekeeping

- test high precision, temperature compensated crystal oscillator with same footprint
- test higher quality gps with lower jitter on pps line
- sync line could be supplied by gps cape in combination with schmitt-trigger-hub to power multiple targets

## Special Constraints for parts

- subtractor for V_EMU_I needed, because DAC does not reach 0 ⇾ differential DAC would be nice
- ADC-mode is differential ⇾ <0 currently not needed, one bit wasted, but not bad to have, for reversed current-flow
- Diodes between beagle-pins and level-changer needed on some pins, because they are active at boot

## Hardware - PinOuts

- PRUs seems to have 28 Pins accessible (PRU0 15, PRU1 13), with the current occupation
  - 2Pin: target UART (on dedicated uart-pins)
  - 1Pin: target SWDCLK (seems to use normal gpio-fn, SWDIO on regular gpio/clkout2)
  - 4Pin: target GPIO
  - 5Pin: SPI to DAC, ADC (on dedicated SPI-pins)
  - 1Pin: Led1 PRU
  - 1Pin: LED2 User Space
  - 1Pin: select LOAD Pru
  - 1Pin: ADC RST/PDN
  - [3Pin: Debug-Pins (will be reserved by dts, but not in layout)]
  - ⇾ leaves 9 (+3) PRU controllable pins on beagle Black
- PRU Tasks
  - PRU0 seems to handle SPI, Leds, load select
  - PRU1 seems to handle target gpios, uart, adc-reset
- Host-Periphery
  - SPI0: P9.17-22
  - SPI1: P9.28-31,42
  - UART1: P9.19,20,24,26
  - UART2: P9.21-22
  - UART4: P9.11,13 P8.33,35
  - UART5: p8.31,32,37,38
  - I2C1: P9.17-18 or P9.24,26
  - I2C2: P9.19-20 or P9.21-22
- BB-Pins seem to drive around 8mA (found in SPRS717L_)
- system SPI, 33 Ohm in series close to processor recommended, to avoid reflections
  - P9_17, gpio0[05], SPI0_cs0
  - P9_18, gpio0[04], SPI0_d1
  - P9_19, gpio0[13], SPI1_cs1
  - P9_20, gpio0[12], SPI1_cs0
  - P9_21, gpio0[03], SPI0_d0
  - P9_22, gpio0[02], SPI0_clk
  - P9_28, gpio3[17], SPI1_cs0
  - P9_29, gpio3[15], SPI1_d0
  - P9_30, gpio3[16], SPI1_d1
  - P9_31, gpio3[14], SPI1_clk
  - P9_42A, gpio0[7], SPI1_clk, SPI1_cs1

## Shepherd V1 Functionality

- see beagle-pinout in excel-sheet (12_concept_hw..)
- GPS: ublox SAM M8Q
- Interfaces
  - Beaglebone 2x46 Pins
  - button + led
  - harvesting-source (VIn, 80%)
  - Energy-Storage
  - Target (4 GPIo, SWD, UART, VCC, BatOK)
  - Jumper to tap into current path
- fixed supply voltage for target
  - DAC6571IDBVR ⇾ i2c-DAC,
  - TPS73101DBVR ⇾ LDO
  - TMUX1101DCK ⇾ Switch 1Port 1Endpoint
- LM27762DSSR ⇾ low_noise pos&neg analog voltage (VDD, VSS) for some OP-Amps
- CAT24C256WI-GT3 ⇾ i2c-EPROM
- Target IO
  - TXB0304RUTR ⇾ BiDir level converter for target uart & swd (switchable)
  - LMP7701MF ⇾ OP-Amp, voltage buffer
  - SN74LV4T125PWR ⇾ UniDir level converter, high imp (Sep. Switchable, not used)
- BQ25504_RGT_16 ⇾ Voltage Reg with MPPT
  - ADG736LBRMZRM_10-L ⇾ Analog Switch 2Port 2Endpoints
- ref Voltage emulation
  - DAC8562_DGS_10 ⇾ 2CH SPI-DAC
  - OPA2388DGK8_L ⇾ dual OP-Amp, Voltage2Current Converter
  - LMP7701MF ⇾ OP-Amp, bias subtractor
- current & voltage measurement (harvesting & load)
  - ADS8694TSSOP38 ⇾ 4CH SPI-ADC
  - OPA2388DGK8 ⇾ OP-Amp, 2x voltage buffers
  - AD8422BRMZ ⇾ precision OP-Amp, 2? Ohm Shunt Amperemeter
- dummy load
  - OPA2388DGK8_L ⇾ dual OP-Amp, voltage buffer & Schmitt Trigger to switch on two LEDs
  - ADG849YKSZ-REELKS_6-L ⇾ Switch 1Port 2Endpoints
- harvesting
  - G3VM-31HR22SOP ⇾ low on-res switch to disconnect harvester
  - AD8422BRMZ ⇾ precision OP-Amp, 2? Ohm Shunt Amperemeter

## Eagle Project

- improvements to project
- allow proper DRC and ERC by redefining pins in symbol-lib
  - NC - not connected
  - In - input
  - Out - output
  - IO - in/out
  - OC - open collector or open drain
  - Hiz - high impedance output
  - Pas - passive (resistor, etc)
  - Pwr - power pin (supply input)
  - Sup - supply output (also for ground)
- swap-level (>0) allow easy pin-changes in later design stages (pins with same swap level)
- function ⇾ inverted (dot), clock, invClk
- add parameters for partnumber, order-number (mouser, digikey), some key specs (forward current, max power, max voltage, ..), price ⇾ eagle does not seem to support that at all?!?
  - reason to switch to kicad?
- minimize BOM
