import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, game):
        super().__init__()
        self.game = game
        self.size = size
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()
        
        game.all_sprites.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1
            if self.frame == 8:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.Surface((30, 30))
                self.image.fill((255, self.frame * 30, 0))
                self.rect = self.image.get_rect(center=center)
                self.last_update = now