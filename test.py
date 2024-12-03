import pygame
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 850, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("zyy surprise number 19 or something idk")

# Colors
RED = (255, 0, 0)
BLACK = (255, 20, 147)
GOLD = (255, 215, 0)
NEON_PINK = (255, 20, 147)

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 33)
large_font = pygame.font.Font(pygame.font.get_default_font(), 48)

# Load Video
video = VideoFileClip("assets/hbd.mp4")  # Replace with your video file
video = video.resized(height=HEIGHT)  # Resize video to match screen height
frame_generator = video.iter_frames(fps=30, dtype="uint8")

# Load Music
pygame.mixer.init()
pygame.mixer.music.load("assets/hbd.mp3")  # Replace with your MP3 file

# Player settings
player = pygame.Rect(50, HEIGHT - 100, 50, 50)
player_color = GOLD
player_speed = 3

# Hearts (collectibles)
hearts = [pygame.Rect(x, HEIGHT - 120, 30, 30) for x in range(200, 800, 150)]
heart_color = RED
collected_hearts = 0

# Messages
messages = [
    "hi zy, move using arrows",
    "ily so much",
    "youre the best in the world",
    "hope youre enjoying this masterpiece i made",
    "keep listening maybe or come back to discord now"
]
message_index = 0

# Game state
game_over = False
game_started = False

# Clock
clock = pygame.time.Clock()

# Functions
def draw_player():
    pygame.draw.rect(screen, player_color, player)

def draw_hearts():
    for heart in hearts:
        pygame.draw.ellipse(screen, heart_color, heart)

def draw_message(message):
    text = font.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

def draw_ending():
    end_message = "Happy Birthday! You are loved!"
    text = large_font.render(end_message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def draw_pre_screen():
    pre_message = "Shake your mouse to unveil gift!"
    text = large_font.render(pre_message, True, NEON_PINK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Game loop
try:
    previous_mouse_x, previous_mouse_y = pygame.mouse.get_pos()  # Track mouse movement
    shake_threshold = 100  # Define how much movement is considered "shaking"
    shake_time_limit = 0.5  # Time window in seconds to detect a shake (e.g., 0.5 seconds)
    last_shake_time = 0  # Time of last shake detection
    shakes_needed = 5  # Number of shakes required
    shakes_detected = 0  # Number of shakes detected so far

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for mouse movement (only during pre-screen)
        if not game_started:
            current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
            mouse_dx = abs(current_mouse_x - previous_mouse_x)
            mouse_dy = abs(current_mouse_y - previous_mouse_y)
            
            # Check if there's a large enough movement and a sufficient time gap
            current_time = time.time()
            if (mouse_dx > shake_threshold or mouse_dy > shake_threshold) and (current_time - last_shake_time > shake_time_limit):
                last_shake_time = current_time  # Update the time of the last shake
                shakes_detected += 1  # Increment shake count

                if shakes_detected >= shakes_needed:
                    game_started = True
                    pygame.mixer.music.play(-1)  # Start the music after shakes are done

            # During pre-screen, display the shake message
            draw_pre_screen()

        else:
            # Display the next frame from the video
            try:
                frame = next(frame_generator)
            except StopIteration:
                # Restart the video when it ends
                frame_generator = video.iter_frames(fps=30, dtype="uint8")
                frame = next(frame_generator)

            # Convert video frame to Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))  # Draw video first

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_UP] and player.bottom == HEIGHT:
                player.y -= 50  # Jump
            if player.bottom < HEIGHT:
                player.y += 5  # Gravity

            # Collision detection
            for heart in hearts[:]:
                if player.colliderect(heart):
                    hearts.remove(heart)
                    collected_hearts += 1
                    if collected_hearts % 1 == 0 and message_index < len(messages) - 1:
                        message_index += 1

            # Drawing elements (after the video frame)
            draw_player()
            draw_hearts()
            if game_over:
                draw_ending()
            else:
                draw_message(messages[message_index])

        pygame.display.flip()
        clock.tick(30)

        # Update previous mouse position
        previous_mouse_x, previous_mouse_y = current_mouse_x, current_mouse_y

except Exception as e:
    print(f"Error: {e}")
    pygame.quit()
    sys.exit()
