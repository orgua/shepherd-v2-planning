# Cape v2.4 - PCB Changes

## Implemented Changes

- 74LVC2T45GS has too small pads ⇾ prone to errors (very hard to see, but shorts under IC in all cases)
- drc-rule: Force proper Fanout with Neck-Down (<=100%) ⇾ EC seems to extend solder mask expansion on its own
- drc-rule: increase solder mask sliver (Gap) >= 0.2 mm
- drc_rule: solder mask expansion default 0.04mm (was .06) ⇾ with manual override for fine-pitch footprints (min. 0.005 for 0.35mm-Pitch)
- drc-rule: silk from pad distance >= 0.08 mm
- paste mask pad fill ~ 66 - 80 % (30% reduction), thermal pads ~ 50-60% (45% reduction) for 100um Stencil
- paste mask minimum dimensions 0.26 * 0.30 mm (T3 Paste with 25-45 um Balls), only exception: 0.35mm-Pitch part and small BGA with round d=0.25 Cutout
- move ~1/3 of paste to not under IC
- silk more symmetrical, cleaner and helpful
- rework footprint-lib accordingly
- feducials can go, are on outer frame
- reverse order of diode & shunt in harvester ?? No, seems fine currently
- rotate harvest port in schematic to reflect board layout
- add usb-c to pcb and ditch BB-pwered mode?
- emulator FB-Resistor-Switch can be removed
- ADC RVS-Pin not needed, remove TPs
- revisit datasheets for lower noise suggestions
- A5V needs 1mF, +10V gets 1x more 47 uF, -6V gets 100 uF
- remove coils for 6V, 5V, 10V, -6V
- bring sense- / FB-line directly to target-por ⇾ NetTie
- testpoints don't need gnd - its all around
- hrv-sense directly at pin, netsplit, also FB-lead
- EMU, replace opa388 with opa189 for main-line
- raise 6V to 6.2V (from 5.4), 578k + 100 k (or 680k)
- Pin1 on Headers not clear ⇾ direction 1 2 ... put mark directly under pin1, in direction of pin1&2
- 74LVC2T45GS
  - dir is referenced to VCCA ⇾ switch side with GND
  - QFN-Pinout is wrong! <https://4donline.ihs.com/images/VipMasterIC/IC/NEXP/NEXP-S-A0002881467/NEXP-S-A0002881253-1.pdf?hkey=6D3A4C79FDBF58556ACFDE234799DDF0>
- harvester
  - ADC-IN: R22 low but not 0, C140 to 1 - *10nF, R16 & TP6 same
  - DAC-OUT: R27 to 33R - 100R, C36 to 1 - *10nF
  - Drain: R20 lower ⇾ faster response to nonlinearity (diode-voltage from PU to PD)
  - VSense: remove R18 1k
  - ShuntBuffer C35 can be 10 - 100nF
  - update to latest profilings
- 5V to BB before the Inductor? Yes
- 1uF should be X7R (not X5R), check others
- 1mF to 6V and A5V
- Sense-Resistors with lower PPM/K - Value, higher precision
- emu
  - OpAmp FB 2k/1nF is 20% better than 1k/1nF (current, smu), 5k also improves on that (+10%), but might be too slow
  - ADCIn-LPF 33R, 10nF is a good compromise, 4% better tan 100R
  - Shunt-Buffer 10 nF is 10-20 % worse than 100nF unlimited but similar in limited space, 570nF is 3-5x worse than both
- External LED-Button-Connector S4B-ZR-SM4A-TF ⇾ Top Entry type: B4B-ZR-SM4-TF
- order new parts:
  - usb-connector, 2x 5.1k R,
  - more Opa189
  - HRV 3x 10nF, 2x 33R, 1x 1nF
  - 100R (1HRV
  - EMU 1x 33R, 3x 10nF,
  - 1x 680k (6V)
  - 39x 1uF X7R
  - 1x 100R 1% 100PPM
  - 50x 100nF 25 V
- [ADC can use 2x more 10uF on ref-pins] ⇾ NO, skip this one, had min to no effect
- add >16 V Cap to BOM, or 2x ~10V ⇾ wurth, see orderlist ⇾ lifetime,
- new 100nF to +10 - 6V directly, 2x
- more pads for Caps on backside
- big 0402 caps near device ⇾ don't bother with 100nF or smaller ⇾ NO, skip this one, ESR / impedance is better on smaller values (same package)
- change 0402 footprint, bring pads closer together
- ref-input for InAmp AD8421 (voltage divider + op1177)
- emu, use free opa388 for reference voltage offset, 5mV (60uV input offset * 50 + 400uV output offset) ⇾ 33R || 10k + Cap
- 10nF <should be NP0, but this seems expensive
- level-translators need to reach 1MHz, 1kOhm is limiting to ~200kHz, 2x 400 Ohm is more fitting
- correct op-fb
- 10uF should be X7R, but X5R has now 16V, X7R will be <6V? (ADC-Bypass) ⇾ Skip

## Changes in Layout

- LATER:
- try V-FB without C ⇾ same for Emu-OpAmp, tune emulator similar to harvester
  - <https://e2e.ti.com/blogs_/b/analogwire/posts/do-it-yourself-three-ways-to-stabilize-op-amp-capacitive-loads>
  - just using R_ISO would have the lowest noise ⇾ but unstable
  - R8 5k is slower for current changes
  - ⇾ best would be to increase shunt-resistor back to 10 Ohm BUT maybe this is no problem after the OpAmp-Swap
- remove 10R by just using 33R?
- switch back to 10 R shunt with 1k1 Ohm RG ?
- add option to supply Opa2388 with noisy 6 V

## New Components

- SPDT Switches Pi5... & the other Test ICs (DG612, DG2501)
- 470 Ohm 1%
- 2x 0R & 100nF
- new NP0 10nF
- Kai, <https://www.mouser.de/ProductDetail/Nordic-Semiconductor/nRF-PPK2?qs=sGAEpiMZZMv0NwlthflBi%2FwrKI1rLznmCjMIzu8H1xs%3D>
- replace corrected BOM-parts
