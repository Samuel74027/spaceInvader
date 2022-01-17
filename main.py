from socket import if_indextoname
from turtle import position
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My First Pygame')

white = (255, 255, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
fps = 100
spaceship_width = 55
spaceship_height = 40
max_bullets = 5
yellow_bullets = []
red_bullets = []

health_font = pygame.font.SysFont('comicsans', 40)
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2


mid_boarder = pygame.Rect(WIDTH//2 - 1, 0, 10, HEIGHT)

yellow_spaceship_import = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_import, (spaceship_width, spaceship_height)), 90)
red_spaceship_import = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_import, (spaceship_width, spaceship_height)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    screen.fill(black)
    pygame.draw.rect(screen, white, mid_boarder)
    
    red_health_text = health_font.render(f'Remaining Health {red_health}', 1, white)
    yellow_health_text = health_font.render(f'Remaining Health {red_health}', 1, white)
    screen.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    screen.blit(yellow_health_text, (10, 10))
    
    screen.blit(yellow_spaceship, (yellow.x, yellow.y))
    screen.blit(red_spaceship, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    pygame.display.update()

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += 5
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= 5
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
def main():
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    clock = pygame.time.Clock()
    red_health = 15
    yellow_health = 15
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 2.5, 10, 5)
                yellow_bullets.append(bullet)
            if event.key == pygame.K_RSHIFT:
                bullet = pygame.Rect(red.x, red.y + red.height//2 + 2.5, 10, 5)
                red_bullets.append(bullet)
        
        if event.type == red_hit:
            red_health -= 1
        
        if event.type == yellow_hit:
            yellow_health -= 1
        
        winner = ''
        if red_health <= 0:
            winner = 'Yellow Wins!'
        
        if yellow_health <= 0:
            winner = "Red Wins!"
        
        keys_pressed = pygame.key.get_pressed()
        #yellow movement
        if keys_pressed[pygame.K_a] and yellow.x > 0:
            yellow.x -= 3
        if keys_pressed[pygame.K_d] and yellow.x + spaceship_width < mid_boarder.x:
            yellow.x += 3
        if keys_pressed[pygame.K_w] and yellow.y > 0:
            yellow.y -= 3
        if keys_pressed[pygame.K_s] and yellow.y + spaceship_height < HEIGHT - 15:
            yellow.y += 3
        #red movement
        if keys_pressed[pygame.K_LEFT] and red.x > mid_boarder.width + mid_boarder.x:
            red.x -= 3
        if keys_pressed[pygame.K_RIGHT] and red.x + spaceship_height < WIDTH:
            red.x += 3
        if keys_pressed[pygame.K_UP] and red.y > 0:
            red.y -= 3
        if keys_pressed[pygame.K_DOWN] and red.y + spaceship_height < HEIGHT - 15:
            red.y += 3
            
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
                
                
                

if __name__ == "__main__":
    main()