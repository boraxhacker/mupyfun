from machine import Pin, SPI, mem32
from neopixel import NeoPixel
from time import sleep

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


SPI0_BASE = 0x4003c000
#SSPRXD
SSPCR0 = 0x000
SSPCR1 = 0x004
SSPDR = 0x008
SSPSR = 0x00c


def any():
    # get IC_STATUS
    status = mem32[SPI0_BASE | SSPSR]

    # check RFNE receive fifio not empty
    if status & 0x0c:
        return True
    return False

def get():
    while not any():
        pass
    return mem32[SPI0_BASE | SSPDR] & 0xff


def csel_handler(spi, pin):
    
    print(f'Reading command [CS: {pin}]...')
    count = 0
    buffer: list[int] = []
    while any():
        buffer.append(get())
        #buffer.append(spi.read(1))
        count = count + 1

    print('Yo BuffBoy', buffer, count)
    

neo = NeoPixel(Pin(16), 1)
bluecmd = BlueCommand(neo)
redcmd = RedCommand(neo)

print('Initializing SPI...')

slval = mem32[SPI0_BASE | SSPCR1]
print('Value-Before', hex(slval))

#spi = SPI(0, baudrate=9600, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

mem32[SPI0_BASE | SSPCR0] = mem32[SPI0_BASE | SSPCR0] & 0xff27 | 0x27

print('SSPCR0', hex(mem32[SPI0_BASE | SSPCR0] & 0xff))

mem32[SPI0_BASE | SSPCR1] = slval & 0xff06 | 0x06
slval = mem32[SPI0_BASE | SSPCR1]
print('Value-After', hex(slval))

csel = Pin(1, Pin.IN)
#csel.irq(trigger=Pin.IRQ_FALLING, handler=lambda p : csel_handler(spi, p))
csel.irq(trigger=Pin.IRQ_FALLING, handler=lambda p : csel_handler(None, p))

print('Starting forever loop...')
try:

    buffer = []

    while True:
        sleep(60)
        print('bump-bump')

finally:

    neo.fill(COLOR_OFF)
    neo.write()





