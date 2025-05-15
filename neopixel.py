import machine
import time

class NeoPixel:
    def __init__(self, pin, num_leds):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.num_leds = num_leds
        self.buffer = bytearray(num_leds * 3)  # Each LED needs 3 bytes (RGB)

    def __setitem__(self, i, color):
        """Set the color of an individual LED."""
        if i < 0 or i >= self.num_leds:
            return
        r, g, b = color
        self.buffer[i * 3] = g  # WS2812 uses GRB order
        self.buffer[i * 3 + 1] = r
        self.buffer[i * 3 + 2] = b

    def write(self):
        """Send color data to the LEDs."""
        for i in range(self.num_leds):
            # Write the color bits for each LED
            for j in range(24):  # 8 bits per color (RGB)
                self.send_bit(self.buffer[i * 3 + (j // 8)], j % 8)

    def send_bit(self, byte, bit):
        """Send a single bit to the WS2812."""
        self.pin.value((byte >> (7 - bit)) & 1)
        time.sleep_us(1)  # Adjust time for the timing requirements of WS2812

    def fill(self, color):
        """Fill the entire strip with one color."""
        for i in range(self.num_leds):
            self[i] = color
        self.write()

