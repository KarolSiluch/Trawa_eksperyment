import pygame
from gameplay.player.states.basic_state import BasicState


class PlayerIdleState(BasicState):
    def _enter(self):
        super()._enter()
        self.context.direction *= 0

    def next_state(self):
        if self.context.direction.magnitude():
            print(self.possible_next_states)
            print('run' in self.possible_next_states)
            return 'run'

    def update(self, dt, *args):
        super().update(dt, *args)
        dx = self._game_events.get('d') - self._game_events.get('a')
        dy = self._game_events.get('s') - self._game_events.get('w')
        direction = pygame.Vector2(dx, dy)
        if direction.magnitude():
            direction.normalize_ip()
        self.context.direction = direction
