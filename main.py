import pygame
import menu.button as button
from math import sin, sqrt
import time
from screen import ScreenSettings


# def Render_Text(screen: pygame.Surface, what: str, color, where):
#     font = pygame.font.Font(None, 30)
#     text = font.render(what, True, pygame.Color(color))
#     screen.blit(text, where)


class Background:
    def __init__(self):
        self._screen_settings = ScreenSettings()
        self._frames = self.generate_frames()
        self._fade = self.generate_fade()

    def generate_fade(self):
        fade = pygame.Surface((2000, self._screen_settings.get_height()))
        fade.fill('black')
        for x in range(fade.get_width(), 0, -1):
            color = int(255 * x / fade.get_width())
            rect = pygame.Rect(0, 0, x, fade.get_height())
            pygame.draw.rect(fade, (color, color, color), rect)
        return fade

    def generate_frames(self):
        frames = {}
        for i in range(-15, 15):
            image = pygame.Surface((16, 16))
            image.set_colorkey((0, 0, 0))
            for x in range(0, 16, 4):
                for y in range(0, 16, 4):
                    size = 2
                    rect = pygame.Rect(x, y, size, size)
                    pygame.draw.rect(image, (50, 50, 50), rect)

            shade = pygame.Surface((16, 16))
            shade.set_alpha((i + 14) * 3)
            image.blit(shade)

            frames[i] = image
        return frames

    def render(self):
        display = self._screen_settings.screen
        for x in range(1 + display.get_width() // 16):
            for y in range(1 + display.get_height() // 16):
                x_offset = (x - display.get_width() // 32) ** 2
                y_offset = (y - display.get_height() // 32) ** 2
                depth = sin(sqrt(x_offset + y_offset) - pygame.time.get_ticks() / 1000) * 15
                image = self._frames[int(depth)]
                display.blit(image, (x * 16, y * 16))
        display.blit(self._fade, special_flags=pygame.BLEND_RGB_MIN)


class Game:
    def __init__(self) -> None:
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time.time()

        self._screen_settings = ScreenSettings()
        self._background = Background()
        self._button_manager = button.ButtonManager()

    def close(self) -> None:
        self._running = False

    def interpret_events(self, event: pygame.Event) -> None:
        if event.type == pygame.QUIT:
            self.close()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._button_manager.click()

    def update(self, dt):
        self._button_manager.update(dt)

    def render(self):
        self._screen_settings.screen.fill('black')
        self._background.render()
        self._button_manager.render()
        pygame.display.update()

    def main_loop(self):
        while self._running:
            for event in pygame.event.get():
                self.interpret_events(event)
            self._clock.tick(300)
            dt = time.time() - self._previous_time
            self._previous_time = time.time()
            self.update(dt)
            self.render()


if __name__ == '__main__':
    pygame.init()
    ScreenSettings.init()
    Game().main_loop()
