import pygame

from settings import (
    WORLD_WIDTH,
    ICE_BOTTOM,
    WATER_TOP
)


class World:
    def __init__(self):

        # ---------------- IMAGES ----------------

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


        # ---------------- ICE OBSTACLES ----------------

        self.ice_obstacles = [
            self.create_ice_obstacle(1200, 900, 120, 300),
            self.create_ice_obstacle(1700, 750, 500, 120),
            self.create_ice_obstacle(2500, 950, 250, 300),
            self.create_ice_obstacle(3100, 650, 600, 150),
        ]


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
        player_y=None
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
        overlap = player.mask.overlap(
            obstacle["mask"],
            (offset_x, offset_y)
        )

        return overlap is not None

    def handle_collision(
            self,
            player,
            old_x,
            old_y,
            new_x,
            new_y,
            quantum_state
    ):
        if quantum_state != 0:
            return

        # ---------------- X COLLISION ----------------

        player.x = new_x
        player.y = old_y

        for obstacle in self.ice_obstacles:

            if self.masks_collide(
                    player,
                    obstacle
            ):
                player.x = old_x
                break

        # ---------------- Y COLLISION ----------------

        player.y = new_y

        for obstacle in self.ice_obstacles:

            if self.masks_collide(
                    player,
                    obstacle
            ):
                player.y = old_y
                break


    def resolve_layer_switch(
        self,
        player,
        new_y
    ):
        for obstacle in self.ice_obstacles:

            # Check the FUTURE player position
            if self.masks_collide(
                player,
                obstacle,
                player.x,
                new_y
            ):

                player_center_x = (
                    player.x
                    + player.width / 2
                )

                obstacle_center_x = (
                    obstacle["x"]
                    + obstacle["width"] / 2
                )

                # Put player on left side
                if player_center_x < obstacle_center_x:

                    player.x = (
                        obstacle["x"]
                        - player.width
                    )

                # Put player on right side
                else:

                    player.x = (
                        obstacle["x"]
                        + obstacle["width"]
                    )

                break

    def draw(
            self,
            screen,
            camera,
            quantum_state
    ):

        # ---------------- ICE EDGE ----------------

        screen.blit(
            self.ice_edge_image,
            (
                camera.apply_x(0),
                camera.apply_y(ICE_BOTTOM)
            )
        )

        # ---------------- ICE OBSTACLES ----------------

        if quantum_state == 0:

            for obstacle in self.ice_obstacles:
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