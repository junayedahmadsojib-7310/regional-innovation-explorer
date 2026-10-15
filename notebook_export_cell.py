# ============================================================
# EXTENDED PROJECT — EXPORT DATA FOR STREAMLIT
# ============================================================
# Run this as the LAST code cell in the completed notebook.
# It does not alter Parts 1–4; it exports their validated outputs.
# ============================================================

from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_predict

# ------------------------------------------------------------
# 0. Output directory
# ------------------------------------------------------------
streamlit_dir = data_folder / "streamlit_export"
streamlit_dir.mkdir(parents=True, exist_ok=True)
print("Streamlit export directory:", streamlit_dir)

# ------------------------------------------------------------
# 1. Out-of-fold predictions for all complete Part 2 counties
# ------------------------------------------------------------
# The assignment's official evaluation remains the untouched
# 20% test set. These 5-fold OOF predictions are only for the
# interactive county-level screening extension.
# ------------------------------------------------------------
streamlit_model_data = model_data.reset_index(drop=True).copy()
X_streamlit = streamlit_model_data[features].copy()
y_streamlit = streamlit_model_data[target].copy()

oof_cv = KFold(n_splits=5, shuffle=True, random_state=42)
oof_rf = clone(best_rf)
oof_pred_log = cross_val_predict(
    oof_rf,
    X_streamlit,
    y_streamlit,
    cv=oof_cv,
    n_jobs=-1,
    method="predict",
)

streamlit_model_data["oof_pred_log_patents_per_1000"] = oof_pred_log
streamlit_model_data["oof_pred_patents_per_1000"] = np.expm1(oof_pred_log)
streamlit_model_data["oof_residual_log"] = (
    streamlit_model_data["log_patents_per_1000"]
    - streamlit_model_data["oof_pred_log_patents_per_1000"]
)
streamlit_model_data["oof_residual_patents_per_1000"] = (
    streamlit_model_data["patents_per_1000"]
    - streamlit_model_data["oof_pred_patents_per_1000"]
)
streamlit_model_data["prediction_position"] = np.select(
    [
        streamlit_model_data["oof_residual_log"] > 0,
        streamlit_model_data["oof_residual_log"] < 0,
    ],
    ["Above model prediction", "Below model prediction"],
    default="Approximately at model prediction",
)
streamlit_model_data["prediction_type"] = "5-fold out-of-fold screening prediction"

# ------------------------------------------------------------
# 2. Part 1 county profiles
# ------------------------------------------------------------
part1_export = (
    final_clusters.reset_index()[
        [
            "FIPS",
            "county_total",
            "tech_breadth",
            "diversification_entropy",
            "strongest_CPC",
            "max_LQ",
            "eligible_cluster",
            "cluster",
            "cluster_profile",
        ]
    ]
    .copy()
)

# ------------------------------------------------------------
# 3. Complete A61 county × decade panel
# ------------------------------------------------------------
a61_observed = (
    a61.groupby(["FIPS", "decade_start"], as_index=False)["patents"].sum()
)
a61_observed["FIPS"] = a61_observed["FIPS"].astype("string").str.zfill(5)

universe_fips = (
    county_universe.astype("string").str.zfill(5).sort_values().tolist()
)

a61_full_index = pd.MultiIndex.from_product(
    [universe_fips, analysis_decades],
    names=["FIPS", "decade_start"],
)

a61_county_decade = (
    a61_full_index.to_frame(index=False)
    .merge(
        a61_observed,
        on=["FIPS", "decade_start"],
        how="left",
        validate="one_to_one",
    )
)
a61_county_decade["patents"] = a61_county_decade["patents"].fillna(0)

for threshold_value in [5, 10, 20]:
    a61_county_decade[f"adopted_{threshold_value}"] = (
        a61_county_decade["patents"] >= threshold_value
    )

# ------------------------------------------------------------
# 4. County-level A61 status
# ------------------------------------------------------------
first_adoption_10 = (
    a61_county_decade[a61_county_decade["adopted_10"]]
    .groupby("FIPS")["decade_start"]
    .min()
    .rename("a61_first_adoption_decade")
)

latest_a61 = (
    a61_county_decade[a61_county_decade["decade_start"] == 2000][
        ["FIPS", "patents", "adopted_5", "adopted_10", "adopted_20"]
    ]
    .rename(
        columns={
            "patents": "a61_patents_2000s",
            "adopted_5": "a61_adopted_5_2000s",
            "adopted_10": "a61_adopted_10_2000s",
            "adopted_20": "a61_adopted_20_2000s",
        }
    )
)

a61_county_status = (
    pd.DataFrame({"FIPS": universe_fips})
    .merge(first_adoption_10, on="FIPS", how="left")
    .merge(latest_a61, on="FIPS", how="left", validate="one_to_one")
)
a61_county_status["a61_ever_adopted_10"] = (
    a61_county_status["a61_first_adoption_decade"].notna()
)

# ------------------------------------------------------------
# 5. Integrated county master table
# ------------------------------------------------------------
county_master = part2_model[
    [
        "FIPS",
        "STNAME",
        "CTYNAME",
        "patents_2000_2009",
        "avg_population_2000_2009",
        "patents_per_1000",
        "log_patents_per_1000",
        "bachelors_pct_2000",
        "firm_density_2000",
        "knowledge_share_2000",
    ]
].copy()

county_master["FIPS"] = county_master["FIPS"].astype("string").str.zfill(5)

model_prediction_export = streamlit_model_data[
    [
        "FIPS",
        "oof_pred_log_patents_per_1000",
        "oof_pred_patents_per_1000",
        "oof_residual_log",
        "oof_residual_patents_per_1000",
        "prediction_position",
        "prediction_type",
    ]
].copy()
model_prediction_export["FIPS"] = (
    model_prediction_export["FIPS"].astype("string").str.zfill(5)
)

part1_export["FIPS"] = part1_export["FIPS"].astype("string").str.zfill(5)

county_master = county_master.merge(
    model_prediction_export,
    on="FIPS",
    how="left",
    validate="one_to_one",
)
county_master["part2_complete_case"] = (
    county_master["oof_pred_log_patents_per_1000"].notna()
)

county_master = county_master.merge(
    part1_export,
    on="FIPS",
    how="left",
    validate="one_to_one",
)
county_master["part1_profile_available"] = county_master["cluster_profile"].notna()

county_master = county_master.merge(
    a61_county_status,
    on="FIPS",
    how="left",
    validate="one_to_one",
)
county_master["part3_a61_available"] = county_master["a61_patents_2000s"].notna()

# ------------------------------------------------------------
# 6. County × CPC specialization export
# ------------------------------------------------------------
county_specialization_export = specialization[
    [
        "FIPS",
        "CPC_3digit",
        "fractional_patents",
        "county_total",
        "LQ",
        "RSCA",
        "eligible_cluster",
    ]
].copy()
county_specialization_export["FIPS"] = (
    county_specialization_export["FIPS"].astype("string").str.zfill(5)
)
county_specialization_export["min_evidence_5"] = (
    county_specialization_export["fractional_patents"] >= 5
)

county_names = (
    part2_model[["FIPS", "STNAME", "CTYNAME"]]
    .drop_duplicates(subset="FIPS")
    .copy()
)
county_names["FIPS"] = county_names["FIPS"].astype("string").str.zfill(5)

county_specialization_export = county_specialization_export.merge(
    county_names,
    on="FIPS",
    how="left",
    validate="many_to_one",
)

# ------------------------------------------------------------
# 7. Diffusion + Moran + model summaries
# ------------------------------------------------------------
a61_diffusion_summary = (
    threshold_trajectory.merge(
        a61_cumulative,
        on=["threshold", "decade_start"],
        how="outer",
        validate="one_to_one",
    )
    .sort_values(["threshold", "decade_start"])
    .reset_index(drop=True)
)

a61_moran_summary = activity_robustness.copy()
model_metrics_export = final_comparison.copy()
model_importance_export = rf_importance.copy()

# ------------------------------------------------------------
# 8. County geometry for web maps
# ------------------------------------------------------------
# Export WGS84 geometry for Plotly/Streamlit rather than the
# projected EPSG:5070 used by static notebook maps.
# ------------------------------------------------------------
streamlit_geo = counties_geo[
    counties_geo["FIPS"].isin(county_master["FIPS"])
][["FIPS", "NAME", "STATEFP", "geometry"]].copy()
streamlit_geo["FIPS"] = streamlit_geo["FIPS"].astype("string").str.zfill(5)
streamlit_geo = streamlit_geo.to_crs(epsg=4326)

# ------------------------------------------------------------
# 9. Save
# ------------------------------------------------------------
county_master.to_csv(streamlit_dir / "county_master.csv", index=False)
county_specialization_export.to_csv(
    streamlit_dir / "county_specialization.csv", index=False
)
a61_county_decade.to_csv(streamlit_dir / "a61_county_decade.csv", index=False)
a61_diffusion_summary.to_csv(
    streamlit_dir / "a61_diffusion_summary.csv", index=False
)
a61_moran_summary.to_csv(streamlit_dir / "a61_moran_summary.csv", index=False)
model_metrics_export.to_csv(streamlit_dir / "model_metrics.csv", index=False)
model_importance_export.to_csv(streamlit_dir / "model_importance.csv", index=False)
streamlit_geo.to_file(
    streamlit_dir / "county_geometry.geojson",
    driver="GeoJSON",
)

# ------------------------------------------------------------
# 10. Validation
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("STREAMLIT EXPORT COMPLETE")
print("=" * 70)
print("County master rows:", f"{len(county_master):,}")
print("Unique county-master FIPS:", f"{county_master['FIPS'].nunique():,}")
print("Part 1 profiles:", f"{county_master['part1_profile_available'].sum():,}")
print("Part 2 OOF predictions:", f"{county_master['part2_complete_case'].sum():,}")
print("Part 3 A61 counties:", f"{county_master['part3_a61_available'].sum():,}")
print("County-specialization rows:", f"{len(county_specialization_export):,}")
print("CPC technologies:", county_specialization_export["CPC_3digit"].nunique())
print("A61 county × decade rows:", f"{len(a61_county_decade):,}")
print("Expected A61 rows:", f"{len(universe_fips) * len(analysis_decades):,}")
print("GeoJSON counties:", f"{len(streamlit_geo):,}")
print("GeoJSON CRS:", streamlit_geo.crs)

print("\nFiles written:")
for export_file in sorted(streamlit_dir.iterdir()):
    print(" -", export_file.name)
