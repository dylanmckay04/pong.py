import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 8
BALL_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
title = pygame.display.set_caption("pong.py")

# Clock object needed to set framerate
clock = pygame.time.Clock()

player = pygame.Rect((10, 250, 10, 80))
enemy = pygame.Rect((780, 250, 10, 80))

# Spawn ball in center of screen
ball = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 10))
ball_velocity = pygame.Vector2(random.choice([-1, 1]) * BALL_SPEED, random.choice([-1, 1]) * BALL_SPEED)

font = pygame.font.SysFont("segoeui", 38, bold=False)
title_text = font.render("pong.py", True, "white")

def draw_net():
    for y in range(0, SCREEN_HEIGHT, 10):
        rect = pygame.Rect(SCREEN_WIDTH // 2, y, 1, 5)
        pygame.draw.rect(screen, (100, 100, 100), rect)

running = True
while running:

    screen.fill("black") # Clear screen each frame

    screen.blit(title_text, (SCREEN_WIDTH // 2.525, 0))

    draw_net() # Draw "net" of repeating lines to divide player & enemy sides

    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", enemy)
    pygame.draw.rect(screen, "white", ball)

    # TODO: MAKE BALL CHANGE COLOR WHEN HIT

    ball.x += ball_velocity.x
    ball.y += ball_velocity.y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_velocity.y *= -1  # Reverse vertical direction
    
    if player.colliderect(ball):
        ball.left = player.right # Prevent ball sticking
        ball_velocity.x *= -1 # Reverse horizontal direction

        offset = (ball.centery - player.centery) / (player.height / 2)
        ball_velocity.y = BALL_SPEED * offset

        if abs(ball_velocity.y) < BALL_SPEED:
            ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1) # Ensure ball stays at least at starting speed

    elif enemy.colliderect(ball):
        ball.right = enemy.left
        ball_velocity.x *= -1 # 

        offset = (ball.centery - enemy.centery) / (enemy.height / 2)
        ball_velocity.y = BALL_SPEED * offset

        if abs(ball_velocity.y) < BALL_SPEED:
            ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1)
    

    enemy.centery = ball.y # Enemy 'follows' the ball

    key = pygame.key.get_pressed()

    if key[pygame.K_w] or key[pygame.K_UP]:
        player.move_ip(0, -PLAYER_SPEED)
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        player.move_ip(0, PLAYER_SPEED)
    
    # Keep player in bounds of screen
    if player.top < 0:
        player.top = 0
    if player.bottom > SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit game
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()