# Timesync Revisited 2024

## Adding a dedicated server

### BBB

```Shell
jane@sheep01:~$ ethtool -T eth0
Time stamping parameters for eth0:
Capabilities:
        hardware-transmit     (SOF_TIMESTAMPING_TX_HARDWARE)
        software-transmit     (SOF_TIMESTAMPING_TX_SOFTWARE)
        hardware-receive      (SOF_TIMESTAMPING_RX_HARDWARE)
        software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)
        software-system-clock (SOF_TIMESTAMPING_SOFTWARE)
        hardware-raw-clock    (SOF_TIMESTAMPING_RAW_HARDWARE)
PTP Hardware Clock: 0
Hardware Transmit Timestamp Modes:
        off                   (HWTSTAMP_TX_OFF)
        on                    (HWTSTAMP_TX_ON)
Hardware Receive Filter Modes:
        none                  (HWTSTAMP_FILTER_NONE)
        ptpv1-l4-event        (HWTSTAMP_FILTER_PTP_V1_L4_EVENT)
        ptpv2-event           (HWTSTAMP_FILTER_PTP_V2_EVENT)
```

Path delay is between 12000 and 14000

### RPi5

```Shell
jane@timeserver01:~ $ ethtool -T eth0
Time stamping parameters for eth0:
Capabilities:
        hardware-transmit
        software-transmit
        hardware-receive
        software-receive
        software-system-clock
        hardware-raw-clock
PTP Hardware Clock: 0
Hardware Transmit Timestamp Modes:
        off
        on
        onestep-sync
Hardware Receive Filter Modes:
        none
        all
```

Strangely the path delay doubled!

```text
Sep 23 19:43:52 sheep13 ptp4l[5882]: [453507.381] master offset         55 s2 freq +126528 path delay     25939
Sep 23 19:43:53 sheep13 ptp4l[5882]: [453508.381] master offset       -124 s2 freq +126366 path delay     25940
Sep 23 19:43:54 sheep13 ptp4l[5882]: [453509.381] master offset        -19 s2 freq +126434 path delay     25940
```

## Tuning parameters

- related systemd services failed after a reboot on the PI - they started too early - changing `Type=simple` to `=idle`
- timeservers now got `masterOnly 1` in ptp4l.conf
- ptp has a better `clock_servo linreg` instead of `pi` (phc2sys already had this via cmd-line parameter)
-
