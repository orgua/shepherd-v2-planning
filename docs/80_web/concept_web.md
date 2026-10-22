# Concept for Web Interface

## MetaInfo

- derived from requirements, concept_shepherd and concept_meeting_notes

## Design-Features

- Privacy is a features - avoid personal data (OAuth, ActiveDirectory)
- usage per website & API
- 1 experiment at a time, no concurrency

## Functions

- user-management
  - permission
  - role management
  - groups (share datapool)
  - Quota (data is linked to user and deleted with the account)
- authentication via external service like OAuth (i.e. GitHub) (if possible)
- Upload user provided data
  - Harvesting- / Energy-Traces, -traces, IV-Curves
  - regulator / converter-definition
  - Target-Firmware
  - user-scripts (sandboxed, limited resources (cpu, ram, storage), only limited libs allowed, limited user, lowest nice-level)
- Scratch-Area for experimentation-results (or DB)
- integrated pre-tests for measurement: test for plausibility, pre-run in software (abstract virtual hardware)
  - link in python code of shepherd project
- scheduler for measurement, time to prepare and follow up (data transfer, conversion, compression, ...)
- results downloadable by user, for a certain time (no hording)
- feedback via e-mail - measurement start, data available, error, shortly before deletion
- (optional) grafana-visualization
- documentation and instructions
  - landing page
  - "what is that thing in my office"
    - clarify use and capability of the boxes (so people sharing an office with the testbed don't freak out)
  - where find what
  - FAQ
- Testbed-Status
  - structure
  - last seen
  - handle lockups (power-cycle)
  - keep testbed alive for a limited time (otherwise it will go to sleep / power down)
- collecting of logs (temp, ram-usage, cpu-usage, time-sync, ...)
- Web-Framework (some points are redundant)
  - user-management (roles for admins and users)
  - experiment-management, configure and control, add data (see below)
  - experiment-scheduling, calender (set active, start-time, duration)
  - data management / quota (retrieve / delete recordings)
  - authentication via external services
  - E-Mail notifications
  - testbed status, topology
  - (optional) grafana visualization of recorded data
  - (admins) server status, quota, testbed control
  - documentation and instructions
  - target-management (specify slots of nodes)
  - (optional) benchmark-management (post-scripts)
- live-view ⇾ lower prio

## Implementation

- possibly python based (django vs flask, big vs small)
  - django offers the most, is flexible, modular and easy to extend
    - admin-interface
    - authentication (also oauth client), accounts
    - session-management
    - sub-websites with html-templates
    - ⇾ security seems to be OK, attach surface is big, but >v3.0 seems to be mature
  - flask is a microframework, offers minimal attack surface and seems perfect for the python REST API
- basic implementation could be similar to <https://github.com/fkt/36c3-junior-ctf-pub> (web-interface for a ctf, that didn't get compromised)
- API: rest
- (prio) allow scripted workflow ⇾ yaml ⇾ rest ⇾ server internals
  - this could also be the base for the web-page-interface
- Database
  - influxDB or
  - timescaleDB
  - postgreSQL
- MessageSystem
  - Protobuf
  - RabbitMQ
  - RPC
- visualization, analysis ⇾ dash?
- option to sample down

## DB Decision

- needed:
  - 30x 100k Inserts of timestamp (8B), node_id (1B), voltage (4B), current (4B)
  - ⇾ 3M Inserts of >=17 Bytes ⇾ 3 GB / minute
  - can happen locally or remote, concurrently is fine
- main bottleneck:
  - databases with timeseries do not seem to have a low level api for insertions, interface is ascii and needs parsing
  - (solution) low level api (raw data, shared mem, ...) ⇾ there are possible formats like::
    - BSON ⇾ MongoDB
    - UBJSON ⇾ TeradataDB, Wolfram (no use for us)
    - apache avro ⇾ Apache Spark SQL
    - JSONB ⇾ Postgresql, but they say: "JSON is faster to ingest vs. JSONB"
- Timescale DB vs Influx ⇾ influx seems to dominate with fewer devices <= 100
- timescale: SQL, robust, based on postgreSQL, time series, relational, various datatypes
  - looks more professional, but like influx they want to sell
  - presetup hard to script
  - 1M insert/s are considered excellent, i landed at ~60k with one remote connection
  - no low level api available, but some SQLs allow to load from file (csv)
- influxDB2:
  - inserting 200s data takes ~ 190s (1 node), with almost no load on VM or system
    - ⇾ makes 108k/s inserts from one node
    - marketing documents say the insert-rate of free-database is good for ~ 250k/s
    - is it artificially limited or is it another invisible bottleneck?
  - ram usage seems to be ok << 1 GB
  - query's with ns resolution can get very slow. ~3s for averaging windows
  - influx can almost naturally import hdf5, numpy-arrays, pandas Dataframes
  - dataexplorer shows plots only windowed, smallest window is 1s (may be unimportant)
- elastic + logstash, search engine,
- redis, key-value store
- mongoDB
  - allows usage of BSON instead of JSON

## DB-Bypass

- measurement-data could be stored directly on the server
- each measurement is stored in a separate folder, named by hash or timestamp
  - it contains config data, logs and results
- file-references are inserted into a DB
- metrics for benchmarks or competitions could be generated by a user-script
  - pandas or numpy, as a fast cPython convenience, allows powerful oneliners
  - these metrics could be displayed on the website as a condensed result
  - these metrics could also be used for some kind of leaderboard
- a downsampled dataset (1 kHz?) could be fed into a database for semi-live analysis / observation
- a full-res dataset could be fed into the database afterward but would mean a longer blocking time between measurements

## TODO

- try paid db-vm (influx)
- compare elastic against influx, no support for nanosec?
- benchmark server (disks / ram)
- offer predefined energy-patterns (on/off, diode, different converters (boost, buck/boost))
- design-choices for later
  - does shepherd need databases for immediate (deep)analysis of result
    - alternative: provide post-scripts that filter data for key-parameters (benchmark-management)
  - data hording or economical use of space?
  - what else ?????
