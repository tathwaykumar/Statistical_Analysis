"""Shared Plotly chart builders using a restrained, consistent visual system."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

NAVY = "#0B1E3D"
CHARCOAL = "#1F2937"
WHITE = "#FFFFFF"
GREY = "#94A3B8"
ACCENT_BLUE = "#3B82F6"
GREEN = "#22C55E"
AMBER = "#F59E0B"
RED = "#EF4444"

TEMPLATE = "plotly_white"
FONT = dict(family="Inter, Segoe UI, sans-serif", size=13, color=CHARCOAL)


def _base_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        template=TEMPLATE, font=FONT, title=dict(text=title, font=dict(size=16, color=NAVY)),
        margin=dict(l=40, r=20, t=60, b=40), plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        legend=dict(bgcolor=WHITE, font=dict(color=CHARCOAL), bordercolor="#E5E7EB", borderwidth=1),
        xaxis=dict(color=CHARCOAL, gridcolor="#E5E7EB"),
        yaxis=dict(color=CHARCOAL, gridcolor="#E5E7EB"),
    )
    return fig


def style_figure(fig: go.Figure, title: str | None = None) -> go.Figure:
    """Apply the shared visual system to an ad-hoc Plotly Express figure.

    Forces an explicit white background and dark, legible text regardless of
    the viewer's browser/OS colour scheme -- Streamlit's st.plotly_chart
    otherwise auto-recolours figures to match its ambient theme (light or
    dark), which can wash out Plotly's own template. Pass theme=None to
    st.plotly_chart alongside this for the colours to actually stick.
    """
    layout_kwargs = dict(
        template=TEMPLATE, font=FONT, margin=dict(l=40, r=20, t=60, b=40),
        plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        legend=dict(bgcolor=WHITE, font=dict(color=CHARCOAL), bordercolor="#E5E7EB", borderwidth=1),
        xaxis=dict(color=CHARCOAL, gridcolor="#E5E7EB"),
        yaxis=dict(color=CHARCOAL, gridcolor="#E5E7EB"),
    )
    if title:
        layout_kwargs["title"] = dict(text=title, font=dict(size=16, color=NAVY))
    fig.update_layout(**layout_kwargs)
    return fig


def histogram(df: pd.DataFrame, col: str, bins: int = 30, title: str | None = None) -> go.Figure:
    fig = px.histogram(df, x=col, nbins=bins, color_discrete_sequence=[ACCENT_BLUE])
    return _base_layout(fig, title or f"Distribution of {col}")


def box_plot(df: pd.DataFrame, col: str, group: str | None = None, title: str | None = None) -> go.Figure:
    fig = px.box(df, x=group, y=col, color=group, color_discrete_sequence=px.colors.qualitative.Safe)
    return _base_layout(fig, title or f"Box plot of {col}" + (f" by {group}" if group else ""))


def density_plot(df: pd.DataFrame, col: str, title: str | None = None) -> go.Figure:
    fig = px.histogram(df, x=col, histnorm="probability density", nbins=40,
                        color_discrete_sequence=[ACCENT_BLUE], marginal=None)
    fig.update_traces(opacity=0.85)
    return _base_layout(fig, title or f"Density of {col}")


def correlation_heatmap(corr_matrix: pd.DataFrame, title: str = "Correlation Heatmap") -> go.Figure:
    fig = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1,
                     aspect="auto")
    return _base_layout(fig, title)


def scatter_with_trendline(df: pd.DataFrame, x: str, y: str, color: str | None = None,
                            title: str | None = None) -> go.Figure:
    fig = px.scatter(df, x=x, y=y, color=color, trendline="ols",
                      color_discrete_sequence=px.colors.qualitative.Safe, opacity=0.7)
    return _base_layout(fig, title or f"{y} vs {x}")


def residual_plot(fitted: np.ndarray, residuals: np.ndarray) -> go.Figure:
    fig = go.Figure(go.Scatter(x=fitted, y=residuals, mode="markers",
                                marker=dict(color=ACCENT_BLUE, opacity=0.6)))
    fig.add_hline(y=0, line_dash="dash", line_color=RED)
    return _base_layout(fig, "Residuals vs Fitted Values")


def predicted_vs_actual(y_true: np.ndarray, y_pred: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_true, y=y_pred, mode="markers",
                              marker=dict(color=ACCENT_BLUE, opacity=0.6), name="Predictions"))
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    fig.add_trace(go.Scatter(x=lims, y=lims, mode="lines", line=dict(color=RED, dash="dash"),
                              name="Perfect prediction"))
    return _base_layout(fig, "Predicted vs Actual")


def bar_group_means(group_stats: dict, title: str) -> go.Figure:
    names = list(group_stats.keys())
    means = [group_stats[n]["mean"] for n in names]
    fig = go.Figure(go.Bar(x=names, y=means, marker_color=ACCENT_BLUE))
    return _base_layout(fig, title)
