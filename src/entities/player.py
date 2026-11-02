import math
import pygame

from settings import (
    WIDTH,
    WORLD_WIDTH,
    PENGUIN_WIDTH,
    PENGUIN_HEIGHT,
    PENGUIN_SPEED,
    ICE_TOP,
    ICE_BOTTOM,
    WATER_TOP,
    WATER_BOTTOM
)


class Player:
    def __init__(self):

        # PLAYER SETTINGS
        self.width = PENGUIN_WIDTH
        self.height = PENGUIN_HEIGHT
        self.speed = PENGUIN_SPEED

        self.x = 330
        self.y = 1050

        # ANIMATION SETTINGS
        self.direction = "down"
        self.moving = False

        self.animation_frame = 0
        self.animation_timer = 0

        self.walk_animation_speed = 10
        self.swim_animation_speed = 12

        # SWIMMING EFFECT
        self.swim_time = 0

        # How many pixels for penguin floating
        self.swim_bob_amplitude = 3

        # Swinging speed
        self.swim_bob_speed = 0.06

        # WALK ANIMATIONS
        self.walk_animations = {
            "down": self.load_frames("walk_down"),
            "up": self.load_frames("walk_up"),
            "right": self.load_frames("walk_side")
        }

        self.walk_animations["left"] = [
            pygame.transform.flip(frame, True, False)
            for frame in self.walk_animations["right"]
        ]

        # SIDE IDLE
        self.idle_side = self.load_image(
            "assets/penguin/idle_side.png"
        )

        self.idle_side_left = pygame.transform.flip(
            self.idle_side,
            True,
            False
        )

        # SWIM ANIMATIONS
        self.swim_frames = self.load_frames("swim")

        # INITIAL IMAGE
        self.image = self.walk_animations["down"][0]
        self.mask = pygame.mask.from_surface(self.image)

        # Attēla nobīde attiecībā pret spēlētāja centru
        self.mask_offset_x = 0
        self.mask_offset_y = 0

    # LOAD IMAGE
    def load_image(self, path):

        image = pygame.image.load(
            path
        ).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (self.width, self.height)
        )

        return image

    # LOAD ANIMATION FRAMES
    def load_frames(self, name):

        frames = []

        for i in (1, 2):

            image = self.load_image(
                f"assets/penguin/{name}_{i}.png"
            )

            frames.append(image)

        return frames

    # SWIMMING DIRECTION
    def get_swim_image(self, frame):

        if self.direction == "up":
            return frame

        if self.direction == "up_right":
            return pygame.transform.rotate(
                frame,
                -45
            )

        if self.direction == "right":
            return pygame.transform.rotate(
                frame,
                -90
            )

        if self.direction == "down_right":
            return pygame.transform.rotate(
                frame,
                -135
            )

        if self.direction == "down":
            return pygame.transform.rotate(
                frame,
                180
            )

        # For left side flip image
        flipped = pygame.transform.flip(
            frame,
            True,
            False
        )

        if self.direction == "up_left":
            return pygame.transform.rotate(
                flipped,
                45
            )

        if self.direction == "left":
            return pygame.transform.rotate(
                flipped,
                90
            )

        if self.direction == "down_left":
            return pygame.transform.rotate(
                flipped,
                135
            )

        return frame

    # UPDATE ANIMATION
    def update_animation(self, quantum_state):

        # ANIMATION SPEED
        if quantum_state == 0:
            animation_speed = self.walk_animation_speed
        else:
            animation_speed = self.swim_animation_speed

        # FRAME TIMER
        if self.moving:

            self.animation_timer += 1

            if self.animation_timer >= animation_speed:

                self.animation_timer = 0

                self.animation_frame = (
                    1 - self.animation_frame
                )

        else:

            self.animation_frame = 0
            self.animation_timer = 0

        # ICE ANIMATION
        if quantum_state == 0:

            if self.direction in (
                "up_right",
                "down_right"
            ):
                self.direction = "right"

            elif self.direction in (
                "up_left",
                "down_left"
            ):
                self.direction = "left"

            if not self.moving:

                if self.direction == "right":
                    self.image = self.idle_side

                elif self.direction == "left":
                    self.image = self.idle_side_left

                else:
                    self.image = self.walk_animations[
                        self.direction
                    ][0]

            else:

                self.image = self.walk_animations[
                    self.direction
                ][self.animation_frame]

        # WATER ANIMATION
        else:

            frame = self.swim_frames[
                self.animation_frame
            ]

            self.image = self.get_swim_image(
                frame
            )

            self.swim_time += 1

        # UPDATE COLLISION MASK
        self.mask = pygame.mask.from_surface(
            self.image
        )

        self.mask_offset_x = (
            self.width - self.image.get_width()
        ) // 2

        self.mask_offset_y = (
            self.height - self.image.get_height()
        ) // 2

    def get_ice_collision_mask(self):
        """
        Returns the collision mask for the ice projection.
        """

        direction = self.direction

        if direction in ("up_right", "down_right"):
            direction = "right"
        elif direction in ("up_left", "down_left"):
            direction = "left"

        if direction not in self.walk_animations:
            direction = "down"

        if not self.moving:
            if direction == "right":
                image = self.idle_side
            elif direction == "left":
                image = self.idle_side_left
            else:
                image = self.walk_animations[direction][0]
        else:
            image = self.walk_animations[direction][self.animation_frame]

        return pygame.mask.from_surface(image)

    # PLAYER MOVEMENT
    def move(self, keys, quantum_state):

        old_x = self.x
        old_y = self.y

        dx = 0
        dy = 0

        # KEY INPUT
        if keys[pygame.K_LEFT]:
            dx -= self.speed

        if keys[pygame.K_RIGHT]:
            dx += self.speed

        if keys[pygame.K_UP]:
            dy -= self.speed

        if keys[pygame.K_DOWN]:
            dy += self.speed

        self.moving = (
            dx != 0 or dy != 0
        )

        # DIRECTION
        if quantum_state == 1:

            # 8 directions in water
            if dx > 0 and dy < 0:
                self.direction = "up_right"

            elif dx < 0 and dy < 0:
                self.direction = "up_left"

            elif dx > 0 and dy > 0:
                self.direction = "down_right"

            elif dx < 0 and dy > 0:
                self.direction = "down_left"

            elif dx > 0:
                self.direction = "right"

            elif dx < 0:
                self.direction = "left"

            elif dy < 0:
                self.direction = "up"

            elif dy > 0:
                self.direction = "down"

        else:

            # 4 directions on ice
            if dx > 0:
                self.direction = "right"

            elif dx < 0:
                self.direction = "left"

            elif dy < 0:
                self.direction = "up"

            elif dy > 0:
                self.direction = "down"

        # APPLY MOVEMENT
        self.x += dx
        self.y += dy

        # WORLD BOUNDARIES
        self.x = max(
            0,
            min(
                self.x,
                WORLD_WIDTH - self.width
            )
        )

        if quantum_state == 0:

            self.y = max(
                ICE_TOP,
                min(
                    self.y,
                    ICE_BOTTOM - self.height
                )
            )

        else:

            self.y = max(
                WATER_TOP,
                min(
                    self.y,
                    WATER_BOTTOM - self.height
                )
            )

        # UPDATE ANIMATION
        self.update_animation(
            quantum_state
        )

        return (
            old_x,
            old_y,
            self.x,
            self.y
        )

    # GET RECT
    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    # SET POSITION
    def set_position(self, x, y):

        self.x = x
        self.y = y

    # DRAW PLAYER
    def draw(self, screen, camera, quantum_state):

        image_rect = self.image.get_rect()
        player_rect = self.get_rect()

        image_rect.center = player_rect.center

        # SWIMMING BOB EFFECT
        if quantum_state == 1:

            bob_offset = math.sin(
                self.swim_time * self.swim_bob_speed
            ) * self.swim_bob_amplitude

            image_rect.y += round(bob_offset)

        # DRAW
        screen.blit(
            self.image,
            (
                camera.apply_x(image_rect.x),
                camera.apply_y(image_rect.y)
            )
        )

    def draw_projection(self, screen, camera, target_layer, alpha=120):
        """
        Draws a translucent penguin projection
        in the specified world layer.
        """

        ice_height = ICE_BOTTOM - ICE_TOP
        water_height = WATER_BOTTOM - WATER_TOP

        # Calculate the relative vertical position.
        if ICE_TOP <= self.y < ICE_BOTTOM:
            relative_y = (self.y - ICE_TOP) / ice_height
        else:
            relative_y = (self.y - WATER_TOP) / water_height

        relative_y = max(0.0, min(1.0, relative_y))

        # Map the position to the target layer.
        if target_layer == 0:
            projection_y = ICE_TOP + relative_y * ice_height
        else:
            projection_y = WATER_TOP + relative_y * water_height

        # Choose an animation frame for the target layer.
        if target_layer == 0:
            direction = self.direction

            if direction in ("up_right", "down_right"):
                direction = "right"
            elif direction in ("up_left", "down_left"):
                direction = "left"

            if direction not in self.walk_animations:
                direction = "down"

            if not self.moving:
                if direction == "right":
                    image = self.idle_side
                elif direction == "left":
                    image = self.idle_side_left
                else:
                    image = self.walk_animations[direction][0]
            else:
                image = self.walk_animations[direction][self.animation_frame]

        else:
            frame = self.swim_frames[self.animation_frame]
            image = self.get_swim_image(frame)

        # Create a transparent copy.
        projection_image = image.copy()
        projection_image.set_alpha(alpha)

        # Center the projection on its logical position.
        image_rect = projection_image.get_rect()

        image_rect.center = (
            self.x + self.width / 2,
            projection_y + self.height / 2
        )

        screen.blit(
            projection_image,
            (
                camera.apply_x(image_rect.x),
                camera.apply_y(image_rect.y)
            )
        )