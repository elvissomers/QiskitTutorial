"""Core plotting routine for the Bloch circle."""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from qiskit.quantum_info import Statevector

from .validation import validate_real_state


def plot_bloch_circle(
    statevector: Statevector,
    *,
    ax: Optional[plt.Axes] = None,
    figsize: tuple[float, float] = (6, 6),
    show: bool = True,
    title: Optional[str] = None,
) -> plt.Axes:
    """Draw a qubit state on the Bloch circle.

    The state a|0⟩ + b|1⟩ is represented as the 2-D vector (a, b)
    inside the unit circle, where |0⟩ points along +x and |1⟩ along +y.

    Parameters
    ----------
    statevector : qiskit.quantum_info.Statevector
        A single-qubit statevector with real amplitudes.
    ax : matplotlib Axes, optional
        An existing axes to draw on.  A new figure is created when *None*.
    figsize : tuple, optional
        Figure size (inches) when creating a new figure.
    show : bool, optional
        Call ``plt.show()`` automatically.  Set to *False* when embedding
        in a larger figure or notebook.
    title : str, optional
        Custom title.  Defaults to the ket notation of the state.

    Returns
    -------
    matplotlib.axes.Axes
    """
    # ── validate ────────────────────────────────────────────────────
    a, b = validate_real_state(statevector)

    # ── set up figure ───────────────────────────────────────────────
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    ax.set_aspect("equal")
    margin = 0.3
    ax.set_xlim(-1 - margin, 1 + margin)
    ax.set_ylim(-1 - margin, 1 + margin)

    # ── style: dark background ──────────────────────────────────────
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="#aaaaaa", labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#444466")

    # ── unit circle ─────────────────────────────────────────────────
    circle = mpatches.Circle(
        (0, 0), 1,
        fill=False,
        edgecolor="#7f5af0",
        linewidth=2,
        linestyle="-",
        zorder=1,
    )
    ax.add_patch(circle)

    # ── axes lines ──────────────────────────────────────────────────
    ax.axhline(0, color="#444466", linewidth=0.8, zorder=0)
    ax.axvline(0, color="#444466", linewidth=0.8, zorder=0)

    # ── basis labels ────────────────────────────────────────────────
    label_kwargs = dict(fontsize=14, fontweight="bold", color="#e0e0e0", ha="center", va="center")
    ax.text(1.15, 0, "|0⟩", **label_kwargs)
    ax.text(-1.15, 0, "−|0⟩", **label_kwargs)
    ax.text(0, 1.15, "|1⟩", **label_kwargs)
    ax.text(0, -1.15, "−|1⟩", **label_kwargs)

    # ── state vector arrow ──────────────────────────────────────────
    ax.annotate(
        "",
        xy=(a, b),
        xytext=(0, 0),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#2ee89e",
            lw=2.5,
            mutation_scale=18,
        ),
        zorder=3,
    )

    # ── dot at tip ──────────────────────────────────────────────────
    ax.plot(a, b, "o", color="#2ee89e", markersize=8, zorder=4)

    # ── angle arc (visual aid) ──────────────────────────────────────
    theta = np.degrees(np.arctan2(b, a))
    if abs(a) + abs(b) > 1e-8:
        arc = mpatches.Arc(
            (0, 0), 0.45, 0.45,
            angle=0,
            theta1=0,
            theta2=theta,
            color="#f5a623",
            linewidth=1.5,
            linestyle="--",
            zorder=2,
        )
        ax.add_patch(arc)
        # label the angle
        mid_angle = np.radians(theta / 2)
        ax.text(
            0.32 * np.cos(mid_angle),
            0.32 * np.sin(mid_angle),
            f"θ={theta:.1f}°",
            fontsize=10,
            color="#f5a623",
            ha="center",
            va="center",
            zorder=5,
        )

    # ── coordinate annotation ───────────────────────────────────────
    ax.text(
        a, b + 0.12,
        f"({a:.3f}, {b:.3f})",
        fontsize=10,
        color="#2ee89e",
        ha="center",
        va="bottom",
        zorder=5,
    )

    # ── title ───────────────────────────────────────────────────────
    if title is None:
        title = _ket_label(a, b)
    ax.set_title(title, fontsize=14, color="#e0e0e0", pad=16)

    # ── grid ────────────────────────────────────────────────────────
    ax.grid(True, color="#333355", linewidth=0.5, linestyle=":")

    if show:
        plt.tight_layout()
        plt.show()

    return ax


# ── helpers ─────────────────────────────────────────────────────────

def _ket_label(a: float, b: float) -> str:
    """Build a nice ket string like ``0.707|0⟩ + 0.707|1⟩``."""
    parts: list[str] = []
    if abs(a) > 1e-10:
        parts.append(f"{a:+.4f}|0⟩")
    if abs(b) > 1e-10:
        parts.append(f"{b:+.4f}|1⟩")
    label = " ".join(parts).lstrip("+").strip()
    return label if label else "0"
