# U.S. Regional Innovation Explorer

An interactive Streamlit extension of the M1 HistPat county innovation assignment.

## Project extension

As an extension to the required assignment, and to reflect the additional scope of a five-member group, we developed an interactive decision-support application for U.S. state and regional economic-development agencies.

The analytical notebook remains the core assignment. The Streamlit application operationalizes the validated outputs from Parts 1–3, allowing the results to be explored interactively at county level without changing the underlying analysis.

## Live application

**Streamlit application:**  
https://regional-innovation-explorer.streamlit.app/

**Assignment notebook / repository:**  
https://colab.research.google.com/drive/1SP00WP6rGvZXF1-yEbo4lHPMR-RXLmmQ?usp=sharing

---

## Purpose

The notebook answers the analytical research questions, while the A4 infographic communicates the main conclusions.

The Streamlit extension adds a third layer:

> **interactive regional exploration and decision support.**

It allows a user to investigate how technological specialization, regional innovation characteristics, and technology diffusion come together for individual U.S. counties.

The central question is:

> **Where is technological capability emerging, where is it deepening, and where are established innovation ecosystems concentrated?**

---

## Application

The application contains three analytical explorers.

### 1. County Innovation Explorer

Select a state and county to view an integrated regional innovation profile combining:

- technological portfolio and specialization;
- technology breadth and diversification;
- observed patent intensity;
- five-fold out-of-fold predicted patent intensity;
- observed-versus-predicted model residual;
- regional predictor values;
- A61 adoption history and first threshold crossing.

This page integrates the main outputs from Parts 1–3 around a single county.

### 2. Technology Landscape

Explore county technological specialization for CPC 3-digit technologies using:

- Revealed Symmetric Comparative Advantage (RSCA);
- Location Quotient (LQ);
- fractional patent activity;
- county rankings;
- technology breadth and portfolio context.

The cluster solution is presented only as an exploratory summary because the final clusters are weakly separated.

### 3. A61 Diffusion Explorer

Explore the geographic diffusion of **A61 — Medical or Veterinary Science; Hygiene** through:

- six consecutive decades from 1950–1959 to 2000–2009;
- adoption thresholds of 5, 10, or 20 patents;
- interactive county adoption maps;
- period and cumulative adoption;
- diffusion trajectories;
- binary-adoption Moran's I;
- patent-intensity Moran's I.

This allows users to distinguish geographic technology entry from deeper inventive concentration.

---

## Key analytical findings

The application is built from the validated assignment results.

- County technological profiles can be summarized into broader/higher-activity and narrower/lower-activity groups, although cluster separation is weak and the groups should not be interpreted as fixed technological types.
- Random Forest provides the strongest predictive performance among the evaluated models, with educational attainment providing the strongest predictive signal among the three included regional variables.
- A61 participation expanded substantially across U.S. counties between the 1950s and 2000s.
- By 2000–2009, **778 counties (25.1%)** had ever crossed the main ≥10-patent adoption threshold.
- Geographic participation spread more widely, while high-intensity inventive activity remained spatially concentrated.
- In the 2000s, Moran's I was approximately **0.381 for binary adoption** and **0.567 for patent intensity**.

These results motivate the distinction between **technology entry** and **sustained innovation depth**.

---

## Intended audience

The application is designed for:

**U.S. state and regional economic-development agencies responsible for innovation and technology-based growth.**

It is intended as a **screening and diagnostic tool**, helping users identify places that may warrant deeper investigation.

It is not designed to prescribe causal policy interventions.

---

## Interpretation boundaries

The following limitations from the analytical notebook also apply to the application:

- Part 1 cluster profiles are broad exploratory summaries, not fixed regional technology types.
- Part 2 is predictive rather than causal.
- Out-of-fold county predictions are used for interactive screening; they do not identify causal mechanisms.
- The official model evaluation remains the held-out test performance reported in the notebook.
- A61 patent thresholds measure patent participation, not commercial technology adoption.
- Moran's I measures spatial association and does not demonstrate causal diffusion between neighboring counties.
- The latest period in the historical diffusion analysis is 2000–2009 and should not be interpreted as the present-day state of A61.

---

## Data-product architecture

The Streamlit application does not rerun the full HistPat analytical pipeline.

Instead, the completed notebook exports validated application-ready datasets:

```text
Analytical data
      ↓
Final assignment notebook
      ↓
Validated analytical outputs
      ↓
CSV / GeoJSON export layer
      ↓
Streamlit application
