import pygame
from math import sin, ceil
from random import choice, randint
from copy import deepcopy
from math import sqrt
from gameplay.tiles.tilemap import TileMap
from gameplay.tiles.tile import Tile
from gameplay.assets_manager import AssetsManager
import gameplay.tiles.groups_picker as gp


class GrassManager(TileMap):
    def __init__(self, tile_size=16, stiffness=400, max_unique=10, padding=13):
        super().__init__(tile_size)
        self.grass_assets = GrassAssets(AssetsManager().get('tiles', 'grass'), self)

        self.grass_cache = {}

        self.formats = {}
        self._format_id = 0

        self.shadows = {}

        self._stiffness = stiffness
        self._tile_size = tile_size
        self._max_unique = max_unique
        self._padding = padding

    @property
    def stiffness(self):
        return self._stiffness

    @property
    def padding(self):
        return self._padding

    @property
    def format_id(self):
        return self._format_id

    def get_format(self, format_id, tile_id, grass_data):
        if format_id not in self.formats.keys():
            self.formats[format_id] = {'count': 1, 'data': [(tile_id, grass_data)]}
            self._format_id += 1
        elif self.formats[format_id]['count'] < self._max_unique:
            self.formats[format_id]['count'] += 1
            self.formats[format_id]['data'].append((tile_id, grass_data))
            self._format_id += 1
        else:
            return deepcopy(choice(self.formats[format_id]['data']))

    def apply_force(self, point, strength, radius):
        grid_pos = int(point[0] // self._tile_size), int(point[1] // self._tile_size)
        tile_range = ceil((radius + strength) / self._tile_size)

        for y in range(tile_range * 2 + 1):
            for x in range(tile_range * 2 + 1):
                x_range = x - tile_range
                y_range = y - tile_range
                pos = (grid_pos[0] + x_range, grid_pos[1] + y_range)
                if tiles := self.tile_map.get(pos):
                    for tile in tiles:
                        tile.apply_force(point, radius, strength)

    def update(self, dt, player_center: pygame.Vector2):
        self.apply_force(player_center, 15, 5)
        for tile in self.grid_tiles_around(player_center, 16):
            tile.update(dt)


class GrassAssets:
    def __init__(self, assets, grass_manager: GrassManager):
        self._grass_manager = grass_manager
        self._blades = assets
        self.convolution_mask = pygame.mask.Mask((1, 1), fill=True)

    def render_blade(self, surface: pygame.Surface, blade_id, location, rotation):
        rot_img = pygame.transform.rotate(self._blades[blade_id], rotation)

        shade_mask = pygame.mask.from_surface(rot_img)
        color_key = rot_img.get_colorkey()
        shade_surface = shade_mask.convolve(self.convolution_mask).to_surface(setcolor='black', unsetcolor=color_key)

        shade_amt = 70 * (abs(rotation) / 90)
        shade_surface.set_alpha(shade_amt)
        rot_img.blit(shade_surface, (0, 0))

        surface.blit(rot_img, (location[0] - rot_img.get_width() // 2, location[1] - rot_img.get_height() // 2))


class GrassTile(Tile):
    def __init__(self, groups, type, amount, config, sort_y_offset=0, offgrid_tile=False, z=5, special_flags=0, **pos):
        self._grass_manager: GrassManager = gp.GroupsPicker().get_group(gp.GroupType.Grass)
        self._grass_assets = self._grass_manager.grass_assets
        self._blades = []
        self._format_id = self._grass_manager.format_id
        self._tile_size = 16
        self._location = (list(pos.values())[0][0] - 8, list(pos.values())[0][1] - 8)
        self.rotation = 0
        self.render_rotation = 0
        self.custom_blade_data = None
        self.padding = self._grass_manager.padding
        self.add_tile(amount, config)
        super().__init__(groups, type, self.get_image(), sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self.generate_shadow()

    def add_tile(self, amount, config):
        for _ in range(amount):
            blade_image = choice(config)
            pos = randint(0, self._tile_size), randint(0, self._tile_size)
            offset_rotation = randint(-10, 10)
            self._blades.append((pos, blade_image, offset_rotation))

        self._blades.sort(key=lambda x: x[1])

        format_id = (amount, tuple(config))
        if format := self._grass_manager.get_format(format_id, self._format_id, self._blades):
            self._format_id = format[0]
            self._blades = format[1]

    def apply_force(self, force_point, strength, force_radius):
        if not self.custom_blade_data:
            self.custom_blade_data = [None] * len(self._blades)

        for blade_id, blade in enumerate(self._blades):
            grid_point_x = self._location[0] + blade[0][0]
            grid_point_y = self._location[1] + blade[0][1]
            # print((self.hitbox.right + self.padding, self.hitbox.top + self.padding), force_point)
            distance = self.get_distance((grid_point_x, grid_point_y), force_point)
            if distance < force_radius:
                force = 2
            else:
                distance = max(0, distance - force_radius)
                force = 1 - min(distance / strength, 1)
            direction = 1 if force_point[0] > (self.hitbox.right + blade[0][0]) else -1

            if self.custom_blade_data[blade_id]:
                if abs(self.custom_blade_data[blade_id][2] - self._blades[blade_id][2]) > abs(force) * 90:
                    return
            self.custom_blade_data[blade_id] = [blade[0], blade[1], blade[2] + direction * force * 90]

    def generate_shadow(self):
        if self._format_id not in self._grass_manager.shadows:
            size = (self._tile_size + 2 * self.padding, self._tile_size + 2 * self.padding)
            shadow_surface = pygame.Surface(size, pygame.SRCALPHA)
            shadow_surface.set_colorkey((0, 0, 0))
            for blade in self._blades:
                center = blade[0][0] + self.padding, blade[0][1] + self.padding
                pygame.draw.circle(shadow_surface, (10, 10, 10), center, 4)
            shadow_surface.set_alpha(60)
            self._grass_manager.shadows[self._format_id] = shadow_surface
        image = self._grass_manager.shadows[self._format_id]
        groups = gp.GroupsPicker().get_groups(gp.GroupType.Visible)
        Tile(groups, 'shadow', image, z=4, topleft=self.hitbox.topleft)

    def update(self, dt):
        super().update(dt)
        self.rotation = int(sin(pygame.time.get_ticks() / 600 + self._location[0] / 100 + self._location[1] / 200) * 14)
        self.render_rotation = 3 * self.rotation
        self.sprite._master_image = self.get_image()

        if self.custom_blade_data:
            matching = True
            for i, blade in enumerate(self.custom_blade_data):
                blade[2] = self.normalize(blade[2], self._grass_manager.stiffness * dt, self._blades[i][2])
                if blade[2] != self._blades[i][2]:
                    matching = False

            if matching:
                self.custom_blade_data = None

    def render_tile(self):
        surf = pygame.Surface((self._tile_size + self.padding * 2, self._tile_size + self.padding * 2))
        surf.set_colorkey((0, 0, 0))

        blades = self.custom_blade_data if self.custom_blade_data else self._blades

        for blade in blades:
            pos = (blade[0][0] + self.padding, blade[0][1] + self.padding)
            self._grass_assets.render_blade(surf, blade[1], pos, self.render_rotation + blade[2])

        return surf

    def get_image(self):
        if self.custom_blade_data:
            return self.render_tile()
        else:
            cache_lookup = (self._format_id, self.rotation)
            if cache_lookup not in self._grass_manager.grass_cache:
                self._grass_manager.grass_cache[cache_lookup] = self.render_tile()
            return self._grass_manager.grass_cache[cache_lookup]

    # def render(self, surf: pygame.Surface, dt, offset=(0, 0)):
    #     self.update_render_data()
    #     if self.custom_blade_data:
    #         pos = (self._location[0] - offset[0] - self.padding, self._location[1] - offset[1] - self.padding)
    #         surf.blit(self._grass_manager.shadows[self._format_id], pos)
    #         surf.blit(self.render_tile(), pos)
    #     else:
    #         cache_lookup = (self._format_id, self.rotation)
    #         if cache_lookup not in self._grass_manager.grass_cache:
    #             self._grass_manager.grass_cache[cache_lookup] = self.render_tile()

    #         pos = (self._location[0] - offset[0] - self.padding, self._location[1] - offset[1] - self.padding)
    #         surf.blit(self._grass_manager.shadows[self._format_id], pos)
    #         surf.blit(self._grass_manager.grass_cache[cache_lookup], pos)

    #     if self.custom_blade_data:
    #         matching = True
    #         for i, blade in enumerate(self.custom_blade_data):
    #             blade[2] = self.normalize(blade[2], self._grass_manager.stiffness * dt, self._blades[i][2])
    #             if blade[2] != self._blades[i][2]:
    #                 matching = False

    #         if matching:
    #             self.custom_blade_data = None

    @staticmethod
    def normalize(val, amt, target):
        if val > target + amt:
            val -= amt
        elif val < target - amt:
            val += amt
        else:
            val = target
        return val

    @staticmethod
    def get_distance(point1, point2):
        x = point1[0] - point2[0]
        y = point1[1] - point2[1]
        return sqrt(x ** 2 + y ** 2)
