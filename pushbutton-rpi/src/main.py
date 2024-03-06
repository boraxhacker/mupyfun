from time import sleep
from gpiozero import Button, LED, OutputDevice
from spidev import SpiDev

print('Initializing SPI...')
# CLK -> GPIO11
# MISO / CIPO -> GPIO10
# MOSI / COPI -> GPIO9
# CS -> GPIO8
spi = SpiDev(0, 0)


def btnblue_pressed_handler():
    print(list(b'GO_COMMAND_BLUE'))
    spi.writebytes(list(b'GO_COMMAND_BLUE'))
    ledblue.on()


def btnblue_released_handler():
    print(list(b'GO_COMMAND_BLUE_OFF'))
    spi.writebytes(list(b'GO_COMMAND_OFF'))
    ledblue.off()


def btnred_pressed_handler():
    print(list(b'GO_COMMAND_RED'))
    spi.writebytes(list(b'GO_COMMAND_RED'))
    ledred.on()


def btnred_released_handler():
    print(list(b'GO_COMMAND_RED_OFF'))
    spi.writebytes(list(b'GO_COMMAND_OFF'))
    ledred.off()


ledblue = LED(23)
ledred = LED(24)

print('Testing LEDS...')
ledblue.on()
ledred.on()
sleep(2)
ledblue.off()
ledred.off()

print('Linking LEDS with buttons...')
btnblue = Button(18, pull_up=True)
btnblue.when_pressed = btnblue_pressed_handler
btnblue.when_released = btnblue_released_handler

btnred = Button(22, pull_up=True)
btnred.when_pressed = btnred_pressed_handler
btnred.when_released = btnred_released_handler

print('Starting forever loop...')
try:

    spi.open(0, 0)
    spi.max_speed_hz = 100_000
    spi.mode = 0x1

    while True:
        sleep(60)
        print('bump-bump')

finally:
    ledblue.off()
    ledred.off()
    spi.close()

