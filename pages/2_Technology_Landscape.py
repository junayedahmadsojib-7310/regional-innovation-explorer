import pandas as pd
import streamlit as st

from utils.data import load_county_master, load_specialization, load_geojson
from utils.charts import county_choropleth, ranking_bar, portfolio_donut
from utils.ui import page_header, section_header, metric_card, callout, method_note


page_header(
    "Technology specialization explorer",
    "Technology Landscape",
    "Choose a CPC 3-digit field and see where relative specialization, patent activity and broader county portfolio context are concentrated.",
)

master = load_county_master()
spec = load_specialization()
geojson = load_geojson()

with st.container(border=True):
    c1, c2, c3 = st.columns([1.05, 1.25, .8], gap="large")
    techs = sorted(spec["CPC_3digit"].dropna().unique())
    with c1:
        tech = st.selectbox("CPC 3-digit technology", techs, index=techs.index("A61") if "A61" in techs else 0)
    with c2:
        metric_label = st.radio(
            "Map measure",
            ["RSCA", "Location Quotient (LQ)", "Fractional patents"],
            horizontal=True,
        )
    with c3:
        min_evidence = st.toggle("Require ≥5 patents for ranking", value=True)

metric_map = {
    "RSCA": "RSCA",
    "Location Quotient (LQ)": "LQ",
    "Fractional patents": "fractional_patents",
}
metric = metric_map[metric_label]

tech_rows = spec[spec["CPC_3digit"] == tech].copy()
base = master[["FIPS", "STNAME", "CTYNAME", "part1_profile_available"]].copy()
map_df = base.merge(
    tech_rows[["FIPS", "fractional_patents", "LQ", "RSCA", "min_evidence_5"]],
    on="FIPS",
    how="left",
)

if metric == "RSCA":
    mask = map_df["part1_profile_available"].fillna(False) & map_df["RSCA"].isna()
    map_df.loc[mask, "RSCA"] = -1.0
elif metric == "LQ":
    mask = map_df["part1_profile_available"].fillna(False) & map_df["LQ"].isna()
    map_df.loc[mask, "LQ"] = 0.0
else:
    map_df["fractional_patents"] = map_df["fractional_patents"].fillna(0.0)

section_header("01", f"Where is {tech} concentrated?", "The map changes with the selected measure; rankings retain the original numeric values.")
fig = county_choropleth(
    map_df,
    geojson,
    metric,
    f"{tech}: county {metric_label}",
    hover_cols=["STNAME", metric],
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

kpis = st.columns(3, gap="medium")
with kpis[0]:
    metric_card("Counties with activity", f"{tech_rows['FIPS'].nunique():,}", "●", f"Observed {tech} patent activity")
with kpis[1]:
    metric_card("Counties with RSCA > 0", f"{(tech_rows['RSCA'] > 0).sum():,}", "↗", "Above national relative share")
with kpis[2]:
    metric_card("Counties with ≥5 patents", f"{(tech_rows['fractional_patents'] >= 5).sum():,}", "✓", "Stronger evidence base")

section_header("02", "Which counties lead under this measure?", "A visual ranking first; the detailed table remains available for inspection.")
rank = tech_rows.copy()
if min_evidence:
    rank = rank[rank["fractional_patents"] >= 5]
rank = rank.sort_values(metric, ascending=False).head(20)

left, right = st.columns([1.35, .65], gap="large")
with left:
    st.plotly_chart(ranking_bar(rank, metric, metric_label), use_container_width=True, config={"displayModeBar": False})
with right:
    callout(
        "<strong>How to read this.</strong><br><br>RSCA and LQ describe relative specialization, while fractional patents describe activity volume. A county can rank highly on specialization without being a large patenting centre."
    )
    with st.expander("Show top-county table"):
        cols = ["CTYNAME", "STNAME", "fractional_patents", "LQ", "RSCA"]
        rank_table = rank[[c for c in cols if c in rank.columns]]
        st.dataframe(
            rank_table.rename(columns={
                "CTYNAME": "County",
                "STNAME": "State",
                "fractional_patents": "Fractional patents",
            }).style.format({"Fractional patents": "{:.2f}", "LQ": "{:.2f}", "RSCA": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

section_header("03", "Portfolio context", "The broad two-profile clustering is retained as context, not as the main technology classification.")
left, right = st.columns([.8, 1.2], gap="large")
with left:
    st.plotly_chart(portfolio_donut(master), use_container_width=True, config={"displayModeBar": False})
with right:
    portfolio = master[master["part1_profile_available"] == True].copy()
    if not portfolio.empty:
        summary = portfolio.groupby("cluster_profile").agg(
            counties=("FIPS", "size"),
            median_patents=("county_total", "median"),
            median_breadth=("tech_breadth", "median"),
            median_diversification=("diversification_entropy", "median"),
        ).reset_index()
        st.dataframe(summary, use_container_width=True, hide_index=True)
        callout("The low silhouette score means these are broad portfolio patterns rather than clean technology archetypes. County-specific CPC evidence should carry more interpretive weight.")

method_note(
    "LQ > 1 indicates a county share of the selected CPC above the national technology share; RSCA symmetrizes LQ to approximately [-1, 1]. Rankings can be unstable when patent counts are tiny, so the app offers a minimum-evidence filter. Missing CPC activity is shown as RSCA = -1 / LQ = 0 only for counties in the Part 1 specialization sample."
)
