class Foundation:
    def __init__(self, groups, type: str, offgrid_tile: bool = False) -> None:
        self.__g = {}
        self.tile_type = type
        self.offgrid_tile = offgrid_tile
        self.__add_to_groups__(groups, offgrid_tile)

    def __add_to_groups__(self, groups: list, offgrid_tile: bool) -> None:
        for group in groups:
            place = group.add(self, offgrid_tile)
            self.__g[group] = place

    def kill(self):
        for group, place in self.__g.items():
            group.remove_internal(self, place)
