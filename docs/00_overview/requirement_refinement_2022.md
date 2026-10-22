# Requirements - Refinement 2022-06

(rough version)

- more focus on a general testbed for the Internet of Things, especially:
- GPIO Monitoring ⇾ higher min sampling frequency / guarantees
  - nRF and MSP430 have 16 MHz baseclock ⇾ same region would be nice
  - chip-rate of 2 MChip/s,
  - 200ns per loop == must, 150 ns == nice, more welcome
  - idea: state-machine triggered sampling with max window size (example: target uses one pin to trigger sampling for 50 ms)
- UART Monitoring (RX from Target-Side), min 461 kBaud, better 922 kBaud (1MBaud maybe easier)
  - software defined, linked with GPIO-Monitoring
  - timestamp with 1ms-resolution is enough, whole line, start of transmission
  - more detailed timestamps are often embedded in message itself
  - document wrap (if needed), for someone that uses no \n\r, OR
  - OR user-defined wrap-symbol
  - test for ascii control chars (storage in h5 and csv-file) ⇾ or document forbidden chars
    - also base64, 85, 91, or raw
  - continuous stream should also be functional (1MBaud, long duration, creates 10Mbyte stream currently ⇾ might be a problem) ⇾ specify max rate if not possible
- actuation (like UART-Sending):
  - telnet seems not useful (tests can run at night, )
  - top-feature: script on observer with additional logic would be nice (read and write gpio / uart)
  - nice-feature: config-file with time-based send-commands
  - min feature: gpio-actuation per PRU, synced
  - idea: state-machine preload, without reads during run,
- lower sampling bounds should be guaranteed and known ⇾ avoid spurious phantom signals
- Sync-Error should be lower than Clock of GPIO-Register of target

  - Example: 1 / 16 MHz ⇾ 62 ns
- GPIO Actuation, set predefined pins, precise between nodes, resolution can be rather low (100 kHz more than enough, even 10 Hz could be enough), parameters:

  - t_offset (since start of measurement)
  - node(s)
  - GPIO(s)
  - State
- GPIO Actuation for Live View could be beneficial (users can check if system is alive, but what else?) (only nice to have)

## Thoughts on Feasibility

### GPIO Monitoring

- with constant voltage (only current-monitoring, no virtual source model) one PRU-Core would be idle ⇾ custom firmware
- PRU0 handles monitoring el. current, actuating GPIOs, Sync timebase, exchange data-buffers
- PRU1 handles only GPIO-Monitoring ⇾ busy waiting

### UART Monitoring

- current design routes UART to ARM controlled Pins (Linux) and PRU (GPIO Monitoring, discrete timestamped Events)
- Linux UART RX will be tested ⇾ we are currently stuck at kernel 4.19 but have to switch to 5.10+ eventually
- for PRU monitoring the dedicated section applies

### Sync-Error

- there is still a low frequency with unknown origin (~ 0.2 Hz)
- current limits are hard to improve
  - error between nodes: +- 400 ns abs, q95% ~ +- 200 ns
  - error between local triggers: ~ +- 120 ns abs, q95% ~ +- 50 ns
- tbd: deployed cisco-switch in TUD has layer 3 routing and >doubled spec ⇾ could improve sync

## TODO

- implement enablers / general improvements

  - decouple GPIO-Ringbuffer from IV-Stream-Buffer ⇾ size constraint of 16k Events per 100 ms
  - current buffer-swap implementation is not optimal, takes too much time and should be replaced by a big ring-buffer ⇾ makes mutex between PRUs redundant
- test UART RX with kernel 4.19 / 5.10 with 461 and 922 kBaud
- fork PRU-Firmware with focus on GPIO-Speed

  - test capabilities
