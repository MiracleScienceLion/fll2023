import cv2
import numpy as np
import random

def add_border(frame, thickness=10, color=(0, 255, 0)):
    """
    Add a border around the frame.
    
    Args:
    - frame (ndarray): The input video frame.
    - thickness (int): The border thickness.
    - color (tuple): The border color (R, G, B).
    
    Returns:
    - ndarray: The video frame with a border.
    """
    height, width, _ = frame.shape
    print(height, width)
    
    frame[:thickness, :, :] = color  # Top border
    frame[-thickness:, :, :] = color  # Bottom border
    frame[:, :thickness, :] = color  # Left border
    frame[:, -thickness:, :] = color  # Right border
    
    return frame

def create_circles(frame, num_circles=5, color=(0, 0, 255)):
    height, width, _ = frame.shape
    mask = np.zeros((height, width), dtype=np.uint8)

    circles = []
    for _ in range(num_circles):
        # Random center
        center_x = random.randint(0, width-1)
        center_y = random.randint(0, height-1)

        # Random radius
        radius = random.randint(10, 40)  # Adjust as needed

        circles.append((center_x, center_y, radius))
    return circles

def draw_circles(frame, circles):
    for center_x, center_y, radius in circles:
        cv2.circle(frame, (center_x, center_y), radius, (255), -1)  # 255 for white circle
    return frame


def main():
    # Open the webcam (0 indicates the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open the webcam.")
        return

    ret, frame = cap.read()  # Capture frame-by-frame
    height, width, _ = frame.shape
    print(height, width)
    circles = create_circles(frame)
    while True:
        ret, frame = cap.read()  # Capture frame-by-frame

        if not ret:
            break

        # Add a border to the frame
        frame = cv2.flip(frame, 1)
        frame = add_border(frame)
        frame = draw_circles(frame,circles)

        # Display the resulting frame
        cv2.imshow('Webcam with Border', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
