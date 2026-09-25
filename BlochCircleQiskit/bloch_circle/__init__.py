"""
bloch_circle — Visualise a qubit on a 2-D Bloch circle.

Works with any Qiskit Statevector whose amplitudes are both real.
The state  a|0⟩ + b|1⟩  is drawn as the vector (a, b) inside the unit
circle.
"""

from .plot import plot_bloch_circle          # noqa: F401
from .validation import validate_real_state  # noqa: F401

__version__ = "0.1.0"
