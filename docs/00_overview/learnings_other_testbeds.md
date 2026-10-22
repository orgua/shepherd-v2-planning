# Learnings from other Testbeds

- notes from meetings with creators of established testbeds
- with pitfalls and (possible) Solutions
- significance for shepherd is incorporated

## Server

- have an upgrade path
  - currently TUD/ZIH offers vServers and plenty of Storage from its datacenters, can be changed, expanded
  - current server: 2 Cores, 4 GB RAM, 50 GB local Storage, 10 TB network storage
  - vmware-tools have option to set cores and ram to 64 (for privileged users)
- avoid windows OS
- splitting servers can be an option (storage with message broker, web-interface, computing)

## Data-Management

- database (not a must)
  - allows easy analysis of data
  - immediate access is nice! real time or direct access for devs (even jupyterNB)
  - needs lots of RAM
  - easiest interface is a socket with json-interface ⇾ inefficient for embedded systems, can often be avoided
  - can produce downloadable data on the fly (at least csv)
- hdf5 / raw-data
  - needs more custom code
  - analysis not available right away
- database-choices
  - influxDB allows nanosec-timestamps as a series
  - postgreSQL works for weeks
  - timescaleDB, inlux competitor, seems to scale better with large number of devices (>1000)
- leave headroom, node-resources can easily become the bottleneck
  - using third party libs is always a good idea, but can come with performance penalties
  - usually compute-load can partially be moved to server
  - there are often performance optimized forks of established libs around (if needed)
- established ways / libs to stream data out
  - protobuf (can be slow for python)
  - rabbitMQ / kombu
  - RPC
- is privacy is feature? avoid personal data (OAuth, ActiveDirectory), make recorded data private (even only delete-access for web-admins)
- grafana seems to have trouble with big datasets

## Nodes

- lockups ⇾ powercycle
  - we (shepherd) may not have the chance to control POE
  - there is an external watchdog on the shepherd-capelet
  - there should also be a watchdog integrated in cpu (untested)
  - until now i (ingmar) had no trouble with the nodes, software base seems solid
- heat through sun, radiators, enclosure
  - degrades cpu, storage
  - BBone stays below 40 deg, case will support convectional cooling
- avoid storage without wear-leveling
  - sd-cards are not up for constant data-storage (and industrial SLC-Versions are expensive)
  - large usb-sticks tend to have wear leveling ⇾ ours probably hasn't
  - BBone has eMMC for the linux image, support for wear leveling is unclear
  - filesystems like F2FS have a software-based wear-leveling
  - possible solution
    - keep results in ram (avoid local storage bottleneck) and stream to server
    - use usb-stick for local storage of energy-traces (more static data)
    - keep system read-only (only deactivate for updates)
    - have replacement BBones at hand (automate installation)
- collect logs
  - gives debugging-hints in events of unwanted behavior
  - temperature, ram-usage, cpu-usage, ...
- target repurposing
  - keep functionality general so it can be used for dev, testing, ...
  - shepherds nRF-Target already has more gpio on edges and optional usb-port
- alternative platforms (copy from 11_concept_hw)
  - zynq (arm-cores + FPGA + shared mem)
    - pro: similar price as BBAI, 1 GBE, FPGA in same Package, hw-timestamping
    - con: xilinx-toolchain, documentation is overwhelming, community small, long dev-cycle
  - embedded amd platform (v2000)
    - pro: compute-power, relatively cheap (>= 200€), fast ethernet, x86-64
    - con: real-time not out of the box, low gpio-count
- slow software controlled GPIO could be a disadvantage
  - sensor and actuator control can have tight timing constraints
  - BBone PRU can also take control over gpio (but this is static / boot time decision)
- observer should always have control over target-reset
  - shepherd can control soft-reset over jtag/swd
  - shepherd can cut power and power-cycle target
  - add resistor bridge just for safety

## Web

- flask-framework is sufficient (same with bigger brother django)
- user-management should also include groups (to share data-pools)
- experiment-scheduler could be done with rabbitMQ (message broker)

## Testbed

- secure against miss-use
  - nodes can vanish, wander
    - fixate the boxes :)
    - make them unobtrusive (glue below desk, non-transparent-case)
    - BUT be transparent about the function
  - user-scripts can get system-access (heavy cpu-load, buffer-overflow, damage linux-partition)
    - put in sandbox
    - limit py-code to shepherd-framework / no other libs
    - run as special user - only essential permissions
    - set to lowest cpu-priority (nice-level)
  - voltage source could destroy hardware
    - gpio- and supply-voltage for shepherd-target are always linked
    - target-pcb has over-voltage-protection
    - experiment-management will check voltage of emulated regulator to match target-constraints
  - sanity-check everything!
  - real world testing required
- maintenance / development can easily occupy 1P full time
- documentation for the next devs

## TODO

- try to design low maintenance, multipurpose, high functionality / speed / quality
- Filesystem
  - f2fs for usb-sticks
  - find read-only-switch for system partition
- is there an easy way to integrate a fresh BBone into the system?
- test target-programming with current shepherd design
  - pyOCD could be an alternative
- BBone
  - is cpu-usage really 70% during emulation?
  - do a performance profiling, find bottlenecks
  - raw data could be sent server, less overhead for BB
