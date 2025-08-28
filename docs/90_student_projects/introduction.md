# Introduction

The [issue-section](https://github.com/nes-lab/shepherd/issues) of the main-repo contains a roadmap of future implementations that are planned for the testbed. A subset is suitable for student projects. Some even qualify to be used as topics for a bachelor or master thesis.

Projects with detailed sub-pages:

- (Web-) [dataviewer for recorded traces](./implement_dataviewer)
- replace [Fifo-system between userspace & pru](./improvement_for_memory_interface)

The sections below are a rough description of possible topics. [Contact us](https://nes-lab.org/) for more details.

## ~~Concept for externalizing IO Sampling~~

- High-Speed, high temporal resolution (>= 1 MHz, <= 100 ns)
- FPGA or MCU as Interface in front of SBC
- optional: bidirectional (also actuating pins)
- example from Flocklab: <https://github.com/ETHZ-TEC/RocketLogger>

## Optimize Network Topology of Testbed

- find and characterize interesting topologies (multi-hop, ring, mesh, ...)
- layout-optimization to include topos as subnets (while keeping node-count small)
- bootstrapping - how to start (with smaller number of nodes)
- optional: consider different PHY (protocol or target dependent)
- link-measurements or channel characterization could be a baseline for research

## Target-Design (more practical work)

- motivation: one free port on shepherd
- what system to choose, feature-set
- survey: what is popular, missing or growing in science-community
- first orientation could be flocklab or <https://www.iot-lab.info/>
- examples for possibles PHYs: lora, wifi, 15.4, uwb
- design, validation of PCB

## ~~Virtual Source Re-Implementation~~

- motivation: change of platform removes a lot of constraints and offers new capabilities
- platform: was Beaglebone + PRUs -> raspberry 4+ & external MCU (i.e. RP2040)
- PRU of Beaglebone
  - no FPU, proper Div or Mult
  - limited RAM and ProgSpace

## Optional time-sync Strategies

- idea: when ptp and gps are out of reach
- DCF77: reference implementation using arduino and a 5 € DCF-Module: <https://blog.blinkenlight.net/experiments/dcf77/local-clock/>
  - phase-detection enables high-res time sync
  - what min error would be possible?
- alternative: lora heartbeat or similar rf-signal to sync on
- interesting for far away nodes (uwb) ⇾ distant subnets that can't use ptp via LAN
- how to correct for error introduced by physical distance?
- topics could also include: antenna design, module concept, control loop optimization

## ~~Cape Redesign - HowTo - Feasibility-Study~~

- characterize constraints
- survey of SBC with included feature-set

## Concept for measuring / recording energy environments

- statistically valid data
- how to scale (50 .. 80 .. 100 nodes)
- sounds easy, but goes in depth and is on master-level

## permanent RSSISpy-Streamer

- currently RSSISpy sends data out via UART - which has some downsides
- FTDI offers (quad) SPI-to-Host-ICs which offer a large bandwidth without the downsides
- nrf-datasheet says: rssi only valid when rx is on -> otherwise run out of spec
- radio on, rx on by setting a 32bit receive address, grab RSSI-Samples - only active until that address was received
- 32bit address can be set to unlikely value, but it can still be triggered by accident / interference
- host
    - config ftdi chip
    - select rf-channel
    - start / stop
    - timestamping?

## Determine Timings of the nRF52 RF-Frontend

- motivation: synchronous transmission, sehr genaue sendezeitpunkte
- problem:
    - radio start-signal, delays bestimmen (verstärker an, einschwingen, usw.)
    - gleiche geräte können eventuell funktionieren -> unterschiedliche devices problematisch
    - nrf weist deutliche delays auf
- Bilder: 1symb/1us
- 1 Takt versatz im schlimmsten Fall 1/16MHz
- Aufgabe:
    - sende-delay nicht direkt beobachtbar
    - empfangsdelay nur zusammen mit sende delay erfassbar
    - wie rausrechnen?
        - A: verschiedene radios, gleichunssystem
        - B: messtechnik - ON AIR beobachten
- Messung0: gpio versatz, tx erzeugt flanke - rx routet gpio durch PPI und gibt es auf anderen gpio -> Versatz messbar
- Messung1: , empfänger vs sender, sync, eventuell auch ON-AIR
- RSSISpy - Repo mit tutorial für main.c mit spy im packet layer, 17 vs 70 kB
- Logic pro verifizieren - gps PPS
- -> Email mit SideInfo von Carsten
- [https://devzone.nordicsemi.com/f/nordic-q-a/83778/undocumented-tx---rx-radio-delay](https://devzone.nordicsemi.com/f/nordic-q-a/83778/undocumented-tx---rx-radio-delay)

- Timings des rf-frontends vermessen
. Fmag ist Fabian, car bin ich.
