import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from epd_driver import EPD_Driver
from ext3_pins import Pico_Ext3

# create the spi device and pins we will need
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

ecs = digitalio.DigitalInOut(Pico_Ext3.panel_cs)
dc = digitalio.DigitalInOut(Pico_Ext3.panel_dc)
srcs = None 
rst = digitalio.DigitalInOut(Pico_Ext3.panel_reset)
rst.direction = digitalio.Direction.OUTPUT
rst.drive_mode = digitalio.DriveMode.PUSH_PULL
busy = digitalio.DigitalInOut(Pico_Ext3.panel_busy)

print("Creating display")

display = EPD_Driver(
    152,
    296,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst, 
    busy_pin=busy
)

display.rotation = 3

# clear the buffer
print("Clear buffer")
display.fill(Adafruit_EPD.WHITE)
display.pixel(10, 100, Adafruit_EPD.BLACK)

print("Draw Rectangles")
display.fill_rect(5, 5, 10, 10, Adafruit_EPD.RED)
display.rect(0, 0, 20, 30, Adafruit_EPD.BLACK)

print("Draw lines")
display.line(0, 0, display.width - 1, display.height - 1, Adafruit_EPD.BLACK)
display.line(0, display.height - 1, display.width - 1, 0, Adafruit_EPD.RED)

print("Draw text")
display.text("hello world", 25, 10, Adafruit_EPD.BLACK)
display.display()

