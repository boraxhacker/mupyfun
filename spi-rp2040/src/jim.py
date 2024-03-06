from machine import Pin, SPI, mem32
from rp2 import PIO, StateMachine, asm_pio
from neopixel import NeoPixel
from utime import sleep

# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
# 4.4.4. List of Registers
SPI0_BASE = const(0x4003c000)
SSPCR0 = const(0x000)
SSPCR1 = const(0x004)
SSPDR = const(0x008)
SSPSR = const(0x00c)
SSPDMACR = const(0x024)

COLOR_OFF = (0, 0, 0)
COLOR_RED = (0, 128, 0)
COLOR_BLUE = (0, 0, 128)


class RedCommand:
    def __init__(self, neo: NeoPixel):
        self.neo = neo

    def execute(self):
        self.neo.fill(COLOR_RED)
        self.neo.write()


class BlueCommand:
    def __init__(self, neo: NeoPixel):
        self.neo = neo

    def execute(self):
        self.neo.fill(COLOR_BLUE)
        self.neo.write()


class OffCommand:
    def __init__(self, neo: NeoPixel):
        self.neo = neo
        
    def execute(self):
        self.neo.fill(COLOR_OFF)
        self.neo.write()



def spi_cs_handler(spi, spi_cs_pin, cmd_map):
    
    # print('handling...')
    buffer: list[int] = []
    while spi_cs_pin.value() == 0:
        while mem32[SPI0_BASE | SSPSR] & 0x4 == 4:
            buffer.append(spi.read(1)[0])
        
    cmd_name = bytes(buffer).decode('utf-8')
    command = cmd_map.get(cmd_name)
    if command is not None:
        command.execute()

    print(cmd_name)
    

print('Initializing SPI...')

# spi pin mappings, and frequency
spi_baudrate = 100_000

spi_clk_pin = Pin(2, Pin.IN)
spi_tx_pin = Pin(3, Pin.OUT)
spi_rx_pin = Pin(4, Pin.IN)


spi = SPI(0, baudrate=spi_baudrate, polarity=0, phase=1, sck=spi_clk_pin, mosi=spi_tx_pin, miso=spi_rx_pin)

# turn off spp
mem32[SPI0_BASE | SSPCR1] = mem32[SPI0_BASE | SSPCR1] & 0xfffd
print('SSP off', hex(mem32[SPI0_BASE | SSPCR1]))
# enable peripheral mode
mem32[SPI0_BASE | SSPCR1] = mem32[SPI0_BASE | SSPCR1] | 0x0004
# enable ssp
mem32[SPI0_BASE | SSPCR1] = mem32[SPI0_BASE | SSPCR1] | 0x0002
print('SSP on', hex(mem32[SPI0_BASE | SSPCR1]))

neo = NeoPixel(Pin(16), 1)

cmd_map = {
    'GO_COMMAND_RED': RedCommand(neo),
    'GO_COMMAND_BLUE': BlueCommand(neo),
    'GO_COMMAND_OFF': OffCommand(neo)
}

# https://www.raspberrypi.com/documentation/pico-sdk/gpio_8h.html#rpip5cf90c7d2064c9b97298
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
# 2.19.2. Function Select
# set to SPIO CSn
spi_cs_pin_id = const(1)
spi_cs_pin = Pin(spi_cs_pin_id, Pin.ALT, alt=0x1)
spi_cs_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda x: spi_cs_handler(spi, spi_cs_pin, cmd_map))

# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
# 2.19.6.1. IO - User Bank
offset = 0x004 + spi_cs_pin_id * 8
print('CS function', hex(mem32[0x40014000 | 0x00c]))

print('Starting Jim loop...')
try:

    sleep(60)
    print('bump-bump')

finally:

    neo.fill(COLOR_OFF)
    neo.write()






