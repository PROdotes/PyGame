import pygame

TILE_SIZE = 32

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacle_sprites):
        super().__init__(group)
        self.import_assets()
        self.status = "down"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        self.obstacle_sprites = obstacle_sprites

    def import_assets(self):
        self.animations = {
            'down': [], 'up': [], 'left': [], 'right': [],
            'down_idle': [], 'up_idle': [], 'left_idle': [], 'right_idle': [],
        }
        walk_sheet = pygame.image.load('./graphics/character/Walk.png').convert_alpha()
        walk_sheet = pygame.transform.scale(walk_sheet, (TILE_SIZE*4, TILE_SIZE*4))
        idle_sheet = pygame.image.load('./graphics/character/Idle.png').convert_alpha()
        idle_sheet = pygame.transform.scale(idle_sheet, (TILE_SIZE*4, TILE_SIZE))
        # walk sheet has 4 frames and idle sheet has 1 frame
        # each frame is 16x16
        self.animations['down_idle'].append(idle_sheet.subsurface((0*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))
        self.animations['up_idle'].append(idle_sheet.subsurface((1*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))
        self.animations['left_idle'].append(idle_sheet.subsurface((2*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))
        self.animations['right_idle'].append(idle_sheet.subsurface((3*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))

        for i in range(4):
            self.animations['down'].append(walk_sheet.subsurface((0*TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)))
            self.animations['up'].append(walk_sheet.subsurface((1*TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)))
            self.animations['left'].append(walk_sheet.subsurface((2*TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)))
            self.animations['right'].append(walk_sheet.subsurface((3*TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)))





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
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery



    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_state()
        self.animate(dt)
