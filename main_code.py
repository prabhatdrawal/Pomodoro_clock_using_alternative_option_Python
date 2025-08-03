''''
if you get any changes to the place of the element
due to diffrent resolution of the screen
you can change the position
by their respective width and height
do brainstorm , see yáll
'''


import pygame
import sys
import time
import os
import datetime
import random

# --- Initialization ---
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # getting infor of width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pomodoro + Campfire Themes") # display caption

# Colors
WHITE = (255, 255, 255)
BUTTON_TEXT = (0, 0, 0)

# Fonts
font_large = pygame.font.SysFont("Times new Roman", 100)
font_button = pygame.font.SysFont("Times new Roman", 30)
clock_font = pygame.font.SysFont("Times new Roman", 80)
quote_font = pygame.font.SysFont("Times new Roman", 40)
focus_font = pygame.font.SysFont("Times new Roman",40)
name_font = pygame.font.SysFont("Times new Roman",30)


# --- Themes ---
themes = [
    {"folder": "campfire", "music": "camp_fire.mp3"},
    {"folder": "midnight_lake", "music": "panda.mp3"},
    {"folder": "gaming_brother", "music": "Spirited.mp3"},
      {"folder": "rainy_highway", "music": "Sparkle.mp3"},
    {"folder": "snow_fall", "music": "lie.mp3"},
    {"folder": "warm_nights", "music": "naruto.mp3"},  
    {"folder": "cyber_cafe", "music": "roses.mp3"},
    {"folder": "bustling_city", "music": "lie2.mp3"}
]

# --- Quotes ---
quotes = [
    "--- A warm fire warms the heart ---",
    "--- Focus is a form of respect ---",
    "--- Silence fuels creativity ---",
    "--- Every second counts ---",
    "--- Burnout happens without balance ---",
    "--- Let the flames carry your thoughts ---",
    "--- Be still like the fire’s glow ---",
    "--- Deep breaths, steady mind ---",
    "--- Flow with focus, not force ---",
    "--- Let stillness sharpen your clarity ---",
    "--- Create slowly, burn brightly ---",
    "--- Rest is part of the rhythm ---",
    "--- The mind clears where the fire crackles ---",
    "--- Calm is your power ---",
    "--- Let your thoughts simmer, not boil ---",
    "--- Drift into focus, like ash in wind ---",
    "--- One moment, fully lived ---",
    "--- Light the fire, not the stress ---",
    "--- In silence, productivity grows ---",
    "--- The ember of effort lights success ---"
]

quote_text = random.choice(quotes)  # initial quote

# Buttons
buttons = {
    "start": pygame.Rect(WIDTH - 1015, HEIGHT - 800, 150, 50), # width , height , length breadth
    "reset": pygame.Rect(WIDTH - 560, HEIGHT - 800, 150, 50)
}

def draw_rounded_button(rect, text, active=False):
    bg_color = (255, 255, 255) if not active else (230, 230, 255)
    pygame.draw.rect(screen, bg_color, rect, border_radius=25)
    text_surface = font_button.render(text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# --- Timer ---
POMODORO_TIME = 25 * 60
time_left = POMODORO_TIME
paused = True
last_tick = time.time()

# --- Animation ---
frame_delay = 200
last_update = pygame.time.get_ticks()
current_frame = 0
frames = []
frame_count = 0
theme_index = 0

def load_theme(theme):
    global frames, frame_count, current_frame, quote_text
    folder = theme["folder"]
    music = theme["music"]
    frames = []

    try:
        for f in sorted(os.listdir(folder)):
            if f.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, f)).convert_alpha()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                frames.append(img)
    except FileNotFoundError:
        print(f"[ERROR] Frame folder '{folder}' not found.")
        pygame.quit()
        sys.exit()

    if not frames:
        print(f"[ERROR] No frames in '{folder}'.")
        pygame.quit()
        sys.exit()

    frame_count = len(frames)
    current_frame = 0

    if os.path.isfile(music):
        try:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"[ERROR] Music load failed: {e}")
    else:
        print(f"[ERROR] Music file '{music}' not found.")

    # New quote for each theme
    quote_text = random.choice(quotes) # random choose quotes

# Shuffle and load first theme
random.shuffle(themes)
load_theme(themes[theme_index])

# --- Main Loop ---
clock = pygame.time.Clock()
running = True
while running:
    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
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

    # --- Timer Update ---
    if not paused:
        current_time = time.time()
        delta = current_time - last_tick
        time_left -= delta
        last_tick = current_time
        if time_left <= 0:
            time_left = POMODORO_TIME
            paused = True

    # --- Animation Frame Update ---
    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        current_frame = (current_frame + 1) % frame_count
        last_update = now

    # --- Draw ---
    screen.blit(frames[current_frame], (0, 0))

    # Pomodoro Timer
    minutes = int(time_left) // 60
    seconds = int(time_left) % 60
    time_str = f"{minutes:02}:{seconds:02}"
    timer_surface = font_large.render(time_str, True, WHITE)
    screen.blit(timer_surface, timer_surface.get_rect(center=(WIDTH - 715, HEIGHT - 775)))

    # Buttons
    draw_rounded_button(buttons["start"], "start") # buttons development - start
    draw_rounded_button(buttons["reset"], "restart") # buttons development - restart

    # Clock
    current_time_str = datetime.datetime.now().strftime("%H:%M:%S") # clock display format
    time_surface = clock_font.render(current_time_str, True, WHITE)
    screen.blit(time_surface, (WIDTH - 857, HEIGHT - 100)) # clock location placement

    # Quote
    quote_surface = quote_font.render(quote_text, True, WHITE)
    quote_rect = quote_surface.get_rect(center=(WIDTH - 700, HEIGHT - 125)) # quote placement
    screen.blit(quote_surface, quote_rect)

     # focus
    focus_surface = focus_font.render("~ FOCUS ~", True, (255,192,203)) # 255,192,203 - gold shade type color code
    focus_rect = focus_surface.get_rect(center=(WIDTH - 720, HEIGHT - 860)) # original place 720 , 860
    screen.blit(focus_surface, focus_rect)

      # name tag on the surface
    name_surface = name_font.render("| Prabhat D Rawal", True, WHITE)
    name_rect = name_surface.get_rect(center=(WIDTH - 150, HEIGHT - 40)) # original place 720 , 860
    screen.blit(name_surface, name_rect) # plotting on the screen

    pygame.display.flip()
    clock.tick(60)

    # --- Theme Change on Music End ---
    if not pygame.mixer.music.get_busy():
        theme_index = (theme_index + 1) % len(themes)
        load_theme(themes[theme_index])

# --- Exit ---
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
