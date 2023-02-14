# https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/main/examples/led_animation_sparkle_animations.py
import board
import neopixel

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import AMBER, JADE

pixel_pin = board.A5
pixel_num = 144

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_num, brightness=0.5, auto_write=False)

sparkle = Sparkle(pixels, speed=0.05, color=AMBER, num_sparkles=10)
sparkle_pulse = SparklePulse(pixels, speed=0.05, period=3, color=JADE)

animations = AnimationSequence(
    sparkle,
    sparkle_pulse,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
