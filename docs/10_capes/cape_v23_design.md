# Cape v2.3 - PCB Changes

NOTE: this could also be the changes for v2.4

## Implemented Changes

- Power Analog-Switch U30 from BB 3V3
- stabilize ADC with 22 pF at Input ⇾ 60 kHz Fc
- stabilizing 1kOhm for VIOBuffer
- decide if rec & emu should be combined
  - more complex design
  - always complete package
  - reduced cost (~ 3*9 €)
  - emu gets voltage-measurement for free
  - ⇾ no for now
- ADC seems to act up sometimes after shp-EN ⇾ test in PRU, re-enable a couple of times ⇾ seems to be fixed with EN
- Pwr-by-BB does not work with current cape-revision ⇾ just add a switch?
  - switch for input power, 1 A, 5V Switch: <https://www.mouser.de/ProductDetail/Dialog-Semiconductor/SLG5NT1594V?qs=sGAEpiMZZMtxrAS98ir%252BsxAQ5ATuKOGcAYPhn0zy8SaYiCqL8FxMXA%3D%3D>
  - test shows that the unpowered watchdog is responsible ⇾ add another diode to also power WD from BB 5V OR power diode directly from middle-pad of 2-WayJumper
  - tests still show unreliable starting-behavior when BB-Pwrd (start on second try), hints at trouble with big coil & Cap ⇾ also implement the switch
- remove overvoltage-protection, due to space constraints
- ditch LSF-LevelTranslator, use 74LVC2T45DC,125 with directed pairs
  - 74LVCH2T45GT, holds, 1.0 * 1.9 mm Package: <https://www.mouser.de/ProductDetail/Nexperia/74LVCH2T45GT115?qs=jquClx72t9BCfx5QcUZHzg%3D%3D>
  - 74LVC2T45GN, without hold, 1.2 x 1.0 Package
  - 74LVC2T45GS, without hold, 1.35 x 1.0 Package ⇾ cheaper, more available
  - 4x100k-PU Array <https://www.mouser.de/ProductDetail/YAGEO/YC124-JR-07100KL?qs=o9qB%2F%252BVTi4WdZhClKs2MsA%3D%3D>
- programming biDir Pins
  - var1: skip leveltranslator and force 3v3 logiclevel, direct connection with analog Switch
  - *var2*: that one pin tdio must have a dir-pin ⇾ hard if PRU-Pins needed
  - var3: still use slow LSF0104 for programming pins (try TI-Version for a change)
  - ⇾ var2 is preferred if sys-gpio is working for programming, (YES, it is)
- GPIO to target, 7x GPIO, 2x UART (rx,tx), BAT_OK (tx)
  - how many gpio should be with variable direction? 2x2 rxtx, 5 static rx?
  - static-Dir TX: CLK1, TMS/CLK2, BATOK ⇾ 2 x 2 CH Translator
  - static-Dir RX: UART-RX, 4x GPIO, ⇾ 3 x 2CH-Translator
  - BiDir: TDIO1, TDIO2, UART-TX, 3x GPIO (4 Dir-Controlling Pins, 2 for programming, 2 for tx&GPIO and 2-4xGPIO)
    ⇾ could be bundled in TDIO/GPIO-Pairs for a 2 x 2CH-Translators (NO)
    - if possible don't share Dir-Pins between programmer / gpio
- possible extension of target port
  - programming pins are exclusive and don't have to be recorded/monitored ⇾ free pins should be used for additional gpio
  - a second target (with option of programming) would help for some usecases (MSP430 + nRF-Radio)
  - var1: analog switch on target-pcb for programming lines controlled by one of the gpio (exclusive or could still be used as gpio)
  - var2: analog switch on cape, 2x2 programming lines on target-port, also allows JTAG
  - var3: intermediate uC on target-pcb for programming targets talking with BBone over programming lines (very custom solution but cape is left untouched similar to var1)
  - ⇾ Var2 preferred
- WD-Wake needs longer Pulse
  - currently 20ms High-Pulse gets inverted, but tests show that > 130 ms are needed
  - var1: diode + RC-Filter could widen the Pulse
    - wake-pin supplies 1mA max
    - SIM: 100 nF / 1 M ⇾ 150 ms > 0.5V (On for MOSFET)
    - SIM: 1 uF / 1M ⇾ >>1s > 0.5V
  - var2: a single capacitor after the mosfet could suffice
    - BB-Schematic only shows a pull-down button
    - TPS65217C, PB_IN, Pin25, internal 100k PU
    - SIM: 1 uF from BB-START to GND shows 100ms delay for signal rise to 2.0V ⇾ sums to 120 ms
      - ~ 64ms in real test
  - ⇾ Var1 preferred, less dependent from BB-Design-Changes
- PUs on sys-side should also be powered by BB 3V3
- New Connector, 4x Pwr, 4x Prog, 10x GPIO ⇾ 18 Pins ⇾ 2x9 Connector
  - info1 ⇾ BB outer width is 54 mm ⇾ 27mm per module
  - info2 ⇾ BB width between headers is 43.2 mm ⇾ 21.7 mm per module
  - var1: remove mounting-holes and allow 2.54mm Connectors (2x 22.2 mm width)
  - var2: switch to smaller 2mm Connector, ~18mm width
  - ⇾ var1 preferred
- GPIO-PUs increase to 100k
- combine shield-pads for EMU & REC
- change Analog switch to microbump-version 863-NLAS4684FCT1G
- change back vias from 550/200 to 600/250
- add more decaps for level-translators
- Remove dedicated harvest-led ⇾ use pru0-LED for that

## Open Issues

- which rails would benefit from big Caps?
- emu-shunt should be stabilized with > 500 nF (and probably the others too)
- additional big Caps on Main-Rails
- Resistor Arrays?
  - 4x 100k <https://www.mouser.de/ProductDetail/YAGEO/YC124-JR-07100KL?qs=o9qB%2F%252BVTi4WdZhClKs2MsA%3D%3D>
  - others1 <https://www.mouser.de/c/passive-components/resistors/resistor-networks-arrays/?resistor%20values=100%20kOhms&instock=y&sort=pricing>
- Beta Tuning:
  - additional 1 nF Cap on Feedback LP, both paths
  - remove 100 nF parallel to shunt
  - give recorder equal layout
- optimize filters with noise-metrics
  - possible tradeoffs: speed of voltage-transitions, compensation of analog switch resistance
- finalize hardware (WD, filters, GPIO-Speed, current bugs)
- test harvesting-target
- get target naming A/B/1/2 straight. it is target 1/2 from now on!
- find reason for 2.3mA Offset
- diodes for coils if needed
- LED of PRU: dedicated pwr_good / harvesting on silkscreen

### Trouble with v2.3c - manual P'n'P

Fixed in v2.3d:

- better comments for parts, U- , L-, R-.... T-
- SLG5... 4pin-mini-package, improve pin1-point and pad-layout should be hinted at
  - also longer pads,
- optimize NLAS-BGA, silk-lines, maybe extend corner-pads, peek over ic-edge or add right angles in copper
- 74LV LVLTrans - longer pads, at least the 4 corner ones ⇾ maybe one package larger
- 0402 pads closer together
- u14 pads further apart
- the 3 new ICs ⇾ maybe back to larger package?
  - 74LV as QFN, end-of-life: <https://www.mouser.de/ProductDetail/Nexperia/74LVC2T45GM125?qs=sGAEpiMZZMtZ661ya8CuXWImkGMxfA6p9uS%252BIOJA%2FTA%3D>
- 1 C tombstone (below emu, above u19)
- level-trans seem to be shorted (densest pad-layout)
- some ICs are shorted ⇾ old paste

## Additional Parts

- 22pF for Emu-ADC
- 1k Ohm VIO-Buffer
- 9 74LVC2T45GS ⇾ 2CH LevelTranslators
- 1x SLG5NT1594V ⇾ 1A Power-Switch
- EN_CONV: R 10k, C 1uF
- WD: 2x NSR05T30XV2T5G, R 100k, C 1uF
- LVL-Trans: >20x 100k, 5x 1uF
- AnalogSwitch: 9x 863-NLAS4684FCT1G
- pinheader 2x18, 2x 649-1012938191801BLF

## Removed Parts

- OVP: 2x FB 0603, C 22 uF, R 10 k, Mosfet BSH105, Diode NSR05T30XV2T5G
- WD: R 10k

## Target Header Design

- GPIO 0            - dir1-pin / rxtx
- GPIO 1            - dir1-pin / rxtx
- GPIO 2            - dir1-pin / rxtx
- GPIO 3            - dir1-pin / rxtx
- GPIO 4            - always RX
- GPIO 5            - always RX
- GPIO 6            - always RX
- GPIO 7 - uart rx  - always RX
- GPIO 8 - uart tx  - dir2-pin / rxtx
- BAT OK            - always TX
- SWD1 CLK - jtag TCK   - always TX
- SWD1 IO  - jtag TDI   - pDir1-pin / rxtx
- SWD2 CLK - jtag TDO   - always TX
- SWD2 IO  - jtag TMS   - pDir2-pin / rxtx

## BBone Pin Changes

see `./PCB/beaglebone_pinout_concept.xlsx` for more details

### Changes

- p8-27 was pru-gpio4, now pru-uart-tx
- P8-39 was pru-gpio2, now pru-gpio6
- P8-40 now pru-uart-rx
- P8-41 now pru-gpio4
- P8-42 now pru-gpio5
- P9-17 only naming, swd1_clk
- P9-18 only naming, swd1_io

### New

- p8-31 / 32 now used for io-dir
- p8-33 sw_swd2_io
- p8-34 sw_gpio6
- p8-35, 36, 37, 38
