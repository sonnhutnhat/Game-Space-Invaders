import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("img/spaceship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 300
        self.rect.bottom = 780
        self.health = 100
        self.speed = 8
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        game.all_sprites.add(self)
        game.players.add(self)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        self.rect.clamp_ip(self.game.screen.get_rect())
        
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.shoot()
                self.last_shot = now

    def shoot(self):
        Bullet(self.rect.centerx, self.rect.top, -10, self.game)
        self.game.sounds['shoot'].play()