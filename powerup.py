import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))  # Green for health
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 600)
        self.rect.y = 0
        self.speedy = 5
        
        game.all_sprites.add(self)
        game.powerups.add(self)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 800:
            self.kill()
        
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        if hits:
            hits[0].health = min(100, hits[0].health + 20)
            self.kill()