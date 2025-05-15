from micropython import const
import time
import framebuf

# ST7735 Command Codes
_SWRESET = const(0x01)
_SLPOUT = const(0x11)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)

# Rotation Values
ROTATE_0 = const(0x00)
ROTATE_90 = const(0x60)

# Define RGB565 Colors
WHITE   = 0xFFFF
BLACK   = 0x0000
RED     = 0xF800
GREEN   = 0x07E0
BLUE    = 0x001F

class ST7735:
    def __init__(self, spi, cs, dc, rst, rotation=ROTATE_90):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = 128  # Default screen size
        self.height = 128
        self.rotation = rotation

        self.buffer = bytearray(self.width * self.height * 2)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

        # Initialize pins
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)

        # Reset and Initialize Display
        self.reset()
        self.init_display()

    def reset(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

    def write_cmd(self, cmd):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(bytearray([data]) if isinstance(data, int) else data)
        self.cs.value(1)

    def init_display(self):
        self.write_cmd(_SWRESET)  # Software reset
        time.sleep_ms(150)
        self.write_cmd(_SLPOUT)  # Exit sleep mode
        time.sleep_ms(150)
        self.write_cmd(_COLMOD)  # Set color mode
        self.write_data(0x05)  # 16-bit color
        self.write_cmd(_MADCTL)  # Set rotation
        self.write_data(self.rotation)
        self.write_cmd(_DISPON)  # Display on

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(_CASET)
        self.write_data(bytearray([0x00, x0, 0x00, x1]))
        self.write_cmd(_RASET)
        self.write_data(bytearray([0x00, y0, 0x00, y1]))
        self.write_cmd(_RAMWR)

    def fill(self, color):
        self.framebuf.fill(color)

    def show(self):
        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.write_data(self.buffer)

