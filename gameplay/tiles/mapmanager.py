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
            gp.GroupType.Grass: GrassManager(tile_size),
            gp.GroupType.Bullets: TileMap(tile_size)
        }
        gp.GroupsPicker.init(self.sprite_groups)
        self._groups_piscker = gp.GroupsPicker()
        self._groups_picker = gp.GroupsPicker()
        self._coursor = mouse.InGameMouse()

        self.player_start_position = (0, 0)

        self._background = Background()

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
            GrassTile(groups, 'grass', 1000, [0, 1, 2, 3, 5], -16, **pos)

        else:
            groups = self._groups_picker.get_groups(gp.GroupType.Visible)
            image = self.game._assets.get('tiles', type)[variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        self.get_camera_offset()
        mouse.InGameMouse.update(self.camera_offset)
        self._background.update(dt)
        self.sprite_groups[gp.GroupType.Grass].update(dt, self.game.player.hitbox.midbottom)
        self.sprite_groups[gp.GroupType.Bullets].update(dt, self.game.player.hitbox.midbottom)

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
        self._background.render()
        screen = self._screnn_settings.screen
        self.sprite_groups[gp.GroupType.Visible].render(screen, self.camera_offset)


class Background:
    class BackgroundRect:
        def __init__(self, posx, angle, speed, angle_speed, radius):
            self._posx = posx
            self._y = 0
            self._angle = angle
            self._speed = speed
            self._angle_speed = angle_speed
            self._radius = radius

        def update(self, dt):
            self._y += self._speed * dt
            self._angle += self._angle_speed * dt

        def done(self, screen_edge):
            return True if self._y > screen_edge + 2 * self._radius else False

        def to_polygon(self):
            points = []
            corner_vector = pygame.Vector2(self._radius, 0)
            corner_vector.rotate_ip(self._angle)
            for _ in range(4):
                corner_vector.rotate_ip(90)
                points.append(corner_vector + (self._posx, self._y))
            return points

    def __init__(self):
        self._screen_settings = ScreenSettings()
        self._display = pygame.Surface(self._screen_settings.get_size())
        self._y_offset = 0
        self._rects = self.get_rects(8)

    def render_lines(self):
        for y_pos in range(-30, self._display.get_height() + 30, 40):
            y_offset = self._y_offset % 40
            point1 = (0, y_pos + y_offset)
            point2 = (self._display.get_width(), y_pos + y_offset + 30)
            pygame.draw.line(self._display, '#332e54', point1, point2, 15)

    def render_rects(self):
        for rect in self._rects:
            points = rect.to_polygon()
            pygame.draw.lines(self._display, '#332e54', True, points, rect._radius)

    def update_rects(self):
        for rect in self._rects:
            if rect.done(self._display.get_height()):
                rect._y = -rect._radius

    def update(self, dt):
        self._display.fill('#151023')
        self.update_rects()
        self._y_offset += 30 * dt
        for rect in self._rects:
            rect.update(dt)

    def render(self):
        self.render_lines()
        self.render_rects()
        self._display.fill('#333c3a')
        self._screen_settings.screen.blit(self._display)

    def get_rect(self):
        posx = randint(0, self._display.get_width())
        rect = self.BackgroundRect(posx, randint(0, 360), randint(30, 100), randint(20, 50), randint(4, 30))
        return rect

    def get_rects(self, n):
        rects = []
        for _ in range(n):
            rects.append(self.get_rect())
        return rects
