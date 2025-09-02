import pygame

BASE_IMAGE_PATH = 'data/images/'

def load_image(path, colorkey=(0, 0, 0)):
  img = pygame.image.load(BASE_IMAGE_PATH+path).convert() #convert() makes img more efficient for pygame
  img.set_colorkey(colorkey)
  return img