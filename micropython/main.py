from utime import sleep_ms

from epd_driver import EPDDriver, ESCREEN_EPD_266, boardRaspberryPiPico_RP2040_EXT3
from image_data import micropython_266_296x152_BW

epd = EPDDriver(ESCREEN_EPD_266, boardRaspberryPiPico_RP2040_EXT3)

# Initialize CoG
epd.cog_initial()

BW_monoBuffer = micropython_266_296x152_BW
BW_0x00Buffer = micropython_266_296x152_BW
BWR_blackBuffer = micropython_266_296x152_BW
BWR_redBuffer = micropython_266_296x152_BW

# Global Update Call
epd.global_update(BW_monoBuffer, BW_0x00Buffer)
sleep_ms(1000)
epd.global_update(BWR_blackBuffer, BWR_redBuffer)

# Turn off CoG
epd.cog_power_off()
