import math
import random


class QuantumState:
    """
    Represents a single qubit.

    |0> = ice
    |1> = water
    """

    def __init__(self):
        # The penguin starts on ice.
        self.alpha = 1 + 0j
        self.beta = 0 + 0j

    # QUANTUM GATES
    def apply_x(self):
        """
        Pauli-X gate: swaps the amplitudes.
        """
        self.alpha, self.beta = self.beta, self.alpha

    def apply_h(self):
        """
        Hadamard gate: creates or removes superposition.
        """
        alpha = self.alpha
        beta = self.beta

        self.alpha = (alpha + beta) / math.sqrt(2)
        self.beta = (alpha - beta) / math.sqrt(2)

    def apply_z(self):
        """
        Pauli-Z gate: flips the phase of |1>.
        """
        self.beta = -self.beta

    # PROBABILITIES
    def get_probabilities(self):
        """
        Returns the probabilities of ice and water.
        """
        return (
            abs(self.alpha) ** 2,
            abs(self.beta) ** 2
        )

    # MEASUREMENT
    def measure(self):
        """
        Measures the qubit and collapses its state.

        Returns:
            0 = ice
            1 = water
        """
        probability_ice = abs(self.alpha) ** 2

        if random.random() < probability_ice:
            self.alpha = 1 + 0j
            self.beta = 0 + 0j
            return 0

        self.alpha = 0 + 0j
        self.beta = 1 + 0j
        return 1

    # STATE IDENTIFICATION
    def get_state_name(self):
        """
        Returns a readable name for common quantum states.
        """
        tolerance = 1e-9

        if abs(self.beta) < tolerance:
            return "|0> ICE"

        if abs(self.alpha) < tolerance:
            return "|1> WATER"

        if abs(self.alpha - self.beta) < tolerance:
            return "|+> SUPERPOSITION"

        if abs(self.alpha + self.beta) < tolerance:
            return "|-> SUPERPOSITION"

        return "QUANTUM SUPERPOSITION"