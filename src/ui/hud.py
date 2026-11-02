"""On-screen status, quest panel, and temporary messages."""
import pygame


class HUD:
    def __init__(self):
        self.fish_icon = pygame.image.load("assets/fish/fish_1.png").convert_alpha()
        self.fish_icon = pygame.transform.smoothscale(self.fish_icon, (54, 36))
        self.large_font = pygame.font.SysFont("arial", 30, bold=True)
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 19)
        self.message = ""
        self.message_timer = 0.0
        self.tutorial_text = []
        self.tutorial_timer = 0.0
        self.tutorial_duration = 0.45
        self.tutorial_previous = []
        self.controls_open = False

    def toggle_controls(self):
        self.controls_open = not self.controls_open

    def set_tutorial(self, text):
        # Keep the current instruction visible until its objective changes.
        # Only the old instruction fades out when it has been completed.
        text = ([text] if isinstance(text, str) and text else list(text or []))
        if text != self.tutorial_text:
            self.tutorial_previous = self.tutorial_text
            self.tutorial_timer = self.tutorial_duration if self.tutorial_previous else 0.0
            self.tutorial_text = text

    def show_message(self, text, duration=3.0):
        self.message = text
        self.message_timer = duration

    def update(self, dt):
        if self.tutorial_timer > 0 and not self.controls_open:
            self.tutorial_timer = max(0.0, self.tutorial_timer - dt)
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
                self.message_timer = 0.0

    @staticmethod
    def panel(screen, rect, color=(25, 40, 60, 195)):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=14)
        screen.blit(surface, rect.topleft)

    def draw(self, screen, fish_count, qubit, quests, hint=""):
        width, height = screen.get_size()
        self.panel(screen, pygame.Rect(10, 10, 370, 135))
        screen.blit(self.fish_icon, (20, 20))
        count = self.large_font.render(str(fish_count), True, (255, 255, 255))
        screen.blit(count, (85, 23))
        gate = self.font.render("X: 1 fish   H: 2 fish   Z: 3 fish", True, (255, 255, 255))
        screen.blit(gate, (20, 60))
        state = self.font.render(qubit.get_state_name(), True, (255, 255, 255))
        screen.blit(state, (20, 95))

        quest_width = 365
        quest_x = width - quest_width - 10
        self.panel(screen, pygame.Rect(quest_x, 10, quest_width, 140))
        gold = (255, 216, 115)
        white = (255, 255, 255)
        muted = (192, 219, 232)
        screen.blit(self.small_font.render("MAIN QUEST", True, gold), (quest_x + 17, 20))
        screen.blit(self.font.render(quests.main_quest, True, white), (quest_x + 17, 44))
        screen.blit(self.small_font.render("CURRENT OBJECTIVE", True, gold), (quest_x + 17, 83))
        screen.blit(self.small_font.render(quests.objective, True, muted), (quest_x + 17, 109))

        # Small permanent shortcut, not a permanent tutorial.
        shortcut = self.small_font.render("TAB - Controls", True, (255, 255, 255))
        shortcut_bg = shortcut.get_rect(bottomright=(width - 16, height - 14)).inflate(16, 10)
        self.panel(screen, shortcut_bg, (25, 40, 60, 165))
        screen.blit(shortcut, shortcut.get_rect(center=shortcut_bg.center))

        # Each active tutorial has its own row. Fishing remains until first catch.
        if not self.controls_open:
            visible = self.tutorial_text
            fading = False
            if not visible and self.tutorial_timer > 0:
                visible = self.tutorial_previous
                fading = True
            for index, instruction in enumerate(visible):
                alpha = (int(255 * self.tutorial_timer / self.tutorial_duration)
                         if fading else 255)
                hint_text = self.small_font.render(instruction, True, white)
                hint_text.set_alpha(alpha)
                hint_rect = hint_text.get_rect(
                    center=(width // 2, height - 112 - index * 39)
                )
                bubble_rect = hint_rect.inflate(28, 15)
                self.panel(screen, bubble_rect, (25, 40, 60, int(alpha * 0.85)))
                screen.blit(hint_text, hint_rect)

        if self.message:
            # Fit long messages within the screen without hiding the quest panel.
            font = self.font
            while font.size(self.message)[0] > width - 80 and font.get_height() > 14:
                font = pygame.font.SysFont("arial", font.get_height() - 2, bold=True)
            text = font.render(self.message, True, white)
            rect = text.get_rect(center=(width // 2, height - 60))
            self.panel(screen, rect.inflate(30, 18), (35, 55, 75, 235))
            screen.blit(text, rect)

        if self.controls_open:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((8, 17, 30, 205))
            screen.blit(overlay, (0, 0))
            panel_width = min(540, width - 40)
            panel_height = 440
            panel_rect = pygame.Rect((width - panel_width) // 2, (height - panel_height) // 2, panel_width, panel_height)
            self.panel(screen, panel_rect, (30, 49, 70, 250))
            title = self.large_font.render("CONTROLS", True, (255, 216, 115))
            screen.blit(title, (panel_rect.x + 28, panel_rect.y + 22))
            entries = [
                ("Arrow keys", "Move the penguin"),
                ("E", "Catch / measure fish"),
                ("F", "Talk / continue dialogue"),
                ("X", "Switch ice and water (1 fish)"),
                ("H", "Hadamard gate (2 fish)"),
                ("Z", "Phase flip in superposition (3 fish)"),
                ("TAB", "Open / close this guide"),
            ]
            y = panel_rect.y + 85
            for key, description in entries:
                key_image = self.font.render(key, True, (255, 216, 115))
                desc_image = self.small_font.render(description, True, (235, 246, 255))
                screen.blit(key_image, (panel_rect.x + 30, y))
                screen.blit(desc_image, (panel_rect.x + 175, y + 2))
                y += 43
            close_text = self.small_font.render("Press TAB or ESC to close", True, (192, 219, 232))
            screen.blit(close_text, close_text.get_rect(center=(width // 2, panel_rect.bottom - 24)))

