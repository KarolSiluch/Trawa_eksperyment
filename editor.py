import pygame
import time
from map_editor.editor_manager import EditorMapManager
from gameplay.mouse.mouse import InGameMouse
from map_editor.editor_tile import EditorTile


def load_image(path) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def import_cut_graphics(image_grid: tuple[int], path):
    combined_image = load_image(path)
    image_width = int(combined_image.get_width() / image_grid[0])
    image_height = int(combined_image.get_height() / image_grid[1])
    result = []
    for y in range(image_grid[1]):
        for x in range(image_grid[0]):
            image = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            offset = (-x * image_width, -y * image_height)
            image.blit(combined_image, offset)
            result.append(image)
    return result


class Editor:
    def __init__(self) -> None:
        pygame.init()
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time.time()
        self._events: dict[str, bool] = {'w': False, 'a': False, 's': False, 'd': False, 'mouse1': False,
                                         'mouse3': False, 'shift': False}

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        size = (screen_size[0] // 3, screen_size[1] // 3)
        self._screen: pygame.Surface = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)

        self.import_assets()
        self._camera_offset = pygame.Vector2(0, 0)
        self._tile_size = 16
        self._map_manager = EditorMapManager(self, self._tile_size)

        self._tile_list = self.tile_list = list(self._assets)
        self._tile_group = 0
        self._tile_variant = 0
        self._off_grid = False
        self._cursor = InGameMouse()

    @property
    def camera_offset(self):
        return self._camera_offset

    @property
    def assets(self):
        return self._assets

    def update(self, dt):
        self._camera_offset.x += (self._events['d'] - self._events['a']) * 200 * dt
        self._camera_offset.y += (self._events['s'] - self._events['w']) * 200 * dt
        self._map_manager.update(dt)

    def show_selected_tile(self):
        type = self._tile_list[self._tile_group]
        current_tile = self._assets[type][self._tile_variant].copy()
        current_tile.set_alpha(200)
        self._screen.blit(current_tile, (20, 20))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if type in {'player', 'enemy', 'kakine'}:
            render_rect = current_tile.get_rect(center=(mouse_x, mouse_y))
            self._screen.blit(current_tile, render_rect)

        elif self._off_grid:
            self._screen.blit(current_tile, (mouse_x, mouse_y))

        else:
            x = ((mouse_x + self._camera_offset.x) // self._tile_size) * self._tile_size - self._camera_offset.x
            y = ((mouse_y + self._camera_offset.y) // self._tile_size) * self._tile_size - self._camera_offset.y
            self._screen.blit(current_tile, (x, y))

    def render(self):
        self._screen.fill('#07123a')
        self._map_manager.render(self._screen)
        self.show_selected_tile()

        for y_offset in range(0, self._screen.height, self._tile_size):
            y = y_offset - self._camera_offset.y % self._tile_size
            pygame.draw.line(self._screen, 'black', (0, y), (self._screen.width, y))
        for x_offset in range(0, self._screen.width, self._tile_size):
            x = x_offset - self._camera_offset.x % self._tile_size
            pygame.draw.line(self._screen, 'black', (x, 0), (x, self._screen.height))

        pygame.display.update()

    def add_tile(self):
        ingame_mpos = self._cursor.get_pos()

        type = self._tile_list[self._tile_group]
        image = self._assets[type][self._tile_variant]

        layer = 5
        if type in {'player'}:
            if not self._off_grid:
                return
            pos = {'center': ingame_mpos}
        elif self._off_grid:
            pos = {'topleft': ingame_mpos}
        elif type == 'grass':
            index_x = (ingame_mpos[0] // self._tile_size * self._tile_size + self._tile_size // 2)
            index_y = (ingame_mpos[1] // self._tile_size * self._tile_size + self._tile_size // 2)
            pos = {'center': (index_x, index_y)}
        else:
            index_x = (ingame_mpos[0] // self._tile_size)
            index_y = (ingame_mpos[1] // self._tile_size)
            pos = {'topleft': (index_x * self._tile_size, index_y * self._tile_size)}

        group = [self._map_manager.sprite_group]
        EditorTile(group, type, self._tile_variant, image, offgrid_tile=self._off_grid, z=layer, **pos)

    def remove_tile(self):
        ingame_mpos = self._cursor.get_pos()

        collision_tiles = []
        for tile in self._map_manager.sprite_group.offgrid_tiles:
            if not tile.sprite.rect.collidepoint(ingame_mpos):
                continue
            collision_tiles.append(tile)
        if len(collision_tiles):
            collision_tiles[-1].kill()
            return

        if len(tiles := self._map_manager.sprite_group.grid_tiles_around(ingame_mpos, 0)):
            tiles[-1].kill()

    def main_loop(self):
        while self._running:
            self._clock.tick()
            dt = time.time() - self._previous_time
            self._previous_time = time.time()
            self.get_events()
            self.update(dt)
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self._events['w'] = True
                if event.key == pygame.K_a:
                    self._events['a'] = True
                if event.key == pygame.K_s:
                    self._events['s'] = True
                if event.key == pygame.K_d:
                    self._events['d'] = True
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = True
                if event.key == pygame.K_g:
                    self._off_grid = not self._off_grid
                if event.key == pygame.K_o:
                    self._map_manager.save('map1.json')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self._events['w'] = False
                if event.key == pygame.K_a:
                    self._events['a'] = False
                if event.key == pygame.K_s:
                    self._events['s'] = False
                if event.key == pygame.K_d:
                    self._events['d'] = False
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.add_tile()
                    self._events['mouse1'] = True
                if event.button == 3:
                    self.remove_tile()
                    self._events['mouse3'] = True
                if event.button == 4:
                    if self._events['shift']:
                        self._tile_variant = 0
                        self._tile_group = (self._tile_group + 1) % len(self._tile_list)
                    else:
                        assets_len = len(self._assets[self._tile_list[self._tile_group]])
                        self._tile_variant = (self._tile_variant + 1) % assets_len
                if event.button == 5:
                    if self._events['shift']:
                        self._tile_variant = 0
                        self._tile_group = (self._tile_group - 1) % len(self._tile_list)
                    else:
                        assets_len = len(self._assets[self.tile_list[self._tile_group]])
                        self._tile_variant = (self._tile_variant - 1) % assets_len
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._events['mouse1'] = False
                if event.button == 3:
                    self._events['mouse3'] = False

    def import_assets(self):
        self._assets = {
            'player': [load_image('assets/game/player/Accelerator.png')],
            'wall': import_cut_graphics((3, 4), 'assets/game/tiles/walls.png'),
            'grass': [load_image('assets/game/grass/grass_editor.png')]
        }


if __name__ == '__main__':
    Editor().main_loop()
