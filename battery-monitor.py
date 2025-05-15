from machine import Pin, I2C
import ssd1306  # OLED library
import time

# I²C Setup (ESP32: SDA=4, SCL=3)
i2c = I2C(0, scl=Pin(3), sda=Pin(4), freq=400000)

# OLED Display (SSD1306, 128x32)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# LC709203F I²C Address
LC709203F_ADDR = 0x0B

def read_voltage():
    """Reads battery voltage from LC709203F."""
    raw = i2c.readfrom_mem(LC709203F_ADDR, 0x09, 2)  # Voltage register
    voltage = int.from_bytes(raw, 'little') / 1000.0  # Convert to volts
    return voltage

def read_percentage():
    """Reads battery percentage from LC709203F."""
    raw = i2c.readfrom_mem(LC709203F_ADDR, 0x0D, 2)  # Battery % register
    percent = int.from_bytes(raw, 'little') / 256.0  # Convert to %
    return percent

# Main Loop
while True:
    voltage = read_voltage()
    percent = read_percentage()
    
    oled.fill(0)  # Clear screen
    oled.text("Battery Monitor", 10, 2)
    oled.text(f"{voltage:.2f}V  {percent:.1f}%", 10, 20)  # Compact text for 128x32
    oled.show()

    time.sleep(2)



