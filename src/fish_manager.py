import random
import math

from src.quantum_fish import QuantumFish
from settings import WIDTH, WORLD_WIDTH


class FishManager:

    def __init__(self):

        # FISH COLLECTION
        self.fish = []

        # POPULATION SETTINGS
        self.max_fish = 8
        self.initial_fish = 5

        # SPAWN SETTINGS
        self.spawn_min = 3.0
        self.spawn_max = 6.0

        self.spawn_timer = 0.0
        self.next_spawn = random.uniform(
            self.spawn_min,
            self.spawn_max
        )

        # Distance outside the camera view
        self.spawn_margin = 130
        self.despawn_margin = 350

        self.initialized = False

    # INITIAL FISH
    def spawn_initial_fish(self, camera):

        """
        Create fish that already exist in the world
        when the game starts.

        Initial fish alternate between swimming
        left and right.
        """

        for index in range(
            min(self.initial_fish, self.max_fish)
        ):

            # Spread fish across the visible camera area
            x = random.uniform(
                camera.x + 80,
                camera.x + WIDTH - 80
            )

            # Alternate directions to guarantee variety
            direction = 1 if index % 2 == 0 else -1

            fish = QuantumFish(x, direction)

            # Give each fish a different wave phase
            fish.wave_time = random.uniform(
                0,
                6.28
            )

            # Start fish in different quantum states
            initial_gates = random.randint(0, 3)

            for _ in range(initial_gates):
                fish.apply_next_gate()

            self.fish.append(fish)

        self.initialized = True

    # SPAWN NEW FISH
    def spawn_fish(self, camera):

        """
        Spawn a new fish outside the visible screen.

        Fish enter from either the left or right side,
        depending on the available world space.
        """

        if len(self.fish) >= self.max_fish:
            return

        # Calculate spawn positions outside the camera
        left_spawn = (
            camera.x - self.spawn_margin
        )

        right_spawn = (
            camera.x + WIDTH + self.spawn_margin
        )

        # Check which spawn positions are inside the world
        available_sides = []

        if left_spawn >= 0:
            available_sides.append("left")

        if right_spawn <= WORLD_WIDTH:
            available_sides.append("right")

        # No valid spawn position
        if not available_sides:
            return

        side = random.choice(available_sides)

        if side == "left":

            x = left_spawn

            # Fish enters from the left and swims right
            direction = 1

        else:

            x = right_spawn

            # Fish enters from the right and swims left
            direction = -1

        fish = QuantumFish(x, direction)

        # Randomize the initial quantum state
        initial_gates = random.randint(0, 3)

        for _ in range(initial_gates):
            fish.apply_next_gate()

        self.fish.append(fish)

    # UPDATE FISH
    def update(self, dt, camera, world=None):

        # INITIAL POPULATION
        if not self.initialized:
            self.spawn_initial_fish(camera)

        # SPAWN TIMER
        self.spawn_timer += dt

        if self.spawn_timer >= self.next_spawn:

            self.spawn_timer = 0.0

            self.next_spawn = random.uniform(
                self.spawn_min,
                self.spawn_max
            )

            if len(self.fish) < self.max_fish:
                self.spawn_fish(camera)

        # UPDATE ACTIVE FISH
        for fish in self.fish:

            # Update movement, animation and quantum state
            fish.update(dt)

            # Adjust flying height near ice obstacles
            if world is not None:
                fish.update_flying_height(dt, world)

        # REMOVE DISTANT FISH
        # Fish are removed only after their entire sprite
        # has moved beyond the camera view plus a margin.
        left_limit = (
            camera.x - self.despawn_margin
        )

        right_limit = (
            camera.x + WIDTH + self.despawn_margin
        )

        self.fish = [
            fish
            for fish in self.fish
            if (
                fish.x + fish.FISH_SIZE[0] >= left_limit
                and fish.x <= right_limit
            )
        ]

    # DRAW FISH
    def draw(self, screen, camera):

        """
        Draw all active fish.

        Each fish is responsible for rendering its
        ice and water quantum projections.
        """

        for fish in self.fish:
            fish.draw(screen, camera)

    # FISH CATCHING
    def try_catch(self, player, layer, is_superposition=False):
        """
        Catch fish based on the player's quantum state.

        In superposition, the penguin can catch a nearby fish
        regardless of which layer the fish collapses into.
        """

        from settings import (
            ICE_TOP,
            ICE_BOTTOM,
            WATER_TOP,
            WATER_BOTTOM
        )

        catch_range = 110

        ice_height = ICE_BOTTOM - ICE_TOP
        water_height = WATER_BOTTOM - WATER_TOP

        player_x = player.x + player.width / 2

        if layer == 0:
            relative_y = (player.y - ICE_TOP) / ice_height
        else:
            relative_y = (player.y - WATER_TOP) / water_height

        relative_y = max(0.0, min(1.0, relative_y))

        nearest_fish = None
        nearest_distance = catch_range

        # Find the nearest fish.
        for fish in self.fish:

            # Check both layers in superposition.
            if is_superposition:
                layers_to_check = (0, 1)
            else:
                layers_to_check = (layer,)

            for current_layer in layers_to_check:

                if current_layer == 0:
                    projected_y = ICE_TOP + relative_y * ice_height
                    probability = abs(fish.alpha) ** 2
                else:
                    projected_y = WATER_TOP + relative_y * water_height
                    probability = abs(fish.beta) ** 2

                if probability <= 1e-9:
                    continue

                player_y = projected_y + player.height / 2

                fish_x, fish_y = fish.get_position(
                    current_layer
                )

                distance = math.hypot(
                    fish_x - player_x,
                    fish_y - player_y
                )

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_fish = fish

        if nearest_fish is None:
            return "none"

        # Measure the fish using the Born rule.
        measurement = nearest_fish.measure()

        if is_superposition:
            # Both penguin projections are available.
            self.fish.remove(nearest_fish)
            return "caught"

        # Normal mode: the fish must collapse
        # into the penguin's current layer.
        if measurement == layer:
            self.fish.remove(nearest_fish)
            return "caught"

        return "missed"