from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surface = pygame.transform.scale(image_surface, (32, 32))
            surface_list.append(image_surface)

    return surface_list
