import pygame
from gameplay.mouse.mouse import InGameMouse
from gameplay.tiles.tile import Tile
from gameplay.assets_manager import AssetsManager
from gameplay.weapon.bullet import Bullet
import gameplay.tiles.groups_picker as gp
from gameplay.events import EventsManager
from gameplay.cooldown import Cooldown


class Weapon:
    class VisualRepresentation(Tile):
        class Sprite(Tile.Sprite):
            def __init__(self, image, sort_y_offset=0, **pos):
                super().__init__(image, sort_y_offset, **pos)
                self._coursor = InGameMouse()

            def update(self):
                super().update()
                mouse_vector = self._coursor.mouse_vector(self.pos)
                if mouse_vector.magnitude():
                    self._render_offset = mouse_vector.copy()
                    self._render_offset.scale_to_length(4)
                    flip = mouse_vector.x < 0
                    self.flip(flip_y=flip)
                    angle = mouse_vector.angle_to(pygame.Vector2(1, 0))
                    self.rotate(angle)

        def update(self, dt):
            self.sprite.pos = self.hitbox.center
            super().update(dt)

    def __init__(self, groups, image, rotation_point):
        pos = {'center': rotation_point}
        self.visual_representation = self.VisualRepresentation(groups, 'weapon', image, 0, True, 6, **pos)
        self._bullet_image = AssetsManager().get('weapons', 'bullet')
        self._events = EventsManager()
        self._shoot_cooldown = Cooldown(200)
        self._shoot_cooldown.reset()

    def update(self, dt, rotation_point):
        self.visual_representation.hitbox.center = rotation_point
        self.visual_representation.update(dt)
        self._shoot_cooldown.timer()
        self.shoot()

    def shoot(self):
        if not self._events.get('mouse1'):
            return
        if not self._shoot_cooldown._done:
            return

        self._shoot_cooldown.reset()
        groups = gp.GroupsPicker().get_groups(gp.GroupType.Bullets, gp.GroupType.Visible)
        direction = InGameMouse().mouse_vector(self.visual_representation.hitbox.center)
        if direction:
            direction.normalize_ip()
        pos = direction * 13 + self.visual_representation.hitbox.center
        Bullet(groups, 'bullet', self._bullet_image, direction, offgrid_tile=True, center=pos)
