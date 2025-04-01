import pygame
import time
from screen import ScreenSettings
import sys
from gameplay.gameplay import Gameplay as Game
from gameplay.events import EventsManager


def Render_Text(screen: pygame.Surface, what: str, color, where):
    font = pygame.font.Font(None, 30)
    text = font.render(what, True, pygame.Color(color))
    screen.blit(text, where)


class Gameplay:
    def __init__(self) -> None:
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time.time()

        self._events = EventsManager

        self._screen_settings = ScreenSettings()

        self.gameplay = Game()

    def close(self) -> None:
        sys.exit()

    def interpret_events(self, event: pygame.Event) -> None:
        if event.type == pygame.QUIT:
            self.close()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._events.key_down('w')
            if event.key == pygame.K_a:
                self._events.key_down('a')
            if event.key == pygame.K_s:
                self._events.key_down('s')
            if event.key == pygame.K_d:
                self._events.key_down('d')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._events.key_up('w')
            if event.key == pygame.K_a:
                self._events.key_up('a')
            if event.key == pygame.K_s:
                self._events.key_up('s')
            if event.key == pygame.K_d:
                self._events.key_up('d')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._events.key_down('mouse1')
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._events.key_up('mouse1')

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
            self._clock.tick(400)
            dt = time.time() - self._previous_time
            self._previous_time = time.time()
            self.update(dt)
            self.render()
