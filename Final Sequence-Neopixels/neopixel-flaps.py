import time
import math
import random
from rpi_ws281x import PixelStrip, Color
from pythonosc import osc_server, dispatcher
import threading

# ───────── LED CONFIG ─────────
STRIP2_COUNT = 168
STRIP2_PIN = 18
STRIP3_COUNT = 300
STRIP3_PIN = 13

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

strip2 = PixelStrip(STRIP2_COUNT, STRIP2_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel=0)
strip3 = PixelStrip(STRIP3_COUNT, STRIP3_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel=1)

strip2.begin()
strip3.begin()

# Active pixel ranges for each strip
STRIP2_ACTIVE_START = 3
STRIP2_ACTIVE_END = 144
STRIP3_ACTIVE_START = 107
STRIP3_ACTIVE_END = 250

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

# ───────── PURPLISH COLOR PALETTE ─────────
colors = [
    (85, 0, 255),
    (140, 70, 255),
    (200, 100, 255),
    (100, 30, 180),
    (170, 120, 255),
]

# ───────── EFFECTS ─────────
def flowing_ribbons(t, blend=1.0):
    wave_speed = 10
    wave_scale = 15.0
    color_count = len(colors)

    for i in range(STRIP2_ACTIVE_START, STRIP2_ACTIVE_END + 1):
        wave = math.sin((i / wave_scale) + t * wave_speed)
        brightness = (wave + 1) / 2
        index = int((i / wave_scale + t) % color_count)
        next_index = (index + 1) % color_count
        frac = (i / wave_scale + t) % 1.0
        r, g, b = lerp_color(colors[index], colors[next_index], frac)
        r = int(r * brightness * blend)
        g = int(g * brightness * blend)
        b = int(b * brightness * blend)
        strip2.setPixelColor(i - 1, rgb(r, g, b))

    for i in range(STRIP3_ACTIVE_START, STRIP3_ACTIVE_END + 1):
        wave = math.sin((i / wave_scale) + t * wave_speed)
        brightness = (wave + 1) / 2
        index = int((i / wave_scale + t) % color_count)
        next_index = (index + 1) % color_count
        frac = (i / wave_scale + t) % 1.0
        r, g, b = lerp_color(colors[index], colors[next_index], frac)
        r = int(r * brightness * blend)
        g = int(g * brightness * blend)
        b = int(b * brightness * blend)
        strip3.setPixelColor(i - 1, rgb(r, g, b))

    strip2.show()
    strip3.show()

def nebula_wave(t, blend=1.0):
    scale = 20.0
    speed = t * 20.0
    total_colors = len(colors)
    total_length = total_colors * scale

    for i in range(STRIP2_ACTIVE_START, STRIP2_ACTIVE_END + 1):
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
        strip2.setPixelColor(i - 1, rgb(r, g, b))

    for i in range(STRIP3_ACTIVE_START, STRIP3_ACTIVE_END + 1):
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
        strip3.setPixelColor(i - 1, rgb(r, g, b))

    strip2.show()
    strip3.show()

def strobe_effect(t, blend=1.0):
    pulse_colors = colors
    total_colors = len(pulse_colors)
    pattern_width = 20
    offset = int(t * 15) % (pattern_width * total_colors)

    bpm = 125
    beat_duration = 60 / bpm
    phase = (t % beat_duration) / beat_duration
    brightness_factor = math.sin(phase * math.pi) * blend

    for i in range(STRIP2_ACTIVE_START, STRIP2_ACTIVE_END + 1):
        pattern_idx = ((i + offset) // pattern_width) % total_colors
        r, g, b = pulse_colors[pattern_idx]
        brightness = (math.sin((i / 5.0) + t * 8) + 1) / 2
        r = int(r * brightness * brightness_factor)
        g = int(g * brightness * brightness_factor)
        b = int(b * brightness * brightness_factor)
        strip2.setPixelColor(i - 1, rgb(r, g, b))

    for i in range(STRIP3_ACTIVE_START, STRIP3_ACTIVE_END + 1):
        pattern_idx = ((i + offset) // pattern_width) % total_colors
        r, g, b = pulse_colors[pattern_idx]
        brightness = (math.sin((i / 5.0) + t * 8) + 1) / 2
        r = int(r * brightness * brightness_factor)
        g = int(g * brightness * brightness_factor)
        b = int(b * brightness * brightness_factor)
        strip3.setPixelColor(i - 1, rgb(r, g, b))

    strip2.show()
    strip3.show()

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
    center2 = (STRIP2_ACTIVE_START + STRIP2_ACTIVE_END) // 2
    center3 = (STRIP3_ACTIVE_START + STRIP3_ACTIVE_END) // 2

    max_offset2 = center2 - STRIP2_ACTIVE_START
    max_offset3 = center3 - STRIP3_ACTIVE_START
    max_offset = max(max_offset2, max_offset3)

    for offset in range(max_offset + 1):
        # Strip 2
        left2 = center2 - offset
        right2 = center2 + offset
        if STRIP2_ACTIVE_START <= left2 <= STRIP2_ACTIVE_END:
            strip2.setPixelColor(left2 - 1, rgb(255, 255, 255))
        if STRIP2_ACTIVE_START <= right2 <= STRIP2_ACTIVE_END and right2 != left2:
            strip2.setPixelColor(right2 - 1, rgb(255, 255, 255))

        # Strip 3
        left3 = center3 - offset
        right3 = center3 + offset
        if STRIP3_ACTIVE_START <= left3 <= STRIP3_ACTIVE_END:
            strip3.setPixelColor(left3 - 1, rgb(255, 255, 255))
        if STRIP3_ACTIVE_START <= right3 <= STRIP3_ACTIVE_END and right3 != left3:
            strip3.setPixelColor(right3 - 1, rgb(255, 255, 255))

        strip2.show()
        strip3.show()
        time.sleep(0.03)

    # Fade out white brightness smoothly
    for brightness in range(255, -1, -5):
        for i in range(STRIP2_ACTIVE_START, STRIP2_ACTIVE_END + 1):
            strip2.setPixelColor(i - 1, rgb(brightness, brightness, brightness))
        for i in range(STRIP3_ACTIVE_START, STRIP3_ACTIVE_END + 1):
            strip3.setPixelColor(i - 1, rgb(brightness, brightness, brightness))
        strip2.show()
        strip3.show()
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
def run_dual_show_168():
    try:
        start_time = time.time()
        loading_done = False
        current = 0
        total_duration = sum(duration_per_effect)
        effect_ranges = [sum(duration_per_effect[:i+1]) for i in range(len(duration_per_effect))]

        while True:
            elapsed = time.time() - start_time
            if elapsed > total_duration:
                fade_to_black(strip2)
                fade_to_black(strip3)
                break

            if elapsed < 3.5:
                clear_strip(strip2)
                clear_strip(strip3)
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
            start_time_eff = 0 if current == 0 else effect_ranges[current - 1]
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
        fade_to_black(strip2)
        fade_to_black(strip3)

# ───────── OSC SETUP ─────────
start_show = False

def osc_start_handler(addr, *args):
    global start_show
    print("Received OSC /start")
    start_show = True

def start_osc_server(ip="192.168.254.51", port=2629):
    disp = dispatcher.Dispatcher()
    disp.map("/print", osc_start_handler)  # <-- Listening to /start OSC message
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"OSC server running on {ip}:{port}")

# ───────── ENTRY POINT ─────────
if __name__ == "__main__":
    try:
        start_osc_server()  # Start the OSC server
        print("Waiting for OSC /start command...")

        while True:
            if start_show:
                run_dual_show_168()
                start_show = False  # Reset after show ends
                print("Show ended. Waiting for next OSC /start...")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nManual stop. Fading out...")
        fade_to_black(strip2)
        fade_to_black(strip3)
