import os
import hashlib
import time
import tkinter as tk
from tkinter import messagebox

def calculate_file_hash(filepath):
    sha512 = hashlib.sha512()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)  # Read the file in chunks of 64KB
            if not data:
                break
            sha512.update(data)
    return sha512.hexdigest()

def erase_baseline_if_already_exists():
    if os.path.exists('baseline.txt'):
        os.remove('baseline.txt')

def collect_baseline():
    erase_baseline_if_already_exists()

    # Calculate Hash from the target files and store in baseline.txt
    with open('baseline.txt', 'w') as baseline_file:
        for root, _, files in os.walk('./Files'):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)
                baseline_file.write(f"{file_path}    |    {file_hash}\n")

def monitor_files():
    file_hash_dict = {}

    # Load file|hash from baseline.txt and store them in a dictionary
    with open('baseline.txt', 'r') as baseline_file:
        for line in baseline_file:
            #print(line.strip().split())
            t=line.strip().split()[0]
            
            #print(t.replace(remove," ",1))
            #print(line.strip().split()[0][:7]+line.strip().split()[0][7:])
            file_path, file_hash = line.strip().split('|')
            remove=file_path.strip().split()[0][:7]+line.strip().split()[0][7:]
            print(remove)
            file_path=remove
            #print(file_path, file_hash)
            file_hash_dict[file_path] = file_hash
    print(file_hash_dict)
    f=1
    while True:
        time.sleep(3)

        for root, _, files in os.walk("./Files"):

            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                file_hash = calculate_file_hash(file_path)
                #print(file_path,file_hash)
                # Notify if a new file has been created
                if file_path not in file_hash_dict:
                    messagebox.showinfo("New File Created", f"{file_path} has been created!")
                    
                    
                    
             
                    
                    

                # Notify if a file has been changed
                elif file_hash_dict[file_path] != file_hash:
                    messagebox.showwarning("File Modified", f"{file_path} has changed!")
                    f=0
                    
                    
            
                    
        # Notify if a file has been deleted
        for file_path in list(file_hash_dict.keys()):
            if not os.path.exists(file_path):
                messagebox.showerror("File Deleted", f"{file_path} has been deleted!")
                del file_hash_dict[file_path]
                f=0
                break

def on_collect_baseline():
    collect_baseline()
    messagebox.showinfo("Baseline Collected", "Baseline has been successfully collected and saved.")

def on_monitor_files():
    monitor_files()

# Create a GUI window
root = tk.Tk()
root.title("File Monitor")

# Create buttons to collect baseline and monitor files
collect_button = tk.Button(root, text="Collect Baseline", command=on_collect_baseline)
collect_button.pack(pady=10)

monitor_button = tk.Button(root, text="Monitor Files", command=on_monitor_files)
monitor_button.pack(pady=10)

root.mainloop()
