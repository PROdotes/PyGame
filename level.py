import pygame
from player import Player
from settings import WORLD_MAP
from tile import Tile


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                if col == 'x':
                    Tile((col_index * 32, row_index * 32), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((col_index * 32, row_index * 32), [self.visible_sprites],
                                         self.obstacle_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(dt)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
