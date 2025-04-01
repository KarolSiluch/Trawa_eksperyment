from gameplay.tiles.tile import Tile


class TileMap:
    def __init__(self, tile_size=16) -> None:
        self.tile_size: int = tile_size
        self.tile_map: dict[tuple][list[Tile]] = {}
        self.offgrid_tiles = []

    def add(self, tile: Tile, offgrid_tile):
        if offgrid_tile:
            self.offgrid_tiles.append(tile)
            return None

        x = tile.hitbox.centerx // self.tile_size
        y = tile.hitbox.centery // self.tile_size
        if not (x, y) in self.tile_map.keys():
            self.tile_map[(x, y)] = [tile]
        else:
            self.tile_map[(x, y)].append(tile)
        return (x, y)

    def tiles(self) -> list[Tile]:
        tiles = []
        for layer in self.tile_map.values():
            tiles.extend(layer)
        tiles.extend(self.offgrid_tiles)
        return tiles

    def grid_tiles_around(self, point: tuple[float], radius: int = 1) -> list[Tile]:
        x_index = point[0] // self.tile_size
        y_index = point[1] // self.tile_size

        tiles = []

        for y_offset in range(-radius, radius + 1):
            for x_offset in range(-radius, radius + 1):
                x, y = x_index + x_offset, y_index + y_offset
                if not (x, y) in self.tile_map.keys():
                    continue
                tiles.extend(self.tile_map[(x, y)])
        return tiles

    def all_tiles_around(self, point: tuple[float], radius: int = 1) -> list[Tile]:
        tiles = self.grid_tiles_around(point, radius)
        tiles.extend(self.offgrid_tiles)
        return tiles

    def update(self, dt, player_center, *args):
        for tile in self.all_tiles_around(player_center, 20):
            tile.update(dt, *args)

    def get_collisions(self, obj: Tile, radius: int = 1):
        collisions: list[Tile] = []

        for tile in self.all_tiles_around(obj.hitbox.center, radius):
            if obj is tile:
                continue
            if not obj.hitbox.colliderect(tile.hitbox):
                continue
            collisions.append(tile)

        return collisions

    def remove_internal(self, sprite, place):
        if not place:
            if sprite not in self.offgrid_tiles:
                return
            self.offgrid_tiles.remove(sprite)
        else:
            if sprite not in self.tile_map[place]:
                return
            self.tile_map[place].remove(sprite)
            if len(self.tile_map[place]) == 0:
                del self.tile_map[place]
