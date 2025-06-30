import pygame
import random

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Catch the Falling Cuties 🌟")
clock = pygame.time.Clock()

# Load backgrounds
bg1 = pygame.image.load("bg_1.png")
bg1 = pygame.transform.scale(bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg2 = pygame.image.load("bg_2.png")
bg2 = pygame.transform.scale(bg2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sizes
basket_size = (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
kid_size = (SCREEN_WIDTH // 15, SCREEN_HEIGHT // 15)

basket = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket, basket_size)

kid_images = [pygame.transform.scale(pygame.image.load(f"kid_{i}.png"), kid_size) for i in range(1, 11)]
heart_img = kid_images[9]

pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.play(-1)
catch_sound = pygame.mixer.Sound("pop.wav")

font = pygame.font.SysFont("Comic Sans MS", SCREEN_HEIGHT // 30)

basket_x = SCREEN_WIDTH // 2
basket_y = SCREEN_HEIGHT - basket_size[1] - 20

# Kids setup with delay
kids = []
MAX_KIDS = 5
kid_delay = 4000  # 4 seconds in milliseconds
last_kid_time = pygame.time.get_ticks()

def spawn_kid():
    x = random.randint(0, SCREEN_WIDTH - kid_size[0])
    y = random.randint(-300, -50)
    img = random.choice(kid_images)
    return [x, y, img]

score = 0
lives = 5
paused = False

# Start screen
def show_start_screen():
    screen.blit(bg1, (0, 0))
    title_font = pygame.font.SysFont("Comic Sans MS", SCREEN_HEIGHT // 10)
    small_font = pygame.font.SysFont("Comic Sans MS", SCREEN_HEIGHT // 25)

    title = title_font.render("✨ Catch the Emoji Kids ✨", True, (255, 255, 255))
    instruction = small_font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
    screen.blit(instruction, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Countdown
def countdown():
    count_font = pygame.font.SysFont("Comic Sans MS", SCREEN_HEIGHT // 5)
    for i in range(3, 0, -1):
        screen.blit(bg1, (0, 0))
        count = count_font.render(str(i), True, (255, 255, 255))
        screen.blit(count, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
        pygame.display.update()
        pygame.time.wait(1000)

# Win screen
def show_win_screen():
    screen.blit(bg2, (0, 0))
    win_font = pygame.font.SysFont("Comic Sans MS", SCREEN_HEIGHT // 10)
    win_text = win_font.render("🎉 You Win! 🎉", True, (255, 255, 0))
    screen.blit(win_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
    quit()

show_start_screen()
countdown()

running = True
while running:
    current_bg = bg2 if score >= 20 else bg1
    screen.blit(current_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused

    if paused:
        pause_text = font.render("⏸️ Paused - Press SPACE to Resume", True, (255, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
        pygame.display.update()
        clock.tick(10)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_x -= 6
    if keys[pygame.K_RIGHT]:
        basket_x += 6
    basket_x = max(0, min(basket_x, SCREEN_WIDTH - basket_size[0]))

    screen.blit(basket, (basket_x, basket_y))
    speed = 2

    # ✅ Spawn a new kid every 4 seconds
    current_time = pygame.time.get_ticks()
    if len(kids) < MAX_KIDS and current_time - last_kid_time > kid_delay:
        kids.append(spawn_kid())
        last_kid_time = current_time

    for kid in kids:
        kid[1] += speed
        screen.blit(kid[2], (kid[0], kid[1]))

        if (basket_x < kid[0] < basket_x + basket_size[0] and
            basket_y < kid[1] < basket_y + basket_size[1]):
            score += 1
            catch_sound.play()
            kids.remove(kid)

            if score >= 50:
                show_win_screen()

        elif kid[1] > SCREEN_HEIGHT:
            lives -= 1
            kids.remove(kid)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    for i in range(lives):
        screen.blit(heart_img, (SCREEN_WIDTH - (i + 1) * (kid_size[0] + 10) - 10, 10))

    if lives <= 0:
        game_over = font.render("Game Over! 😢", True, (255, 0, 0))
        screen.blit(game_over, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()

