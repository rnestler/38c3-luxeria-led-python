import cv2
import socket
import struct
import numpy as np
import pyscreenshot as ImageGrab

# Configuration
UDP_IP = "151.217.243.91"  # Replace with the target IP address
UDP_PORT = 54321            # Replace with the target port
WIDTH, HEIGHT = 48, 24
GAMMA = 2.2  # Gamma correction value

OY = 24
SCALE = 2

REGION = (0, OY, WIDTH * SCALE, HEIGHT * SCALE + OY)  # Screen region (left, top, right, bottom)

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Capture screen region
        screenshot = ImageGrab.grab(bbox=REGION)
        frame = np.array(screenshot)

        # Resize frame to 48x24
        resized_frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # Convert to bytes (3 bytes per pixel - RGB)
        data = resized_frame.flatten().tobytes()

        # Send data over UDP
        sock.sendto(data, (UDP_IP, UDP_PORT))

except KeyboardInterrupt:
    print("Stream stopped by user.")
finally:
    # Release resources
    sock.close()
    print("Resources released.")

