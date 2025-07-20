import pygame
import random

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Blaster - Coded by Amazing")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
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

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def draw_restart_button():
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
    pygame.draw.rect(screen, GREEN, button_rect)
    draw_text("RESTART", small_font, BLACK, screen, WIDTH//2 - 55, HEIGHT//2 + 10)
    return button_rect

def reset_game():
    global alien, bullets, score, game_over
    alien = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
    bullets = []
    score = 0
    game_over = False

# Game variables
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 50)
alien = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
bullets = []
score = 0
game_over = False

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 5, player.top, 10, 20)
                bullets.append(bullet)
                shoot_sound.play()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_restart_button().collidepoint(event.pos):
                    reset_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 5

    if not game_over:
        alien.y += 3

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 10
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                explosion_sound.play()
                alien = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
                score += 1
            elif bullet.bottom < 0:
                bullets.remove(bullet)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Draw player and alien
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, PINK, alien)

        # Game over check
        if alien.bottom >= HEIGHT:
            game_over = True

    # Draw score
    draw_text(f"Score: {score}", small_font, WHITE, screen, 10, 10)

    # Show Game Over screen
    if game_over:
        draw_text("GAME OVER", font, WHITE, screen, WIDTH//2 - 120, HEIGHT//2 - 60)
        draw_restart_button()

    pygame.display.flip()

pygame.quit()
