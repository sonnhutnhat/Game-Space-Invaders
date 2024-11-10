import pygame
import random
from alien_bullet import AlienBullet

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load(f"img/alien{random.randint(1,5)}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000  # 2 giây

        game.all_sprites.add(self)
        game.aliens.add(self)

    def update(self):
        self.rect.x += self.speed * self.direction
        
        if self.rect.right > 600 or self.rect.left < 0:
            self.direction *= -1
            self.rect.y += 25

        # Logic bắn đạn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            if random.random() < 0.3:  # 30% khả năng bắn
                self.shoot()
            self.last_shot = now

    def shoot(self):
        bullet = AlienBullet(self.rect.centerx, self.rect.bottom, 5, self.game)
