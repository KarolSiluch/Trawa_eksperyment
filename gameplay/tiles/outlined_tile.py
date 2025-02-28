import pygame
from tiles.tile import Tile


class OutlinedTile(Tile):
    class Sprite(Tile.Sprite):
        def __init__(self, image: pygame.Surface, sort_y_offset: int = 0, **pos: tuple[int]) -> None:
            super().__init__(image, sort_y_offset, **pos)
            self.convolution_mask = pygame.mask.Mask((3, 3), fill=True)
            self.outlined_image = self.outline_surface()
            self.outlined_rect = self.outlined_image.get_rect(center=self.rect_center)
            self.show_outline = False

        def outline_surface(self):
            mask = pygame.mask.from_surface(self.raw_image)
            surface_outline = mask.convolve(self.convolution_mask).to_surface(setcolor='white', unsetcolor=self.raw_image.get_colorkey())
            surface_outline.blit(self.raw_image, (1, 1))
            return surface_outline

        def render_image(self):
            self.final_image = self.outlined_image if self.show_outline else self.raw_image
            self.show_outline = False
            return self.final_image

        def render_rect(self):
            return self.final_image.get_rect(center=self.rect_center)

    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, **pos)
        self.activation_trigger = self.hitbox.copy().inflate(10, 10)

    def show_outline(self):
        self.sprite.show_outline = True
