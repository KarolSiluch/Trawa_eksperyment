from pygame import Surface
from gameplay.tiles.tile import Tile


class EditorTile(Tile):
    def __init__(self, groups, type: str, variant: int, image: Surface, sort_y_offset: int = 0,
                 offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, **pos)
        self._variant = variant
        self._created_position = pos

    @property
    def variant(self):
        return self._variant

    @property
    def created_position(self):
        return self._created_position
