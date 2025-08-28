# Python Speed-Optimizations

## Benchmarking

Howto

```Shell
sudo python3 -m cProfile -o profile.pstats  /opt/shepherd/software/python-package/shepherd_sheep/cli.py -v run --config /etc/shepherd/example_config_emulation.yml
python -m pip install snakeviz
snakeviz.exe .\profile.pstats

sudo python3 -m cProfile -o profile.pstats  /opt/shepherd/software/python-package/shepherd_sheep/cli.py -v inventorize

# ⇾ cleaner call
sudo python3 -m cProfile -o profile.pstats /usr/bin/shepherd-sheep -v inventorize
```

PyCode-Performance

| Name                  | CPU-Load | Description                           |
|-----------------------|----------|---------------------------------------|
| h5-NoCompression      | 77 %     | 47 mb / 30s                           |
| h5-lzf                | 89 %     | 24 mb/ 30s                            |
| loggerOpt1 - ifVerb   | 84 %     | same                                  |
| loggerOpt2 - traceOff | 83 %     |                                       |
| profiler1             | 83 %     |                                       |
| with monitors         | 91 %     | tevent.wait() instead of time.sleep() |
| same w/o profiling    | 81 %     |                                       |

looking at individual commands - also imports

```Shell
sudo python3 -m timeit -n 1 -r 1 "import shepherd_core"
# 12.8 s on sheep, pydantic 2.4.0
# 11.5 s on sheep, pydantic 2.4.1
# 11.9 s on sheep, pydantic 2.4.2
# 12.4 s on sheep, pydantic 2.5.0 - new pydantic import-improvements?
# 12.1 s on sheep, pydantic 2.5.2
# 12.1 s on sheep, pydantic 2.6.1
# 12.8 s on sheep, pydantic 2.7.0 / 2.18.1 - with lib 24.4.2 (16.6s without cache, 17.7/13.8 deferred)
#  sudo rm /root/.cache/shepherd/fixtures.pickle
#
sudo python3 -X importtime -c "import shepherd_core"
# to shell
sudo python3 -X importtime -c 'from shepherd_core.data_models.task import EmulationTask' 2> profile_pydantic.csv
# to file, now only replace some symbols by ";" and open with excel to sort
```

In addition, there are benchmarks in the main-repo: https://github.com/nes-lab/shepherd/tree/main/software/python-package/tests_manual

## Optimization - Low-hanging Fruits

These things can be done to reduce cpu load:

- ditch lzf-compression for writing files
- compression-tradeoff: double the file-size for ~ 12 less percent-points cpu-load (absolut value)
- disable logging-sys-monitors (cpu/ram-usage, sync ... get written to h5-file) ⇾ per argument
- reduce python-logging ⇾ verbose level argument
- wait for python 3.11 and later ⇾ four performance-stages for cpython are planned (https://github.com/markshannon/faster-cpython/blob/master/plan.md)
- omit writing of timestamp
- overhaul buffer-exchange (segmented ring-buffer should go)
- [according to forum](https://forum.beagleboard.org/t/beaglebone-overclocking-success/11628) the CPU can be overclocked by 60%, RAM by 50%
    - sudo cpufreq-set -g powersave     ⇾ 230mA @ 300 MHz
    - sudo cpufreq-set -g performance   ⇾ 330mA @ 1 GHz
    - cpufreq-info

More Complex, but still easiest optimizations beyond that
- datastream from memory-carveout to hdf5-file should be ported to cython (seems to be possible)
- replace h5py by a more performant lib?
- "click" seems to be slowing down start of programs substantially (is it parsing the whole codebase?)

## Logging Performance-Impact

Logging-module of python has serious performance impact

- example: 4*10 msg/s in debug-mode are >20 % overhead on BB
- follow https://docs.python.org/3/howto/logging.html#optimization
- avoid assembling these 4 most critical fast-Strings
    - __init__.py/emulator.return_buffer(), external verbose
    - datalog.py/LogReader.read_buffers(), generator with internal verbose ⇾ good enough
    - shepherd_io.py/ShepherdIO.get_buffer(), external verbose
        - SharedMem.read_buffer(), external verbose & GPIO-Msg disabled
- try to avoid collection of useless data (thread,process,_srcfile)

Implemented Improvements:

- warn in config-yamls about impact of verbose>2
- avoid overhead (assembling strings, jump in logging-routines) by hiding verbose code in if-branch
- reduce or consolidate debug-code

## General python-Cleanups

- `range(len(x))` ⇾ `enumerate(x)`
- initializes `list([])` ⇾ `[]`, `dict()` ⇾ `{}`
- allow resizing the fifo-buffer, largest value seems to be 107 (< 10k pages)
- https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- not needed `str()` casting for paths before open(), and a lot of other castings removed
- `asyncio.sleep()` or `threading.Event().wait()` in code? ⇾ use sleep(), .wait() has small overhead

- compile h5py for beagle ⇾ fails, see below
- cython, numba, nuitka, pypy: https://doc.pypy.org/en/latest/faq.html

## Updating Py-Libs (without compiling)

Watch out for H5Py improvements ⇾ main load according to profiler

Profiling-results for h5py-3.4

| runtime | Function                               |
|---------|----------------------------------------|
| 624 s   | total runtime                          |
| 26 s    | h5.shape                               |
| 96 s    | sleep                                  |
| 34 s    | h5.datalog.read_buffers.__getitem__    |
| 447 s   | h5.datalog.write_buffers               |
| 184 s   | h5.datalog.?.__getitem__(h5.group.py)  |
| 103 s   | h5.datalog.?._setitem__(h5.dataset.py) |

Update H5Py

```Shell
sudo /usr/bin/python3 -m pip show h5py
# ⇾ v2.1?
sudo /usr/bin/python3 -m pip list --outdated
sudo /usr/bin/python3 -m pip install --upgrade wheel h5py
# ⇾ v3.4
```

updated numpy is giving libblas-trouble

```Shell
sudo /usr/bin/python3 -m pip uninstall numpy scipy
sudo apt --reinstall install python3-numpy python3-scipy

# further update all packets
sudo /usr/bin/python3 -m pip install --upgrade click cryptography decorator distlib
# failing because of distutil greenlet: gevent platformdirs pybind11  msgpack-numpy
sudo /usr/bin/python3 -m pip install --upgrade pyyml six virtualenv zope.event zope.interface
# another distutils: xdg

sudo /usr/bin/python3 -m pip install --upgrade --force-reinstall h5py --no-binary :all:
# ⇾ still fails libhdf5.so after over 1h

# lib-experiments
sudo /usr/bin/python3 -m pip install --upgrade --force-reinstall h5py numpy scipy
sudo apt install python3-dev gfortran libopenblas-base liblapack3 libopenblas-dev liblapack-dev libatlas-base-dev
libopenblas* liblapack*
sudo apt remove libopenblas-base  # could be the culprit that overwrites the one working and needed lib
# https://stackoverflow.com/a/34956540
```

h5py-compilation-cookbook from kai (slightly modded):

```Shell
sudo apt-get install libhdf5-dev
sudo pip3 install --upgrade cython
ln -s /usr/include/locale.h /usr/include/xlocale.h
#sudo /usr/bin/python3 -m pip uninstall numpy h5py
#sudo /usr/bin/python3 -m pip install --only-binary=numpy numpy==1.17.5
sudo /usr/bin/python3 -m pip install --no-binary=h5py h5py
# ⇾ v3.4, created wheel filename=h5py-3.4.0-cp39-cp39-linux_armv7l.whl size=5487437
# ⇾ relatively quick, but no benefit to precompiled version
```
