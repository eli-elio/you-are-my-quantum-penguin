import pygame

from settings import (
    WORLD_WIDTH,
    MOUNTAINS_TOP,
    MOUNTAINS_BOTTOM,
    ICE_TOP,
    ICE_BOTTOM,
    WATER_TOP,
    WATER_BOTTOM
)


class Background:
    def __init__(self):

        mountains_height = (
            MOUNTAINS_BOTTOM - MOUNTAINS_TOP
        )

        ice_height = ICE_BOTTOM - ICE_TOP

        # ---------------- SKY ----------------

        sky_image = pygame.image.load(
            "assets/backgrounds/sky.png"
        ).convert()

        self.sky = pygame.transform.smoothscale(
            sky_image,
            (WORLD_WIDTH, mountains_height)
        )

        # ---------------- FAR MOUNTAINS ----------------

        far_image = pygame.image.load(
            "assets/backgrounds/far_mountains.png"
        ).convert_alpha()

        self.far_mountains = self.scale_to_height(
            far_image,
            mountains_height
        )

        # ---------------- NEAR MOUNTAINS ----------------

        near_image = pygame.image.load(
            "assets/backgrounds/near_mountains.png"
        ).convert_alpha()

        self.near_mountains = self.scale_to_height(
            near_image,
            180
        )

        # ---------------- ICE GROUND ----------------

        ice_image = pygame.image.load(
            "assets/backgrounds/ice_ground.png"
        ).convert()

        self.ice_ground = pygame.transform.smoothscale(
            ice_image,
            (WORLD_WIDTH, ice_height)
        )

        # ---------------- UNDERWATER BACKGROUND ----------------

        water_image = pygame.image.load(
            "assets/backgrounds/underwater_bg.png"
        ).convert()

        self.underwater_bg = pygame.transform.smoothscale(
            water_image,
            (
                WORLD_WIDTH,
                WATER_BOTTOM - WATER_TOP
            )
        )

    def scale_to_height(self, image, target_height):
        """
        Scale image while preserving its aspect ratio.
        """
        original_width, original_height = image.get_size()

        scale = target_height / original_height

        new_width = max(
            1,
            round(original_width * scale)
        )

        return pygame.transform.smoothscale(
            image,
            (new_width, target_height)
        )

    def draw_repeating_layer(
        self,
        screen,
        image,
        camera,
        world_y,
        parallax_factor
    ):
        image_width = image.get_width()

        offset_x = int(camera.x * parallax_factor)

        start_x = -(offset_x % image_width)

        screen_y = camera.apply_y(world_y)

        x = start_x

        while x < screen.get_width():
            screen.blit(
                image,
                (x, screen_y)
            )

            x += image_width

    def draw(self, screen, camera):

        # ---------------- SKY ----------------

        screen.blit(
            self.sky,
            (
                camera.apply_x(0),
                camera.apply_y(MOUNTAINS_TOP)
            )
        )

        # ---------------- FAR MOUNTAINS ----------------

        self.draw_repeating_layer(
            screen,
            self.far_mountains,
            camera,
            MOUNTAINS_TOP,
            0.25
        )

        # ---------------- NEAR MOUNTAINS ----------------

        self.draw_repeating_layer(
            screen,
            self.near_mountains,
            camera,
            MOUNTAINS_BOTTOM - self.near_mountains.get_height(),
            0.60
        )

        # ---------------- ICE GROUND ----------------

        screen.blit(
            self.ice_ground,
            (
                camera.apply_x(0),
                camera.apply_y(ICE_TOP)
            )
        )

        # ---------------- UNDERWATER BACKGROUND ----------------

        screen.blit(
            self.underwater_bg,
            (
                camera.apply_x(0),
                camera.apply_y(WATER_TOP)
            )
        )