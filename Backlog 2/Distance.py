import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time


# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Set gain (adjust based on max expected voltage)
# - GAIN=1 for 0-4.096V (default)
# - GAIN=2/3 for 0-6.144V (if URM09 outputs 5V)
ads.gain = 1

# Configure analog input (A0)
chan = AnalogIn(ads, ADS.P1)

def get_voltage():
    return chan.voltage

# URM09 calibration (adjust based on datasheet)
def analog_to_distance(voltage):
    # URM09 analog voltage to distance conversion
    # Datasheet: output is roughly linear: 0.3V to 2.5V → 30cm to 500cm
    # Example formula: distance_cm = voltage / 0.00488 (or approximate based on testing)
    return voltage * 100  # Rough estimate, calibrate based on your unit

while True:
    voltage = chan.voltage
    distance = analog_to_distance(voltage)
    distance_int = int(distance)
    if 1 <= distance < 15:
        distance = 10
    elif 15 <= distance < 25:
        distance = 20
    elif 25 <= distance < 35:
        distance = 30
    elif 35 <= distance < 45:
        distance = 40
    else:
        distance = distance

    print(f"Voltage: {voltage:.2f} V | Estimated Distance: {distance} cm")
    time.sleep(0.5)