import sorter as s
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
 
sorter = TkinterDnD.Tk()


def on_button_click():
    basedir = entry.get()
    func = sorts[selection.get()][0]
    variation = sorts[selection.get()][1]
    print(func, variation)
    if variation:
        file_types = func(basedir, variation)
    else:
        file_types = func(basedir)
    s.move(file_types, basedir)


sorts = {'select sort type': [None, None],
         'File Type': [s.file_type, None],
         'File Extension': [s.file_ext, None],
         'File Date(days)': [s.file_date_new, 'days'],
         'File Date(months)': [s.file_date_new, 'months'],
         'File Date(years)': [s.file_date_new, 'years'],
         'EXTRACT': [s.extract, None],
         }


def sortby_selection(event):
    sort = selection.get()
    print(f'Selected: {sort}')


selection = tk.StringVar()


def drop(event):
    dropped_files = event.data
    if dropped_files.startswith('{') and dropped_files.endswith('}'):
        dropped_files = dropped_files[1:-1]
    entry.delete(0, tk.END)
    entry.insert(0, dropped_files)


selection.set(list(sorts.keys())[0])
sorter.title("File Sorter")
sorter.attributes("-topmost", True)
sorter.geometry("315x260")
label = tk.Label(sorter, text="File Path to Sort:")
entry = tk.Entry(sorter, width=40)
button = tk.Button(sorter, text="Sort", command=on_button_click, height=1, width=20)
egg = tk.Label(sorter, text="( ͡° ͜ʖ ͡°)")
dropdown = ttk.OptionMenu(sorter, selection, *sorts, command=sortby_selection)
file_eater = tk.Label(sorter, text="Drag and drop files here", bg="lightgrey", width=40, height=8)


file_eater.drop_target_register(DND_FILES)
file_eater.dnd_bind('<<Drop>>', drop)


#Build
label.pack()
entry.pack(pady=10)
file_eater.pack()
button.pack(pady=10)
dropdown.pack()
egg.pack(pady=90)

# Run the application
sorter.mainloop()

