#!/usr/bin/bash

if [ -L /dev/udpi ] ; then
    if [ -e /dev/udpi ] ; then
        echo "- Burning bootloader via UDPI..."
        python3 -u /home/pi/factory-test/tools/prog.py -t uart -u /dev/udpi -b 230400 -d avr128db48 --fuses 0:0x00 1:0x00 2:0x00 5:0b11001000 6:0b00001100 7:0x00 8:0x01 -f/home/pi/factory-test/bootloaders/optiboot_dx128_ser3.hex -a write -v > /home/pi/factory-test/udpi.log
        
        check=$(grep -e "Verify successful" /home/pi/factory-test/udpi.log)
        if [ ! "$check" ] ; then
            echo "- Bootloader upload: **FAIL** ..is USB-C connected? orientation?"
        else
            echo "- Bootloader upload: PASS (probe can be released)" 
            
            if [ -L /dev/emontx ] ; then
                if [ -e /dev/emontx ] ; then
                    echo "- Uploading factoavrdude -p atmega328p -c avrispmkII -P usb -e -U efuse:w:0x05:m -U hfuse:w:0xD6:m -U lfuse:w:0xFF:m -U flash:w:' + bootloader_path + ':i -Ulock:w:0x0f:mry test firmware..."
                    /usr/bin/avrdude -C/home/pi/factory-test/avrdude.conf -v -pavr128db48 -carduino -D -P/dev/emontx -b115200 -Uflash:w:/home/pi/factory-test/testfw/EmonPi2_FactoryTest.ino.hex:i -l /home/pi/factory-test/avrdude.log
                    check=$(grep -e "bytes of flash verified" /home/pi/factory-test/avrdude.log)
                    if [ ! "$check" ] ; then
                        echo "- Firmware upload: **FAIL**"
                    else
                        echo "- Firmware upload: PASS"
                        echo "- Running function test..."
                        python3 /home/pi/factory-test/testscript/test.py
                    fi
                else
                    echo "- USB Link: MISSING"
                fi
            else
                echo "- USB Link: MISSING"
            fi
        fi
    else 
        echo "- UDPI Programmer: MISSING"
    fi
else
    echo "- UDPI Programmer: MISSING"
fi
echo "End"
