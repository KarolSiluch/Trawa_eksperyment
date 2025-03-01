import pygame
from gameplay.tiles.mapmanager import MapManager
from gameplay.player.player import Player
import gameplay.tiles.groups_picker as gp
from gameplay.assets_manager import AssetsManager


class Gameplay:
    def __init__(self) -> None:
        AssetsManager.init()
        self._assets = AssetsManager()
        self.current_map = MapManager(self, 16, 'map1', 0)
        self.transiton = Transition(self)

        groups = gp.GroupsPicker().get_groups(gp.GroupType.Visible)
        player_assets = self._assets.get('player')
        player_pos = {'center': self.current_map.player_start_position}
        self.player: Player = Player(groups, 'player', player_assets, **player_pos)

    def new_map(self, map):
        self.transiton.new_map(map)

    # def import_map(self, map):
    #     if map == 'lobby':
    #         self.stage = 0
    #         self.current_map = self.current_map = self.lobby
    #         self.current_map.enter()
    #         self.player.hp = self.player.max_hp
    #     else:
    #         self.current_map = MapManager(self, 16, map, self.stage)

    #     self.ui.import_map()
    #     self.player.hitbox.center = self.current_map.player_start_position
    #     self.player.sprite.rect.center = self.current_map.player_start_position
    #     self.player.add_to_new_group()

    def update(self, dt: float) -> None:
        # self.transiton.update(dt)
        self.player.update(dt)
        self.current_map.update(dt)
        # self.ui.update(dt)

        # if self.player.hp > 0: return
        # if self.transiton.next_map: return
        # self.new_map('lobby')

    def render(self):
        self.current_map.render()
        # self.ui.render(display)
        # self.transiton.render(display)


class Transition:
    def __init__(self, game: Gameplay):
        self.game = game
        self.transition = 320
        self.next_map = None

    def new_map(self, map):
        self.next_map = map
        self.transition = -320

    def update(self, dt):
        self.transition = min(self.transition + dt * 500, 320)
        if self.next_map:
            if self.transition > 0:
                self.game.import_map(self.next_map)
                self.next_map = None

    def render(self, display: pygame.Surface):
        if self.transition < 320:
            transition_surface = pygame.Surface(display.get_size())
            pos = (display.get_width() // 2, display.get_height() // 2)
            pygame.draw.circle(transition_surface, 'white', pos, abs(self.transition))
            transition_surface.set_colorkey('white')
            display.blit(transition_surface, (0, 0))
