#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as font
import subprocess
import threading
from tkinter import messagebox
import time

window = tk.Tk()
window.title('OpenEnergyMonitor Factory Test')
window.attributes("-fullscreen", True)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
screen_resolution = str(screen_width)+'x'+str(int(screen_height))
window.geometry(screen_resolution)




class WritableStringVar(tk.StringVar):
    def write(self, added_text):
        new_text = self.get() + added_text
        self.set(new_text)

    def clear(self):
        self.set("")

class CmdThread (threading.Thread):
   def __init__(self, command, textvar):
        threading.Thread.__init__(self)
        self.command = command
        self.textvar = textvar

   def run(self):
        textvar.clear()
        time.sleep(0.5)
        proc = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        while not proc.poll():
            data = proc.stdout.readline().decode()
            if data:
                print(data, file=textvar, end='')
            else:
                break

def emontxv4():
	thread = CmdThread(["/home/pi/factory-test/./upload_and_test_EmonTx4.sh"], textvar)
	thread.start()
	#messagebox.showinfo( "Test", "This is a test notification")

def emonpi2():
	thread = CmdThread(["/home/pi/factory-test/./upload_and_test_EmonPi2.sh"], textvar)
	thread.start()
	#messagebox.showinfo( "Test", "This is a test notification")
	
def emonth():	
	thread = CmdThread(["/home/pi/factory-test/./upload_and_test_EmonTH.sh"], textvar)
	thread.start()

	
def shutdown():
	subprocess.Popen(['sudo','shutdown','-h','now'])

def restart():
	subprocess.Popen(['sudo','shutdown','-r','now'])
	
def quit():
	window.destroy()


shutdown = tk.Button(window, text ="Shutdown", command = shutdown)
shutdown.pack(side=tk.RIGHT, anchor=tk.NE)

restart = tk.Button(window, text ="Restart", command = restart)
restart.pack(side=tk.RIGHT, anchor=tk.NE)

quit = tk.Button(window, text ="Quit", command = quit)
quit.pack(side=tk.RIGHT, anchor=tk.NE)

label1 = tk.Label(window, text='1a: Tx/Pi: Connect USB-C, RJ11, Antenna & UDPI Probe')
label1.config(font=("Ariel", 13))
label1.pack(side=tk.TOP, anchor=tk.W)

label2 = tk.Label(window, text='1b: emonTH: Connect ISP & UART programmers')
label2.config(font=("Ariel", 13))
label2.pack(side=tk.TOP, anchor=tk.W)

label3 = tk.Label(window, text='2: Tap button to start')
label3.config(font=("Ariel", 13))
label3.pack(side=tk.TOP, anchor=tk.W)

myFont = font.Font(weight="bold", size=20)

B1 = tk.Button(window, text ="emonTx V4", command = emontxv4, bg='#0052cc', fg='#ffffff')
B1['font'] = myFont
B1.pack(side=tk.LEFT, anchor=tk.NW)
# B1.pack(anchor=tk.NW)

B2 = tk.Button(window, text ="emonPi2", command = emonpi2, bg='#52CC00', fg='#ffffff')
B2['font'] = myFont
B2.pack(side=tk.LEFT, anchor=tk.NW)
# B2.pack(anchor=tk.NW)

B3 = tk.Button(window, text ="emonTH", command = emonth, bg='#CC0052', fg='#ffffff')
B3['font'] = myFont
B3.pack(side=tk.LEFT, anchor=tk.NW)
# B3.pack(anchor=tk.NW)


textvar = WritableStringVar(window)
# label=tk.Label(window, textvariable=textvar, justify=tk.LEFT)
box=tk.Label(window, textvariable=textvar)
box.config(font=("Ariel", 12))
box.pack(side=tk.BOTTOM, anchor=tk.W)
# box.pack()


window.mainloop()
