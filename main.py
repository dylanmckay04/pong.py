import pygame
import asyncio
from random import choice
from sys import exit

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 10
ENEMY_SPEED = 7
BALL_SPEED = 8
PLAYER_STARTING_COORDS = (10, 250)
ENEMY_STARTING_COORDS = (780, 250)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
title = pygame.display.set_caption("pong.py")
clock = pygame.time.Clock()

player = pygame.Rect((10, 250, 10, 80))
enemy = pygame.Rect((780, 250, 10, 80))



def draw_net():
    for y in range(0, SCREEN_HEIGHT, 10):
        rect = pygame.Rect(SCREEN_WIDTH // 2, y, 1, 5)
        pygame.draw.rect(screen, (100, 100, 100), rect)

def display_message(font, text, size, bold = False, color = "white", y_offset = 0, centered = True, position = (0,0)):
    font = pygame.font.SysFont(font, size, bold)
    message = font.render(text, True, color)
    if centered:
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    else:
        message_rect = message.get_rect(topleft=position)
    screen.blit(message, message_rect)

async def welcome_screen():
    while True:
        screen.fill("black")
        display_message("segoeui", "pong.py", 64, bold = True, y_offset = -20)
        display_message("segoeui", "press any key to play", 42, bold = False, y_offset = 100)
        display_message("segoeui", "'w' or '↑': move up", 20, bold=False, y_offset=220)
        display_message("segoeui", "'s' or '↓': move down", 20, bold=False, y_offset=245)
        display_message("segoeui", "'esc' or 'p' to pause", 20, bold=False, y_offset=270)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                return


async def game_lost():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    loss_sound = pygame.mixer.Sound("audio/loss.ogg")
    loss_sound.set_volume(0.1)
    loss_sound.play()
    
    while True:
        screen.fill("black")
        display_message("segoeui", "you lost!", 42, bold = True, y_offset = -20)
        display_message("segoeui", "press any key to play again", 32, bold = False, y_offset = 150)
        display_message("segoeui", "press 'esc' to exit", 21, bold = False, y_offset = 225)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                await main()

async def game_won():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    win_sound = pygame.mixer.Sound("audio/victory.ogg")
    win_sound.set_volume(0.1)
    win_sound.play()

    while True:
        screen.fill("black")
        display_message("segoeui", "you won!", 42, bold = True, y_offset = -20)
        display_message("segoeui", "press any key to play again", 32, bold = False, y_offset = 150)
        display_message("segoeui", "press 'Esc' to exit", 21, bold = False, y_offset = 225)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                await main()

def reset_ball_state(ball_rect, ball_surface, ball_velocity, ball_colors, player, enemy):
    player.x, player.y = PLAYER_STARTING_COORDS
    enemy.x, enemy.y = ENEMY_STARTING_COORDS
    ball_surface.fill(ball_colors[0])
    ball_rect.topleft = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    ball_velocity.xy = (0,0)
    starting_velocity = pygame.Vector2(choice([-1, 1]) * BALL_SPEED, choice([-1, 1]) * BALL_SPEED)
    return pygame.time.get_ticks(), starting_velocity

async def main():
    while True:
        await welcome_screen()

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()

        bounce_sound = pygame.mixer.Sound("audio/ball_bounce.ogg")
        bounce_sound.set_volume(0.1)
        score_sound = pygame.mixer.Sound("audio/score_sound.ogg")
        score_sound.set_volume(0.025)
        enemy_score_sound = pygame.mixer.Sound("audio/enemy_score.ogg")
        enemy_score_sound.set_volume(0.075)

        player_score = 0
        enemy_score = 0

        reset_ball = False
        reset_timer = pygame.time.get_ticks()
        ball_out_of_bounds = False

        ball_surface = pygame.Surface((15, 15))
        ball_rect = ball_surface.get_rect()
        ball_rect.topleft = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # Spawn ball in center of screen
        ball_velocity = pygame.Vector2(choice([-1, 1]) * BALL_SPEED, choice([-1, 1]) * BALL_SPEED)
        ball_colors = ["white", "blue", "red"]
        ball_surface.fill(ball_colors[0])

        running = True
        paused = False
        while running:
            screen.fill("black") # Clear screen each frame

            draw_net() # Draw "net" of repeating lines to divide player & enemy sides

            pygame.draw.rect(screen, "white", player)
            pygame.draw.rect(screen, "white", enemy)
            screen.blit(ball_surface, ball_rect) # Use surface & blit for ball to allow color changing

            # Display Title and Score text
            display_message("segoeui", "pong.py", 38, y_offset=-275, centered=True)
            display_message("segoeui", f"player score: {player_score}", 26, centered=False, position=(SCREEN_WIDTH // 10, 5))
            display_message("segoeui", f"enemy score: {enemy_score}", 26, centered=False, position=(SCREEN_WIDTH - 250, 5))

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False # Exit game
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                        paused = not paused

            if not paused:
                ball_rect.x += ball_velocity.x
                ball_rect.y += ball_velocity.y

                if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
                    bounce_sound.play()
                    ball_velocity.y *= -1  # Reverse vertical direction
                
                if player.colliderect(ball_rect):
                    bounce_sound.play()
                    ball_surface.fill(ball_colors[1])
                    ball_rect.left = player.right # Prevent ball sticking
                    ball_velocity.x *= -1 # Reverse horizontal direction

                    offset = (ball_rect.centery - player.centery) / (player.height / 2)
                    ball_velocity.y = BALL_SPEED * offset

                    if abs(ball_velocity.y) < BALL_SPEED:
                        ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1) # Ensure ball stays at least at starting speed

                elif enemy.colliderect(ball_rect):
                    bounce_sound.play()
                    ball_surface.fill(ball_colors[2])
                    ball_rect.right = enemy.left
                    ball_velocity.x *= -1

                    offset = (ball_rect.centery - enemy.centery) / (enemy.height / 2)
                    ball_velocity.y = BALL_SPEED * offset

                    if abs(ball_velocity.y) < BALL_SPEED:
                        ball_velocity.y = BALL_SPEED * (1 if ball_velocity.y > 0 else -1)
                
                # Increment score when ball hits a wall
                if not ball_out_of_bounds:
                    if ball_rect.right >= SCREEN_WIDTH:
                        score_sound.play()
                        player_score += 1
                        ball_out_of_bounds = True
                    elif ball_rect.left <= 0:
                        enemy_score_sound.play()
                        enemy_score += 1
                        ball_out_of_bounds = True
                
                # Reset ball when it hits a wall
                if ball_out_of_bounds and not reset_ball:
                    reset_timer, starting_velocity = reset_ball_state(ball_rect, ball_surface, ball_velocity, ball_colors, player, enemy)
                    reset_ball = True
                
                # Wait 1 second before 'serving' ball
                if reset_ball:
                    if pygame.time.get_ticks() - reset_timer >= 1000:
                        ball_velocity.xy = starting_velocity
                        reset_ball = False
                        ball_out_of_bounds = False
                
                # Win/Lose condition
                if enemy_score >= 10:
                    bounce_sound.stop()
                    score_sound.stop()
                    enemy_score_sound.stop()
                    await game_lost()
                elif player_score >= 10:
                    bounce_sound.stop()
                    score_sound.stop()
                    enemy_score_sound.stop()
                    await game_won()
                
                # Enemy 'AI' logic
                if ball_rect.centery > enemy.centery:
                    enemy.centery += ENEMY_SPEED
                elif ball_rect.centery < enemy.centery:
                    enemy.centery -= ENEMY_SPEED

                # Player movement logic
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
            else:
                display_message("segoeui", "PAUSED", 42, bold=True)
            pygame.display.update()
            clock.tick(60)
        if not running:
            break

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())