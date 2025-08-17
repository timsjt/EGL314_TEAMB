## Step 1: Enable I²C on Raspberry Pi
<h3>
1. Open the terminal and run:
</h3>

```
sudo raspi-config
```
<h3>
2. Navigate to Interfacing Options → I²C → Enable
</h3>

<h3>
3. Reboot the Pi:
</h3>

```
sudo reboot
```
<h3>
4. Verify I²C is working:
</h3>


```
sudo I²Cdetect -y 1
```
(You should see the ADS1115 address, typically 0x48).

## Step 2: Install Required 
<h3>
1. Update packages:
</h3>

```
sudo apt update && sudo apt upgrade -y
```

<h3>
2. Install Python libraries (Ultrasonic Sensors):
</h3>

```
sudo apt install python3-pip
pip3 install adafruit-ads1x15
```
<h3>
3. Install Python libraries (Button)
</h3>

```
sudo apt install python3-rpi.gpio
```
The Raspberry Pi OS already includes GPIO support, but you may need to install RPi.GPIO (if not present)

## Step 3: Write a Python Script (Ultrasonic Sensors)
<h3>
1. Initialization Phase
</h3>

```
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
```
<h3>
2. I²C Setup & ADC Configuration
</h3>

```
I²C = busio.I²C(board.SCL, board.SDA)  # Initialize I²C bus
ads = ADS.ADS1115(I²C)                  # Create ADS1115 object
ads.gain = 1                            # Set gain (±4.096V range)
```
* I²C Bus: Uses default GPIO pins (SCL=GPIO3, SDA=GPIO2).

* ADS1115 Settings:
    * Gain 1 means the ADC measures voltages between 0-4.096V (ideal for URM09's 0.3V–2.8V output).

<h3>
3. Sensor Channel Setup
</h3>

```
chan0 = AnalogIn(ads, ADS.P0)  # A0
chan1 = AnalogIn(ads, ADS.P1)  # A1
chan2 = AnalogIn(ads, ADS.P2)  # A2
```
* Analog Channels:
    * Three URM09 sensors connected to A0, A1, A2 of the ADS1115.
    * Each AnalogIn object reads voltage from its respective pin.

<h3>
4. Voltage Reading Function
</h3>

```
def get_voltage(sensor_num=2):  # Defaults to A2 (chan2)
    if sensor_num == 0:
        return chan0.voltage
    elif sensor_num == 1:
        return chan1.voltage
    elif sensor_num == 2:
        return chan2.voltage
    else:
        return 0.0  # Fallback for invalid sensor numbers
```
* Logic:
    * Takes a sensor_num argument (0, 1, or 2) to select which sensor to read.
    * Returns the voltage value from the specified sensor (or 0.0 for invalid inputs).
    * Defaults to A2 (Sensor 3) if no argument is passed.

<h3>
5. Distance Conversion
</h3>

```
def analog_to_distance(voltage):
    return voltage * 100  # Rough estimate (calibrate this!)
```
* Formula:
    * Placeholder linear conversion: Assumes 1V = 100cm.
    * Converts raw voltages to distance estimates

<h3>
6. Distance Quantization
</h3>

```
def quantize_distance(distance):
    if 1 <= distance < 15:
        return 10
    elif 15 <= distance < 25:
        return 20
    elif 25 <= distance < 35:
        return 30
    elif 35 <= distance < 45:
        return 40
    else:
        return distance
```
* Simplifies noisy sensor data into clean, standardized values.
* Processes all channels independently

<h3>
7. Main Loop
</h3>

```
while True:
    # Read all 3 sensors
    voltage0 = get_voltage(0)  # A0
    voltage1 = get_voltage(1)  # A1
    voltage2 = get_voltage(2)  # A2

    # Convert voltages to distances
    distance0 = analog_to_distance(voltage0)
    distance1 = analog_to_distance(voltage1)
    distance2 = analog_to_distance(voltage2)

     # Quantize distances
    quantized0 = quantize_distance(distance0)
    quantized1 = quantize_distance(distance1)
    quantized2 = quantize_distance(distance2)

    print(f"Sensor 1: {quantized0:.1f} cm | Sensor 2: {quantized1:.1f} cm | Sensor 3: {quantized2:.1f} cm")
    time.sleep(0.5)  # Delay to avoid flooding the console
```
* Workflow:
    * Reads voltages from all 3 sensors using get_voltage().
    * Converts voltages to distances using analog_to_distance().
    * Applies quantization to each distance reading
    * Prints distances in a formatted string.
    * Waits 0.5 seconds before repeating.