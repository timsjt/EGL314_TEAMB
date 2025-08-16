import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time

# Initialize components
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Button setup
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lock_in = False  # Global flag

def button_callback(channel):
    global lock_in
    lock_in = True
    print("Button pressed! Answer locked in.")

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

def analog_to_distance(voltage):
    return voltage * 100  # Adjust for real-world calibration

def quantize_distance(distance):
    if distance <= 17:
        return 10
    elif 17 < distance <= 23:
        return 20
    elif 23 < distance <= 28:
        return 30
    else:
        return 40  # Default quantization for distances beyond range

def quantize_distance2(distance):
    if distance <= 18:
        return 10
    elif 18 < distance <= 24:
        return 20
    elif 24 < distance <= 28:
        return 30
    else:
        return 40  # Default quantization for distances beyond range
    
def quantize_distance3(distance):
    if distance <= 17:
        return 10
    elif 17 < distance <= 24:
        return 20
    elif 24 < distance <= 30:
        return 30
    else:
        return 40  # Default quantization for distances beyond range
    
def quantize_distance4(distance):
    if distance <= 19:
        return 10
    elif 19 < distance <= 25:
        return 20
    elif 25 < distance <= 31:
        return 30
    else:
        return 40  # Default quantization for distances beyond range

def get_dist_sensor1():
    return quantize_distance(analog_to_distance(chan0.voltage))

def get_dist_sensor2():
    return quantize_distance2(analog_to_distance(chan1.voltage))

def get_dist_sensor3():
    return quantize_distance3(analog_to_distance(chan2.voltage))

def get_dist_sensor4():
    return quantize_distance4(analog_to_distance(chan3.voltage))

# def get_dist_sensor1():
#     return int(analog_to_distance(chan0.voltage))

# def get_dist_sensor2():
#     return int(analog_to_distance(chan1.voltage))

# def get_dist_sensor3():
#     return int(analog_to_distance(chan2.voltage))

# def get_dist_sensor4():
#     return int(analog_to_distance(chan3.voltage))

def validation(sensor_input):
    try:
        if len(sensor_input) != 4 :
            raise ValueError
        return sensor_input
    except ValueError:
        return None

def matching_numbers(sensor_input, random_no_gen):
    unmatched_randoms = random_no_gen.copy()  # Track unmatched numbers from random_no_gen
    results = []

    # First pass: Mark exact matches as 'green'
    for i, (s, r) in enumerate(zip(sensor_input, random_no_gen)):
        if s == r:
            results.append('green')
            unmatched_randoms[i] = None  # Mark this random number as matched
        else:
            results.append(None)  # Placeholder for now

    # Second pass: Mark 'yellow' and 'red'
    for i, s in enumerate(sensor_input):
        if results[i] is not None:
            continue  # Skip if already marked as 'green'
        if s in unmatched_randoms:
            results[i] = 'yellow'
            unmatched_randoms[unmatched_randoms.index(s)] = None  # Mark as matched
        else:
            results[i] = 'red'

    return results
