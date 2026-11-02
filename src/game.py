"""Game setup, update loop, and rendering."""

import pygame
from settings import WIDTH, HEIGHT, FPS, ICE_TOP, ICE_BOTTOM, WATER_TOP, WATER_BOTTOM
from src.world.camera import Camera
from src.entities.player import Player
from src.world.world import World
from src.world.background import Background
from src.systems.fish_manager import FishManager
from src.world.split_screen import SplitScreenCamera
from src.ui.hud import HUD
from src.systems.quest_manager import QuestManager
from src.ui.dialogue import Dialogue
from src.quantum.quantum_controller import QuantumController
from src.input_handler import InputHandler


def draw_split_screen(screen, player, world, background, fish_manager, ice_camera, water_camera):
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



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("You Are My Quantum Penguin")
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player()
        self.ice_camera = SplitScreenCamera(0, self.player)
        self.water_camera = SplitScreenCamera(1, self.player)
        self.world = World()
        self.background = Background()
        self.fish_manager = FishManager()
        self.quantum = QuantumController(self.player, self.world)
        self.hud = HUD()
        self.quests = QuestManager()
        self.dialogue = Dialogue()
        self.input_handler = InputHandler(self)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.input_handler.handle(event)
            if not self.running:
                break
            self.update(dt)
            self.draw(dt)
            pygame.display.flip()
        pygame.quit()

    def update(self, dt):
        player = self.player
        world = self.world
        quantum = self.quantum

        world.update_quantum_barrier(quantum.qubit)
        world.update_barrier_animation(dt)

        keys = pygame.key.get_pressed()
        if self.dialogue.active or self.hud.controls_open:
            old_x = new_x = player.x
            old_y = new_y = player.y
        else:
            old_x, old_y, new_x, new_y = player.move(keys, quantum.layer)

        # Show the barrier hint only after an attempted collision.
        if (
            not self.dialogue.active
            and not self.hud.controls_open
            and (new_x != old_x or new_y != old_y)
            and world.barrier_collides(player, new_x, new_y, quantum.layer)
        ):
            self.quests.touch_barrier()

        if quantum.is_superposition:
            world.handle_superposition_collision(
                player, old_x, old_y, new_x, new_y, quantum.layer
            )
        else:
            world.handle_collision(
                player, old_x, old_y, new_x, new_y, quantum.layer
            )

        self.camera.update(player.x, player.y, player.width, player.height)
        self.fish_manager.update(dt, self.camera, world)
        self.quests.update(player.x, world.quantum_barrier.x, world.barrier_open)
        self.dialogue.update(dt)

    def draw(self, dt):
        screen = self.screen
        player = self.player
        quantum = self.quantum

        if quantum.is_superposition:
            draw_split_screen(
                screen, player, self.world, self.background, self.fish_manager,
                self.ice_camera, self.water_camera
            )
            self.dialogue.draw(screen, self.ice_camera, player, self.world, 0)
        else:
            screen.fill((190, 225, 240))
            self.background.draw(screen, self.camera)
            self.world.draw(screen, self.camera, quantum.layer)
            self.fish_manager.draw(screen, self.camera)
            player.draw(screen, self.camera, quantum.layer)
            self.dialogue.draw(screen, self.camera, player, self.world, quantum.layer)

        hints = self.quests.get_hints(
            quantum.fish_count, player.x, self.world.quantum_barrier.x,
            quantum.is_superposition, quantum.qubit.get_state_name()
        )
        if self.dialogue.active:
            hints = ["Press F to continue the conversation"]
        self.hud.set_tutorial(hints)
        self.hud.update(dt)
        self.hud.draw(screen, quantum.fish_count, quantum.qubit, self.quests)
