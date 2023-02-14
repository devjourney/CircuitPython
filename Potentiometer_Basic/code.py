import time
import board
from analogio import AnalogIn


class Potentiometer:
    def __init__(self, pin, max_analog=61000, ohms_tolerance=200):
        self.__pot = AnalogIn(pin)
        self.value = self.__pot.value
        self.radius = ohms_tolerance
        # the ESP32-S3 can only emit up to 61000 from an analog read
        self.max_analog = max_analog

    def changeDetected(self):
        val = self.__pot.value
        if val < (self.value - self.radius) or val > (self.value + self.radius):
            self.value = val
            return True
        return False

    def mapValueTo(self, minimum, maximum, decimal_places=0):
        return round(
            minimum + float(self.__pot.value / self.max_analog * (maximum - minimum)),
            decimal_places,
        )


pot = Potentiometer(board.A1, ohms_tolerance=100)
print((pot.mapValueTo(0, 255),))

while True:
    if pot.changeDetected():
        print((pot.mapValueTo(0, 255),))
    time.sleep(0.4)
