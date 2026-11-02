import pygame

from settings import (
    WIDTH,
    HEIGHT,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    ICE_TOP,
    ICE_BOTTOM,
    WATER_TOP,
    WATER_BOTTOM,
    MOUNTAINS_TOP
)


class SplitScreenCamera:
    def __init__(self, layer, player):
        self.x = 0
        self.y = 0

        self.layer = layer
        self.viewport_width = WIDTH
        self.viewport_height = HEIGHT // 2

        self.update(player)

    def update(self, player):
        # Keep the same horizontal position in both worlds.
        self.x = player.x - self.viewport_width // 2 + player.width // 2

        self.x = max(
            0,
            min(self.x, WORLD_WIDTH - self.viewport_width)
        )

        # Map the player's vertical position between layers.
        ice_height = ICE_BOTTOM - ICE_TOP
        water_height = WATER_BOTTOM - WATER_TOP

        if ICE_TOP <= player.y < ICE_BOTTOM:
            relative_y = (player.y - ICE_TOP) / ice_height
        else:
            relative_y = (player.y - WATER_TOP) / water_height

        relative_y = max(0.0, min(1.0, relative_y))

        if self.layer == 0:
            target_y = ICE_TOP + relative_y * ice_height
            layer_top = ICE_TOP
            layer_bottom = ICE_BOTTOM
        else:
            target_y = WATER_TOP + relative_y * water_height
            layer_top = WATER_TOP
            layer_bottom = WATER_BOTTOM

        self.y = (
                target_y
                + player.height / 2
                - self.viewport_height / 2
        )

        # Keep each viewport inside its corresponding layer.
        # Allow the camera to show scenery outside the playable layer.
        if self.layer == 0:
            camera_min_y = MOUNTAINS_TOP
            camera_max_y = ICE_BOTTOM - self.viewport_height
        else:
            camera_min_y = WATER_TOP - 100
            camera_max_y = WORLD_HEIGHT - self.viewport_height

        self.y = max(
            camera_min_y,
            min(self.y, camera_max_y)
        )

        self.y = max(
            0,
            min(self.y, WORLD_HEIGHT - self.viewport_height)
        )

    def apply_x(self, world_x):
        return world_x - self.x

    def apply_y(self, world_y):
        return world_y - self.y