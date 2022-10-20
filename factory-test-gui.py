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
#w, h = window.winfo_screenwidth(), window.winfo_screenheight()
#window.geometry("%dx%d+0+0" % (w, h))
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
	thread = CmdThread(['./upload_and_test.sh'], textvar)
	#thread = CmdThread(['./test.sh'], textvar)
	thread.start()
	#messagebox.showinfo( "Test", "This is a test notification")

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

label = tk.Label(window, text='Touch button below to start:')
label.pack(side=tk.TOP, anchor=tk.W)

myFont = font.Font(weight="bold", size=40)
B = tk.Button(window, text ="emonTx V4", command = emontxv4, bg='#0052cc', fg='#ffffff')
B['font'] = myFont
B.pack(side=tk.TOP, anchor=tk.W)


textvar = WritableStringVar(window)
label = tk.Label(window, textvariable=textvar)
label.pack(side=tk.TOP, anchor=tk.W)

window.mainloop()
