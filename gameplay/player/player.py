from gameplay.tiles.animated_tile import Entity
from gameplay.mouse.mouse import InGameMouse
from gameplay.player.states.state_machine import StateMachine
from gameplay.tiles.shadow import Shadow
import gameplay.tiles.groups_picker as gp
from gameplay.weapon.weapon import Weapon
from gameplay.assets_manager import AssetsManager


class Player(Entity):
    class Sprite(Entity.Sprite):
        def __init__(self, image, sort_y_offset=0, **pos):
            super().__init__(image, sort_y_offset, **pos)
            self._coursor = InGameMouse()

        def get_flip(self):
            return self._coursor.get_pos()[0] < self.pos[0]

        def update(self):
            super().update()
            flip = self.get_flip()
            self.flip(flip_x=flip)

    def __init__(self, groups, type, animations, render_y_offset=0, offgrid_tile=True, **pos):
        super().__init__(groups, type, animations, StateMachine, 'idle', render_y_offset, offgrid_tile, **pos)
        self.hitbox.inflate_ip(0, -0.9 * self.hitbox.height)
        self.add_shadow()
        groups = gp.GroupsPicker().get_groups(gp.GroupType.Visible)
        image = AssetsManager().get('weapons', 'ak')
        self._weapon = Weapon(groups, image, self.weapon_rotation_point())

    def add_shadow(self):
        groups = gp.GroupsPicker().get_groups(gp.GroupType.Visible)
        rect = self.sprite.rect
        self.shadow = Shadow(groups, (14, 8), midbottom=rect.midbottom)

    def update_shadow(self, dt):
        rect = self.sprite.rect
        self.shadow.hitbox.center = rect.midbottom
        self.shadow.update(dt)

    def weapon_rotation_point(self):
        x = self.hitbox.centerx
        y = self.hitbox.centery + 4
        return (x, y)

    def update(self, dt):
        super().update(dt)
        # self.wall_hirbox.center = self.hitbox.center
        self.state_machine.update(dt)
        self._weapon.update(dt, self.weapon_rotation_point())
        self.update_shadow(dt)
        self.animate()
