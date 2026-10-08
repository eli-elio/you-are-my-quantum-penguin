import pygame
from settings import *
from camera import Camera
from player import Player
from world import World
from background import Background

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You Are My Quantum Penguin")

clock = pygame.time.Clock()

# Camera
camera = Camera()

# Penguin
player = Player()

# World
world = World()

#Background
background = Background()

# Quantum state
# 0 = ice
# 1 = water
quantum_state = 0


running = True

while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_x:

                # ICE -> WATER
                if quantum_state == 0:

                    # Calculate relative position inside ice layer
                    ice_height = ICE_BOTTOM - ICE_TOP
                    water_height = WATER_BOTTOM - WATER_TOP

                    relative_y = (
                                         player.y - ICE_TOP
                                 ) / ice_height

                    # Move to corresponding position in water
                    player.y = (
                            WATER_TOP
                            + relative_y * water_height
                    )

                    quantum_state = 1

                # WATER -> ICE
                else:

                    # Calculate relative position inside water layer
                    water_height = WATER_BOTTOM - WATER_TOP
                    ice_height = ICE_BOTTOM - ICE_TOP

                    relative_y = (
                                         player.y - WATER_TOP
                                 ) / water_height

                    # Calculate target position on ice
                    new_y = (
                            ICE_TOP
                            + relative_y * ice_height
                    )

                    # Resolve obstacle before appearing on ice
                    world.resolve_layer_switch(
                        player,
                        new_y
                    )

                    player.y = new_y
                    quantum_state = 0

    # ---------------- MOVEMENT ----------------

    keys = pygame.key.get_pressed()

    old_x, old_y, new_x, new_y = player.move(
        keys,
        quantum_state
    )

    # ---------------- COLLISION ----------------

    world.handle_collision(
        player,
        old_x,
        old_y,
        new_x,
        new_y,
        quantum_state
    )


    # ---------------- CAMERA ----------------

    camera.update(
        player.x,
        player.y,
        player.width,
        player.height
    )


    # ---------------- DRAW ----------------

    # ---------------- CLEAR SCREEN ----------------

    screen.fill((190, 225, 240))

    # ---------------- BACKGROUND ----------------

    background.draw(
        screen,
        camera
    )

    # ---------------- WORLD OBJECTS ----------------

    world.draw(
        screen,
        camera,
        quantum_state
    )

    # ---------------- PLAYER ----------------

    player.draw(
        screen,
        camera,
        quantum_state
    )

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()