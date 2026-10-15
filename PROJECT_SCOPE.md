# Final Streamlit scope

## Product
**U.S. Regional Innovation Explorer — From technological entry to innovation depth**

## Audience
U.S. state and regional economic-development agencies responsible for innovation and technology-based growth.

## Why the extension exists
The notebook answers the analytical questions. The one-page infographic communicates the main conclusions. The Streamlit extension lets a decision-maker explore the validated findings for a specific county, technology, decade, and adoption threshold.

## Three pages only
1. **County Innovation Explorer** — flagship page integrating Parts 1–3 for one county.
2. **Technology Landscape** — interactive CPC specialization map/ranking using LQ, RSCA, and patent activity.
3. **A61 Diffusion Explorer** — interactive decade/threshold maps plus diffusion and Moran diagnostics.

## Guardrails
- No causal policy simulator.
- No live retraining in Streamlit.
- No recreation of the full HistPat pipeline inside the app.
- Cluster labels are broad exploratory profiles, not rigid regional technology types.
- Out-of-fold county predictions are screening diagnostics, not causal effects.
- Moran's I measures spatial association, not neighbor-to-neighbor causality.

## Central user question
**Where is technological capability emerging, where is it deepening, and where are established inventive ecosystems already concentrated?**
