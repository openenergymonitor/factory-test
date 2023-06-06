#!/usr/bin/bash

uartprogrammer=/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0

# # Use newer version of avrdude (6.3-20190619) 
# echo "- Setting fuses via ISP..."
 /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf -uq -p atmega328p -c usbasp -P usb -e -U lock:w:0x3F:m -U efuse:w:0xFD:m -U hfuse:w:0xDE:m -Ulfuse:w:0xFF:m 

# echo "- Burning bootloader via ISP..."
 /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf -uq -p atmega328p -c usbasp -P usb -U flash:w:/home/pi/factory-test/bootloaders/optiboot_atmega328.hex:i -Ulock:w:0x0F:m 

if [ -e $uartprogrammer ]; then
    echo "- Uploading factory test firmware..."
    /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf  -uq -c arduino -p ATMEGA328P -P $uartprogrammer -b115200 -Uflash:w:/home/pi/factory-test/testfw/EmonTH_FactoryTest.ino.hex:i -l /home/pi/factory-test/avrdude.log
    check=$(grep -e "bytes of flash verified" /home/pi/factory-test/avrdude.log)
    if [ ! "$check" ] ; then
        echo "- Firmware upload: **FAIL**"
    else
        echo "- Firmware upload: PASS"
        echo "- Running function test..."
        python3 /home/pi/factory-test/test-emonth.py
    fi
else
    echo "- ERROR UART Programmer: MISSING"
fi
echo "End"
