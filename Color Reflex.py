import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Match Game")

# Colors
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Orange": (255, 165, 0),
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.Font(None, 74)

# Game Variables
score = 0
lives = 9  # Default for Catlife mode
current_text = ""
current_font_color = None
game_mode = "text_mode"  # Modes: 'text_mode', 'button_mode'
difficulty = "catlife"  # Modes: 'death', 'catlife', 'reincarnation'

# Timing
color_change_interval = 1000  # 1 second
last_color_change = pygame.time.get_ticks()

# Button properties
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 50)
button_color = random.choice(list(COLORS.values()))


def get_random_color_and_text():
    color_name = random.choice(list(COLORS.keys()))
    font_color = random.choice(list(COLORS.values()))
    return color_name, font_color


def render_text_and_button():
    # Clear screen
    screen.fill(WHITE)

    # Render text
    text_surface = font.render(current_text, True, current_font_color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text_surface, text_rect)

    # Render button
    pygame.draw.rect(screen, button_color, button_rect)

    # Render score and lives
    score_surface = font.render(f"Score: {score}", True, BLACK)
    lives_surface = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_surface, (20, 20))
    screen.blit(lives_surface, (WIDTH - 200, 20))


def check_match():
    global score, lives

    if game_mode == "text_mode":
        # Check if text matches font color
        if COLORS[current_text] == current_font_color:
            return True
    elif game_mode == "button_mode":
        # Check if button color matches text
        if COLORS[current_text] == button_color:
            return True

    return False


def handle_input():
    global score, lives

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                if check_match():
                    score += 1
                else:
                    lives -= 1
                    if difficulty == "death" or (difficulty == "reincarnation" and lives <= 2) or lives <= 0:
                        game_over()


def game_over():
    global running

    screen.fill(WHITE)
    game_over_surface = font.render("Game Over!", True, BLACK)
    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    running = False


# Main Game Loop
running = True
current_text, current_font_color = get_random_color_and_text()

while running:
    # Handle input
    handle_input()

    # Update game state
    now = pygame.time.get_ticks()
    if now - last_color_change > color_change_interval:
        last_color_change = now
        current_text, current_font_color = get_random_color_and_text()
        if game_mode == "button_mode":
            button_color = random.choice(list(COLORS.values()))

    # Render everything
    render_text_and_button()
    pygame.display.flip()

