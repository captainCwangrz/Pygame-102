import pygame, sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Ninja Game")
    self.clock = pygame.time.Clock()

    self.assets = {
      'Player' : load_image('entities/player.png')
    }
    self.player = PhysicsEntity(self, 'Player', (50, 50), (8, 15))
    self.movement = [False, False] #up, down

  def run(self):
    while True:
      self.clock.tick(60)
      self.screen.fill((14, 219, 228))

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
      self.player.render(self.screen)

      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Game().run()