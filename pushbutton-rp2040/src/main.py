from machine import Pin, UART, SPI
from neopixel import NeoPixel
from time import sleep


PB_UP = 1
PB_DOWN = 0


class PushButtonCommand:
    def __init__(self, uart: UART, neo: NeoPixel, color: tuple[int, int, int]):
        self.uart = uart
        self.neo = neo
        self.color = color

    def execute(self):
        self.neo[0] = self.color
        self.neo.write()
        
        self.uart.write(f'on-{self.color}\r\n')

    def stop(self):
        self.neo[0] = (0, 0, 0)
        self.neo.write()

        self.uart.write(f'off-{self.color}\r\n')


class PushButton:

    def __init__(self, pin: Pin, command: PushButtonCommand):

        self.pin = pin
        self.command = command

        self.state: int = PB_UP
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.handler)

    def handler(self, pin):

        if pin.value() == PB_DOWN and self.state == PB_UP:

            self.state = PB_DOWN
            self.command.execute()
            print('ON')

        elif pin.value() == PB_UP and self.state == PB_DOWN:

            self.state = PB_UP
            self.command.stop()
            print('OFF')


neo = NeoPixel(Pin(16), 1)

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)

bluepin = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
redpin = Pin(6, mode=Pin.IN, pull=Pin.PULL_UP)

bluebutton = PushButton(bluepin, PushButtonCommand(uart, neo, (0, 0, 128)))
redbutton = PushButton(redpin, PushButtonCommand(uart, neo, (0, 128, 0)))

b: bytes = 0x00
spi = SPI()
try:

    while True:
        sleep(60)
        print('bump-bump')

finally:
    
    neo[0] = (0, 0, 0)
    neo.write()
    