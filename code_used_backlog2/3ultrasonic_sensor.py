import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Configure sensor channels
sensor1 = AnalogIn(ads, ADS.P0)  # A0
sensor2 = AnalogIn(ads, ADS.P1)  # A1
sensor3 = AnalogIn(ads, ADS.P2)  # A2

# Calibration (adjust based on your sensor)
VOLTAGE_PER_CM = 0.0049  # 4.9mV per cm (example)

def read_distance(voltage):
    return voltage / VOLTAGE_PER_CM

try:
    while True:
        # Read voltages
        v1 = sensor1.voltage
        v2 = sensor2.voltage
        v3 = sensor3.voltage

        # Calculate distances
        d1 = read_distance(v1)
        d2 = read_distance(v2)
        d3 = read_distance(v3)

        print(f"Sensor 1: {d1:.1f} cm | Sensor 2: {d2:.1f} cm | Sensor 3: {d3:.1f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped.")
