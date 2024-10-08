import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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


def convert_srec_to_hex(srec_file, hex_file):
    try:
        result = subprocess.run(["srec_cat", srec_file, "-Motorola", "-o", hex_file, "-Intel"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            messagebox.showinfo("Success", f"Successfully converted {srec_file} to {hex_file}")
        else:
            messagebox.showerror("Error", f"Error: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_hex_file():
    file_path = filedialog.askopenfilename(title="Select HEX file", filetypes=[("HEX files", "*.hex")])
    hex_file_entry.delete(0, tk.END)
    hex_file_entry.insert(0, file_path)

def save_hex_file():
    file_path = filedialog.asksaveasfilename(title="Save as HEX file", defaultextension=".hex", filetypes=[("HEX files", "*.hex")])
    hex_file_entry.delete(0, tk.END)
    hex_file_entry.insert(0, file_path)

def browse_srec_file():
    file_path = filedialog.askopenfilename(title="Select SREC file", filetypes=[("SREC files", "*.s19")])
    srec_file_entry.delete(0, tk.END)
    srec_file_entry.insert(0, file_path)

def save_srec_file():
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

def start_conversion2():
    hex_file = hex_file_entry.get()
    srec_file = srec_file_entry.get()
    if not hex_file or not srec_file:
        messagebox.showwarning("Input error", "Please select both HEX and SREC file paths.")
    else:
        convert_srec_to_hex(srec_file, hex_file)

        

def browse_and_open_srec_file():
    file_path = filedialog.askopenfilename(title="Open SREC file", filetypes=[("SREC files", "*.s19")])
    if file_path:
        checksum_table.delete(*checksum_table.get_children())  # Clear the table
        
        try:
            with open(file_path, 'r') as file:
                srec_data = file.readlines()
                for line_number, line in enumerate(srec_data, start=1):
                    cleaned_line = line.strip()
                    checksum = calculate_checksum(cleaned_line)
                    checksum_table.insert('', 'end', values=(line_number, cleaned_line, checksum))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

def calculate_checksum(srec_line):
    """
    Calculates the checksum of a given SREC line based on the SREC format.
    The checksum is the least significant byte of the ones' complement of the sum of the byte count, address, and data fields.
    """
    try:
        srec_data = srec_line[2:]  # Exclude the 'S' and record type

        byte_values = [int(srec_data[i:i+2], 16) for i in range(0, len(srec_data) - 2, 2)]  # Exclude the last 2 chars (checksum)

        total_sum = sum(byte_values)

        checksum = 0xFF - (total_sum & 0xFF)

        return f"0x{checksum:02X}"
    except Exception as e:
        return "Error"

def show_conversion_frame():
    conversion_frame.tkraise()

def show_srec_viewer_frame():
    srec_viewer_frame.tkraise()

def show_checksum_frame():
    checksum_frame.tkraise()

def close_app():
    root.quit()

def about_app():
    messagebox.showinfo("About", "HEX2SREC Converter\nVersion 1.0\nPowered by SRecord tool\nAuthor: Akhil Simha Neela (github.com/akhilsimha)")

# Function for calculating checksum for single SREC line
def calculate_single_checksum():
    srec_line = single_srec_entry.get()
    if not srec_line.startswith('S'):
        messagebox.showerror("Error", "Invalid SREC line. It should start with 'S'.")
        return
    checksum = calculate_checksum(srec_line)
    checksum_result_label.config(text=f"Calculated Checksum: {checksum}")

# Create main window
root = tk.Tk()
root.title("HEX2SREC")
root.iconbitmap("Logo.ico")
root.geometry("800x600")

# Apply ttk style for modern look
style = ttk.Style()

style.theme_use('clam')  # You can use "clam" for customizable styling

# Menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="SREC Converter", command=show_conversion_frame)  
file_menu.add_command(label="SREC Viewer", command=show_srec_viewer_frame)
file_menu.add_command(label="Checksum Calculator", command=show_checksum_frame)  # New option for checksum calculation
file_menu.add_separator()  
file_menu.add_command(label="Quit", command=close_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# About menu
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=about_app)
menu_bar.add_cascade(label="About", menu=about_menu)

root.config(menu=menu_bar)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame for HEX to SREC Conversion
conversion_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
conversion_frame.grid(row=0, column=0, sticky="nsew")

conversion_frame.grid_rowconfigure(0, weight=1)
conversion_frame.grid_rowconfigure(1, weight=1)
conversion_frame.grid_rowconfigure(2, weight=1)
conversion_frame.grid_columnconfigure(1, weight=1)

# HEX file selection
ttk.Label(conversion_frame, text="Select HEX File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
hex_file_entry = ttk.Entry(conversion_frame)
hex_file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(conversion_frame, text="Browse", command=browse_hex_file).grid(row=0, column=2, padx=5, pady=10)

# SREC file selection
ttk.Label(conversion_frame, text="Select Output SREC File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
srec_file_entry = ttk.Entry(conversion_frame)
srec_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(conversion_frame, text="Browse", command=browse_srec_file).grid(row=1, column=2, padx=5, pady=10)

ttk.Button(conversion_frame, text="Convert", command=start_conversion).grid(row=2, column=1, pady=20)

# SREC file selection
ttk.Label(conversion_frame, text="Select SREC File:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
srec_file_entry = ttk.Entry(conversion_frame)
srec_file_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(conversion_frame, text="Browse", command=browse_srec_file).grid(row=3, column=2, padx=5, pady=10)

# HEX file selection
ttk.Label(conversion_frame, text="Select Output HEX File:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
hex_file_entry = ttk.Entry(conversion_frame)
hex_file_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(conversion_frame, text="Browse", command=save_hex_file).grid(row=4, column=2, padx=5, pady=10)

ttk.Button(conversion_frame, text="Convert", command=start_conversion2).grid(row=5, column=1, pady=20)

# Frame for SREC Viewer
srec_viewer_frame = ttk.Frame(root)
srec_viewer_frame.grid(row=0, column=0, sticky="nsew")

srec_viewer_frame.grid_rowconfigure(1, weight=1)
srec_viewer_frame.grid_columnconfigure(0, weight=1)

ttk.Label(srec_viewer_frame, text="Open and View SREC File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
ttk.Button(srec_viewer_frame, text="Open SREC File", command=browse_and_open_srec_file).grid(row=0, column=1, padx=10, pady=10)

checksum_table_frame = ttk.Frame(srec_viewer_frame)
checksum_table_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

columns = ('Line No.', 'Data', 'Calculated Checksum')
checksum_table = ttk.Treeview(checksum_table_frame, columns=columns, show='headings', height=15)

checksum_table.heading('Line No.', text='Line No.')
checksum_table.heading('Data', text='Data')
checksum_table.heading('Calculated Checksum', text='Calculated Checksum')

checksum_table.column('Line No.', width=100, anchor='center')
checksum_table.column('Data', width=500, anchor='w')
checksum_table.column('Calculated Checksum', width=150, anchor='center')

scrollbar = ttk.Scrollbar(checksum_table_frame, orient='vertical', command=checksum_table.yview)
checksum_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

checksum_table.pack(fill=tk.BOTH, expand=True)

# Frame for Single Line Checksum Calculation
checksum_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
checksum_frame.grid(row=0, column=0, sticky="nsew")

checksum_frame.grid_columnconfigure(1, weight=1)

ttk.Label(checksum_frame, text="Enter or Paste SREC Line:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
single_srec_entry = ttk.Entry(checksum_frame)
single_srec_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

ttk.Button(checksum_frame, text="Calculate Checksum", command=calculate_single_checksum).grid(row=1, column=1, padx=10, pady=10)

checksum_result_label = ttk.Label(checksum_frame, text="Calculated Checksum: ")
checksum_result_label.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
