import pygame, os

BASE_IMAGE_PATH = 'data/images/'

def load_image(path, colorkey=(0, 0, 0)):
  img = pygame.image.load(BASE_IMAGE_PATH + path).convert() #convert() makes img more efficient for pygame
  img.set_colorkey(colorkey)
  return img

def load_images(path, colorkey=(0, 0, 0)):
  images = []
  for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)): #sorted because tile type depends on this order
    img = load_image(path + '/' + img_name)
    images.append(img)
  return images