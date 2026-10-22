# Cape v2.0 - Performance

## Advantages of v2

- shunt for current-sensing included in Voltage-Buffer-Loop, so output stays the same ⇾ voltages sensing ADC only needed for calibration
  - also switches that come afterward (before target)
- 2 separate fast ADCs are perfect for parallel and faster data acquisition, up to 50 MHz SPI
  - goal: maximize time for calculations
- Analog-Switch to target had 4 Ohms Resistance? Now 500mOhm. leakage is < 10 nA when off
- old biDir Level-Translators Type TXB needed 3mA drive strength, and even leaked 1-2uA when off
  - TI: TXS and TXB need side A to have a higher Vin as side B because of a protection diode
  - TI: LSF needs side B to be higher Voltage ⇾ wrong assumption / conclusion
  - specs of new one: operational from 1.3 to 5 V, 100 k PUs, 1 MOhm when running
- low noise LDO for all analog ICs, with additional PI-Filter for ICs with continuous current draw
- EMI-Cage for recorder and emulator
- rugged external input power on shepherd module, protected for reverse polarity
- watchdog-timer to trigger boot and reset if bbone unresponsive or POE-Switching fails or is not allowed
- extra low leakage recording and emulation
  - 500 pA for OpAmp
  - < 40 nA for Diodes
  - < 50 nA for Mosfet
  - ~1 nA for analog switches
  - 1-5 uA for level translators (behind switches)
- extra low noise OpAmps, DAC and ADC
- high speed, low power gpio to target
- support for two targets

## BOM

- full version has 292 parts, 42 unique, without recorder 235 / 40
- previous design had 160 parts, 59 unique

## GPIO performance

Target-GPIO of triggered edges on Port, without target present.

- target voltage 3v3, triggering from user-space-pins
- (quickprint102/103) < 2 us from 0 to 2V, but last 1/2 Volt can take 100 us
- (qs104) < 5 us for complete transition, < 2 us for first 2 V
- ⇾ performance should be good for at least 500 kHz
- pru-pins - rising edge - first 2V ~ 1us, complete in 2-3 us
- pru-pins - falling edge - first 2V ~ 1us, complete in 3-4 us

## Input Drain and Leakage

measured with Keithley 2604B

- Target GPIO when switched off
  - Target A GPIO1 to GND, >~ 240 MOhm @ 5V, > 10 GOhm @ 2.4 - 4.6 V, > 1 GOhm @ < 2.4 V
  - Target A SWD_IO, similar results
- Target GPIO when turned on, but v_out = 0V
  - Target B GPIO1, 99.9k to GND
- Target GPIO when turned on, Vout = 3v3
  - meter shows 3.2976 V
  - Target B GPIO1, >~ 5 k to GND when linux side pulls low, >~ 62 k to GND when open on other side
  - TODO: very cryptic, is test-voltage
- Recorder - V-Sense
  - 5V, 360 kOhm, ADC shows 4990 mV
  - 4.8 V, > 100 GOhm, ADC shows 4801 mV
  - 4.0 V, > 40 GOhm, ADC shows 4001 mV
  - 3.0 V, > 30 GOhm, ADC shows 3001 mV
  - 2.0 V, > 20 GOhm, ADC shows 2000 mV
  - 1.0 V, ~ 10 GOhm, ADC shows 1000 mV
  - ⇾ 100 pA lost through pin
- Recorder - V-Harvest, Mosfet disabled (VHarv = 5V/Max, currentlimit of source meter 10mA)
  - 5.0 V, ~ 0.25 MOhm ⇾ drain showing 7 - 20 mA
  - 4.9 V, ~ 110 MOhm
  - 4.8 V, ~ 43 MOhm
  - 4.0 V, ~ 8.64 MOhm
  - 3.0 V, ~ 3.94 MOhm
  - 2.0 V, ~ 2.55 MOhm
  - 1.0 V, ~ 1.24 MOhm
  - todo

## Resume

- recorder V-Sense outperforms rated Specs, 100pA lost through pin
- recorder V-Harvest, biggest leakage through MOSFET with 50nA and diode with 40nA (datasheet)
  - ~90 nA should result in 11 MOhm, but performance is 10x worse

## TODO

- add signal flow for gpio, simplified schematic
- target gpio with enabled switch (5k/62k), results are questionable
- further explore "high" input current over mosfet
  - is gate-voltage zero?
  - separate mosfet and diode, find the culprit
