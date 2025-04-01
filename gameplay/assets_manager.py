from gameplay.animation.animation import Animation
import pygame


class AssetsManager:
    @classmethod
    def init(cls):
        cls._assets = {
            'player': {
                'idle': Animation(cls.import_cut_graphics((5, 1), 'assets/game/player/idle.png'), animation_speed=7),
                'run': Animation(cls.import_cut_graphics((4, 1), 'assets/game/player/run.png'), animation_speed=9)
            },
            'weapons': {
                'ak': cls.load_image('assets/game/weapons/ak.png'),
                'bullet': cls.load_image('assets/game/weapons/bullet.png')
            },
            'tiles': {
                'wall': cls.import_cut_graphics((3, 4), 'assets/game/tiles/walls.png'),
                'grass': cls.import_cut_graphics((6, 1), 'assets/game/grass/grass.png')
            }
        }

    @staticmethod
    def load_image(path) -> pygame.Surface:
        return pygame.image.load(path).convert_alpha()

    @classmethod
    def import_cut_graphics(cls, image_grid: tuple[int], path):
        combined_image = cls.load_image(path)
        image_width = int(combined_image.get_width() / image_grid[0])
        image_height = int(combined_image.get_height() / image_grid[1])
        result = []
        for y in range(image_grid[1]):
            for x in range(image_grid[0]):
                image = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
                offset = (-x * image_width, -y * image_height)
                image.blit(combined_image, offset)
                result.append(image)
        return result

    def get(self, *args):
        result = self._assets.get(args[0])
        for arg in args[1::]:
            result = result.get(arg)
        return result
