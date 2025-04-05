import pygame
from random import choice

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 8
BALL_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
title = pygame.display.set_caption("pong.py")
clock = pygame.time.Clock()

player = pygame.Rect((10, 250, 10, 80))
enemy = pygame.Rect((780, 250, 10, 80))

ball_surface = pygame.Surface((15, 15))
ball_rect = ball_surface.get_rect()
ball_rect.topleft = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # Spawn ball in center of screen
ball_velocity = pygame.Vector2(choice([-1, 1]) * BALL_SPEED, choice([-1, 1]) * BALL_SPEED)
ball_colors = ["white", "blue", "red"]
ball_surface.fill(ball_colors[0])

def draw_net():
    for y in range(0, SCREEN_HEIGHT, 10):
        rect = pygame.Rect(SCREEN_WIDTH // 2, y, 1, 5)
        pygame.draw.rect(screen, (100, 100, 100), rect)

def display_message(font, text, size, color, y_offset = 0, centered = True, position = (0,0)):
    font = pygame.font.SysFont(font, size)
    message = font.render(text, True, color)
    if centered:
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    else:
        message_rect = message.get_rect(topleft=position)
    screen.blit(message, message_rect)

def welcome_screen():
    pass


def game_over():
    pass

def main():
    player_score = 0
    enemy_score = 0

    running = True
    while running:

        screen.fill("black") # Clear screen each frame

        draw_net() # Draw "net" of repeating lines to divide player & enemy sides

        pygame.draw.rect(screen, "white", player)
        pygame.draw.rect(screen, "white", enemy)
        screen.blit(ball_surface, ball_rect) # Use surface & blit for ball to allow color changing

        # Display Title and Score text
        display_message("segoeui", f"pong.py", 38, "white", -275, True)
        display_message("segoeui", f"Player Score : {player_score}", 26, "white", centered=False, position=(SCREEN_WIDTH // 10, 5))
        display_message("segoeui", f"Enemy Score : {enemy_score}", 26, "white", centered=False, position=(SCREEN_WIDTH - 250, 5))

        ball_rect.x += ball_velocity.x
        ball_rect.y += ball_velocity.y

        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_velocity.y *= -1  # Reverse vertical direction
        
        if player.colliderect(ball_rect):
            player_score += 1
            ball_surface.fill(ball_colors[1])
            ball_rect.left = player.right # Prevent ball sticking
            ball_velocity.x *= -1 # Reverse horizontal direction

            offset = (ball_rect.centery - player.centery) / (player.height / 2)
            ball_velocity.y = BALL_SPEED * offset

            if abs(ball_velocity.y) < BALL_SPEED:
                ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1) # Ensure ball stays at least at starting speed

        elif enemy.colliderect(ball_rect):
            enemy_score += 1
            ball_surface.fill(ball_colors[2])
            ball_rect.right = enemy.left
            ball_velocity.x *= -1 # 

            offset = (ball_rect.centery - enemy.centery) / (enemy.height / 2)
            ball_velocity.y = BALL_SPEED * offset

            if abs(ball_velocity.y) < BALL_SPEED:
                ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1)
        

        enemy.centery = ball_rect.y # Enemy 'follows' the ball

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.move_ip(0, -PLAYER_SPEED)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
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

if __name__ == "__main__":
    main()