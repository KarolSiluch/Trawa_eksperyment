import pygame


class ScreenSettings:
    @classmethod
    def init(cls):
        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        flags = pygame.FULLSCREEN | pygame.SCALED
        cls._screen: pygame. Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), flags)

    def get_size(self) -> tuple[int]:
        return self._screen.get_size()

    def get_width(self) -> int:
        return self._screen.get_width()

    def get_height(self) -> int:
        return self._screen.get_height()

    @property
    def screen(self) -> pygame.Surface:
        return self._screen
