import socket
import time
import random
import json

# -----------------------------
# CONFIG
# -----------------------------
UDP_IP = "127.0.0.1"   # Change if receiver is on another machine
UDP_PORTS = [5005, 5007]
SEND_INTERVAL = 0.1    # 10 Hz
# -----------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Mock Nicla Vision sender started")

mode = "normal"
mode_timer = time.time()

def random_imu(scale=0.05):
    return {
        "ax": random.uniform(-scale, scale),
        "ay": random.uniform(-scale, scale),
        "az": 9.8 + random.uniform(-scale, scale),
        "gx": random.uniform(-scale, scale),
        "gy": random.uniform(-scale, scale),
        "gz": random.uniform(-scale, scale),
    }

while True:
    now = time.time()

    # Change scenario every ~5 seconds
    if now - mode_timer > 5:
        mode = random.choice(["normal", "obstacle", "fall", "horn"])
        mode_timer = now

    alert = "NONE"
    tof_mm = random.randint(900, 1500)
    imu = random_imu()

    if mode == "obstacle":
        tof_mm = random.randint(300, 700)
        alert = "OBSTACLE_AHEAD. STOP!"

    elif mode == "fall":
        imu = {
            "ax": random.uniform(-8, 8),
            "ay": random.uniform(-8, 8),
            "az": random.uniform(-8, 8),
            "gx": random.uniform(-10, 10),
            "gy": random.uniform(-10, 10),
            "gz": random.uniform(-10, 10),
        }
        alert = "FALL_DETECTED. GET UP SLOWLY!"

    elif mode == "horn":
        alert = "HORN SOUND DETECTED. BE CAREFUL! FLASHING LIGHTS!"

    packet = {
        "timestamp": now,
        "imu": imu,
        "tof_mm": tof_mm,
        "alert": alert
    }

    encoded_packet = json.dumps(packet).encode()
    for port in UDP_PORTS:
        sock.sendto(encoded_packet, (UDP_IP, port))
    time.sleep(SEND_INTERVAL)
