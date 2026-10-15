import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


INK = "#102a43"
MUTED = "#6b7f93"
TEAL = "#0f8b8d"
TEAL_2 = "#1bb3a9"
CYAN = "#76d7d0"
NAVY = "#0b3046"
BLUE = "#3e7fa3"
AMBER = "#f3b34c"
CORAL = "#e7775b"
GRID = "#e6eef3"


def _style(fig, height=390, title=None):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=12),
        margin=dict(l=16, r=16, t=58 if title else 28, b=16),
        title=dict(text=title, x=0.02, xanchor="left", font=dict(size=17, color=INK)),
        hoverlabel=dict(bgcolor="white", font=dict(color=INK, size=12)),
        legend=dict(
            bgcolor="rgba(255,255,255,.80)",
            bordercolor="#dce7ef",
            borderwidth=1,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, title_font=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, title_font=dict(color=MUTED))
    return fig


def county_choropleth(df, geojson, value_col, title, hover_cols=None, discrete=False):
    hover_cols = hover_cols or []
    data = df.copy()

    if discrete:
        fig = px.choropleth(
            data,
            geojson=geojson,
            locations="FIPS",
            featureidkey="properties.FIPS",
            color=value_col,
            hover_name="CTYNAME" if "CTYNAME" in data.columns else None,
            hover_data=hover_cols,
            scope="usa",
            color_discrete_map={
                "Adopted": TEAL,
                "Below threshold": "#d9e5eb",
                "Higher-activity / broader technology profile": TEAL,
                "Lower-activity / narrower technology profile": "#92aebe",
            },
            category_orders={value_col: ["Below threshold", "Adopted"]},
        )
    else:
        kwargs = {}
        if value_col == "RSCA":
            kwargs.update(
                color_continuous_scale=[
                    [0.0, "#d9e5eb"],
                    [0.5, "#f8fbfd"],
                    [1.0, TEAL],
                ],
                range_color=(-1, 1),
                color_continuous_midpoint=0,
            )
        elif "log" in value_col.lower() or "patent" in value_col.lower():
            kwargs.update(color_continuous_scale=["#edf4f8", "#9ddad6", "#0f8b8d", "#08384c"])
        else:
            kwargs.update(color_continuous_scale=["#edf4f8", "#86d2cd", "#0f8b8d", "#08384c"])

        fig = px.choropleth(
            data,
            geojson=geojson,
            locations="FIPS",
            featureidkey="properties.FIPS",
            color=value_col,
            hover_name="CTYNAME" if "CTYNAME" in data.columns else None,
            hover_data=hover_cols,
            scope="usa",
            **kwargs,
        )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="albers usa",
        bgcolor="rgba(0,0,0,0)",
        showland=True,
        landcolor="#f5f8fa",
    )
    fig.update_traces(marker_line_width=0.12, marker_line_color="rgba(255,255,255,.72)")
    fig.update_layout(
        margin=dict(l=0, r=0, t=48, b=0),
        coloraxis_colorbar=dict(thickness=11, len=.66, outlinewidth=0, tickfont=dict(size=10)),
        legend_title_text="",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK),
        title=dict(text=title, x=0.01, xanchor="left", font=dict(size=17, color=INK)),
        height=540,
    )
    return fig


def observed_vs_predicted_chart(actual, predicted):
    values = [actual, predicted]
    labels = ["Observed", "OOF prediction"]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=values,
            orientation="h",
            marker_color=[TEAL, "#9eb4c3"],
            text=[f"{v:.2f}" for v in values],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}: %{x:.2f}<extra></extra>",
        )
    )
    delta = actual - predicted
    fig.add_annotation(
        x=max(values) * .98 if max(values) > 0 else .1,
        y=1.35,
        text=f"Observed − predicted: {delta:+.2f}",
        showarrow=False,
        font=dict(size=12, color=TEAL if delta >= 0 else CORAL),
        bgcolor="#f6fbfb",
        bordercolor="#dce7ef",
        borderpad=6,
    )
    fig.update_xaxes(title="Patents per 1,000 inhabitants", rangemode="tozero")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_layout(showlegend=False, bargap=.45)
    return _style(fig, height=310, title="Observed vs model-expected patent intensity")


def predictor_importance_chart(importance):
    imp = importance.copy().sort_values("Importance")
    label_map = {
        "bachelors_pct_2000": "Bachelor's degree %",
        "firm_density_2000": "Firm density",
        "knowledge_share_2000": "Knowledge-sector share",
    }
    imp["Label"] = imp["Predictor"].map(label_map).fillna(imp["Predictor"])
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=imp["Importance"],
            y=imp["Label"],
            orientation="h",
            marker=dict(
                color=["#83cfc9", "#4caeaa", TEAL][:len(imp)],
                line=dict(width=0),
            ),
            error_x=dict(
                type="data",
                array=imp["Importance_SD"] if "Importance_SD" in imp.columns else None,
                visible="Importance_SD" in imp.columns,
                color="#50677a",
                thickness=1.2,
            ),
            hovertemplate="%{y}<br>Importance: %{x:.3f}<extra></extra>",
        )
    )
    fig.update_xaxes(title="Permutation importance")
    fig.update_yaxes(title="")
    fig.update_layout(showlegend=False)
    return _style(fig, height=330, title="Which regional signal contributed most to prediction?")


def specialization_bar(top):
    data = top.copy().sort_values("RSCA")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["RSCA"],
            y=data["CPC_3digit"],
            orientation="h",
            marker=dict(color=data["RSCA"], colorscale=[[0, "#a7becb"], [1, TEAL]], cmin=-1, cmax=1),
            customdata=np.stack([data["fractional_patents"], data["LQ"]], axis=-1),
            hovertemplate="CPC %{y}<br>RSCA %{x:.3f}<br>Fractional patents %{customdata[0]:.2f}<br>LQ %{customdata[1]:.2f}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_width=1, line_color="#9fb3c2")
    fig.update_xaxes(title="RSCA", range=[-1, 1])
    fig.update_yaxes(title="")
    return _style(fig, height=380, title="Strongest observed specializations")


def county_a61_timeline(county_panel):
    df = county_panel.sort_values("decade_start").copy()
    df["period"] = df["decade_start"].astype(int).astype(str) + "s"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["period"],
            y=df["patents"],
            mode="lines+markers",
            line=dict(color=TEAL, width=3),
            marker=dict(size=8, color="white", line=dict(color=TEAL, width=2.5)),
            fill="tozeroy",
            fillcolor="rgba(15,139,141,.09)",
            hovertemplate="%{x}<br>A61 patents: %{y:.1f}<extra></extra>",
        )
    )
    fig.add_hline(
        y=10,
        line_dash="dash",
        line_color=AMBER,
        annotation_text="Main threshold = 10",
        annotation_position="top left",
        annotation_font_color="#85601c",
    )
    fig.update_xaxes(title="Decade")
    fig.update_yaxes(title="A61 patents", rangemode="tozero")
    fig.update_layout(showlegend=False)
    return _style(fig, height=350, title="A61 activity through time")


def diffusion_curve(summary):
    df = summary.copy()
    df["threshold_label"] = "≥" + df["threshold"].astype(int).astype(str) + " patents"
    df["period"] = df["decade_start"].astype(int).astype(str) + "s"
    colors = {"≥5 patents": "#8aa7b8", "≥10 patents": TEAL, "≥20 patents": AMBER}
    fig = px.line(
        df,
        x="period",
        y="cumulative_adopters",
        color="threshold_label",
        markers=True,
        color_discrete_map=colors,
    )
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_xaxes(title="Decade")
    fig.update_yaxes(title="Cumulative adopting counties", rangemode="tozero")
    fig.update_layout(legend_title_text="Threshold")
    return _style(fig, height=390, title="Cumulative geographic diffusion")


def threshold_sensitivity_chart(summary):
    df = summary.copy()
    df["threshold_label"] = "≥" + df["threshold"].astype(int).astype(str) + " patents"
    df["period"] = df["decade_start"].astype(int).astype(str) + "s"
    colors = {"≥5 patents": "#8aa7b8", "≥10 patents": TEAL, "≥20 patents": AMBER}
    fig = px.line(
        df,
        x="period",
        y="period_adopters",
        color="threshold_label",
        markers=True,
        color_discrete_map=colors,
    )
    fig.update_traces(line_width=2.7, marker_size=7)
    fig.update_xaxes(title="Decade")
    fig.update_yaxes(title="Period adopters", rangemode="tozero")
    fig.update_layout(legend_title_text="Threshold")
    return _style(fig, height=360, title="Threshold sensitivity: period adopters")


def moran_chart(moran):
    df = moran.copy()
    df["period"] = df["decade_start"].astype(int).astype(str) + "s"
    long = df.melt(
        id_vars="period",
        value_vars=["binary_moran_I", "activity_moran_I"],
        var_name="measure",
        value_name="moran_I",
    )
    long["measure"] = long["measure"].map({
        "binary_moran_I": "Adoption status",
        "activity_moran_I": "Patent activity intensity",
    })
    fig = px.line(
        long,
        x="period",
        y="moran_I",
        color="measure",
        markers=True,
        color_discrete_map={"Adoption status": "#8aa7b8", "Patent activity intensity": TEAL},
    )
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_xaxes(title="Decade")
    fig.update_yaxes(title="Global Moran's I", range=[0, max(.65, float(long["moran_I"].max()) + .05)])
    fig.update_layout(legend_title_text="Measure")
    return _style(fig, height=390, title="Spatial concentration over time")


def ranking_bar(rank, metric, metric_label):
    data = rank.copy().head(12).sort_values(metric)
    if data.empty:
        return go.Figure()
    data["label"] = data["CTYNAME"].fillna("Unknown") + ", " + data["STNAME"].fillna("")
    fig = go.Figure(
        go.Bar(
            x=data[metric],
            y=data["label"],
            orientation="h",
            marker_color=TEAL,
            customdata=np.stack([data["fractional_patents"], data["LQ"], data["RSCA"]], axis=-1),
            hovertemplate=(
                "%{y}<br>Value: %{x:.3f}<br>Fractional patents: %{customdata[0]:.2f}"
                "<br>LQ: %{customdata[1]:.2f}<br>RSCA: %{customdata[2]:.3f}<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title=metric_label)
    fig.update_yaxes(title="")
    return _style(fig, height=430, title="Leading counties under the selected measure")


def portfolio_donut(master):
    data = master[master["part1_profile_available"] == True]["cluster_profile"].value_counts().reset_index()
    data.columns = ["profile", "counties"]
    if data.empty:
        return go.Figure()
    fig = px.pie(
        data,
        names="profile",
        values="counties",
        hole=.68,
        color="profile",
        color_discrete_map={
            "Higher-activity / broader technology profile": TEAL,
            "Lower-activity / narrower technology profile": "#9fb5c3",
        },
    )
    fig.update_traces(textinfo="percent", hovertemplate="%{label}<br>%{value:,} counties (%{percent})<extra></extra>")
    fig.add_annotation(text=f"{int(data['counties'].sum()):,}<br><span style='font-size:11px'>counties</span>", x=.5, y=.5, showarrow=False, font=dict(size=22, color=INK))
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-.05, x=0))
    return _style(fig, height=350, title="Broad portfolio profiles")
