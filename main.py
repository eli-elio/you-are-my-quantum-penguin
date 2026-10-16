import pygame

from settings import *
from camera import Camera
from player import Player
from world import World
from background import Background
from fish_manager import FishManager


# ==================================================
# INITIALIZATION
# ==================================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You Are My Quantum Penguin")

clock = pygame.time.Clock()


# ==================================================
# GAME OBJECTS
# ==================================================

camera = Camera()
player = Player()
world = World()
background = Background()
fish_manager = FishManager()


# ==================================================
# GAME STATE
# ==================================================

# 0 = ice
# 1 = water
quantum_state = 0

# Fish are the resource used to activate quantum gates.
fish_count = 0

# Quantum gate costs
X_COST = 1
H_COST = 2
Z_COST = 3


# ==================================================
# HUD
# ==================================================

fish_icon = pygame.image.load(
    "assets/fish/fish_1.png"
).convert_alpha()

fish_icon = pygame.transform.smoothscale(
    fish_icon,
    (54, 36)
)

hud_font = pygame.font.SysFont(
    "arial",
    30,
    bold=True
)

message_font = pygame.font.SysFont(
    "arial",
    24,
    bold=True
)

# Temporary message displayed after an interaction
message = ""
message_timer = 0.0

MESSAGE_DURATION = 1.8


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def show_message(text):
    global message, message_timer

    message = text
    message_timer = MESSAGE_DURATION


def switch_layer(player, world, current_state):
    """
    Apply the X gate by switching the penguin
    between the ice and water layers.

    Returns the new quantum state.
    """

    ice_height = ICE_BOTTOM - ICE_TOP
    water_height = WATER_BOTTOM - WATER_TOP

    # ---------------- ICE TO WATER ----------------

    if current_state == 0:

        relative_y = (
            player.y - ICE_TOP
        ) / ice_height

        player.y = (
            WATER_TOP
            + relative_y * water_height
        )

        return 1

    # ---------------- WATER TO ICE ----------------

    relative_y = (
        player.y - WATER_TOP
    ) / water_height

    new_y = (
        ICE_TOP
        + relative_y * ice_height
    )

    # Resolve collisions with ice obstacles
    world.resolve_layer_switch(
        player,
        new_y
    )

    player.y = new_y

    return 0


# ==================================================
# MAIN GAME LOOP
# ==================================================

running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ------------------------------------------
            # X GATE: SWITCH QUANTUM LAYER
            # ------------------------------------------

            if event.key == pygame.K_x:

                if fish_count >= X_COST:

                    new_state = switch_layer(
                        player,
                        world,
                        quantum_state
                    )

                    if new_state != quantum_state:

                        quantum_state = new_state
                        fish_count -= X_COST

                        show_message(
                            "X gate activated! -1 fish"
                        )

                else:

                    show_message(
                        "Not enough fish for X gate!"
                    )

            # ------------------------------------------
            # CATCH FISH
            # ------------------------------------------

            elif event.key == pygame.K_e:

                result = fish_manager.try_catch(
                    player,
                    quantum_state
                )

                if result == "caught":

                    fish_count += 1

                    show_message(
                        "Fish caught! +1 fish"
                    )

                elif result == "missed":

                    show_message(
                        "Measurement failed!"
                    )

                else:

                    show_message(
                        "No fish within reach"
                    )

            # ------------------------------------------
            # H GATE: NOT IMPLEMENTED YET
            # ------------------------------------------

            elif event.key == pygame.K_h:

                show_message(
                    "H gate coming soon!"
                )

            # ------------------------------------------
            # Z GATE: NOT IMPLEMENTED YET
            # ------------------------------------------

            elif event.key == pygame.K_z:

                show_message(
                    "Z gate coming soon!"
                )

    # ==================================================
    # PLAYER MOVEMENT
    # ==================================================

    keys = pygame.key.get_pressed()

    old_x, old_y, new_x, new_y = player.move(
        keys,
        quantum_state
    )

    # ==================================================
    # COLLISION
    # ==================================================

    world.handle_collision(
        player,
        old_x,
        old_y,
        new_x,
        new_y,
        quantum_state
    )

    # ==================================================
    # CAMERA
    # ==================================================

    camera.update(
        player.x,
        player.y,
        player.width,
        player.height
    )

    # ==================================================
    # FISH UPDATE
    # ==================================================

    fish_manager.update(
        dt,
        camera,
        world
    )

    # ==================================================
    # MESSAGE TIMER
    # ==================================================

    if message_timer > 0:

        message_timer -= dt

        if message_timer <= 0:

            message_timer = 0
            message = ""

    # ==================================================
    # DRAW
    # ==================================================

    # ---------------- CLEAR SCREEN ----------------

    screen.fill((190, 225, 240))

    # ---------------- BACKGROUND ----------------

    background.draw(
        screen,
        camera
    )

    # ---------------- WORLD ----------------

    world.draw(
        screen,
        camera,
        quantum_state
    )

    # ---------------- FISH ----------------

    fish_manager.draw(
        screen,
        camera
    )

    # ---------------- PLAYER ----------------

    player.draw(
        screen,
        camera,
        quantum_state
    )

    # ==================================================
    # DRAW HUD
    # ==================================================

    screen.blit(
        fish_icon,
        (20, 20)
    )

    fish_text = hud_font.render(
        str(fish_count),
        True,
        (255, 255, 255)
    )

    screen.blit(
        fish_text,
        (85, 23)
    )

    # ---------------- QUANTUM GATE COSTS ----------------

    gate_text = message_font.render(
        "X: 1 fish   H: 2 fish   Z: 3 fish",
        True,
        (255, 255, 255)
    )

    screen.blit(
        gate_text,
        (20, 60)
    )

    # ---------------- INTERACTION MESSAGE ----------------

    if message:

        message_surface = message_font.render(
            message,
            True,
            (255, 255, 255)
        )

        message_rect = message_surface.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT - 60
            )
        )

        # Dark background for better readability
        message_background = message_rect.inflate(
            30,
            16
        )

        pygame.draw.rect(
            screen,
            (35, 55, 75),
            message_background,
            border_radius=10
        )

        screen.blit(
            message_surface,
            message_rect
        )

    # ==================================================
    # DISPLAY UPDATE
    # ==================================================

    pygame.display.flip()


pygame.quit()