from gameplay.tiles.tile import Tile
from gameplay.animation.animation import Animation
import pygame


class AnimatedTile(Tile):
    def __init__(self, groups, type: str, animations, first_state,
                 render_y_offset: int = 0, offgrid_tile: bool = False, **pos) -> None:
        self.animations = animations
        self.current_animation: Animation = self.animations[first_state].copy()
        super().__init__(groups, type, self.current_animation.img(), render_y_offset, offgrid_tile, **pos)

    def animate(self):
        self.sprite._master_image = self.current_animation.img()

    def change_animation(self, state):
        self.current_animation = self.animations[state].copy()


class Entity(AnimatedTile):
    def __init__(self, groups, type: str, animations, state_machine, first_state,
                 render_y_offset: int = 0, offgrid_tile: bool = False, **pos):
        super().__init__(groups, type, animations, first_state, render_y_offset, offgrid_tile, **pos)
        self.state_machine = state_machine(self, first_state)
        self.direction = pygame.Vector2()
        self.velocity = 150
        self.acceleration = pygame.Vector2()


# class Entity(Tile):
#     def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0,
#                  offgrid_tile: bool = False, **pos: tuple[int]) -> None:
#         super().__init__(groups, type, image, sort_y_offset, offgrid_tile, **pos)
#         self.direction = pygame.Vector2()
#         self.velocity = 150
#         self.acceleration = pygame.Vector2()
