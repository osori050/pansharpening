"""
Pansharpening User Interface - Intended to be used with resolution_changing_code.py file in shared directory

Script Contents:
    - Import Tkinter packages and pansharpening script
    - Create functions necessary to retrieve pansharpening parameters and run resolution_changing_code.py
    - Create Tkinter widgets for the tool window and assign their location
    - Open tool window

This function combines the pansharpening tool from GDAL and the simple_mean pansharpening developed by Thomas Wang, 
which can be found here: https://github.com/ThomasWangWeiHong/Simple-Pansharpening-Algorithms/blob/master/Simple_Pansharpen.py

Created by Erik Sauer and Diego Osorio
"""

#####################################################################################################################

import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import resolution_changing_code

#####################################################################################################################

# Create empty dictionary for each pansharpen input to be populated with file dialog functions
HR_dict = {1: "HR_path"}  # High Resolution / Panchromatic File Path
M_dict = {1: "M_path"}  # Multispectral File Path
Output_dict = {1: "Outpath"}  # Output Filename and Path

def browseinHRFiles():
    """
    This function is used to retrieve the High Resolution File from the set directory

    Inputs:
    - initialdir: starting directory the file dialog will open
    - title: select filename to set or retrieve
    - filetypes: acceptable filetypes
    """
    HR_dict[1] = filedialog.askopenfilename(
        initialdir="/",
        title="Select a High-Resolution File",
        filetypes=(("GTiff", "*.tif*"), ("all files", "*.*")),
    )
    try:
        open(HR_dict[1], 'r')
    except OSError:
        messagebox.showerror('Python Error', 'Error: File Path Not Found!')

def browseinMFiles():
    """
    This function is used to retrieve the Multispectral File from the set directory

    Inputs:
    - initialdir: starting directory the file dialog will open
    - title: select filename to set or retrieve
    - filetypes: acceptable filetypes
    """
    M_dict[1] = filedialog.askopenfilename(
        initialdir="/",
        title="Select a Multispectral File",
        filetypes=(("GTiff", "*.tif*"), ("all files", "*.*")),
    )
    try:
        open(M_dict[1], 'r')
    except OSError:
        messagebox.showerror('Python Error', 'Error: File Path Not Found!')

def browseoutFiles():
    """
    This function is used to set the output file name and location from the set directory

    Inputs:
    - initialdir: starting directory the file dialog will open
    - title: select filename to set or retrieve
    - filetypes: acceptable filetypes
    """
    Output_dict[1] = (
        filedialog.asksaveasfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("GTiff", "*.tif*"),),
        )
        + ".tif"
    )

def pansharpen_run():
    """
    This function is used to retrieve functions from the resolution changing code and run them according to parameters
    input in the interface window

    Inputs:
    - HR: High resolution filepath used in the pansharpening function
    - Output: Output filepath and name
    - M: Multispectral filepath used in the pansharpening function
    - simple_mean: Thomas Wang's Simple Mean script (True/False)
    - resampling: Selected resampling technique from dropdown menu
    """
    resolution_changing_code.wrapper_pansharpen(
        HR_dict[1], Output_dict[1], M_dict[1], simple_mean = mean_input,resampling=(resample_technique.get())
    )
    # Check if box is checked. If 1, run pre-built function. If 0, do not run
    if stack_bands.get() == 1:
        stacked_output = f"{Output_dict[1].split('.')[0]}_stacked.tif"
        resolution_changing_code.stack_bands(
            pan_name=HR_dict[1], psh_names=Output_dict[1], dst_filename=stacked_output
        )
        if calc_statistics.get() == 1:
            resolution_changing_code.calculate_stats(stacked_output)
        if gen_pyramids.get() == 1:
            resolution_changing_code.create_pyramids(stacked_output, resample_pyramids.get())
        os.remove(Output_dict[1])
    
    else:
        if calc_statistics.get() == 1:
            resolution_changing_code.calculate_stats(Output_dict[1])
        if gen_pyramids.get() == 1:
            resolution_changing_code.create_pyramids(Output_dict[1], resample_pyramids.get())
    
#####################################################################################################################

"""
Widget creation, using the following methods:
    - geometry: used to set interface window dimensions
    - title: takes string input to set name at the top of the interface window
    - Button: creates clickable text box with option to attach a command. Command can be a function or method
    - grid: uses a table system to organize widget placement, set with columns and rows
    - StringVar: holds a specified string for string variables
    - OptionMenu: creates dropdown menu with list of clickable options, selection can be saved as a string or
      integer variable. UI window name must be input first (i.e. "window")
    - Label: creates a text widget with string input, appearance can adjusted using width, font, style, etc.
    - IntVar: holds a specified value for integer variables
    - Checkbutton: creates a checkbox with specified string name. Allows a specified "off" value if box is not 
      checked, and "on" value if box is checked
"""
# Create Window, set size and title
window = Tk()
window.geometry("275x205")
window.title("Pansharpening Tool")

# Simple Mean checkbox
mean_input = tk.StringVar() # Create empty "clicked" variable
simple_mean_check = ttk.Checkbutton(
    window,
    variable=mean_input,
    text="Simple Mean",
    onvalue="True",
    offvalue="False",
)
simple_mean_check.grid(column=0, row=3, sticky=tk.W)

# Generate Pyramids Checkbox and Option Menu
gen_pyramids = tk.IntVar() # Create empty "clicked" variable
gen_pyramids_check = ttk.Checkbutton(
    window,
    variable=gen_pyramids,
    text="Generate Pyramids",
    onvalue=1,
    offvalue=0,
)
gen_pyramids_check.grid(column=1, row=3, sticky=tk.W)

# Pyramids method selection, using dropdown menu
resample_pyramids = tk.StringVar() # Create empty "clicked" variable
resample_pyramids.set("Select an Option")
ttk.Label(window, text="Pyramid Method:").grid(column=0, row=4, sticky=tk.W)
gen_pyramids_options = tk.OptionMenu(
    window,
    resample_pyramids,
    "nearest",
    "bilinear",
    "cubic",
    "cubic_spline",
    "lanczos",
    "average",
    "mode",
    "gauss",
    "max",
    "min",
    "med",
    "q1",
    "q3",
    "sum",
    "rms",
)
gen_pyramids_options.grid(column=1, row=4)

# Calculate Statistics checkbox
calc_statistics = tk.IntVar() # Create empty "clicked" variable
calc_statistics_check = ttk.Checkbutton(
    window,
    variable=calc_statistics,
    text="Calculate Statistics",
    onvalue=1,
    offvalue=0,
)
calc_statistics_check.grid(column=0, row=5, sticky=tk.W)

# Stack bands checkbox
stack_bands = tk.IntVar() # Create empty "clicked" variable
stack_bands_check = ttk.Checkbutton(
    window,
    text="Stack Bands",
    variable=stack_bands,
    onvalue=1,
    offvalue=0,
)
stack_bands_check.grid(column=1, row=5, sticky=tk.W)

# Resampling Technique Selection, creates dropdown menu.
# Use .set to have default text
# Current options are those available with gdal_pansharpen
resample_technique = tk.StringVar()
resample_technique.set("Select an Option")
Resample_options = tk.OptionMenu(
    window,
    resample_technique,
    "Nearest Neighbor",
    "Bilinear Interpolation",
    "Cubic Convolution",
    "Cubicspline",
    "Lanczos",
    "Average",
)
Resample_options.grid(
    row=7,
    column=1,
)

# Resampling Technique Label
ttk.Label(window, text="Resampling Technique:").grid(column=0, row=7, sticky=tk.W)

# High Res Input Label/Button
ttk.Label(window, text="High Resolution Input").grid(column=0, row=1, sticky=tk.W)
highres = ttk.Label(window, width=60)
highres.grid(column=2, row=1, sticky=tk.W)
highres_find = ttk.Button(window, text="Find...", command=browseinHRFiles)
highres_find.grid(column=1, row=1)

# Multispectral File Input Label/Button
ttk.Label(window, text="Multispectral Input").grid(column=0, row=2, sticky=tk.W)
multi = ttk.Label(window, width=60)
multi.grid(column=2, row=2, sticky=tk.W)
multi_find = ttk.Button(window, text="Find...", command=browseinMFiles)
multi_find.grid(column=1, row=2)

# Output File Label/Button:
ttk.Label(window, text="Output File").grid(column=0, row=8, sticky=tk.W)
output_label = ttk.Label(window, width=60)
output_label.grid(column=2, row=8, sticky=tk.W)
output_find = ttk.Button(window, text="Set...", command=browseoutFiles)
output_find.grid(column=1, row=8)

# Run Button with pansharpening code incorporated
ttk.Button(
    window,
    text="Run",
    command=pansharpen_run,
).grid(column=1, row=9)

#####################################################################################################################

# Create UI window
window.mainloop()