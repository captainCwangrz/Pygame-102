class Tilemap:
  def __init__(self, game, tile_size=16):
    self.game = game
    self.tile_size = tile_size
    self.tilemap = {}
    self.offgrid_tiles = []  #not perfectly aligned sutff?

    for i in range(10):
      self.tilemap[str(3 + i) + ';10'] = {'type' : 'Grass', 'variant' : 1, 'pos' : (3 + i, 10)}
      self.tilemap['10;' + str(5 + i)] = {'type' : 'Stone', 'variant' : 1, 'pos' : (10, 5 + i)}
  
  def render(self, surf):
    # Render offgrid stuff first because they are usually bg decors
    for tile in self.offgrid_tiles: 
      surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos']) #no * tile_size cuz...off grid?
    
    for tile in self.tilemap.values():
      loc = tile['pos']
      image = self.game.assets[tile['type']][tile['variant']]
      surf.blit(image, (loc[0]*self.tile_size, loc[1]*self.tile_size))
      
  