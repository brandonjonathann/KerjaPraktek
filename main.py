import tkinter as tk
import ttkbootstrap as ttk
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

def screen_center(self: tk.Tk, width, height):
    x = int((self.winfo_screenwidth() - width) / 2)
    y = int((self.winfo_screenheight() - height) / 2)
    return f'{width}x{height}+{x}+{y}'

class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Attributes
        self.title('CV. Missouri Farm Rancakalong')
        self.iconbitmap('icon.ico')
        self.starting_width = int(0.75 * self.winfo_screenwidth())
        self.starting_height = int(0.75 * self.winfo_screenheight())
        self.minsize(self.starting_width, self.starting_height)
        self.geometry(screen_center(self, self.starting_width, self.starting_height))

        # Grid
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 8, uniform = 'a')
        self.columnconfigure(2, weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1, uniform = 'a')
        self.rowconfigure(1, weight = 9, uniform = 'a')

        # Widgets
        Main_Menu_Buttons(self, 'Import Data', lambda: import_data_function(self), 2, 0)

        # Mainloop
        self.mainloop()

class Main_Menu_Buttons(ttk.Button):
    def __init__(self, parent, text, command, column, row):
        super().__init__(parent, text = text, command = command)
        self.grid(column = column, row = row, sticky = 'nsew', padx = 10, pady = 10)

class No_Port_Notification(ttk.Toplevel):
    def __init__(self, parent: Main_Window):
        super().__init__(parent)
        self.geometry(screen_center(parent, 250, 100))
        self.overrideredirect(True)

        ttk.Label(self, text = 'No port is currently available.').pack(padx = 10, pady = 10)
        ttk.Button(self, text = 'OK', command = self.destroy).pack(padx = 10, pady = 10)
        self.grab_set()
        parent.wait_window(self)
        self.grab_release()

class Import_Menu(ttk.Toplevel):
    def __init__(self, parent: Main_Window, port, waiting_for_connection_variable, new_files):
        super().__init__(parent)
        self.geometry(screen_center(parent, 250, 100))
        self.overrideredirect(True)
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
        
        ttk.Label(self, text = f'IP Address: {HOST}').grid(column = 0, row = 0)
        ttk.Label(self, text = f'Port: {port}').grid(column = 0, row = 1)
        ttk.Label(self, textvariable = waiting_for_connection_variable).grid(column = 0, row = 2)
        ttk.Button(self, text = 'End Import', command = lambda: end_server(port)).grid(column = 0, row = 3)

        server_thread = threading.Thread(target = lambda: start_server(port, new_files))
        server_thread.start()
        connection_thread = threading.Thread(target = lambda: change_connecting_label_text(server_thread, waiting_for_connection_variable, new_files, self))
        connection_thread.start()

        self.grab_set()
        parent.wait_window(self)
        self.grab_release()

def import_data_function(parent):
    port = find_open_port()
    if port == None:
        No_Port_Notification(parent)
    else:
        new_files = []
        waiting_for_connection_variable = ttk.StringVar()
        Import_Menu(parent, port, waiting_for_connection_variable, new_files)

def change_connecting_label_text(server_thread: threading.Thread, waiting_for_connection_variable: ttk.StringVar, new_files, menu: Import_Menu):
    time_sleeping = 0
    while server_thread.is_alive():
        if time_sleeping % 3 == 0:
            waiting_for_connection_variable.set('Waiting for connection, please wait.')
        elif time_sleeping % 3 == 1:
            waiting_for_connection_variable.set('Waiting for connection, please wait..')
        else:
            waiting_for_connection_variable.set('Waiting for connection, please wait...')
        time.sleep(1)
        time_sleeping += 1
    menu.destroy()

    for file in new_files:
        if os.path.exists(file):
            if file.endswith('.csv'):
                append_data_to_database(file)
                os.remove(file)

Main_Window()

# # Functions

# def import_function():

#     menu.place_forget()
#     port = find_open_port()

#     if port == None:

#         no_port_frame = ttk.Frame(window)
#         no_port_label = ttk.Label(no_port_frame, text = 'No port is available.')
#         no_port_button = ttk.Button(no_port_frame, text = 'OK', command = no_port_frame.place_forget)

#         no_port_frame.place(relx = 0.5, rely = 0.5, anchor = 'center')
#         no_port_label.pack(fill = 'both')
#         no_port_button.pack(fill = 'both')

#     else:

#         # Widgets
#         import_frame = ttk.Frame(window)
#         import_frame.columnconfigure(0, weight = 1, uniform = 'a')
#         import_frame.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
#         import_frame.grid(column = 2, row = 1, sticky = 'nsew')

#         host_label = ttk.Label(import_frame, text = f'IP Address: {HOST}')
#         host_label.grid(column = 0, row = 0)

#         port_label = ttk.Label(import_frame, text = f'Port being used: Port {port}.')
#         port_label.grid(column = 0, row = 1)
        
#         waiting_for_connection_variable = tk.StringVar()
#         connecting_label = ttk.Label(import_frame, textvariable = waiting_for_connection_variable)
#         connecting_label.grid(column = 0, row = 2)

#         import_end_button = ttk.Button(import_frame, text = f'End Import', command = lambda : end_server(port))
#         import_end_button.grid(column = 0, row = 3, sticky = 'nsew', padx = 10, pady = 10)

#         # Import Process
#         new_files = []

#         server_thread = threading.Thread(target = lambda: start_server(port, new_files))
#         server_thread.start()

#         def change_connecting_label_text():
#             time_sleeping = 0
#             while server_thread.is_alive():
#                 if time_sleeping % 3 == 0:
#                     waiting_for_connection_variable.set('Waiting for connection, please wait.')
#                 elif time_sleeping % 3 == 1:
#                     waiting_for_connection_variable.set('Waiting for connection, please wait..')
#                 else:
#                     waiting_for_connection_variable.set('Waiting for connection, please wait...')
#                 time.sleep(1)
#                 time_sleeping += 1
#             import_frame.grid_forget()

#             for file in new_files:
#                 if os.path.exists(file):
#                     if file.endswith('.csv'):
#                         append_data_to_database(file)
#                         os.remove(file)

#         connecting_label_thread = threading.Thread(target = change_connecting_label_text)
#         connecting_label_thread.start()

# def sort_kandang(list_of_kandang_number: list[str]):
#     temporary_list = []
#     for kandang in list_of_kandang_number:
#         temporary_list.append(int(kandang.split('R')[1]))

#     temporary_list = sorted(temporary_list)
#     for index in range(len(temporary_list)):
#         temporary_list[index] = f'R{temporary_list[index]}'
    
#     return temporary_list

# class Kandang:
#     def __init__(self, number, parent):
#         self.parent = parent
#         self.number = number
#         self.checkvar = ttk.IntVar(value = 0)
#         ttk.Checkbutton(self.parent, text = self.number, variable = self.checkvar, onvalue = 1, offvalue = 0, command = lambda: print(self.checkvar.get())).pack(fill = 'x')

# # Variables
# list_of_kandang_number = [str]
# list_of_kandang = [Kandang]

# def menu_kandang():
    
#     global list_of_kandang_number
#     global list_of_kandang

#     list_of_kandang_number = sort_kandang(os.listdir(DATABASE))

#     menu.place_forget()

#     menu_kandang_frame = ttk.Frame(window)
#     menu_kandang_frame.grid(column = 1, row = 1, sticky = 'nsew')

#     kandang_list_frame = ttk.Frame(menu_kandang_frame)
#     kandang_list_frame.grid(column = 1, row = 1, sticky = 'nsew')

#     for kandang_number in list_of_kandang_number:
#         list_of_kandang.append(Kandang(kandang_number, kandang_list_frame))
    
# # Widgets
# menu_button1 = ttk.Button(window, text = '=', command = open_menu)
# menu_button1.grid(column = 0, row = 0, sticky = 'nsew')

# menu = ttk.Frame(window)
# menu.columnconfigure(0, weight = 1, uniform = 'a')
# menu.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
# menu.rowconfigure(4, weight = 6, uniform = 'a')

# menu_button2 = ttk.Button(menu, text = '=', command = menu.place_forget)
# today_data = ttk.Button(menu, text = "Today's Data")

# select_kandang = ttk.Button(menu, text = "Select Kandang", command = menu_kandang)
# import_file = ttk.Button(menu, text = "Import File", command = import_function)

# welcome_label = ttk.Label(window, text = 'Welcome Back')
# welcome_label.grid(column = 1, row = 0, columnspan = 2, sticky = 'nsew', padx = 10)

