
if [ -L /dev/udpi ] ; then
   if [ -e /dev/udpi ] ; then
       python3 -u /home/pi/factory-test/tools/prog.py -t uart -u /dev/udpi -b 230400 -d avr128db48 --fuses 0:0x00 1:0x00 2:0x00 5:0b11001000 6:0b00001100 7:0x00 8:0x01 -f/home/pi/factory-test/optiboot_dx128_ser3.hex -a write -v > udpi.log
       grep -e "Verify successful. Data in flash matches data in specified hex-file" /home/pi/factory-test/udpi.log
   fi
fi
