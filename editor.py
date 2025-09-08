import pygame, sys
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2

class Editor:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((640, 480))
    self.display = pygame.Surface((320, 240)) # To be stretched
    pygame.display.set_caption("Editor")
    self.clock = pygame.time.Clock()

    self.assets = {
      'Decor' : load_images('tiles/decor'),
      'Grass' : load_images('tiles/grass'),
      'Large Decor' : load_images('tiles/large_decor'),
      'Stone' : load_images('tiles/stone'),
    }
    self.asset_group = list(self.assets) # list of keys
    self.current_group = 0
    self.current_variant = 0
    self.clicking = False
    self.right_clicking = False
    self.shift = False
    self.offgrid = False

    self.movement = [False, False, False, False] #left, right, up, down
    self.scroll = [0, 0] 

    self.tilemap = Tilemap(self)

    try:
      self.tilemap.load('map.json')
    except FileNotFoundError:
      print('No map data found.')

  def run(self):
    while True:
      self.clock.tick(60)
      self.display.fill((0,0, 0))
      
      self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
      self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      self.tilemap.render(self.display, offset = render_scroll)

      current_tile_img = self.assets[self.asset_group[self.current_group]][self.current_variant].copy()
      current_tile_img.set_alpha(100)

      mpos = pygame.mouse.get_pos()
      mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # mouse pixel pos corrected by RENDER_SCALE (display vs screen)
      tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))


      if self.offgrid:
        self.display.blit(current_tile_img, mpos)
      else:
        self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))

      if self.clicking and not self.offgrid:
        self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type' : self.asset_group[self.current_group], 'variant' : self.current_variant, 'pos' : tile_pos}
      
      if self.right_clicking:
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]
        for off_tile in self.tilemap.offgrid_tiles.copy():
          tile_img = self.assets[off_tile['type']][off_tile['variant']]
          tile_rect = pygame.Rect(off_tile['pos'][0] - self.scroll[0], off_tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
          if tile_rect.collidepoint(mpos):
            self.tilemap.offgrid_tiles.remove(off_tile)
          
          
      

      self.display.blit(current_tile_img, (5, 5))


      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: # 1 - left, 2 - wheel, 3 - right, 4 - scroll up, 5 - scroll down
          if event.button == 1:
            self.clicking = True
            if self.offgrid:
              self.tilemap.offgrid_tiles.append({'type' : self.asset_group[self.current_group], 'variant' : self.current_variant, 'pos' : (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
          if event.button == 3:
            self.right_clicking = True
          if self.shift:
            if event.button == 4:
              self.current_group = (self.current_group - 1) % (len(self.asset_group))
              self.current_variant = 0
            if event.button == 5:
              self.current_group = (self.current_group + 1) % ( len(self.asset_group))
              self.current_variant = 0
          else:
            if event.button == 4:
              self.current_variant = (self.current_variant - 1) % (len(self.assets[self.asset_group[self.current_group]]))
            if event.button == 5:
              self.current_variant = (self.current_variant + 1) % (len(self.assets[self.asset_group[self.current_group]]))
        
        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.clicking = False
          if event.button == 3:
            self.right_clicking = False
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_a:
            self.movement[0] = True
          if event.key == pygame.K_d:
            self.movement[1] = True
          if event.key == pygame.K_w:
            self.movement[2] = True
          if event.key == pygame.K_s:
            self.movement[3] = True
          if event.key == pygame.K_LSHIFT:
            self.shift = True
          if event.key == pygame.K_g:
            self.offgrid = not self.offgrid
          if event.key == pygame.K_t:
            self.tilemap.autotile()
          if event.key == pygame.K_o:
            self.tilemap.save('map.json')
        
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a:
            self.movement[0] = False
          if event.key == pygame.K_d:
            self.movement[1] = False
          if event.key == pygame.K_w:
            self.movement[2] = False
          if event.key == pygame.K_s:
            self.movement[3] = False
          if event.key == pygame.K_LSHIFT:
            self.shift = False

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

      pygame.display.flip() #safe full-page refresh, otherwise use update([rect_list])

Editor().run()