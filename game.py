import pygame, sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((640, 480))
    self.display = pygame.Surface((320, 240)) # To be stretched
    pygame.display.set_caption("Ninja Game")
    self.clock = pygame.time.Clock()

    self.assets = {
      'Player' : load_image('entities/player.png'),
      'Decor' : load_images('tiles/decor'),
      'Grass' : load_images('tiles/grass'),
      'Large Decor' : load_images('tiles/large_decor'),
      'Stone' : load_images('tiles/stone')
    }
    self.player = PhysicsEntity(self, 'Player', (50, 50), (8, 15))
    self.movement = [False, False] #up, down

    self.tilemap = Tilemap(self)

  def run(self):
    while True:
      self.clock.tick(60)
      self.display.fill((14, 219, 228))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False

      self.player.update((self.movement[1] - self.movement[0], 0))
      self.player.render(self.display)
      self.tilemap.render(self.display)
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Game().run()