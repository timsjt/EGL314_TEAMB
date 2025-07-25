import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

def analog_to_distance(voltage):
    return voltage * 100  # Calibration factor

def quantize_distance(distance):
    if distance <= 13:
        return 10
    elif distance <= 20:
        return 20
    elif distance <= 25:
        return 30
    else:
        return 40

def quantize_distance2(distance):
    if distance <= 15:
        return 10
    elif distance <= 20:
        return 20
    elif distance <= 25:
        return 30
    else:
        return 40

def quantize_distance3(distance):
    if distance <= 15:
        return 10
    elif distance <= 22:
        return 20
    elif distance <= 26:
        return 30
    else:
        return 40

def quantize_distance4(distance):
    if distance <= 21:
        return 10
    elif distance <= 27:
        return 20
    elif distance <= 30:
        return 30
    else:
        return 40

# def get_dist_sensor1():
#     return analog_to_distance(chan0.voltage)

# def get_dist_sensor2():
#     return analog_to_distance(chan1.voltage)

# def get_dist_sensor3():
#     return analog_to_distance(chan2.voltage)

# def get_dist_sensor4():
#     return analog_to_distance(chan3.voltage)

def get_dist_sensor1():
    return quantize_distance(analog_to_distance(chan0.voltage))

def get_dist_sensor2():
    return quantize_distance2(analog_to_distance(chan1.voltage))

def get_dist_sensor3():
    return quantize_distance3(analog_to_distance(chan2.voltage))

def get_dist_sensor4():
    return quantize_distance4(analog_to_distance(chan3.voltage))

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
###