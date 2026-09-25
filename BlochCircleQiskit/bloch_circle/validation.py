"""Validation helpers for the bloch_circle package."""

from __future__ import annotations

import numpy as np
from qiskit.quantum_info import Statevector


def validate_real_state(
    statevector: Statevector,
    tol: float = 1e-10,
) -> tuple[float, float]:
    """Return (a, b) if the state a|0⟩ + b|1⟩ has real amplitudes.

    Parameters
    ----------
    statevector : qiskit.quantum_info.Statevector
        A single-qubit statevector.
    tol : float
        Tolerance for treating imaginary parts as zero.

    Returns
    -------
    (a, b) : tuple[float, float]

    Raises
    ------
    ValueError
        If the statevector is not a single qubit or if any amplitude has
        a non-negligible imaginary part.
    """
    data = np.asarray(statevector.data, dtype=complex)

    if data.shape != (2,):
        raise ValueError(
            f"Expected a single-qubit state (length 2), got length {data.shape[0]}."
        )

    if np.any(np.abs(data.imag) > tol):
        raise ValueError(
            "The qubit state has complex amplitudes — cannot be represented "
            "on a Bloch circle.\n"
            f"  amplitudes = {data[0]}, {data[1]}"
        )

    a, b = data.real
    return float(a), float(b)
