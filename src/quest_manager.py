"""Simple quest tracking for the playable prototype."""
class QuestManager:
    def __init__(self):
        self.talked_to_partner = False
        self.has_caught_fish = False
        self.reached_barrier = False
        self.touched_barrier = False
        self.passed_barrier = False
        self.main_quest = "Find the perfect pebble"
        self.objective = "Talk to your partner (F)"

    def talk_to_partner(self):
        self.talked_to_partner = True

    def record_fish_caught(self):
        self.has_caught_fish = True

    def touch_barrier(self):
        self.touched_barrier = True

    def update(self, player_x, barrier_x, barrier_open):
        if player_x >= barrier_x + 80:
            self.passed_barrier = True
        if self.touched_barrier:
            self.reached_barrier = True
        if not self.talked_to_partner:
            self.objective = "Talk to your partner (F)"
        elif self.passed_barrier:
            self.objective = "Explore beyond the barrier"
        elif self.reached_barrier:
            self.objective = "Open the |-> phase barrier"
        else:
            self.objective = "Explore Antarctica"

    def get_hint(self, fish_count, player_x, barrier_x, is_superposition, state_name):
        if not self.talked_to_partner:
            return "Arrow keys: move  |  F: talk to your partner"
        if self.reached_barrier and not self.passed_barrier:
            if state_name == "|-> SUPERPOSITION":
                return "Barrier open! Move through it"
            if not is_superposition:
                return "Barrier needs |->  |  H: superposition (2 fish)"
            return "Z: change the relative phase (3 fish)"
        if not self.has_caught_fish:
            return "Find fish and press E to catch them"
        return ""
