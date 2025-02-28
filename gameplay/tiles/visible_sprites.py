import pygame
from gameplay.tiles.tilemap import TileMap


class YSortCamera(TileMap):
    def __init__(self, tile_size=48) -> None:
        super().__init__(tile_size)

    def __str__(self):
        print_parts = []
        tiles = sorted(self.tiles(), key=lambda tile: tile.sprite.rect.centery + tile.sprite.sort_y_offset)
        for tile in tiles:
            print_parts.append(f'type: {tile.type}, (x, y): {tile.sprite.rect.center}')
        return '\n'.join(print_parts)

    def render(self, display: pygame.Surface, camera_offset: pygame.Vector2):
        for tile in sorted(self.tiles(), key=lambda tile:
                           (tile.z, tile.sprite.rect.bottom + tile.sprite.sort_y_offset + tile.sprite.render_offset.y)):
            if not tile.sprite.show:
                continue
            image, rect = tile.get_sprite()
            pos = rect.topleft - camera_offset + tile.sprite.render_offset
            display.blit(image, pos, special_flags=tile.special_flags)
