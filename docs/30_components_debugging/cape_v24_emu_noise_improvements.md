# Noise in Current-Measurement for Emu

**TLDR**: even after tuning, fixes and redesigns the noise level is higher than expected.

## Problem

- Cape PCB v2.4
- current measurement is noiser than expected

## TLDR - Proposed Design-Changes

- 10R shunt has no advantages
- buffer 10mV with 2x 10uF (C147, 148)
- increase LP for DAC & Opa with 2x +1nF (C141, C3)
- add LP to InAmp (2x 150R, 2x1nF to GND, 10nF mid)
- increase LP for ADC, C62, 100nF

## Measurement Setup

nrf-only target ⇾ SMU shows 19nA
nrf-msp-target shows 22nA ?!?

All @3V

- msp430fr    370 nA LPM4, RAM-off
  45 nA LPM4.5
- nrf52840    400 nA full off
- AB1805     55 nA with XTAL
  ⇾ expected target-deep-sleep of 500nA

## Measurements

```text
modded emu
	mean: 1.6004410204895745e-05
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018641925054200628
	si_converted: true
	⇾ real max 120uA,
	⇾ spikes 3-4mA

L5V + 440uF, 16V + 200uF
	mean: 1.6004386495825593e-05
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018599748256676585
	si_converted: true

Disable ADC NAP-Mode
	mean: 1.6193738583897284e-05
	min: 0.0
	max: 0.052991051431562665
	std: 0.0001887569381431854
	si_converted: true

ADC-LP C62 10 + 100 nF
	mean: 1.3531731793128161e-05         !!!!!!!!!!!!!!!!!!!! 18%
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018367630487575625
	⇾ peaks 3-3.5mA,
	⇾ noise max 100uA

Opa388 C3 1nF + 10nF ⇾ NOT PRACTICAL FOR SHP
	mean: 1.0455438489796289e-05         !!!!!!!!!!!!!!!!!!!! 35%
	min: 0.0
	max: 0.052991051431562665
	std: 0.0001860522023556891
	⇾ peaks ~2mA,
	⇾ noise max 60uA

Opa388 preLP C141 - 1nF + 10nF (DAC-LP) ⇾ NOT PRACTICAL FOR SHP
	mean: 9.878907951293827e-06
	min: 0.0
	max: 0.052991051431562665
	std: 0.000186174473005531

InAmp-LP C6 - 10nF + 470 nF
	mean: 9.972048052732577e-06
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018590133186560957

10mV Line seems noisy ⇾ Stabilize it
10mV Feedback Loop C147 1nF + 100nF
	mean: 5.733954503662093e-06          !!!!!!!!!!!!!!!!!!!!! >40%
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018286370435970868
	⇾ noise now almost always <40 us

10mV Feedback Loop C147 1nF + 10uF, C148 1uF + 10uF
	mean: 4.9549580492108525e-06		!!!!!! ~ 15%
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018244044034161253
	⇾ noise <35 us

10mV 2R to 0R ⇾ BAD
	mean: 2.617486645454759e-05

10mV 2R to 10R
	mean: 4.674731441450113e-06			!!!! +6%
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018262812750511275

Use new external low noise 5V Reg
	mean: 4.692708771278293e-06
	min: 0.0
	max: 0.052991051431562665
	std: 0.00018250544961560884

Use groung-ref (instead of 10mV)
	mean: 5.54111107625806e-06
	min: 0.0
	max: 0.053087651207939214
	std: 0.000185190245376952

Redone same Meas
	mean: 5.434298259766783e-06
	min: 0.0
	max: 0.053087651207939214
	std: 0.00018587143801792032

R-Meas 2R ⇾ 10R, also remove 470nF from C6 (not the final value)
	mean: 4.1520301763114815e-06
	min: 0.0
	max: 0.010638361792748255
	std: 4.803128913306609e-05
	⇾ noise <30us, mostly <20us

Correct to new Gain, 210R ⇾ 1k1
	mean: 4.782893691940752e-06
	min: 0.0
	max: 0.051209728558494774
	std: 0.00018735460074661376

Reactivate 10mV
	mean: 4.637892780687054e-06
	min: 0.0
	max: 0.051104246202174
	std: 0.0001788977286549849

Test with 2M Resistor Drain instead of nRF
	mean: 1.3642972695455144e-06
	min: 0.0
	max: 0.009015438714457391
	std: 7.952129501787741e-06

Opa388 C3 11nF ⇾ 1nF (Reverse)
	mean: 8.665722187069113e-06
	min: 0.0
	max: 0.051104246202174
	std: 0.00018307058133007159

Opa388 C3 1nF ⇾ 2nF
	mean: 8.252601292100976e-06
	min: 0.0
	max: 0.051104246202174
	std: 0.00018409876586589433

DAC-LP C141 11nF ⇾ 1nF
	mean: 1.0808221578953813e-05
	min: 0.0
	max: 0.051104246202174
	std: 0.00018555489134210082

DAC-LP C141 1nF ⇾ 2nF
	mean: 1.0662866140672243e-05
	min: 0.0
	max: 0.051104246202174
	std: 0.00018326430050986863

SAME, but now with negative values
	mean: 2.167918340381766e-06
	min: -0.00010665508840421124
	max: 0.051104246202174
	std: 0.00018421319283520122
```

InAmp ⇾ Add LP with 2x150R, 2x1nF to GND, 10nF mid

Switch to ADC +- Range
