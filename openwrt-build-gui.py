#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os.path
import csv
import json
import gzip
import urllib.request

#####################################################################
######################## VARIABLES ##################################
#####################################################################

# Enable file caching and some dev output
debug=True

#####################################################################
######################## FUNCTIONS ##################################
#####################################################################

def get_toh():
    """
    Retrieves the openwrt.org table of hardware and returns it as a list of dicts
    """
    toh_cache_file = "sources/toh.tsv"
    if debug is True and os.path.isfile(toh_cache_file):
        with open(toh_cache_file) as infile:
            toh = json.load(infile)
    else:
        toh_gz_handle = urllib.request.urlopen("https://openwrt.org/_media/toh_dump_tab_separated.gz")
        toh_handle = gzip.open(toh_gz_handle, mode='rt', encoding='ISO-8859-1')
        toh_dict = csv.DictReader(toh_handle, delimiter='\t')
        # Convert the DictReader object to a native list of dicts
        toh = list(toh_dict)

    # Sanitize it
    junk = ['', 'nan', 'NULL', '-', '?', '¿', ' ']
    toh = [d for d in toh if d['target'] not in junk and d['subtarget'] not in junk]

    # Save to cache file
    with open(toh_cache_file, 'w') as outfile:
        json.dump(toh, outfile)

    return toh

#####################################################################
######################## CLASSES ####################################
#####################################################################

class DeviceFrame(tk.Frame):
    """This class renders the device information frame"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Make a dict to hold our widgets
        self.widgets = {}

        # Get the Table of Hardware (toh) data frame from openwrt.org
        self.toh = get_toh()

        # Create device frame and widgets
        self.device_frame = tk.LabelFrame(self, text="Select Device")
        self.device_frame.grid(row=0, column=0, sticky=(tk.W + tk.E))
        self.info_frame = tk.LabelFrame(self, text="Info")
        self.info_frame.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.version_frame = tk.LabelFrame(self, text="Version")
        self.version_frame.grid(row=2, column=0, sticky=(tk.W + tk.E))

        self.targets_widget(parent)
        self.subtargets_widget(parent)
        self.info_widget(parent)
        self.version_widget(parent)

        # Create some traces to repopulate the subtarget menu and info widget
        parent.target.trace("w", lambda var_name, var_index, operation: self.subtargets_widget(parent, regen=True))
        parent.subtarget.trace("w", lambda var_name, var_index, operation: self.info_widget(parent, regen=True))

        # Place the widgets in the device frame
        self.widgets['Target'].grid(row=0, column=0)
        self.widgets['Subtarget'].grid(row=1, column=0)
        self.widgets['Version'].grid(row=0, column=0)
        self.widgets['Info'].grid(row=0, column=1)
        

    def targets_widget(self, parent):
        """A Combobox of targets from the ToH"""

        targets = [k['target'] for k in self.toh]
        targets = sorted(set(targets))
        parent.target.set(targets[0])

        self.widgets['Target'] = LabelInput(
            self.device_frame,
            label='Target:',
            input_class=ttk.Combobox,
            input_var=parent.target,
            options_list=targets
        )


    def subtargets_widget(self, parent, regen=None):
        """A Combobox of subtargets of the current target"""
        regen = regen or False
        subtargets = [d['subtarget'] for d in self.toh if d['target'] == parent.target.get()]
        subtargets = sorted(set(subtargets))
        parent.subtarget.set(subtargets[0])
        if regen is True:
            self.widgets['Subtarget'].input['values'] = subtargets
            return
        self.widgets['Subtarget'] = LabelInput(
            self.device_frame,
            label='Subtarget:',
            input_class=ttk.Combobox,
            input_var=parent.subtarget,
            options_list=subtargets
        )


    def info_widget(self, parent, regen=None):
        """An InfoBox of info about the current subtarget"""
        regen = regen or False
        # Add any stat that you wish to display to this list
        stats = {'devicetype': 'Type', 'brand': 'Brand', 'model': 'Model', 'cpu': 'CPU', 'supportedsincerel': 'First Release', 
            'supportedcurrentrel': 'Current Release', 'packagearchitecture': 'Arch',  'wikideviurl': 'Wiki'}
        for device in self.toh:
            if device['target'] == parent.target.get() and device['subtarget'] == parent.subtarget.get():
                break
        # Stringify
        stats_str = '\n'.join('{}: {}'.format(stats[k], v) for k, v in device.items() if k in stats)
        parent.subtarget_info.set(stats_str)
        if regen is True:
            return
        self.widgets['Info'] = LabelInput(
            self.device_frame,
            label='',
            input_class=ttk.Label,
            input_var=parent.subtarget_info,
            textvariable=parent.subtarget_info,
        )


    def version_widget(self, parent):
        """A Combobox of version numbers"""
        # A space-delim'd string of version numbers TODO: make automatic from scraped data (repo tags?)
        versions = 'snapshot 12.09'

        parent.version.set('snapshot')

        self.widgets['Version'] = LabelInput(
            self.version_frame,
            label='',
            input_class=ttk.Combobox,
            input_var=parent.version,
            options_list=versions
        )


 
class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, *args,  label='', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None, options_list=None,
                 **kwargs):
        super().__init__(parent)
        input_args = input_args or {}
        label_args = label_args or {}
        options_list = options_list or []
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var
            if input_class in (ttk.OptionMenu, ttk.Combobox):
                input_args["values"] = options_list
            

        if input_class is ttk.OptionMenu:
            self.input = input_class(self, self.variable, *options_list)
        else:
            self.input = input_class(self, **input_args)

        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        if self.variable:
            return self.variable.get()
        elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.END)
        else:
            return self.input.get()

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
                self.variable.set(bool(value))
        elif self.variable:
                self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)



class GUI(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the window properties
        self.title("openwrt-build")
        self.geometry("800x600")
        self.resizable(width=False, height=False)

        ttk.Label(
            self,
            text="OpenWRT Image Builder",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        # Let's store the global tk vars in this top-level class
        self.target = tk.StringVar()
        self.subtarget = tk.StringVar()
        self.subtarget_info = tk.StringVar()
        self.version = tk.StringVar()

        # Add each frame class
        self.device_frame = DeviceFrame(self)
        self.device_frame.grid(row=1, column=0, sticky=(tk.W + tk.E))


if __name__ == '__main__':
    app = GUI()
    app.mainloop()

