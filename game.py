from machine import Pin, SPI, PWM
import st7735
import time
import random

# Initialize SPI
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(12), mosi=Pin(11), miso=Pin(9))

# Define TFT Pins
cs = Pin(10, Pin.OUT)
dc = Pin(13, Pin.OUT)
rst = Pin(8, Pin.OUT)

# Initialize Display
display = st7735.ST7735(spi, cs=cs, dc=dc, rst=rst, rotation=st7735.ROTATE_90)

# Backlight Control (PWM on GPIO 47)
led = PWM(Pin(47))
led.freq(1000)
brightness = 500
led.duty(brightness)

# Button Pins
btn_jump = Pin(16, Pin.IN, Pin.PULL_UP)  
btn_up = Pin(7, Pin.IN, Pin.PULL_UP)     
btn_down = Pin(15, Pin.IN, Pin.PULL_UP)  

# Colors
WHITE = st7735.WHITE
GREEN = 0x07E0  # Green pipes
BLACK = st7735.BLACK
RED = st7735.RED
YELLOW = 0xFFE0

# Game Constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128
BIRD_X = 20  
BIRD_SIZE = 12  
PIPE_WIDTH = 25  
PIPE_GAP = 45  
GRAVITY = 1
JUMP_STRENGTH = -6

# ASCII Bird Sprite
bird_sprite = [
    "  ##   ",
    " ###   ",
    "#####  ",
    " ## ## ",
    "  ###  ",
    "   #   "
]

def reset_game():
    global bird_y, velocity, pipe_x, pipe_y, score, game_over
    bird_y = SCREEN_HEIGHT // 2
    velocity = 0
    pipe_x = SCREEN_WIDTH
    pipe_y = random.randint(30, SCREEN_HEIGHT - PIPE_GAP - 30)
    score = 0
    game_over = False

def draw_bird(y):
    """Draws Bird at the given Y position."""
    for row_idx, row in enumerate(bird_sprite):
        for col_idx, pixel in enumerate(row):
            if pixel == "#":
                display.framebuf.pixel(BIRD_X + col_idx, y + row_idx, WHITE)

def draw_pipe(x, gap_y):
    """Draws green pipes."""
    display.framebuf.fill_rect(x, 0, PIPE_WIDTH, gap_y, GREEN)  # Top pipe
    display.framebuf.fill_rect(x, gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (gap_y + PIPE_GAP), GREEN)  # Bottom pipe

def check_collision(y, pipe_x, pipe_y):
    """Checks if Bird collides with pipes."""
    if (BIRD_X < pipe_x + PIPE_WIDTH and BIRD_X + BIRD_SIZE > pipe_x):
        if y < pipe_y or y + BIRD_SIZE > pipe_y + PIPE_GAP:
            return True
    return y <= 0 or y + BIRD_SIZE >= SCREEN_HEIGHT

def draw_centered_text(text, y, color):
    """Helper function to center text accurately."""
    text_x = (SCREEN_WIDTH - len(text) * 6) // 2 - 8
    display.framebuf.text(text, text_x, y, color)

def adjust_brightness():
    global brightness
    if btn_up.value() == 0:
        brightness = min(brightness + 50, 1023)
        led.duty(brightness)
        time.sleep(0.2)
    if btn_down.value() == 0:
        brightness = max(brightness - 50, 0)
        led.duty(brightness)
        time.sleep(0.2)

# Initialize Game
reset_game()

# Game Loop
while True:
    if game_over:
        display.fill(BLACK)
        draw_centered_text("Game Over!", 40, RED)
        draw_centered_text(f"Score: {score}", 60, WHITE)
        draw_centered_text("Press Button", 80, YELLOW)
        display.show()

        while btn_jump.value() == 1:
            adjust_brightness()
            time.sleep(0.1)

        reset_game()

    adjust_brightness()

    if btn_jump.value() == 0:
        velocity = JUMP_STRENGTH

    velocity += GRAVITY
    bird_y += velocity

    pipe_x -= 3
    if pipe_x < -PIPE_WIDTH:
        pipe_x = SCREEN_WIDTH
        pipe_y = random.randint(30, SCREEN_HEIGHT - PIPE_GAP - 30)
        score += 1

    if check_collision(bird_y, pipe_x, pipe_y):
        game_over = True

    display.fill(BLACK)
    draw_bird(bird_y)
    draw_pipe(pipe_x, pipe_y)
    draw_centered_text(f"Score: {score}", 5, WHITE)
    display.show()

    time.sleep(0.05)
