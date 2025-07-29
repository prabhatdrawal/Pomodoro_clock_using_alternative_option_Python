import pygame
import os
import sys
import datetime


pygame.init()
pygame.mixer.init()


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Campfire Pixel Art Animation")
clock = pygame.time.Clock()


frame_folder = "japanese_house_frame"
frames = []
try:
    for f in sorted(os.listdir(frame_folder)):
        if f.endswith('.png'):
            img_path = os.path.join(frame_folder, f)
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # scale to fullscreen resolution
            frames.append(img)
except FileNotFoundError:
    print(f"[ERROR] Folder '{frame_folder}' not found. Please make sure it exists.")
    pygame.quit()
    sys.exit()

if not frames:
    print("[ERROR] No .png frames found in the folder.")
    pygame.quit()
    sys.exit()

frame_count = len(frames)
current_frame = 0
frame_delay = 100 
last_update = pygame.time.get_ticks()


def is_night():
    hour = datetime.datetime.now().hour
    return hour < 6 or hour >= 18


running = True
while running:
    
    screen.fill((0, 0, 0) if is_night() else (180, 220, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False

    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        current_frame = (current_frame + 1) % frame_count
        last_update = now


    screen.blit(frames[current_frame], (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
