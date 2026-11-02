"""Quantum gate rules, resources, and physical-layer synchronization."""

from settings import ICE_TOP, ICE_BOTTOM, WATER_TOP, WATER_BOTTOM
from src.quantum.quantum_state import QuantumState


class QuantumController:
    X_COST = 1
    H_COST = 2
    Z_COST = 3

    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.qubit = QuantumState()
        self.layer = 0
        self.fish_count = 0

    @property
    def is_superposition(self):
        ice, water = self.qubit.get_probabilities()
        return ice > 1e-9 and water > 1e-9

    def add_fish(self):
        self.fish_count += 1

    def switch_layer(self):
        ice_height = ICE_BOTTOM - ICE_TOP
        water_height = WATER_BOTTOM - WATER_TOP
        if self.layer == 0:
            relative_y = (self.player.y - ICE_TOP) / ice_height
            self.player.y = WATER_TOP + relative_y * water_height
            self.layer = 1
        else:
            relative_y = (self.player.y - WATER_TOP) / water_height
            new_y = ICE_TOP + relative_y * ice_height
            self.world.resolve_layer_switch(self.player, new_y)
            self.player.y = new_y
            self.layer = 0

    def sync_physical_layer(self):
        if self.is_superposition:
            return
        ice, _ = self.qubit.get_probabilities()
        target = 0 if ice > 1 - 1e-9 else 1
        if target != self.layer:
            self.switch_layer()

    def apply_gate(self, gate):
        """Apply a gate and return the existing player-facing message."""
        if gate == "X":
            if self.is_superposition:
                return "X in superposition is coming soon!"
            if self.fish_count < self.X_COST:
                return "Not enough fish for X gate!"
            self.qubit.apply_x()
            self.switch_layer()
            self.fish_count -= self.X_COST
            return "X gate activated! -1 fish"

        if gate == "H":
            if self.fish_count < self.H_COST:
                return "Not enough fish for H gate!"
            self.qubit.apply_h()
            self.sync_physical_layer()
            self.fish_count -= self.H_COST
            return "H gate activated! -2 fish"

        if gate == "Z":
            if not self.is_superposition:
                return "Z gate requires superposition!"
            if self.fish_count < self.Z_COST:
                return "Not enough fish for Z gate!"
            self.qubit.apply_z()
            self.fish_count -= self.Z_COST
            return "Z gate activated! -3 fish"

        raise ValueError(f"Unknown quantum gate: {gate}")
