import pygame

from settings import *
from src.camera import Camera
from src.player import Player
from src.world import World
from src.background import Background
from src.fish_manager import FishManager
from src.quantum_state import QuantumState
from src.split_screen import SplitScreenCamera
from src.hud import HUD
from src.quest_manager import QuestManager
from src.dialogue import Dialogue

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

# UI AND QUESTS
hud = HUD()
quests = QuestManager()
dialogue = Dialogue()


def show_message(text):
    hud.show_message(text)


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

            if event.key == pygame.K_TAB:
                hud.toggle_controls()
                continue

            if hud.controls_open:
                if event.key == pygame.K_ESCAPE:
                    hud.toggle_controls()
                continue

            # While talking, F advances one line and other keys do nothing.
            if dialogue.active:
                if event.key == pygame.K_f:
                    if dialogue.advance() and not quests.talked_to_partner:
                        quests.talk_to_partner()
                continue

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

            # TALK TO PARTNER
            elif event.key == pygame.K_f:

                # Talk to the partner when nearby in the ice layer.
                partner_center_x = world.partner_x + world.partner_image.get_width() / 2
                partner_center_y = world.partner_y + world.partner_image.get_height() / 2
                player_center_x = player.x + player.width / 2
                player_center_y = player.y + player.height / 2
                near_partner = (
                    quantum_state == 0
                    and abs(player_center_x - partner_center_x) < 135
                    and abs(player_center_y - partner_center_y) < 125
                )

                if near_partner:
                    if not quests.talked_to_partner:
                        dialogue.say([
                            ("player", "I want to explore! Maybe I'll find the perfect pebble!"),
                            ("partner", "Have fun! I'll be waiting here!"),
                        ])
                    else:
                        dialogue.say([("partner", "Welcome back! How is your adventure?")])
                    continue

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
                    quests.record_fish_caught()

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

    # UPDATE QUANTUM PHASE BARRIER
    world.update_quantum_barrier(
        penguin_qubit
    )

    world.update_barrier_animation(dt)

    # PLAYER MOVEMENT
    keys = pygame.key.get_pressed()

    if dialogue.active or hud.controls_open:
        # Pause movement during the conversation.
        old_x = new_x = player.x
        old_y = new_y = player.y
    else:
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

    # Detect an attempted collision before movement is resolved.
    # This triggers the barrier tutorial only when the penguin actually
    # tries to walk into the closed barrier, not merely approaches it.
    if (
        not dialogue.active
        and not hud.controls_open
        and (new_x != old_x or new_y != old_y)
        and world.barrier_collides(player, new_x, new_y, quantum_state)
    ):
        quests.touch_barrier()

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

    # UPDATE QUESTS AND UI
    quests.update(player.x, world.quantum_barrier.x, world.barrier_open)
    dialogue.update(dt)

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

    # Draw speech bubbles in the world, then overlay the HUD.
    if is_superposition:
        dialogue.draw(screen, ice_camera, player, world, 0)
    else:
        dialogue.draw(screen, camera, player, world, quantum_state)

    hint = quests.get_hint(
        fish_count, player.x, world.quantum_barrier.x,
        is_superposition, penguin_qubit.get_state_name()
    )
    if dialogue.active:
        hint = "Press F to continue the conversation"
    hud.set_tutorial(hint)
    hud.update(dt)
    hud.draw(screen, fish_count, penguin_qubit, quests)

    # DISPLAY UPDATE
    pygame.display.flip()


pygame.quit()