import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()
        self.status = "down"
        self.image = self.animations[self.status]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

    def import_assets(self):
        self.animations = {
            'down': [],
            'left': [],
            'right': [],
            'up': [],
        }
        for animation in self.animations.keys():
            image = f'./graphics/character/{animation}.png'
            self.animations[animation] = pygame.image.load(image).convert_alpha()
            # set the image size to 32x32
            self.animations[animation] = pygame.transform.scale(self.animations[animation], (32, 32))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
        elif keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
        else:
            self.direction.y = 0

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
