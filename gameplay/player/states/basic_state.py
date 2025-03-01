import pygame
from gameplay.cooldown import Cooldown
from gameplay.events import EventsManager


class BasicState:
    def __init__(self, context, animation: str, possible_next_states: set[str], cooldown=0) -> None:
        self._game_events = EventsManager()
        self._context = context
        self.cooldown = Cooldown(cooldown)
        self.possible_next_states = possible_next_states
        self._animation = animation
        self._player_direction = pygame.Vector2(0, 0)

    def _enter(self):
        self._context.change_animation(self._animation)
        self._player_direction = self._context.direction.copy()

    def _exsit(self):
        self.cooldown.reset()
        self._context.direction = self._player_direction.copy()

    def animate(self, dt):
        direction = self._context.sprite.get_flip() * 2 - 1
        direction = direction if self._context.direction.x < 0 else - direction
        direction = 1 if self._context.direction.x == 0 else direction
        self._context.current_animation.update(dt, direction)

    def update(self, dt):
        self.animate(dt)

    def next_state(self): ...
