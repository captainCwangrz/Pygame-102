import pygame

TILE_OFFSETS = ((0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1))
PHYSICS_TILES = {'Grass', 'Stone'}


class Tilemap:
  def __init__(self, game, tile_size=16):
    self.game = game
    self.tile_size = tile_size
    self.tilemap = {}
    self.offgrid_tiles = []  #not perfectly aligned sutff?

    for i in range(10):
      self.tilemap[str(3 + i) + ';10'] = {'type' : 'Grass', 'variant' : 1, 'pos' : (3 + i, 10)}
      self.tilemap['10;' + str(5 + i)] = {'type' : 'Stone', 'variant' : 1, 'pos' : (10, 5 + i)}
  
  def tiles_around(self, pos):
    tiles =[]
    tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) 
    for offset in TILE_OFFSETS:
      check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap: #ignors empty space
        tiles.append(self.tilemap[check_loc]) #adds the actual tile at that loc
    return tiles

  def physics_tiles_around(self, pos):
    rects = []
    for tile in self.tiles_around(pos):
      if tile['type'] in PHYSICS_TILES:
        rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
    return rects

  def render(self, surf, offset = (0, 0)):
    # Render offgrid stuff first because they are usually bg decors
    for tile in self.offgrid_tiles: 
      surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])) #no * tile_size cuz...off grid?
    
    for tile in self.tilemap.values():
      loc = tile['pos']
      image = self.game.assets[tile['type']][tile['variant']]
      surf.blit(image, (loc[0] * self.tile_size - offset[0], loc[1] * self.tile_size - offset[1]))
      
  