# Improvements to PRU-Code

Classification: irrelevant, mostly dev-dump

## Getting started - handling PRUs

Was made more accessible by [ansible-playbook](https://github.com/nes-lab/shepherd/blob/main/deploy/dev_rebuild_sw.yml)

```Shell
ansible-playbook deploy/dev-rebuild_sw.yml
```

Manual Shell-Code

```Shell
sudo su

# stopping PRUs
echo "stop" > /sys/class/remoteproc/remoteproc1/state
echo "stop" > /sys/class/remoteproc/remoteproc2/state

# stop and start kernel module ⇾ warning: some states are not reset this way
modprobe -r shepherd
modprobe -a shepherd
# fw gets flashed and PRUs started by module

# test code on live system
sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml

# test suite in /opt/shepherd/software/python-package
sudo python3 setup.py test --addopts "-vv"

# helpful when build-system was used with sudo
sudo chown -R user ./
```

## Code Improvements

### Toolchain

- switch to gcc-pru, cmake?
- add all gpio to lib,
- ``global`` include should be named ``shared``
- sometimes precedence could be made more clear: https://en.cppreference.com/w/c/language/operator_precedence
- PRU could control MUX by using pad control registers, in control module (SPRUH73Q, p1458) 0x44E1_0000, 128 kB
- currently already implemented
    - update pru-software-support-package-5.4.0 to
        - official v5.7, or
        - gcc version https://github.com/dinuxbg/pru-software-support-package (fork of V4), with cherry-picking
        - updating fork: http://www.bartread.com/2014/02/12/git-basics-how-to-merge-changes-from-a-different-fork-into-your-own-branch/
    - fix make files
    - switch from -O2 to -O4, drop debug-symbols, nail char to unsigned, forbid float
    - add more const-correctness, less mixing of signed with unsigned (expensive typecast)
    - avoid signed int < 32bit, also expensive typecast
    - avoid a lot of far/slow register reads, but there can be done more
    - defines are better and more safe to use, explicit typing, proper usage of brackets
    - add lib-fn to access gpio-registers of sys
    - remove a lot of bottlenecks in PRUs
    - initialize vars were possible
    - printf became more userfriendly and selfexplaining
    - avoid global vars, or restrict them by "static" if possible
    - improve constness of fn-parameters throughout the code
    - expensive modulo was used at least 4 times, but never really needed
    - raise warning/hinting-level ⇾ fix warnings and errors
    - code compiles with gcc, but linker has problems with cmake

### Statistics

- PRU0-Codesize shrank from 161 KB to 99 KB
- PRU1-Codesize shrank from 131 KB to 91 KB
- GPIO-Sampling is now at around 5.5 MHz, the routine only needs 100 ns, 720 ns when writing (was originally 360, 1500)
- pru1-loop takes around 220 to 260 ns on average (with ~30-50 ns debug-overhead), max is 5700 ns
    - event 1 takes 200 ns
    - event 2 takes 250 ns
    - event 3 takes 540 ns (reply-pending-part) without control reply, and 4550 ns with reply (was originally 5200 ns)
- pru0
    - 560 ns for handle_rpmsg(), sometimes 1020 ns
    - 4340 ns sampling() / harvesting & load
    - 6860 ns sampling() / emulation
    - 4220 ns sampling() / vcap
    - blocking mutex part in buffer-exchange (handling block end) was reduced from 2700 ns to 460 ns
    - sampling happens with 100 kHz, every 10 us, but due to pru1 as a trigger, the jitter is at least the min-loop-timing (~200ns) and increases on gpio-value-writing (~900ns)

### PRU1

- most of the control state-machine should be on PRU0 ⇾ get spi-readout triggered by tmr_cmp1 for high precision readout timing
- virtqueue / rpmsg is heavily unoptimized for 2-8 byte transfers (~5 us)
- timer-defines in config and main are codependent, it would be easier to base them on the CLK
- clean up timecalc, it seems complicated, at least the naming of vars
- fast loop could be more consistent if there would be a "continue" at the end of the events
- is "/2" an obvious bitshift?
- TIMER_BASE_PERIOD / 10 seems to be a constant
- currently already implemented
    - pin writes could be optimized, bit-shift right away (combinable)
    - mix of types, unsigned int VS. fixed uint32_t
    - typecasting for defines, or just literals
    - event 3 should be on position 1 (if possible), highest prio

### PRU0

- firmware should do self-tests for its key components
    - both cores running
    - ram-interface to cpu responsive
    - dac and adc available (chk product-id register)
    - setting voltage is measurable
    - bring it down to kernel module or (if not possible, or additionally) as blink-codes
    - show printf as kernelmsg, but don't spam too much
- so many magic numbers! config seems not like a config, because it needs to know what is in ``resource_table_def``
- currently already implemented
    - ringbuffer can be optimized
    - ``init_ring`` should be ``ringbuffer_init``, consistency
    - int_source is global, it shouldn't ⇾ it can be reduced to a local bool ``got_sig_block_end``
    - free_buffers is global, but then passed by pointer
    - shared_mem is global
    - int-return is mostly const and not needed
    - context switch by function calls are expensive (inline, variables via const ref)

### PRU0 vCap

- it would be perfect to use constexpr-fn to pre-calculate LUTs and literals for proper human readable unit conversion
- modularize code, because vCap also contains MPPT-Converter, they could be swappable
- unit-test critical parts (add from teensy project)
- demystify magic numbers
- control loop should be faster than 100 kHz, to handle sudden TX-Spikes, depending on local-input-capacitance and pwr-consumption of target-board
    - adc/dac transfer could happen simultaneously with 17 MHz, so data is read, control is calculated and written on next tick
- find a better name
- allow freezing energy in capacitor

### PRU-Changes for after HW-Completion

- Control-Code from PRU1 would be partly more suited for PRU0 now
- could the buffer swap be more efficient? it should be just a switch of base-address
- is the gpio-buffer properly initialized or nulled in between? or only partially in hdf5 saved by py-routines
- vCap still needs a lot of care
- add asserts, simple define-version is enough: https://interrupt.memfault.com/blog/asserts-in-embedded-systems
- prepare power-down options to save more energy
- add new hardware as abstract layer
- add option to preCharge Target or just begin with full Cap
- Presence-Check SPI ADC (ID or similar)
- downsampling (pyCode)
- measure sync-offset-limits
