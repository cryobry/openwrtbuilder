#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas
import gzip
import urllib.request


class Main(tk.Frame):
    """This module generates information for the tkinter gui"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Get Table of Hardware (toh) from openwrt.org and save to a pandas df
        self.toh_df = self.get_toh_df()

        # Target menu
        self.target = tk.StringVar()
        self.targets, self.target_menu = self.gen_target_menu()
        self.target.set(self.targets[0])

        # Subtarget menu
        self.subtarget = tk.StringVar()
        self.subtargets, self.subtarget_menu = self.gen_subtarget_menu()
        self.subtarget.set(self.subtargets[0])
        self.target.trace("w", lambda var_name, var_index, operation: self.gen_subtarget_menu(regen=True))

        # Backup file
        self.backup_file = tk.StringVar()
        self.backup_file_entry = ttk.Entry(self, textvariable=self.backup_file)
        self.backup_file_button = ttk.Button(self, text="Select backup file", command=self.open_sysbackup)

        # Device Info
        self.device_info = tk.StringVar()
        

        # Layout
        self.target_menu.grid(row=0, column=0, sticky=(tk.W + tk.E))
        self.subtarget_menu.grid(row=0, column=1, sticky=(tk.W + tk.E))
        self.backup_file_entry.grid(row=1, column=1, sticky=(tk.W + tk.E))
        self.backup_file_button.grid(row=1, column=0, sticky=(tk.W))
        self.columnconfigure(1, weight=1)

    
    def get_toh_df(self):
        toh_gz_handle = urllib.request.urlopen("https://openwrt.org/_media/toh_dump_tab_separated.gz")
        toh_handle = gzip.open(toh_gz_handle)
        toh_df = pandas.read_csv(toh_handle, sep="\t", encoding = "ISO-8859-1")
        toh_df = toh_df[(toh_df.target.notnull()) & 
                             (toh_df.subtarget.notnull()) &
                             (toh_df.target != '¿') &
                             (toh_df.subtarget != '¿')]
        return toh_df
        

    def gen_target_menu(self, *args, **kwargs):
        targets = sorted(set(self.toh_df.target.tolist()))
        target_menu = ttk.OptionMenu(self, self.target, targets[0], *targets)
        return targets, target_menu


    def gen_subtarget_menu(self, regen=False, *args, **kwargs):
        subtargets_df = self.toh_df[self.toh_df.target == self.target.get()]
        subtargets = sorted(set(subtargets_df.subtarget.tolist()))
        if regen is False:
            subtarget_menu = ttk.OptionMenu(self, self.subtarget, subtargets[0], *subtargets)
            return subtargets, subtarget_menu
        else: # Regen
            self.subtarget_menu["menu"].delete(0, "end")
            for subtarget in subtargets:
                self.subtarget_menu["menu"].add_command(label=subtarget, command=lambda value=subtarget: self.subtarget.set(subtarget))
            self.subtarget.set(subtargets[0])


    def open_sysbackup(self):
        file = filedialog.askopenfile(mode ='r', title="Select Backup File", filetypes=[("OpenWRT sysbackup file", ".tar.gz")])
        if file is not None:
            self.backup_file.set(file.name)

        


class GUI(tk.Tk):
    """Create the GUI"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the window properties
        self.title("openwrt-build")
        self.geometry("1280x960")
        self.resizable(width=False, height=False)

        # Define the UI
        Main(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)


if __name__ == '__main__':
    app = GUI()
    app.mainloop()



#
#        , usecols=['brand',
#         'model', 
#          'supportedsincerel', 
#           'supportedcurrentrel', 
#          'target', 
#        'subtarget']
#