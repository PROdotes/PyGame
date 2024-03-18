import pygame
from settings import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacle_sprites):
        super().__init__(group)
        self.import_assets()
        self.status = "down"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_offset_y = -20
        self.hitbox_offset_x = -2
        self.hitbox = self.rect.inflate(self.hitbox_offset_x, self.hitbox_offset_y)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
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
        self.update_pos()
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.update_pos()
        self.collision('vertical')



    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.left + self.hitbox_offset_x/2
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.left + self.hitbox_offset_x/2
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.top + self.hitbox_offset_y/2
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.top + self.hitbox_offset_y/2
                self.update_pos()



    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_state()
        self.animate(dt)

    def update_pos(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.hitbox.center = self.rect.center
