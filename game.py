import pygame, sys

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Ninja Game")
    self.clock = pygame.time.Clock()

    self.img = pygame.image.load('data/images/clouds/cloud_1.png')
    self.img.set_colorkey((0, 0, 0)) #turn a specific color to transparent
    self.img_pos = [160, 0]
    self.movement = [False, False] #up, down
    self.collision_area = pygame.Rect(160,200,100,100)

  def run(self):
    while True:
      self.clock.tick(60)
      self.screen.fill((14, 219, 228))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            self.movement[0] = True
          if event.key == pygame.K_DOWN:
            self.movement[1] = True
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_UP:
            self.movement[0] = False
          if event.key == pygame.K_DOWN:
            self.movement[1] = False

      
      self.img_pos[1] += (self.movement[1] - self.movement[0]) * 2
      img_rect = self.img.get_rect(topleft = self.img_pos)
      
      if (img_rect.colliderect(self.collision_area)):
        pygame.draw.rect(self.screen, (255, 0 ,0), self.collision_area)
      else:
        pygame.draw.rect(self.screen, (0, 255, 0 ), self.collision_area)
      
      
      self.screen.blit(self.img, self.img_pos)
      pygame.draw.rect(self.screen, (0, 0, 255), img_rect, 2)

      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Game().run()