from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from neopixel import NeoPixel

###
# WARNING FM - clocked input code for PIO
###
@asm_pio(autopush=True,push_thresh=8,in_shiftdir=PIO.SHIFT_LEFT, fifo_join=PIO.JOIN_RX)
def spi_recv():
    label("start")
    jmp("check_cs") # if chip select is low, continue, otherwise jump to check_cs

    wrap_target()
    wait(0, pins, 2)
    wait(1, pins, 2)
    in_(pins, 1)

    label("check_cs")
    jmp(pin, "start") # if chip select is high, go to 'start' state



COLOR_OFF = (0, 0, 0)
COLOR_RED = (0, 128, 0)
COLOR_BLUE = (0, 0, 128)


class RedCommand:
    def __init__(self, neo: NeoPixel):
        self.neo = neo

    def execute(self):
        self.neo.fill(COLOR_RED)
        self.neo.write()

    def stop(self):
        self.neo.fill(COLOR_OFF)
        self.neo.write()


class BlueCommand:
    def __init__(self, neo: NeoPixel):
        self.neo = neo

    def execute(self):
        self.neo.fill(COLOR_BLUE)
        self.neo.write()

    def stop(self):
        self.neo.fill(COLOR_OFF)
        self.neo.write()


neo = NeoPixel(Pin(16), 1)
bluecmd = BlueCommand(neo)
redcmd = RedCommand(neo)

print('Initializing SPI...')

# spi pin mappings, and frequency (times 16 bits?)
spi_baudrate = 100_000 * 16
spi_cs_pin = Pin(1, Pin.IN, Pin.PULL_UP)
spi_clk_pin = Pin(2, Pin.IN, Pin.PULL_UP)
spi_rx_pin = Pin(4, Pin.IN, Pin.PULL_UP)

# Receive bytes from master when using spi.write() on master
receive_sm = StateMachine(0, spi_recv, freq=spi_baudrate, in_base=(spi_rx_pin), jmp_pin=(spi_clk_pin))
receive_sm.active(1)

print('Starting forever loop...')
try:
    buffer: list[int] = []
    while True:
        while receive_sm.rx_fifo():
            buffer.append(receive_sm.get())
            
        if spi_cs_pin.value() and len(buffer):
            command = bytes(buffer).decode('utf-8')
            if command == 'GO_COMMAND_RED':
                redcmd.execute()
            elif command == 'GO_COMMAND_BLUE':
                bluecmd.execute()
                
            print(command)
            buffer = []

finally:

    neo.fill(COLOR_OFF)
    neo.write()





