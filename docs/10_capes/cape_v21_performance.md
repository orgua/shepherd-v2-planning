# Cape v2.1r0 - Performance

## Setup

- BB powered by benchsupply 5.1 V, ~ 400 mA
- Shepherd powered by BB, VIn 5.08V
- Mods
  - big cap on input
  - switched rails for emu
  - later: lowpasses raised to 160 kHz
  - intermediate: rail B with short loop (exclude switch)
  - intermediate: small 100 nF Buffer Cap for Target 1 (instead of 1 uF)
  - later: 1 Ohm Shunt on Rail B, 100 Ohm for InAmp for 1:100 Amp
  - later: railB, long loop, 1.6 MHz Feedback Lowpass with 100 Ohms
- recorder
  - 1 kOhm from V_virtBuf to V_harvest
  - v_harvest connected to V_sense
- Emu
  - 1 kOhm on V_supply on target 1
- scope screenshots are in ./media_v2.1r0

## Validating Components

### Power-Rails

- Problem: Voltage Drop on Enable
- switching power on can result in unstable states for BB and ICs
- scope shows (Quickprint[1-3].png)
  - 3 Drop-Stages with ~ 620 mV drop in around 700 us
  - slowly recovering 300 mV after that
- adding a 1 mF / 16 V Cap on 5 V Input improves situation (Quickprint4.png)
  - drop of 200 mV for ~ 4 ms
  - 2 remaining Spikes with 328 mV
  - no recovery after that ⇾ quick return to previous rail-voltage

### DAC-Responses

Goal: optimize analog circuit connected to the DAC

#### Harvester

- Harvest-VMatch
  - 1V raise - < 8 us, < 10 % overshoot (QuickPrint23.png)
  - 1V fall - < 8 us for ~ 90 % (QuickPrint22.png)
  - 3V raise - < 8 us, no overshoot (QuickPrint20.png)
  - 3V fall - < 8 us for ~ 90 % (QuickPrint21.png)
  - 4V8 raise - < 12 us, no overshoot (QuickPrint24.png)
  - 4V8 fall - < 10 us for ~ 90 % (QuickPrint26.png)
  - result: reference for a fast response, higher voltages are limited by raise-time
- Harvest-SimBuf, 1 kOhm Drain
  - 1V raise - < 30 us, < 12 % overshoot (QuickPrint31.png)
  - 1V fall - < 25 us for ~ 90 % (QuickPrint32.png)
  - 3V raise - < 30 us, < 10 % overshoot (QuickPrint30.png)
  - 3V fall - < 25 us for ~ 90 % (QuickPrint33.png)
  - 4V8 raise - < 30 us, no overshoot (QuickPrint29.png)
  - 4V8 fall - < 20 us for ~ 90 % (QuickPrint28.png)
  - result: probably limited by lowpass, should be faster
- Harvest-SimBuf, 1 kOhm Drain, 160 kHz Mod
  - 1V raise - < 15 us, 40 % overshoot (QuickPrint93.png)
  - 1V fall - ~ 12 us for ~ 90 % (QuickPrint94.png)
  - 3V raise - ~ 14 us, 15 % overshoot (QuickPrint96.png)
  - 3V fall - ~ 10 us for ~ 90 % (QuickPrint95.png)
  - 4V8 raise - ~ 14 us, 5 % overshoot (QuickPrint97.png)
  - 4V8 fall - ~ 12 us for ~ 90 % (QuickPrint98.png)
  - result: significantly better performance, but still no match with speed of VMatch, probably because of additional 100 nF ⇾ preview of possible Mod for Emu-Rails (reduce 1uF to 100 nF)

#### Emulator

- Emulate, Rail A
  - 1V raise - 50 us, 20 % overshoot (QuickPrint5.png)
  - 1V fall - 90 us for ~ 90 % (QuickPrint8.png)
  - 2V raise - 50 us, 20 % overshoot (QuickPrint7.png)
  - 2V fall - 80 us for ~ 90 % (QuickPrint6.png)
  - 3V raise - 60 us, 20 % overshoot (QuickPrint9.png)
  - 3V fall - 90 us for ~ 90 % (QuickPrint10.png)
  - 4V raise - 60 us, 14 % overshoot (QuickPrint12.png)
  - 4V fall - 70 us for ~ 90 % (QuickPrint11.png)
  - 5V raise - 70 us, no overshoot (QuickPrint13.png)
  - 5V fall - 70 us for ~ 90 % (QuickPrint15.png)
  - result: lowpass might slow down control loop, cut off delay is ~ 60 us (16 kHz)
- Emulate, Rail B, 1 kOhm Drain,
  - 1V raise - 50 us, 20 % overshoot (QuickPrint16.png)
  - 1V fall - 90 us for ~ 90 % (QuickPrint17.png)
  - 2V raise - 50 us, 20 % overshoot (QuickPrint19.png)
  - 2V fall - 70 us for ~ 90 % (QuickPrint18.png)
  - result: very similar to Rail A
  - perspective: v2.0 was 100 us to rise (75us for 80%) and 400us to fall (75us for 80%)
- Emulate, Rail B, 1 kOhm Drain, 160 kHz Mod
  - 1V raise - 45 us, 20 % overshoot (QuickPrint88.png)
  - 1V fall - 80 us for ~ 90 % (QuickPrint87.png)
  - 3V raise - 50 us, 10 % overshoot (QuickPrint89.png)
  - 3V fall - 80 us for ~ 90 % (QuickPrint90.png)
  - 4V8 raise - 60 us, no overshoot (QuickPrint92.png)
  - 4V8 fall - 70 us for ~ 90 % (QuickPrint91.png)
  - result: the lowpass only has a small influence, try small loop next
- Emulate, Rail B, 1 kOhm Drain, 160 kHz Mod, Small Loop Mod
  - 1V raise - 30 us, 20 % overshoot (QuickPrint104.png)
  - 1V fall - 80 us for ~ 90 % (QuickPrint103.png)
  - 3V raise - 50 us, 10 % overshoot (QuickPrint101.png)
  - 3V fall - 70 us for ~ 90 % (QuickPrint102.png)
  - 4V8 raise - 70 us, no overshoot (QuickPrint100.png)
  - 4V8 fall - 70 us for ~ 90 % (QuickPrint99.png)
  - result: a bit faster for lower voltages, enough for ditching the switch-compensation?
- Emulate, Rail B, 1 kOhm Drain, 160 kHz Mod, Small Loop Mod, Smaller Cap Mod
  - 1V raise - ~ 8 us, 20 % overshoot (QuickPrint201.png)
  - 1V fall - ~ 10 us for ~ 90 % (QuickPrint202.png)
  - 3V raise - ~ 10 us, 10 % overshoot (QuickPrint205.png)
  - 3V fall - ~ 12 us for ~ 90 % (QuickPrint204.png)
  - 4V8 raise - ~ 14 us, no overshoot (QuickPrint206.png)
  - 4V8 fall - ~ 12 us for ~ 90 % (QuickPrint207.png)
  - result: small cap brings edge-response from 30-80 us down to 8-14 us ⇾ target can buffer on its own
- Emulate, Rail B, 1 kOhm Drain, 160 kHz Mod, Small Loop Mod, 1 Ohm Shunt Mod
  - 1V raise - ~ 6 us, 30 % overshoot (QuickPrint301.png)
  - 1V fall - ~ 8 us for ~ 90 % (QuickPrint302.png)
  - 3V raise - ~ 8 us, 10 % overshoot (QuickPrint303.png)
  - 3V fall - ~ 10 us for ~ 90 % (QuickPrint304.png)
  - 4V8 raise - ~ 10 us, 5 % overshoot (QuickPrint305.png)
  - 4V8 fall - < 10 us for ~ 90 % (QuickPrint306.png)
  - result: voltage seems unstable, but responses are fast! could also be caused by noisy 10/-6 V
- Emulate, Rail B, No Drain, 160 kHz Mod, Long loop, 2 Ohm Shunt, 1 uF Buffer
  - 2V raise  - 40 us, 10 % Overshoot (Quickprint354)
  - 2V fall   - 80 us, 90 % (Quickprint353)
- Emulate, Rail B, No Drain, 160 kHz Mod, Long loop, 2 Ohm Shunt, 100 nF Buffer
  - 2V raise - < 10 us, < 20 % Overshoot (Quickprint355)
  - 2V fall - < 10 us, 90 % (Quickprint356)
  - result: 100 nF without any load still shows slight constant ringing
- Emulate, Rail B, 1k Drain, [same as before]
  - 2V raise  - < 10 us, < 20 % Overshoot (Quickprint358)
  - 2V fall   - < 10 us, 90 % (Quickprint357)
- Emulator: total propagation beginning with ChipSelect
  - DAC-CS & OpAmpOut (100nF Buffer, 1kOhm Load), Quickprint364
  - SPI Communication takes ~ 800 ns
  - Voltage begins changing after ~ 2.2 us of CS-High
  - Voltages overshoots in 3 us and falls to wanted voltage in additional 1.5 us
  - result: 8 us from beginning of communication to voltage-set

#### TODO

- try long loop, smaller feedback-resistor, but it shouldn't change much - extra ADC for voltage and 10 Ohm Shunt seems important
latest Mod: rail B, long loop, 1.6 MHz Feedback Lowpass with 100 Ohms
- still 60 mVpp Ripple on VTarget, 600 kHz
- fav: 100nF, ensure system function, noise is ok, buffering done by target
- measure reverse current of diode
- fix lowpass on recorder, or at least the 12mV Spikes every 3.3 us (~7% integral of 12 mV)
- test delay of (recorder) setting voltage-level

### Current Measurements

- Emulator
  - ohm-meter says R = 995 Ohm
  - I0 = 2.338 # mA
  - V = [1, 2, 3, 4, 5, 4.8] # V
  - I = [3.255, 4.155, 5.068, 5.977, 6.797, 6.711] # mA
  - ⇾ R = [1090.513, 1100.715, 1098.901, 1099.203, 1121.328, 1097.645] # Ohm
  - result:
    - at 5 V system has a 100 mV drop when adding 1 kOhm Load. gone below 4.9 V
    - resulting R for 2-4.8 V is very consistent (not considering noise, or further filtering)

- Emulator ⇾ after Shunt-Mod (1 Ohm)
  - ohm-meter says R = 995 Ohm
  - I0 = 2.346 # mA
  - V = [1, 2, 3, 4, 5, 4.8] # V
  - I = [3.173, 3.996, 4.821, 5.647, 6.429, 6.308] # mA
  - ⇾ R = [1209.19, 1212.121, 1212.121, 1211.754, 1224.59, 1211.509] # Ohm
  - result:
    - resulting R for 2-4.8 V is very consistent, similar to first measurement

- Recorder
  - Ohm-meter says R = 998 Ohm
  - I0 = 2.274 # mA
  - VCombinations = 0/5, 4.9/1, 4/1, 3/1, 2/1, 2/0, 1/0, 4/3
  - V = [-5, 3.9, 3, 2, 1, 2, 1, 1] # VDiff
  - I = [1.84, 5.821, 5.001, 4.092, 3.181, 4.092, 3.182, 3.180] # mA
  - ⇾ R = [11520.737, 1099.521, 1100.11, 1100.11, 1102.536, 1100.11, 1101.322, 1103.753] # Ohm
  - result:
    - reverse current is significantly higher than expected (400 nA instead of 40 nA), even seconds diode can't fix that :( replace it?
    - resulting R is very consistent, similar to emulator-results

### Emulator - Dynamic Behavior to load-changes

- setup
  - aux channel with 10 Ohm shunt
  - v-target = 2.0 V
  - loads: 10, 20, 30, 40, 50 mA ⇾ 200, 100, 66.7, 50, 40 Ohm
  - resulting load-resistors: 200, 100, 68, 51, 43 Ohm
  - buffering: 100 nF, 1 uF
  - scope in AC-Mode,
- experiment A1: 2V, 100 nF, long loop, ON
  - 10 mA: -72 mV, gone after ~ 25 us, Quickprint319,321
  - 20 mA: -144 mV, gone after ~ 35 us, Quickprint322
  - 30 mA: -192 mV, gone after ~ 45 us, Quickprint324
  - 40 mA: -268 mV, gone after ~ 45 us, Quickprint323
  - 50 mA: -332 mV, gone after ~ 50 us, Quickprint325
- experiment A2: 2V, 100 nF, long loop, OFF
  - 10 mA: +92 mV, gone after ~ 30 us, Quickprint326
  - 20 mA: +168 mV, gone after ~ 40 us, Quickprint329
  - 30 mA: +248 mV, gone after ~ 40 us, Quickprint328
  - 40 mA: +320 mV, gone after ~ 45 us, Quickprint330
  - 50 mA: +380 mV, gone after ~ 45 us, Quickprint332
- experiment B1: 2V, 1 uF, long loop, ON
  - 10 mA: -56 mV, gone after ~ 30 us, Quickprint334
  - 20 mA: -112 mV, gone after ~ 35 us, Quickprint335
  - 30 mA: -172 mV, gone after ~ 40 us, Quickprint336
  - 40 mA: -192 mV, gone after ~ 45 us, Quickprint337
  - 50 mA: -248 mV, gone after ~ 45 us, Quickprint338
- experiment B2: 2V, 1 uF, long loop, OFF
  - 10 mA: +72 mV, gone after ~ 30 us, Quickprint340
  - 20 mA: +148 mV, gone after ~ 35 us, Quickprint342
  - 30 mA: +180 mV, gone after ~ 40 us, Quickprint344
  - 40 mA: +236 mV, gone after ~ 40 us, Quickprint345
  - 50 mA: +288 mV, gone after ~ 40 us, Quickprint346
- experiment C: 2V, 1 uF, long loop, 1 Ohm Shunt, 50 mA load
  - without load unstable, 72 mVpp
  - transition between loads has no significant voltage drop, even 50 mA drop is below resonance Quickprint347/348/
- result
  - 100 nF Dips are roughly corresponding to voltage divider between shunt and load (10/(43+10)=377mV)
- experiment D1: 2V, 100 nF Buffer, long loop, 2 Ohm Shunt, 50 mA load / 43 Ohm
  - on: - 84 mV, < 5 us, Quickprint360
  - off: + 76 mV, < 5 us, Quickprint359
  - result: 100nF slightly unstable, 20 mVpp Ringing
- experiment D1: 2V, 1 uF Buffer, [unchanged]
  - on: - 48 mV, < 5 us, Quickprint361
  - off: + 56 mV, < 5 us, some dampened ringing afterwards < 30 us, Quickprint362

### Noise Behavior

- Short ⇾ Quickprint 49 - 54 (Ground-noise-floor)
  - 1.38 mVpp (10ms), 900 uVpp (100ns)
- L3V3 ⇾ Quickprint 34 - 40
  - 1.94 mVpp (50ms), 1.44 mVpp with 5 MHz ripple (1us)
- RailB TargetA ⇾ Quickprint 41 - 48
  - 1.56 mVpp (10ms), 980 uVpp (100ns)
- A5V ⇾ Quickprint 55 - 61
  - 1.8 mVpp (50ms), 1.4 mVpp with 100 kHz RampRipple (10us), 1.06 mVpp (100ns)
- 6V ⇾ Quickprint 62 - 68
  - 4.56 mVpp (50ms), 4.24 mVpp with spiky ripple (1ms), 1.52 mVpp with 1 MHz switching noise (1us)
- 10V ⇾ Quickprint 69 - 75 ⇾ high Noise
  - 2.8 mVpp (50ms), 2.68 mVpp with spiky ripple (1ms), 1.48 mVpp with 1 MHz switching noise (1us)
- -6V ⇾ Quickprint 76 - 82 ⇾ high Noise
  - 5.12 mVpp (50ms), 4.6 mVpp still noisy (1ms), 3.68 mVpp with 1 MHz switching noise (1us) (!!!!!)
- 10 Ohm shunt@1V, RailB, 1k Load, A5V ⇾ Quickprint 83 - 86 ⇾ 40 mVpp ???
  - 21-30 mVpp with strong 50 Hz switching noise (10ms)

#### TODO

- shunt-noise is bad, why? ⇾ it isn't, ~
- are -6V and 6V and 10V improved to last time?
  - 10 V is similar
  - 6 V has no record
  - -6V is worse! (USB-Powered)
- how does input voltage perform?

### GPIO to Target

- PRU-Recording
  - GPIO 0 ⇾ 1 (r31_00) ⇾ GPIO0
  - GPIO 1 ⇾ 2 (r31_01) ⇾ GPIO1
  - GPIO 2 ⇾ 64 (r31_06) ⇾ GPIO2
  - GPIO 3 ⇾ 128 (r31_07) ⇾ GPIO3
  - GPIO 4 ⇾ 256 (r31_08) ⇾ GPIO4
  - GPIO 5 ⇾ 16 (r31_04) ⇾ UART_TX
  - GPIO 6 ⇾ 32 (r31_05) ⇾ UART_RX
  - GPIO 7 ⇾ 4 (r31_02) ⇾ SWD_CLK
  - GPIO 8 ⇾ 8 (r32_03) ⇾ SWD_IO
  - result: 0,1,5-8 are not connected (P8-41 to P8-46) and can't be handled by PRU
    - fix: connect afterwards (avoid boots-issues)
- Logic-Analyzer Target 1
  - GPIO 0 to 4 correspond to Pin 3 to 7
  - GPIO 5 to 8 correspond to Pin 9 to 12
  - BATOK ⇾ Pin 8
  - result: ALL OK
- Logic-Analyzer Target 2
  - GPIO 0 to 4 correspond to Pin 3 to 7
  - GPIO 5 to 8 correspond to Pin 9 to 12
  - BATOK ⇾ Pin 8
  - result: ALL OK (after removing solder bridge)
- Getting Pin6 to work
  - disable uart in uEnv.txt
  - enable pins in DT
  - fault: solder bridge under IC (could not be seen from side / above)
- edge-timings
  - config: target A, pin4 / GPIO1, triggered by linux, scope on linux and target pin
  - 3 V rise: 25 us, fully, quickprint307
  - 3 V fall: 4 us, fully, quickprint308
  - 2 V rise: 20 us, fully, quickprint309
  - 2 V fall: < 4 us, fully, quickprint310
  - 4 V rise: 25 us, fully, quickprint311
  - 4 V fall: 4 us, fully, quickprint312
  - 4.8 rise: 25 us, fully, quickprint313
  - 4.8 fall: 4 us, fully, quickprint314
  - confirmed with same pin on target B and pin3
  - result: 20 kbaud ?!? is it enough that 66% of signal is there after 5 us?
- faulty behavior: both target-gpios are limited to 3V ?
  - V_IO_Buf is also limited to 3V
  - V_IO is on full rail > 4.6 V
  - 1k shunt too high! 10 * 10 k are pulling down, resulting in 1 k
  - replace V_IO_BUF OPAmp-Resistor by 10 Ohms
  - confirmation: full range of voltage
- edge-timings (revisit)
  - 4.8 V rise: 40 us for fully, 12.5 us for 80 %, Quickprint315
  - 4.8 V fall: 10 us for fully, 8 us for 80 %, Quickprint316
- 10x ScopeProbe with reduced capacitance has low impact on rise-time
- faulty behavior: previous version had edge-timing of 3-4 us both ways!
  - difference: TargetGPIO was pulled up with 100k instead of 10k and 1k to lvl-changer
  - Theory: something is pulling down, maybe FET-Connection is not working as expected

Trying to find reason of slow rising edges

- Taking apart the LSF
  - refB is sources with 240k on 3.306 V, settling at 1.524 V
  - refA settles at 0.967 V (between 1M and 100k) ⇾ voltage drop over FET (refAB) is 0.558 mV
  - modding refB with 200k increases refB to 1.625 V, refA to 1.053 V ⇾ drop = .572 V
- LSF-SignalPads A to B ⇾ resistance while on = 6 Ohm, off = infinite
- 100k as PU on Target side worsens the edge-timing

#### TODO

- test reverse-channel
- test 1k PU on BB-Side
- add scope-shots to project with leading 3xx
- Goal 1Mbit UART
- Friedrich is getting < 500 ns Edges with no Series Resistor, 10 k PU on both sides, and 140k on RefA for slightly higher V_thres = 1.2 V

#### Program EEPROM

```Shell
sudo shepherd-sheep -vvv eeprom read
sudo shepherd-sheep -vvv eeprom write -v 00B0 -s 210617AA0001 --no-calib
```

- access fails 'FileNotFoundError: [Errno 2] No such file or directory: '/sys/bus/i2c/devices/2-0054/eeprom'
- EEPROM is on port P9_19/20 and write_protection on P9_23
- /dev lists i2c-0 and i2c-2
  - BB EEPROM is on I2C-0
  - SWD-Interface for Target is on I2C-1
- 'sudo i2cdetect 2' shows a 0x54 device, this should be the EEPROM
- ODD: uEnv.txt shows active I2C1 as overlay, but only 0 and 2 are activate /lib/firmware
- error theory: eeprom has no power during boot and is therefore not added to sysfs
  - fixed by hardwiring 3V3 from BB to offline L3V3 line
- WORKS as expected

### External Power

- Switching Ferrite is not as intuitive as imagined ⇾ mark better

TODO: measure changes in Noise

### Watchdog

- BB_nSTART = P9_09, BB_nRES = B9_10, WD_ACK = P8_10
- watchdog is set to 60min per schematic, but is now modded to 20 min (parallel 2x 100k as R101)
- launcher is sending an ACK every 600s
  - confirmed: 2.5 ms High from launcher
  - nice extra: ACK-Pin is high for 10s during uboot
- boot works with connected WD
- during normal BB run
  - ACKs come in like clockwork
  - @ 350 s ⇾ some jitter on logic-analyzer ACK was high for ~ 100 ns, nRES also 100 ns 8x during 0.1 ms without harm (Soldering Iron was switched off)
  - @ 1100 s ⇾ BB_nSTART was pulled low for 15 us without any harm
  - @ 2179 s ⇾ BB_nSTART was again pulled low for 15 us
- on shutdown state
  - ACK and nRES are low
  - nSTART is @3V3
  - 730 s silence
  - nSTART gets 20.8 ms low (quickprint317) but its not enough for the "old" BB to react to it
    - not enough for a fresh BB either...
  - there does not seem to come another PullDown (25'000 seconds wait)
- manual wakeup: 130 ms do the trick :(
- provoking a reset
  - fresh start (ACK is issued by uboot)
  - shepherd-launcher is stopped
  - @ 1100 s WD tries a nSTART
  - no one ACKs
  - @ 2100 s WD pulls reset low for 327 ms
  - BB resets properly

stop launcher::

```text
systemctl stop shepherd-launcher
```

TODO: Why is boot not working? Even a fresh BB does not respond to a ~ 20 ms LOW nSTART

### External Button

- V2.0 SocketConfig: 3V, LED_OD, BTN_SENSE, GND (was taken from Kais schematic, but there the footprint was flipped)
- V2.1 SocketConfig: GND, BTN_SENSE, LED_OD, 3V3 (1:1 Shepherd 1.x)
- Button-Plug-Config for v2.0 - view from metalside: red, black, yellow, white (flipped from 1.x Version)
- Button-Config for 2.1: flipped back again
- problem: shepherd-service expects correct /etc/shepherd/config.yml ...
- all fine now - works!

### BeagleBone-Boot-Pins

- Bootpin-Overlay conflicts with bootup
- Problem 1: some essential PRU-Pins are also deciding how the BB boots up
- Problem 2: was hard to catch, because reboots und some powerups seem to be fine
- Used by Shepherd: P8 Pin 39-46, states in when unconnected with BB
  - 39, 40, are low
  - 41, 43 are High
  - 42, 44 are needed high (but shepherd feeds in 80 ms high, follows with serial, low afterwards)
  - 45, 46 are low
  - P8-42 is connected to P9-26 with 2 kOhm (is uart-rx ???)
  - P8-44 is connected to P9-18 with 2 kOhm (is i2c1-sda)
- Bootup from BB
  - 41, 42, 43, 44 are high
  - 45, 46 are low
- leaving one pin unconnected
  - 41 ⇾ all Leds light up forever
  - 43 ⇾ short break + flashes, repeat forever
  - 42, 44, 45, 46 ⇾ no led response
- leaving some pins unconnected
  - 41+43 ⇾ NoLeds
  - 42+44 ⇾ NoLeds
  - 41 - 44 ⇾ OK
  - 41+42 ⇾ All Leds light up forever
  - 43+44 ⇾ NoLeds
  - 42+43 ⇾ Flashes
  - 42 - 44 ⇾ NoLeds (????, pin 41 is high and expected to be high)
- Function during Boot
  - 41 - Bootdevice, High
  - 42 - CLKOUT, High
  - 43 - Bootdevice, High, but depends SDCard if LOW
  - 44 - Bootdevice, High
- solution: analog switch for 41-44

## Validation

- 2nd (fresh) BBone was tested with current Shepherd v2.1 ⇾ works fine (when omitting pins p9 41-44 during uboot)
