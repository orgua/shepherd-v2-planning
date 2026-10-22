# Timesync - PTP-tuning

## Problem

- ptp seems to sync too fast - the client is oscillating around 500 ns offset with +- 500 ns jitter
- ptp seems to loose sync from time to time
  - logs show a big jump in frequency and the node needs some minutes to recover
- setup - like in last doc "timesync_pru_level"

## Log of Losing Sync

```Shell
sudo journalctl -u ptp4l (Client)

    Feb 16 10:58:18 sheep1 ptp4l[378]: [802.623] master offset       -395 s2 freq  +43044 path delay     12491
    Feb 16 10:58:19 sheep1 ptp4l[378]: [803.623] master offset       -338 s2 freq  +42983 path delay     12483
    Feb 16 10:58:20 sheep1 ptp4l[378]: [804.624] master offset       -338 s2 freq  +42881 path delay     12483
    Feb 16 10:58:21 sheep1 ptp4l[378]: [805.624] master offset       -257 s2 freq  +42861 path delay     12485
    Feb 16 10:58:22 sheep1 ptp4l[378]: [806.624] master offset       -325 s2 freq  +42716 path delay     12485
    Feb 16 10:58:23 sheep1 ptp4l[378]: [807.625] master offset       -346 s2 freq  +42597 path delay     12488
    Feb 16 10:58:24 sheep1 ptp4l[378]: [808.625] master offset      26301 s2 freq  +69140 path delay     12488
    Feb 16 10:58:25 sheep1 ptp4l[378]: [809.626] master offset     147687 s2 freq +198417 path delay     12484
    Feb 16 10:58:26 sheep1 ptp4l[378]: [810.626] master offset     291723 s2 freq +386759 path delay     12482
    Feb 16 10:58:27 sheep1 ptp4l[378]: [811.627] master offset     279267 s2 freq +461820 path delay     12484
    Feb 16 10:58:28 sheep1 ptp4l[378]: [812.627] master offset     177496 s2 freq +443829 path delay     12493
    Feb 16 10:58:29 sheep1 ptp4l[378]: [813.627] master offset      69843 s2 freq +389425 path delay     12493
    Feb 16 10:58:30 sheep1 ptp4l[378]: [814.627] master offset      -3069 s2 freq +337466 path delay     12498
    Feb 16 10:58:31 sheep1 ptp4l[378]: [815.627] master offset     -36917 s2 freq +302697 path delay     12498
    Feb 16 10:58:32 sheep1 ptp4l[378]: [816.628] master offset     -43520 s2 freq +285019 path delay     12498
    Feb 16 10:58:33 sheep1 ptp4l[378]: [817.628] master offset     -35970 s2 freq +279513 path delay     12498
    Feb 16 10:58:34 sheep1 ptp4l[378]: [818.628] master offset     -24814 s2 freq +279878 path delay     12498
    Feb 16 10:58:35 sheep1 ptp4l[378]: [819.628] master offset     -14984 s2 freq +282264 path delay     12498
    Feb 16 10:58:36 sheep1 ptp4l[378]: [820.629] master offset      -8124 s2 freq +284628 path delay     12488
    Feb 16 10:58:37 sheep1 ptp4l[378]: [821.629] master offset      -4426 s2 freq +285889 path delay     12484
    Feb 16 10:58:38 sheep1 ptp4l[378]: [822.630] master offset      -2714 s2 freq +286273 path delay     12484
    Feb 16 10:58:39 sheep1 ptp4l[378]: [823.630] master offset      -2257 s2 freq +285916 path delay     12448
    Feb 16 10:58:40 sheep1 ptp4l[378]: [824.630] master offset      -2299 s2 freq +285197 path delay     12484
    Feb 16 10:58:41 sheep1 ptp4l[378]: [825.631] master offset      -2659 s2 freq +284147 path delay     12469
    Feb 16 10:58:42 sheep1 ptp4l[378]: [826.631] master offset      -2634 s2 freq +283375 path delay     12439
    Feb 16 10:58:43 sheep1 ptp4l[378]: [827.631] master offset      -3034 s2 freq +282184 path delay     12480
    Feb 16 10:58:44 sheep1 ptp4l[378]: [828.632] master offset      -2953 s2 freq +281355 path delay     12480
    ⇾ output of ptp-master shows no strange messages, BUT phc2sys on master
```

```text
sudo journalctl -u phc2sys  (Master)
    Feb 16 10:58:22 sheep0 phc2sys[358]: phc2sys[1105.795]: sys offset      -316 s2
    Feb 16 10:58:23 sheep0 phc2sys[358]: phc2sys[1106.796]: sys offset      -321 s2
    Feb 16 10:58:24 sheep0 phc2sys[358]: phc2sys[1107.797]: sys offset     72504 s2
    Feb 16 10:58:25 sheep0 phc2sys[358]: phc2sys[1108.797]: sys offset    257798 s2
    Feb 16 10:58:26 sheep0 phc2sys[358]: phc2sys[1109.798]: sys offset    234922 s2
    Feb 16 10:58:27 sheep0 phc2sys[358]: phc2sys[1110.799]: sys offset    156508 s2
    Feb 16 10:58:28 sheep0 phc2sys[358]: phc2sys[1111.799]: sys offset     85091 s2
    Feb 16 10:58:29 sheep0 phc2sys[358]: phc2sys[1112.800]: sys offset     37172 s2
    Feb 16 10:58:30 sheep0 phc2sys[358]: phc2sys[1113.800]: sys offset     10707 s2
    Feb 16 10:58:31 sheep0 phc2sys[358]: phc2sys[1114.801]: sys offset     -1419 s2
    Feb 16 10:58:32 sheep0 phc2sys[358]: phc2sys[1115.802]: sys offset     -5533 s2
    Feb 16 10:58:33 sheep0 phc2sys[358]: phc2sys[1116.802]: sys offset     -6101 s2
    Feb 16 10:58:34 sheep0 phc2sys[358]: phc2sys[1117.803]: sys offset     -5399 s2
    Feb 16 10:58:35 sheep0 phc2sys[358]: phc2sys[1118.804]: sys offset     -4465 s2
    Feb 16 10:58:36 sheep0 phc2sys[358]: phc2sys[1119.804]: sys offset     -3781 s2
```

```text
cp /opt/shepherd/software/meta-package/example_config_harvest.yml /etc/shepherd/config.yml
sudo shepherd-sheep -vvv run --config /etc/shepherd/config.yml
```

## Config-tuning

- found in /etc/linuxptp/ptp4l.conf
- explained vars: <https://www.mankier.com/8/ptp4l>

Possible tuning-candidates

```text
delay_filter_length     was 10 samples, try higher val, 100 is too much, 20
egressLatency or ingressLatency, probably ingress to get rid of static offset
clockAccuracy
clock_servo
```

### Tuning delay filter length to 20 - after 30min

```text
(master)
Feb 16 11:29:11 sheep0 phc2sys[358]: phc2sys[2954.880]: sys offset       -35 s2 freq  +59597 delay   3976
Feb 16 11:29:12 sheep0 phc2sys[358]: phc2sys[2955.880]: sys offset        22 s2 freq  +59644 delay   3976
Feb 16 11:29:13 sheep0 phc2sys[358]: phc2sys[2956.881]: sys offset       -88 s2 freq  +59541 delay   3959
Feb 16 11:29:14 sheep0 phc2sys[358]: phc2sys[2957.881]: sys offset       -48 s2 freq  +59554 delay   3984
Feb 16 11:29:15 sheep0 phc2sys[358]: phc2sys[2958.882]: sys offset       -39 s2 freq  +59549 delay   3967
Feb 16 11:29:16 sheep0 phc2sys[358]: phc2sys[2959.882]: sys offset       -63 s2 freq  +59513 delay   3960
Feb 16 11:29:17 sheep0 phc2sys[358]: phc2sys[2960.882]: sys offset       -40 s2 freq  +59517 delay   3967
Feb 16 11:29:18 sheep0 phc2sys[358]: phc2sys[2961.883]: sys offset       -83 s2 freq  +59462 delay   4000
Feb 16 11:29:19 sheep0 phc2sys[358]: phc2sys[2962.883]: sys offset       -21 s2 freq  +59499 delay   3976
Feb 16 11:29:20 sheep0 phc2sys[358]: phc2sys[2963.884]: sys offset       -51 s2 freq  +59463 delay   4000
Feb 16 11:29:21 sheep0 phc2sys[358]: phc2sys[2964.884]: sys offset       -39 s2 freq  +59460 delay   3968
Feb 16 11:29:22 sheep0 phc2sys[358]: phc2sys[2965.885]: sys offset       -63 s2 freq  +59424 delay   3991
Feb 16 11:29:23 sheep0 phc2sys[358]: phc2sys[2966.885]: sys offset       -52 s2 freq  +59416 delay   3991
```

```text
(client)
Feb 16 11:29:29 sheep1 ptp4l[378]: [2673.354] master offset        -14 s2 freq  +65139 path delay     12478
Feb 16 11:29:30 sheep1 ptp4l[378]: [2674.355] master offset        -36 s2 freq  +65112 path delay     12478
Feb 16 11:29:31 sheep1 ptp4l[378]: [2675.355] master offset        -11 s2 freq  +65127 path delay     12489
Feb 16 11:29:32 sheep1 ptp4l[378]: [2676.356] master offset       -127 s2 freq  +65007 path delay     12489
Feb 16 11:29:33 sheep1 ptp4l[378]: [2677.357] master offset        -75 s2 freq  +65021 path delay     12489
Feb 16 11:29:34 sheep1 ptp4l[378]: [2678.357] master offset        118 s2 freq  +65192 path delay     12489
Feb 16 11:29:35 sheep1 ptp4l[378]: [2679.358] master offset       -131 s2 freq  +64978 path delay     12489
Feb 16 11:29:36 sheep1 ptp4l[378]: [2680.359] master offset        -93 s2 freq  +64977 path delay     12489
Feb 16 11:29:37 sheep1 ptp4l[378]: [2681.359] master offset        -58 s2 freq  +64984 path delay     12489
Feb 16 11:29:38 sheep1 ptp4l[378]: [2682.360] master offset          7 s2 freq  +65031 path delay     12484
Feb 16 11:29:39 sheep1 ptp4l[378]: [2683.361] master offset         40 s2 freq  +65067 path delay     12484
Feb 16 11:29:40 sheep1 ptp4l[378]: [2684.361] master offset        -78 s2 freq  +64961 path delay     12484
Feb 16 11:29:41 sheep1 ptp4l[378]: [2685.362] master offset       -110 s2 freq  +64905 path delay     12484
⇾ near < 100 ns jitter
```

### Tuning delay filter length to 20 - after 4h

```text
(master)
Feb 16 14:48:09 sheep0 phc2sys[358]: phc2sys[14892.879]: sys offset        -8 s2 freq  +67159 delay   3968
Feb 16 14:48:10 sheep0 phc2sys[358]: phc2sys[14893.880]: sys offset        -3 s2 freq  +67162 delay   4000
Feb 16 14:48:11 sheep0 phc2sys[358]: phc2sys[14894.880]: sys offset        19 s2 freq  +67183 delay   3976
Feb 16 14:48:12 sheep0 phc2sys[358]: phc2sys[14895.880]: sys offset        15 s2 freq  +67185 delay   3968
Feb 16 14:48:13 sheep0 phc2sys[358]: phc2sys[14896.881]: sys offset       -17 s2 freq  +67157 delay   3992
Feb 16 14:48:14 sheep0 phc2sys[358]: phc2sys[14897.881]: sys offset        -7 s2 freq  +67162 delay   4000
Feb 16 14:48:15 sheep0 phc2sys[358]: phc2sys[14898.882]: sys offset         5 s2 freq  +67172 delay   3976
Feb 16 14:48:16 sheep0 phc2sys[358]: phc2sys[14899.882]: sys offset       -13 s2 freq  +67155 delay   3991
Feb 16 14:48:17 sheep0 phc2sys[358]: phc2sys[14900.882]: sys offset       -31 s2 freq  +67134 delay   3984
Feb 16 14:48:18 sheep0 phc2sys[358]: phc2sys[14901.883]: sys offset        23 s2 freq  +67178 delay   3984
Feb 16 14:48:19 sheep0 phc2sys[358]: phc2sys[14902.883]: sys offset        32 s2 freq  +67194 delay   3960
Feb 16 14:48:20 sheep0 phc2sys[358]: phc2sys[14903.883]: sys offset       -10 s2 freq  +67162 delay   3984
Feb 16 14:48:21 sheep0 phc2sys[358]: phc2sys[14904.884]: sys offset        -8 s2 freq  +67161 delay   3976
```

```text
(client)
Feb 16 14:48:33 sheep1 ptp4l[378]: [14617.669] master offset         -9 s2 freq  +73133 path delay     12496
Feb 16 14:48:34 sheep1 ptp4l[378]: [14618.669] master offset         42 s2 freq  +73181 path delay     12496
Feb 16 14:48:35 sheep1 ptp4l[378]: [14619.670] master offset         33 s2 freq  +73185 path delay     12493
Feb 16 14:48:36 sheep1 ptp4l[378]: [14620.670] master offset         54 s2 freq  +73216 path delay     12493
Feb 16 14:48:37 sheep1 ptp4l[378]: [14621.670] master offset        -46 s2 freq  +73132 path delay     12493
Feb 16 14:48:38 sheep1 ptp4l[378]: [14622.670] master offset          6 s2 freq  +73170 path delay     12486
Feb 16 14:48:39 sheep1 ptp4l[378]: [14623.671] master offset         30 s2 freq  +73196 path delay     12486
Feb 16 14:48:40 sheep1 ptp4l[378]: [14624.671] master offset        -57 s2 freq  +73118 path delay     12494
Feb 16 14:48:41 sheep1 ptp4l[378]: [14625.671] master offset         30 s2 freq  +73188 path delay     12494
Feb 16 14:48:42 sheep1 ptp4l[378]: [14626.672] master offset         33 s2 freq  +73200 path delay     12500
Feb 16 14:48:43 sheep1 ptp4l[378]: [14627.672] master offset         46 s2 freq  +73223 path delay     12500
Feb 16 14:48:44 sheep1 ptp4l[378]: [14628.672] master offset        -65 s2 freq  +73126 path delay     12500
Feb 16 14:48:45 sheep1 ptp4l[378]: [14629.673] master offset        -94 s2 freq  +73077 path delay     12500
⇾ clearly < 100 ns jitter
```

### Tuning Config with DelayAsymmetry for ptp4l

- try "delayAsymmetry": The time difference in nanoseconds of the transmit and receive paths. This value should be positive when the master-to-slave propagation time is longer and negative when the slave-to-master time is longer. The default is 0 nanoseconds.
- only relevant if ptp-master is also measuring
- client lacks behind ~400 ns, try correcting it with +200 (half of value)
- seems to be improving, maybe a bit to much. will set to 100 for now

### Tuning Config with delay_filter_length for ptp4l

- a higher filter length, shows very slow asymptotic behavior, but clock seems more stable ⇾ try higher pi_integral_value
- change from 10 to 20 had huge success
- change to 30 and restart of both nodes brought a very slow startup. 1800 s (30min) for sub 1 us (CS-edges)
  - could be improved by raising limit for clock-skew
  - ⇾ ptp4l-log does not show any improvements

## Clock-Crystal on BB

- Schematic shows MC-306, an Epson 100ppm crystal, with two 18 pF Capacitors around (C_12)
- Package says 32C846, so it is a unspecified replacement
- a replacement part CM200C32768HZFT (5ppm, 12.5pF) from Citizen FineDevice has similar marking "32C826"
  - there are 20, 10 and 5 ppm - Versions
  - load capacitance CL: 6, 9, 12.5, 7 pF
  - C_12 = 2 * (CL - C_Pin - C_pcb)
    - with guesses for the unknown capacities: C_pin ~ 1 pF, C_pcb ~ 4pF (Script), C_12_max ~ 20 pF
    - CL = C_12/2 + C_Pin + C_pcb = 18/2 + 1 + 4 = 14 pF ⇾ next best match is the 12.5 pF Version
- replaced client, master kept running, resync only took 80s and it was on a level that is similar to the previous 4h period

## TODO

- try to check SERVO_LOCKED_STABLE, clock enters this state when timing is considered ok
  - config: servo_offset_threshold, servo_num_offset_values
- there seem to be ptp-options in the switch
