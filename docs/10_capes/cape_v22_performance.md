# Cape v2.2 - Performance

## Hardware

- 8 Capes without Recorder, produced by Egas
- Serialnumbers
  - unknown num ⇾ kai
  - 1191022, -23, -25, -27 ⇾ kai
  - 1191029 ⇾ debug-setup
- lend out to kai
  - 1 Cape with pinheader (unknown number)
  - 4 Capes with Long PinSocket (1022, 1023, 1025, 1027)
  - 2 + 1 + 3 Targets

## Initial Test for Functionality

- visual inspection OK
- External powered single cape (current limited)
  - disabled cape ⇾ draws 0 mA @ 5 V
  - 35 mA @ 5 V when EN-Pin is Pulled Up with 3 V
  - ⇾ no unusual behavior
- BB powered by bench-supply 5.1 V, ~ 350 - 400 mA
- Shepherd powered by BB, VIn 5.08V
- Main Voltages on enabled Cape

| Name      | expected V | Comment                    |
|-----------|------------|----------------------------|
| A5V/L5V      | 5.000 V    | Should be Spot On          |
| A3V/L3V3  | 3.300 V    | Should be Spot On          |
| 6V        | 5.38 V     | [5.29; 5.47] V with 1% Res |
| 10V          | 9.73 V     | [9.56; 9.90] V with 1% Res |
| -6V       | -6 V          | [5.94; 6.06] V with 1% Res |

- calibration with 10 uF (1206, 25 VMax, 16 nA Leak) on both Ports
- Generated Voltages on Target Ports ⇾ deviation is ~ 0.1 mV
- ADC Current-Readout is noisy, despite 10 uF Buffer
- GPIO pass-through:
  - gpio 0-8 and BATOK to TA & TB
  - unconnected pru-pins (p8-41to44) are not reporting activity ⇾ fixed
- GPIO-Speed-Test by programming a target

## Capes - fixed and tested

- 1191022: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO, gpio0 has also speed-fix
  - was used for debugging, some resistors are replaced instead of stacked during modding
- 1191023: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
  - 3v3 is a bit off with 3.275 V
- 1191025: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
- 1191027: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
  - 3v3 is a bit off with 3.286 V
- 1191029: boot-fix, stabile V_IO

## Debug-Investigation on 1191022

- BB still fails to boot when P8-41to44 are connected to cape ⇾ lines are separated by a analog switch?!?
  - switch is powered by L3V3 ?!?
  - drilling out the via above the switch and routing enamel-wire from capacitor of switch to 3V3-Source
  - BB is booting!
- current-readout is very noisy
  - add 470 nF over shunt, to get 570 nF ⇾ much better, Lowpass changes from 796 kHz to 140 kHz
    - this cap is bad idea!
  - 2 V rising stable in 6 us, falling in 10 - 16 us
  - add 1 nF over feedback-cap, to get 2 nF ⇾ no Large Effect
  - TODO: switch back to small feedback loop without switch?
- GPIO-Edges ⇾ BB - 1 k - 10 k PU, [33 R PRU] - LSF - 1 k - 10 k PU, Switch - TA
  - baseline test
    - BB-Source Low takes 50 ns from 3.3 to 0 V
    - TB-Receiv Low takes 2-3 us from 2 to 0.8 V
    - PRU-Recv Low take 300 ns from 3.3 to 0 V
    - BB-Source Hi takes 100 ns to 3.3 V (100%)
    - TB-Receiv Hi takes 20 us from 0.8 to 2 V
    - PRU-Recv Hi takes 800 ns from 0 to 3.3 V
  - ⇾ try 2x 300 R Series Resistance, @5V only slightly above (8.3mA) current-limit of BB-Pins
    - 330 R || 1k = 248 R, 430 || 1k = 301 R
    - BB-Source Low 60 ns, High 80 ns
    - TB-Recv low 1 us, Hi ~ 20 us
    - PRU_Rec low 100 ns + 700 ns, Hi 400 ns
    - signal on target side between seriesRes and Switch is similar to target-output
    - signal on sys side between seriesRes and LSF is slower (400 ns rise instead of 50)
    - RefA = 0.961 V, RefB = 1.526 V ⇾ fet-diode = 565 mV
  - lower RefB Resistor from 240k to 200k
    - TB-Recv low 1-1.5 us, high 15-20 us
    - RefA = 1.053 V, RefB = 1.611 V ⇾ fet-diode 558 mV
  - PU on both sides lowered from 10k to 2.1k, (= 2.7k || 10k)
    - TB-Recv low ~< 1 us, Hi 3-5 us
  - other ideas?
    - lower PU on both sides at least for uart & programming ⇾ 2.1 k seem to do the trick
    - capacity of line?
    - remove sys-series-resistor
    - disconnect pru-side
- WD is not starting the BB ⇾ Pulse too short

TODO: look for voltage-spikes on coils when turning off power

## Fixes for v2.2

- analog switch to pru
  - drill out via with <1mm drill, first layer is enough, trace from IC to Cap should stay intact
  - route wire from cap, through mounting hole to P9-2/3 (3V3 of BB)
- fast gpio-lines for swd and uart with stronger PUs, and lower series resistance
  - target side: on lower LSF (U12),
    - 10 k PU-Array, add 2.7k in parallel to lower 4 resistors, results in ~2.1 k
    - 1 k SeriesResistor-Array, add 100 R in parallel to lower 4 resistors, results in 91 Ohm
  - sys side:
    - same treatment for PUs, above P9-16, above / between P9-18/20, above left side P9-24, above right side P9-26
    - 1 k Series-Array, add 430 R in parallel
  - LSF - 1M parallel to existing 240 k on RefB ⇾ resulting 200 k
- stabilize current measurement
  - 22 pF to GND on amplified path, right before ADC ⇾ 22+5 pF + 100 k ⇾ 60 kHz
  - additional 1 nF Cap on Feedback LP, both paths
  - Terminate unused Ports with 1 uF
  - remove 100 nF parallel to shunt
- stabilize IO-Buf-Voltage
  - cut left trace between 10 R and 1 nF, add 1k
- summary: 22 additional 0402-parts, 1 removed 0402, 2 cuts, 1 enamel trace ⇾ ~ 1 h manual work

## Mods to close the gap to v2.4

- mostly emulator related, due to 10 already produced PCBs
- boost converter - raise voltage to >6V - R104 from 576k to 680k
- Emu
  - DAC-lowpass 1nF on TP3, after R5, same on TP2
  - ADC-Lowpass R10 100k to 33R, add 10 nF after that (on TP4)
  - Shunt-smoothing, C6 100nF to 10nF
- general improvement
  - switch enamel wire from 3v3 to 5vIn for analog switch that guards the boot-pins
  - extra kapton tape for enamel wire around mounting hole (possible easy short)
- EMU: try removing C3 1nF for more stable OpAmp-FB ⇾ bad idea
  - C3 200 pF
  - C3 1 nF ⇾ OK
  - R8 5k1 ⇾ OK, but should be lower
  - R8 10k
  - R1 5k1 ⇾ fine
    ⇾ final change: C3 stays 1nF, R8 & R1 now 5k1
- remove most of the coils
  - 10V ⇾ L13
  - -6V ⇾ L11
  - A5V ⇾ L7
- EMU increase shunt from 2R to 10 R (R9) and RGain R12 from 210R to 1.1k
  - lower noise, specially for low currents
- profiling shows:
  - 10k Feedback:
    - 0 mA load, 30 mVpp oscillation with 400 kHz
    - 40 mA load, 12 mVpp, no oscillation
    - 40 mA loadswitch, 320 mVpp drop for 40 us
  - 5k1 Feedback:
    - 0 mA load, 26 mVpp oscillation with 400 kHz
    - 40 mA load, 12 mVpp, no oscillation
    - 40 mA loadswitch < 200 mVpp drop for 25 us
  - 5V out @ 50 mA reduces Voltage to 4.27 V
    - 100 mV comes from 2 R Shunt
    - 20 mV come from trace after feedback-loop
    - remaining drop is due to 5V supply

## Profiling Emulator

### 2R Shunt

```text
SMU-reference: 1.000 mA @ 3.1999 V;   emu-c-raw: mean=5000.10, stddev=3.30 @ 3.200 V
SMU-reference: 5.000 mA @ 3.1998 V;   emu-c-raw: mean=24741.11, stddev=19.33 @ 3.200 V
SMU-reference: 10.000 mA @ 3.1997 V;   emu-c-raw: mean=49409.33, stddev=19.37 @ 3.200 V
SMU-reference: 15.000 mA @ 3.1996 V;   emu-c-raw: mean=74101.05, stddev=37.38 @ 3.200 V
SMU-reference: 20.000 mA @ 3.1995 V;   emu-c-raw: mean=98767.96, stddev=37.42 @ 3.200 V
SMU-reference: 25.000 mA @ 3.1994 V;   emu-c-raw: mean=123441.02, stddev=36.68 @ 3.200 V
SMU-reference: 30.000 mA @ 3.1993 V;   emu-c-raw: mean=148106.87, stddev=37.72 @ 3.200 V
SMU-reference: 35.000 mA @ 3.1991 V;   emu-c-raw: mean=172779.27, stddev=42.50 @ 3.200 V
SMU-reference: 40.000 mA @ 3.1990 V;   emu-c-raw: mean=197441.15, stddev=42.80 @ 3.200 V
SMU-reference: 45.000 mA @ 3.1953 V;   emu-c-raw: mean=222110.22, stddev=41.39 @ 3.200 V
SMU-reference: 50.000 mA @ 3.1811 V;   emu-c-raw: mean=246769.44, stddev=40.81 @ 3.200 V

SMU-reference: 1.000 mA @ 4.3999 V;   emu-c-raw: mean=4999.34, stddev=3.33 @ 4.400 V
SMU-reference: 5.000 mA @ 4.3998 V;   emu-c-raw: mean=24741.03, stddev=19.48 @ 4.400 V
SMU-reference: 10.000 mA @ 4.3997 V;   emu-c-raw: mean=49407.86, stddev=19.54 @ 4.400 V
SMU-reference: 15.000 mA @ 4.3995 V;   emu-c-raw: mean=74099.36, stddev=37.22 @ 4.400 V
SMU-reference: 20.000 mA @ 4.3994 V;   emu-c-raw: mean=98767.49, stddev=37.35 @ 4.400 V
SMU-reference: 25.000 mA @ 4.3993 V;   emu-c-raw: mean=123442.35, stddev=36.73 @ 4.400 V
SMU-reference: 30.000 mA @ 4.3992 V;   emu-c-raw: mean=148108.01, stddev=37.72 @ 4.400 V
SMU-reference: 35.000 mA @ 4.3863 V;   emu-c-raw: mean=172779.94, stddev=39.42 @ 4.400 V
SMU-reference: 40.000 mA @ 4.3481 V;   emu-c-raw: mean=197442.74, stddev=38.15 @ 4.400 V
SMU-reference: 45.000 mA @ 4.2972 V;   emu-c-raw: mean=222114.24, stddev=36.88 @ 4.400 V
SMU-reference: 50.000 mA @ 4.2273 V;   emu-c-raw: mean=246772.54, stddev=34.40 @ 4.400 V

SMU-reference: 1.000 mA @ 4.9694 V;   emu-c-raw: mean=4998.55, stddev=3.10 @ 5.000 V
SMU-reference: 5.000 mA @ 4.9209 V;   emu-c-raw: mean=24741.21, stddev=17.52 @ 5.000 V
SMU-reference: 10.000 mA @ 4.8602 V;   emu-c-raw: mean=49408.38, stddev=17.40 @ 5.000 V
SMU-reference: 15.000 mA @ 4.7982 V;   emu-c-raw: mean=74101.53, stddev=32.35 @ 5.000 V
SMU-reference: 20.000 mA @ 4.7337 V;   emu-c-raw: mean=98768.89, stddev=32.09 @ 5.000 V
SMU-reference: 25.000 mA @ 4.6663 V;   emu-c-raw: mean=123444.18, stddev=31.66 @ 5.000 V
SMU-reference: 30.000 mA @ 4.5959 V;   emu-c-raw: mean=148110.96, stddev=32.14 @ 5.000 V
SMU-reference: 35.000 mA @ 4.5221 V;   emu-c-raw: mean=172783.01, stddev=34.65 @ 5.000 V
SMU-reference: 40.000 mA @ 4.4440 V;   emu-c-raw: mean=197444.95, stddev=34.46 @ 5.000 V
SMU-reference: 45.000 mA @ 4.3607 V;   emu-c-raw: mean=222116.58, stddev=34.18 @ 5.000 V
SMU-reference: 50.000 mA @ 4.2701 V;   emu-c-raw: mean=246776.35, stddev=33.46 @ 5.000 V
```

### 10R Shunt

```text
SMU-reference: 1.000 mA @ 3.2001 V;   emu-c-raw: mean=5130.99, stddev=3.16 @ 3.200 V
SMU-reference: 5.000 mA @ 3.2001 V;   emu-c-raw: mean=25605.70, stddev=21.25 @ 3.200 V
SMU-reference: 10.000 mA @ 3.1999 V;   emu-c-raw: mean=51186.94, stddev=21.20 @ 3.200 V
SMU-reference: 15.000 mA @ 3.1998 V;   emu-c-raw: mean=76793.88, stddev=40.36 @ 3.200 V
SMU-reference: 20.000 mA @ 3.1996 V;   emu-c-raw: mean=102374.39, stddev=40.14 @ 3.200 V
SMU-reference: 25.000 mA @ 3.1995 V;   emu-c-raw: mean=127962.74, stddev=39.88 @ 3.200 V
SMU-reference: 30.000 mA @ 3.1993 V;   emu-c-raw: mean=153542.74, stddev=40.43 @ 3.200 V
SMU-reference: 35.000 mA @ 3.1992 V;   emu-c-raw: mean=179127.57, stddev=46.09 @ 3.200 V
SMU-reference: 40.000 mA @ 3.1991 V;   emu-c-raw: mean=204702.33, stddev=45.85 @ 3.200 V
SMU-reference: 45.000 mA @ 3.1938 V;   emu-c-raw: mean=230285.98, stddev=44.23 @ 3.200 V
SMU-reference: 50.000 mA @ 3.1780 V;   emu-c-raw: mean=255859.07, stddev=43.50 @ 3.200 V

SMU-reference: 1.000 mA @ 4.4002 V;   emu-c-raw: mean=5130.41, stddev=3.24 @ 4.400 V
SMU-reference: 5.000 mA @ 4.4001 V;   emu-c-raw: mean=25605.84, stddev=21.32 @ 4.400 V
SMU-reference: 10.000 mA @ 4.3999 V;   emu-c-raw: mean=51186.59, stddev=21.36 @ 4.400 V
SMU-reference: 15.000 mA @ 4.3998 V;   emu-c-raw: mean=76798.10, stddev=40.39 @ 4.400 V
SMU-reference: 20.000 mA @ 4.3996 V;   emu-c-raw: mean=102378.49, stddev=39.93 @ 4.400 V
SMU-reference: 25.000 mA @ 4.3898 V;   emu-c-raw: mean=127967.95, stddev=34.89 @ 4.400 V
SMU-reference: 30.000 mA @ 4.3194 V;   emu-c-raw: mean=153545.53, stddev=32.60 @ 4.400 V
SMU-reference: 35.000 mA @ 4.2228 V;   emu-c-raw: mean=179133.17, stddev=33.42 @ 4.400 V
SMU-reference: 40.000 mA @ 4.1050 V;   emu-c-raw: mean=204707.56, stddev=32.38 @ 4.400 V
SMU-reference: 45.000 mA @ 3.9764 V;   emu-c-raw: mean=230292.51, stddev=31.78 @ 4.400 V
SMU-reference: 50.000 mA @ 3.8379 V;   emu-c-raw: mean=255862.87, stddev=31.12 @ 4.400 V

SMU-reference: 1.000 mA @ 4.9618 V;   emu-c-raw: mean=5129.80, stddev=2.93 @ 5.000 V
SMU-reference: 5.000 mA @ 4.8830 V;   emu-c-raw: mean=25603.63, stddev=16.67 @ 5.000 V
SMU-reference: 10.000 mA @ 4.7831 V;   emu-c-raw: mean=51188.07, stddev=16.38 @ 5.000 V
SMU-reference: 15.000 mA @ 4.6804 V;   emu-c-raw: mean=76788.55, stddev=30.26 @ 5.000 V
SMU-reference: 20.000 mA @ 4.5753 V;   emu-c-raw: mean=102370.88, stddev=30.14 @ 5.000 V
SMU-reference: 25.000 mA @ 4.4677 V;   emu-c-raw: mean=127964.19, stddev=29.70 @ 5.000 V
SMU-reference: 30.000 mA @ 4.3576 V;   emu-c-raw: mean=153546.69, stddev=29.32 @ 5.000 V
SMU-reference: 35.000 mA @ 4.2441 V;   emu-c-raw: mean=179136.95, stddev=31.96 @ 5.000 V
SMU-reference: 40.000 mA @ 4.1266 V;   emu-c-raw: mean=204716.23, stddev=31.68 @ 5.000 V
SMU-reference: 45.000 mA @ 4.0034 V;   emu-c-raw: mean=230304.75, stddev=31.84 @ 5.000 V
SMU-reference: 50.000 mA @ 3.8733 V;   emu-c-raw: mean=255879.39, stddev=31.02 @ 5.000 V
```
