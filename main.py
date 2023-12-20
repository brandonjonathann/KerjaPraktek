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

list_kandang_cache = []
data_kandang_cache = []

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
        self.columnconfigure(0, weight = 1, uniform = 'a', minsize = 100)
        self.columnconfigure(1, weight = 8, uniform = 'a')
        self.columnconfigure(2, weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1, uniform = 'a')
        self.rowconfigure(1, weight = 9, uniform = 'a')

        # Widgets
        self.import_button = Main_Menu_Buttons(self, 'Import Data', lambda: import_data_function(self), 2, 0)
        self.list_kandang = Display_List_Kandang(self, 0, 1)
        self.radiobuttons = Radiobuttons(self, 0, 0)
        self.checkbuttons = Checkbuttons(self, 1, 0)

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

class Display_List_Kandang(ttk.Frame):
    def __init__(self, parent: Main_Window, column, row):
        super().__init__(parent)
        self.treeview = ttk.Treeview(self, columns = ('kandang'), show = 'headings', selectmode = 'browse')
        self.treeview.pack(expand = True, fill = 'both')
        self.treeview.heading('kandang', text = 'Kandang')
        self.treeview.column('kandang', width = self.winfo_width())
        for kandang in list_of_kandang:
            self.treeview.insert(parent = '', index = 'end', values = kandang)
        self.grid(column = column, row = row, sticky = 'nsew')
        self.selected_kandang = None
        self.data_kandang = None

        def item_select(_):
            if self.data_kandang != None:
                self.data_kandang.destroy()

            self.selected_kandang = self.treeview.item(self.treeview.selection())['values'][0]

            if self.selected_kandang not in list_kandang_cache:
                list_kandang_cache.append(self.selected_kandang)
                data_kandang_cache.append(data_kandang(self.selected_kandang))

            index = list_kandang_cache.index(self.selected_kandang)
            data = data_kandang_cache[index]

            self.data_kandang = Display_Data_Kandang(parent, data)
            self.data_kandang.grid(column = column + 1, columnspan = 2, row = row, sticky = 'nsw')

        self.treeview.bind('<<TreeviewSelect>>', item_select)

class Checkbuttons(ttk.Frame):
    def __init__(self, parent: Main_Window, column, row):
        super().__init__(parent)
        self.columnconfigure((0, 1, 2, 3, 4, 5), uniform = 'a', weight = 1)
        self.rowconfigure((0, 1), uniform = 'a', weight = 1)

        self.var_betina = ttk.BooleanVar(value = False)
        self.but_betina = ttk.Checkbutton(self, text = '♀', variable = self.var_betina)
        self.but_betina.grid(column = 0, row = 0, sticky = 'w')
        self.var_jantan = ttk.BooleanVar(value = False)
        self.but_jantan = ttk.Checkbutton(self, text = '♂', variable = self.var_jantan)
        self.but_jantan.grid(column = 1, row = 0, sticky = 'w')
        self.var_betina_B = ttk.BooleanVar(value = False)
        self.but_betina_B = ttk.Checkbutton(self, text = '♀ B', variable = self.var_betina_B)
        self.but_betina_B.grid(column = 2, row = 0, sticky = 'w')
        self.var_jantan_B = ttk.BooleanVar(value = False)
        self.but_jantan_B = ttk.Checkbutton(self, text = '♂ B', variable = self.var_jantan_B)
        self.but_jantan_B.grid(column = 3, row = 0, sticky = 'w')
        self.var_SE = ttk.BooleanVar(value = False)
        self.but_SE = ttk.Checkbutton(self, text = 'SE', variable = self.var_SE)
        self.but_SE.grid(column = 4, row = 0, sticky = 'w')
        self.reset = ttk.Button(self, text = 'Reset')
        self.reset.grid(column = 5, row = 0, sticky = 'w')
        
        self.var_telur = ttk.BooleanVar(value = False)
        self.but_telur = ttk.Checkbutton(self, text = 'Produksi Telur', variable = self.var_telur)
        self.but_telur.grid(column = 0, row = 1, sticky = 'w')
        self.var_mati = ttk.BooleanVar(value = False)
        self.but_mati = ttk.Checkbutton(self, text = 'Kematian', variable = self.var_mati)
        self.but_mati.grid(column = 1, row = 1, sticky = 'w')
        self.var_jumlah = ttk.BooleanVar(value = False)
        self.but_jumlah = ttk.Checkbutton(self, text = 'Jumlah Ayam', variable = self.var_jumlah)
        self.but_jumlah.grid(column = 2, row = 1, sticky = 'w')
        self.var_eceran = ttk.BooleanVar(value = False)
        self.but_eceran = ttk.Checkbutton(self, text = 'Eceran Pakan', variable = self.var_eceran)
        self.but_eceran.grid(column = 3, row = 1, sticky = 'w')
        self.var_pakan = ttk.BooleanVar(value = False)
        self.but_pakan = ttk.Checkbutton(self, text = 'Jumlah Pakan', variable = self.var_pakan)
        self.but_pakan.grid(column = 4, row = 1, sticky = 'w')
        self.var_keterangan = ttk.BooleanVar(value = False)
        self.but_keterangan = ttk.Checkbutton(self, text = 'Keterangan', variable = self.var_keterangan)
        self.but_keterangan.grid(column = 5, row = 1, sticky = 'w')

        def reset():
            self.var_betina.set(False)
            self.var_jantan.set(False)
            self.var_betina_B.set(False)
            self.var_jantan_B.set(False)
            self.var_SE.set(False)
            self.var_telur.set(False)
            self.var_mati.set(False)
            self.var_jumlah.set(False)
            self.var_eceran.set(False)
            self.var_pakan.set(False)
            self.var_keterangan.set(False)
        self.reset.configure(command = reset)

        self.grid(column = column, row = row, sticky = 'nsew')

class Radiobuttons(ttk.Frame):
    def __init__(self, parent: Main_Window, column, row):
        super().__init__(parent)
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.rowconfigure((0, 1), weight = 1, uniform = 'a')

        self.radio_var = ttk.BooleanVar(value = True)
        self.radio1 = ttk.Radiobutton(self, text = 'Table View', variable = self.radio_var, value = True)
        self.radio1.grid(column = 0, row = 0, sticky = 'w', padx = 5)
        self.radio2 = ttk.Radiobutton(self, text = 'Graph View', variable = self.radio_var, value = False)
        self.radio2.grid(column = 0, row = 1, sticky = 'w', padx = 5)

        self.grid(column = column, row = row, sticky = 'nsew')

class Display_Data_Kandang(ttk.Frame):
    def __init__(self, parent: Main_Window, dataset):
        super().__init__(parent)

        columns = ['tanggal', 'hari']        
        text = ['Tanggal', 'Hari']
        entry = [0, 1]

        if parent.checkbuttons.var_telur.get() == True:
            columns.append('telur')
            text.append('Telur')
            entry.append(4)
        if parent.checkbuttons.var_betina.get() == True:
            if parent.checkbuttons.var_mati.get() == True:
                columns.append('mati_betina')
                text.append('Kematian ♀')
                entry.append(6)
            if parent.checkbuttons.var_jumlah.get() == True:
                columns.append('jumlah_betina')
                text.append('Jumlah ♀')
                entry.append(21)
            if parent.checkbuttons.var_eceran.get() == True:
                columns.append('eceran_betina')
                text.append('Eceran ♀ (kg)')
                entry.append(11)
            if parent.checkbuttons.var_pakan.get() == True:
                columns.append('pakan_betina')
                text.append('Pakan ♀ (g)')
                entry.append(16)
        if parent.checkbuttons.var_jantan.get() == True:
            if parent.checkbuttons.var_mati.get() == True:
                columns.append('mati_jantan')
                text.append('Kematian ♂')
                entry.append(7)
            if parent.checkbuttons.var_jumlah.get() == True:
                columns.append('jumlah_jantan')
                text.append('Jumlah ♂')
                entry.append(22)
            if parent.checkbuttons.var_eceran.get() == True:
                columns.append('eceran_jantan')
                text.append('Eceran ♂')
                entry.append(12)
            if parent.checkbuttons.var_pakan.get() == True:
                columns.append('pakan_jantan')
                text.append('Pakan ♂')
                entry.append(17)
        if parent.checkbuttons.var_betina_B.get() == True:
            if parent.checkbuttons.var_mati.get() == True:
                columns.append('mati_betina_B')
                text.append('Kematian ♀ B')
                entry.append(8)
            if parent.checkbuttons.var_jumlah.get() == True:
                columns.append('jumlah_betina_B')
                text.append('Jumlah ♀ B')
                entry.append(23)
            if parent.checkbuttons.var_eceran.get() == True:
                columns.append('eceran_betina_B')
                text.append('Eceran ♀ B')
                entry.append(13)
            if parent.checkbuttons.var_pakan.get() == True:
                columns.append('pakan_betina_B')
                text.append('Pakan ♀ B')
                entry.append(18)
        if parent.checkbuttons.var_jantan_B.get() == True:
            if parent.checkbuttons.var_mati.get() == True:
                columns.append('mati_jantan_B')
                text.append('Kematian ♂ B')
                entry.append(9)
            if parent.checkbuttons.var_jumlah.get() == True:
                columns.append('jumlah_jantan_B')
                text.append('Jumlah ♂ B')
                entry.append(24)
            if parent.checkbuttons.var_eceran.get() == True:
                columns.append('eceran_jantan_B')
                text.append('Eceran ♂ B')
                entry.append(14)
            if parent.checkbuttons.var_pakan.get() == True:
                columns.append('pakan_jantan_B')
                text.append('Pakan ♂ B')
                entry.append(19)
        if parent.checkbuttons.var_SE.get() == True:
            if parent.checkbuttons.var_mati.get() == True:
                columns.append('mati_SE')
                text.append('Kematian SE')
                entry.append(10)
            if parent.checkbuttons.var_jumlah.get() == True:
                columns.append('jumlah_SE')
                text.append('Jumlah SE')
                entry.append(25)
            if parent.checkbuttons.var_eceran.get() == True:
                columns.append('eceran_SE')
                text.append('Eceran SE')
                entry.append(15)
            if parent.checkbuttons.var_pakan.get() == True:
                columns.append('pakan_SE')
                text.append('Pakan SE')
                entry.append(20)
        if parent.checkbuttons.var_keterangan.get() == True:
            columns.append('keterangan')
            text.append('Keterangan')
            entry.append(26)

        self.treeview = ttk.Treeview(self, columns = tuple(columns), show = 'headings', height = 5)

        for i in range (len(columns)):
            self.treeview.heading(columns[i], text = text[i])
            self.treeview.column(columns[i], width = 100)

        self.treeview.pack(fill = 'both', expand = True)

        self.scrollbar = ttk.Scrollbar(self, orient = 'horizontal', command = self.treeview.xview)
        self.treeview.configure(xscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(fill = 'x')
        
        for data in dataset:
            data_entry = []
            for index in entry:
                data_entry.append(data[index])
            self.treeview.insert(parent = '', index = 'end', values = data_entry)

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