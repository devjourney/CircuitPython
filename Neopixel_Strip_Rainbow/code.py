import board
import neopixel
import time

PIXEL_PIN = board.A5
NUM_PIXELS = 144
COLOR_ORDER = neopixel.GRB


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS, brightness=0.3, auto_write=False, pixel_order=COLOR_ORDER
)

iteration = 0
while True:
    rainbow_cycle(0.020)  # rainbow cycle with 1ms delay per step
    print("iteration " + str(iteration))
    iteration = iteration + 1
