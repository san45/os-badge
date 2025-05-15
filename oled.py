# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from machine import Pin, I2C
import ssd1306

# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(3))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.text('Sanjay', 0, 0, 1)
display.show()
