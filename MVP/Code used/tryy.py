import RPi.GPIO as GPIO
import time

# Pin mappings for HC-SR04 sensors
SENSORS = [
    {'TRIG': 5, 'ECHO': 6},     # Sensor 1
    {'TRIG': 22, 'ECHO': 25},   # Sensor 2
    {'TRIG': 17, 'ECHO': 27},   # Sensor 3
    {'TRIG': 23, 'ECHO': 24}    # Sensor 4
]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for sensor in SENSORS:
    GPIO.setup(sensor['TRIG'], GPIO.OUT)
    GPIO.setup(sensor['ECHO'], GPIO.IN)
    GPIO.output(sensor['TRIG'], False)

time.sleep(2)  # Let sensors settle

# Load thresholds from file
def load_all_thresholds(filename):
    thresholds = []
    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                _, value = line.strip().split(':')
                thresholds.append(float(value.strip()))
    return thresholds

all_thresholds = load_all_thresholds("thresholds.txt")

thresholds1 = all_thresholds[0:3]
thresholds2 = all_thresholds[3:6]
thresholds3 = all_thresholds[6:9]
thresholds4 = all_thresholds[9:12]

# Measure distance in cm
def measure_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(trig_pin, False)

    start = time.time()
    stop = time.time()

    # Wait for echo to go high
    while GPIO.input(echo_pin) == 0:
        start = time.time()
    # Wait for echo to go low
    while GPIO.input(echo_pin) == 1:
        stop = time.time()

    duration = stop - start
    distance_cm = duration * 17150  # speed of sound adjustment
    return round(distance_cm, 2)

# Quantization logic
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

# Sensor access functions
def get_dist_sensor1():
    d = measure_distance(SENSORS[0]['TRIG'], SENSORS[0]['ECHO'])
    return quantize_distance(d, thresholds1)

def get_dist_sensor2():
    d = measure_distance(SENSORS[1]['TRIG'], SENSORS[1]['ECHO'])
    return quantize_distance(d, thresholds2)

def get_dist_sensor3():
    d = measure_distance(SENSORS[2]['TRIG'], SENSORS[2]['ECHO'])
    return quantize_distance(d, thresholds3)

def get_dist_sensor4():
    d = measure_distance(SENSORS[3]['TRIG'], SENSORS[3]['ECHO'])
    return quantize_distance(d, thresholds4)

# Validation & Matching Logic
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