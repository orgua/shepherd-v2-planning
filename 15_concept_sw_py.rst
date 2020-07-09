Concept - Software - Python API
===============================

- lean on interface of established entry-level projects (i.e. wiring, arduino)
- submodules as classes -> basic configuration at instantiation
- lib could be compiled for speed
- do we need exact timestamps for start and stop or is a global trigger enough
- hdf5 seems a bit overkill -> maybe file-based numpy-data-containers suffice (conversion to csv, xls, ... is a one-liner)
- try to separate between scenario and measurement (reusability)
- modules
   - harvesting-emulator: energy-trace(s), sampling-rate, playback (mirrored, loop)
      - or skip emulator by using constant voltage module
      - traces are file based, there will be a default-folder with pre-selected ones (already on beagle)
   - harvesting-recorder: save-path, capture-duration, start-timestamp, sampling-rate
       - includes current-recorder and switch for dummy-load
   - dc-emulation-modul: converter modell parameter, capacitor parameters, pre-charge ...
      - low-level model in PRU
   - target-module: path for trace-dumps,
      - submodules: firmware (+addressing by firmware-manipulation), uart, gpios
      - allow to disconnect all iO (document in logs with timestamp + Event)
- bidirectional GPIO usage
   - allow to pass thread-function to nodes that handle reactions
- start of measurement should be triggered by absolute timestamp and marks T=0
   - after that it seems easier to use relative time increments for controlling submodules
   - interact with cron-jobs or other linux-scheduler
