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
    packet = rfm9x.receive(with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("RSSI: {0}".format(rfm9x.last_rssi))
    else:
        print(f"No packet received {count}.")
    count = count + 1
    time.sleep(5.0)