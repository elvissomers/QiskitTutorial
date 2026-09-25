"""Example usage of the bloch_circle package."""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from bloch_circle import plot_bloch_circle

# ── Example 1: |+⟩ state ───────────────────────────────────────────
print("=== Example 1: Hadamard on |0⟩  →  |+⟩ ===")
qc = QuantumCircuit(1)
qc.h(0)
sv = Statevector.from_instruction(qc)
plot_bloch_circle(sv, title="Hadamard |+⟩ state")

# ── Example 2: Ry rotation ─────────────────────────────────────────
import numpy as np

print("\n=== Example 2: Ry(π/3) on |0⟩ ===")
qc2 = QuantumCircuit(1)
qc2.ry(np.pi / 3, 0)
sv2 = Statevector.from_instruction(qc2)
plot_bloch_circle(sv2, title="Ry(π/3) state")

# ── Example 3: complex state (should error) ────────────────────────
print("\n=== Example 3: Complex state — should print error ===")
qc3 = QuantumCircuit(1)
qc3.h(0)
qc3.s(0)        # introduces a phase of i on |1⟩
sv3 = Statevector.from_instruction(qc3)
try:
    plot_bloch_circle(sv3)
except ValueError as e:
    print(f"ERROR: {e}")
