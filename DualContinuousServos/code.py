import time
import board
import pwmio
from analogio import AnalogIn
from adafruit_motor import servo


class Potentiometer:
    def __init__(self, pin, max_analog=60500, tolerance=400):
        self.__pot = AnalogIn(pin)
        self.value = self.__pot.value
        self.radius = tolerance
        # the ESP32-S3 can only emit up to 61000 from an analog read
        self.max_analog = max_analog

    @property
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


pwm11 = pwmio.PWMOut(board.D11, frequency=50)
pwm12 = pwmio.PWMOut(board.D12, frequency=50)
pot = Potentiometer(board.A5, tolerance=700)
right_servo = servo.ContinuousServo(pwm11, min_pulse=500, max_pulse=2575)
left_servo = servo.ContinuousServo(pwm12, min_pulse=500, max_pulse=2575)

while True:
    if pot.changeDetected:
        speed_and_direction = pot.mapValueTo(-1.0, 1.0, 2)
        # make the zone around zero (stopped) sticky
        if abs(speed_and_direction) < 0.03:
            print('SpeedDir = stopped')
            right_servo.fraction = None
            left_servo.fraction = None
        else:
            print(f'SpeedDir = {speed_and_direction}')
            right_servo.throttle = speed_and_direction
            left_servo.throttle = speed_and_direction
    time.sleep(0.1)
