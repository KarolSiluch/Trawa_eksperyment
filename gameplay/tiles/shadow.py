import pygame
from gameplay.tiles.tile import Tile


class Shadow(Tile):
    def __init__(self, groups, size, sort_y_offset=0, offgrid_tile=True,
                 z=4, special_flags=0, **pos):

        super().__init__(groups, 'shadow', self.generate_shadow(size),
                         sort_y_offset, offgrid_tile, z, special_flags, **pos)

    @staticmethod
    def generate_shadow(size):
        shadow_surface = pygame.Surface(size, pygame.SRCALPHA)
        rect = pygame.Rect((0, 0), size)
        pygame.draw.ellipse(shadow_surface, (10, 10, 10), rect)
        shadow_surface.set_alpha(100)
        return shadow_surface

    def update(self, dt):
        self.sprite.pos = self.hitbox.center
        super().update(dt)
