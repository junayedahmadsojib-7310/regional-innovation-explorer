import pandas as pd
import streamlit as st

from utils.data import (
    load_county_master,
    load_specialization,
    load_a61_panel,
    format_num,
    format_pct,
)
from utils.charts import observed_vs_predicted_chart, county_a61_timeline, specialization_bar
from utils.ui import page_header, section_header, metric_card, status_chips, callout, method_note


page_header(
    "Integrated county intelligence",
    "County Innovation Explorer",
    "Bring Parts 1–3 together for one place: technological portfolio, predictive innovation signal, and A61 diffusion history.",
)

master = load_county_master()
specialization = load_specialization()
a61 = load_a61_panel()

with st.container(border=True):
    f1, f2 = st.columns([1, 1], gap="large")
    states = sorted(master["STNAME"].dropna().unique())
    with f1:
        state = st.selectbox("State", states)
    state_df = master[master["STNAME"] == state].copy().sort_values("CTYNAME")
    with f2:
        county_name = st.selectbox("County", state_df["CTYNAME"].dropna().unique())

row = state_df[state_df["CTYNAME"] == county_name].iloc[0]
fips = row["FIPS"]
profile = row.get("cluster_profile")

st.markdown(f"### {county_name}, {state}")
status_items = [(f"FIPS {fips}", "neutral")]
if pd.notna(profile):
    status_items.append((str(profile), "good" if "Higher" in str(profile) else "neutral"))
if pd.notna(row.get("prediction_position")):
    status_items.append((str(row.get("prediction_position")), "good" if "Above" in str(row.get("prediction_position")) else "neutral"))
status_chips(status_items)

section_header("01", "Technology portfolio", "Read the county's breadth and specialization directly; treat the two broad clusters as descriptive summaries only.")

cols = st.columns(4, gap="medium")
with cols[0]:
    metric_card("Fractional patents", format_num(row.get("county_total"), 1), "◫", "Part 1 activity")
with cols[1]:
    metric_card("Technology breadth", format_num(row.get("tech_breadth"), 0), "◎", "CPC fields with specialization")
with cols[2]:
    metric_card("Diversification", format_num(row.get("diversification_entropy"), 3), "◌", "Normalized entropy")
with cols[3]:
    metric_card("Strongest CPC", "—" if pd.isna(row.get("strongest_CPC")) else str(row.get("strongest_CPC")), "◆", "Highest observed LQ")

county_spec = specialization[specialization["FIPS"] == fips].copy()
if not county_spec.empty:
    left, right = st.columns([1.35, .75], gap="large")
    with left:
        require_evidence = st.toggle(
            "Prioritize specializations supported by at least 5 fractional patents",
            value=True,
            help="This reduces the risk of emphasizing extreme LQ/RSCA values supported by very small patent counts.",
        )
        shown = county_spec[county_spec["min_evidence_5"]] if require_evidence and "min_evidence_5" in county_spec.columns else county_spec
        if shown.empty:
            st.warning("No specialization meets the evidence filter, so all observed technologies are shown.")
            shown = county_spec
        top = shown.sort_values(["RSCA", "fractional_patents"], ascending=False).head(10)
        st.plotly_chart(specialization_bar(top), use_container_width=True, config={"displayModeBar": False})
    with right:
        if pd.notna(profile):
            callout(f"<strong>Broad profile:</strong> {profile}.<br><br>This label summarizes breadth/activity structure; it is not a rigid technology type.")
        else:
            callout("<strong>Broad profile unavailable.</strong> This county did not meet the minimum activity threshold for the Part 1 clustering sample.")
        with st.expander("Show specialization table"):
            st.dataframe(
                top[["CPC_3digit", "fractional_patents", "LQ", "RSCA"]].rename(columns={
                    "CPC_3digit": "CPC",
                    "fractional_patents": "Fractional patents",
                }).style.format({"Fractional patents": "{:.2f}", "LQ": "{:.2f}", "RSCA": "{:.3f}"}),
                use_container_width=True,
                hide_index=True,
            )
else:
    st.info("No Part 1 specialization rows are available for this county.")

method_note(
    "Part 1 uses county × CPC 3-digit specialization. The final two-cluster solution is weakly separated, so the app treats the cluster label as a broad portfolio summary rather than a rigid technology type. County-specific CPC results are more informative."
)

section_header("02", "Observed innovation vs model expectation", "A screening lens: is observed patent intensity above or below what the three-variable Random Forest predicts for this county?")

actual = row.get("patents_per_1000")
pred = row.get("oof_pred_patents_per_1000")
resid = row.get("oof_residual_patents_per_1000")

mcols = st.columns(4, gap="medium")
with mcols[0]:
    metric_card("Observed / 1,000", format_num(actual, 2), "●", "Observed county intensity")
with mcols[1]:
    metric_card("OOF prediction", format_num(pred, 2), "◇", "5-fold screening estimate")
with mcols[2]:
    metric_card("Observed − predicted", format_num(resid, 2), "±", "Positive = above expectation")
with mcols[3]:
    metric_card("Model position", "—" if pd.isna(row.get("prediction_position")) else row.get("prediction_position"), "↗", "Descriptive screening label")

if pd.notna(actual) and pd.notna(pred):
    left, right = st.columns([1.25, .75], gap="large")
    with left:
        st.plotly_chart(observed_vs_predicted_chart(actual, pred), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown("#### Regional predictor values")
        p1, p2, p3 = st.columns(3)
        p1.metric("Bachelor's %", format_pct(row.get("bachelors_pct_2000")))
        p2.metric("Firm density", format_num(row.get("firm_density_2000"), 3))
        p3.metric("Knowledge share", format_pct(row.get("knowledge_share_2000")))
        callout("A positive residual means the county patents more intensively than the three-variable model predicts. It does <strong>not</strong> identify the cause of that difference.")
else:
    st.info("This county does not have a complete three-predictor record, so no out-of-fold prediction is shown.")

method_note(
    "The app uses 5-fold out-of-fold Random Forest predictions for county-level screening. The assignment's formal performance statistics remain the untouched held-out test results. Residuals are predictive discrepancies, not causal effects."
)

section_header("03", "A61 diffusion position", "See when the county entered A61 and whether patent activity deepened after entry.")
county_a61 = a61[a61["FIPS"] == fips].sort_values("decade_start").copy()

first_decade = None
if county_a61.empty:
    st.info("This county is outside the fixed Part 3 county universe.")
else:
    adopted = county_a61[county_a61["adopted_10"] == True]
    first_decade = int(adopted["decade_start"].min()) if not adopted.empty else None
    latest = county_a61[county_a61["decade_start"] == county_a61["decade_start"].max()].iloc[0]

    acols = st.columns(3, gap="medium")
    with acols[0]:
        metric_card("Ever crossed ≥10", "Yes" if first_decade is not None else "No", "✓" if first_decade is not None else "—", "Main adoption threshold")
    with acols[1]:
        metric_card("First threshold crossing", f"{first_decade}s" if first_decade is not None else "Not reached", "◷", "First decade ≥10 patents")
    with acols[2]:
        metric_card("A61 patents in 2000s", format_num(latest["patents"], 1), "↗", "Latest observed decade")

    st.plotly_chart(county_a61_timeline(county_a61), use_container_width=True, config={"displayModeBar": False})
    with st.expander("Show decade-by-decade A61 table"):
        st.dataframe(
            county_a61[["decade_start", "patents", "adopted_5", "adopted_10", "adopted_20"]].rename(columns={
                "decade_start": "Decade",
                "patents": "A61 patents",
                "adopted_5": "≥5",
                "adopted_10": "≥10",
                "adopted_20": "≥20",
            }),
            use_container_width=True,
            hide_index=True,
        )

section_header("04", "Integrated reading", "Use the signals together; no single indicator is treated as a final policy prescription.")
messages = []
if pd.notna(profile):
    messages.append(f"Its Part 1 portfolio is summarized as <strong>{str(profile).lower()}</strong>.")
if pd.notna(row.get("prediction_position")):
    messages.append(f"Observed patent intensity is <strong>{str(row.get('prediction_position')).lower()}</strong> under the three-variable model.")
if not county_a61.empty:
    if first_decade is None:
        messages.append("It did <strong>not</strong> cross the main A61 adoption threshold during 1950–2009.")
    else:
        messages.append(f"It first crossed the main A61 threshold in the <strong>{first_decade}s</strong>.")

if messages:
    callout(" ".join(messages) + " These signals identify where deeper regional investigation may be useful; they do not automate policy choice.")
