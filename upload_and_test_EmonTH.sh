#!/usr/bin/bash

exit 0

if [ -L /dev/serial/by-id/XXXXISPPROGXXXX ] ; then
    if [ -e /dev/serial/by-id/XXXISPPROGXXXXX ] ; then
        echo "- Burning bootloader via ISP..."
        /usr/bin/avrdude -p atmega328p -c usbasp -P usb -e -U efuse:w:0x05:m -U hfuse:w:0xD6:m -U lfuse:w:0xFF:m -U flash:w:/home/pi/factory-test/bootloaders/optiboot_atmega328.hex:i -Ulock:w:0x0f:m > /home/pi/factory-test/isp.log       
        check=$(grep -e "Verify successful TODO" /home/pi/factory-test/isp.log)
        if [ ! "$check" ] ; then
            echo "- Bootloader upload: **FAIL** ..is ISP connected correctly?"
        else
            echo "- Bootloader upload: PASS" 
            
            if [ -L /dev//dev/serial/by-id/XXXUARTPPROGXXXXX ] ; then
                if [ -e /dev//dev/serial/by-id/XXXUARTPPROGXXXXX ] ; then
                    echo "- Uploading factory test firmware..."
                    /usr/bin/avrdude -uV -c arduino -p ATMEGA328P -P /dev//dev/serial/by-id/XXXUARTPPROGXXXXX -b115200 -Uflash:w:/home/pi/factory-test/EmonTH_FactoryTest.ino.hex:i -l /home/pi/factory-test/avrdude.log
                    check=$(grep -e "bytes of flash verified" /home/pi/factory-test/avrdude.log)
                    if [ ! "$check" ] ; then
                        echo "- Firmware upload: **FAIL**"
                    else
                        echo "- Firmware upload: PASS"
                        echo "- Running function test..."
                        python3 /home/pi/factory-test/test-emonth.py
                    fi
                else
                    echo "- UART Programmer: MISSING"
                fi
            else
                echo "- UART Programmer: MISSING"
            fi
        fi
    else 
        echo "- ISP Programmer: MISSING"
    fi
else
    echo "- ISP Programmer: MISSING"
fi
echo "End"
