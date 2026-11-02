"""Sequential, player-controlled speech bubbles anchored in the world."""
import pygame


class Dialogue:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 18, bold=True)
        self.lines = []
        self.index = 0

    @property
    def active(self):
        return self.index < len(self.lines)

    def say(self, lines):
        self.lines = list(lines)
        self.index = 0

    def advance(self):
        if not self.active:
            return False
        self.index += 1
        if not self.active:
            self.lines = []
            self.index = 0
            return True  # The conversation has finished.
        return False

    def update(self, dt):
        pass  # Dialogue waits for the player to press F.

    def draw(self, screen, camera, player, world, layer):
        if not self.active or layer != 0:
            return
        speaker, message = self.lines[self.index]
        if speaker == "player":
            center_x = player.x + player.width / 2
            top_y = player.y
        else:
            center_x = world.partner_x + world.partner_image.get_width() / 2
            top_y = world.partner_y
        x = int(camera.apply_x(center_x))
        y = int(camera.apply_y(top_y))
        self._bubble(screen, x, y, message, speaker == "player")

    def _bubble(self, screen, x, y, message, is_player):
        max_width = 250
        lines = []
        current = ""
        for word in message.split():
            trial = f"{current} {word}".strip()
            if current and self.font.size(trial)[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
        if not lines:
            return
        padding = 12
        width = max(self.font.size(s)[0] for s in lines) + padding * 2
        height = len(lines) * 23 + padding * 2
        left = max(6, min(screen.get_width() - width - 6, x - width // 2))
        top = max(6, y - height - 18)
        color = (233, 247, 255) if is_player else (255, 239, 244)
        pygame.draw.rect(screen, color, (left, top, width, height), border_radius=12)
        pygame.draw.rect(screen, (55, 77, 94), (left, top, width, height), 2, border_radius=12)
        tip_x = max(left + 14, min(left + width - 14, x))
        pygame.draw.polygon(screen, color, [
            (tip_x - 8, top + height - 1),
            (tip_x + 8, top + height - 1),
            (tip_x, top + height + 11),
        ])
        for i, line in enumerate(lines):
            surface = self.font.render(line, True, (39, 57, 74))
            screen.blit(surface, (left + padding, top + padding + i * 23))
