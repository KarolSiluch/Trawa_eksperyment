import pygame
from gameplay.player.states.basic_state import BasicState
from gameplay.tiles.tile import Tile
import gameplay.tiles.groups_picker as gp


class PlayerRunState(BasicState):
    def __init__(self, context, possible_next_states, animation, cooldown=0):
        super().__init__(context, possible_next_states, animation, cooldown)
        self._collidable_sprites = {'wall'}
        self._groups_picker = gp.GroupsPicker()

    def move(self, dt, direction: pygame.Vector2):
        self._context.hitbox.x += direction.x * self._context.velocity * dt
        tilemap = self._groups_picker.get_group(gp.GroupType.Collidable)
        collisions: list[Tile] = tilemap.get_collisions(self._context)
        for tile in collisions:
            if tile.tile_type not in self._collidable_sprites:
                continue
            if direction.x > 0:
                self._context.hitbox.right = tile.hitbox.left
            elif direction.x < 0:
                self._context.hitbox.left = tile.hitbox.right

        self._context.hitbox.y += direction.y * self._context.velocity * dt
        collisions: list[Tile] = tilemap.get_collisions(self._context)
        for tile in collisions:
            if tile.tile_type not in self._collidable_sprites:
                continue
            if direction.y > 0:
                self._context.hitbox.bottom = tile.hitbox.top
            elif direction.y < 0:
                self._context.hitbox.top = tile.hitbox.bottom

        self._context.sprite.pos = self._context.hitbox.center

    def update(self, dt):
        super().update(dt)
        dx = self._game_events.get('d') - self._game_events.get('a')
        dy = self._game_events.get('s') - self._game_events.get('w')
        direction = pygame.Vector2(dx, dy)
        if direction.magnitude():
            direction.normalize_ip()
        self._player_direction = direction
        self.move(dt, direction)

    def next_state(self):
        if not self._player_direction.magnitude():
            return 'idle'
