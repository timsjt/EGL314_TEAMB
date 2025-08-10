import time
import math
import random
from rpi_ws281x import PixelStrip, Color
from pythonosc import dispatcher, osc_server
import threading

# ───────── LED CONFIG ─────────
STRIP0_COUNT = 300
STRIP0_PIN = 18
STRIP1_COUNT = 300
STRIP1_PIN = 13

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

strip0 = PixelStrip(STRIP0_COUNT, STRIP0_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel=0)
strip1 = PixelStrip(STRIP1_COUNT, STRIP1_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel=1)

strip0.begin()
strip1.begin()

ACTIVE_START = 25
ACTIVE_END = 255

# ───────── UTILITIES ─────────
def rgb(r, g, b):
    return Color(int(r), int(g), int(b))

def clear_strip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, rgb(0, 0, 0))
    strip.show()

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

# ───────── EFFECTS ─────────
colors = [
    (17, 0, 158),
    (73, 66, 228),
    (134, 150, 254),
    (196, 176, 255)
]

def flowing_ribbons(t, blend=1.0):
    wave_speed = 10
    wave_scale = 15.0
    color_count = len(colors)

    for i in range(ACTIVE_START, ACTIVE_END + 1):
        wave = math.sin((i / wave_scale) + t * wave_speed)
        brightness = (wave + 1) / 2

        index = int((i / wave_scale + t) % color_count)
        next_index = (index + 1) % color_count
        frac = (i / wave_scale + t) % 1.0

        r, g, b = lerp_color(colors[index], colors[next_index], frac)
        r = int(r * brightness * blend)
        g = int(g * brightness * blend)
        b = int(b * brightness * blend)

        strip0.setPixelColor(i, rgb(r, g, b))
        strip1.setPixelColor(i, rgb(r, g, b))

    strip0.show()
    strip1.show()

def nebula_wave(t, blend=1.0):
    scale = 20.0
    speed = t * 20.0
    total_colors = len(colors)
    total_length = total_colors * scale

    for i in range(ACTIVE_START, ACTIVE_END + 1):
        pos = (i + speed) % total_length
        index = int(pos // scale)
        frac = (pos % scale) / scale

        c1 = colors[index % total_colors]
        c2 = colors[(index + 1) % total_colors]
        r, g, b = lerp_color(c1, c2, frac)

        brightness_wave = (math.sin((i / 10.0) + t) + 1) / 2 * 0.5 + 0.5
        r = int(r * brightness_wave * blend)
        g = int(g * brightness_wave * blend)
        b = int(b * brightness_wave * blend)

        strip0.setPixelColor(i, rgb(r, g, b))
        strip1.setPixelColor(i, rgb(r, g, b))

    strip0.show()
    strip1.show()

def strobe_effect(t, blend=1.0):
    pulse_colors = colors
    total_colors = len(pulse_colors)
    pattern_width = 20
    offset = int(t * 15) % (pattern_width * total_colors)

    bpm = 125
    beat_duration = 60 / bpm
    phase = (t % beat_duration) / beat_duration

    brightness_factor = math.sin(phase * math.pi) * blend

    for i in range(ACTIVE_START, ACTIVE_END + 1):
        pattern_idx = ((i + offset) // pattern_width) % total_colors
        r, g, b = pulse_colors[pattern_idx]
        brightness = (math.sin((i / 5.0) + t * 8) + 1) / 2
        r = int(r * brightness * brightness_factor)
        g = int(g * brightness * brightness_factor)
        b = int(b * brightness * brightness_factor)
        strip0.setPixelColor(i, rgb(r, g, b))
        strip1.setPixelColor(i, rgb(r, g, b))

    strip0.show()
    strip1.show()

# ───────── TRANSITION SYSTEM ─────────
def fade_transition(from_func, to_func, t):
    steps = 30
    for s in range(steps):
        b1 = 1.0 - s / steps
        b2 = s / steps
        from_func(t, b1)
        to_func(t, b2)
        time.sleep(0.02)

# ───────── ANIMATION CYCLE ─────────
duration_per_effect = [10, 7, 6, 7, 14]
effects = [nebula_wave, flowing_ribbons, strobe_effect, flowing_ribbons, nebula_wave]

# ───────── WHITE LOADING ANIMATION ─────────
def white_loading_animation_dual():
    center = (ACTIVE_START + ACTIVE_END) // 2
    for offset in range(center - ACTIVE_START + 1):
        left = ACTIVE_START + offset
        right = ACTIVE_END - offset
        strip0.setPixelColor(left, rgb(255, 255, 255))
        strip0.setPixelColor(right, rgb(255, 255, 255))
        strip1.setPixelColor(left, rgb(255, 255, 255))
        strip1.setPixelColor(right, rgb(255, 255, 255))
        strip0.show()
        strip1.show()
        time.sleep(0.021)
    time.sleep(0.5)
    for brightness in range(255, -1, -5):
        for i in range(ACTIVE_START, ACTIVE_END + 1):
            strip0.setPixelColor(i, rgb(brightness, brightness, brightness))
            strip1.setPixelColor(i, rgb(brightness, brightness, brightness))
        strip0.show()
        strip1.show()
        time.sleep(0.01)

# ───────── FADE TO BLACK FUNCTION ─────────
def fade_to_black(strip):
    for brightness in range(255, -1, -5):
        for i in range(strip.numPixels()):
            color = strip.getPixelColor(i)
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            r = int(r * brightness / 255)
            g = int(g * brightness / 255)
            b = int(b * brightness / 255)
            strip.setPixelColor(i, rgb(r, g, b))
        strip.show()
        time.sleep(0.05)

# ───────── MAIN LOOP ─────────
def run_dual_show():
    try:
        start_time = time.time()
        loading_done = False
        current = 0
        total_duration = sum(duration_per_effect)
        effect_ranges = [sum(duration_per_effect[:i+1]) for i in range(len(duration_per_effect))]

        while True:
            elapsed = time.time() - start_time
            if elapsed > total_duration:
                fade_to_black(strip0)
                fade_to_black(strip1)
                break

            if elapsed < 3.5:
                clear_strip(strip0)
                clear_strip(strip1)
                time.sleep(0.02)
                continue

            if not loading_done:
                white_loading_animation_dual()
                loading_done = True
                start_time = time.time() - 3.5
                elapsed = 3.5

            for i, end_time in enumerate(effect_ranges):
                if elapsed < end_time:
                    current = i
                    break

            blend = 1.0
            start_time_eff = 0 if current == 0 else effect_ranges[current-1]
            end_time_eff = effect_ranges[current]
            duration = end_time_eff - start_time_eff
            local_t = elapsed - start_time_eff

            fade_duration = 2.0
            if local_t < fade_duration:
                blend = local_t / fade_duration
            elif local_t > duration - fade_duration:
                blend = (duration - local_t) / fade_duration

            effects[current](elapsed, blend)
            time.sleep(0.02)

    finally:
        fade_to_black(strip0)
        fade_to_black(strip1)

# ───────── OSC SETUP ─────────
start_show = False

def osc_start_handler(addr, *args):
    global start_show
    print("Received OSC /start")
    start_show = True

def start_osc_server(ip="192.168.254.49", port=2629):
    disp = dispatcher.Dispatcher()
    disp.map("/print", osc_start_handler)
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"OSC server running on {ip}:{port}")

# ───────── ENTRY POINT ─────────
if __name__ == "__main__":
    start_osc_server()
    print("Waiting for OSC '/start' message...")
    try:
        while not start_show:
            time.sleep(0.1)
        run_dual_show()
    except KeyboardInterrupt:
        print("Stopped manually. Fading to black...")
        fade_to_black(strip0)
        fade_to_black(strip1)
