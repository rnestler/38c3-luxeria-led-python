import cv2
import socket
import struct
import time
import numpy as np

# Configuration
UDP_IP = "151.217.243.91"  # Replace with the target IP address
UDP_PORT = 54321            # Replace with the target port
WIDTH, HEIGHT = 48, 24
STEP_X, STEP_Y = 5, 5  # Step size for moving window

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Load image from file
IMAGE_PATH = 'space.jpg'  # Replace with the path to your image file
# IMAGE_PATH = 'perlin.png'  # Replace with the path to your image file
# IMAGE_PATH = 'chess.jpg'  # Replace with the path to your image file
# IMAGE_PATH = 'chess-small.jpg'  # Replace with the path to your image file
# IMAGE_PATH = 'waldo.jpg'  # Replace with the path to your image file

frame = cv2.imread(IMAGE_PATH)

if frame is None:
    print("Error: Could not load image.")
    exit()

# Get image dimensions
img_height, img_width, _ = frame.shape

# Initialize window position
x, y, zoom = 0, 0, 1

# initialize velocity
dx, dy, dz = 2, 1, 0.01

scale = 1
MAX_SCALE = 32

try:
    while True:
        height = round(HEIGHT * scale)
        width = round(WIDTH * scale)
        # Extract moving window
        window = frame[y:y+height, x:x+width]

        # Handle edge cases by padding if needed
        if window.shape[0] < HEIGHT or window.shape[1] < WIDTH:
            padded_window = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            padded_window[:window.shape[0], :window.shape[1]] = window
            window = padded_window

        # Convert BGR to RGB
        window_rgb = cv2.cvtColor(window, cv2.COLOR_BGR2RGB)

        # Resize frame to 48x24
        resized_frame = cv2.resize(window_rgb, (WIDTH, HEIGHT))

        # Convert to bytes (3 bytes per pixel - RGB)
        data = resized_frame.flatten().tobytes()

        # Send data over UDP
        sock.sendto(data, (UDP_IP, UDP_PORT))

        # Update window position
        x += dx
        y += dy
        scale += dz
        #print(x,y)
        if x + dx > (img_width - width) or x + dx < 0:
            dx = -dx
        if y + dy > (img_height - height) or y + dy < 0:
            dy = -dy

        if scale < 1 or scale > MAX_SCALE:
            dz = -dz
        time.sleep(0.1)  # Adjust the frame rate as needed

except KeyboardInterrupt:
    print("Stream stopped by user.")
finally:
    # Release resources
    sock.close()
    print("Resources released.")

