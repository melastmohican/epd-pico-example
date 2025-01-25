import time
from micropython import const
from digitalio import Direction
import adafruit_framebuf
from adafruit_epd.epd import Adafruit_EPD


_PDI_SOFT_RESET = const(0x00)
_PDI_INPUT_TEMP = const(0xE5)
_PDI_ACTIVE_TEMP = const(0xE0)
_PDI_PANEL_SETTINGS = const(0x00)
_PDI_DCDC_POWER_ON = const(0x04)
_PDI_DCDC_POWER_OFF = const(0x02)
_PDI_DISPLAY_REFRESH = const(0x12)

_PDI_DTM1 = const(0x10)
_PDI_DTM2 = const(0x13)


class EPD_Driver(Adafruit_EPD):
    def __init__(
        self, width, height, spi, cs_pin, dc_pin, sramcs_pin, rst_pin, busy_pin
    ):

        super().__init__(
            width, height, spi, cs_pin, dc_pin, sramcs_pin, rst_pin, busy_pin
        )

        self._buffer1_size = int(width * height / 8)
        self._buffer2_size = int(width * height / 8)

        if sramcs_pin:
            self._buffer1 = self.sram.get_view(0)
            self._buffer2 = self.sram.get_view(self._buffer1_size)
        else:
            self._buffer1 = bytearray((width * height) // 8)
            self._buffer2 = bytearray((width * height) // 8)

        self._framebuf1 = adafruit_framebuf.FrameBuffer(
            self._buffer1, width, height, buf_format=adafruit_framebuf.MHMSB
        )
        self._framebuf2 = adafruit_framebuf.FrameBuffer(
            self._buffer2, width, height, buf_format=adafruit_framebuf.MHMSB
        )
        self.set_black_buffer(0, True)
        self.set_color_buffer(1, True)
        self._single_byte_tx = True


        self._black_inverted = False
        self._color_inverted = False

    def power_up(self):
        """Power up the display in preparation for writing RAM and updating"""
        self._dc.value = True
        if self._rst:
            self._rst.value = True
        self._cs.value = True
        self.power_on_cog()

    def power_down(self):
        """Power down"""
        self.command(_PDI_DCDC_POWER_OFF, bytearray([0x00]))
        self.busy_wait()

        self._dc.value = False
        self._cs.value = False
        if self._busy:
            self._busy.direction = Direction.OUTPUT
            self._busy.value = False
        time.sleep(150 / 1000)
        if self._rst:
            self._rst.value = False

    def power_on_cog(self):
        """ Power on the COG"""
        self.hardware_reset()
        self.soft_reset()

        # https://github.com/PervasiveDisplays/EPD_Driver_GU_small/blob/main/src/EPD_Configuration.h#L226-L228
        self.command(_PDI_INPUT_TEMP, bytearray([0x19]))  # Input Temperature; 0x19=25C ---- 0x12 = 65F/18C
        self.command(_PDI_ACTIVE_TEMP, bytearray([0x02])) # Active Temperature
        self.command(_PDI_PANEL_SETTINGS, bytearray([0xCF, 0x8D]))  # Panel Settings

    def hardware_reset(self):
        if self._rst:
            self._rst.value = False
            time.sleep(1 / 1000)
            self._rst.value = True
            time.sleep(5 / 1000)
            self._rst.value = False
            time.sleep(10 / 1000)
            self._rst.value = True
            time.sleep(5 / 1000)

    def soft_reset(self):
        """Perform a soft reset"""
        self.command(_PDI_SOFT_RESET, bytearray([0x0E]))
        self.busy_wait()


    def busy_wait(self):
        """Wait for display to be done with current task, either by polling the
        busy pin, or pausing"""
        if self._busy:
            while not self._busy.value:
                time.sleep(0.01)
        else:
            time.sleep(0.5)

    def dcdc_power_on(self):
        self.command(_PDI_DCDC_POWER_ON, bytearray([0x00]))
        self.busy_wait()

    def update(self):
        self.dcdc_power_on()
        self.command(_PDI_DISPLAY_REFRESH)
        self.busy_wait()

        self.power_down()


    def write_ram(self, index):
        """Send the one byte command for starting the RAM write process. Returns
        the byte read at the same time over SPI. index is the RAM buffer, can be
        0 or 1 for tri-color displays."""
        if index == 0:
            return self.command(_PDI_DTM1, end=False)
        if index == 1:
            return self.command(_PDI_DTM2, end=False)
        raise RuntimeError("RAM index must be 0 or 1")

    def set_ram_address(self, x, y):  # pylint: disable=unused-argument, no-self-use
        """Set the RAM address location, not used on this chipset but required by
        the superclass"""
        return  # on this chip it does nothing

    def flush(self):
        pass

    def clear(self):
        pass