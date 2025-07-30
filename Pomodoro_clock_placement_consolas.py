import pygame
import sys
import time
import os
import datetime

# --- Init ---
pygame.init()
pygame.mixer.init()

# Screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pomodoro + Campfire")

# Colors
WHITE = (255, 255, 255)
BUTTON_TEXT = (0, 0, 0)

# Fonts
font_large = pygame.font.SysFont("consolas", 100, bold=True)
font_button = pygame.font.SysFont("consolas", 30)
clock_font = pygame.font.SysFont("consolas", 100)
quote_font = pygame.font.SysFont("consolas", 40)

# Load frames
frame_folder = "campfire"
frames = []
for f in sorted(os.listdir(frame_folder)):
    if f.endswith('.png'):
        img = pygame.image.load(os.path.join(frame_folder, f)).convert_alpha()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        frames.append(img)

if not frames:
    print("No frames found!")
    pygame.quit()
    sys.exit()

# Load audio
audio_file = "camp_fire.mp3"
if os.path.isfile(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(-1)

# Frame animation
frame_count = len(frames)
current_frame = 0
frame_delay = 200
last_update = pygame.time.get_ticks()

# Timer settings
POMODORO_TIME = 25 * 60
time_left = POMODORO_TIME
paused = True
last_tick = time.time()

# Buttons
buttons = {
    "start": pygame.Rect(WIDTH - 1075, HEIGHT -  835, 150, 50),# as the width increase it shift to left and on height increment
    "reset": pygame.Rect(WIDTH - 500, HEIGHT  - 835, 150, 50) # it shift up
} # width , height , length , breadth - 

def draw_rounded_button(rect, text, active=False):
    bg_color = (255, 255, 255) if not active else (230, 230, 255)
    pygame.draw.rect(screen, bg_color, rect, border_radius=25)
    text_surface = font_button.render(text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if buttons["start"].collidepoint(mouse_pos):
                if time_left <= 0:
                    time_left = POMODORO_TIME
                paused = False
                last_tick = time.time()
            elif buttons["reset"].collidepoint(mouse_pos):
                time_left = POMODORO_TIME
                paused = True

    # Update timer
    if not paused:
        current_time = time.time()
        delta = current_time - last_tick
        time_left -= delta
        last_tick = current_time
        if time_left <= 0:
            time_left = POMODORO_TIME
            paused = True

    # Advance frame
    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        current_frame = (current_frame + 1) % frame_count
        last_update = now

    # Draw background animation
    screen.blit(frames[current_frame], (0, 0))

    # Draw timer
    minutes = int(time_left) // 60
    seconds = int(time_left) % 60
    time_str = f"{minutes:02}:{seconds:02}"
    timer_surface = font_large.render(time_str, True, WHITE)
    screen.blit(timer_surface, timer_surface.get_rect(center=(WIDTH - 715 , HEIGHT - 800))) # change position of 25 minute timer

    # Draw buttons
    draw_rounded_button(buttons["start"], "start")
    draw_rounded_button(buttons["reset"], "restart")

    # Real-time system clock
    current_time_str = datetime.datetime.now().strftime("%H:%M:%S")
    time_surface = clock_font.render(current_time_str, True, WHITE)
    screen.blit(time_surface, (WIDTH - 945, HEIGHT - 90)) # height up height increase # width increases move left

    # Quote
    quote_text = "--- A warm fire warms the heart ---"
    quote_surface = quote_font.render(quote_text, True, WHITE)
    quote_rect = quote_surface.get_rect(center=(WIDTH - 700, HEIGHT - 125)) 
    screen.blit(quote_surface, quote_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()


