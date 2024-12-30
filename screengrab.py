import cv2
import socket
import struct
import time
import numpy as np
import pyscreenshot as ImageGrab
from pynput import mouse

# Configuration
UDP_IP = "151.217.233.92"  # Replace with the target IP address
UDP_PORT = 54321            # Replace with the target port
WIDTH, HEIGHT = 48, 24
GAMMA = 2.2  # Gamma correction value

OY = 24
SCALE = 1

REGION = (0, OY, WIDTH * SCALE, HEIGHT * SCALE + OY)  # Screen region (left, top, right, bottom)

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mouse_x = 0
mouse_y = 0
def on_move(x, y):
    print(x,y)
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

listener = mouse.Listener(on_move=on_move)
listener.start()
print('hello')

try:
    while True:
        # Capture screen region
        listener.wait()
        x = mouse_x
        y = mouse_y
        region = (x, y, WIDTH * SCALE + x, HEIGHT * SCALE + y)
        screenshot = ImageGrab.grab(bbox=region)
        frame = np.array(screenshot)

        # Resize frame to 48x24
        resized_frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # Convert to bytes (3 bytes per pixel - RGB)
        data = resized_frame.flatten().tobytes()

        # Send data over UDP
        sock.sendto(data, (UDP_IP, UDP_PORT))

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stream stopped by user.")
finally:
    # Release resources
    sock.close()
    print("Resources released.")

