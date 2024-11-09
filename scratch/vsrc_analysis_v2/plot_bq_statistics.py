from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from bq_kit import paths_digital, get_digital, get_analog, paths_analog
from solar import paths_ivcurve, open_ivcurve

result_eval: dict = {
    "name": [],
    "intensity": [],
    "duty_on": [],
    "rate_per_min": [],
    "durations_on": [],
    "efficiency": [],
}

for name, path in paths_digital.items():
    # first cmd throws away 1st & last entry to avoid partially sampled durations
    data = get_digital(path).iloc[1:-1, :]
    # generate Stats
    timestamps = data["Time [s]"].to_numpy()
    if timestamps.shape[0] < 2:
        print(f"skipping {name} due to low BAT-OK activity")
        continue
    durations = timestamps[1:] - timestamps[:-1]
    time_total = timestamps[-1] - timestamps[0]
    data = data.iloc[:-1, :]  # last value is unusable for this
    data["duration"] = durations
    filter_on = data["BAT_OK"] == 1
    durations_on = data.loc[filter_on, "duration"].to_numpy()
    duty_on = 100 * durations_on.sum() / time_total
    rate_per_min = filter_on.sum() / time_total * 60.0
    print(f"{name}, duty = {duty_on:.1f} %, "
          f"switch_rate = {rate_per_min:.3f} n/min, "
          f"on-time min {1000*durations_on.min():.2f} ms, "
          f"mean {1000*durations_on.mean():.2f} ms, "
          f"max {1000*durations_on.max():.2f} ms")
    # efficiency - combined with ivcurve
    path_ivcurve = paths_ivcurve.get(name[:8])
    if path_ivcurve:
        ivcurve = open_ivcurve(path_ivcurve)
        P_inp_max = (ivcurve["Voltage [V]"] * ivcurve["Current [A]"]).max()
    else:
        raise FileNotFoundError("No IV curve available")
    data_analog = get_analog(paths_analog[name])
    R_out = 1000
    P_out = data_analog["V_OUT"] * data_analog["V_OUT"] / R_out
    # duration = data_analog["Time [s]"].iloc[-1] - data_analog["Time [s]"].iloc[0]
    P_out_mean = P_out.sum() / len(P_out)
    efficiency = 100 * P_out_mean / P_inp_max
    # save stats for plots
    result_eval["name"].append(name)
    result_eval["intensity"].append(float(name[4:6]))
    result_eval["duty_on"].append(duty_on)
    result_eval["rate_per_min"].append(rate_per_min)
    result_eval["durations_on"].append(durations_on)
    result_eval["efficiency"].append(efficiency)


fig, axs = plt.subplots(4, 1, sharex="all", figsize=(10, 2 * 6), layout="tight")
fig.suptitle(f"BQ25570 Eval Kit Characteristics")

axs[0].set_ylabel("Duty Cycle [%]")
axs[0].plot(result_eval["intensity"], result_eval["duty_on"])
# axs[0].legend(["Sim", "Eval"], loc="upper right")

axs[1].set_ylabel("Switch Rate [n/min]")
axs[1].plot(result_eval["intensity"], result_eval["rate_per_min"])

axs[2].set_ylabel("On-duration [s]")
axs[2].plot(result_eval["intensity"], [_x.min() for _x in result_eval["durations_on"]])
axs[2].plot(result_eval["intensity"], [_x.mean() for _x in result_eval["durations_on"]])
axs[2].plot(result_eval["intensity"], [_x.max() for _x in result_eval["durations_on"]])
axs[2].legend(["min", "mean", "max"], loc="lower right")
axs[2].set_yscale("log")

axs[3].set_ylabel("Efficiency [%]")
axs[3].plot(result_eval["intensity"], result_eval["efficiency"])
axs[3].set_xlabel("LED-Intensity [%]")
axs[3].set_xticks(np.arange(2, 23, 2))

for ax in axs:
    # deactivates offset-creation for ax-ticks
    #ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.grid(True)

# TODO: add efficiency, PwrIn, PwrOut

plt.savefig(Path(__file__).with_suffix(".png"))
plt.savefig(Path(__file__).with_suffix(".svg"))
plt.close(fig)
plt.clf()
