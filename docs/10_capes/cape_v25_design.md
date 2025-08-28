# Cape v2.5 - PCB Changes

Status 2024-02: still not produced - maybe skipped for switching platform

## Implemented Changes v2.5a

- lower current-limiting resistors from 470 R to 240 R (see new target)
- emu U32 replace OPA189 by OPA388
- LP for InAmp AD8421 ⇾ 80kHz with 2x 100R, +2x 1nF to GND
- change invNr-Sys to solid white rect
- Emu - use 10mV Ref directly, without Switch
- Rec - use GND as Ref directly
- stabilize 10 mV ⇾ 1uF increase to 2x 10uF, 2R increase to 10R
- replace electrolytic Caps by MLCC (Optionals on Backside)

⇾ implemented in V2.5a - https://github.com/orgua/shepherd-v2-planning/tree/main/PCBs/shepherd_cape_v2.5a

## Implemented Changes v2.5b/c

- production optimized for JLC
  - 6 layer includes via filling & capping (type 7) -> optional as via in pad is not used
  - vias were reduced to 0.2 mm hole, 0.35 ring dia
- replace target header with 40pin edge-Connector
- add 17V converter (previously external)
- Screw-Connector now supports 7 - 17V
- remove XYZ - for this last version - testbed only
  - usb-input
  - harvester frontend
  - ~~external switch & LED~~
- pin-changes on BBB Sockets, documented in `shepherd-git/hardware/_deprecated/beaglebone_pinout_concept.xlsx`
  - P8_14 is GPIO7, was targets GPIO0
  - P8_17 is GPIO8, was targets GPIO1
  - P8_27 is pru1_GPIO8, was pru_uart_tx
  - P8_28 is pru1_GPIO10, in addition to PRU1-LED0 (switch to input)
  - P8_29 is pru1_GPIO9, was pru1_batOK (switch to input)
  - P8_30 is pru1_GPIO11, in addition to PRU1-LED1 (switch to input)
  - P8_37 is now controlling direction of gpio-group A
  - P8_38 is now controlling direction of gpio-group B
  - P8_40 is pru1_GPIO7, was pru_uart_rx
  - P9_14 is now controlling direction of gpio-group C, was EN_Recorder
  - P9_25 is free, was CS_ADC2_REC
  - P9_27 is PWR_GOOD_L, was CS_DAC_REC
  - P9_41B is PWR_GOOD_H, was CS_ADC1_REC
- Target mapping Changed!
  - Target-GPIO9..11 are now input pru0-r31 (P8_29, P8_28, P8_30)
  - Target_GPIO0 is now UART-RX
  - BBone Pins changed
  - PinDirections are different
  - new BBone to target mapping is in separate section below, it now supports recording 12 pins
- GPS-Sync-Header added

## Implemented Changes v2.5d

- BOM-Trouble
  - NLAS4684 / NLAS4684FCT1G not available at all
    - Analog Switch, Dual SPDT, 500 mOhm Rds, 300 mA continuous, 500 mA peak, <10 nA Leakage (1 nA for -55 to 25°C)
    - we still have **~200x NLAS4684MN**, so will switch to that for now (+ larger, safer package)
  - PI5A4158 / PI5A4158ZAEX currently not avail
    - Analog Switch, Dual SPDT, 800 mOhm Rds, ~40 nA Leakage, high speed ~150 MHz with < 40 pF
    - PI3USB102G: 4 Ohm, 5V5 max, 6 pF, **BUT** 200 nA leakage
    - PI5A23157: 10 Ohm, 6V max, 18 pF, **BUT** 50 - 1000 nA leakage
    - **PI5A4157 / 729-PI5A4157CEX: single channel version of same IC, but only larger SC70 package (2.2x2.4) available**
    - **729-PI5A4157ZUEX**: UDFN-Package, 1x1 mm, mouser totally hides out of life parts, is in stock
  - LP2989-3.3 not avail as VSSOP-8 / TSOP
    - switch to WSON?
    - **926-LP2989AIMM33NOPB**, same but double the price
  - 10k 0402 667-ERJ-2GEJ103X -> 603-RC0402FR-7W10KL
  - 5.1k 0402 667-ERJ-2RKF5101X -> 603-RC0402FR-075K1L

BOM-Additions:
- 60x 649-77313-802-46LF, header 2x23
- 10x 667-ERA-3ARW102V, 1k-0603-0.05%
- 10x 754-RG1608N-101-W-T1, 100R-0603-0.05%

Manual Mods (not final):

- xp: add 150R as LP for Emu-InAmp (~50kHz)
- xp: double C141, C3 (Emu around U32 Opa)
- xp: 10mV Ref input - C149 - 1uF + 10uF

TODO:
- software changes
- harvester seems a bit too fast - current is overswinging - see SM141K04LV ivcurve
- disable GPIO IO if voltage is cut (due to low_threshold)
- switch to usb PD with 12V?

## Errors of v2.5d

- button-connector has no paste on gnd-pads

## Pin Def

### Target Port - Cape 2.4

```
pru_reg     name            BB_pin	sys_pin sys_reg
r31_00      TARGET_GPIO0    P8_45	P8_14, g0[26] -> 26
r31_01      TARGET_GPIO1    P8_46	P8_17, g0[27] -> 27
r31_02      TARGET_GPIO2    P8_43	P8_16, g1[14] -> 46
r31_03      TARGET_GPIO3    P8_44	P8_15, g1[15] -> 47
r31_04      TARGET_GPIO4    P8_41	P8_26, g1[29] -> 61
r31_05      TARGET_GPIO5    P8_42	P8_36, g2[16] -> 80
r31_06      TARGET_GPIO6    P8_39	P8_34, g2[17] -> 81
r31_07      TARGET_UART_RX  P8_40	P9_26, g0[14] -> 14
r31_08      TARGET_UART_TX  P8_27	P9_24, g0[15] -> 15
r30_09/out  TARGET_BAT_OK   P8_29	-
```

### Target Port - Cape 2.5

```
pru_reg       name              BB_pin	sys_pin sys_reg
pru1_r31_00   TARGET_GPIO0/uRx  P8_45	P9_26, g0[14] -> 14 (also Sys/PRU-UART)
pru1_r31_01   TARGET_GPIO1/uTx  P8_46	P9_24, g0[15] -> 15 (also Sys/PRU-UART)
pru1_r31_02   TARGET_GPIO2      P8_43	P8_16, g1[14] -> 46
pru1_r31_03   TARGET_GPIO3      P8_44	P8_15, g1[15] -> 47
pru1_r31_04   TARGET_GPIO4      P8_41	P8_26, g1[29] -> 61
pru1_r31_05   TARGET_GPIO5      P8_42	P8_36, g2[16] -> 80
pru1_r31_06   TARGET_GPIO6      P8_39	P8_34, g2[17] -> 81
pru1_r31_07   TARGET_GPIO7      P8_40	P8_14, g0[26] -> 26
pru1_r31_08   TARGET_GPIO8      P8_27	P8_17, g0[27] -> 27
pru1_r31_09   TARGET_GPIO9      P8_29	-
pru1_r31_10   TARGET_GPIO10     P8_28   - !! PRU1-LED0, direction must be changed in DTree for debugging
pru1_r31_11   TARGET_GPIO11     P8_30   - !! PRU1-LED1, direction must be changed in DTree

pru0_r30_05   PWR_GOOD_L        P9_27     (was CS_DAC_REC), gets added to bit 12 for GPIO-Sampling
pru0_r30_06   PWR_GOOD_H        P9_41B    (was CS_ADC1_REC), gets added to bit 13 for GPIO-Sampling
pru0_r30_07   -                 P9_25     (was CS_ADC2_REC)
```

# solder paste

- loctite GC 10 only 100 g and more
- chip quik
  - SMDLTLFP 15 T4, 15g, Sn42/Bi57.6/Ag0.4
  - **TS391LT50**, 50g, T4 (20-38 microns), Sn42/Bi57.6/Ag0.4, Lead Free, No Clean, Thermally Stable, LOW TEMP 140°C
  - TS391SNL50, 50g, T4, Sn96.5/Ag03/Cu0.5, Lead Free, No Clean, Thermally Stable, 220°C
  - T4 (20-38 microns)
  - T5 (15-25 microns)
  - T6 (5-15)
  - SMDLTLFP10T5, 35g, T5, Sn42/Bi57.6/Ag0.4, Lead Free, Low Temperature
  - **SMD291SNL10T5**, 35g, T5 (15-25 microns), Sn96.5/Ag3.0/Cu0.5, Lead Free, 217-220C, refridge > 6 month, room > 2 month
  - good filters: https://www.chipquik.com/store/product_info.php?products_id=440012
- msp430FR-datasheet states compliance to jedec j-std-020 reflow profile
- ordered: 31 parts Target, SMD291SNL10T5, TS391LT50

# extra PCBs

- RP2350 - test - connector
- harvesting frontends
-
