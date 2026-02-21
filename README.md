# GeOceanographers

**Team Members:** Mary Orrand, Colin, Ellie Barkyoumb, Arya

This repository contains all coursework for the **MLGEO-2026** class (Machine Learning in the Geosciences, Winter 2026) at the University of Washington Department of Earth and Space Sciences.

---

## Repository Structure

```
Geoceanographers/
├── README.md              ← You are here
├── Stehekin/              ← Assignment: API-based debris flow analysis
│   ├── README.md
│   ├── API_class.ipynb
│   └── StehekinRiver.ipynb
└── TeamProject/           ← Team project: Ocean carbon cycle ML modeling
    ├── README.md
    └── GeOceanProject/    ← Project code, data, notebooks, and plots
        ├── README.md
        ├── requirements.txt
        ├── notebooks/
        ├── data/           ← Includes DATA_ANALYSIS_WORKFLOW.md
        ├── plots/
        └── docs/
```

## Contents

### [Stehekin/](Stehekin/) — Atmospheric River & Debris Flow Analysis

Class assignment using weather and hydrology APIs to characterize the December 2025 atmospheric river event and resulting debris flows on fire-burned slopes in Stehekin, WA. Uses USDA SNOTEL and NWS API data.

→ See [Stehekin/README.md](Stehekin/README.md) for full details.

### [TeamProject/](TeamProject/) — Ocean Carbon Cycle ML Modeling

Team project applying machine learning to predict ocean pCO2 from satellite and buoy observations. Combines NOAA satellite SST data (JPL MUR, ~4.6 km resolution) with buoy-measured water chemistry from 7 coastal monitoring sites spanning 2013–2025.

→ See [TeamProject/README.md](TeamProject/README.md) for project overview and navigation.
→ See [TeamProject/GeOceanProject/README.md](TeamProject/GeOceanProject/README.md) for the full data pipeline and technical documentation.
→ See [TeamProject/GeOceanProject/data/DATA_ANALYSIS_WORKFLOW.md](TeamProject/GeOceanProject/data/DATA_ANALYSIS_WORKFLOW.md) for a detailed processing walkthrough.

---

## Getting Started

1. Clone this repository
2. Navigate to the relevant folder (`Stehekin/` or `TeamProject/`)
3. Follow the README in each folder for setup instructions and notebook run order

## Course Information

- **Course:** MLGEO-2026 — Machine Learning in the Geosciences
- **Quarter:** Winter 2026
- **Institution:** University of Washington, Dept. of Earth and Space Sciences
