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
        proc = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        while not proc.poll():
            data = proc.stdout.readline()
            if data:
                print(data, file=textvar)
                #textvar.set(textvar.get()[:-1])
            else:
                break

def emontxv4():	
	thread = CmdThread(['./upload_and_test.sh'], textvar)
	#thread = CmdThread(['./test.sh'], textvar)
	thread.start()
	#messagebox.showinfo( "Test", "This is a test notification")


label = tk.Label(window, text='Select hardware to start upload:')
label.pack(ipadx=10, ipady=10)

B = tk.Button(window, text ="emonTx V4", command = emontxv4)
B.pack()


textvar = WritableStringVar(window)
label = tk.Label(window, textvariable=textvar)
label.pack(ipadx=10, ipady=10)





window.mainloop()
