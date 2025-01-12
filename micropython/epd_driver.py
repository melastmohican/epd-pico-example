from machine import Pin, SPI
from utime import sleep_ms

# Monochrome screens and default color screens
# SMALL-sized
ESCREEN_EPD_154 = 0x1509  # reference xE2154CSxxx
ESCREEN_EPD_213 = 0x2100  # reference xE2213CSxxx
ESCREEN_EPD_266 = 0x2600  # reference xE2266CSxxx
ESCREEN_EPD_271 = 0x2700  # reference xE2271CSxxx
ESCREEN_EPD_287 = 0x2800  # reference xE2287CSxxx
ESCREEN_EPD_370 = 0x3700  # reference xE2370CSxxx
ESCREEN_EPD_417 = 0x4100  # reference xE2417CSxxx
ESCREEN_EPD_437 = 0x430C  # reference xE2437CSxxx

# MID-sized
ESCREEN_EPD_581 = 0x580B  # reference xE2581CS0Bx, same as eScreen_EPD_581_0B
ESCREEN_EPD_741 = 0x740B  # reference xE2741CS0Bx, same as eScreen_EPD_741_0B

FRAME_SIZE_EPD_EXT3_154 = 2888
FRAME_SIZE_EPD_EXT3_213 = 2756
FRAME_SIZE_EPD_EXT3_266 = 5624
FRAME_SIZE_EPD_EXT3_271 = 5808
FRAME_SIZE_EPD_EXT3_287 = 4736
FRAME_SIZE_EPD_EXT3_370 = 12480
FRAME_SIZE_EPD_EXT3_417 = 15000
FRAME_SIZE_EPD_EXT3_437 = 10560
FRAME_SIZE_EPD_EXT3_581 = 23040
FRAME_SIZE_EPD_EXT3_741 = 48000

# Screen resolutions for small and mid-sized EPDs
epd_idx = [0x15, 0x21, 0x26, 0x27, 0x28, 0x37, 0x41, 0x43, 0x58, 0x74]
image_data_size = [2888, 2756, 5624, 5808, 4736, 12480, 15000, 10560, 23040, 48000]

# Not connected pin
NOT_CONNECTED = 0xFF


class Ext3Pins:
    def __init__(self, panel_busy, panel_dc, panel_reset, panel_cs, flash_cs, panel_css=NOT_CONNECTED,
                 flash_css=NOT_CONNECTED):
        # EXT3 and EXT3.1 pin 1 Black -> +3.3V
        # EXT3 and EXT3.1 pin 2 Brown -> SPI SCK
        self.panel_busy = panel_busy  # EXT3 and EXT3.1 pin 3 Red
        self.panel_dc = panel_dc  # EXT3 and EXT3.1 pin 4 Orange
        self.panel_reset = panel_reset  # EXT3 and EXT3.1 pin 5 Yellow
        # EXT3 and EXT3.1 pin 6 Green -> SPI MISO
        # EXT3 and EXT3.1 pin 7 Blue -> SPI MOSI
        self.panel_cs = panel_cs  # EXT3 and EXT3.1 pin 8 Violet
        self.flash_cs = flash_cs  # EXT3 and EXT3.1 pin 9 Grey
        # EXT3 and EXT3.1 pin 10 White -> GROUND
        self.panel_css = panel_css  # EXT3 and EXT3.1 pin 12 Grey2
        self.flash_css = flash_css  # EXT3 pin 20 or EXT3.1 pin 11 Black2


# Board configurations
boardLaunchPad_EXT3 = Ext3Pins(
    panel_busy=11,
    panel_dc=12,
    panel_reset=13,
    panel_cs=19,
    flash_cs=NOT_CONNECTED
)

boardRaspberryPiPico_RP2040_EXT3 = Ext3Pins(
    panel_busy=13,
    panel_dc=12,
    panel_reset=11,
    panel_cs=17,
    flash_cs=10
)

boardArduinoM0Pro_EXT3 = Ext3Pins(
    panel_busy=4,
    panel_dc=5,
    panel_reset=6,
    panel_cs=8,
    flash_cs=NOT_CONNECTED
)

# Register initializations
# 0x00, soft-reset, temperature, active temp, PSR0, PSR1
register_data_mid = [0x00, 0x0E, 0x19, 0x02, 0x0F, 0x89]
register_data_sm = [0x00, 0x0E, 0x19, 0x02, 0xCF, 0x8D]


class EPDDriver:
    def __init__(self, escreen_epd, board: Ext3Pins):
        self.spi_basic = board

        # Set pin modes
        self.busy = Pin(self.spi_basic.panel_busy, Pin.IN)
        self.dc = Pin(self.spi_basic.panel_dc, Pin.OUT, Pin.PULL_UP)
        self.reset = Pin(self.spi_basic.panel_reset, Pin.OUT, Pin.PULL_UP)
        self.cs = Pin(self.spi_basic.panel_cs, Pin.OUT, Pin.PULL_UP)
        self.spi = SPI(0, baudrate=100000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

        # Type
        self.pdi_cp = int(escreen_epd)
        self.pdi_size = int(escreen_epd >> 8)

        _screenSizeV = 0
        _screenSizeH = 0
        _screenDiagonal = 0
        _refreshTime = 0

        if self.pdi_size == 0x15:  # 1.54"
            _screenSizeV = 152  # vertical = wide size
            _screenSizeH = 152  # horizontal = small size
            _screenDiagonal = 154
            _refreshTime = 16

        elif self.pdi_size == 0x21:  # 2.13"
            _screenSizeV = 212  # vertical = wide size
            _screenSizeH = 104  # horizontal = small size
            _screenDiagonal = 213
            _refreshTime = 15

        elif self.pdi_size == 0x26:  # 2.66"
            _screenSizeV = 296  # vertical = wide size
            _screenSizeH = 152  # horizontal = small size
            _screenDiagonal = 266
            _refreshTime = 15

        elif self.pdi_size == 0x27:  # 2.71"
            _screenSizeV = 264  # vertical = wide size
            _screenSizeH = 176  # horizontal = small size
            _screenDiagonal = 271
            _refreshTime = 19

        elif self.pdi_size == 0x28:  # 2.87"
            _screenSizeV = 296  # vertical = wide size
            _screenSizeH = 128  # horizontal = small size
            _screenDiagonal = 287
            _refreshTime = 14

        elif self.pdi_size == 0x37:  # 3.70"
            _screenSizeV = 416  # vertical = wide size
            _screenSizeH = 240  # horizontal = small size
            _screenDiagonal = 370
            _refreshTime = 15  # ?

        elif self.pdi_size == 0x41:  # 4.17"
            _screenSizeV = 300  # vertical = wide size
            _screenSizeH = 400  # horizontal = small size
            _screenDiagonal = 417
            _refreshTime = 19

        elif self.pdi_size == 0x43:  # 4.37"
            _screenSizeV = 480  # vertical = wide size
            _screenSizeH = 176  # horizontal = small size
            _screenDiagonal = 437
            _refreshTime = 21

        # Actually for 1 color; BWR requires 2 pages
        self.image_data_size = int(_screenSizeV) * int(_screenSizeH // 8)

        self.register_data = register_data_sm[:len(register_data_sm)]

    # CoG initialization function
    # Implements Tcon(COG) power - on and temperature input to COG
    # INPUT:
    #   - none but requires global variables on SPI pinout and config register data
    def cog_initial(self):
        self.dc.high()
        self.reset.high()
        self.cs.high()
        sleep_ms(5)

        # Power On COG driver sequence
        self._reset(1, 5, 10, 5, 1)

        self._soft_reset()

        self._send_index_data(0xe5, self.register_data, 1, 2)  # Input Temperature: 25C
        self._send_index_data(0xe0, self.register_data, 1,2)  # Active Temperature
        self._send_index_data(0x00, self.register_data, 2, 4)  # PSR

    # CoG shutdown function
    # Shuts down the CoG and DC/DC circuit after all update functions
    # INPUT:
    #   - none, but requires global variables for SPI pinout and config register data
    def cog_power_off(self):
        # Send the command to turn off DC/DC
        self._send_index_data(0x02, self.register_data, 0, 0)  # Turn off DC/DC

        # Wait until the panel is no longer busy
        while self.busy.value() != Pin.PULL_UP:
            pass

        # Set panel pins to low states
        self.dc.low()
        self.cs.low()
        self.busy.low()

        # Wait for 150 milliseconds
        sleep_ms(15)

        # Reset the panel
        self.reset.low()

    # Global Update function
    # Implements global update functionality on either small/mid EPD
    # INPUT:
    #   - Two image data arrays (either BW and 0x00, or BW and BWR types)
    def global_update(self, data1s, data2s):
        # Send the first frame
        self._send_index_data(0x10, data1s, self.image_data_size)  # First frame

        # Send the second frame
        self._send_index_data(0x13, data2s, self.image_data_size)  # Second frame

        # Perform DC/DC power on
        self._dcdc_power_on()

        # Refresh the display
        self._display_refresh()

        # Optional: Handle chip select, if needed
        # self.cs.high()

    # SPI transfer function
    # Implements SPI transfer of index and data (consult user manual for EPD SPI process)
    # - INPUT:
    #   - register address
    #   - pointer to data byte array
    #   - length/size of data
    def _send_index_data(self, index, data, length, start_index=0):
        # Set DC (Data/Command) pin to LOW
        self.dc.low()  # DC Low

        # Set CS (Chip Select) pin to LOW
        self.cs.low()  # CS Low

        # Transfer the index (command)
        self.spi.write(bytearray([index]))

        # Set CS pin back to HIGH
        self.cs.high()  # CS High

        # Set DC pin to HIGH for data phase
        self.dc.high()  # DC High

        # Set CS pin to LOW before transferring data
        self.cs.low()  # CS Low

        # Loop through the data and transfer each byte
        self.spi.write(bytearray(data[start_index:start_index+length]))

        # Set CS pin back to HIGH after data transfer
        self.cs.high()  # CS High

    # CoG soft-reset function
    # INPUT:
    #   - none, but requires global variables for SPI pinout and config register data
    def _soft_reset(self):
        # Send the soft-reset command
        self._send_index_data(0x00, self.register_data, 1, 1)  # Soft-reset to run the internal LUT for global update

        # Wait until the panel is no longer busy
        while self.busy.value() != Pin.PULL_UP:
            pass

    # EPD Screen refresh function
    # INPUT:
    #   - none, but requires global variables for SPI pinout and config register data
    def _display_refresh(self):
        # Send the display refresh command
        self._send_index_data(0x12, self.register_data, 1, 0)  # Display Refresh

        # Wait until the panel is no longer busy
        while self.busy.value() != Pin.PULL_UP:
            pass

    # CoG driver power-on hard reset
    # INPUT:
    #   - none, but requires global variables for SPI pinout and config register data
    def _reset(self, ms1, ms2, ms3, ms4, ms5):
        # Group delays into one array
        sleep_ms(ms1)
        self.reset.high()  # RES# = 1
        sleep_ms(ms2)
        self.reset.low()  # RES# = 0
        sleep_ms(ms3)
        self.reset.high()  # RES# = 1
        sleep_ms(ms4)
        self.cs.high()  # CS# = 1
        sleep_ms(ms5)

    # DC-DC power-on command
    # Implemented after image data are uploaded to CoG
    # Specific to small-sized EPDs only
    # INPUT:
    #   - none, but requires global variables for SPI pinout and config register data
    def _dcdc_power_on(self):
        # Send the power-on command
        self._send_index_data(0x04, self.register_data, 1, 0)  # Power on

        # Wait until the panel is no longer busy
        while self.busy.value() != Pin.PULL_UP:
            pass
