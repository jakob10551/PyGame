import pygame
import csv
import sys

# --- CONFIG & INIT ---
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_DROP = 30
ENEMY_ROWS = 4
ENEMY_COLS = 8

RUN_COUNT = 0
ADD_SCORE = 10




# --- CLASSES ---
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 30)
        self.speed = PLAYER_SPEED

    def move(self, dx):
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 10)

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)

    def off_screen(self):
        return self.rect.y < 0


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


# --- HELPER FUNCTIONS ---
def get_top_score(filename="high_scores.csv"):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            scores = [int(row[1]) for row in reader if row]
            return max(scores) if scores else 0
    except (FileNotFoundError, ValueError):
        return 0


def create_enemy_grid(enemies):
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            enemies.append(Enemy(80 + col * 70, 50 + row * 50))


# -------------------------
# PHASE 1: THE ACTUAL GAME
# -------------------------
def run_game():
    global ADD_SCORE
    player = Player()
    bullets = []
    enemies = []
    create_enemy_grid(enemies)

    current_enemy_speed = 2  # Start speed
    enemy_direction = 1
    score = 0
    high_score = get_top_score()
    game_running = True

    while game_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.move(-1)
        if keys[pygame.K_RIGHT]: player.move(1)

        for bullet in bullets[:]:
            bullet.update()
            if bullet.off_screen(): bullets.remove(bullet)

        move_down = False
        for enemy in enemies:
            enemy.rect.x += enemy_direction * current_enemy_speed
            if enemy.rect.right >= WIDTH or enemy.rect.left <= 0: move_down = True

        if move_down:
            enemy_direction *= -1
            for enemy in enemies: enemy.rect.y += ENEMY_DROP

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += ADD_SCORE
                    if score > high_score: high_score = score
                    break

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect) or enemy.rect.bottom >= HEIGHT:

                game_running = False

        if not enemies:

            create_enemy_grid(enemies)
            ADD_SCORE += 10
            current_enemy_speed += 1

        screen.fill((0, 0, 0))
        player.draw(screen)
        for b in bullets: b.draw(screen)
        for e in enemies: e.draw(screen)

        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        hi_surf = font.render(f"High Score: {high_score}", True, (255, 255, 0))
        screen.blit(score_surf, (10, 10))
        screen.blit(hi_surf, hi_surf.get_rect(topright=(WIDTH - 10, 10)))

        pygame.display.flip()

    return score


# -------------------------
# PHASE 2: NAME ENTRY
# -------------------------
def save_score_screen(score):
    user_text = ""
    typing = True
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open("high_scores.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([user_text if user_text else "Player", score])
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 10:
                        user_text += event.unicode

        screen.fill((20, 20, 20))
        screen.blit(font.render(f"GAME OVER! Score: {score}", True, (255, 0, 0)), (WIDTH // 2 - 150, 200))
        screen.blit(font.render(f"Enter Name: {user_text}", True, (255, 255, 255)), (WIDTH // 2 - 150, 260))
        screen.blit(font.render("Press Enter to Save", True, (100, 100, 100)), (WIDTH // 2 - 150, 320))
        pygame.display.flip()


# -------------------------
# PHASE 3: RESTART MENU
# -------------------------
def main_menu():
    while True:
        global ADD_SCORE
        final_score = run_game()
        save_score_screen(final_score)

        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            screen.blit(font.render("Press 'R' to Restart or 'Q' to Quit", True, (255, 255, 255)),
                        (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        ADD_SCORE = 10
                        waiting = False  # This goes back to run_game()
                    if event.key == pygame.K_q:
                        pygame.quit();
                        sys.exit()


if __name__ == "__main__":
    main_menu()