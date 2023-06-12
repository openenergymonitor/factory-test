#!/usr/bin/python3
# 1
# Read from serial with data coming from RFM12PI with RFM12_Demo sketch 
# All Emoncms code is released under the GNU Affero General Public License.

import serial, sys, string, time, struct

import spidev

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from RFM69 import Radio

# Set this to the serial port of UART programmer
usb = serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 115200)    

board = {'isHighPower': False, 'interruptPin': 22, 'resetPin': None, 'selPin':26, 'spiDevice': 0, 'encryptionKey':"89txbe4p8aik5kt3"}
radio = Radio(43, 5, 210, verbose=False, **board)

# print (radio.init_success)

radio.__enter__()

usb_str = ""
radio_str = ""

rx_msg_flag = {}

timeout = time.time() + 60   # 7s 

while 1:

  # Read from USB
  if (usb.in_waiting > 0):
    c = usb.read(usb.in_waiting).decode()
    usb_str = usb_str + c
   
    if '\n' in usb_str:
        usb_str = usb_str.rstrip()
        # print(usb_str)
        inputs = {}
        if usb_str[0:4]=="temp":
            #print(usb_str)
            pairs = usb_str.split(",")
            for pair in pairs:
                keyval = pair.split(":")

                inputs[keyval[0]] = keyval[1]
        
        if 'temp' in inputs and 'humidity' in inputs:
            print ("- SERIAL: temperature: " + str(inputs.get('temp')) + " C")
            print ("- SERIAL: humidity: " + str(inputs.get('humidity')) + " RH")
            # Check if temp and humidity are in the range 1-100 
            if int(float(inputs.get('temp'))) in range(1,100) and int(float(inputs.get('humidity'))) in range(1,100):
                print("SERIAL: PASS")
            else:
                print("SERIAL: **FAIL**")
        usb_str = ""
  
  packet = radio.get_packet()
  if packet:
    # print(packet.sender)
    # print(len(packet.data))
    if packet.sender==23 and len(packet.data)==12:
        unpacked = struct.unpack('hhhhL',bytes(packet.data))
        # print (unpacked)
        temperature = unpacked[0]
        humidity = unpacked[2]

        print("- RADIO: PASS")
        print ("- RADIO temperature: %0.1f C" % (temperature*0.1))
        print ("- RADIO humidity: %0.1f RH" % (humidity*0.1))
        # Check if temp and humidity are in the range 1-100 
        if not int(temperature) in range(10,1000): 
            print ("- Temperature value FAIL")
        if not int(humidity) in range(10,1000):
            print ("- Humidity value FAIL")
            
        sys.exit(0)
            
  if time.time() > timeout:
        break
  time.sleep(0.1)

print("TIMEOUT RADIO: **FAIL**") 
radio.__exit__()
