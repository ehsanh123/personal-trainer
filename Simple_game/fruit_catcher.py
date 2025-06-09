import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

basket_x = 350  # Starting position
basket = pygame.Rect(basket_x, 550, 100, 20)  # Basket rectangle
fruit = pygame.Rect(random.randint(0, 780), 0, 20, 20)  # Falling fruit
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move basket with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.x > 0:
        basket.x -= 5
    if keys[pygame.K_RIGHT] and basket.x < 700:
        basket.x += 5

    # Move fruit down
    fruit.y += 3
    if fruit.y > 600:  # Reset if missed
        fruit.y = 0
        fruit.x = random.randint(0, 780)

    # Check collision
    if basket.colliderect(fruit):
        score += 1
        fruit.y = 0
        fruit.x = random.randint(0, 780)

    # Draw everything
    screen.fill((255, 255, 255))  # White background
    pygame.draw.rect(screen, (0, 0, 255), basket)  # Blue basket
    pygame.draw.rect(screen, (255, 0, 0), fruit)  # Red fruit
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(120)  # 60 FPS

pygame.quit()