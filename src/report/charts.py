"""Matplotlib chart generation for embedding static images in the PDF report."""
from __future__ import annotations

import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

NAVY = "#0B1E3D"
ACCENT_BLUE = "#3B82F6"


def _fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def grade_histogram_png(df: pd.DataFrame) -> bytes:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.hist(df["G3"], bins=20, color=ACCENT_BLUE, edgecolor="white")
    ax.set_title("Distribution of Final Grade (G3)", color=NAVY, fontsize=11)
    ax.set_xlabel("G3"); ax.set_ylabel("Frequency")
    return _fig_to_bytes(fig)


def correlation_heatmap_png(corr: pd.DataFrame) -> bytes:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(corr, cmap="RdBu", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns))); ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(corr.columns))); ax.set_yticklabels(corr.columns, fontsize=8)
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=6, color="black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation Heatmap", color=NAVY, fontsize=11)
    return _fig_to_bytes(fig)


def anova_group_means_png(group_stats: dict, title: str) -> bytes:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    names = list(group_stats.keys())
    means = [group_stats[n]["mean"] for n in names]
    ax.bar(names, means, color=ACCENT_BLUE)
    ax.set_title(title, color=NAVY, fontsize=11)
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    return _fig_to_bytes(fig)


def regression_residual_png(fitted, residuals) -> bytes:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.scatter(fitted, residuals, alpha=0.5, color=ACCENT_BLUE, s=14)
    ax.axhline(0, color="red", linestyle="--")
    ax.set_title("Residuals vs Fitted Values", color=NAVY, fontsize=11)
    ax.set_xlabel("Fitted"); ax.set_ylabel("Residual")
    return _fig_to_bytes(fig)
