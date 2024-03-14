import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()
        self.status = "down"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

    def import_assets(self):
        self.animations = {
            'down': [], 'left': [], 'right': [], 'up': [],
            'down_idle': [], 'left_idle': [], 'right_idle': [], 'up_idle': [],
        }
        for animation in self.animations.keys():
            path = f'./graphics/character/{animation}/'
            self.animations[animation] = import_folder(path)

    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
            self.status = 'down'
        elif keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
            self.status = 'up'
        else:
            self.direction.y = 0

    def get_state(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'


    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            self.pos.x += self.direction.x * self.speed * dt
            self.rect.centerx = self.pos.x

            self.pos.y += self.direction.y * self.speed * dt
            self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_state()
        self.animate(dt)
