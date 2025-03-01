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
        self.context.hitbox.x += direction.x * self.context.velocity * dt
        tilemap = self._groups_picker.get_group(gp.GroupType.Collidable)
        collisions: list[Tile] = tilemap.get_collisions(self.context)
        for tile in collisions:
            if tile.type not in self._collidable_sprites:
                continue
            if direction.x > 0:
                self.context.hitbox.right = tile.hitbox.left
            elif direction.x < 0:
                self.context.hitbox.left = tile.hitbox.right

        self.context.hitbox.y += direction.y * self.context.velocity * dt
        collisions: list[Tile] = tilemap.get_collisions(self.context)
        for tile in collisions:
            if tile.type not in self._collidable_sprites:
                continue
            if direction.y > 0:
                self.context.hitbox.bottom = tile.hitbox.top
            elif direction.y < 0:
                self.context.hitbox.top = tile.hitbox.bottom

        self.context.sprite.pos = self.context.hitbox.center

    def update(self, dt):
        super().update(dt)
        dx = self._game_events.get('d') - self._game_events.get('a')
        dy = self._game_events.get('s') - self._game_events.get('w')
        direction = pygame.Vector2(dx, dy)
        if direction.magnitude():
            direction.normalize_ip()
        self.context.direction = direction
        self.move(dt, direction)

    def next_state(self):
        if not self.context.direction.magnitude():
            return 'idle'
