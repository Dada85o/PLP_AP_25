import pygame
import tkinter as tk
from tkinter import messagebox
import sys
import random
import time

# Inicializace
pygame.init()
root = tk.Tk()
root.withdraw()

pygame.font.init()
font = pygame.font.SysFont("Arial", 28)

WIDTH, HEIGHT = 800, 600
fullscreen = False
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("pak sbírá bodíky")

# Barvy
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# Hráč (Pak)
pak_size = 40
pak_x = WIDTH // 2
pak_y = HEIGHT // 2
pak_speed = 7
boost = False

# Skóre a power-upy
score = 0
score_double = 1
boost_active = False
boost_start = 0
boost_end = 5

bod_radius = 5
bod = []
green_bod = []
cyan_bod = []

# Body
def spawn_dots():
    x = random.randint(bod_radius, WIDTH - bod_radius * 2)
    y = random.randint(bod_radius, HEIGHT - bod_radius * 2)
    return pygame.Rect(x, y, bod_radius * 2, bod_radius * 2)

for _ in range(20):
    bod.append(spawn_dots())

#funkce
def double():
    if random.randint(1, 900) == 1 and len(green_bod) == 0:
        green_bod.append((spawn_dots(), time.time()))

def spawn_zmrzlina():
    if score >= 1000 and random.randint(1, 500) == 1 and len(cyan_bod) == 0:
        cyan_bod.append((spawn_dots(), time.time()))

zdi_active = False
zdi = [
    pygame.Rect(200, 150, 400, 20),
    pygame.Rect(100, 400, 600, 20),
]

# Bubák
bubak_size = 40
bubak_x = random.randint(0, WIDTH - bubak_size)
bubak_y = random.randint(0, HEIGHT - bubak_size)
bubak_speed = 3
bubak_active = False
bubak_frozen = False
bubak_frozen_start = 0
bubak_FREEZE_DURATION = 3

# Druhý bubák
bubak2_active = False
bubak2_x = random.randint(0, WIDTH - bubak_size)
bubak2_y = random.randint(0, HEIGHT - bubak_size)

def move_bubak():
    global bubak_x, bubak_y
    if bubak_frozen:
        return
    if bubak_x < pak_x:
        bubak_x += bubak_speed
    elif bubak_x > pak_x:
        bubak_x -= bubak_speed
    if bubak_y < pak_y:
        bubak_y += bubak_speed
    elif bubak_y > pak_y:
        bubak_y -= bubak_speed

def move_bubak2():
    global bubak2_x, bubak2_y
    if bubak_frozen:
        return
    if bubak2_x < pak_x:
        bubak2_x += bubak_speed
    elif bubak2_x > pak_x:
        bubak2_x -= bubak_speed
    if bubak2_y < pak_y:
        bubak2_y += bubak_speed
    elif bubak2_y > pak_y:
        bubak2_y -= bubak_speed

def confirm_exit():
    return messagebox.askyesno("Ukončit hru", "Opravdu chceš ukončit hru?")

def end():
    while True:
        WIN.fill(WHITE)
        zprava1 = font.render(f"Pak byl chycen! Skóre: {score}", True, RED)
        zprava2 = font.render("R - Restart   |   ESC - Konec", True, BLACK)
        WIN.blit(zprava1, (WIDTH//2 - zprava1.get_width()//2, HEIGHT//2 - 40))
        WIN.blit(zprava2, (WIDTH//2 - zprava2.get_width()//2, HEIGHT//2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def reset_game():
    global pak_x, pak_y, score, score_double, boost_active, boost, bubak_active
    global bubak_frozen, bod, green_bod, cyan_bod, pak_speed
    global bubak_x, bubak_y, bubak2_active, bubak2_x, bubak2_y

    pak_x = WIDTH // 2
    pak_y = HEIGHT // 2
    score = 0
    score_double = 1
    boost_active = False
    boost = False
    bubak_active = False
    bubak2_active = False
    bubak_frozen = False
    pak_speed = 7
    bod = [spawn_dots() for _ in range(20)]
    green_bod.clear()
    cyan_bod.clear()
    bubak_x = random.randint(0, WIDTH - bubak_size)
    bubak_y = random.randint(0, HEIGHT - bubak_size)
    bubak2_x = random.randint(0, WIDTH - bubak_size)
    bubak2_y = random.randint(0, HEIGHT - bubak_size)

# Herní smyčka
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    current_time = time.time()
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if confirm_exit():
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    WIN = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
            elif event.key == pygame.K_ESCAPE:
                if confirm_exit():
                    running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        pak_y -= pak_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        pak_y += pak_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pak_x -= pak_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pak_x += pak_speed

    if score >= 500 and not boost:
        pak_speed = 10
        boost = True

    pak_x = max(0, min(pak_x, WIDTH - pak_size))
    pak_y = max(0, min(pak_y, HEIGHT - pak_size))

    center_x = pak_x + pak_size // 2
    center_y = pak_y + pak_size // 2
    radius_outer = pak_size // 2
    radius_inner = radius_outer - 3
    pygame.draw.circle(WIN, BLACK, (center_x, center_y), radius_outer)
    pygame.draw.circle(WIN, YELLOW, (center_x, center_y), radius_inner)

    pak_rect = pygame.Rect(pak_x, pak_y, pak_size, pak_size)
        
    for dot in bod[:]:
        if pak_rect.colliderect(dot):
            bod.remove(dot)
            score += 10 * score_double
            bod.append(spawn_dots())
    for dot in bod:
        pygame.draw.circle(WIN, BLUE, dot.center, bod_radius)

    double()
    for green_dot, spawn_time in green_bod[:]:
        if current_time - spawn_time > 10:
            green_bod.remove((green_dot, spawn_time))
        elif pak_rect.colliderect(green_dot):
            green_bod.remove((green_dot, spawn_time))
            score_double = 2
            boost_active = True
            boost_start = current_time
        else:
            pygame.draw.circle(WIN, GREEN, green_dot.center, bod_radius)

    if boost_active:
        time_left = boost_end - int(current_time - boost_start)
        if time_left <= 0:
            score_double = 1
            boost_active = False
        else:
            boost_text = font.render(f"2x: {time_left}s", True, GREEN)
            WIN.blit(boost_text, (200, 10))

    spawn_zmrzlina()
    for cyan_dot, spawn_time in cyan_bod[:]:
        if current_time - spawn_time > 10:
            cyan_bod.remove((cyan_dot, spawn_time))
        elif pak_rect.colliderect(cyan_dot):
            cyan_bod.remove((cyan_dot, spawn_time))
            bubak_frozen = True
            bubak_frozen_start = current_time
        else:
            pygame.draw.circle(WIN, CYAN, cyan_dot.center, bod_radius)

    if bubak_frozen:
        freeze_time_left = bubak_FREEZE_DURATION - int(current_time - bubak_frozen_start)
        if freeze_time_left <= 0:
            bubak_frozen = False
        else:
            freeze_text = font.render(f"Freeze: {freeze_time_left}s", True, CYAN)
            WIN.blit(freeze_text, (350, 10))

    if score >= 1000 and not bubak_active:
        bubak_active = True

    if bubak_active:
        move_bubak()
        bubak_color = CYAN if bubak_frozen else RED
        pygame.draw.rect(WIN, bubak_color, (bubak_x, bubak_y, bubak_size, bubak_size))
        bubak_rect = pygame.Rect(bubak_x, bubak_y, bubak_size, bubak_size)
        if pak_rect.colliderect(bubak_rect):
            if end():
                reset_game()
                continue
            else:
                running = False
    #ZDI
    if score >= 2000:
        zdi_active = True

    if zdi_active:
        for zed in zdi:
            pygame.draw.rect(WIN, BLACK, zed)
            if pak_rect.colliderect(zed):
                # Odskočení od zdi podle směru pohybu
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    pak_y += pak_speed
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    pak_y -= pak_speed
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    pak_x += pak_speed
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    pak_x -= pak_speed


    

    if score >= 3000 and not bubak2_active:
        bubak2_active = True

    if bubak2_active:
        move_bubak2()
        pygame.draw.rect(WIN, CYAN if bubak_frozen else RED, (bubak2_x, bubak2_y, bubak_size, bubak_size))
        bubak2_rect = pygame.Rect(bubak2_x, bubak2_y, bubak_size, bubak_size)
        if pak_rect.colliderect(bubak2_rect):
            if end():
                reset_game()
                continue
            else:
                running = False

    if score >= 5000:
        WIN.fill(WHITE)
        win_text = font.render("Gratulace! Vyhrál jsi!", True, GREEN)
        final_score = font.render(f"Konečné skóre: {score}", True, BLACK)
        WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 40))
        WIN.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()
        pygame.time.wait(5000)
        running = False
        break

    score_text = font.render(f"Skóre: {score}", True, BLACK)
    WIN.blit(score_text, (10, 10))
    pygame.display.update()

pygame.quit()
sys.exit()
