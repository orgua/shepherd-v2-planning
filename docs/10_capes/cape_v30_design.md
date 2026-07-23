# Cape v3.0 - PCB Changes (WIP)

## Main-Changes

- design modular sub-PCBs, to
  - reduce complexity
  - make iterations easier
  - reduce cost (cape is either hrv or emu)
  - trivial switching of platform
- allow 4 Targets
- prepare support for Raspberry Compute Module (CM4 for now)

## TODO NextGen

- change ADC to higher resolution?
  - better: stabilize reading, lower noise level
- use second input of ADC to monitor actual voltage?
- make system modular !!
  - (+) less complexity -> dedicated emu OR hrv
  - (-) cal-data is harder to store, sync
  - (+) hrv can be ported to other platforms (cheaper, scalable)
  - (+) changing subsystems is easier
- direction pin GPO:3 for leveltranslators is named strangely
- rename Recorder ⇾ Harvester
- switch to rpi Cm4 Platform !!!
- offer gps-port with pps & uart on Cape
- put single gpio-lines onto SWD-IO switches (switch 2x for free)? or is dir controlled by PRU?
  - Switchable Directions:
  - Group A = GPIO 0:3 -> Group C GPIO2:5
  - Group B = GPIO 8 -> Group A GPIO0
  - Group C = GPIO 9 -> Group B GPIO1
- Sensor for light intensity on harv node?
- try to drive 150 - 200 mA to Target
  - change OP-Ampdriver to higher current output? Double Opa388?
- try to offer more than 10 GPIO to target (Goal=16)
- all GPIO should at least be INPUTs, some (2-4) also switchable

## Modularization

- would allow specialized observers (Hrv OR Emu)
- Cape mostly does routing between modules (and target-Ports)
- sub-PCBs are reusable (and changeable)
- harvesting with a cheaper network of nrf52 + pwr + hrv (rf-syncronized)
- a generalized USB-Interface + Hubs would allow usage on all (usb-capable) hosts

### Host-Interface / Header

- 2x4+ pins for MCU-Links
- 1 pin clock-sync-input
- 1 pin enable shepherd
- 1 pin reset host (predefined)
- 10..16 pins gpio-tracing (optional, mirrored)
- 2 pins for dir selection (optional, mirrored)
- 4 pins for programming (optional, mirrored)
- 2x USB to MCUs
=> 10 pins min, 26..32 pins optionally in total

### PWR-Module

Header

- GND
- 3 inputs (Enable, 5V, <= 17V)
- 4 Output (L3V3, -6V, L5V, 10V)
  - 10mV becomes part of Emu
- enable-signal (could also be on main PCB)

### EMU / HRV Module

Content

- MCU (maybe RP2350)
- DACs & ADCs, Current-Shunt

Header

- GND
- 4 voltages in (L3V3, L5V, 10V, -6V)
- **Variation A - MCU on Module**
  - 4 pins for host-link (i.e. SPI)
  - 1 pin Clock-Sync Input
  - 2 pin Output as Power-good-signal (or sync-channels for target)
  - Note: it might be more advantageous to keep the MCU off this module
- Variation B - 'dumb' standalone module
  - 6 pins to analog frontend (3 SPI, 3 SPI-CS)
  - 1 pin reset / enable (optional)
  - ~~(generalized) - no enable needed~~
- 4 voltages outputs (2 Rails, 2 Feedback)

GPIO-Budget

- 4+ pins for host-link
  - SPI? must manage 100 kHz * 2 * 32 bit = 6.4 MBit/s
  - due to FPU this could be 2x18 (raw) in both directions
- 6 pins to analog frontend (3x SPI + 3x CS)
- 1..2 pins for target selection (set once, 2 or 4 Ports)
- 1 pin reset
=> 12..13+ pins in total

Voltage-Rating of Current-Sensing-Input of Harvester

- R & C -> 50 V
- OPA189 -> supply 36 V max (+10/-6 V for us), input (v+)+0.5V
  - NOTE: opamp only drives between 0..5 V and it will pull down the sensing-input-line
- AD8421 -> max -Vs + 40 V = 34 V

### GPIO-Trace-Module

Content

- MCU (maybe RP2354B)
- levelshifter
- Current limiting resistors
- voltage buffer?

GPIO-Budget

- 4+ pins for Host-Link (SPI, or similar)
- 1 pin Clock-Sync Input
- 10..16 pins gpio-tracing
- 2..4 pins for direction selection
- 2 pins for logging power good (optional?)
=> 19..27+ pins in total

Programmer GPIO-Budget

- 4+ pins for Host-Link OR just USB
- 4 pins for programming (SWD, SBW, JTAG)
- 2 pins for direction selection
- todo: add boot-pin to enable automatic remote flashing?
- todo: always add debug-connector (swd + gnd)
=> 10 pins in total

## 4-Way Switching

- allows more targets

### Current 2-Way solution

NLAS4684 (for voltage-routing)
- dual SPDT Analog Switch
- 500 mOhm RDS
- 300 mA continuous, 500 mA peak
- < 10 nA leak (~1 nA for -55..25°C) -> important
- 300 pF additional capacitance on line
  - datasheet shows 330 pF (ON) and 104 pF (OFF), typical
  - rise-time with 1kOhm shows 434 pF trace-capacity (with ~40pF from actual traces)
- 1V8..5V5

-> replacement: 4 Way, >= 5.5 V, <<10 nA leak, <= 500 mOhm RDS, >= 250 mA continuous

PI5A4158ZA (for gpio-routing)
- dual SPDT analog switch
- high bandwidth, 150 MHz,
- 500 mOhm (less relevant)
- < 40 pF added capacitance
- +-40 nA leakage
- strange package
- 1V65..5v5

-> replacement: 4 Way, >= 5.5 V, high bandwidth >40pF,

### replacements

- for more target-ports (=4)
- TODO: look through old notes, update PI-Altium data

## RPi + RP2354B

Pi-40Pin-Header
- 28 GPIO, 2 SPI, 1 UART, SDIO

Pi4
- 1 GBE
- 28 GPIO, 5 SPI, 5 UART,
- CM4 has no usable USB, but raw PCIe 2x1 !
- runs stable, has enough power, cool to the touch

Pi5
- PCIe on extra connector, 5 GT/s
- requires 5.1V, 27 W
- pretty hot (~60°C) without sink
- RP1 handles most IO - not well documented ATM
  - triggering sync-gpio from kernel-module is harder (TBD)

- RP2350
  - pin 50..56 seems to have quad SPI (separate from GPIO)
  - USB1.1 Controller, Full Speed 12 Mbps
  - 30+ GPIO

```ad-todo
- determine max SPI-Speed (rpi4-to-RP2350)
- determine max usb-throughput (rpi4-to-RP2350)
- do a demo pcb
- pcb for adapting new target
- firmware-update-options for RP2350
- RP2350 needs a big FIFO, option: program MCU directly and use large QSPI-Flash for
  - FRAM SPI Flash
  - but also RAM via SPI,
- pio example available - 48 MHZ, 8 bit wide, 380 Mbit
  - pio - fifo - dma - ram
- option for interface RPI - RP2350
  - direct SPI
  - ~~usb1.1 Full-Speed~~
  - RPI - usb3 - usb3-hub - ftdi QSPI - RP2350
  - parallel interface
  - cypress - usb2 480 MBit - free programmable - i.e. massstorage -
    - https://www.infineon.com/cms/en/product/universal-serial-bus/usb-peripheral-controllers-for-superspeed/ez-usb-fx3-usb-5gbps-peripheral-controller/
    - cyusb301### costs 20€/IC
    - usb-analyzer: https://www.ellisys.com/products/usbcompare.php
  - sdio
- Test:
  - RP2350 - serial usb firmware - max output - receive per terminal -
    - rpi should ask interface regularly, buffer on RP2350 should not overflow
    -
- SDIO is documented in https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf, Chapter 4, Page 60
```

### Power-Output to Target

- req: 200 mA

### Improve Noise-Performance

- what did the uCurrent do?
- https://github.com/joeltroughton/uSMU
- jule counter of tegBed -> can we offer millivolt range with enhanced res?
