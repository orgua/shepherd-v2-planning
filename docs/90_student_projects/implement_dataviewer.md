# Dataviewer

## Implementation of a Dataviewer for Shepherd-Recordings

The Shepherd-Testbed produces voltage-, current and gpio-traces that can be post-processed by the [shepherd-tools](https://github.com/nes-lab/shepherd-tools). The tools serve as a documentation for the internal h5-structure for shepherd as well as a tool for creating, reading and modifying the recordings. There is also some basic plotting implemented based on matplotlib, but a fast and responsive data-viewer would be extremely helpful as recordings can span over several days and may include up to 30 - 100 shepherd-nodes.

A data-viewer would allow to identify points of interest by quickly skimming over the dataset. The ability to zoom into the traces is a required feature. As it is also possible to sample digital signals it would be also nice to have an option to decode protocols like uart.

The implementation would be preferably based on an existing software. On the first look sigrok & pulseview look promising. Pulseview seems to support several input-formats, so a converter should suffice. But maybe it is also possible to extend Pulseview to support the shepherd-hdf5-format directly.

## Current Situation

Each `Shepherd Node` produces:

- IV-Samples (voltage & current) with 100 kHz and 18bit resolution
- event based gpio-sampling of 10 pins (with at least one high-speed capable uart good for 4 - 10 MBaud)

The data-tool allows to plot parts of the ivsample-recording ⇾ [CLI-Interface ⇾ Plot IVSamples](https://github.com/nes-lab/shepherd-tools#cli-interface>). Multiplots for several recordings are supported, as well as prior downsampling.

There is a basic implementation of a [viewer based on DPG](https://github.com/orgua/shepherd-v2-planning/blob/main/scratch/shepherd_dataview/viewer.py>). It is limited to one recording, only IVSamples and is not optimized at all. So recordings >60s are challenging because there is no downsampling depending on the zoom-levels.

The Saleae Logic tool has an [open api](https://support.saleae.com/extensions/api-documentation) and file format, but does only support gpio- and voltage-traces. Shepherd features also current-traces or derived power-traces.

Tests with timeseries-databases were done. TimescaleDB and InfluxDB are both to slow to handle the live data of 30 nodes in the testbed. So currently the database-idea was put on hold for a pure file-based approach.

## Goals

From high to lower priority:

- have an interactive viewer for iv-sample-data and gpio-traces with timestamps
- a web-viewer would be helpful for the testbed itself
- a standalone viewer would also be desired (but can be the wrapped web-viewer)
- preferably written in python (like all other high-level shepherd-tools)
- allow to overlay several recordings or plot them in individual graphs (no overlay but in series) with the same timebase (both has advantages)
- decoding digital protocols like uart and spi
- search / highlight points of interest ⇾ tbd

Side-notes:

- data-conversion is OK ⇾ probably a more performant format and a chain of downsamples are needed to handle the performance on large overviews
- in terms of usability and functionality the tool [Saleae Logic](https://www.saleae.com/downloads/) is regarded as a role model

## Milestones / Steps

TBD, proposal:

- prepare an overview of options
- prototype experiments
- decision how to proceed
- redefine goals and possible features
- working version of the viewer


## Useful links

`FlockLab` - a similar Testbed [implemented plotting](https://github.com/ETHZ-TEC/FlockLab-Tools) with [Bokeh](https://bokeh.org/) both for web and offline usage.

An alternative to Bokeh could be [plotly](https://github.com/plotly/plotly.py).
source: <https://pauliacomi.com/2020/06/07/plotly-v-bokeh.html>

For bundling and filtering plots in an overview-page:

- <https://awesome-panel.org/> ⇾ the video <https://www.youtube.com/watch?v=0DBEXiMdSKc&t=530s> talks about Terabytes of data visualized with datashader, rapids cuxFilter ⇾ problem: GPU / CUDA based
- Alternative: [Streamlit](https://streamlit.io)

More Info on current GPIO-Pins routed to the targets:

- [General Info](https://nes-lab.github.io/shepherd/dev/v2_improvements.html#pins-to-target)
- [Bit Position Info included in H5-File](https://github.com/nes-lab/shepherd/blob/main/software/python-package/shepherd/commons.py#L38)

## Test-Data

- the [tool-examples](https://github.com/nes-lab/shepherd-tools/blob/main/shepherd_data/examples/example_convert_ivonne.py) can produce initial datasets
- TBD
