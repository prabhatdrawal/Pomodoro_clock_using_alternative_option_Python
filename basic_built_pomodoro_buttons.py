import pygame
import sys
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_PURPLE = (189, 147, 249)
BUTTON_BG = (255, 255, 255)
BUTTON_TEXT = (0, 0, 0)
BACKGROUND = LIGHT_PURPLE

font_large = pygame.font.SysFont("consolas", 100, bold=True)
font_button = pygame.font.SysFont("consolas", 30)

SESSIONS = {
    "pomodoro": 25 * 60,
    "short": 5 * 60,
    "long": 15 * 60
}

current_session = "pomodoro"
time_left = SESSIONS[current_session]
paused = True
last_tick = time.time()

buttons = {
    "pomodoro": pygame.Rect(WIDTH//2 - 330, 100, 200, 50),
    "short":    pygame.Rect(WIDTH//2 - 100, 100, 230, 50),
    "long":     pygame.Rect(WIDTH//2 + 160, 100, 210, 50),
    "start":    pygame.Rect(WIDTH//2 - 75, HEIGHT//2 + 100, 150, 50),
    "pause":    pygame.Rect(WIDTH//2 - 250, HEIGHT//2 + 100, 150, 50),
    "reset":    pygame.Rect(WIDTH//2 + 110, HEIGHT//2 + 100, 60, 50)
}

clock = pygame.time.Clock()
running = True

def draw_rounded_button(rect, text, active=False):
    is_session_button = rect in (buttons["pomodoro"], buttons["short"], buttons["long"])

    if is_session_button:
        border_color = WHITE if not active else (255, 255, 180)  # Highlight current session
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=25)
        text_surface = font_button.render(text, True, border_color)
    else:
        bg_color = (255, 255, 255) if not active else (230, 230, 255)
        pygame.draw.rect(screen, bg_color, rect, border_radius=25)
        text_surface = font_button.render(text, True, BUTTON_TEXT)

    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def switch_session(session_name):
    global current_session, time_left, paused
    current_session = session_name
    time_left = SESSIONS[session_name]
    paused = True

while running:
    screen.fill(BACKGROUND)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if buttons["start"].collidepoint(mouse_pos):
                paused = False
                last_tick = time.time()
            elif buttons["pause"].collidepoint(mouse_pos):
                paused = True
            elif buttons["reset"].collidepoint(mouse_pos):
                time_left = SESSIONS[current_session]
                paused = True
            elif buttons["pomodoro"].collidepoint(mouse_pos):
                switch_session("pomodoro")
            elif buttons["short"].collidepoint(mouse_pos):
                switch_session("short")
            elif buttons["long"].collidepoint(mouse_pos):
                switch_session("long")


    if not paused:
        current_time = time.time()
        delta = current_time - last_tick
        time_left -= delta
        last_tick = current_time
        if time_left <= 0:
            time_left = 0
            paused = True

 
    draw_rounded_button(buttons["pomodoro"], "pomodoro", current_session == "pomodoro")
    draw_rounded_button(buttons["short"], "short break", current_session == "short")
    draw_rounded_button(buttons["long"], "long break", current_session == "long")

    minutes = int(time_left) // 60
    seconds = int(time_left) % 60
    time_str = f"{minutes:02}:{seconds:02}"
    timer_surface = font_large.render(time_str, True, WHITE)
    timer_rect = timer_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(timer_surface, timer_rect)

    draw_rounded_button(buttons["pause"], "pause")
    draw_rounded_button(buttons["start"], "start")
    draw_rounded_button(buttons["reset"], "⟳")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
