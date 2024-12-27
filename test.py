import cv2
import socket
import struct
import numpy as np

# Configuration
UDP_IP = "151.217.243.91"  # Replace with the target IP address
UDP_PORT = 54321            # Replace with the target port
WIDTH, HEIGHT = 48, 24
GAMMA = 2.2  # Gamma correction value

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Build gamma correction lookup table
gamma_table = np.array([((i / 255.0) ** (1.0 / GAMMA)) * 255 for i in range(256)]).astype("uint8")

try:
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Apply gamma correction
        # frame = cv2.LUT(frame, gamma_table)

        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
    cap.release()
    sock.close()
    print("Resources released.")

