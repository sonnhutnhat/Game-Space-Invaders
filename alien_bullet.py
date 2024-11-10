import pygame

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, game):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0))  # Màu đỏ cho đạn Alien
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
        game.all_sprites.add(self)
        game.alien_bullets.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()
