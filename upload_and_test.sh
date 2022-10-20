#!/usr/bin/bash

if [ -L /dev/udpi ] ; then
    if [ -e /dev/udpi ] ; then
        echo "- Burning bootloader via UDPI"
        python3 -u tools/prog.py -t uart -u /dev/udpi -b 230400 -d avr128db48 --fuses 0:0x00 1:0x00 2:0x00 5:0b11001000 6:0b00001100 7:0x00 8:0x01 -foptiboot_dx128_ser3.hex -a write -v > udpi.log
        
        check=$(grep -e "Verify successful" udpi.log)
        if [ ! "$check" ] ; then
            echo "- Bootloader upload: FAIL"
        else
            echo "- Bootloader upload: PASS" 
            
            if [ -L /dev/emontx ] ; then
                if [ -e /dev/emontx ] ; then
                    echo "- Uploading EmonTx4 Factory Test Firmware"
                    /usr/bin/avrdude -Cavrdude.conf -v -pavr128db48 -carduino -D -P/dev/emontx -b115200 -Uflash:w:EmonTxV4CM_FactoryTest.ino.hex:i -l avrdude.log
                    check=$(grep -e "avrdude: 20022 bytes of flash verified" avrdude.log)
                    if [ ! "$check" ] ; then
                        echo "- Firmware upload: FAIL"
                    else
                        echo "- Firmware upload: PASS"
                        python3 test.py
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
