from gameplay.tiles.animated_tile import Entity
from gameplay.mouse.mouse import InGameMouse
from gameplay.player.states.state_machine import StateMachine


class Player(Entity):
    class Sprite(Entity.Sprite):
        def __init__(self, image, sort_y_offset=0, **pos):
            super().__init__(image, sort_y_offset, **pos)
            self._coursor = InGameMouse()

        def get_flip(self):
            return self._coursor.get_pos()[0] < self.pos[0]

        def update(self):
            super().update()
            flip = self.get_flip()
            self.flip(flip_x=flip)

    def __init__(self, groups, type, animations, render_y_offset=0, offgrid_tile=False, **pos):
        super().__init__(groups, type, animations, StateMachine, 'idle', render_y_offset, offgrid_tile, **pos)

    def update(self, dt):
        super().update(dt)
        self.state_machine.update(dt)
        self.animate()
