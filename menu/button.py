import pygame
from screen import ScreenSettings
from math import cos, pi
from game import Gameplay


class Button:
    def __init__(self, image: pygame.Surface, pos: tuple[int], button_id: int, action) -> None:
        self._screen_settings = ScreenSettings()
        self._image = image
        self._id = button_id
        self._action = action
        self.rect = self._image.get_frect(center=pos)
        self.pos = pos

    @property
    def id(self):
        return self._id

    def click(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self._action()


class ActionButton(Button):
    def __init__(self, image, button_id, action):
        super().__init__(image, (0, 0), button_id, action)
        self.x_offset = 0

    def update(self, dt, current_id):
        self.rect.centerx += (self.pos[0] - self.rect.centerx) * dt * 10
        self.rect.centery += (self.pos[1] - self.rect.centery) * dt * 10

        id_offset = self._id - current_id
        x = 60 + cos(id_offset) * 20 + self.x_offset
        y = int(self._screen_settings.get_height() // 2) + id_offset * 50
        self.pos = (x, y)

        if id_offset == 0:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.x_offset = 20
            else:
                self.x_offset = 0

    def render(self):
        image = self._image
        alpha = 255 - abs(self._screen_settings.get_height() // 2 - self.rect.centery) * 4
        image.set_alpha(alpha)
        self._screen_settings.screen.blit(image, self.rect)


class ArrowButton(Button):
    def __init__(self, image, pos, button_id, action):
        super().__init__(image, pos, button_id, action)
        self.render_ofset = 0

    def update(self, dt):
        self.render_ofset = cos(self.id * pi + pygame.time.get_ticks() / 300) * 2

    def render(self):
        self._screen_settings.screen.blit(self._image, (self.rect.x, self.rect.y + self.render_ofset))


class ButtonManager:
    @staticmethod
    def import_asset(button_type):
        path = 'assets/lobby/{type}.png'
        image = pygame.image.load(path.format(type=button_type)).convert_alpha()
        return image

    def __init__(self):
        self._screen_settings = ScreenSettings()
        button_image = self.import_asset('button')
        arrow = self.import_asset('arrow')

        self._buttons = [
            ActionButton(button_image, 0, lambda: print('options')),
            ActionButton(button_image, 1, lambda: Gameplay().main_loop()),
            ActionButton(button_image, 2, lambda: print('credits')),
        ]

        pos = (80, self._screen_settings.get_height() // 2 - 100)
        self._arrow_up = ArrowButton(arrow, pos, 0, lambda: self.change_id(1))
        pos = (80, self._screen_settings.get_height() // 2 + 100)
        self._arrow_down = ArrowButton(pygame.transform.flip(arrow, False, True), pos, 1, lambda: self.change_id(-1))

        self._button_id = int(len(self._buttons) / 2)

    def change_id(self, x: int):
        self._button_id = sorted([0, self._button_id + x, len(self._buttons) - 1])[1]

    def update(self, dt):
        for button in self._buttons:
            button.update(dt, self._button_id)
        self._arrow_down.update(dt)
        self._arrow_up.update(dt)

    def render(self):
        for offset in range(-1, 2):
            if 0 <= self._button_id + offset < len(self._buttons):
                self._buttons[self._button_id + offset].render()
        self._arrow_down.render()
        self._arrow_up.render()

    def click(self):
        self._buttons[self._button_id].click()
        self._arrow_down.click()
        self._arrow_up.click()
