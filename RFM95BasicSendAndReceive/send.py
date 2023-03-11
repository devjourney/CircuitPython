import board
import digitalio
# uncomment the following import if required to initialize the SPI bus
#import busio
import time
import adafruit_rfm9x

# uncomment the next line if the SPI bus hasn't
# already been initialized, e.g. by an attached TFT
#spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# comment out the next line if initializing the SPI bus here
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D9)
reset = digitalio.DigitalInOut(board.D10)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
count = 0

while True:
    rfm9x.send(bytes(f'Packet {count}', "utf-8"))
    print(f'Sent packet {count}')
    count = count + 1
    time.sleep(5.0)
