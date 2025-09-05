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

class Animation:
  def __init__(self, images, frame_duration = 5, loop = True):
    self.images = images
    self.duration = frame_duration
    self.loop = loop
    self.frame_count = 0
    self.done = False

  def copy(self):
    return Animation(self.images, self.duration, self.loop)

  def update(self):
    if self.loop:
      self.frame_count = (self.frame_count + 1) % (self.duration * len(self.images))
    else:
      self.frame_count = min(self.frame_count + 1, self.duration * len(self.images) - 1)
      if self.frame_count >= self.duration * len(self.images) - 1:
        self.done = True

  def get_current_image(self):
    return self.images[self.frame_count // self.duration]