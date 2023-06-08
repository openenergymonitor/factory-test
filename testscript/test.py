#!/usr/bin/python3
# 1
# Read from serial with data coming from RFM12PI with RFM12_Demo sketch 
# All Emoncms code is released under the GNU Affero General Public License.

import serial, sys, string, time, struct

import spidev

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from RFM69 import Radio

# Set this to the serial port of your emontx and baud rate, 9600 is standard emontx baud rate
usb = serial.Serial('/dev/emontx', 115200)    

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
  
    if "\r\n" in usb_str:
        usb_str = usb_str.rstrip()
        # print(usb_str)
        
        inputs = {}
        
        if usb_str[0:3]=="MSG":
            pairs = usb_str.split(",")
            for pair in pairs:
                keyval = pair.split(":")
                inputs[keyval[0]] = keyval[1]
        
        if 'MSG' in inputs and 'Vrms' in inputs:
        
            msg = int(inputs['MSG'])
            Vrms = float(inputs['Vrms'])
        
            if not msg in rx_msg_flag:
                rx_msg_flag[msg] = {'radio':0,'usb':Vrms}
            else:
                rx_msg_flag[msg]['usb'] = Vrms   
                
        if 'Vrms' in inputs:
            Vrms = float(inputs['Vrms'])   
            if Vrms>220 and Vrms<260:
                print("- VOLTAGE: PASS")
            else:
                print("- VOLTAGE: **FAIL** ("+str(Vrms)+") ..is RJ11/RJ45 connected?")

        for i in range(1,7):
            name = 'P'+str(i)
            if name in inputs:
                P = float(inputs[name])   
                if P>1900 and P<2200:
                    print("- CT CHANNEL "+str(i)+": PASS")
                else:
                    print("- CT CHANNEL "+str(i)+": **FAIL** ("+str(P)+")")

        if 'T1' in inputs:
            T1 = float(inputs['T1'])   
            if T1>0 and T1<50:
                print("- TEMPERATURE: PASS")
    
        usb_str = ""
  
  packet = radio.get_packet()
  if packet:
    # print(packet.sender)
    # print(len(packet.data))
    if packet.sender==15 and len(packet.data)==28:
        unpacked = struct.unpack('LhhhhhhhhhhL',bytes(packet.data))
        # print (unpacked)
        msg = unpacked[0]
        Vrms = unpacked[1]*0.01
            
        if not msg in rx_msg_flag:
            rx_msg_flag[msg] = {'radio':Vrms,'usb':0}
        else:
            rx_msg_flag[msg]['radio'] = Vrms
        
    for msg in rx_msg_flag:
        if rx_msg_flag[msg]['radio']==rx_msg_flag[msg]['usb']:
            print("- RADIO: PASS")
            sys.exit(0)
            
  if time.time() > timeout:
        break
  time.sleep(0.1)

print("TIMEOUT: **FAIL**") 
radio.__exit__()
