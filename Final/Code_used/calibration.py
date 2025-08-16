import RPi.GPIO as GPIO
import time

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# === Define HC-SR04 Sensor Pins ===
SENSORS = [
    {"Trig": 5,  "Echo": 6},   # Sensor 0
    {"Trig": 22, "Echo": 25},  # Sensor 1
    {"Trig": 17, "Echo": 27},  # Sensor 2
    {"Trig": 23, "Echo": 24},  # Sensor 3
]

# === Setup GPIO Pins ===
for sensor in SENSORS:
    GPIO.setup(sensor["Trig"], GPIO.OUT)
    GPIO.setup(sensor["Echo"], GPIO.IN)
    GPIO.output(sensor["Trig"], False)

time.sleep(2)  # Allow sensors to settle

# === Measure distance using HC-SR04 ===
def get_distance(sensor_index):
    trig = SENSORS[sensor_index]["Trig"]
    echo = SENSORS[sensor_index]["Echo"]

    # Trigger pulse
    GPIO.output(trig, True)
    time.sleep(0.00001)  # 10µs pulse
    GPIO.output(trig, False)

    # Wait for Echo to go high and then low
    start_time = time.time()
    while GPIO.input(echo) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    # Calculate pulse duration and convert to distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # cm

    return distance

# === Main loop ===
sensor_index = 0 # Choose sensor 0-3
sum_distance = 0
counter = 0

print(f"Reading from sensor {sensor_index}... Press Ctrl+C to stop.")
try:
    while True:
        if 0 <= sensor_index < len(SENSORS):
            distance = get_distance(sensor_index)

            sum_distance += distance
            counter += 1
            avg_distance = sum_distance / counter

            print(f"[Sensor {sensor_index}] Distance: {distance:.2f} cm | Running Average: {avg_distance:.2f} cm | Samples: {counter}\n")

            time.sleep(0.2)
        else:
            print("Invalid sensor index. Please select 0, 1, 2, or 3.")
except KeyboardInterrupt:
    print("\nStopped by user.")
    GPIO.cleanup()