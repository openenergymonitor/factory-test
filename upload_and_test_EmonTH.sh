#!/usr/bin/bash

uartprogrammer=/dev/serial/by-id/usb-FTDI_LC231X_FT6QHI03-if00-port0

# echo "test"
# exit 0
# # Use newer version of avrdude (6.3-20190619) 
echo "- Setting fuses via ISP..."
 /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf -uq -p atmega328p -c avrispmkII -P usb -e -U lock:w:0x3F:m -U efuse:w:0xFD:m -U hfuse:w:0xDE:m -Ulfuse:w:0xFF:m -l /home/pi/factory-test/avrdude.log
 check=$(grep -e "1 bytes of lfuse verified" /home/pi/factory-test/avrdude.log)
    if [ ! "$check" ] ; then
        echo "Setting fuses: **FAIL** ...check ISP programmer?"
        tail /home/pi/factory-test/avrdude.log
        echo " "
        exit 1
    else
        echo "Setting fuses: PASS"
    fi

echo "- Burning bootloader via ISP..."
 /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf -uq -p atmega328p -c avrispmkII -P usb -U flash:w:/home/pi/factory-test/bootloaders/optiboot_atmega328.hex:i -Ulock:w:0x0F:m -l /home/pi/factory-test/avrdude.log
  check=$(grep -e "1 bytes of lock verified" /home/pi/factory-test/avrdude.log)
    if [ ! "$check" ] ; then
        echo "Burning bootloader: **FAIL** ...check ISP programmer?"
        echo " "
        tail /home/pi/factory-test/avrdude.log
        exit 1
    else
        echo "Burning bootloader: PASS"
    fi

if [ -L $uartprogrammer ]; then
    echo "- Uploading firmware via UART...wait 15s"
    /home/pi/arduino-1.8.19/hardware/tools/avr/bin/avrdude -C /home/pi/arduino-1.8.19/hardware/tools/avr/etc/avrdude.conf  -uq -c arduino -p ATMEGA328P -P $uartprogrammer -b115200 -Uflash:w:/home/pi/factory-test/testfw/EmonTH_FactoryTest.ino.hex:i -l /home/pi/factory-test/avrdude.log
    check=$(grep -e "bytes of flash verified" /home/pi/factory-test/avrdude.log)
    if [ ! "$check" ] ; then
        echo "Firmware upload: **FAIL** ...check UART programmer?"
        echo " "
        tail /home/pi/factory-test/avrdude.log
        exit 1
    else
        echo "Firmware upload: PASS"
        echo "- Running function test..."
        python3 /home/pi/factory-test/testscript/test-emonth.py
    fi
else
    echo "**FAIL** UART Programmer: MISSING"
    exit 1
fi
echo "End"
exit 0
