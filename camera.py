from settings import WIDTH, HEIGHT, WORLD_WIDTH, WORLD_HEIGHT


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, player_x, player_y, player_width, player_height):
        # Center camera on player
        self.x = (
            player_x
            - WIDTH // 2
            + player_width // 2
        )

        self.y = (
            player_y
            - HEIGHT // 2
            + player_height // 2
        )

        # Keep camera inside world
        self.x = max(
            0,
            min(self.x, WORLD_WIDTH - WIDTH)
        )

        self.y = max(
            0,
            min(self.y, WORLD_HEIGHT - HEIGHT)
        )

    def apply_x(self, world_x):
        return world_x - self.x

    def apply_y(self, world_y):
        return world_y - self.y