import random
import math

from quantum_fish import QuantumFish
from settings import WIDTH, WORLD_WIDTH


class FishManager:

    def __init__(self):

        # ---------------- FISH COLLECTION ----------------

        self.fish = []

        # ---------------- POPULATION SETTINGS ----------------

        self.max_fish = 8
        self.initial_fish = 5

        # ---------------- SPAWN SETTINGS ----------------

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

    # ==================================================
    # INITIAL FISH
    # ==================================================

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

    # ==================================================
    # SPAWN NEW FISH
    # ==================================================

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

    # ==================================================
    # UPDATE FISH
    # ==================================================

    def update(self, dt, camera, world=None):

        # ---------------- INITIAL POPULATION ----------------

        if not self.initialized:
            self.spawn_initial_fish(camera)

        # ---------------- SPAWN TIMER ----------------

        self.spawn_timer += dt

        if self.spawn_timer >= self.next_spawn:

            self.spawn_timer = 0.0

            self.next_spawn = random.uniform(
                self.spawn_min,
                self.spawn_max
            )

            if len(self.fish) < self.max_fish:
                self.spawn_fish(camera)

        # ---------------- UPDATE ACTIVE FISH ----------------

        for fish in self.fish:

            # Update movement, animation and quantum state
            fish.update(dt)

            # Adjust flying height near ice obstacles
            if world is not None:
                fish.update_flying_height(dt, world)

        # ---------------- REMOVE DISTANT FISH ----------------

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

    # ==================================================
    # DRAW FISH
    # ==================================================

    def draw(self, screen, camera):

        """
        Draw all active fish.

        Each fish is responsible for rendering its
        ice and water quantum projections.
        """

        for fish in self.fish:
            fish.draw(screen, camera)


    # ==================================================
    # FISH CATCHING
    # ==================================================

    def try_catch(self, player, layer):
        """
        Attempt to catch the nearest fish
        within interaction range.

        Returns:
            "caught"  - successful catch
            "missed" - measurement found the fish
                       in the opposite layer
            "none"   - no fish within range
        """

        catch_range = 110

        player_x = player.x + player.width / 2
        player_y = player.y + player.height / 2

        nearest_fish = None
        nearest_distance = catch_range

        for fish in self.fish:

            fish_x, fish_y = fish.get_position(layer)

            distance = math.hypot(
                fish_x - player_x,
                fish_y - player_y
            )

            if distance < nearest_distance:

                nearest_distance = distance
                nearest_fish = fish

        if nearest_fish is None:
            return "none"

        measurement = nearest_fish.measure()

        if measurement == layer:

            self.fish.remove(nearest_fish)

            return "caught"

        return "missed"