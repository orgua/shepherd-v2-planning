# Cape v2.4 - Measurement data

## Ref = GND

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=466.85, stddev=99.89
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=4903.37, stddev=85.11
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3995 V;      I_raw: mean=49276.55, stddev=88.43
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=98601.06, stddev=101.11

DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=465.69, stddev=82.45
DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=4902.77, stddev=70.92
DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9996 V;      I_raw: mean=49274.69, stddev=75.39
DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9993 V;      I_raw: mean=98596.15, stddev=86.44

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9828 V;       I_raw: mean=463.06, stddev=5.78
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=4900.14, stddev=5.81
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8746 V;      I_raw: mean=49275.76, stddev=7.61
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7552 V;      I_raw: mean=98601.86, stddev=12.64
```

## Ref = 10 mV

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1023.15, stddev=99.29
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5464.52, stddev=85.00
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=49884.01, stddev=88.74
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99258.19, stddev=101.85

DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=1182.66, stddev=83.35
DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=5623.73, stddev=73.04
DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9997 V;      I_raw: mean=50041.69, stddev=76.88
DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9995 V;      I_raw: mean=99412.23, stddev=87.57

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9827 V;       I_raw: mean=1458.09, stddev=6.08
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=5899.41, stddev=6.18
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8756 V;      I_raw: mean=50311.76, stddev=7.57
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7576 V;      I_raw: mean=99679.24, stddev=12.69
```

## Ref = 10 mV, double 0R

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1335.36, stddev=99.78
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5776.61, stddev=85.28
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=50194.40, stddev=88.54
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99565.63, stddev=101.33

DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=1494.28, stddev=82.19
DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=5935.56, stddev=71.70
DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9997 V;      I_raw: mean=50351.44, stddev=75.40
DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9994 V;      I_raw: mean=99723.23, stddev=86.35

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9827 V;       I_raw: mean=1771.01, stddev=6.09
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=6212.20, stddev=6.03
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8753 V;      I_raw: mean=50624.02, stddev=7.78
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7568 V;      I_raw: mean=99989.86, stddev=12.78

adc_voltage = value_raw * 1.25 * 4.096 / (2**18)
            = 8.39 mV
```

## Reproducibility

1 week apart, temp diff + smu not warmed up

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1335.36, stddev=99.78
... 1 week apart, temp diff + smu not warmed up ...
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1335.34, stddev=97.43
```

## Ref = 10 mV, like prev + Shorten 2R of ref-source

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1297.64, stddev=97.59
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3997 V;       I_raw: mean=5738.92, stddev=83.36
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3993 V;      I_raw: mean=50152.39, stddev=87.12
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3987 V;      I_raw: mean=99519.54, stddev=101.28

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9827 V;       I_raw: mean=1712.70, stddev=5.71
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9731 V;       I_raw: mean=6152.22, stddev=5.95
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8745 V;      I_raw: mean=50559.49, stddev=7.67
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7553 V;      I_raw: mean=99919.79, stddev=13.19

⇾ deltas: 415 n (lowC), 400 n (highC)
```

## Ref = 10 mV, like prev + remove hrv inAmp from as ref-sink

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1011.49, stddev=137.60
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5449.12, stddev=128.51
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3995 V;      I_raw: mean=49820.79, stddev=127.02
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3991 V;      I_raw: mean=99158.27, stddev=143.76

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9825 V;       I_raw: mean=1012.30, stddev=24.70
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9729 V;       I_raw: mean=5438.26, stddev=9.83
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8746 V;      I_raw: mean=49839.18, stddev=7.63
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7555 V;      I_raw: mean=99205.87, stddev=12.89

⇾ deltas: 1 n (lowC), 47 n (highC)
⇾ relatively high stddev
```

## Ref = 10 mV, like prev + but with 2R for ref-source again

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=991.82, stddev=124.02
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5431.74, stddev=112.72
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3995 V;      I_raw: mean=49799.03, stddev=117.72
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3991 V;      I_raw: mean=99127.33, stddev=127.84

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9826 V;       I_raw: mean=1013.25, stddev=5.71
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9730 V;       I_raw: mean=5453.93, stddev=5.89
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8743 V;      I_raw: mean=49862.53, stddev=7.69
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7547 V;      I_raw: mean=99225.21, stddev=12.89

⇾ deltas: 22 n (lowC), 98 n (highC)
```

## Ref = 10 mV, like prev + terminate ref-end at hrv with 100 nF

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=989.22, stddev=126.67
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5425.08, stddev=115.39
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=49799.86, stddev=121.68
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99130.67, stddev=129.18

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9826 V;       I_raw: mean=1010.08, stddev=5.90
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9731 V;       I_raw: mean=5450.96, stddev=6.09
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8751 V;      I_raw: mean=49861.05, stddev=7.84
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7566 V;      I_raw: mean=99225.34, stddev=12.98

⇾ worse performance?
```

## Ref = 10 mV, short 2R again with 0R

```text
DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1012.27, stddev=145.49
DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5448.99, stddev=135.98
DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=49818.31, stddev=141.67
DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99156.22, stddev=150.77
DAC @ 0.400 V;        SMU: 40.000 mA @ 0.3988 V;      I_raw: mean=197764.61, stddev=166.50
DAC @ 0.400 V;        SMU: 50.000 mA @ 0.3886 V;      I_raw: mean=247049.18, stddev=107.93

DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=1038.09, stddev=142.64
DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9998 V;       I_raw: mean=5478.18, stddev=137.46
DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9996 V;      I_raw: mean=49860.64, stddev=145.65
DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9994 V;      I_raw: mean=99189.29, stddev=151.19
DAC @ 2.000 V;        SMU: 40.000 mA @ 1.9989 V;      I_raw: mean=197791.91, stddev=160.91
DAC @ 2.000 V;        SMU: 50.000 mA @ 1.9883 V;      I_raw: mean=247075.61, stddev=117.17

DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9826 V;       I_raw: mean=1002.66, stddev=5.62
DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9729 V;       I_raw: mean=5438.80, stddev=5.49
DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8725 V;      I_raw: mean=49836.73, stddev=7.33
DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7681 V;      I_raw: mean=99191.95, stddev=16.16
DAC @ 5.000 V;        SMU: 40.000 mA @ 4.4668 V;      I_raw: mean=197841.90, stddev=15.72
DAC @ 5.000 V;        SMU: 50.000 mA @ 4.2851 V;      I_raw: mean=247155.88, stddev=16.96
```
