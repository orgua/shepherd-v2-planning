# V2 Requirements (2020)

## Testbed-Infrastructure

- 12 - 30 nodes ⇾ depending on budget calculations
- distributed on one floor, several rooms
- use own infrastructure or parts of the university
- dedicated server or (better) use infrastructure of ZIH
  - contains: user data, web interface, shepherd controller
- WIFI + other RF-Standards as controllable interference
- support for channel monitoring, either packet- or spectral-based

## Test-procedure

- only 1 experiment, no concurrency
- reservation with calender-tool
- internal tests have higher priority

## Hardware - Cape & Capelets

- `>=2` Target-Ports with preselection before measurement (software defined targets)
  - nice to have: second target continues to get powered, so there would be a choice to support two different targets or one target and a monitoring device
- record traces for >= 4 Target-GPIOs (better 8 - 16), if 8 then 8+1 would be perfect
- Target-GPIO-Connection bidirectional, usable per script
- Target-UART-Connection support for several baud-rates, if possible >= 1MBit
- additional synchronous serial interface (i.e. SPI) for target
- mostly standardized data interfaces to all kind of targets
  - SDR-Target (with user programmable FPGA)
  - interferer
- reliable timebase (<=100ns deviation)
  - support for external sync-Line
- support for other Targets beside nRF52 (i.e. Long Range) and programmer (JTAG, SWD, ..)
- mobility of nodes (low prio), means two things moving system as well as distant long range nodes
  - req 1: tcp based (mobile network) for control-side-channel
  - req 2: scheduler via pre-configuration (node needs access to time-base)
- virtual capacitor and DC-Converter (real ones are either removed or bridged)
  - harvesting-traces remain basic input source
- support for On-Off-Pattern for power source (capacitor is currently interfering)
- Remote-Debugging not needed
- recording of harvesting traces not part of big testbeds → saves some money for parts
- variable TX-Power for multi-hop-scenario
- simple and fast to modify casing is ok

## Software - Script-Support / API

- support user-contributed energy-traces for targets, also offer preselected default ones
- support individual energy-traces per node
- control GPIOs (copy, for reference)
- dynamic addressing of targets (firmware-manipulation before flashing)
- API modular and encapsulated ⇾ separation between scenario and measurement, for reusability
- allow switching between targets

## Software - Website / Frontend

- user-management, permission / role management
- Quota
- authentication via external service like OAuth (i.e. Github)
- Upload: Scripts, Harvesting-Traces, Firmware
- Scratch-Area for user-data
- integrated tests for measurement: test for plausibility, pre-run in software (abstract virtual hardware)
- scheduler for measurement, time to prepare and follow up (data transfer, conversion, compression, ...)
- manipulation of target-firmware to individualize ID and TX-Power
- results downloadable by user, for a certain time
- feedback via e-mail - measurement start, data available, error, shortly before deletion
- grafana-visualization
- documentation and instructions
