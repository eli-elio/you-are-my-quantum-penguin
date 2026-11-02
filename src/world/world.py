import math
import pygame

from settings import (
    WORLD_WIDTH,
    ICE_BOTTOM,
    WATER_TOP
)

class World:
    def __init__(self):

        # IMAGES
        self.ice_cliff_image = pygame.image.load(
            "assets/objects/ice_cliff.png"
        ).convert_alpha()

        self.ice_edge_image = pygame.image.load(
            "assets/objects/ice_edge.png"
        ).convert_alpha()

        self.ice_edge_image = pygame.transform.smoothscale(
            self.ice_edge_image,
            (
                WORLD_WIDTH,
                WATER_TOP - ICE_BOTTOM
            )
        )

        # Home and partner assets
        self.home_image = pygame.image.load(
            "assets/objects/home.png"
        ).convert_alpha()

        self.partner_image = pygame.image.load(
            "assets/penguin/partner.png"
        ).convert_alpha()

        # Resize home while preserving its original proportions
        home_width = 340

        original_width, original_height = self.home_image.get_size()
        home_height = round(
            original_height * home_width / original_width
        )

        self.home_image = pygame.transform.smoothscale(
            self.home_image,
            (home_width, home_height)
        )

        # Resize partner
        self.partner_image = pygame.transform.smoothscale(
            self.partner_image,
            (70, 90)
        )

        # Home position
        self.home_x = 100
        self.home_y = 1100 - home_height

        # Partner stands near the igloo entrance
        self.partner_x = 260
        self.partner_y = 1050

        # Pixel-perfect collision masks
        self.home_mask = pygame.mask.from_surface(
            self.home_image
        )

        self.partner_mask = pygame.mask.from_surface(
            self.partner_image
        )

        # Home and partner collision objects
        self.home_obstacle = {
            "x": self.home_x,
            "y": self.home_y,
            "width": self.home_image.get_width(),
            "height": self.home_image.get_height(),
            "image": self.home_image,
            "mask": self.home_mask,
        }

        self.partner_obstacle = {
            "x": self.partner_x,
            "y": self.partner_y,
            "width": self.partner_image.get_width(),
            "height": self.partner_image.get_height(),
            "image": self.partner_image,
            "mask": self.partner_mask,
        }

        # ICE OBSTACLES
        self.ice_obstacles = [
            self.create_ice_obstacle(1200, 900, 120, 300),
            self.create_ice_obstacle(1700, 750, 500, 120),
            self.create_ice_obstacle(2500, 950, 250, 300),
            self.create_ice_obstacle(3100, 650, 600, 150),
        ]

        # QUANTUM PHASE BARRIER
        self.quantum_barrier = pygame.Rect(
            1050,
            0,
            35,
            0
        )

        self.barrier_open = False

        self.barrier_time = 0.0


    def create_ice_obstacle(
        self,
        x,
        y,
        width,
        height
    ):
        # Scale cliff image to obstacle size
        image = pygame.transform.smoothscale(
            self.ice_cliff_image,
            (width, height)
        )

        # Create pixel-perfect mask
        mask = pygame.mask.from_surface(image)

        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "image": image,
            "mask": mask
        }


    def masks_collide(
        self,
        player,
        obstacle,
        player_x=None,
        player_y=None,
        player_mask=None
    ):
        # Use current player position unless
        # another position was supplied
        if player_x is None:
            player_x = player.x

        if player_y is None:
            player_y = player.y

        # Position of obstacle relative to player
        offset_x = int(
            obstacle["x"] - player_x
        )

        offset_y = int(
            obstacle["y"] - player_y
        )

        # Check if opaque pixels overlap
        if player_mask is None:
            player_mask = player.mask

        overlap = player_mask.overlap(
            obstacle["mask"],
            (offset_x, offset_y)
        )

        return overlap is not None

    def collision_overlap_area(
            self,
            player,
            obstacle,
            x,
            y,
            player_mask=None
    ):
        if player_mask is None:
            player_mask = player.mask

        offset_x = int(obstacle["x"] - x)
        offset_y = int(obstacle["y"] - y)

        return player_mask.overlap_area(
            obstacle["mask"],
            (offset_x, offset_y)
        )

    def update_barrier_animation(self, dt):
        """
        Update the barrier's animation timer.
        """
        self.barrier_time += dt

    def update_quantum_barrier(self, qubit):
        """
        Open the barrier only in the |-> state.
        """

        self.barrier_open = (
            qubit.get_state_name() == "|-> SUPERPOSITION"
        )

    def barrier_collides(self, player, x, y, layer):
        """
        Check collision with the quantum barrier.

        The barrier blocks the entire world height
        unless the penguin is in the |-> state.
        """

        if self.barrier_open:
            return False

        from settings import (
            MOUNTAINS_BOTTOM,
            WORLD_HEIGHT
        )

        barrier_rect = pygame.Rect(
            self.quantum_barrier.x,
            MOUNTAINS_BOTTOM,
            self.quantum_barrier.width,
            WORLD_HEIGHT - MOUNTAINS_BOTTOM
        )

        player_rect = pygame.Rect(
            int(x),
            int(y),
            player.width,
            player.height
        )

        return player_rect.colliderect(
            barrier_rect
        )

    def draw_quantum_barrier(self, screen, camera, layer):
        """
        Draw a softly glowing golden quantum barrier.
        """

        from settings import (
            MOUNTAINS_BOTTOM,
            WORLD_HEIGHT
        )

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        barrier_width = self.quantum_barrier.width

        screen_x = int(
            camera.apply_x(self.quantum_barrier.x)
        )

        # Skip drawing when the barrier is off-screen.
        if (
                screen_x + barrier_width < 0
                or screen_x > screen_width
        ):
            return

        # The barrier starts below the mountains.
        screen_top = int(
            camera.apply_y(MOUNTAINS_BOTTOM)
        )

        screen_bottom = int(
            camera.apply_y(WORLD_HEIGHT)
        )

        visible_top = max(0, screen_top)
        visible_bottom = min(screen_height, screen_bottom)

        if visible_bottom <= visible_top:
            return

        visible_height = visible_bottom - visible_top

        # Smooth pulsing animation.
        pulse = (
                        math.sin(self.barrier_time * 2.5) + 1.0
                ) / 2.0

        if self.barrier_open:
            base_alpha = 30
            glow_alpha = 12
        else:
            base_alpha = int(110 + 65 * pulse)
            glow_alpha = int(18 + 30 * pulse)

        # SOFT OUTER GLOW
        glow_width = barrier_width + 60

        glow_surface = pygame.Surface(
            (glow_width, visible_height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (255, 215, 80, glow_alpha),
            glow_surface.get_rect(),
            border_radius=15
        )

        screen.blit(
            glow_surface,
            (
                screen_x - 30,
                visible_top
            )
        )

        # MAIN GOLDEN BARRIER
        barrier_surface = pygame.Surface(
            (barrier_width, visible_height),
            pygame.SRCALPHA
        )

        barrier_surface.fill(
            (255, 205, 60, base_alpha)
        )

        screen.blit(
            barrier_surface,
            (
                screen_x,
                visible_top
            )
        )

        # BRIGHT INNER CORE
        core_width = 6

        core_surface = pygame.Surface(
            (core_width, visible_height),
            pygame.SRCALPHA
        )

        core_alpha = (
            35 if self.barrier_open
            else int(75 + 65 * pulse)
        )

        core_surface.fill(
            (255, 250, 190, core_alpha)
        )

        screen.blit(
            core_surface,
            (
                screen_x + (barrier_width - core_width) // 2,
                visible_top
            )
        )

        # REQUIRED QUANTUM STATE LABEL
        font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

        label = font.render(
            "|->",
            True,
            (255, 245, 200)
        )

        label_rect = label.get_rect(
            center=(
                screen_x + barrier_width // 2,
                visible_top + 35
            )
        )

        # Dark brown background for contrast.
        label_background = label_rect.inflate(
            16,
            10
        )

        pygame.draw.rect(
            screen,
            (95, 65, 25),
            label_background,
            border_radius=8
        )

        screen.blit(
            label,
            label_rect
        )

    def get_ice_obstacles(self):
        return (
                self.ice_obstacles
                + [self.home_obstacle, self.partner_obstacle]
        )

    def collision_is_worse(self, player, obstacle, old_x, old_y,
                           new_x, new_y, player_mask=None):
        """Block a move only when it increases opaque-pixel overlap."""
        old_area = self.collision_overlap_area(
            player, obstacle, old_x, old_y, player_mask
        )
        new_area = self.collision_overlap_area(
            player, obstacle, new_x, new_y, player_mask
        )
        return new_area > old_area

    def barrier_overlap_area(self, player, x, y):
        """Measure overlap with the closed barrier rectangle."""
        if self.barrier_open:
            return 0

        from settings import MOUNTAINS_BOTTOM, WORLD_HEIGHT

        barrier = pygame.Rect(
            self.quantum_barrier.x,
            MOUNTAINS_BOTTOM,
            self.quantum_barrier.width,
            WORLD_HEIGHT - MOUNTAINS_BOTTOM,
        )
        player_rect = pygame.Rect(
            int(x), int(y), player.width, player.height
        )
        intersection = player_rect.clip(barrier)
        return intersection.width * intersection.height

    def barrier_move_is_worse(self, player, old_x, old_y, new_x, new_y):
        return (
            self.barrier_overlap_area(player, new_x, new_y)
            > self.barrier_overlap_area(player, old_x, old_y)
        )

    def handle_collision(self, player, old_x, old_y,
                         new_x, new_y, quantum_state):
        # Resolve horizontal movement first.
        player.x = new_x
        player.y = old_y

        blocked_x = self.barrier_move_is_worse(
            player, old_x, old_y, new_x, old_y
        )
        if quantum_state == 0:
            for obstacle in self.get_ice_obstacles():
                if self.collision_is_worse(
                    player, obstacle, old_x, old_y, new_x, old_y
                ):
                    blocked_x = True
                    break

        if blocked_x:
            player.x = old_x

        # Resolve vertical movement using the accepted horizontal position.
        accepted_x = player.x
        player.y = new_y

        blocked_y = self.barrier_move_is_worse(
            player, accepted_x, old_y, accepted_x, new_y
        )
        if quantum_state == 0:
            for obstacle in self.get_ice_obstacles():
                if self.collision_is_worse(
                    player, obstacle, accepted_x, old_y,
                    accepted_x, new_y
                ):
                    blocked_y = True
                    break

        if blocked_y:
            player.y = old_y

    def handle_superposition_collision(self, player, old_x, old_y,
                                       new_x, new_y, active_layer):
        """Check both projections; ice obstacles use the ice projection."""
        from settings import ICE_TOP, ICE_BOTTOM, WATER_TOP, WATER_BOTTOM

        ice_mask = player.get_ice_collision_mask()
        ice_height = ICE_BOTTOM - ICE_TOP
        water_height = WATER_BOTTOM - WATER_TOP

        def get_ice_y(y):
            if active_layer == 0:
                return y
            relative_y = (y - WATER_TOP) / water_height
            return ICE_TOP + relative_y * ice_height

        old_ice_y = get_ice_y(old_y)
        new_ice_y = get_ice_y(new_y)

        # Resolve horizontal movement.
        player.x = new_x
        player.y = old_y

        blocked_x = self.barrier_move_is_worse(
            player, old_x, old_y, new_x, old_y
        )
        for obstacle in self.get_ice_obstacles():
            if self.collision_is_worse(
                player, obstacle, old_x, old_ice_y,
                new_x, old_ice_y, player_mask=ice_mask
            ):
                blocked_x = True
                break

        if blocked_x:
            player.x = old_x

        # Resolve vertical movement.
        accepted_x = player.x
        player.y = new_y

        blocked_y = self.barrier_move_is_worse(
            player, accepted_x, old_y, accepted_x, new_y
        )
        for obstacle in self.get_ice_obstacles():
            if self.collision_is_worse(
                player, obstacle, accepted_x, old_ice_y,
                accepted_x, new_ice_y, player_mask=ice_mask
            ):
                blocked_y = True
                break

        if blocked_y:
            player.y = old_y

    def resolve_layer_switch(self, player, new_y):
        """Find a nearby clear position when entering the ice layer."""
        obstacles = self.get_ice_obstacles()

        def position_is_clear(x):
            return all(
                not self.masks_collide(player, obstacle, x, new_y)
                for obstacle in obstacles
            ) and not self.barrier_collides(player, x, new_y, 0)

        if position_is_clear(player.x):
            return

        # Search to the left and right, keeping the player in world bounds.
        start_x = player.x
        for distance in range(1, WORLD_WIDTH + 1):
            for candidate_x in (start_x - distance, start_x + distance):
                if 0 <= candidate_x <= WORLD_WIDTH - player.width:
                    if position_is_clear(candidate_x):
                        player.x = candidate_x
                        return

        # Extremely unlikely fallback: retain the current x position.

    def draw(
            self,
            screen,
            camera,
            quantum_state
    ):

        # ICE EDGE
        screen.blit(
            self.ice_edge_image,
            (
                camera.apply_x(0),
                camera.apply_y(ICE_BOTTOM)
            )
        )

        # ICE OBSTACLES
        if quantum_state == 0:

            for obstacle in self.get_ice_obstacles():
                screen.blit(
                    obstacle["image"],
                    (
                        camera.apply_x(
                            obstacle["x"]
                        ),
                        camera.apply_y(
                            obstacle["y"]
                        )
                    )
                )

        # QUANTUM PHASE BARRIER
        self.draw_quantum_barrier(
            screen,
            camera,
            quantum_state
        )

