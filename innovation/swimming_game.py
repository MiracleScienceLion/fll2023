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

fish_x = 0
fish_y = 500
turtle_x = 250
turtle_y = 250
star_x = 500
star_y = 0


################################################################
# Utilities
def draw_object(image):
    image_surface = pygame.image.load(image).convert_alpha()
    resized_image_surface = pygame.transform.scale(image_surface, (150, 100))

    # Create a bitmask from the surface
    image_bitmask = pygame.mask.from_surface(resized_image_surface)

    return resized_image_surface, image_bitmask, 150, 100


def draw_fish():
    # create a surface for loading image and resize 
    image_surface = pygame.image.load('img/nemo.png').convert_alpha()
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

    # Convert background to a video
    foreground = pygame.surfarray.array3d(binary_mask_surface)
    video_frame = get_next_video_frame(background_video)
    video_frame = pygame.transform.scale(pygame.surfarray.make_surface(video_frame), (WIDTH, HEIGHT))
    background = pygame.surfarray.array3d(video_frame)
    blended_image = np.where(foreground == [0, 0, 0], background, foreground)
    new_surface = pygame.surfarray.make_surface(blended_image)

    return new_surface, binary_mask


def random_reposition_target(mask1: pygame.Mask, mask2, width, height):

    new_pos_x, new_pos_y = 0, 0
    for trial in range (0, 10):
        offset_x, offset_y = random.randint(0, WIDTH - width - 1), random.randint(0, HEIGHT - height - 1)
        is_overlap = overlap(mask1, mask2, offset_x, offset_y)
        if not is_overlap:
            return offset_x, offset_y

    return offset_x, offset_y


def get_next_video_frame(video):
    ret, frame = video.read()

    if not ret:
        # Restart the video if it has ended
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()

    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, gem_color, x, y):
        super().__init__()

        if gem_color == 'GREEN':
            frame_files = [f"img/green_gem2/{i:04}.png" for i in range(1, 61) if i % 2 != 0]
        elif gem_color == 'YELLOW':
            frame_files = [f"img/yellow_gem6/{i:04}.png" for i in range(1, 61) if i % 2 != 0]
        elif gem_color == 'RED':
            frame_files = [f"img/red_gem3/{i:04}.png" for i in range(1, 61) if i % 2 != 0]
        else:
            frame_files = None

        self.frames = [pygame.image.load(f) for f in frame_files]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.frame_duration = 1
        self.animation_duration = 2000
        self.last_update = pygame.time.get_ticks()
        self.initial_update = self.last_update

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # if the animation is complete, reset animation index
        if self.current_frame >= len(self.frames) - 1 and now - self.initial_update > self.animation_duration:
            self.kill()
#########################################################
# Initialization
pygame.init()
pygame.mixer.init()
bubble_sound = pygame.mixer.Sound('img/archivo.mp3')
# image list
nemo_image = 'img/nemo.png'
star_image = 'img/star.png'
turtle_image = 'img/turtle.png'
background_video_path = 'img/tank floor.mp4'
# Open the background video using OpenCV
background_video = cv2.VideoCapture(background_video_path)
if not background_video.isOpened():
    print("Could not open the background video.")
    sys.exit()

# Setup webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():  #
    print("Could not open the webcam.")
    sys.exit()

# Get the dimensions based on the webcam feed
WIDTH, HEIGHT = int(cap.get(3)), int(cap.get(4))
window = pygame.display.set_mode((WIDTH, HEIGHT))
animation_group = pygame.sprite.Group()

# Draw the target object on a surface.
# Only do it in initialization because the object is not constantly changing in shape.
# Otherwise, need to be put in while loop
fish_surface, fish_mask, fish_width, fish_height = draw_object(nemo_image)
turtle_surface, turtle_mask, turtle_width, turtle_height = draw_object(turtle_image)
star_surface, star_mask, star_width, star_height = draw_object(star_image)
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

    collision_fish = overlap(fish_mask, binary_mask, fish_x, fish_y)
    collision_turtle = overlap(turtle_mask, binary_mask, turtle_x, turtle_y)
    collision_star = overlap(star_mask, binary_mask, star_x, star_y)

    if collision_fish or collision_turtle or collision_star:
        bubble_sound.play()
        #pygame.time.wait(int(bubble_sound.get_length() * 500))

        if collision_fish:
            animation_group.add(AnimatedSprite('RED', fish_x + fish_width/2, fish_y + fish_height/2))
            fish_x, fish_y = random_reposition_target(fish_mask, binary_mask, fish_width, fish_height)

        if collision_turtle:
            animation_group.add(AnimatedSprite('GREEN', turtle_x + turtle_width/2, turtle_y + turtle_height/2))
            turtle_x, turtle_y = random_reposition_target(turtle_mask, binary_mask, turtle_width, turtle_height)

        if (collision_star):
            animation_group.add(AnimatedSprite('YELLOW', star_x + star_width/2, star_y + star_height/2))
            star_x, star_y = random_reposition_target(star_mask, binary_mask, star_width, star_height)

    # Blit the segmented mask and the circle
    window.blit(binary_mask_surface, (0, 0))
    window.blit(turtle_surface, (turtle_x, turtle_y))
    window.blit(fish_surface, (fish_x, fish_y))
    window.blit(star_surface, (star_x, star_y))

    animation_group.draw(window)
    animation_group.update()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #clock.tick(20)

background_video.release()
cap.release()
pygame.quit()
sys.exit()
