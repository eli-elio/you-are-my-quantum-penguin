import pygame

from settings import *
from src.camera import Camera
from src.player import Player
from src.world import World
from src.background import Background
from src.fish_manager import FishManager
from src.quantum_state import QuantumState
from src.split_screen import SplitScreenCamera

# INITIALIZATION
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You Are My Quantum Penguin")

clock = pygame.time.Clock()

# GAME OBJECTS
camera = Camera()
player = Player()
ice_camera = SplitScreenCamera(0, player)
water_camera = SplitScreenCamera(1, player)
world = World()
background = Background()
fish_manager = FishManager()

# GAME STATE
# Penguin quantum state
penguin_qubit = QuantumState()

# Current physical layer used by movement and rendering
# 0 = ice, 1 = water
quantum_state = 0

# Fish are the resource used to activate quantum gates.
fish_count = 0

# Quantum gate costs
X_COST = 1
H_COST = 2
Z_COST = 3

# HUD
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

# HELPER FUNCTIONS
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

    # ICE TO WATER
    if current_state == 0:

        relative_y = (
            player.y - ICE_TOP
        ) / ice_height

        player.y = (
            WATER_TOP
            + relative_y * water_height
        )

        return 1

    # WATER TO ICE
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

def sync_physical_layer(player, world, current_layer, qubit):
    """
    Synchronize the player's physical layer with the qubit.

    Only changes the physical layer when the quantum
    state is no longer in superposition.
    """

    probability_ice, probability_water = (
        qubit.get_probabilities()
    )

    tolerance = 1e-9

    # The penguin is in superposition.
    if (
        probability_ice > tolerance
        and probability_water > tolerance
    ):
        return current_layer

    # Determine the physical layer from the qubit.
    if probability_ice > 1 - tolerance:
        target_layer = 0
    else:
        target_layer = 1

    # The penguin is already in the correct layer.
    if target_layer == current_layer:
        return current_layer

    # Move the penguin to the correct world layer.
    return switch_layer(
        player,
        world,
        current_layer
    )

def draw_split_screen(screen, player, world, background, fish_manager):
    half_height = HEIGHT // 2

    ice_camera.update(player)
    water_camera.update(player)

    # ICE VIEW
    ice_surface = pygame.Surface((WIDTH, half_height))
    ice_surface.fill((190, 225, 240))

    background.draw(ice_surface, ice_camera)
    world.draw(ice_surface, ice_camera, 0)
    fish_manager.draw(ice_surface, ice_camera)

    if ICE_TOP <= player.y < ICE_BOTTOM:
        player.draw(ice_surface, ice_camera, 0)
    else:
        player.draw_projection(
            ice_surface,
            ice_camera,
            0,
            alpha=180
        )

    screen.blit(ice_surface, (0, 0))

    # WATER VIEW
    water_surface = pygame.Surface((WIDTH, half_height))
    water_surface.fill((40, 100, 140))

    background.draw(water_surface, water_camera)
    world.draw(water_surface, water_camera, 1)
    fish_manager.draw(water_surface, water_camera)

    if WATER_TOP <= player.y < WATER_BOTTOM:
        player.draw(water_surface, water_camera, 1)
    else:
        player.draw_projection(
            water_surface,
            water_camera,
            1,
            alpha=180
        )

    screen.blit(water_surface, (0, half_height))

    # DIVIDER
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0, half_height),
        (WIDTH, half_height),
        4
    )

# MAIN GAME LOOP
running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # X GATE: SWITCH QUANTUM LAYER
            if event.key == pygame.K_x:
                probability_ice, probability_water = penguin_qubit.get_probabilities()

                is_superposition = (
                        probability_ice > 1e-9
                        and probability_water > 1e-9
                )

                if is_superposition:
                    show_message("X in superposition is coming soon!")

                elif fish_count >= X_COST:
                    penguin_qubit.apply_x()

                    quantum_state = switch_layer(
                        player,
                        world,
                        quantum_state
                    )

                    fish_count -= X_COST
                    show_message("X gate activated! -1 fish")

                else:
                    show_message("Not enough fish for X gate!")

            # CATCH FISH
            elif event.key == pygame.K_e:

                probability_ice, probability_water = (
                    penguin_qubit.get_probabilities()
                )

                is_superposition = (
                        probability_ice > 1e-9
                        and probability_water > 1e-9
                )

                result = fish_manager.try_catch(
                    player,
                    quantum_state,
                    is_superposition
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

            # H GATE: HADAMARD
            elif event.key == pygame.K_h:

                if fish_count >= H_COST:

                    # Apply the Hadamard gate.
                    penguin_qubit.apply_h()

                    # Synchronize the physical layer
                    # if the result is a basis state.
                    quantum_state = sync_physical_layer(
                        player,
                        world,
                        quantum_state,
                        penguin_qubit
                    )

                    fish_count -= H_COST

                    show_message(
                        "H gate activated! -2 fish"
                    )

                else:
                    show_message(
                        "Not enough fish for H gate!"
                    )

            # Z GATE: PHASE FLIP
            elif event.key == pygame.K_z:

                probability_ice, probability_water = (
                    penguin_qubit.get_probabilities()
                )

                is_superposition = (
                        probability_ice > 1e-9
                        and probability_water > 1e-9
                )

                if not is_superposition:
                    show_message(
                        "Z gate requires superposition!"
                    )

                elif fish_count < Z_COST:
                    show_message(
                        "Not enough fish for Z gate!"
                    )

                else:
                    penguin_qubit.apply_z()

                    fish_count -= Z_COST

                    show_message(
                        "Z gate activated! -3 fish"
                    )

    # PLAYER MOVEMENT
    keys = pygame.key.get_pressed()

    old_x, old_y, new_x, new_y = player.move(
        keys,
        quantum_state
    )

    probability_ice, probability_water = (
        penguin_qubit.get_probabilities()
    )

    is_superposition = (
            probability_ice > 1e-9
            and probability_water > 1e-9
    )

    # COLLISION
    if is_superposition:
        world.handle_superposition_collision(
            player,
            old_x,
            old_y,
            new_x,
            new_y,
            quantum_state
        )
    else:
        world.handle_collision(
            player,
            old_x,
            old_y,
            new_x,
            new_y,
            quantum_state
        )

    # CAMERA
    camera.update(
        player.x,
        player.y,
        player.width,
        player.height
    )

    # FISH UPDATE
    fish_manager.update(
        dt,
        camera,
        world
    )

    # MESSAGE TIMER
    if message_timer > 0:

        message_timer -= dt

        if message_timer <= 0:

            message_timer = 0
            message = ""

    #DRAW
    probability_ice, probability_water = (
        penguin_qubit.get_probabilities()
    )

    is_superposition = (
            probability_ice > 1e-9
            and probability_water > 1e-9
    )

    if is_superposition:
        draw_split_screen(
            screen,
            player,
            world,
            background,
            fish_manager
        )
    else:
        screen.fill((190, 225, 240))

        background.draw(screen, camera)
        world.draw(screen, camera, quantum_state)
        fish_manager.draw(screen, camera)
        player.draw(screen, camera, quantum_state)

    # DRAW HUD
    # HUD BACKGROUND
    hud_background = pygame.Surface(
        (370, 135),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        hud_background,
        (25, 40, 60, 185),
        hud_background.get_rect(),
        border_radius=15
    )

    screen.blit(
        hud_background,
        (10, 10)
    )

    # FISH ICON
    screen.blit(
        fish_icon,
        (20, 20)
    )

    # FISH COUNT
    fish_text = hud_font.render(
        str(fish_count),
        True,
        (255, 255, 255)
    )

    screen.blit(
        fish_text,
        (85, 23)
    )

    # GATE COSTS
    gate_text = message_font.render(
        "X: 1 fish   H: 2 fish   Z: 3 fish",
        True,
        (255, 255, 255)
    )

    screen.blit(
        gate_text,
        (20, 60)
    )

    # QUANTUM STATE
    state_text = message_font.render(
        penguin_qubit.get_state_name(),
        True,
        (255, 255, 255)
    )

    screen.blit(
        state_text,
        (20, 95)
    )

    #INTERACTION MESSAGE
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

    # DISPLAY UPDATE
    pygame.display.flip()


pygame.quit()