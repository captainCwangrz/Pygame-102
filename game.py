import pygame, sys

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Ninja Game")
    self.clock = pygame.time.Clock()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      self.clock.tick(60)
      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Game().run()