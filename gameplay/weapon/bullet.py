import pygame
from gameplay.tiles.tile import Tile
from gameplay.cooldown import Cooldown
import gameplay.tiles.groups_picker as gp


class Bullet(Tile):
    def __init__(self, groups, type, image, direction: pygame.Vector2, sort_y_offset=0,
                 offgrid_tile=False, z=5, special_flags=0, **pos):
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self._direction = direction
        self._angle = direction.angle_to(pygame.Vector2(1, 0))
        self._life_span = Cooldown(500)
        self._life_span.reset()
        self._groups_picker = gp.GroupsPicker()

    def move(self, dt, direction: pygame.Vector2):
        self.hitbox.center += 800 * dt * direction
        self.sprite.pos = self.hitbox.center
        self.sprite.rect.center = self.hitbox.center

    def collide(self):
        tilemap = self._groups_picker.get_group(gp.GroupType.Collidable)
        if tilemap.get_collisions(self):
            self.kill()

    def update(self, dt):
        super().update(dt)
        self.sprite.rotate(self._angle)
        self._life_span.timer()
        self.move(dt, self._direction)
        self.collide()
        if self._life_span._done:
            self.kill()
