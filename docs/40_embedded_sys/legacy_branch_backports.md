# Legacy V1 Code-Branch

This document is for tracking backports made for v1 branch

## Intro

- for hw revision 1.x
- where: https://github.com/nes-lab/shepherd/tree/hw_revision_1.x
- branched on 15. Jan 2021 [52f087a]
- currently 227 commits behind main
    - main is not stable, fall back to [1c02230] 21. Feb 2021 (branch "fw_ok")
- comparison
    - legacy (15. Jan) vs fw_ok ⇾ https://github.com/nes-lab/shepherd/compare/hw_revision_1.x...orgua:fw_ok
    - legacy (20. Apr) vs master ⇾ https://github.com/nes-lab/shepherd/compare/hw_revision_1.x...orgua:master
        - "two points"-Compare seem to be more helpful https://github.com/nes-lab/shepherd/compare/orgua:master..orgua:hw_revision_1.x
    - legacy (20. Apr) vs master ⇾ https://github.com/nes-lab/shepherd/compare/fw_ok..orgua:master


## Improvements 2021-06-01

- fix overwrite-bug in playbook for files in /etc/shepherd/

## Improvements 2021-05-06

- 1.x branch is now on par with v2-branch from 2021-05-06, except for
    - rpmsg-replacement for buffer exchange ⇾ must be thoroughly tested first
    - optimized spi-asm-code (faster, simultaneous clk/data-edges) ⇾ ICs have changed in v2

- make-system fixed and improved
- ansible playbooks improved
- pru: many bottlenecks and overhead removed ⇾ headroom for more complex code
    - gpio is now sampled with 1.0 to 5.5 MHz (mean ~ 4 MHz)
    - is mostly depending on spi-transfer but whole emulation takes 6860 ns of max of 10000 ns (100 kHz)
    - timesync is mostly done by kernel (less overhead for pru)
- pru: some race conditions could be identified and removed
- pru: biggest time-waster in
    - 4340 ns sampling() / harvesting & load
    - 6860 ns sampling() / emulation
    - 2740 ns handling block end ⇾ pru1-blocking part was reduced to 460 ns
- c-code-quality
    - less global vars
    - usage of fixed width ints
    - more const-correctness
    - better naming
    - less magic numbers
- adc-sampling of pru0 reacts directly to interrupt now instead of extra trigger from pru1 ⇾ less jitter and less error
    - both PRUs had separate sample-counters and were more vulnerable to race-conditions
    - pru1 does not use rpmsgs for sync-system with kernel-module but a simple system via shared-memory
        - before: checking for a message took ~550 ns and receiving (and processing) it took ~ 4800 ns
        - new system checks in 40 ns and receives & processes in 1140 ns
        - the transmission of the system also works faster ⇾ previously the pru was checking for messages ~8 times, now the answer is there on first or second try
        - gpio-sampling was improved by that: min frequency increased from <200 kHz to 600 kHz, mean is now at ~4.00 MHz
        - for reference: timings were taken with enabled debug-code
- python
    - improved console output
    - more explicit code
    - more graceful handling of common errors or user-induced exits
- API-Changes Python ⇾ same as v2 codebase
    - input ⇾ input_path
    - output ⇾ output_path (still -o)
    - length ⇾ duration (now -d instead of -l)
    - force ⇾ force_overwrite (still -f)
    - eeprom_wp ⇾ eeprom_write (properly reflect behavior)
    - NOTE1: if only an output-directory is specified the recording will be saved with an ISO 8601 timestamp (ie. rec_2021-04-20_12-12-12.h5)
    - NOTE2: this fixes (theoretical) conflict with -l for shepherd-herd (--limit) and sheep (--length)
- removed virtcap-code, as it was not working as intended
- more sanity-checks throughout codebase, i.e.
    - unusual jumps for buffer-timestamps are shown (in kernel before sending to pru, in python after receiving from pru)
    - time-sync gets reported from kernel-module when not stabile (yet)
    - show when a message to pru stays unread (backpressure) or it is altered (hint for mem-corruption)
    - [...]

## Known Bugs / Open Issues

- ending python programs with ctrl&c can result in (false) error-messages - graceful shutdown is yet to come
- starting the sheep with

### Pipenv-Trouble

- pipenv fails to scan for deps in sub-folders when python wasn't pinned to v3 (
- black-lib had troubles -
    - kai uses "--pre" for installation
    - i used "pipenv install "black==20.8b1" (if i recall correctly)
- dbus-python package had trouble with sub-dependency (dbus-1), when the following apt-package wasn't installed: libdbus-glib-1-dev

Pipenv (TODO: not perfect place here)

```Shell
pipenv --three
pipenv install
pipenv shell
pipenv run pip list
pipenv --rm
pipenv update
pipenv graph
```

## TODO

- asm-code in main-branch is cleaner and edges are clock-synchronous
- commits from legacy
- commits from main:
- synced with master: 72aad92 - may 06
- original/dev-branch: 8b3054d 9e5925729e60939e137b970e1791e9a4f (21-04-19) ..d9a5073 24e1123fc6af10117351d0a703f28f1ef (21-05-05)

```Shell
cd /opt/shepherd/software/python-package/
sudo python3 setup.py test --addopts "-vvv"

cp /opt/shepherd/software/meta-package/example_config.yml /etc/shepherd/config.yml
sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml
dmesg -wH
watch -n 1 "df -h"
# plot with tool in /extras

# merge several commits from A to B to another branch
git cherry-pick A^..B
```
