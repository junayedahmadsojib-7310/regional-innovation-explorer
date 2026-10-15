import numpy as np
import streamlit as st

from utils.data import (
    load_county_master,
    load_a61_panel,
    load_diffusion_summary,
    load_moran_summary,
    load_geojson,
)
from utils.charts import county_choropleth, diffusion_curve, moran_chart, threshold_sensitivity_chart
from utils.ui import page_header, section_header, metric_card, callout, method_note


page_header(
    "Spatial diffusion through time",
    "A61 Diffusion Explorer",
    "Move across six decades, change the adoption threshold, and compare geographic participation with the spatial concentration of deeper inventive activity.",
)

master = load_county_master()
panel = load_a61_panel()
diffusion = load_diffusion_summary()
moran = load_moran_summary()
geojson = load_geojson()

with st.container(border=True):
    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        decade = st.select_slider(
            "Decade",
            options=sorted(panel["decade_start"].astype(int).unique()),
            value=int(panel["decade_start"].max()),
            format_func=lambda x: f"{x}s",
        )
    with c2:
        threshold = st.radio("Adoption threshold", [5, 10, 20], index=1, horizontal=True, format_func=lambda x: f"≥{x}")
    with c3:
        view = st.radio("Map view", ["Adoption status", "Patent activity"], horizontal=True)

period = panel[panel["decade_start"] == decade].copy()
period = period.merge(master[["FIPS", "STNAME", "CTYNAME"]], on="FIPS", how="left")

section_header("01", f"A61 in the {decade}s", "The map responds to decade, threshold and whether you want to see presence or inventive intensity.")
if view == "Adoption status":
    adopted_col = f"adopted_{threshold}"
    period["status"] = np.where(period[adopted_col].fillna(False), "Adopted", "Below threshold")
    fig = county_choropleth(
        period,
        geojson,
        "status",
        f"A61 adoption status, {decade}–{decade + 9} (≥{threshold} patents)",
        hover_cols=["STNAME", "patents"],
        discrete=True,
    )
else:
    period["log_patent_activity"] = np.log1p(period["patents"])
    fig = county_choropleth(
        period,
        geojson,
        "log_patent_activity",
        f"A61 patent activity, {decade}–{decade + 9}",
        hover_cols=["STNAME", "patents"],
    )

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

summary_row = diffusion[(diffusion["threshold"] == threshold) & (diffusion["decade_start"] == decade)].iloc[0]
moran_row = moran[moran["decade_start"] == decade].iloc[0]

mcols = st.columns(4, gap="medium")
with mcols[0]:
    metric_card("Period adopters", f"{int(summary_row['period_adopters']):,}", "●", f"Counties meeting ≥{threshold}")
with mcols[1]:
    metric_card("Cumulative adopters", f"{int(summary_row['cumulative_adopters']):,}", "↗", "Ever crossed by this decade")
with mcols[2]:
    metric_card("Cumulative share", f"{summary_row['cumulative_share_pct']:.1f}%", "◫", "Share of county universe")
with mcols[3]:
    metric_card(
        "Binary Moran's I",
        f"{moran_row['binary_moran_I']:.3f}" if threshold == 10 else "N/A",
        "⌾",
        "Calculated for main ≥10 threshold" if threshold == 10 else "Main threshold only",
    )

callout(
    f"<strong>Inventive-depth signal:</strong> activity-intensity Moran's I in the {decade}s is <strong>{moran_row['activity_moran_I']:.3f}</strong>. Compare this with the adoption map to distinguish geographic spread from concentration of deeper patent activity."
)

section_header("02", "How did diffusion and concentration evolve?", "The cumulative adoption trajectory and Moran's I answer related but different questions.")
c1, c2 = st.columns(2, gap="large")
with c1:
    st.plotly_chart(diffusion_curve(diffusion), use_container_width=True, config={"displayModeBar": False})
with c2:
    st.plotly_chart(moran_chart(moran), use_container_width=True, config={"displayModeBar": False})

section_header("03", "Is the story sensitive to the adoption threshold?", "The 5, 10 and 20 patent thresholds change counts, but let you assess whether the qualitative diffusion pattern is robust.")
st.plotly_chart(threshold_sensitivity_chart(diffusion), use_container_width=True, config={"displayModeBar": False})

with st.expander("Show threshold sensitivity table"):
    pivot = diffusion.pivot(index="decade_start", columns="threshold", values="cumulative_adopters").reset_index()
    pivot.columns = ["Decade"] + [f"≥{int(c)}" for c in pivot.columns[1:]]
    st.dataframe(pivot, use_container_width=True, hide_index=True)

method_note(
    "Adoption is defined as reaching a patent-count threshold within a 10-year period. The assignment's main threshold is ≥10 patents; ≥5 and ≥20 provide sensitivity checks. Moran's I summarizes global spatial association, not causal diffusion from one county to its neighbors. The activity-intensity Moran measure uses log(1 + patent count)."
)
