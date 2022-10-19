#!/usr/bin/bash

python3 -u tools/prog.py -t uart -u /dev/udpi -b 230400 -d avr128db48 --fuses 0:0x00 1:0x00 2:0x00 5:0b11001000 6:0b00001100 7:0x00 8:0x01 -foptiboot_dx128_ser3.hex -a write -v

/usr/bin/avrdude -Cavrdude.conf -v -pavr128db48 -carduino -D -P/dev/emontx -b115200 -Uflash:w:EmonTxV4CM_FactoryTest.ino.hex:i 

python3 test.py
