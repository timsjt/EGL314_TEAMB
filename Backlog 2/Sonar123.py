import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Configure 3 sensors
chan0 = AnalogIn(ads, ADS.P0)  # A0
chan1 = AnalogIn(ads, ADS.P1)  # A1 (original)
chan2 = AnalogIn(ads, ADS.P2)  # A2

# Modified get_voltage() to support all 3 sensors
def get_voltage(sensor_num=2):  # Defaults to original (A1)
    if sensor_num == 0:
        return chan0.voltage
    elif sensor_num == 1:
        return chan1.voltage
    elif sensor_num == 2:
        return chan2.voltage
    else:
        return 0.0  # Invalid sensor

def analog_to_distance(voltage):
    return voltage * 100  # Rough estimate

while True:
    # Read all 3 sensors using get_voltage()
    voltage0 = get_voltage(0)
    voltage1 = get_voltage(1)  # Original behavior
    voltage2 = get_voltage(2)

    distance0 = analog_to_distance(voltage0)
    distance1 = analog_to_distance(voltage1)
    distance2 = analog_to_distance(voltage2)

    print(f"Sensor 1: {distance0:.1f} cm | Sensor 2: {distance1:.1f} cm | Sensor 3: {distance2:.1f} cm")
    time.sleep(0.5)