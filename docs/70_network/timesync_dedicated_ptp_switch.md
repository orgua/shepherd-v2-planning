# PTP-capable Switches

## Switch Comparison

- current tests: 2012 Cisco Catalyst 2960-S / WS-C2960S-24PS-L
  - ~ 11 us path delay (ptp4l)
- testbed: Cisco Catalyst 2960-X / WS-C2960X-48FPD-L
  - 48 Ports, 1 GBE, 2x 10 GBit SFP+
  - 740 W PoE+
  - remote: SNMP 1, RMON 1, RMON 2, RMON 3, RMON 9, Telnet, SNMP 3, SNMP 2c, HTTP, TFTP, SSH, CLI
  - 2500 €
  - -X version seems to be the newer Model (compared to -S) with layer 3 routing and >doubled spec
    - <https://ipwithease.com/cisco-2960-x-vs-2960-s/>

## PTP-Capable Switches

- D-Link DGS-3630-52PC
  - <https://www.bechtle.com/shop/d-link-dgs-3630-52pc-si-poe-switch--4292164--p>
  - 3770 €
  - 4x SFP, 4 SFP+
  - Gigabit L3 Switch, 48 Ports, 370W POE+
  - ptp is listed as supported in the management-tab
- Cisco CATALYST 9300L 48P POE
  - <https://www.future-x.de/cisco-catalyst-9300l-48p-poe-switch-power-over-ethernet-p-6649022/>
  - 5907 €
  - 4x SFP+ Uplink
  - Gigabit L3 Switch, 48 Ports, 505 W POE+
  - ptp seems to be supported: <https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/q-and-a-c67-744007.pdf>
    - needs "network-advantage" packet
    - <100ns is expected
- juniper switches

## TODO

- does the catalyst 9300L fit into ZIH-Infrastructure?
  - ZIH confirms compatibility and offers to help configuring the box
- can we get a test-device from cisco?
  - ZIH has no device but connected us with the local account manager
  - request was sent to cisco
