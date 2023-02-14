# https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/main/examples/led_animation_sequence.py
# https://learn.adafruit.com/circuitpython-led-animations?view=all

import board
import neopixel

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, AMBER, JADE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A5
# Update to match the number of NeoPixels you have connected
pixel_num = 144

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_num, brightness=0.5, auto_write=False)

blink = Blink(pixels, speed=0.5, color=JADE)
comet = Comet(pixels, speed=0.015, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=5, spacing=6, color=AMBER)


animations = AnimationSequence(
    blink, comet, chase, advance_interval=5, auto_clear=True)

while True:
    animations.animate()
