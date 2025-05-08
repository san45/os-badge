# os-badge

To flash microcontroller

Steps here:
https://micropython.org/download/ESP32_GENERIC_S3/

Download Thonny from below

https://thonny.org/

Testing the Installation

Important: before testing the installation, your ESP32/ESP8266 board needs to be flashed with MicroPython firmware (see the previous step).

Connect the board to your computer using a USB cable. To test the installation, you need to tell Thonny that you want to run MicroPython Interpreter and select the board you are using.

1. Go to Tools > Options and select the Interpreter tab. Make sure you’ve selected the right interpreter for your board as well as the COM port.

You can also select the “Try to detect automatically” option, but only if you just have one board connected to your computer at a time. Otherwise, select the specific port for the board you’re using.

2. Thonny IDE should now be connected to your board and you should see the prompt on the Shell.

Creating the boot.py file on your board

1. When you open Thonny IDE for the first time, the Editor shows an untitled file. Save that file as boot.py by clicking on the save icon.
In Where to save choose MicroPython device

