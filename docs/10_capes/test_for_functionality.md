# Tests-Protocol for Capes

## Visual Inspection

Look for tombstones, shorts, missing components and parts with wrong rotation (diodes, ICs)

It's beneficial to take macro-shots of the untouched PCBs for later reference as it is hard to determine error causes once the PCBs are fully assembled, encased and deployed.

## Isolated Cape-PCB

- apply external power to PCB directly (current limited 5V via lab supply)
- initial consumption < 1 mA
- Pull Up EN_Shepherd (P8-13) with 3V3
  - consumption on 5V rises to ~71 mA
  - Power-LED below recorder should light up
- check generated voltages on board (marked at capacitors by silkscreen)

| Name | Expected Voltage | Comment                                   |
|------|------------------|-------------------------------------------|
| L5V  | 5.000 V          | Should be Spot On                         |
| A5V  | 5.000 V          | Should be Spot On (is L5V with pi-filter) |
| L3V3 | 3.300 V          | Should be Spot On                         |
| 6V   | 5.38 V           | \[5.29; 5.47] V with 1% Res               |
| 10V  | 9.73 V           | \[9.56; 9.90] V with 1% Res               |
| -6V  | -6 V             | \[5.94; 6.06] V with 1% Res               |

## Cape-PCB on BeagleBone, powered

- BB starts 390 mA on VDD-5V line, booted: 170-240 mA
- sudden 66 mA increase on shepherd EN is no problem for BB
- WD-Pins could be a problem - my current test-BB is sensitive for power-button and shuts down ⇾ use jumper?
- P8-43 or 44 is sensitive for input - BB does not boot when shepherd connects with these pins
  - both are for boot-config, BUT
  - LA shows that both pins are high even before 3v3 gets to the pins, lasts 7.4s for a fresh BB
    - P8-45/46 stay low during boot an later on
    - p8-41/42 are HIGH for the same 7.5 s on boot
- EN-Shepherd (P8-13) stays low during boot - perfect!
- a fresh BB is sensitive for boot-pin during operation, it will shut down! start by triggering boot-pin again. Reset does nothing during power-off
  - boot is high even before power-up. then low 2.3s until 3v3 come to pin ⇾ shutdown command (short low), but then stays high during power-off
    - react to shutdown seem to be controlled by software (important for watchdog)
  - reset is low, changes to high when 3v3 come to pin, when 3v3 go on shutdown, the pin also changes to low
- GPIO to target
  - GPIO 0 - 4 are working bidirectional
  - BATOK is always high (currently), pru-debug-answer shows it
  - uarx (target - right) shows 1.5V, TODO
  - urtx (target - legt) shows 3V, TODO
  - swdIO is inversed? low for 80ms instead of 10 ms high, or something is pulling
  - swdCLK is fine
- Noise from Outside (v2.0r1)
  - BB 5V Lines (both) show cutting 1V transients every 23.6 ms, around 400 us long (quickshot 73/74/80) ⇾ due to diode between both 5V-Lines
  - entry-filtering is not doing much for these rails
  - 6V has +120/-80 mV Spikes (qs77, 78)
  - 5V and 6V are only used as intermediate voltage steps
  - 10V +46/-30 mV
  - -6V +42/-30 mV
  - A5V +36/-28
  - 36 us, +-10mV Spikes, 500 ns long (qs82, 84)
  - ⇾ add a big external Cap on 5V
  - diode-connection between the two 5V-Rails could be the problem - there are no voltage-spikes over the diode, so the current seemed to be constant
    - without diode: Big Spikes are gone, 5V has now max -200 mV and other (qs85)
    - -6V & 10v & A5V are cleaner, delta 30mV (qs86-88)
  - a Cap, 1F 5V5, before the ferrites, does not improve the situation
- Performance (v2.0r1):
  - 0 to 5V Target A, with 1 kOhm Load, 75 us for 80%, ~100 us for 100% (QS92 & 94)
  - 5V to 0V T-A, ...., 75 us for 80%, 400 us for 100%?, qs93
  - Recorder is following, with 5V in, 1k pre-resistor, the op-amp switches from 0..5V with 20us period, shape of thin half sine
    - big voltage jumps take 1 to 1.7 ms, 0 to 5V, that's also the period duration for no active load
- Performance (v2.1r0)

Current PCB-Mods (v2.0r1):
    - P8-43/44 disconnected, messes with boot
    - P9-9/10 possible problem, unconnected for now
    - 2x 10k-PU from EMU/REC EN routed to 3V3 (easy) instead of 5V, ADCs still work
    - 2x 1k-PU for boot, reset pins, only on shep-pcb als external jumper
    - switched inputs of R13, Shunt of Recorder, 2 lines cut and rerouted
    - diode over reverse-pol-mosfet
    - 1k for LEDs ⇾ OK
    - 1 Level Translator fixed (single supply & lower threshold voltage ~ 900 mV)
    - (NO!) 5V_SYS switched over to 5V_VDD
    - 8 Ohm right before Shunt ⇾ stabilize

Current PCB-Mods (v2.1r0):

- switched target-power-lines between OP-Amp and switch
- 1 mF / 16 V Cap on 5V PCB-Input ⇾ helps stability during shepherd-enable
- change R15 (V_harv_sim), R8 (emu-rail_b) from 10k to 1k to bring lowpass to 160 kHz (6us) instead of 16 kHz (62us)
- incomplete list, see "44_hw_performance_v2.1r0"
