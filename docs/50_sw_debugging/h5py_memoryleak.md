# Hunting a Memory-leak (h5py)

## First Proof

- RAM-Increase 5% (24mb) in 10 min, slower but steady increase later on
- sheep starts with 13.2 % of system memory ⇾ after 5000 s it uses 28 % already
- setup: 10 h input file, no output-writing for V & C & GPIO
- mem-profiler shows slightly asymptotic behavior ⇾ maybe normal lazy garbage collection depending on free ram?
- after not even 6h the BB became unstable due to saturated RAM

**TLDR: h5py was the culprit ⇾ reading from files**

## Investigation

- only a few possibilities to leaking memory in python ⇾ look for circular references and custom **del**()-methods
- try to avoid exception-handling as a default-strategy in mainloop ⇾ only in shepherdio._get_msg() ⇾ no difference
- file-descriptors or other things without calling close() can leak ⇾ not the case here
- tracemalloc-profiler is in stdlib ⇾ brings no clue as mem usage and peak settle at a low value
  - constant timejumps and higher cpu-usage after 30000 s or 464 of 484 mb RAM
- profile code with pympler, tracker, muppy, ... (<https://pythonhosted.org/Pympler/muppy.html>)
  - finds nothing, code must hide in cpython (compiled libs) out of scope for profiles
- valgrind ⇾ powerful, but too slow to work

```Shell
sudo valgrind --tool=memcheck shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
sudo valgrind --tool=memcheck --leak-check=yes shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
```

- chap <https://stackoverflow.com/questions/61288749/finding-memory-leak-in-python-by-tracemalloc-module>
- fil, python memory profiler, <https://pythonspeed.com/fil/docs/fil/what-it-tracks.html>
  - trouble as arm is not natively supported, but github-issue for arm-macos gives a fix

```Shell
#sudo /usr/bin/python3 -m pip install filprofiler
sudo apt install rustc
pip install git+https://github.com/pythonspeed/filprofiler.git#egg=filprofiler
fil-profile run --no-browser shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
# ⇾ fails to compile for armV7 ⇾ missing SYS_mmap2
```

## Disable Submodules

candidates: logging, memread, h5pywrite, compression ⇾ one by one

- loglevel = 0
- disable h5-writer & compression
- Mods to allow uninterrupted testing
  - pru0/main.c, line99, //send_status(...NOFREEBUF
  - pypkg/init.py, line 626, start_time = + 25
- not use click and logging (logging.getLogger(**name**).addHandler(NullHandler()))
  - rec: mem-usage is growing 11.3? to 12.9 % in 10min, 50% CPU
  - emu1: 13.0 to 13.6.. %, 22 % CPU
  - emu2: 14.1 to 15.3, 55 % CPU ?? ⇾ why not ~80 % ?
- also replace shared_mem.read_buffer() by random-data
  - emu1: 11.7 to 13.7 % ⇾ ram-usage stays between
  - emu2: to 16.3 %
- also replace .get_msg/buffer and emu.return_buffer() by dummy, also gc.collect() in between
  - untrottled run on 100% cpu
  - emu1: 11.7 to 13.7
  - emu2: 13.7 to 16.4
- also skip hdf5-writing
  - emu1: 11.6 - 13.5
  - emu2: 13.6 - 14.6 ⇾ improved memory - for real?
- also skip databuffer-Class
  - e12: up to 14.8
- reading or writing is problem? one h5py-issue mentions vlen-type
  - rec. 10.x - 12.5
- removing lzf again
  - rec. 10.7 - 11.3
- isolated datalogger, 25 min sim,
  - rec 5.6 - 7.9 % (seems to be maxed there), emu
  - emu 6.0 % - 16 % (after 2330 s) ⇾ **that's the bug! reading from h5py, (lzf?)**
- with this result the code could be isolated and the bug is reproducible with pypthon 3.10, windows and even on x86/64bit
