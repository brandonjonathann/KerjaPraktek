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
from modules.kandang import *

list_of_kandang = list_kandang()

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
        self.import_button = Main_Menu_Buttons(self, 'Import Data', lambda: import_data_function(self), 2, 0)
        self.list_kandang = Display_List_Kandang(self, 0, 1)

        # display_kandang()

        # Mainloop
        self.mainloop()

class Main_Menu_Buttons(ttk.Button):
    def __init__(self, parent, text, command, column, row):
        super().__init__(parent, text = text, command = command)
        self.grid(column = column, row = row, sticky = 'nsew', padx = 5, pady = 5)

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
    def __init__(self, parent: Main_Window, port: int, waiting_for_connection_variable: ttk.StringVar, new_files):
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

class Display_List_Kandang_1(ttk.Canvas):
    def __init__(self, parent: Main_Window, column, row):
        super().__init__(parent)
        self.grid(column = column, row = row, sticky = 'nsew')
        self.jumlah_kandang = len(list_of_kandang)
        self.list_height = self.jumlah_kandang * 50
        self.configure(scrollregion = (0, 0, self.winfo_width(), self.list_height))

        self.frame = ttk.Frame(self)

        for index, kandang in enumerate(list_of_kandang):
            print(f'{index} + {kandang}')
            kandang_button_list.append(ttk.Button(self.frame, text = kandang))
            kandang_button_list[index].pack(expand = True, fill = 'both', padx = 1, pady = 1)

        self.scrollbar = ttk.Canvas(parent)
        self.scrollbar.grid(column = column + 1, row = row, sticky = 'nsew', padx = 1, pady = 1)
        self.scrollbar.bind('<MouseWheel>', lambda event: self.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size)            

    def update_size(self, event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.scrollbar.bind('<MouseWheel>', lambda event: self.yview_scroll(-int(event.delta / 60), "units"))
        else:
            height = self.list_height
            self.unbind_all('<MouseWheel>')

        self.create_window((0, 0), window = self.frame, anchor = 'nw', width = self.winfo_width(), height = height)

class Display_List_Kandang(ttk.Frame):
    def __init__(self, parent: Main_Window, column, row):
        super().__init__(parent)
        self.treeview = ttk.Treeview(self, columns = ('kandang'), show = 'headings')
        self.treeview.pack(expand = True, fill = 'both')
        self.treeview.heading('kandang', text = 'Kandang')
        self.treeview.column('kandang', width = self.winfo_width())
        for kandang in list_of_kandang:
            self.treeview.insert(parent = '', index = 'end', values = kandang)
        self.grid(column = column, row = row, sticky = 'nsew')

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

# def display_kandang():
#     kandang = list_kandang()
#     pass

Main_Window()