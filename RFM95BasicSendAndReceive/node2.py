import time
import board
import busio
import digitalio
import adafruit_rfm9x

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# spi = board.SPI()
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.node = 2
rfm9x.destination = 1
counter = 0
msg = f'msg {counter} from {rfm9x.node} to {rfm9x.destination}'
rfm9x.send(bytes(msg, "UTF-8"))
print(f'Sent "{msg}". Listening...')
time_now = time.monotonic()

while True:
    packet = rfm9x.receive(with_header=True)
    if packet is not None:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(str(packet[4:], 'utf-8')))
        print("Received RSSI: {0}".format(rfm9x.last_rssi))
        counter = counter + 1
        if counter % 10 == 0:
            time.sleep(0.5)
            rfm9x.identifier = counter & 0xFF
            msg = f'msg {counter} from {rfm9x.node} to {rfm9x.destination}'
            rfm9x.send(bytes(msg, "UTF-8"), keep_listening=True)
            print(f'Sent "{msg}". Listening...')
