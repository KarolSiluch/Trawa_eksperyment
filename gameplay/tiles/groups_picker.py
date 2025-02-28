from enum import Enum
from gameplay.tiles.tilemap import TileMap


class GroupType(Enum):
    Visible = 1
    Collidable = 2
    Grass = 3
    Bullets = 4
    ProceduralParticles = 5
    Trees = 6
    Activitable = 7
    Enemy = 8
    HitableEntities = 9
    ContactDamage = 10


class GroupsPicker:
    groups = None

    @classmethod
    def init(cls, groups) -> None:
        cls.groups = groups

    def __init__(self):
        if not self.groups:
            raise AttributeError('list of groups has not been defined')

    def get_groups(self, *group_types) -> list[TileMap]:
        sprite_groups = []
        for type in group_types:
            sprite_groups.append(self.groups[type])
        return sprite_groups

    def get_group(self, type: GroupType) -> TileMap:
        return self.groups[type]
