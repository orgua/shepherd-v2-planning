Feasibility of Requirements
===========================

- this part is looking mainly on the hardware-challenges (software can be adapted later if the hardware is prepared)

Emulation of Capacitor / DC-Converter
-------------------------------------

- Problem: PRU of beaglebone black is currently already quite occupied with measuring and replay of energy-trace, emulation means real time control loop, the PRU has limited capability for that (no division, ...)
- Enabler 1: keep previous hw-design (fall-back), but add switches to bridge converter and cap (one additional pin - does not need to be connected to PRU)
- Improvement 1: optimize PRU-Code, i.e. bitbanging of SPI
- Improvement 2: current beaglebone AI offers two PRU and 2x dual-arm-cortex-M4 cores (price is 122 € instead of 60 €)
- Improvement 3: try to find approach where same cape-pinout can be used with beaglebone black and beaglebone AI
- assessment:
   - mostly critical is software / firmware implementation
   - -> hardware enabled approach, not difficult in hardware, low risk and low impact on time expense
   - also allows On-Off-Pattern for target-power

More GPIO to Target
-------------------

- Problem: gpio must be real time in PRU, PRU Pin-count and workload limited
- improvement 1: share programming-pins (currently not possible)
- improvement 2: beaglebone AI offers one more PRU, hopefully with more usable pins
- assessment:
   - PRU has still 9+ unused pins, even 10 (with current ones) in a register-row, but 8 seems like a more suited number

Bidirectional GPIO and fast/variable UART / SPI to Target
---------------------------------------------------

- Problem: logic signal must be level-shifted and detachable (possible energy transfer) and also high-speed
- current layout: Target-GPIO are output only, uart bi-dir & recorded in PRU, programmer is in user space (currently not recordable, dedicated pins on nRF52)
- improvement: change level-changer and switches / muxer if needed
- assessment:
   - bidirectional gpios will be recorded properly, but never react in realtime if handled in python-api
   - (high-speed) SPI is hardly possible, there are no further dedicated hw-spi that share pru-pins
   - uart-speeds, TODO: must check with PRU-Documentation,


Allow user-provided Energy-Traces
----------------------------------

- assumption: 8 byte timestamp, 2x 4 byte U/I-ADC-Value, 100 kHz -> ~ 1.6 MB/s
- Problem: traces for an hour or day become hard to handle via internet
- improvement 1: allow looping of short sequences (also mirroring for continuity)
- improvement 2: U/I-Values could be partial linear dependent and therefore compressible (data-compression-algorithm, vectorization, delta-conversion)
- improvement 3: beaglebone AI has GBE instead of 100 mbit, that makes data-handling a lot smoother
- assessment:
   - no hardware-changes needed, lib-changes seem manageable

Accuracy of time-base
---------------------

- Problem: jitter on gpio-traces from different nodes
- Improvement 1: use ethernet switches with ptp-support, QoS and GPS-Interface
- Improvement 2: GBE of beaglebone AI could bring advantage (faster processing in stack / switch, stricter timing constraints)
- Improvement 3: change crystal oscillators of beaglebone to temperature compensated ones (lower PPMs for drift and aging). Oven controlled crystals would be to big
- Improvement 4: external sync port is already available for the gps-capelet, even if it is not used for time-keeping, it can be recorded for later trace-alignment
- improvement 5: ptp has a lot of undocumented set-screws ...
- assessment:
   - no definitive solution for sub 1 µs accuracy, but some of the solutions should be considered in concept phase, others are sw / hw mods in a later stage
   - no risk on hw-level, minimal more time expense in design-stage

Mobility of Nodes
-----------------

- Problem: node presumably without network access and gps-reception, not powered all the time
- Improvement 1: allow external gps-antenna (not possible for current ublox SAM M8Q / 22 €)
- Improvement 2: offer backup power to gps module, small LiPo or supercap
- Improvement 3: offer software based scheduling and pre-config of measurements on nodes
- Improvement 4: offer a robust power-connection
- improvement 5: tweak linux for low power usage (turn off unused devices)
- improvement 6: proper casing with interfaces (i.e. eth, power-switch/connector, gps-antenna, pps)
- assessment:
   - low risk on hw-level

Support for other Targets
-------------------------

- Problem: different µC need various programmers
- Info: Flocklab and D-Cube support nRF52 (DFU / USB, SWD), STM32L4 (SWD), MSP430 / 432 & CC430 (JTAG, Serial, USB, Spy-By-Wire)
- Enabler 1: generalize programmer pins and GPIO-Pins to Target (specialize on target-carrier-pcb)
- Enabler 2: bring usb to target device if possible (beaglebone-Pinheader does not have USB, but could be realized via cable)
- assessment:
   - if openOCD supports targets and prog-protocol (or implementing them is easy), chances are good
   - pin-sharing with target-gpio is hard -> device-tree seems pretty static
   - general idea seems viable -> TODO: more reading

Support for two selectable Targets
----------------------------------

- Problem 1: gpios with PRU support are limited
- enabler: relay-switching of targets by beaglebone (not necessarily PRU-Pins)
- problem 2: how to distinguish between ICs automatically
- enabler: software-defined PRU-openOCD could try to probe, get chip-ID with various methods (jtag, swd)
- assessment:
   - hardware changes are fine, board space is not limited (cape can be bigger than beaglebone)
   - software could be more tricky -> py-lib should be "general" (without board-specific config), but target still has to be choosable, and target-firmware has to match the choosen target


GeneralPurpose-Capelet-Port
---------------------------

- more specific: usable for SDR / FPGA
- Problem: unknown data-rate, use of GPIO, interfaces, programming interface
- assessment:
   - a simple sensor interface with gpios, spi, i2c would be feasable
      - there is a free uart5 and half uart4 that could be freed, and 20+ user space gpio
   - SDR exceeds limits of project -> would be better suited on a second beaglebone or PicoZed-Board (Zynq-FPGA + SDR)

Separate RF-Interferer
----------------------

- more specific: controllable rf-standards as interference
- enabler: modules for WIFI and BT could be added per USB / Hub and controlled via linux, defined traffic via iperf (for WIFI) or JamLab-NG
- assessment:
   - should not be main goal for shepherd V2, maybe stretch goal
   - has no influence on cape-hw-design or python-API, can be completely separate (even on extra beaglebone or server)

Channel-Monitoring
------------------

- problem: analog to rf-interferer
