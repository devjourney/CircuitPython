import time
import board
import pwmio
from analogio import AnalogIn
from adafruit_motor import servo
import digitalio
from adafruit_debouncer import Button


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


# two continuous rotation servos on D11 and D12
pwm11 = pwmio.PWMOut(board.D11, frequency=50)
pwm12 = pwmio.PWMOut(board.D12, frequency=50)
right_servo = servo.ContinuousServo(pwm11, min_pulse=1000, max_pulse=2000)
left_servo = servo.ContinuousServo(pwm12, min_pulse=1000, max_pulse=2000)

# a potentiometer on A5 for servo speed and direction control
pot = Potentiometer(board.A5, tolerance=700)

# a debounced button on D10 to toggle in and out of sticky mode
btn10 = digitalio.DigitalInOut(board.D10)
btn10.direction = digitalio.Direction.INPUT
btn10.pull = digitalio.Pull.UP
sticky_button = Button(btn10)

# track sticky mode
sticky = True

while True:
    sticky_button.update()
    if sticky_button.pressed:
        sticky = not sticky

    if pot.changeDetected:
        speed_and_direction = pot.mapValueTo(-0.4, 0.45, 3)
        # make the zone around zero (stopped) sticky when enabled
        if sticky and abs(speed_and_direction) < 0.015:
            right_servo.fraction = None
            left_servo.fraction = None
            print(
                f'SD={speed_and_direction} (stopped), DC={pwm11.duty_cycle}, Sticky={sticky}')
        else:
            right_servo.throttle = speed_and_direction
            left_servo.throttle = speed_and_direction
            print(
                f'SD={speed_and_direction}, DC={pwm11.duty_cycle}, Sticky={sticky}')
    time.sleep(0.1)
