import numpy as np
import pandas as pd
import streamlit as st

from utils.data import (
    load_county_master,
    load_a61_panel,
    load_diffusion_summary,
    load_moran_summary,
    load_model_metrics,
    load_model_importance,
    load_geojson,
    missing_files,
)

from utils.charts import (
    county_choropleth,
    diffusion_curve,
    predictor_importance_chart,
)

from utils.ui import (
    hero,
    metric_card,
    section_header,
    nav_card,
    process_rail,
    callout,
)


# ============================================================
# 1. CHECK REQUIRED DATA FILES
# ============================================================

missing = missing_files()

if missing:
    hero(
        "Interactive regional intelligence",
        "U.S. Regional Innovation Explorer",
        (
            "The application shell is ready. Add the validated "
            "notebook exports to activate the county-level "
            "intelligence layer."
        ),
        [
            "County specialization",
            "Predictive modelling",
            "Spatial diffusion",
        ],
    )

    st.warning(
        "The exported notebook data have not been copied "
        "into the `data/` folder yet."
    )

    st.code(
        "\n".join(missing),
        language="text",
    )

    st.stop()


# ============================================================
# 2. LOAD DATA
# ============================================================

master = load_county_master()
panel = load_a61_panel()
diffusion = load_diffusion_summary()
moran = load_moran_summary()
metrics = load_model_metrics()
importance = load_model_importance()
geojson = load_geojson()


# ============================================================
# 3. PREPARE OVERVIEW METRICS
# ============================================================

main_a61 = (
    diffusion[
        diffusion["threshold"] == 10
    ]
    .sort_values("decade_start")
)

latest_a61 = main_a61.iloc[-1]

latest_moran = (
    moran
    .sort_values("decade_start")
    .iloc[-1]
)

rf = (
    metrics[
        metrics["Model"] == "Random Forest"
    ]
    .iloc[0]
)


# ============================================================
# 4. HERO
# ============================================================

hero(
    "County-level decision support",
    "See where technology is entering — and where innovation runs deeper.",
    (
        "Explore U.S. county technological portfolios, compare observed "
        "patent intensity with model expectations, and trace the spatial "
        "diffusion of A61 from the 1950s to the 2000s."
    ),
    [
        "HistPat county evidence",
        "CPC 3-digit specialization",
        "5-fold OOF screening",
        "Queen-contiguity Moran's I",
    ],
)


# ============================================================
# 5. KPI CARDS
# ============================================================

cols = st.columns(
    4,
    gap="medium",
)

with cols[0]:
    metric_card(
        "Counties in master table",
        f"{len(master):,}",
        "◫",
        "Integrated county layer",
    )

with cols[1]:
    metric_card(
        "A61 ever-adopted share",
        f"{latest_a61['cumulative_share_pct']:.1f}%",
        "↗",
        "Main threshold: ≥10 patents",
    )

with cols[2]:
    metric_card(
        "A61 activity Moran's I",
        f"{latest_moran['activity_moran_I']:.3f}",
        "⌾",
        "2000s spatial concentration",
    )

with cols[3]:
    metric_card(
        "Random Forest test R²",
        f"{rf['R2']:.3f}",
        "◈",
        "Held-out county performance",
    )


# ============================================================
# 6. PROJECT IN ONE VIEW
# ============================================================

section_header(
    "01",
    "The project in one view",
    (
        "A national diffusion story on the left; "
        "the predictive signal structure on the right."
    ),
)

left, right = st.columns(
    [1.5, 1],
    gap="large",
)


# ------------------------------------------------------------
# LEFT — A61 MAP
# ------------------------------------------------------------

with left:

    latest_period = (
        panel[
            panel["decade_start"] == 2000
        ]
        .copy()
    )

    latest_period = (
        latest_period
        .merge(
            master[
                [
                    "FIPS",
                    "STNAME",
                    "CTYNAME",
                ]
            ],
            on="FIPS",
            how="left",
        )
    )

    latest_period["status"] = np.where(
        latest_period[
            "adopted_10"
        ].fillna(False),
        "Adopted",
        "Below threshold",
    )

    fig = county_choropleth(
        latest_period,
        geojson,
        "status",
        "A61 adoption footprint in 2000–2009",
        hover_cols=[
            "STNAME",
            "patents",
        ],
        discrete=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        },
    )


# ------------------------------------------------------------
# RIGHT — PREDICTOR IMPORTANCE
# ------------------------------------------------------------

with right:

    st.plotly_chart(
        predictor_importance_chart(
            importance
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        },
    )

    callout(
        (
            "<strong>Central finding.</strong> "
            "Technological participation spreads to more counties "
            "over time, while deeper inventive activity remains "
            "spatially concentrated. Entry into a technology should "
            "not automatically be read as an established innovation "
            "ecosystem."
        )
    )


# ============================================================
# 7. RESEARCH → REGIONAL INTELLIGENCE
# ============================================================

section_header(
    "02",
    "From research result to regional intelligence",
    (
        "The app connects the three analytical parts around "
        "decisions a regional agency can actually explore."
    ),
)

process_rail(
    [
        (
            "Detect",
            (
                "See where technologies appear and which "
                "counties are specialized."
            ),
        ),
        (
            "Diagnose",
            (
                "Compare portfolio breadth and regional "
                "predictive signals."
            ),
        ),
        (
            "Distinguish",
            (
                "Separate technology entry from deeper "
                "inventive intensity."
            ),
        ),
        (
            "Investigate",
            (
                "Identify counties that warrant closer "
                "regional assessment."
            ),
        ),
    ]
)


# ============================================================
# 8. NAVIGATION CARDS
# ============================================================

section_header(
    "03",
    "Choose your lens",
    (
        "Each explorer answers a different practical question "
        "without rerunning the full analytical pipeline."
    ),
)

nav_cols = st.columns(
    3,
    gap="large",
)


# ------------------------------------------------------------
# COUNTY EXPLORER
# ------------------------------------------------------------

with nav_cols[0]:

    nav_card(
        "📍",
        "County Innovation Explorer",
        (
            "Select a state and county, then combine its "
            "technology portfolio, observed-versus-expected "
            "patent intensity, and A61 diffusion history "
            "in one profile."
        ),
    )

    st.page_link(
        "pages/1_County_Innovation_Explorer.py",
        label="Open county explorer",
        icon=":material/arrow_forward:",
        width="stretch",
    )


# ------------------------------------------------------------
# TECHNOLOGY LANDSCAPE
# ------------------------------------------------------------

with nav_cols[1]:

    nav_card(
        "🧭",
        "Technology Landscape",
        (
            "Choose any CPC 3-digit technology and map county "
            "specialization, RSCA, LQ, or patent activity with "
            "evidence-aware county rankings."
        ),
    )

    st.page_link(
        "pages/2_Technology_Landscape.py",
        label="Open technology landscape",
        icon=":material/arrow_forward:",
        width="stretch",
    )


# ------------------------------------------------------------
# A61 DIFFUSION EXPLORER
# ------------------------------------------------------------

with nav_cols[2]:

    nav_card(
        "🌐",
        "A61 Diffusion Explorer",
        (
            "Move through six decades, change the adoption "
            "threshold, and see how geographic participation "
            "and spatial concentration evolve together."
        ),
    )

    st.page_link(
        "pages/3_A61_Diffusion_Explorer.py",
        label="Open diffusion explorer",
        icon=":material/arrow_forward:",
        width="stretch",
    )


# ============================================================
# 9. DIFFUSION OVERVIEW
# ============================================================

section_header(
    "04",
    "Diffusion at a glance",
    (
        "The empirical trajectory shows substantial expansion, "
        "but the observed period does not establish full saturation."
    ),
)

st.plotly_chart(
    diffusion_curve(
        diffusion
    ),
    use_container_width=True,
    config={
        "displayModeBar": False
    },
)


# ============================================================
# 10. INTERPRETATION BOUNDARY
# ============================================================

st.caption(
    (
        "Interpretation boundary: Random Forest results are predictive "
        "and Moran's I is descriptive of spatial association. "
        "The application supports screening and diagnosis, "
        "not causal policy prescriptions."
    )
)
