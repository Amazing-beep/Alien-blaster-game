import pygame
import random

# Initialize pygame
pygame.init()


# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Blaster - Coded by Amazing")

background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load sounds
shoot_sound = pygame.mixer.Sound("Sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("Sounds/explosion.wav")

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Load images (make sure they are in the Images/ folder)
player_img = pygame.image.load("shooting.png").convert_alpha()
alien_img = pygame.image.load("alien.png").convert_alpha()
bullet_img = pygame.Surface((10, 20))  # simple white bullet
bullet_img.fill(WHITE)

# --- SPRITE CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (110, 110))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(alien_img, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), 0))
    
    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Function to draw restart button
def draw_restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, GREEN, button_rect)
    draw_text("RESTART", small_font, BLACK, screen, WIDTH // 2 - 55, HEIGHT // 2 + 10)
    return button_rect

# Game reset function
def reset_game():
    global score, game_over
    score = 0
    game_over = False
    all_sprites.empty()
    aliens.empty()
    bullets.empty()
    all_sprites.add(player)

# Sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Variables
score = 0
game_over = False
alien_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(alien_spawn_timer, 2000)  # Spawn alien every second

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()
            if event.type == alien_spawn_timer:
                alien = Alien()
                all_sprites.add(alien)
                aliens.add(alien)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_restart_button().collidepoint(event.pos):
                    reset_game()
    
    if not game_over:
        # Update all sprites
        all_sprites.update()
        
        # Collision: Bullet hits alien
        hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
        for hit in hits:
            explosion_sound.play()
            score += 1
        
        # Collision: Alien reaches bottom
        for alien in aliens:
            if alien.rect.bottom >= HEIGHT:
                game_over = True
    
    # Draw sprites
    all_sprites.draw(screen)
    draw_text(f"Score: {score}", small_font, WHITE, screen, 10, 10)
    
    if game_over:
        draw_text("GAME OVER", font, WHITE, screen, WIDTH // 2 - 120, HEIGHT // 2 - 60)
        draw_restart_button()

    pygame.display.flip()

pygame.quit()
