import pygame
import json
from map_editor.editor_tile import EditorTile
from gameplay.tiles.visible_sprites import YSortCamera
from gameplay.mouse.mouse import InGameMouse


class EditorMapManager:
    def __init__(self, game, tile_size: int) -> None:
        self._game = game
        self._tile_size = tile_size
        self._camera_offset = pygame.Vector2()
        self._sprite_group = YSortCamera(tile_size)

        try:
            self.load('map1.json')
        except FileNotFoundError:
            pass

    @property
    def sprite_group(self):
        return self._sprite_group

    def save(self, path):
        f = open(path, 'w')
        tilemap = []
        for tile in self._sprite_group.tiles():
            tilemap.append({'type': tile.tile_type, 'variant': tile.variant, 'offgrid_tile': tile.offgrid_tile,
                            'z': tile.z, 'pos': tile.created_position})

        json.dump({'tilemap': tilemap, 'tile_size': self._tile_size}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map = json.load(f)
        f.close()
        for tile_data in map['tilemap']:
            type = tile_data['type']
            variant = tile_data['variant']
            image = self._game.assets[type][variant]
            offgrid_tile = tile_data['offgrid_tile']
            layer = tile_data['z']
            pos = tile_data['pos']
            EditorTile([self._sprite_group], type, variant, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        self._camera_offset = self._game.camera_offset
        InGameMouse.update(self._camera_offset)

    def render(self, display: pygame.Surface):
        self._sprite_group.render(display, self._camera_offset)
