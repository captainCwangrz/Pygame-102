import pygame

class PhysicsEntity:
  def __init__(self, game, e_type, pos, size):
    self.game = game
    self.type = e_type
    self.pos = list(pos) #prevent global edit and handles collections
    self.size = size
    self.velocity = [0, 0]
    self.collisions = {'UP' : False, 'DOWN' : False, 'LEFT' : False, 'RIGHT' : False}
  
  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def update(self, tilemap, movement=(0,0)):
    self.collisions = {'UP' : False, 'DOWN' : False, 'LEFT' : False, 'RIGHT' : False}

    frame_movement = (movement[0]+self.velocity[0], movement[1]+self.velocity[1])
    self.pos[0] += frame_movement[0]
    entity_rect = self.rect()
    for rect in tilemap.physics_tiles_around(self.pos):
      if rect.colliderect(entity_rect):
        if frame_movement[0] > 0:
          self.collisions['RIGHT'] = True
          entity_rect.right = rect.left
        if frame_movement[0] < 0:
          self.collisions['LEFT'] = True
          entity_rect.left = rect.right
        self.pos[0] = entity_rect.x
    
    self.pos[1] += frame_movement[1]
    entity_rect = self.rect()
    for rect in tilemap.physics_tiles_around(self.pos):
      if rect.colliderect(entity_rect):
        if frame_movement[1] > 0:
          self.collisions['DOWN'] = True
          entity_rect.bottom = rect.top
        if frame_movement[1] < 0:
          self.collisions['UP'] = True
          entity_rect.top = rect.bottom
        self.pos[1] = entity_rect.y
    
    if self.collisions['UP'] or self.collisions['DOWN']:
      self.velocity[1] = 0 # resets velocity when you hit a wall vertically
    
    #gravity with terminal v
    self.velocity[1] = min(5, self.velocity[1] + 0.1)

  def render(self, surf, offset = (0, 0)):
    surf.blit(self.game.assets[self.type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
  