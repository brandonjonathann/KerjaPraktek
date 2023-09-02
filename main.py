import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
import pathlib
import sys
import threading
import time
import os

PATH = pathlib.Path().absolute()
DATABASE = f'{PATH}/database'
MODULES = f'{PATH}/modules'
sys.path.append(MODULES)

from modules.append_data import *
from modules.server import *
# from modules.client import *
# from modules.readcsv import *

# Starting the Window
window = tk.Tk()
window.title("CV. Missouri Farm Rancakalong")
window.iconbitmap('icon.ico')

# Screen Atrributes
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

# Setting Window Attribute
window_starting_height = int(0.75 * screen_height)
window_starting_width = int(1.25 * screen_height)
window.resizable(False, False)

# Start Window in the Middle of The Screen
left_starting_point = int((screen_width - window_starting_width) / 2)
top_starting_point = int((screen_height - window_starting_height) / 2 - 20) #20 for title bar
window.geometry(f"{window_starting_width}x{window_starting_height}+{left_starting_point}+{top_starting_point}")

# Grid
window.columnconfigure((0, 1), weight = 1, uniform = 'a')
window.columnconfigure(2, weight = 8, uniform = 'a')
window.rowconfigure(0, weight = 1, uniform = 'a')
window.rowconfigure(1, weight = 9, uniform = 'a')

# Functions
def open_menu():
    menu.place(x = 0, y = 0, relwidth = 0.3, relheight = 1)
    menu.lift()
    menu_button2.grid(column = 0, row = 0, sticky = 'nsew')
    today_data.grid(column = 0, row = 1, sticky = 'nsew')
    select_kandang.grid(column = 0, row = 2, sticky = 'nsew')
    import_file.grid(column = 0, row = 3, sticky = 'nsew')

def close_menu():
    menu.place_forget()

def import_function():

    close_menu()
    port = find_open_port()

    # if port == None:
    #     there is no open port, create a pop up
    # else:
    #     there is an open port, proceed

    # Widgets
    import_frame = ttk.Frame(window)
    import_frame.columnconfigure(0, weight = 1, uniform = 'a')
    import_frame.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
    import_frame.grid(column = 2, row = 1, sticky = 'nsew')

    host_label = ttk.Label(import_frame, text = f'IP Address: {get_host()}')
    host_label.grid(column = 0, row = 0)

    port_label = ttk.Label(import_frame, text = f'Port being used: Port {port}.')
    port_label.grid(column = 0, row = 1)
    
    connecting_label_text = tk.StringVar()
    connecting_label = ttk.Label(import_frame, textvariable = connecting_label_text)
    connecting_label.grid(column = 0, row = 2)

    import_end_button = ttk.Button(import_frame, text = f'End Import', command = lambda : end_server(port))
    import_end_button.grid(column = 0, row = 3, sticky = 'nsew', padx = 10, pady = 10)

    # Import Process
    new_files = []

    server_thread = threading.Thread(target = lambda: start_server(port, new_files))
    server_thread.start()

    def change_connecting_label_text():
        time_sleeping = 0
        while server_thread.is_alive():
            if time_sleeping % 3 == 0:
                connecting_label_text.set('Waiting for connection, please wait.')
            elif time_sleeping % 3 == 1:
                connecting_label_text.set('Waiting for connection, please wait..')
            else:
                connecting_label_text.set('Waiting for connection, please wait...')
            time.sleep(1)
            time_sleeping += 1
        print(f'Server has been closed.')
        import_frame.grid_forget()

        for file in new_files:
            if os.path.exists(file):
                if file.endswith('.csv'):
                    append_data_to_database(file)
                    os.remove(file)

    connecting_label_thread = threading.Thread(target = change_connecting_label_text)
    connecting_label_thread.start()

# Widgets
menu_button1 = ttk.Button(window, text = '=', command = open_menu)
menu_button1.grid(column = 0, row = 0, sticky = 'nsew')

menu = ttk.Frame(window)
menu.columnconfigure(0, weight = 1, uniform = 'a')
menu.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
menu.rowconfigure(4, weight = 6, uniform = 'a')

menu_button2 = ttk.Button(menu, text = '=', command = close_menu)
today_data = ttk.Button(menu, text = "Today's Data")
select_kandang = ttk.Button(menu, text = "Select Kandang")
import_file = ttk.Button(menu, text = "Import File", command = import_function)

welcome_label = ttk.Label(window, text = 'Welcome Back')
welcome_label.grid(column = 1, row = 0, columnspan = 2, sticky = 'nsew', padx = 10)



# main_tabs = ttk.Notebook(window)
# tab1 = ttk.Frame(main_tabs)
# tab2 = ttk.Frame(main_tabs)
# main_tabs.add(tab1, text = 'Tab 1')
# main_tabs.add(tab2, text = 'Tab 2')

# main_tabs.grid(row = 1, column = 0, columnspan = 2, sticky = 'nwes')

# welcome = ttk.Label(window, text = "Welcome Back")
# welcome.grid(row = 0, column = 0)

# today_insights = ttk.Label(window, text = "Today's Insights")
# today_insights.pack()

# import_button = ttk.Button(window, text = "Import", command = import_function)
# import_button.pack()

# show_insights = ttk.Label(window, text = "Checkbuttons")
# # show_insights.pack()

# def kandang_function():
#     files = os.listdir(DATABASE)
#     print(files)

# kandang_button = ttk.Button(window, text = "Kandang", command = kandang_function)
# kandang_button.pack()

window.mainloop()