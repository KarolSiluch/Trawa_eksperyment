from gameplay.cooldown import Cooldown
from gameplay.events import EventsManager


class BasicState:
    def __init__(self, context, animation: str, possible_next_states: set[str], cooldown=0) -> None:
        self.context = context
        self.cooldown = Cooldown(cooldown)
        self.possible_next_states = possible_next_states
        self._animation = animation
        self._game_events = EventsManager()

    def _enter(self):
        self.context.change_animation(self._animation)

    def _exsit(self):
        self.cooldown.reset()

    def animate(self, dt):
        direction = self.context.sprite.get_flip() * 2 - 1
        direction = direction if self.context.direction.x < 0 else - direction
        direction = 1 if self.context.direction.x == 0 else direction
        self.context.current_animation.update(dt, direction)

    def update(self, dt, *args):
        self.animate(dt)

    def next_state(self): ...
