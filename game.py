import pygame
import time
from screen import ScreenSettings
import sys
from gameplay.gameplay import Gameplay as Game


def Render_Text(screen: pygame.Surface, what: str, color, where):
    font = pygame.font.Font(None, 30)
    text = font.render(what, True, pygame.Color(color))
    screen.blit(text, where)


class Gameplay:
    def __init__(self) -> None:
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time.time()
        self._screen_settings = ScreenSettings()

        self.gameplay = Game()

    def close(self) -> None:
        sys.exit()

    def interpret_events(self, event: pygame.Event) -> None:
        if event.type == pygame.QUIT:
            self.close()

    def update(self, dt):
        self.gameplay.update(dt)

    def render(self):
        self._screen_settings.screen.fill('#394541')
        self.gameplay.render()
        pos = (self._screen_settings.get_width() - 40, 3)
        Render_Text(self._screen_settings.screen, str(int(self._clock.get_fps())), (255, 0, 0), pos)
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
