import pulseio
import time

pwm = pulseio.PulseIn(board.D2)

while True:
    # wait for at least one high pulse
    while len(pwm) == 0 or pwm[0] < 100:
        pass

    # measure high pulse
    high_pulse = pwm.popleft()

    # wait for at least one low pulse
    while len(pwm) == 0 or pwm[0] > 100:
        pass

    # measure low pulse
    low_pulse = pwm.popleft()

    # calculate duty cycle as percentage
    duty_cycle = high_pulse / (high_pulse + low_pulse) * 100

    # print frequency and duty cycle
    print("Frequency: {} Hz".format(pwm.frequency))
    print("Duty Cycle: {:.1f} %".format(duty_cycle))

    # wait for one second
    time.sleep(1)