import pygame
import random
import sys

# -------------------------
# CONFIG
# -------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1
ENEMY_DROP = 30
ENEMY_ROWS = 4
ENEMY_COLS = 8

# -------------------------
# INIT
# -------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# -------------------------
# CLASSES
# -------------------------
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


# -------------------------
# GAME SETUP
# -------------------------
player = Player()
bullets = []
enemies = []

# Create enemy grid
def create_enemy_grid():
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = 80 + col * 70
            y = 50 + row * 50
            enemies.append(Enemy(x, y))

enemy_direction = 1
score = 0

create_enemy_grid()

# -------------------------
# GAME LOOP
# -------------------------
running = True
while running:
    clock.tick(FPS)

    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))

    # ---- INPUT ----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_RIGHT]:
        player.move(1)

    # ---- UPDATE BULLETS ----
    for bullet in bullets[:]:
        bullet.update()
        if bullet.off_screen():
            bullets.remove(bullet)

    # ---- UPDATE ENEMIES ----
    move_down = False
    for enemy in enemies:
        enemy.rect.x += enemy_direction * ENEMY_SPEED
        if enemy.rect.right >= WIDTH or enemy.rect.left <= 0:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.rect.y += ENEMY_DROP

    # ---- COLLISIONS ----
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break
    for enemy in enemies:
        if enemy.rect.colliderect(player.rect):
            running = False
            break

    if len(enemies) == 0:
        create_enemy_grid()
        ENEMY_SPEED = ENEMY_SPEED + 1

    # ---- GAME OVER ----
    for enemy in enemies:
        if enemy.rect.bottom >= HEIGHT:
            running = False



    # ---- DRAW ----
    screen.fill((0, 0, 0))

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)


    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# -------------------------
# CLEANUP
# -------------------------
pygame.quit()
sys.exit()