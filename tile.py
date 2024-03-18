import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/map/objects/TilesetNature.png').convert_alpha()
        # get only the part from pixel 16x16 to 16x32
        self.image = self.image.subsurface((16*6, 16*14, 16, 16))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
