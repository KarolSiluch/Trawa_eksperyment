from gameplay.tiles.animated_tile import AnimatedTile
from gameplay.mouse.mouse import InGameMouse


class Player(AnimatedTile):
    class Sprite(AnimatedTile.Sprite):
        def __init__(self, image, sort_y_offset=0, **pos):
            super().__init__(image, sort_y_offset, **pos)
            self._coursor = InGameMouse()

        def update(self):
            super().update()
            flip = self._coursor.get_pos()[0] < self.pos[0]
            self.flip(flip_x=flip)

    def update(self, dt):
        super().update(dt)
        self.current_animation.update(dt, True)
        self.animate()
