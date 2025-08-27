from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

files = {
    # "sync_2BB_20_pi-64-128",
    "sync_2BB_19_smooth_ctrl",
    "sync_2BB_18b_new_trigger",
    # pru only watches for interrupt & immediately triggers adc sampling
    # "sync_2BB_18_new_trigger",
    # "sync_2BB_17_tuning", #
    "sync_2BB_16_tuning",
    "sync_2BB_15_sawtooth_fix",
    "sync_2BB_14_delay_p350",
    "sync_2BB_13_trigger_opt",
    # "sync_2BB_12_pru_opt", # duration to short
    # "sync_2BB_11_pru_opt",  #
    # "sync_2BB_10_pru_opt",  #
    # "sync_2BB_08_pru_opt",  #
    "sync_2BB_07_kernel_opt",
    # "sync_2BB_06_kernel_opt",  #
    # "sync_2BB_05_pru_opt", # the following changes are mostly to reduce pru-overhead
    "sync_2BB_04_crystal_2h",  # changed crystal to a defined 5ppm version
    "sync_2BB_03_n20_4h",
    # "sync_2BB_02_n20_30min",
    "sync_2BB_01_n10_30min",  # ptp delay_filter_length = 10, 30 min time to sync
}
file_names_short = [file.split(".")[0][9:] for file in files]  # reduces to "04_crystal_2h"

sample_frequency = 100e6
sync_list: list = []
trigger_list: list = []


def filter_cs_falling_edge(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = data.columns.str.strip()  # fixes weird space before column-names
    # values are binary -> get timestamps of chipselect-start (falling Edge)
    # - first calc the derivative (current value - previous value)
    # - second filter for "-1" and keep only these
    # - now subtract the timestamps
    # data = data[data["Time[s]"] > 1]
    dtime = data["Time[s]"].iloc[1:]
    ch0 = data.loc[:, "Channel 0"]
    ch0d = pd.Series(ch0.array[1:] - ch0.array[:-1], index=ch0.index[1:])
    ch0t = dtime[ch0d < 0]
    ch1 = data.loc[:, "Channel 1"]
    ch1d = pd.Series(ch1.array[1:] - ch1.array[:-1], index=ch1.index[1:])
    ch1t = dtime[ch1d < 0]
    # filter time-series for start and end that both series cover
    time_start = max(ch0t.min(), ch1t.min()) - 5e-6
    time_stop = min(ch0t.max(), ch1t.max()) - 5e-6
    ch0t = ch0t[(ch0t > time_start) & (ch0t < time_stop)].reset_index(drop=True)
    ch1t = ch1t[(ch1t > time_start) & (ch1t < time_stop)].reset_index(drop=True)
    min_length = min(ch0t.shape[0], ch1t.shape[0])
    # cut series to proper length and determine channel offset
    data_new = [
        ch0t.iloc[0:min_length].mul(1e9).round(0),
        ch1t.iloc[0:min_length].mul(1e9).round(0),
    ]
    df = pd.concat(data_new, axis=1)
    df.columns = ["Ch0", "Ch1"]
    return df


def series_statistics(data: pd.Series, name: str) -> None:
    dmin = int(data.min())
    dmax = int(data.max())
    dq05 = int(data.quantile(0.05))
    dq95 = int(data.quantile(0.95))
    dmean = round(data.mean(), 2)
    print("       \t[  min <|  q05% ||  mean   ||  q95% |>  max ]")
    print(f"{name} \t[ {dmin} <| {dq05} || {dmean} || {dq95} |> {dmax} ]")


def plot_graph(x: Sequence, y: Sequence, y_name: str, filename: str, size: tuple = (18, 8)) -> None:
    fig, ax = plt.subplots(figsize=size)
    len_min = min(len(x), len(y))
    plt.plot(x[:len_min], y[:len_min])
    ax.set_xlabel("time [s]")
    ax.axes.set_ylabel(y_name)
    ax.axes.set_title(filename.split(".")[0])
    fig.savefig(filename)
    plt.close()


def plot_graph2(
    x1: Sequence,
    y1: Sequence,
    x2: Sequence,
    y2: Sequence,
    y_name: str,
    filename: str,
    size: tuple = (18, 8),
) -> None:
    fig, ax = plt.subplots(figsize=size)
    len_min = min(len(x1), len(y1), len(x2), len(y2))
    plt.plot(x1[:len_min], y1[:len_min])
    plt.plot(x2[:len_min], y2[:len_min])
    ax.set_xlabel("time [s]")
    ax.axes.set_ylabel(y_name)
    ax.axes.set_title(filename.split(".")[0])
    fig.savefig(filename)
    plt.close()


if __name__ == "__main__":
    for file in files:
        if Path(file + ".pkl").exists():
            fdata = pd.read_pickle(file + ".pkl", compression="xz")  # noqa: S301
        elif Path(file + ".csv").exists():
            data_raw = pd.read_csv(
                file + ".csv",
                delimiter=",",
                decimal=".",
                float_precision="high",
                index_col=False,
            )  # index_col="Time[s]"
            fdata = filter_cs_falling_edge(data_raw)
            # preprocessing csv and save them as pickle, reduces 240 to 7 mb
            fdata.to_pickle(file + ".pkl", compression="xz")
        else:
            continue

        print(f"\n\nFILE: {file}")
        ch0t = fdata["Ch0"]
        ch1t = fdata["Ch1"]
        time_delta = ch1t - ch0t
        series_statistics(time_delta, "dt_ns")
        ch0td = pd.Series(ch0t.array[1:] - ch0t.array[:-1], index=ch0t.index[1:])
        series_statistics(ch0td, "Ch0_ns")
        ch1td = pd.Series(ch1t.array[1:] - ch1t.array[:-1], index=ch1t.index[1:])
        series_statistics(ch1td, "Ch1_ns")
        ch0t = ch0t.div(1e9)  # bring ns to sec
        ch1t = ch1t.div(1e9)

        plot_graph(ch0t.values, time_delta.values, "sync_delay [ns]", file + "_sync_overview.png")
        plot_graph(
            ch0t.array[0:22000],
            time_delta.array[0:22000],
            "sync_delay [ns]",
            file + "_sync_detail.png",
            (30, 8),
        )
        plot_graph(
            ch0t.array[:22000],
            ch0td.array[:22000],
            "trigger_delay [ns]",
            file + "_trigger_period_ch0.png",
            (30, 8),
        )
        plot_graph(
            ch1t.array[:22000],
            ch1td.array[:22000],
            "trigger_delay [ns]",
            file + "_trigger_period_ch1.png",
            (30, 8),
        )
        sync_list.append(time_delta)
        trigger_list.append(ch0td)

    file_names_short.reverse()
    fig_title = "improvement_sync_statistics_boxplot"
    sync_list.reverse()
    df = pd.concat(sync_list, axis=1)
    df.columns = file_names_short
    ax = df.plot.box(figsize=(20, 8), return_type="axes")
    ax.set_ylabel("sync_delay [ns]")
    ax.set_title(fig_title)
    plt.grid(
        visible=True,
        which="major",
        axis="y",
        color="grey",
        linewidth="0.6",
        linestyle=":",
        alpha=0.8,
    )
    plt.savefig(fig_title + ".png")
    plt.close()

    trigger_list.reverse()
    fig_title = "improvement_trigger_statistics_boxplot"
    df = pd.concat(trigger_list, axis=1)
    df.columns = file_names_short
    ax = df.plot.box(figsize=(20, 8), return_type="axes")
    ax.set_ylabel("trigger_delay [ns]")
    ax.set_title(fig_title)
    plt.grid(
        visible=True,
        which="major",
        axis="y",
        color="grey",
        linewidth="0.6",
        linestyle=":",
        alpha=0.8,
    )
    plt.savefig(fig_title + ".png")
    plt.close()

    file_title = "improvement_sync"
    plot_graph(
        sync_list[0].values,
        time_delta.values,
        "sync_delay [ns]",
        file_title + "_sync_overview_vs.png",
    )
    plot_graph(
        ch0t.array[0:22000],
        time_delta.array[0:22000],
        "sync_delay [ns]",
        file_title + "_sync_detail_vs.png",
        (30, 8),
    )
