import time
import board
import digitalio
#import analogio
import pwmio
import adafruit_thermistor

'''
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return round(steinhart, 1)
'''

# thermistor = analogio.AnalogIn(board.GP28)
thermistor = adafruit_thermistor.Thermistor(
    board.GP28, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.GP5)
button.switch_to_input(pull=digitalio.Pull.DOWN)
buzzer = pwmio.PWMOut(board.GP16, frequency=680, duty_cycle=0, variable_frequency=True)
last_press_state = False
last_temp_C = 0.0

while True:
    # current_temp = steinhart_temperature_C(10000 / (65535/thermistor.value - 1))
    current_temp = round(thermistor.temperature, 1)
    if abs(current_temp - last_temp_C) > 0.6:
        last_temp_C = current_temp
        print(f'Temp = {current_temp}℃ {current_temp * 1.8 + 32}℉')
    current_press_state = button.value
    if (current_press_state != last_press_state):
        # print(f'Changing button state from {last_press_state} to {current_press_state}')
        last_press_state = current_press_state
        led.value = last_press_state
        if last_press_state:
            buzzer.duty_cycle = 2 ** 15
            time.sleep(0.1)
            buzzer.duty_cycle = 0
    # time.sleep(0.25)
