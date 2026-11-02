"""Keyboard input and player interactions."""

import pygame
from src.ui.dialogue_data import INTRO_DIALOGUE, RETURN_DIALOGUE


class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle(self, event):
        game = self.game
        if event.type == pygame.QUIT:
            game.running = False
            return
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_TAB:
            game.hud.toggle_controls()
            return

        if game.hud.controls_open:
            if event.key == pygame.K_ESCAPE:
                game.hud.toggle_controls()
            return

        if game.dialogue.active:
            if event.key == pygame.K_f:
                if game.dialogue.advance() and not game.quests.talked_to_partner:
                    game.quests.talk_to_partner()
            return

        gate_keys = {
            pygame.K_x: "X",
            pygame.K_h: "H",
            pygame.K_z: "Z",
        }
        if event.key in gate_keys:
            game.hud.show_message(game.quantum.apply_gate(gate_keys[event.key]))
        elif event.key == pygame.K_f:
            self.talk_to_partner()
        elif event.key == pygame.K_e:
            self.catch_fish()

    def talk_to_partner(self):
        game = self.game
        world = game.world
        player = game.player
        partner_x = world.partner_x + world.partner_image.get_width() / 2
        partner_y = world.partner_y + world.partner_image.get_height() / 2
        player_x = player.x + player.width / 2
        player_y = player.y + player.height / 2
        near_partner = (
            game.quantum.layer == 0
            and abs(player_x - partner_x) < 135
            and abs(player_y - partner_y) < 125
        )
        if near_partner:
            lines = RETURN_DIALOGUE if game.quests.talked_to_partner else INTRO_DIALOGUE
            game.dialogue.say(lines)

    def catch_fish(self):
        game = self.game
        result = game.fish_manager.try_catch(
            game.player, game.quantum.layer, game.quantum.is_superposition
        )
        if result == "caught":
            game.quantum.add_fish()
            game.quests.record_fish_caught()
            game.hud.show_message("Fish caught! +1 fish")
        elif result == "missed":
            game.hud.show_message("Measurement failed!")
        else:
            game.hud.show_message("No fish within reach")
