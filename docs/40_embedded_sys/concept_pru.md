# Concept for Realtime-Units (PRUs)

- SPI to adc/dac ⇾ use dedicated hardware and not bit-banging
  - bit-banging transfer takes 8 (DAC) - 12 (ADC) ticks per bit ⇾ so 192 ticks for 24 bit at best (DAC) and 384 ticks for 32 bit (ADC)
  - no PRU-Peripheral is utilizable for it
  - Host-SPI is accessible by PRU (~40 ticks read delay for <= 32-bit, writing should take 1 tick) ⇾ Buffered, FIFO, allows 4-32 bit words, max 48 MHz
  - CS-Pins need precise timing, or at least repeatable (same delay, equidistant), so at beginning of IRQ-Loop
    - no IRQ to synchronize transaction!
    - start of transaction on host-spi can be half a SPI-Clock-Cycle accurate (Start Request ⇾ CS Low)
    - CS Pin could be PRU-Controlled/Monitored-Pin
  - alternative: DAC needs no MISO, so one extra PIN would allow to talk to both ICs at the same time
    - clk can be shared and would be reduced to the lower one (ADC is slower and has longer registers, so improvement would be 1/3 less time)
- GPIO to target
  - PRU-GPIO pin direction is controlled by host, in linux via device tree or alternatively via ["cape-universal"](https://github.com/cdsteinkuehler/beaglebone-universal-io)
  - PRU can't access host GPIO (i found no memory-mapping)
  - a trick would be to reduce PRU to an observer with his separate pins ⇾ linux can then program, control and listen on it's own pins
  - one PRU could sample 16 bits with close to 100 MHz ...
  - there is no interrupt for PRU-pin-changes, but for transitions on host-gpio-modules
  - NOTE: some pins allow hardware-timestamping via int-routine, data-sheet even implies this is possible for all pins
- UART to target ⇾ seems to be only host-controlled
  - could also be handled by PRU ⇾ has dedicated UART (TL16C550) no autobaud, 192 Mbps, 16-bit FIFO
  - HOST-UART is accessible by PRU (~40 ticks read delay) ⇾ (16C750), 300 bps to 3.7 Mbps, autobaud up to 115.2 Kbps
  - could just be monitored by PRU (GPIO)
- SPI to target
  - control by userspace seems to be the way to go, so user can decide whether to use SPI or just the GPIO
  - one additional SPI available
  - monitor and timestamp by PRU
- Programmer, currently for SWD, but also allow JTAG
  - should stay in user-space, SWD needs flexible pin-direction
- unify Pins to Target ⇾ Programming, SPI, UART and GPIO
  - would be possible if Pins are controlled and used in Linux, PRU is just recording Pins
- I2C to dac (static voltage) handled by PRU, to minimize errors
  - PRU could access host-I2C
  - PRU can utilize MDIO-Interface for that
- vCap ⇾ see sub-chapter below
- Scheduling
  - one PRU should do time critical things, i.e. sampling into ringbuffer in shared PRU-Memory → other PRU-Core should handle transfer to cpu-memory
  - work timer/interrupt-based with short transactions, could do pin-reading the rest of the time
- try to add unit tests for critical code sections (vCap) ⇾ make it more modular
- benchmark the loop
  - timer, counter with min, max, mean with copy to host
  - or just use debug-pins to mark active parts and analyze like pwm
  - maybe more useful than disassembling via godbolt

## vCap - Converter & Capacitor Emulation

- main future goals from the thesis regarding vCap
  - dynamic capacitance ⇾ allow capacitor sweeps, find optimum cost by benchmarking the target firmware
  - energy aware debugging ⇾ keep energy in capacitor constant during commands
  - support more targets, mainly msp430
- find a better name

## BeagleBone Features, Comparison

- High-level-Overview: <https://elinux.org/Ti_AM33XX_PRUSSv2>
- TI-Wiki: <https://processors.wiki.ti.com/index.php/PRU-ICSS>
- PRU-Projects: <https://processors.wiki.ti.com/index.php/PRU_Projects>
- Feature-comparison: <http://www.ti.com/lit/sprac90>

### PRU ICSS High-level-Overview

- 200 MHz cores
- one 32bit-op per cycle
- no division
- 8 kB RAM per Core
- 12 kB shared RAM
- 3 banks of Scratch-Pad (=3x30x 32-bit registers) directly between the cores, 1Cycle Access
- access to host memory, L3 interconnect (expensive wait, see benchmark below)
- INTC, 64 events, 10 channels
- access to host periphery (QSPI, GPIO, even USB), ~ 40 cycles read latency
- CPU has mailbox system to send 4x 32-bit IRQ-messages to individual cores (also PRUs)

### TI-Wiki contains datasheets for various sub-topics

- PRU C/C++ optimization guide, presentations,
- Subprocessor documentation
- PRU-Projects_, notably
  - PyPRUSS (programming PRUs on beaglebone black),
  - libpruio (high speed data handling),
  - BeagleLogic (100 MHz, 14CH Logic Analyzer),
  - High Speed data acquisition

### Latency Benchmarks

source: "sprace8a.pdf"

- writes take normally 1 cycle, reads 2 to 14 (UART) cycles local, reads 30 - 40 cycles global (periphery)
- transfer shared RAM to DDR 5 cycles / 4 byte, to 65 cycles / 128 byte
- transfer DDR to shared RAM 47 cycles / 4 byte, 107 cycles / 128 byte ⇾ prefer large chunks

### PRUs (ICSS, ICSSG) Supported techniques

source: link for feature-comparison

- mostly called (enhanced) EGPIO:
- 16 bit parallel capture input for GPIO, r31[15:0] are DataIn, r31[16] is ClockIn
- 28 bit shift input ⇾ pru<n>_DATAIN, r31_status[27:0], with counter stats, internal clock source ⇾ which pin?
  - WARNING: this seems to leave only ONE input
- 3 Ch peripheral interface (on ICSS device dependent) - not found on BBB **??**
- Shift output
- **dedicated UART (with 16-bit FIFO, 192 Mbps) based on TL16C550**, no speedsense, but autoflow (cts, rts)
- eCAP (enhanced Capture)
- IEP (industrial Ethernet)
- 2x MII_RT (media independent interface), MDIO (management Data IO)
  - each MII has 32 byte RX FIFO, 64 byte TX FIFO, even TX_EN (as Chip-select) but has clk input ⇾ NO SPI

### Beagle Black ⇾ AM3358

- 1 PRU = 2 Cores, 200 MHz, 8 KB IRAM (instructions) per Core, 8 KB DRAM per core, 12 KB shared DRAM, 17/17 GP-Inp, 16/16 GP-Out, 3 Banks Scratch Pad
- eGPIO on register x30000 / pins pr1_pru0_pru_r31[16:0] (INP) and pr1_pru0_pru_r30[15:0] (OUT) for PRU0, same for PRU1 with changed register name
- UART on register x28000 / pins pr1_uart0_rxd/txd/cts_n/rts_n
- eCap on pr1_ecap0_ecap_capin_apwm_o ⇾ capture input or aux PWM out
- MDIO has an IO pin pr1_mdio_data

### Beagle AI ⇾ AM5729

- 2 PRU, 200 MHz, 12 KB IRAM per Core, 8 KB DRAM per Core, 32 KB shared DRAM, 21/21 GP-Inp, 21 GP-Out, 3 Banks Scratch Pad
- same peripherals as AM3358

### Possible Compilers

- ti c compiler, supports c99, asm and c++2003 (<https://www.ti.com/tool/TI-CGT#PRU>)
- gcc pru port, in mainline now, (<https://github.com/dinuxbg/gnupru/wiki>)

## Program - Optimizations

### PRU Good Practice

- passing of arguments: 16 registers to pass 32-bit each
- auto-incrementing loops are without overhead [for (i = 0; i < X; ++i)]
- O2 tries to rewrite div-const-int into reciprocal mult
- mixing of asm, c, c++ can bring trouble when activating optimizations
- a more efficient (single instruction) access to local memory in the lower 16-bits (__near), can be used
- variables in shared memory always "volatile"
- const helps, at least to save RAM (if defined at compile-time)
- compiler switch can decide if char is signed or unsigned
- don't mix signed and unsigned variables ⇾ expensive typecast
- don't bring signed variable <32bit into code ⇾ expensive typecast and handling

### CCS Compiler Switches

- opt_level=[1-4]
- opt_for_speed=[0-5]
- fp_mode=[strict] ⇾ disable fp-usage

### Current Program Flow PRU0

- only drawing on paper atm

### Current Program Flow PRU1

- only drawing on paper atm
