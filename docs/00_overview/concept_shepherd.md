# Concept for Shepherd V2

A more detailed moved to [shepherd/docs/dev/v2_improvements.rst](https://github.com/nes-lab/shepherd/blob/main/docs/dev/v2_improvements.md)

## Overview

- (mobile) testbed for battery-less IoT
- observer-nodes for an IoT-Target
- works autonomous or time-synchronized with a network backplane
- "software defined power source", emulation of
    - harvesting source (pre-recorded, simulated)
    - regulator / converter - circuit
    - intermediate storage-capacitor
    - "software defined" is largely true, but changing basic behavior needs a deep dive into PRU-Code
- allows to experiment with emulated spatio-temporal energy availability
- recording of energy-traces ⇾ key-parameters like current-drain and (virtual) capacitor-voltage
- additional functionality: recording of harvesting sources (not part of testbed)

## Nodes

- embedded linux board with shepherd-cape
- time critical code runs on two real-time processors
- two targets-ports are available
    - both can be supplied with individual voltages, only one is current-tracked
    - general purpose IO, target selection independent of power-supply-selection
    - separate 3V3 line
- bidirectional GPIO on 10 channels, 2x2 lanes are currently reserved for SWD / Spy-by-Wire, UART
- Targets (currently planned)
    - nRF52840
    - MSP430

## Testbed

- 30 Nodes on one floor in a university office-building
- nodes powered via POE
- (optional) one PTP-Masterclock, Node with GPS
- 1 Ubuntu Control-vServer, 10 TB of additional Storage
- 1 experiment at a time, no concurrency
- Web-Framework
    - user-management (roles for admins and users)
    - experiment-management, configure and control, add data (see below)
    - experiment-scheduling, calendar (set active, start-time, duration)
    - data management / quota (retrieve / delete recordings)
    - authentication via external services
    - E-Mail notifications
    - testbed status, topology
    - (optional) grafana visualization of recorded data
    - (admins) server status, quota, testbed control
    - documentation and instructions
    - target-management (specify slots of nodes)
    - (optional) benchmark-management (post-scripts)
- user-provided data (experiment management)
    - (optional) energy-traces, IV-Curves
    - regulator / converter-config
    - target-firmware
    - (optional) python userspace script that interacts with gpio / serial

## Technical details

- BeagleBone Green with 1 Core for Linux and heavy use of PRU for low-latency code
- target-voltage 0 to 4.5 V, max 50 mA per Target
    - 16 bit DAC, LSB results in 76 uV
    - 100 kHz sampling rate, jitter max +- 90 ns, 95% Quantile is 60 ns
    - 18 bit ADC, LSB results in 19.1 uV or 191 nA
- speed of voltage-drive
    - DAC has 0.75 V/us slew and 7 to 10 us settling (error < 0.x %)
    - OpAmp has 5 V/us slew
    - following Lowpass has corner-frequency of 16 kHz
    - 10 kHz on-off-patterns should be well in range
- low noise & high precision design for analog frontend
- 10 shared GPIOs with system
    - bidirectional level translation works from ~ 1.3 to 5 V
    - line is driven by PUs, always matched to target-voltage (low power usage)
    - recording: sampling rate is asynchronous, between ~ 1 to 5 MHz
    - data throughput untested, but edges look fine for > 1 MBaud
    - leakage during operation < 2 uA from target-side
    - gpio can be turned off, < 10 nA leak from target-side
- data-rates
    - 1 min ~ >= 54 MiB of measurement data (more with heavy GPIO actions)
    - 1 Hour, 30 Nodes ⇾ 100 GiB uncompressed (hdf5)
- time-synchronization
    - in linux via PTP,
    - chip-select edge of two test-nodes have a maximum jitter of about +- 300 ns, 95% quantile is 160 ns
- external watchdog for wakeup / restart on
- network
    - Server has 10 GBit Link to Switch
    - Nodes have 100 MBit Link to Switch
