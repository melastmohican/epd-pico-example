import board

# Not connected pin
NOT_CONNECTED = None

# https://www.pervasivedisplays.com/product/epd-pico-kit-epdk/
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


Pico_Ext3 = Ext3Pins(
    panel_busy=board.GP13,
    panel_dc=board.GP12,
    panel_reset=board.GP11,
    panel_cs=board.GP17,
    flash_cs=board.GP10
)