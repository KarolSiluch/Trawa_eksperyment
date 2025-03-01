import pygame
import json
from gameplay.tiles.tilemap import TileMap
from gameplay.tiles.tile import Tile
from gameplay.tiles.visible_sprites import YSortCamera
import gameplay.tiles.groups_picker as gp
import gameplay.mouse.mouse as mouse
from screen import ScreenSettings
from random import randint
from gameplay.grass.grass import GrassManager, GrassTile


class MapManager:
    def __init__(self, game, tile_size: int, map: str, stage: int) -> None:
        self._screnn_settings = ScreenSettings()
        self.game = game
        self.tile_size = tile_size
        self.camera_offset = pygame.Vector2()
        self.map = map
        self.sprite_groups = {
            gp.GroupType.Visible: YSortCamera(tile_size),
            gp.GroupType.Collidable: TileMap(tile_size),
            gp.GroupType.Grass: GrassManager(tile_size)

        }
        gp.GroupsPicker.init(self.sprite_groups)
        self._groups_piscker = gp.GroupsPicker()
        self._groups_picker = gp.GroupsPicker()
        self._coursor = mouse.InGameMouse()

        self.player_start_position = (0, 0)

        self.load(f'{map}.json')

    def enter(self):
        gp.GroupsPicker.init(self.sprite_groups)

    def load(self, path):
        with open(path, 'r') as f:
            map_date = json.load(f)
            for tile_data in map_date['tilemap']:
                self.create_tile(tile_data)

    def create_tile(self, tile_data):
        type = tile_data['type']
        variant = tile_data['variant']
        offgrid_tile = tile_data['offgrid_tile']
        layer = tile_data['z']
        pos: dict = tile_data['pos']

        if type in {'wall'}:
            groups = self._groups_picker.get_groups(gp.GroupType.Visible, gp.GroupType.Collidable)
            image = self.game._assets.get('tiles', type)[variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type == 'player':
            self.player_start_position = list(pos.values())[0]

        elif type == 'grass':
            groups = self._groups_picker.get_groups(gp.GroupType.Visible, gp.GroupType.Grass)
            GrassTile(groups, 'grass', randint(5, 9), [0, 1, 2, 3, 5], -16, **pos)

        else:
            groups = self._groups_picker.get_groups(gp.GroupType.Visible)
            image = self.game._assets.get('tiles', type)[variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        self.get_camera_offset()
        mouse.InGameMouse.update(self.camera_offset)
        self.sprite_groups[gp.GroupType.Grass].update(dt, self.game.player.hitbox.midbottom)

    def get_camera_offset(self):
        mouse_vector = self._coursor.mouse_vector(self.game.player.hitbox.center)
        vector_size = min(mouse_vector.magnitude() / 7, 60)
        if vector_size:
            mouse_vector.scale_to_length(vector_size)

        mouse_offset_x = self.game.player.hitbox.centerx + mouse_vector.x
        mouse_offset_y = self.game.player.hitbox.centery + mouse_vector.y

        display = self._screnn_settings.screen
        self.camera_offset.x += (mouse_offset_x - display.get_width() // 2 - self.camera_offset.x) / 10
        self.camera_offset.y += (mouse_offset_y - display.get_height() // 2 - self.camera_offset.y) / 10

    def render(self):
        screen = self._screnn_settings.screen
        self.sprite_groups[gp.GroupType.Visible].render(screen, self.camera_offset)
