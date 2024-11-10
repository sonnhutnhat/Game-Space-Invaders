import pygame
import json
import random
from player import Player
from alien import Alien
from bullet import Bullet
from powerup import PowerUp
from explosion import Explosion

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
HIGH_SCORES = 3
PAUSED = 4

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Invaders')
        self.load_assets()
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.level = 1
        self.score = 0
        self.create_sprite_groups()
        self.settings = self.load_settings()
        self.player = None
        self.username = "Player"
        self.high_scores = []  # Thay thế DB bằng danh sách điểm cao

    def load_assets(self):
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.bg = pygame.image.load("img/bg.png").convert()
        self.sounds = {
            'shoot': pygame.mixer.Sound("img/laser.wav"),
            'explosion': pygame.mixer.Sound("img/explosion.wav"),
            'powerup': pygame.mixer.Sound("img/explosion2.wav")
        }

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'sound_enabled': True,
                'music_enabled': True,
                'difficulty': 'normal'
            }

    def create_sprite_groups(self):
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == MENU:
                if event.key == pygame.K_SPACE:
                    self.start_game()
                elif event.key == pygame.K_h:
                    self.state = HIGH_SCORES
            elif self.state == PLAYING:
                if event.key == pygame.K_p:
                    self.state = PAUSED
                elif event.key == pygame.K_ESCAPE:
                    self.state = MENU
            elif self.state == PAUSED:
                if event.key == pygame.K_p:
                    self.state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = MENU
            elif self.state == GAME_OVER or self.state == HIGH_SCORES:
                if event.key == pygame.K_RETURN:
                    self.state = MENU

    def start_game(self):
        self.state = PLAYING
        self.level = 1
        self.score = 0
    
    # Xóa tất cả đối tượng hiện có
        self.all_sprites.empty()
        self.players.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.alien_bullets.empty()
    
        self.player = Player(self)  # Tạo đối tượng người chơi mới
        self.create_level()
        

    def game_over(self):
        self.state = GAME_OVER
        self.high_scores.append((self.username, self.score))  # Lưu điểm vào danh sách

    def spawn_powerup(self):
        if random.random() < 0.001:  # 5% chance each frame
            PowerUp(self)

    def handle_collisions(self):
        hits = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        for hit in hits:
            self.score += 100
            self.sounds['explosion'].play()
            Explosion(hit.rect.center, 'lg', self)
        
        hits = pygame.sprite.spritecollide(self.player, self.alien_bullets, True)
        for hit in hits:
            self.player.health -= 10
            self.sounds['explosion'].play()
            if self.player.health <= 0:
                self.game_over()

    def update(self):
        if self.state == PLAYING:
            self.all_sprites.update()
            self.handle_collisions()
            self.spawn_powerup()
            if len(self.aliens) == 0:
                self.level += 1
                self.create_level()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.all_sprites.draw(self.screen)
            self.draw_hud()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == HIGH_SCORES:
            self.draw_high_scores()
        elif self.state == PAUSED:
            self.draw_pause_menu()
        pygame.display.flip()

    def draw_menu(self):
        title = self.font_large.render('SPACE INVADERS', True, WHITE)
        play_btn = self.font_medium.render('Press SPACE to Play', True, WHITE)
        scores_btn = self.font_medium.render('Press H for High Scores', True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
        self.screen.blit(play_btn, (SCREEN_WIDTH//2 - play_btn.get_width()//2, 400))
        self.screen.blit(scores_btn, (SCREEN_WIDTH//2 - scores_btn.get_width()//2, 450))

    def draw_game_over(self):
        text = self.font_large.render('GAME OVER', True, WHITE)
        score = self.font_medium.render(f'Final Score: {self.score}', True, WHITE)
        restart = self.font_medium.render('Press ENTER to continue', True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300))
        self.screen.blit(score, (SCREEN_WIDTH//2 - score.get_width()//2, 400))
        self.screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 500))

    def draw_high_scores(self):
        title = self.font_large.render('HIGH SCORES', True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        for i, (name, score) in enumerate(sorted(self.high_scores, key=lambda x: x[1], reverse=True)[:10]):
            text = self.font_medium.render(f'{name}: {score}', True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
        back = self.font_medium.render('Press ENTER to return', True, WHITE)
        self.screen.blit(back, (SCREEN_WIDTH//2 - back.get_width()//2, 700))

    def draw_pause_menu(self):
        text = self.font_large.render('PAUSED', True, WHITE)
        resume = self.font_medium.render('Press P to Resume', True, WHITE)
        quit_text = self.font_medium.render('Press ESC to Quit', True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300))
        self.screen.blit(resume, (SCREEN_WIDTH//2 - resume.get_width()//2, 400))
        self.screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))

    def draw_hud(self):
        score_text = self.font_small.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        level_text = self.font_small.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(level_text, (10, 40))
        health_width = 200 * (self.player.health / 100)
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 70, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 70, health_width, 20))

    def create_level(self):
        for alien in self.aliens:
            alien.kill()
        for row in range(5):
            for col in range(10):
                x = 50 + col * 50
                y = 50 + row * 50
                Alien(x, y, self)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
            self.update()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
