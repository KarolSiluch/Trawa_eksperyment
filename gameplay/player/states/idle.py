import pygame
from gameplay.player.states.basic_state import BasicState


class PlayerIdleState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.direction *= 0

    def next_state(self):
        if self._player_direction.magnitude():
            return 'run'

    def update(self, dt, *args):
        super().update(dt, *args)
        dx = self._game_events.get('d') - self._game_events.get('a')
        dy = self._game_events.get('s') - self._game_events.get('w')
        direction = pygame.Vector2(dx, dy)
        if direction.magnitude():
            direction.normalize_ip()
        self._player_direction = direction
