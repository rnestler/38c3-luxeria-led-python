import cv2
import socket
import numpy as np

# Configuration
UDP_IP = "151.217.243.91"  # Replace with the target IP address
UDP_PORT = 54321            # Replace with the target port
WIDTH, HEIGHT = 48, 24

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Load image from file
IMAGE_PATH = 'space.jpg'  # Replace with the path to your image file
frame = cv2.imread(IMAGE_PATH)

if frame is None:
    print("Error: Could not load image.")
    exit()

try:
    while True:
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize frame to 48x24
        resized_frame = cv2.resize(frame_rgb, (WIDTH, HEIGHT))

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

