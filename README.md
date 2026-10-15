# U.S. Regional Innovation Explorer

Interactive Streamlit extension of the M1 HistPat county innovation assignment.

## What this adds
The analytical notebook establishes the results, and the A4 infographic communicates the main findings. This app adds a county-level exploration and decision-support layer without rerunning the full HistPat workflow.

The final product has only three analysis pages:

1. **County Innovation Explorer** — integrates county technology profile, observed vs out-of-fold predicted patent intensity, and A61 adoption history.
2. **Technology Landscape** — explores CPC 3-digit specialization using RSCA, LQ, and patent activity.
3. **A61 Diffusion Explorer** — explores diffusion by decade and thresholds 5/10/20 and compares adoption with spatial concentration.

## Step 1 — Export the notebook results

Open the completed assignment notebook and add the contents of:

`notebook_export_cell.py`

as the **last code cell after Part 4**. Run it after all Parts 1–4 have executed successfully.

It creates a folder named:

`streamlit_export/`

with these files:

- `county_master.csv`
- `county_specialization.csv`
- `a61_county_decade.csv`
- `a61_diffusion_summary.csv`
- `a61_moran_summary.csv`
- `model_metrics.csv`
- `model_importance.csv`
- `county_geometry.geojson`

Copy all eight files into this project's `data/` folder.

## Step 2 — Install dependencies

From a terminal opened inside this project folder:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Step 3 — Run the app

```bash
python -m streamlit run app.py
```

On Windows, after dependencies are installed, you can also double-click `run_windows.bat`.

## Interpretation boundaries

This application is designed for **regional screening and diagnosis**, not causal policy prescription.

- Part 1 cluster profiles are weakly separated broad portfolio summaries, not fixed regional technology types.
- Part 2 uses out-of-fold predictions for county exploration. A residual does not identify a causal mechanism.
- The assignment's official model evaluation remains the held-out test metrics in the notebook.
- A61 adoption thresholds describe patent participation; they do not measure commercial adoption.
- Moran's I measures spatial association, not causal diffusion between neighboring counties.

## Repository layout

```text
regional_innovation_explorer/
├── app.py
├── pages/
│   ├── 1_County_Innovation_Explorer.py
│   ├── 2_Technology_Landscape.py
│   └── 3_A61_Diffusion_Explorer.py
├── utils/
│   ├── data.py
│   ├── charts.py
│   └── ui.py
├── data/
│   └── [eight notebook exports go here]
├── .streamlit/
│   └── config.toml
├── notebook_export_cell.py
├── PROJECT_SCOPE.md
├── requirements.txt
└── README.md
```

## Interface redesign

The application uses a custom visual system rather than Streamlit's default dashboard styling:

- branded gradient hero and dark navigation sidebar
- custom KPI cards and status chips
- large evidence-first county maps
- visual county specialization rankings
- integrated observed-vs-predicted county profile
- interactive A61 diffusion and threshold-sensitivity graphics
- consistent methodological cautions without cluttering the main decision flow

The design deliberately keeps the analytical outputs unchanged. The redesign affects presentation and interaction only.
