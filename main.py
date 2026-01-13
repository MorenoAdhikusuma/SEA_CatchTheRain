import pygame
import random
import sys
import os

pygame.init()
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SeaChan - Catch the Rain")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHT = (255,255,255)
BLU = (0,200,255)
RED = (255,0,0)
BLK = (0,0,0)

SCORE_FILE = "scores.txt"
SCORE_SOUND = pygame.mixer.Sound(os.path.join('SFX', 'ScoreSFX.mp3'))
SCORE_SOUND.set_volume(0.3)

def load_scores():
    scores = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            for line in f:
                try:
                    name, sc = line.strip().split(",")
                    scores.append((name, int(sc)))
                except:
                    pass
    return scores

def save_score(name, score):
    with open(SCORE_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def name_input_screen(final_score):
    name = ""
    entering = True

    while entering:
        screen.fill(BLK)

        title = font.render("GAME OVER", True, RED)
        prompt = font.render("Enter your name:", True, WHT)
        name_text = font.render(name + "|", True, BLU)
        score_text = font.render(f"Score: {final_score}", True, WHT)

        screen.blit(title, (W//2 - 90, 150))
        screen.blit(score_text, (W//2 - 70, 200))
        screen.blit(prompt, (W//2 - 130, 260))
        screen.blit(name_text, (W//2 - 130, 300))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip():
                    entering = False
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10 and e.unicode.isprintable():
                    name += e.unicode

        clock.tick(60)

    return name

def scoreboard_screen():
    scores = load_scores()
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:8]

    showing = True
    while showing:
        screen.fill(BLK)

        title = font.render("SCOREBOARD", True, BLU)
        screen.blit(title, (W//2 - 90, 60))

        y = 130
        for i, (name, sc) in enumerate(scores, 1):
            txt = font.render(f"{i}. {name} - {sc}", True, WHT)
            screen.blit(txt, (W//2 - 130, y))
            y += 40

        hint = font.render("Press any key to exit", True, RED)
        screen.blit(hint, (W//2 - 150, 520))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                showing = False

        clock.tick(60)

# ================== GAME ==================
def main_game():
    paddle = pygame.Rect(W // 2 - 60, H - 40, 120, 20)
    block = pygame.Rect(random.randint(0, W - 20), 0, 20, 20)
    b_speed = 5
    score = 0
    #Sprites
    PLAYER_IMAGE = pygame.image.load(os.path.join('sprites', 'SeaChan.png')).convert_alpha()
    PLAYER_IMAGE = pygame.transform.smoothscale(PLAYER_IMAGE, (120, 80))
    paddle = PLAYER_IMAGE.get_rect(midbottom=(W//2, H-10))


    running = True
    while running:
        screen.fill(BLK)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 8
        if keys[pygame.K_RIGHT] and paddle.right < W:
            paddle.x += 8

        block.y += b_speed

        if block.colliderect(paddle):
            block.y = 0
            block.x = random.randint(0, W - 20)
            SCORE_SOUND.play()
            score += 1
            b_speed += 0.4

        if block.y > H:
            name = name_input_screen(score)
            save_score(name, score)
            scoreboard_screen()
            running = False

        screen.blit(PLAYER_IMAGE, paddle)
        pygame.draw.rect(screen, BLU, block)

        score_text = font.render(f"Score: {score}", True, WHT)
        screen.blit(score_text, (10, 10))
        objective_text = font.render(f"Bantu SeaChan menangkap air hujan", True, WHT)
        screen.blit(objective_text, (50,50))

        pygame.display.flip()
        clock.tick(60)

# ================== RUN ==================
main_game()
pygame.quit()
