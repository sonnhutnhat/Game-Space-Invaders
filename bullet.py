import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, game):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
        game.all_sprites.add(self)
        game.bullets.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > 800:
            self.kill()