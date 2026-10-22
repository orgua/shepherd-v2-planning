# Concept for the Testbed

## General Philosophy

- only as complex as needed
- most bang for the buck, not too expensive and too specialized design, hardware, etc
- possibility to build on your own
- unique selling point is the replay of energy (harvesting) sources and emulation of power converters with high temporal resolution

## Infrastructure

- ~ 30 RF-Nodes (Beaglebone with custom RF-IC) with Ethernet-Backchannel
- distributed on cfaed-floors, several rooms / offices, also on corridors
  - i.e. BAR II55 - II75, III50 - III80, II52 - II54, II40A-II43A (end in another dispatch-room)
  - we could use right side of ethernet-socket (largely unpatched for now)
  - Nodes should be secured by powerstrips (on the wall, under desk, ..)
- RF stays within ETSI Norms, mainly bluetooth (Nordic nRF-Modules) or other IEEE 802.15.4 based standard
- Nodes connected and powered via Ethernet-Backchannel, optional with PTP, QoS, POE-Support
  - preferred if Nodes are connected to one switch (in BAR II65) for low jitter for ~100 ns PTP timing-constraint
  - preferred if PoE could be controlled to shut down and reset nodes (mainly to safe energy)
- **ZIH-Response and -Requirements**:
  - Nodes need installed fusion-inventory (to scan for vulnerabilities)
  - no QoS on Campus ("has more disadvantages")
  - POE ⇾ Configuration-Access to Switch only when used exclusively for this vLAN
    - alternative: wake on LAN (WOL) ⇾ no native beaglebone support (BBAI unclear, but unlikely)
  - current Switches should have very low jitter under low load, time in ASIC-Stack ~ 300 ns
    - lower latency ZIH alternative: infiniband, not applicable for us
  - we can't use the cable canal (== structural change)
  - wifi is used on channel 1, 6, 11, self-managed with varying tx-power, often < 20 mW
  - nodes are allowed to use the 2.4 GHz Band without restrictions, ZIH also offers to disable Wifi on these channels either for one floor or based on a schedule (routers seem to have that option, but it is untested)
  - cisco switches offer "clean air"-Monitor-Service ⇾ for II57 it reports 100% Quality with < 10 % non Wifi
  - ports on corridors can be used but ZIH-Infrastructure has higher priority
  - nodes may not get direct internet connection (relayed)

## RF-Network-Design

- limit to one floor
- ring-structure (due to impenetrable II800) would be a nice novelty
- the 3 consecutive NES-Rooms should be center of a cluster / group (something like 7 Offices with 3 Nodes each)
- remaining network can be more sparse (1 in each office, or 1 every two)
- there could be nodes with higher tx power and special antennas to directly link II59 and II71 (cut through II800)

## Control-Server

- one control-server that contains: user accounts, web interface, shepherd controller, measurement data
- needs linux from debian-family, python 3.7+, ansible
- 4 - 20 TB scratch area
- Port 80 accessible from the internet
- manageable from the intranet
- needs access to vLAN of RF-Nodes (mostly ssh-based)
- **ZIH-Requirements**:
  - managed by ZIH with Centreon
  - for access from internet the server needs a security-concept ⇾ needs to pass Greenbone Security Manager Test (GSM-Test)
  - access via subdomain, cfaed, tu-website ⇾ SSL-Certificate
  - no SSH from Internet

## Data-Storage Constraints

- 1 node, 1 min ⇾ 54 MiB of measurement data
  - 7z compressible to 12 MiB (22%)
  - zip ⇾ 23 MiB
  - tar ⇾ 12 MiB
- 1 Hour, 30 Nodes ⇾ 100 GiB uncompressed

## Misc

- Casing in laser-acrylic or off-the-shelf case with custom front
  - input Marco: open and transparent is fine
  - Case should blend in, be passive and option to use powerstrips to attach it to wall or below desk
- dynamic roles of nodes ⇾ config can be "static" (network access, gps attached, mobile) ⇾ ansible-roles
- switching to BB-AI seems to be an important step, but price increase is 3.5 fold
  - focus is still on the PRUs, now 4 Cores
  - GBE is more than welcome
  - we get a more reliable power connection (type c instead of micro-usb)
  - CPU is hopefully drastically faster
    - BBB brings 995 BogoMIPS, 277 MIPS FP, 1600 MIPS Int (numbers from internet, see 25_improve_sw_linux.rst)
    - BBAI TBD
  - documentation and community is small, underdeveloped
- with vCap in mind, PRU would be best replaced by a teensy 4.1 (keep it simple) or same uController
  - teensy has lots of iO, SPI with DMA & FIFO, FPU, 600 MHz, 1 MB RAM
- web-interface should make clear that users are responsible to stay within ETSI-norm, no misuse, no out-of-boundary, monitoring and logging is active
- ssh-interface should also make clear about project, active monitoring and offer a contact-email
