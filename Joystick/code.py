import time
import board
from analogio import AnalogIn
import digitalio
from adafruit_debouncer import Button


class Potentiometer:
    def __init__(self, pin, max_analog=60500, tolerance=400):
        self.__pot = AnalogIn(pin)
        self.value = self.__pot.value
        self.radius = tolerance
        # the ESP32-S3 can only emit up to 61000 from an analog read
        self.max_analog = max_analog

    def changeDetected(self):
        val = self.__pot.value
        if val < (self.value - self.radius):
            # print(f'LO diff={self.value - val}, old={self.value}, new={val}')
            self.value = val
            return True
        if val > (self.value + self.radius):
            # print(f'HI diff={val - self.value}, old={self.value}, new={val}')
            self.value = val
            return True
        return False

    def mapValueTo(self, minimum, maximum, decimal_places=0):
        return round(
            minimum + float(self.__pot.value /
                            self.max_analog * (maximum - minimum)),
            decimal_places
        )

    def percentage(self):
        self.value = self.__pot.value
        result = self.value / self.max_analog
        return max(0.0, min(1.0, result))


potA = Potentiometer(board.A5, tolerance=500)
potX = Potentiometer(board.A2, tolerance=100)
potY = Potentiometer(board.A3, tolerance=100)
btn = digitalio.DigitalInOut(board.D12)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP
switch = Button(btn)

while True:
    switch.update()
    if switch.pressed:
        print(f'X={potX.mapValueTo(0, 255)}, Y={potY.mapValueTo(0, 255)}')
    if potA.changeDetected():
        print(f'A={potA.percentage() * 100}%')
    time.sleep(0.1)
