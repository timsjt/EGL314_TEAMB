import time
import math
import random
from rpi_ws281x import PixelStrip, Color

# ───── LED CONFIG ─────
STRIP1_COUNT = 120
STRIP1_PIN = 13  # PWM1 (GPIO13, Channel 1)

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

strip1 = PixelStrip(STRIP1_COUNT, STRIP1_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel=1)
strip1.begin()

# ───── UTILS ─────
def rgb(r, g, b):
    return Color(int(r), int(g), int(b))

def clear_strip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, rgb(0, 0, 0))
    strip.show()

# ───── FULL FLAME EFFECT ─────
def update_rocket_flame(t, brightness=1.0, strobe=False):
    strobe_strength = (math.sin(t * 25) + 1) / 2 if strobe else 1.0

    for i in range(STRIP1_COUNT):
        # Flame intensity decreases toward tip
        pos_factor = 1 - (i / STRIP1_COUNT)
        flicker = random.uniform(0.6, 1.0) * strobe_strength

        r = (200 + 55 * pos_factor) * flicker * brightness
        g = (20 + 80 * pos_factor) * flicker * brightness * 0.5
        b = 0

        strip1.setPixelColor(i, rgb(r, g, b))

    strip1.show()

# ───── MAIN LOOP ─────
try:
    while True:
        t = time.time()
        update_rocket_flame(t)
        time.sleep(0.02)

except KeyboardInterrupt:
    clear_strip(strip1)
