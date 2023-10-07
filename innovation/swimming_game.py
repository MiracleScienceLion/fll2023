import pygame
import sys
import random
import cv2
import numpy as np
import mediapipe as mp

################################################################
# Parameters

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (27, 161, 226)  # Blue color that's close to swimming pool

circle_radius = 50

target_x = 500
target_y = 0


################################################################
# Utilities

def draw_fish():
    # Create a surface and draw a red circle on it
    image_surface = pygame.image.load('nemo.png').convert_alpha()
    resized_image_surface = pygame.transform.scale(image_surface, (150, 100))

    # Create a bitmask from the surface
    image_bitmask = pygame.mask.from_surface(resized_image_surface)

    return resized_image_surface, image_bitmask, 150, 100

# Draw the target object, return the corresponding surface and bitmask
def draw_circle():
    # Create a surface and draw a red circle on it
    circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, RED, (circle_radius, circle_radius), circle_radius)

    # Create a bitmask from the surface
    circle_bitmask = pygame.mask.from_surface(circle_surface)

    return circle_surface, circle_bitmask, circle_radius * 2, circle_radius * 2


# Detects if the two bitmasks are overlapping
def overlap(mask1: pygame.Mask, mask2, offset_x, offset_y):
    for x in range(mask1.get_size()[0]):
        for y in range(mask1.get_size()[1]):
            if mask1.get_at((x, y)) and mask2[y + offset_y][x + offset_x]:
                return x, y

    return None


# Capture the frame and return the RGB color space image
def capture_frame(capture):
    ret, frame = capture.read()  # Capture frame-by-frame

    if not ret:
        return None

    # Convert the BGR image to RGB
    return cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)


def get_human_segmentation(segmentation_processor, frame):
    # Convert the mask values to binary (0 or 1) for clearer visualization. You can adjust the threshold if needed.
    binary_mask = (segmentation_processor.process(frame).segmentation_mask > 0.5)

    # swap width and height generated by opencv and used in Pygame
    binary_mask_transposed = np.transpose(binary_mask, (1, 0))

    # Convert the binary mask to a Pygame surface by scaling the 0/1 to the range of 0-255
    binary_mask_surface = pygame.surfarray.make_surface(binary_mask_transposed * 255)

    # Convert background color to BLUE
    pixel_array = pygame.surfarray.array3d(binary_mask_surface)
    black_pixels = np.all(pixel_array == [0, 0, 0], axis=-1)
    pixel_array[black_pixels] = BLUE

    new_surface = pygame.surfarray.make_surface(pixel_array)

    return new_surface, binary_mask


def random_reposition_target(width, height):
    return random.randint(0, WIDTH - width - 1), random.randint(0, HEIGHT - height - 1)


#########################################################
# Initialization
pygame.init()
pygame.mixer.init()
bubble_sound = pygame.mixer.Sound('bubble_pop_trim.mp3')

# Setup webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open the webcam.")
    sys.exit()

# Get the dimensions of based on the webcam feed
WIDTH, HEIGHT = int(cap.get(3)), int(cap.get(4))
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Draw the target object on a surface.
# Only do it in initialization because the object is not constantly changing in shape.
# Otherwise, need to be put in while loop
target_surface, target_mask, target_width, target_height = draw_fish()

clock = pygame.time.Clock()

# Initialize selfie segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation_processor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

#################################################################
# Main

while True:
    frame = capture_frame(cap)

    if frame is None:
        break

    binary_mask_surface, binary_mask = get_human_segmentation(selfie_segmentation_processor, frame)

    collision = overlap(target_mask, binary_mask, target_x, target_y)

    if collision:
        # In this example, target is circle
        target_x, target_y = random_reposition_target(target_width, target_height)
        bubble_sound.play()
        pygame.time.wait(int(bubble_sound.get_length() * 1000))

        for trial in range(5):
            collision = overlap(target_mask, binary_mask, target_x, target_y)
            if collision:
                target_x, target_y = random_reposition_target(target_width, target_height)
            else:
                break
                
    # Draw everything
    window.fill(WHITE)
    # Blit the segmented mask and the circle
    window.blit(binary_mask_surface, (0, 0))
    # if show_circle:
    window.blit(target_surface, (target_x, target_y))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)

cap.release()
pygame.quit()
sys.exit()
