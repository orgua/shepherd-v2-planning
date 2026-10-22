# Recorder Drain

conclusion from the future: voltage buffering OpAmp works flawlessly!

## Problem

- harvest source is weak, so it should be connected with low leakage
- current drain is a Mosfet, that can pull the source to the desired voltage
- mosfet is controlled by an inverted opAmp-voltage-buffer, resulting in a PWM-Controller that is smoothed out by a slow RC-Filter
- RC-Lowpass is delaying (big) voltage-changes by 1 to 1.7 ms
- second problem: opAmp is oscillating, there must be a better way

## Ideas / Approaches

- JFET
  - pro: larger resistive range than mosfet
  - con: negative voltage required, very little variety
- PID controlled Mosfet
  - controller can hopefully be reduced to just one OpAmp
  - con: very complex, tuning required
  - TODO: maybe there is just some integrator and a small proportional part needed
- Bipolar Transistor
  - TODO: can a BJT go into very high impedance? Seems not (small sample check)
- drain directly into output of OpAmp (voltage buffer)
  - pro: fast, clean, simple
  - con: no high impedance, could feed into a harvest source
- Switched OpAmp-Sink
  - Mosfet above OpAmp ⇾ would need voltage offset to control mosfet
  - analog switch would be a nicer solution than mosfet
  - con: could still feed into harvest source
- oneway OpAmp-Sink
  - Diode above OpAmp to stop reverse flow
  - could be included in opAmp-return-path (compensate diode offset)
  - high impedance (over opAmp voltage range) with a low leakage diode
  - con: still no (real) high impedance, needs dual supplied opAmp to reach 0 V

## Conclusion

- combined switched oneway OpAmp-Sink is a proper solution
- diode-solution should be fine
- WARNING for diode solution
  - watch out with power-levels mixed with enabled-states
  - if OpAmps VOut settles at V-, the diode will drain harvester below GND
  - V- could be higher than V+ in disabled state (LDO for Pos, BoostInverter for Neg)
