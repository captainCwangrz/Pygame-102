import pygame, sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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
      'Stone' : load_images('tiles/stone'),
      'Background' : load_image('background.png'),
      'Clouds' : load_images('clouds'),
      'Player/idle' : Animation(load_images('entities/player/idle'), frame_duration = 6),
      'Player/run' : Animation(load_images('entities/player/run'), frame_duration = 4),
      'Player/jump' : Animation(load_images('entities/player/jump')),
      'Player/slide' : Animation(load_images('entities/player/slide')),
      'Player/wall_slide' : Animation(load_images('entities/player/wall_slide'))
    }

    self.player = Player(self, (50, 50), (8, 15))
    self.movement = [False, False] #left, right
    self.scroll = [0, 0] 

    self.tilemap = Tilemap(self)
    self.tilemap.load('map.json')
    self.clouds = Clouds(self.assets['Clouds'], count = 16)

  def run(self):
    while True:
      self.clock.tick(60)

      self.scroll[0] += (self.player.rect().centerx - self.display.get_width() // 2 - self.scroll[0]) / 30
      self.scroll[1] += (self.player.rect().centery - self.display.get_height() // 2 - self.scroll[1]) / 30
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

      self.display.blit(self.assets['Background'], (0, 0))
      self.clouds.update()
      self.clouds.render(self.display, offset = render_scroll)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_SPACE:
            self.player.velocity[1] = -3
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False

  
      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, offset = render_scroll)
      self.tilemap.render(self.display, offset = render_scroll)
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Game().run()