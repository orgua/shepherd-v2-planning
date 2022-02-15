# -*- coding: utf-8 -*-
import os
from typing import NoReturn
import dearpygui.dearpygui as dpg
import time
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import signal
import h5py

def assemble_window(dataseries):

    with dpg.window(tag="main", label="Shepherd Testing and Debug Tool", width=-1, height=-1):
        with dpg.plot(label="Line Series", height=-1, width=-1):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Time [s]")
            dpg.add_plot_axis(dpg.mvYAxis, label="Voltage [V]", tag="y_voltage")
            dpg.add_plot_axis(dpg.mvYAxis, label="Currant [mA]", tag="y_current")
            dpg.add_plot_axis(dpg.mvYAxis, label="Power [mW]", tag="y_power")
            dpg.add_line_series(dataseries["time"].tolist(), dataseries["voltage"].tolist(), label="Voltage [V]", parent="y_voltage", tag="voltage_tag")
            dpg.add_line_series(dataseries["time"].tolist(), (dataseries["current"] * 1e3).tolist(), label="Current [mA]", parent="y_current", tag="current_tag")
            dpg.add_line_series(dataseries["time"].tolist(), (dataseries["power"] * 1e3).tolist(), label="Power [mW]", parent="y_power", tag="power_tag")
            dpg.set_axis_limits_auto("y_voltage")
            dpg.set_axis_limits_auto("y_current")
            dpg.set_axis_limits_auto("y_power")

def stat(dataset, name):
    print(f"-> {name} min={np.min(dataset)}, max={np.max(dataset)}, mean={np.mean(dataset)}")


if __name__ == '__main__':

    infile = "./hrv_iv1000_open.h5"
    dc = dict()

    with h5py.File(infile, "r") as hf:
        ds_time = hf["data"]["time"][:] - hf["data"]["time"][0]
        fs_original = 1e9 / ((ds_time[10000] - ds_time[0]) / 10_000)
        print(f"original sampling rate: {int(fs_original/1000)}kHz")
        dc["time"] = ds_time

        for var in ["voltage", "current"]:
            ds = hf["data"][var]
            # Apply the calibration settings (gain and offset)
            dc[var] = ds[:] * ds.attrs["gain"] + ds.attrs["offset"]
            dc[var][dc[var] < 0] = 0
            stat(dc[var], var)
        dc["power"] = dc["voltage"] * dc["current"]
        stat(dc["power"], "power")
        print(f" power sum = {np.sum(dc['power'])/fs_original}")


    dpg.create_context()
    dpg.create_viewport(title="Shepherd Testing and Debug Tool (VP)", width=1800, height=800)
    dpg.setup_dearpygui()

    assemble_window(dc)
    dpg.set_primary_window("main", True)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

