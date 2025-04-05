import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
title = pygame.display.set_caption("pong.py")

clock = pygame.time.Clock()

player = pygame.Rect((10, 250, 10, 80))
enemy = pygame.Rect((780, 250, 10, 80))

ball = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 10))

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

    draw_net() # Draws "net" of repeating lines

    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", enemy)
    pygame.draw.rect(screen, "white", ball)

    key = pygame.key.get_pressed()

    if key[pygame.K_w] or key[pygame.K_UP]:
        player.move_ip(0, -PLAYER_SPEED)
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        player.move_ip(0, PLAYER_SPEED)
    
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