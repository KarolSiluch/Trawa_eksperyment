class Animation:
    def __init__(self, images, animation_speed=5, loop=True):
        self.images = images
        self.loop = loop
        self.animation_speed = animation_speed
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.animation_speed, self.loop)

    def length(self):
        return len(self.images)

    # True: +, False: -
    def update(self, dt, direction: int):
        if self.loop:
            self.frame += direction * self.animation_speed * dt
        else:
            self.frame = min(self.frame + direction * self.animation_speed * dt, self.length() - 1)
            if self.frame >= self.length() - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame % (self.length() - 1))]


class SetAnimation:
    def __init__(self, images, loop=True):
        self.images = images
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return SetAnimation(self.images, self.loop)

    def length(self):
        return len(self.images)

    def update(self, dt, frame):
        self.frame = frame

    def img(self):
        return self.images[int(self.frame % (self.length() - 1))]
