# Emulator Target Voltage

## Problem

- A: target voltage with current-measurement is unstable (oscillation for low voltage / low load)
- B: voltage buffer feedback is excluding the switch afterward

## Setup

- BB powered by bench-supply
- Target voltage drained by keithley source meter (current mode)
- target voltage is monitored by scope with probe in AC-Mode to analyze Noise

NOTE: part of the oscillation is probably also partly caused by the measurement setup ⇾ heisenbug

## Measurements for unstable Voltage

- VTarget = 0.5 V shows 10mVpp oscillation ~ 260 kHz
- VTarget = 1.0 V is stable
- other documentation is lost
- problem is fixed

## Measurements for voltage drop

- source current ⇾ TargetA Voltage
  - 0 uA; 2.9983 V
  - 1 mA; 2.9987 V
  - 5 mA; 3.0001 V
  - 10 mA; 3.0024 V
  - 20 mA; 3.0065 V
  - 30 mA; 3.0106 V
  - 40 mA; 3.0148 V
- drain current ⇾ TargetA Voltage
  - 0 mA; 2.9983 V
  - 1 mA; 2.9979 V
  - 10 mA; 2.9942 V
  - 20 mA; 2.9901 V
  - 30 mA; 2.9860 V
  - 40 mA; 2.9818 V
  - 50 mA; 2.9732 V

## Analysis of voltage drop

- side node: shepherd is able to drain power
- drain-experiment shows voltage drop of 25.1 mV for 50 mA ⇾ 502 mOhm Internal Resistance after OpAmp
- switch-datasheet claims 500 mOhm Rds_on ⇾ very close to measurement including traces
- influence of switch ⇾ 50mA @ 3V equals 60 Ohm ⇾ 500 mOhm are 0.83 % of that

## Conclusion

- A: oscillation can be fixed by bigger shunt-resistance
- B: voltage drop can be fixed by including switch into feedback loop ⇾ needs additional switch
