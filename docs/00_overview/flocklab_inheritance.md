# Inheriting Flocklab

## The Package

- 30 complete observer-nodes (current deployment)
- one laptop as server
- and / or 25 boards as extension, replacement or second flocklab-testbed

## Current State

- flocklab is open-source, with no plans to commercialize
- testbed is very mature and stable (nodes only fail rarely, 1 node in 2y)
- most maintenance is for (new) users that break the interface or services (in a novel way)
- software is consisting of

  - observer: python 3.4 scripts, c programs, pru firmware (rocketlogger and one pru completely programmed in assembly)
  - server: python scripts, php web-frontend, mysql-database, xml-parsing
  - flocklab-tools: python-lib for uploading experiments, analyzing and visualizing data
- some things to be aware of

  - system is mature, but software is aging slowly for ~ 4 - 6 years
  - flock-beaglebone uses debian 9, kernel 4.14, python 3.4 ⇾ should be separated in a network with no internet-access
  - there are no unittests!
  - some things are destined to fail, ie. for experiments there is a 1 minute setup and finalizing phase, after that the next experiment can run. but with power traces enabled the data collection from the beaglebones creates high cpu-usage and may crash the followup experiment
- relocation overhead was seen as minimal - mostly changing the URLs and bringing the server online
- Stats (2022-6)

  - 35 active users, last 12 month
  - 5 minutes mean test duration
  - with covid the usage decreased but it is rising again
  - currently 15 % utilization
  - most used modules (from high to low): serial, gpio tracing, actuation, power profiling,
  - most used targets: dpp2-lora, nrf,
- wireless energy traces were planned for special nodes, also interference-generators

## Why should we inherit Flocklab

- do we learn something from running it?
- do we plan to use it more frequently?
- there are two other interested parties / maintainers

## Flocklab Details

API: <https://gitlab.ethz.ch/tec/public/flocklab/wiki/-/wikis/Man/Services>

XML: <https://gitlab.ethz.ch/tec/public/flocklab/wiki/-/wikis/Man/XmlConfig#debug-configuration>

- it is possible to configure a test online, download the xml and use variations of it for later experiments

- experiments

  - 1 minute setup and finalizing time ⇾ copy data, start services
  - copying (scp) continues and may collide with followup experiment

- a lot of code is in scripts - 2 cronjobs, 1 SQL-DB (setup-script for structure in git), PHP Frontend

- rarely to no defects for sd-cards or emmc-storage

- GPIO sampling

  - written as ASM-File / firmware, 20 Cycles, 10 Mhz, but only shortly with full bandwidth
  - there are two buffers that are read from userspace ⇾ ~ 16 kB
  - 10 MHz only for short period of time ⇾ after that only ~ 500 kHz

- no unittests, only manual testing

- cleaner - for stuck and zombie threads / experiments

- visualizierung ⇾ bokeh, web

- rocketlogger is pru-code + analog frontend (8 channel, 24 bit ADC)

- sync with gps is sub 100 ns accurate

- sync with ptp is only < 10 us ⇾ most definitely caused by nw-switch

- adc for current measurement can capture single digit nano-amps - but noise is reducing resolution to ~ 100 nA

## Learnings and Homework for Shepherd

- flocklab backbone / infrastructure is not helpful for shepherd, but the mature APIs collect years of user-experience
- interference and wireless energy traces would be awesome to have ⇾ simulated channel environment would be best ⇾ without that the tests are not reliably reproducible
- targets

  - tmote target is good for publicity (msp430 + cc2420) but currently only rarely used
  - uwb - is coming, low power and standardized,
  - Lora important ⇾ but power draw is ~ 150 mA, +22db, sx1262+ ⇾ but there are ICs with only 14 dBm
- 16 stations with years of solar traces, before and after solar cell
- lower sampling rates are useful for users (less data, faster processing & download)
- uart should be available as plain text with start- and end-timestamp (postprocessing on server)
- frontend

  - updates and maintenance messages per email
  - high level overview for data useful ⇾ plots with bokeh
  - flockid variable of the taget-images will be patched with node-id
  - sweep for automated tests very useful ⇾ also add human readable fields (title & description) to encode documentation
  - netcat link to beaglebones ⇾ serial-interface to targets
  - User can choose which observer ID (fixed hardware ID) is part of the experiment ⇾ gets (re)numbered as node ID (also used as flockid for target-fw)
  - some or most logs can be compiled to one per experiment (currently one per observer)
- backend

  - testbed should collect hardware-id / cpu serial of targets and map out what kind of target is where
  - better error-management ⇾ log everything
  - beaglebone-status is not necessarily part of the user-data
  - gpio actuation (!!!!) with level, offset, period, count
  - unused modules (power tracing, ...) can really be turned of ⇾ saves overhead
  - use checksums for firmware and traces ⇾ reusable with that ID
- managed userbase with quotas seems like a valid approach
- beaglebones ethernet interface can lock up ⇾ bbbrtc unlock, long reset ⇾ josh.com
- add plausibility tests, ie. BBone pings server and restarts if not accessible
- writing in bulk to RAM seems important - as the PRU locks up the ARM-Core
- PRU: min & max cycles per loop for both PRUs
- simulation is interesting ⇾ only solar ? iv-curve ⇾ basic idea: take an embedded system, remove solar cell and connect it to our testbed
- sub ms sync - xx us - for debug traces
