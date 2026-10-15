from pathlib import Path
import json
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

REQUIRED_FILES = [
    "county_master.csv",
    "county_specialization.csv",
    "a61_county_decade.csv",
    "a61_diffusion_summary.csv",
    "a61_moran_summary.csv",
    "model_metrics.csv",
    "model_importance.csv",
    "county_geometry.geojson",
]


def _fix_fips(df: pd.DataFrame) -> pd.DataFrame:
    if "FIPS" in df.columns:
        df = df.copy()
        df["FIPS"] = df["FIPS"].astype("string").str.replace(".0", "", regex=False).str.zfill(5)
    return df


def missing_files():
    return [name for name in REQUIRED_FILES if not (DATA_DIR / name).exists()]


def require_data():
    missing = missing_files()
    if missing:
        st.error(
            "The Streamlit export files are not in the app's data folder yet. "
            "Run the notebook export cell first, then copy the generated files into `data/`."
        )
        st.code("\n".join(missing), language="text")
        st.stop()


@st.cache_data(show_spinner=False)
def load_county_master():
    require_data()
    return _fix_fips(pd.read_csv(DATA_DIR / "county_master.csv", dtype={"FIPS": "string"}))


@st.cache_data(show_spinner=False)
def load_specialization():
    require_data()
    return _fix_fips(pd.read_csv(DATA_DIR / "county_specialization.csv", dtype={"FIPS": "string"}))


@st.cache_data(show_spinner=False)
def load_a61_panel():
    require_data()
    return _fix_fips(pd.read_csv(DATA_DIR / "a61_county_decade.csv", dtype={"FIPS": "string"}))


@st.cache_data(show_spinner=False)
def load_diffusion_summary():
    require_data()
    return pd.read_csv(DATA_DIR / "a61_diffusion_summary.csv")


@st.cache_data(show_spinner=False)
def load_moran_summary():
    require_data()
    return pd.read_csv(DATA_DIR / "a61_moran_summary.csv")


@st.cache_data(show_spinner=False)
def load_model_metrics():
    require_data()
    return pd.read_csv(DATA_DIR / "model_metrics.csv")


@st.cache_data(show_spinner=False)
def load_model_importance():
    require_data()
    return pd.read_csv(DATA_DIR / "model_importance.csv")


@st.cache_data(show_spinner=False)
def load_geojson():
    require_data()
    with open(DATA_DIR / "county_geometry.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    return geojson


def county_label(row):
    county = row.get("CTYNAME")
    state = row.get("STNAME")
    if pd.isna(county):
        county = "Unknown county"
    if pd.isna(state):
        state = "Unknown state"
    return f"{county}, {state}"


def format_num(value, decimals=2, missing="—"):
    if pd.isna(value):
        return missing
    return f"{value:,.{decimals}f}"


def format_pct(value, decimals=1, missing="—"):
    if pd.isna(value):
        return missing
    return f"{value:,.{decimals}f}%"
