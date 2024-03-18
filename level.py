import pygame
from player import Player
from map import WORLD_MAP
from tile import Tile


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                if col == 'x':
                    Tile((col_index * 32, row_index * 32),[self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((col_index * 32, row_index * 32), [self.visible_sprites], self.obstacle_sprites)


    def run(self, dt):
        self.display_surface.fill('black')
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(dt)
