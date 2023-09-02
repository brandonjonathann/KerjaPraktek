import tkinter as tk
import ttkbootstrap as ttk
import time
import threading

window = tk.Tk()

labeltext = ttk.StringVar(value = 'waiting')
label = ttk.Label(window, textvariable = labeltext)
label.pack()

def change_variable():
    global labeltext

    for i in range(5):
        labeltext.set(i)
        time.sleep(1)

thread = threading.Thread(target = change_variable)

button = ttk.Button(window, text = 'change variable', command = thread.start)
button.pack()

window.mainloop()