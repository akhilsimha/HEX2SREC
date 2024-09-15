import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def convert_hex_to_srec(hex_file, srec_file):
    try:
        result = subprocess.run(["srec_cat", hex_file, "-Intel", "-o", srec_file, "-Motorola"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            messagebox.showinfo("Success", f"Successfully converted {hex_file} to {srec_file}")
        else:
            messagebox.showerror("Error", f"Error: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_hex_file():
    file_path = filedialog.askopenfilename(title="Select HEX file", filetypes=[("HEX files", "*.hex")])
    hex_file_entry.delete(0, tk.END)
    hex_file_entry.insert(0, file_path)

def browse_srec_file():
    file_path = filedialog.asksaveasfilename(title="Save as SREC file", defaultextension=".s19", filetypes=[("SREC files", "*.s19")])
    srec_file_entry.delete(0, tk.END)
    srec_file_entry.insert(0, file_path)

def start_conversion():
    hex_file = hex_file_entry.get()
    srec_file = srec_file_entry.get()
    if not hex_file or not srec_file:
        messagebox.showwarning("Input error", "Please select both HEX and SREC file paths.")
    else:
        convert_hex_to_srec(hex_file, srec_file)

def browse_and_open_srec_file():
    file_path = filedialog.askopenfilename(title="Open SREC file", filetypes=[("SREC files", "*.s19")])
    if file_path:
        srec_viewer.delete(1.0, tk.END)
        try:
            with open(file_path, 'r') as file:
                srec_data = file.read()
                srec_viewer.insert(tk.END, srec_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

def show_conversion_frame():
    conversion_frame.tkraise()

def show_srec_viewer_frame():
    srec_viewer_frame.tkraise()

def close_app():
    root.quit()

def about_app():
    messagebox.showinfo("About", "HEX2SREC Converter\nVersion 1.0\nPowered by SRecord tool\nAuthor: Akhil Simha Neela (github.com/akhilsimha)")

# Create main window
root = tk.Tk()
root.title("HEX2SREC")
root.iconbitmap("Logo.ico")
root.geometry("800x600")

# Menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open S19 Viewer", command=show_srec_viewer_frame)  # Add option to open S19 viewer
file_menu.add_command(label="Close", command=close_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# About menu
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=about_app)
menu_bar.add_cascade(label="About", menu=about_menu)

# Set the menu to the window
root.config(menu=menu_bar)

# Frame for HEX to SREC Conversion
conversion_frame = tk.Frame(root)
conversion_frame.grid(row=0, column=0, sticky="nsew")

# HEX file selection
tk.Label(conversion_frame, text="Select HEX File:").grid(row=0, column=0, padx=10, pady=10)
hex_file_entry = tk.Entry(conversion_frame, width=50)
hex_file_entry.grid(row=0, column=1, padx=10)
tk.Button(conversion_frame, text="Browse", command=browse_hex_file).grid(row=0, column=2, padx=10)

# SREC file selection
tk.Label(conversion_frame, text="Select Output SREC File:").grid(row=1, column=0, padx=10, pady=10)
srec_file_entry = tk.Entry(conversion_frame, width=50)
srec_file_entry.grid(row=1, column=1, padx=10)
tk.Button(conversion_frame, text="Browse", command=browse_srec_file).grid(row=1, column=2, padx=10)

# Convert button
tk.Button(conversion_frame, text="Convert", command=start_conversion, height=2, width=15).grid(row=2, column=1, pady=20)

# Frame for SREC Viewer
srec_viewer_frame = tk.Frame(root)
srec_viewer_frame.grid(row=0, column=0, sticky="nsew")

# SREC Viewer
tk.Label(srec_viewer_frame, text="Open and View SREC File:").grid(row=0, column=0, padx=10, pady=10)
tk.Button(srec_viewer_frame, text="Open SREC File", command=browse_and_open_srec_file).grid(row=0, column=1, padx=10, pady=10)

# Scrolled text box to display the contents of the SREC file
srec_viewer = scrolledtext.ScrolledText(srec_viewer_frame, width=90, height=20, wrap=tk.WORD)
srec_viewer.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start by showing the conversion frame
conversion_frame.tkraise()

root.mainloop()
