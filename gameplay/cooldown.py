import pygame


class Cooldown:
    def __init__(self, duration: int) -> None:
        self._duration = duration
        self._done = True
        self._last_used_time = pygame.time.get_ticks()

    def reset(self):
        self._last_used_time = pygame.time.get_ticks()
        self._done = False

    def timer(self) -> None:
        current_time = pygame.time.get_ticks()
        if self._done:
            return
        if current_time - self._last_used_time < self._duration:
            return
        self._done = True

    def __call__(self):
        return self._done
