import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)

# Create the screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load balloon images and sound
balloon_frames = [pygame.image.load(f"balloon_frame_{i}.png") for i in range(5)]  # Assuming you have 5 frames
pop_sound = pygame.mixer.Sound("pop_sound.wav")

# Balloon properties
balloon_x, balloon_y = WIDTH // 2, HEIGHT // 2
current_frame = 0
is_popping = False

running = True
while running:
    screen.fill(WHITE)

    # Draw the current balloon frame
    screen.blit(balloon_frames[current_frame], (balloon_x, balloon_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_popping:
                is_popping = True
                pop_sound.play()

    if is_popping and current_frame < len(balloon_frames) - 1:
        current_frame += 1

    pygame.display.flip()
    clock.tick(15)  # Adjust for desired frame rate

pygame.quit()