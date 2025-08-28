# Test-Setup

- 11x BBB in dedicated vLan of TUD - all PTP clients
- 1x RPi5 as time-server (just ptp, no ntp or GPS)
- Chip-Select of two BBB was recorded for 100s

Changed parameters:

- clockservo: pi or linreg
- cpu-scheduler on server: ondemand or performance
- time to stabilize (1min, 5min)

TODO:

- rpi5 or rpi4 as server (RPi5 shows very high path delays)
- replace ringbuffer and fix misfire (double CS-Pulse)

See [Step-By-Step-Guide](https://nes-lab.github.io/shepherd/dev/time_sync_measurement/readme.html) for hw-setup, measurement and data-preparation.

See [Example Analysis](https://nes-lab.github.io/shepherd/dev/time_sync_analysis/readme.html#) for more context regarding plots and raw-data.


## Results

- general sync with RPi5 seems to be very good -> 5 min is `Δ_q1=356ns`
- system seems to misfire, see screenshots as explanation for too high `Δ_max`

## Raw data from Sync Analysis

```
TYPE: diff
                                                  name  min [ns]  q1 [ns]  q5 [ns]  mean [ns]  q95 [ns]  q99 [ns]  max [ns]  t_min [s]  t_max [s]  Δ_q1 [ns]  Δ_max [ns]
0     01_rp5_master_piservo_1min_cpu_ondemand_diff_0u1     -9252     -292     -226          6       228       274      9116  64.480748  15.878116        566       18368
1     02_rp5_master_piservo_5min_cpu_ondemand_diff_0u1     -9156     -150      -96         30       156       206      9110  64.089889  23.587700        356       18266
2  03_rp5_master_piservo_5min_cpu_performance_diff_0u1     -9238     -250     -192         25       260       406      9314  54.582309  33.281139        656       18552

TYPE: rising
                                                        name  min [ns]  q1 [ns]  q5 [ns]  mean [ns]  q95 [ns]  q99 [ns]  max [ns]  t_min [s]  t_max [s]  Δ_q1 [ns]  Δ_max [ns]
0     01_rp5_master_piservo_1min_cpu_ondemand_ch0_rising_0ms     -8996      -52      -50          1        36        40      9012  55.580258  66.380841         92       18008
1     01_rp5_master_piservo_1min_cpu_ondemand_ch1_rising_0ms     -8998      -52      -50          1        36        84      9012  56.680317  56.680318        136       18010
2     02_rp5_master_piservo_5min_cpu_ondemand_ch0_rising_0ms     -8998      -52      -50          1        36        40      9012  26.987882   4.186654         92       18010
3     02_rp5_master_piservo_5min_cpu_ondemand_ch1_rising_0ms     -8998      -52      -50          1        36        84      9012  54.289352  46.688944        136       18010
4  03_rp5_master_piservo_5min_cpu_performance_ch0_rising_0ms     -8998      -52      -50          1        36        40      9014  66.282936  66.282937         92       18012
5  03_rp5_master_piservo_5min_cpu_performance_ch1_rising_0ms     -8998      -52      -50          1        36        40      9014  39.481476  10.379890         92       18012

TYPE: low
                                                 name  min [ns]  q1 [ns]  q5 [ns]  mean [ns]  q95 [ns]  q99 [ns]  max [ns]  t_min [s]  t_max [s]  Δ_q1 [ns]  Δ_max [ns]
0     01_rp5_master_piservo_1min_cpu_ondemand_ch0_low       102      104      104        104       106       106       106  66.856605   8.000078          2           4
1     01_rp5_master_piservo_1min_cpu_ondemand_ch1_low       102      104      104        105       106       106       106  65.858972   8.000148          2           4
2     02_rp5_master_piservo_5min_cpu_ondemand_ch0_low       102      104      104        104       106       106       106  65.666754   8.002179          2           4
3     02_rp5_master_piservo_5min_cpu_ondemand_ch1_low       102      104      104        105       106       106       106  64.276619   8.000158          2           4
4  03_rp5_master_piservo_5min_cpu_performance_ch0_low       102      104      104        104       106       106       106  64.076955   8.001760          2           4
5  03_rp5_master_piservo_5min_cpu_performance_ch1_low       102      104      104        105       106       106       106  65.761227   8.000250          2           4
```
