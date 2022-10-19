#!/usr/bin/env python3

import tkinter as tk
import subprocess
import threading
from tkinter import messagebox

window = tk.Tk()
window.title('OpenEnergyMonitor Factory Test')
#window.attributes("-fullscreen", True) 
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
#window.geometry('300x200')


class CmdThread (threading.Thread):
   def __init__(self, command, textvar):
        threading.Thread.__init__(self)
        self.command = command
        self.textvar = textvar

   def run(self):
        proc = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        while not proc.poll():
            data = proc.stdout.readline()
            if data:
                print(data)
                self.textvar.set(data)
            else:
                break

def emontxv4():	
	thread = CmdThread(['./upload_and_test.sh'], text)
	thread.start()
	#messagebox.showinfo( "Test", "This is a test notification")


label = tk.Label(window, text='Select hardware to start upload:')
label.pack(ipadx=10, ipady=10)

B = tk.Button(window, text ="emonTx V4", command = emontxv4)
B.pack()

text = tk.StringVar()
label = tk.Label(textvariable=text)
label.pack(ipadx=10, ipady=10)



window.mainloop()
