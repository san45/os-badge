from machine import Pin, SPI, PWM
import st7735
import time

# SPI Configuration for ESP32 with updated pin mappings
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(12), mosi=Pin(11), miso=Pin(9))

# TFT Display Pins
cs = Pin(10, Pin.OUT)
dc = Pin(13, Pin.OUT)
rst = Pin(8, Pin.OUT)

# Initialize Display with 90-degree rotation
display = st7735.ST7735(spi, cs=cs, dc=dc, rst=rst, width=128, height=128, rotation=st7735.ROTATE_90)

# Control Backlight Brightness (0 - 1023)
led = PWM(Pin(47))  # Use GPIO 47 for backlight
led.freq(1000)
led.duty(100)  # Adjust this value for brightness (0 = off, 1023 = full brightness)

# Clear Screen
display.fill(st7735.BLACK)
display.show()

# Draw Text
display.text("ESP32 + TFT", 10, 10, st7735.WHITE)
display.show()

# Draw a Filled Red Rectangle
display.fill_rect(10, 30, 100, 50, st7735.RED)
display.show()

# Draw a Blue Circle (approximation)
for i in range(20):
    display.fill_rect(50 - i, 80 - i, i * 2, i * 2, st7735.BLUE)
display.show()



