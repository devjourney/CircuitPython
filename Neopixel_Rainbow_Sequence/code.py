# https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/main/examples/led_animation_rainbow_animations.py
# https://learn.adafruit.com/circuitpython-led-animations?view=all
import board
import neopixel

from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence

pixel_pin = board.A5
pixel_num = 144

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_num, brightness=0.5, auto_write=False)

rainbow = Rainbow(pixels, speed=0.1, period=2)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=5, spacing=3)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)


animations = AnimationSequence(
    rainbow,
    rainbow_chase,
    rainbow_comet,
    rainbow_sparkle,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
