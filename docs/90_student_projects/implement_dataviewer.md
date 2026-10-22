# Design of a Multi-Node Dataviewer for Analyzing Recordings of the Shepherd-Testbed

## Keywords & Title

- dataviewer, analyzer, analytics
- interactive
- multi-node, cross-node, scalable
- advanced filtering for finding events & states, multi-dimensional relation between individual data streams
- GPIO, IV, Shepherd Testbed
- performant, responsive

### Title-Proposals

- Interactive Cross-Node Analysis of Heterogeneous Datasets: Design and Evaluation of a Viewer and Analyzer for the Shepherd Testbed
- Exploring Multi-Dimensional Relations in Distributed Wireless Networks: A Scalable Viewer and Analysis Tool for GPIO and IV Traces of the Shepherd Testbed

Note: the first title leaves lots of wiggle room and doesn't promise a finished viewer.

## Introduction & Motivation

Analyzing experiments in the domain of embedded wireless networks can be challenging and highly individual.
The main goal of the viewer is to provide a basic set of tooling.
It should support users to analyze their recorded data.
Getting a rough overview of the data is considered a central pillar of the viewer.
Having a quick look at the relevant information with a quick zoom on individual events can be very helpful to plan the next steps of an analysis.
A seconds pillar are the search-options, as large multi-hour recordings with i.e. 1 MSPS for GPIO can become challenging.
A user should be able to find points-of-interest and navigate to them quickly.

The Shepherd-Testbed produces voltage-, current and GPIO-traces that can be post-processed by the [shepherd-tools](https://github.com/nes-lab/shepherd-tools).
The tools serve as a documentation for the internal h5-structure for shepherd as well as a tool for creating, reading and modifying the recordings.
There is also some basic static plotting implemented based on matplotlib, but a fast and responsive data-viewer would be extremely helpful as recordings can span over several days and may include up to 30 - 100 shepherd-nodes.

The implementation would be preferably based on an existing software.

## Current Situation

Each `Shepherd Node` produces:

- IV-Samples (voltage & current) with 100 kHz and 18bit resolution each
  - alternatively a power-trace (= I * V combined) is stored, to save bandwidth
  - both types can be [resampled to 10'000, 1000, 100 or 10 Hz](https://github.com/nes-lab/shepherd-tools/blob/1ed11034a68852dcade02443cf453fe95488ad3f/shepherd_core/shepherd_core/data_models/experiment/observer_features.py#L68) to save bandwidth
- event based gpio-sampling of 16 pins with [< 2 MHz sample-rate](https://github.com/nes-lab/shepherd-nova/blob/main/docs/content/infrastructure.md?plain=1#L86)
- on demand UART logging with up to 460 kBaud
- diverse logs of service like PTP, the kernel and system statistics

### State of the Art

The data-tool allows to plot parts of the ivsample-recording ⇾ [CLI-Interface ⇾ Plot IVSamples](https://github.com/nes-lab/shepherd-tools#cli-interface>). Multiplots for several recordings are supported, as well as prior downsampling.

There is a basic implementation of a [viewer based on DPG](https://github.com/orgua/shepherd-v2-planning/blob/main/scratch/shepherd_dataview/viewer.py>). It is limited to one recording, only IVSamples and is not optimized at all. So recordings >60s are challenging because there is no downsampling depending on the zoom-levels.

The Saleae Logic tool has an [open api](https://support.saleae.com/extensions/api-documentation) and (open?) file format, but does only support GPIO- and voltage-traces. Shepherd features also current-traces or derived power-traces.
The software is a defacto standard for ease of use and minimal design.
It is fast, responsive and allows filtering and has protocol-decoders included.

Tests with timeseries-databases were done. TimescaleDB and InfluxDB are both too slow to handle the live data of 30 nodes of the testbed. So currently the database-idea was put on hold for a pure file-based approach. But the viewer is not live, so it could be a viable option. Beside that
sqlite is file-based and really fast.

## Goals

From high to lower priority:

- have an interactive viewer for iv-sample-data as plotted timeseries
- viewer for GPIO as a plotted timeseries (each GPIO separately)
- multi node support - allows to load a whole directory (not recursive) of recordings
  - plots can be stacked, so multiple plots show up in one plot with different colors
  - synchronized timestamp can be used to align different nodes in one plot
  - naming could either be derived from embedded hostname or from filename
- calculate & show power-trace (as voltage and current on its own are sometimes less helpful)
- never hide events! To keep performance high the data might need to be resampled or filtered. It's easy to mess that up, so that nanosecond events disappear on lower zoom levels
- on-demand filtering & search options (more on that below)
- on-demand configuration options. Mentions below mostly reduce visual and computational overhead. A live-update after changing config would
  - allow to (de)select individual nodes
  - allow to (de)select Voltage, Current, Power viewer
  - allow to (de)select individual GPIO
  - (optional) allow to ignore absolute timestamp (for aligning plots) and use start of measurement as reference to allow comparing different experiments
- a standalone viewer-program would be desired (but can be the wrapped web-viewer)
- (optional) a web-viewer would be helpful for the testbed itself
- (optional) saving/loading of configuration (including filter-settings)
- (optional) preferably written in python (like all other high-level shepherd-tools) - but performance is a potential problem
- allow to overlay several recordings or plot them in individual graphs (no overlay but in series) with the same timebase (both has advantages)
- (optional) decoding digital protocols like UART (text) and SPI (numerical, hex) or offer a plugin-interface for that
- (optional) show marks where testbed did not run as expected
  - it either threw an error
  - sync was higher than i.e. 1 us
  - cpu-util was higher than i.e. 90 %
- (optional) visualize debug information embedded in files (CPU-util, network-traffic, PRU-util)
- search / highlight points of interest ⇾ tbd

Side-notes:

- these goals can be interpreted as requirements or wishlist. The actual spec is TBD and open for discussion.
- data-conversion is OK ⇾ probably a more performant format and a chain of downsamples are needed to handle the performance on large overviews
- in terms of usability and functionality the tool [Saleae Logic](https://www.saleae.com/downloads/) is regarded as a role model

## Filter & Search

Filtering in the viewer-context means marking events in the dataset based on individual datastreams and their states that are put into relation.

Example 1:
A user wants to look at all events where a node transmitted something (and other nodes maybe received it).
So one approach would be to look at the current-draw or power-usage of the nodes and search for individual events where a certain threshold was crossed for a specific amount of time.

Example 2:
A user with the same setup uses individual GPIO-lines for the different states of the nodes.
So actively transmitting data might be signaled with a high period of gpio0, active receive window is shown on gpio1 and a successful packet-reception is visible on the gpio2-channel. To make matters worse:
To debug wireless protocols one might look for a list where one node transmitted data (gpio0) and at least one other node received the data (gpio2).
But to make the situation more complex - the gpio-states might not be signaled at the same time, just close together.
RF-Transceivers might first decode the data and do checksum-tests before informing the program about a new package.
So transmission is already over before gpio2 rises to signal a successful reception.

Example 3:
A RF-protocol wants to span a mesh-network in a power-constrained environment, so nodes have to sleep a lot to preserve energy.
An algorithm has to determine when to listen for packets and when to send data to increase the chance of a rendezvous.
The researcher wants to see successful rendezvous with at least 2, 3, or more nodes sharing data.
But slightly misses in the meeting-window might tell more about actual flaws of the algorithm.

For a more formal description:

- filters should work on all possible inputs: voltage, current, power, individual GPIO, (..?)
- filters should work on states or individual events of these inputs
  - states have usually a specific timeframe (i.e. gpio0 is high/low, voltage is below/above 3 V)
  - events have a specific timestamp (i.e. rising/falling of gpio1, power-draw rising/falling & crossing a threshold)
- (optional) chaining of filters
- (optional) filters itself should have a time-component (i.e. high-state was at least 100 us, at most 1 ms )
- (optional) filter-chains have a time-component (i.e. filter2 less than 1 ms after filter1)
- (optional) for decoders, the system could filter on individual words

Having that event-collection in a list or table and be able to quickly navigate to the events would help a lot.
The table was mentioned because some statistics could be included in that even-log.
First of course is knowing the number of events found.
Second some basic statistics of the event itself would help:

- duration of the timeframe
- energy usage (accumulated power usage over duration)
- included node-count

Such statistic could also be show when a user selects a timeframe by setting start- & stop-markers.
That's purely optional.

## Main Challenges

There are two major challenges to evaluate (or solve) in this thesis

- How to handle multiple large datasets without needing a super-computer (1 hour of recording with 100 kHz and also GPIO-Input for 20+ Nodes can be become really large)
- How to filter through the datasets

To be clear: The polished viewer may/is not be the product of this thesis! Research takes time and evaluating the options is often the main task and timekiller. Writing the viewer is an engineering- or programming-task. Evaluating the options, finding metrics for comparison, measuring them are important steps before and a major part of the written thesis. It can also stand on its own when the prototype is able to do the basics and show the concept.

## Milestones / Steps

TBD, proposal:

- read into the topic
- draft a 1-2 page proposal (can be changed later)
- set up draft of requirements (that serve as a realistic goal for the thesis)
- capture the state of the art
  - prepare an overview of options & looking at publications
  - can be papers, available frameworks, similar of-the-shelf products
- experiment with rough prototypes
- (optional) midterm presentation for collecting feedback from the research-team
- decision how to proceed / what to choose
- redefine requirements and possible features
- focus on working version
- in between: document design-decisions and other information that helps writing the thesis

## Existing Software & Useful links

`FlockLab` - a similar Testbed [implemented plotting](https://github.com/ETHZ-TEC/FlockLab-Tools) with [Bokeh](https://bokeh.org/) both for web and offline usage.

An alternative to Bokeh could be [plotly](https://github.com/plotly/plotly.py).
source: <https://pauliacomi.com/2020/06/07/plotly-v-bokeh.html>

For bundling and filtering plots in an overview-page:

- <https://awesome-panel.org/> ⇾ the video <https://www.youtube.com/watch?v=0DBEXiMdSKc&t=530s> talks about Terabytes of data visualized with datashader, rapids cuxFilter ⇾ problem: GPU / CUDA based
- Alternative: [Streamlit](https://streamlit.io)

More Info on current GPIO-Pins routed to the targets:

- [General Info](https://nes-lab.github.io/shepherd/dev/v2_improvements.html#pins-to-target)
- [Bit Position Info included in H5-File](https://github.com/nes-lab/shepherd/blob/main/software/python-package/shepherd/commons.py#L38)

Trafficbench uses <https://glueviz.org/> and Glue to visualize data and multi-dimensional filtering. Performance might be a bottleneck.

Existing tools like sigrok & pulseview look promising.
Pulseview seems to support several input-formats, so a converter should suffice.
But maybe it is also possible to extend Pulseview to support the shepherd-hdf5-format directly.

## Test-Data

- the [tool-examples](https://github.com/nes-lab/shepherd-tools/blob/main/shepherd_data/examples/example_convert_ivonne.py) can produce initial datasets
- Carsten agreed to provide firmware for the testbed to create actual protocol-data
- TBD
