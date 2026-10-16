import math
import random
import pygame

from settings import (
    ICE_TOP,
    ICE_BOTTOM,
    WATER_TOP,
    WATER_BOTTOM
)


class QuantumFish:

    FISH_SIZE = (75, 50)

    FISH_VARIANTS = [
        ("fish_1.png", "fish_2.png"),
        ("fish_1_1.png", "fish_2_2.png"),
        ("fish_1_1_1.png", "fish_2_2_2.png")
    ]

    def __init__(self, x, direction):

        # ---------------- POSITION ----------------

        self.x = float(x)

        # Shared relative Y position for both quantum layers
        self.relative_y = random.uniform(0.15, 0.85)

        # ---------------- MOVEMENT ----------------

        # -1 = left, 1 = right
        self.direction = direction

        # Individual swimming speed
        self.speed = random.uniform(55, 110)

        # Current vertical swimming speed
        self.vertical_speed = random.uniform(-12, 12)

        # Target vertical speed for smooth direction changes
        self.target_vertical_speed = random.uniform(-25, 25)

        # Individual direction change timer
        self.turn_timer = 0
        self.turn_interval = random.uniform(2.5, 6.0)

        # How quickly the fish adjusts its swimming angle
        self.turn_smoothness = 18

        # Gentle wave movement
        self.wave_time = random.uniform(0, math.tau)
        self.wave_speed = random.uniform(1.5, 3.0)
        self.wave_amplitude = random.uniform(3, 7)

        # ---------------- ANIMATION ----------------

        self.animation_time = 0
        self.animation_frame = 0
        self.animation_interval = random.uniform(0.12, 0.20)

        # Randomly select one of the three fish color variants
        variant = random.choice(self.FISH_VARIANTS)

        self.frames = [
            self.load_image(variant[0]),
            self.load_image(variant[1])
        ]

        # ---------------- SHADOW ----------------

        shadow_image = pygame.image.load(
            "assets/fish/fish_shadow.png"
        ).convert_alpha()

        self.shadow = pygame.transform.smoothscale(
            shadow_image,
            (65, 22)
        )

        self.shadow.set_alpha(85)

        # ---------------- QUANTUM STATE ----------------

        # Initial quantum state: |0>
        self.alpha = 1 + 0j
        self.beta = 0 + 0j

        # Each fish follows its own automatic gate sequence
        self.gates = random.choice([
            ["H", "Z", "H", "X"],
            ["X", "H", "Z", "H"],
            ["H", "X", "H", "Z"]
        ])

        self.gate_index = 0

        # Independent quantum evolution timer
        self.quantum_timer = 0
        self.quantum_interval = random.uniform(2.0, 4.0)

        # ---------------- FLYING EFFECT ----------------

        self.fly_height = random.uniform(15, 25)

        # ---------------- OBSTACLE FLYING ----------------

        self.current_fly_height = self.fly_height

        self.obstacle_extra_height = 0

        self.fly_transition_speed = 90

    # ==================================================
    # IMAGE LOADING
    # ==================================================

    def load_image(self, filename):

        image = pygame.image.load(
            f"assets/fish/{filename}"
        ).convert_alpha()

        return pygame.transform.smoothscale(
            image,
            self.FISH_SIZE
        )

    # ==================================================
    # QUANTUM GATES
    # ==================================================

    def apply_h(self):

        alpha = self.alpha
        beta = self.beta

        self.alpha = (alpha + beta) / math.sqrt(2)
        self.beta = (alpha - beta) / math.sqrt(2)

    def apply_x(self):

        self.alpha, self.beta = self.beta, self.alpha

    def apply_z(self):

        self.beta = -self.beta

    def apply_next_gate(self):

        gate = self.gates[self.gate_index]

        if gate == "H":
            self.apply_h()

        elif gate == "X":
            self.apply_x()

        elif gate == "Z":
            self.apply_z()

        self.gate_index = (
            self.gate_index + 1
        ) % len(self.gates)

    # ==================================================
    # MOVEMENT
    # ==================================================

    def update_movement(self, dt):

        # ---------------- DIRECTION CHANGES ----------------

        self.turn_timer += dt

        if self.turn_timer >= self.turn_interval:

            self.turn_timer = 0

            self.turn_interval = random.uniform(
                2.5,
                6.0
            )

            # Choose a new vertical swimming speed
            self.target_vertical_speed = random.uniform(
                -35,
                35
            )

            # Occasionally reverse horizontal direction
            if random.random() < 0.35:
                self.direction *= -1

        # ---------------- SMOOTH VERTICAL TURNING ----------------

        difference = (
            self.target_vertical_speed
            - self.vertical_speed
        )

        max_change = self.turn_smoothness * dt

        if abs(difference) <= max_change:

            self.vertical_speed = self.target_vertical_speed

        elif difference > 0:

            self.vertical_speed += max_change

        else:

            self.vertical_speed -= max_change

        # ---------------- POSITION UPDATE ----------------

        self.x += self.direction * self.speed * dt

        layer_height = WATER_BOTTOM - WATER_TOP

        self.relative_y += (
            self.vertical_speed * dt / layer_height
        )

        # ---------------- VERTICAL BOUNDARIES ----------------

        if self.relative_y < 0.12:

            self.relative_y = 0.12

            self.vertical_speed = abs(
                self.vertical_speed
            )

            self.target_vertical_speed = abs(
                self.target_vertical_speed
            )

        elif self.relative_y > 0.88:

            self.relative_y = 0.88

            self.vertical_speed = -abs(
                self.vertical_speed
            )

            self.target_vertical_speed = -abs(
                self.target_vertical_speed
            )

        # ---------------- WAVE MOVEMENT ----------------

        self.wave_time += self.wave_speed * dt

    # ==================================================
    # ANIMATION
    # ==================================================

    def update_animation(self, dt):

        self.animation_time += dt

        if self.animation_time >= self.animation_interval:

            self.animation_time = 0

            self.animation_frame = (
                1 - self.animation_frame
            )

    # ==================================================
    # QUANTUM EVOLUTION
    # ==================================================

    def update_quantum(self, dt):

        self.quantum_timer += dt

        if self.quantum_timer >= self.quantum_interval:

            self.quantum_timer = 0

            self.apply_next_gate()

            self.quantum_interval = random.uniform(
                2.0,
                4.0
            )

    # ==================================================
    # MAIN UPDATE
    # ==================================================

    def update(self, dt):

        self.update_movement(dt)

        self.update_animation(dt)

        self.update_quantum(dt)

    # ==================================================
    # POSITION IN EACH LAYER
    # ==================================================

    def get_layer_y(self, layer):

        if layer == 0:

            top = ICE_TOP
            bottom = ICE_BOTTOM

        else:

            top = WATER_TOP
            bottom = WATER_BOTTOM

        return top + self.relative_y * (
            bottom - top
        )

    # ==================================================
    # OBSTACLE FLYING
    # ==================================================

    def update_flying_height(self, dt, world):

        target_extra_height = 0

        fish_left = self.x
        fish_right = self.x + self.FISH_SIZE[0]

        # Check the area ahead of the fish
        look_ahead = 80

        if self.direction == 1:

            check_left = fish_right
            check_right = fish_right + look_ahead

        else:

            check_left = fish_left - look_ahead
            check_right = fish_left

        fish_y = self.get_layer_y(0)

        for obstacle in world.ice_obstacles:

            obstacle_left = obstacle["x"]
            obstacle_right = (
                obstacle["x"] + obstacle["width"]
            )

            obstacle_top = obstacle["y"]
            obstacle_bottom = (
                obstacle["y"] + obstacle["height"]
            )

            horizontal_overlap = (
                check_right > obstacle_left
                and check_left < obstacle_right
            )

            vertical_overlap = (
                fish_y > obstacle_top - 100
                and fish_y < obstacle_bottom + 30
            )

            if horizontal_overlap and vertical_overlap:

                target_extra_height = max(
                    target_extra_height,
                    55
                )

        # Smoothly approach the required flying height
        difference = (
            target_extra_height
            - self.obstacle_extra_height
        )

        max_change = (
            self.fly_transition_speed * dt
        )

        if abs(difference) <= max_change:

            self.obstacle_extra_height = (
                target_extra_height
            )

        elif difference > 0:

            self.obstacle_extra_height += max_change

        else:

            self.obstacle_extra_height -= max_change

    # ==================================================
    # DRAW ONE QUANTUM PROJECTION
    # ==================================================

    def draw_projection(
        self,
        screen,
        camera,
        layer,
        opacity
    ):

        if opacity <= 0:
            return

        # ---------------- SELECT ANIMATION FRAME ----------------

        image = self.frames[self.animation_frame]

        # Original sprites face left
        if self.direction == 1:

            image = pygame.transform.flip(
                image,
                True,
                False
            )

        # ---------------- ROTATE FISH ----------------

        angle = math.degrees(
            math.atan2(
                -self.vertical_speed,
                self.speed
            )
        )

        # Adjust rotation for left-facing fish
        if self.direction == -1:
            angle = -angle

        image = pygame.transform.rotate(
            image,
            angle
        )

        image = image.copy()
        image.set_alpha(opacity)

        # ---------------- WAVE OFFSET ----------------

        wave_offset = math.sin(
            self.wave_time
        ) * self.wave_amplitude

        fish_y = (
            self.get_layer_y(layer)
            + wave_offset
        )

        # ---------------- FLYING SHADOW ----------------

        if layer == 0:

            shadow_x = (
                self.x
                + self.FISH_SIZE[0] / 2
            )

            shadow_y = (
                fish_y
                + self.FISH_SIZE[1] / 2
                + 8
            )

            shadow = self.shadow.copy()

            shadow.set_alpha(
                min(85, opacity)
            )

            shadow_rect = shadow.get_rect(
                center=(
                    camera.apply_x(shadow_x),
                    camera.apply_y(shadow_y)
                )
            )

            screen.blit(
                shadow,
                shadow_rect
            )

            # Raise the fish above the ice
            fish_y -= (
                self.current_fly_height
                + self.obstacle_extra_height
            )

        # ---------------- DRAW FISH ----------------

        image_rect = image.get_rect(
            center=(
                camera.apply_x(
                    self.x + self.FISH_SIZE[0] / 2
                ),
                camera.apply_y(
                    fish_y + self.FISH_SIZE[1] / 2
                )
            )
        )

        screen.blit(
            image,
            image_rect
        )

    # ==================================================
    # DRAW BOTH QUANTUM PROJECTIONS
    # ==================================================

    def draw(self, screen, camera):

        # Quantum measurement probabilities
        p_ice = abs(self.alpha) ** 2
        p_water = abs(self.beta) ** 2

        # Convert probabilities to visual opacity
        ice_opacity = round(255 * p_ice)
        water_opacity = round(255 * p_water)

        self.draw_projection(
            screen,
            camera,
            0,
            ice_opacity
        )

        self.draw_projection(
            screen,
            camera,
            1,
            water_opacity
        )

    # ==================================================
    # QUANTUM MEASUREMENT
    # ==================================================

    def measure(self):
        """
        Measure the fish in the computational basis.

        Returns:
            0 for the ice layer
            1 for the water layer
        """

        probability_ice = abs(self.alpha) ** 2

        if random.random() < probability_ice:
            self.alpha = 1 + 0j
            self.beta = 0 + 0j

            return 0

        self.alpha = 0 + 0j
        self.beta = 1 + 0j

        return 1

    def get_position(self, layer):
        """
        Return the center of the fish projection
        in the requested layer.
        """

        fish_x = self.x + self.FISH_SIZE[0] / 2
        fish_y = self.get_layer_y(layer)

        if layer == 0:
            fish_y -= (
                    self.current_fly_height
                    + self.obstacle_extra_height
            )

        return fish_x, fish_y + self.FISH_SIZE[1] / 2