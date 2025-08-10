import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Digital Ultrasonic Sensor GPIO Pins (HC-SR04)
SENSORS = [
    {"Trig": 5,  "Echo": 6},   # Sensor A
    {"Trig": 22, "Echo": 25},  # Sensor B
    {"Trig": 17, "Echo": 27},  # Sensor C
    {"Trig": 23, "Echo": 24},  # Sensor D
]

# Setup GPIO pins
for sensor in SENSORS:
    GPIO.setup(sensor["Trig"], GPIO.OUT)
    GPIO.setup(sensor["Echo"], GPIO.IN)
    GPIO.output(sensor["Trig"], False)

time.sleep(2)

# Load quantization thresholds
def load_all_thresholds(filename):
    thresholds = []
    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                _, value = line.strip().split(':')
                thresholds.append(float(value.strip()))
    return thresholds

all_thresholds = load_all_thresholds("thresholds.txt")
threshold_sets = [all_thresholds[i:i+3] for i in range(0, 12, 3)]

# Distance measurement function
def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.01)
    GPIO.output(trig, True)
    time.sleep(0.001)
    GPIO.output(trig, False)

    start = time.time()
    timeout = start + 0.2

    while GPIO.input(echo) == 0:
        start = time.time()
        if start > timeout:
            return -1
    while GPIO.input(echo) == 1:
        end = time.time()
        if end > timeout:
            return -1

    duration = end - start
    distance = duration * 17150
    return round(distance, 2)

# Quantize to 10 / 20 / 30 / 40
def quantize_distance(distance, thresholds):
    t1, t2, t3 = thresholds
    if distance <= t1:
        return 10
    elif distance <= t2:
        return 20
    elif distance <= t3:
        return 30
    else:
        return 40

# Individual sensor functions
def get_dist_sensor1():
    d = get_distance(SENSORS[0]["Trig"], SENSORS[0]["Echo"])
    return quantize_distance(d, threshold_sets[0]) if d != -1 else 0

def get_dist_sensor2():
    d = get_distance(SENSORS[1]["Trig"], SENSORS[1]["Echo"])
    return quantize_distance(d, threshold_sets[1]) if d != -1 else 0

def get_dist_sensor3():
    d = get_distance(SENSORS[2]["Trig"], SENSORS[2]["Echo"])
    return quantize_distance(d, threshold_sets[2]) if d != -1 else 0

def get_dist_sensor4():
    d = get_distance(SENSORS[3]["Trig"], SENSORS[3]["Echo"])
    return quantize_distance(d, threshold_sets[3]) if d != -1 else 0

# Input validation and matching logic (unchanged)
def validation(sensor_input):
    return sensor_input if len(sensor_input) == 4 else None

def matching_numbers(sensor_input, random_no_gen):
    unmatched_randoms = random_no_gen.copy()
    results = []
    for i, (s, r) in enumerate(zip(sensor_input, random_no_gen)):
        if s == r:
            results.append('green')
            unmatched_randoms[i] = None
        else:
            results.append(None)
    for i, s in enumerate(sensor_input):
        if results[i] is not None:
            continue
        if s in unmatched_randoms:
            results[i] = 'yellow'
            unmatched_randoms[unmatched_randoms.index(s)] = None
        else:
            results[i] = 'red'
    return results
