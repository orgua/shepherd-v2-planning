# Cape v2.1 - PCB Changes

## Implemented Changes

- level translators - implement single voltage supply
- smooth 6v-boost ⇾ larger capacitors 58uF to 158uF, ferrite, lower boost-voltage 5.38 V instead of 6.766
  - typical on A5V are 38mA for Quiet/On, 150mA max, mp3221 gives formular for upper thresholds of Vpp
  - old config: 164 uVpp (38mA) to 645 uVpp (150mA)
  - new config: 27 uVpp (38mA) to 104 uVpp (150mA) ⇾ effect of ferrite not included
  - LDO is rated for 60 dB dampening, but measurements show a factor of ~ 500x of ripple rejection
- 6V Regulator overdrive is edgy, sw-pin is good for +8V, currently there are ~ 7.14 V
- Target-IO-PUs - get powered by unmonitored voltage buffer
- add 3v3 converter (linear), because BB provides very noisy power (both 5V & 3V)
- make sure shepherd works (theoretically) with BB Black (not only Green) ⇾ Boot-CFG is identical
- recheck which IC gets which voltage (5V Sys is exceptional noisy)
- allow to run completely from external power ⇾ move sys-5v ferrite
- main power switch not needed
- mark ext input
- sensitive lines should get more distance from gnd-polygon
- consider ultra low noise ldo for -6 and 10V
  - No suitable 5 to 10V voltage doubler found (fast switching, low noise)
  - there are quiet inverters (LM27761) though
  - see "noise_performance.rst" for more info
- adjusted Pads of some footprints - reduce width a bit when solder resist was too narrow on ICs
- improve GPIO signal integrity (1k from target can be removed), 100k PU on Sys-Side replace by 10 k
- better buffer the io voltage, needs single OPA, but gets rid of one NLAS-Switch
- PI-Filter is bad for varying loads, so only use with dac / adc
  - keep 100 uF constant, but vary inductance to optimize voltage drop ⇾ << 1 mV
- external cables, filter and buffer (100nF)
- (NOT DONE) if there is enough space ⇾ switch out 47uH Coil of LC-LP to 150uF (larger)
- **gpio - RC lowpass** ⇾ Line-Capacity vs. current-limiting resistor
  - L1L2 distance 2x 180 um, e_r ~4.2
  - trace width 250 um
  - length BB-Side [50; 87], LVL ~ 17, Target-Side [13; 27]
  - C = e*A/d = 3.4 pF ⇾ max capacitance of 1 gpio-trace on shepherd-pcb
  - C_lvl = 12.5 pF
  - R = 1k
  - fc = 10 MHz (neglecting target and BB capacitances)
- re-evaluate spi-lines ⇾ fine
- via-fence near the lan-port
- QR-Code is readable, but still a bit messed up ⇾ negative
- target-connector-redefinition, bring GND to first and last position (EMV)
- (target) reset (P0.18) with Resistor bridge to gpio-header
- (target) remove more metal around antenna
- compare LSF-Versions of TI with nexperia ones ⇾ seems to be exact copy
- would 1000 Hz on-off-pattern be possible? YES
- (if there is time) - implement fixed recorder design

## Additional Parts

- lvl trans: 2x 240k, 2x 1M, 1x NLAS4684
- emu vSwing: 10R 0.1%, 1.1k 1%
- emu vDrop: NLAS4684, 100nF?
- A3v3: lp2989-3.3, 10nF X7R,
- VSenseStabilize: 1k
- 6V Stabilize: 576k, 100uF, Ferrite
- InAmp Stabilize: 100nF, 100k
- DNP: Ferrite 5V_SYS (for pwr-rerouting)
- 16VStability: 4x 33uH, 4x 10uF
- 20x 10k, Opa388, 100nF, 1uF
- removed: 1x NLAS, 2x Ferrite
- removed: 20x 100k, 10x 1k
- new: opa189 for recorder
- removed / rec: mosfet, 1M, 10k

## Power-Budget

- see separate spreadsheet (PowerConsumption.ods)
- BB takes <= 2W
- Shepherd MAX ~ 1 W (4mW @ 3V, 743mW @ 5V, 36mW @ 6V, 74mW @ 16V) (with 2x 50mA Target)
- Shepherd ON ~ 340 mW (4mW @ 3V, 190mW @ 5V, 36mW @ 6V, 74mW @ 16V)
- ON Quiet Current matches with reality (66mA measured, 68mA calculated)

## Open Issues

- additional PCB for POE
  - poe is noisy (up to 25 mVpp for TL-POE10R, 300 mVpp for NoNameThing)
  - switching regulator for 12/9 to 6V
  - linear regulator with proper noise resistance for 6 to 5V
  - OR just 2-Stage LC-LowPass (15uA / 770mA from previous Order), additional 100 uF
- fix layerwindows
- optimize position of current limiting resistors
- power-supply-pins? upgrade path to stacked pcb, because current space is already maxed out
- check / measure real reverse current of diode
- evaluate higher driving strength for Target-Supply
TODO:
- new coil is now 963-NR3015T3R3M
