import argparse
import cv2
import socket
import time
import sys
import numpy as np

from arguments import common_arguments

parser = argparse.ArgumentParser(
    parents=[common_arguments], description="send an image"
)
parser.add_argument("filename", help="Path to the image file")
args = parser.parse_args()

WIDTH, HEIGHT = args.width, args.height

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

frame = cv2.imread(args.filename)

if frame is None:
    print("Error: Could not load image.")
    exit()

# Get image dimensions
img_height, img_width, _ = frame.shape

# Initialize window position
x, y, zoom = 0, 0, 1

# initialize velocity
dx, dy, dz = 0.75, 0.5, 0.05

scale = 2
MAX_SCALE = 32

try:
    while True:
        height = HEIGHT * scale
        width = WIDTH * scale

        # Extract moving window
        window = frame[int(y) : int(y + height), int(x) : int(x + width)]

        # Handle edge cases by padding if needed
        if window.shape[0] < HEIGHT or window.shape[1] < WIDTH:
            padded_window = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            padded_window[: window.shape[0], : window.shape[1]] = window
            window = padded_window

        # Convert BGR to RGB
        window_rgb = cv2.cvtColor(window, cv2.COLOR_BGR2RGB)

        # Resize frame to 48x24
        resized_frame = cv2.resize(window_rgb, (WIDTH, HEIGHT))

        # Convert to bytes (3 bytes per pixel - RGB)
        data = resized_frame.flatten().tobytes()

        # Send data over UDP
        sock.sendto(data, (args.ip, args.port))

        # Update window position
        x += dx * ( 1+ (0.5 * (scale-1)))
        y += dy * ( 1+ (0.5 * (scale-1)))
        scale += dz
        # print(x,y)
        if x + dx > (img_width - width) or x + dx < 0:
            dx = -dx
        if y + dy > (img_height - height) or y + dy < 0:
            dy = -dy

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        if scale < 1 or scale > MAX_SCALE:
            dz = -dz

        if scale < 1:
            scale = 1

        time.sleep(0.1)  # Adjust the frame rate as needed

except KeyboardInterrupt:
    print("Stream stopped by user.")
finally:
    # Release resources
    sock.close()
    print("Resources released.")
