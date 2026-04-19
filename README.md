# el-phase-2-data-and-dataprocessing
### GPS Data Collection & Processing Pipeline for AlgoTransit

> Raw BMTC bus GPS data collection, cleaning, and preprocessing scripts that feed into the [AlgoTransit](https://github.com/k-karthik-pai/AlgoTransit) optimization engine.

---

## Overview

This repository handles **Phase 1** of the AlgoTransit pipeline — taking raw GPS location logs from BMTC buses and converting them into clean velocity profiles ready for swarm intelligence optimization.

Raw GPS data is noisy. Bus stops, signal halts, and logging gaps create spikes and gaps in speed profiles that would confuse the optimization algorithm if fed directly. This repo solves that.

---

## Repository Structure

```
el-phase-2-data-and-dataprocessing/
│
├── BMTC_1/             # Raw + processed data for BMTC route dataset 1
├── BMTC_2/             # Raw + processed data for BMTC route dataset 2
│
├── Bus_Project_1/      # Processing scripts for bus trip set 1
├── Bus_Project_2/      # Processing scripts for bus trip set 2
├── Bus_Project_3/      # Processing scripts for bus trip set 3
├── Bus_Project_4/      # Processing scripts for bus trip set 4
├── Bus_Project_5/      # Processing scripts for bus trip set 5
│
└── LocationRecords/    # Raw GPS logs (Latitude, Longitude, Timestamp)
```

---

## The Processing Pipeline

```
LocationRecords/
[Raw GPS: Lat, Lon, Timestamp]
        ↓
  Geodesic Distance Calculation
  [geopy.distance — converts coordinate pairs to metres]
        ↓
  Speed Derivation
  [speed (m/s) = distance / time_delta]
        ↓
  Noise Filtering
  [Remove outlier spikes, smooth with rolling window]
        ↓
  Cleaned Velocity Profile (CSV)
  [Ready for MMAS-ABC optimization in AlgoTransit]
```

---

## Data Description

**BMTC_1 / BMTC_2** — Real-world GPS traces collected from BMTC bus routes in Bengaluru. Each record contains latitude, longitude, and timestamp at regular intervals.

**Bus_Project_1 through 5** — Processed subsets corresponding to individual trip segments. Each folder contains the cleaned output CSV and the Python script used to generate it.

**LocationRecords** — The raw source data before any processing.

---

## Tech Stack

- **Python 3.9**
- `pandas` — data loading, cleaning, and export
- `numpy` — numerical operations and smoothing
- `geopy` — geodesic distance calculations from GPS coordinates
- `matplotlib` — optional visualization of raw vs cleaned profiles

---

## Getting Started

**Install dependencies**
```bash
pip install pandas numpy geopy matplotlib
```

**Run a processing script**
```bash
cd Bus_Project_1/
python process.py
```

The cleaned CSV output will be saved in the same folder and can be passed directly to the AlgoTransit algorithm.

---

## Output Format

Each processed CSV contains:

| Column | Description |
|---|---|
| `timestamp` | Original GPS timestamp |
| `speed_mps` | Derived speed in metres per second |
| `distance_m` | Cumulative distance in metres |
| `smoothed_speed` | Noise-filtered speed profile |

---

## Related Repository

The optimization algorithm that consumes this data:
[AlgoTransit — Hybrid MMAS-ABC Optimizer](https://github.com/k-karthik-pai/AlgoTransit)

---

## Context

Developed as part of **Experiential Learning (EL) Phase 2** at RV College of Engineering, Bengaluru — Urban Development, Mobility & Smart Cities track (Project #49).
