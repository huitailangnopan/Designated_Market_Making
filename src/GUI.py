import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


def get_entry_value(entry, default):
    return int(entry.get()) if entry.get() else default


def run_simulation():
    try:
        num_rounds = get_entry_value(num_rounds_entry, 100)
        num_market_makers = get_entry_value(num_market_makers_entry, 1)
        use_real_market = use_real_market_var.get()

        messagebox.showinfo("Simulation Parameters",
                            f"Number of Rounds: {num_rounds}\n"
                            f"Number of Market Makers: {num_market_makers}\n"
                            f"Use Real Market Price: {'Yes' if use_real_market else 'No'}")

        command = ["python", "main.py", "--num_rounds", str(num_rounds), "--num_market_makers", str(num_market_makers)]
        if use_real_market:
            command.append("--use_real_market")
        subprocess.run(command)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for rounds and market makers.")


root = tk.Tk()
root.title("Simulation Configuration")


def create_label_entry(label_text, row):
    ttk.Label(root, text=label_text).grid(row=row, column=0, padx=10, pady=10, sticky="w")
    entry = ttk.Entry(root)
    entry.grid(row=row, column=1, padx=10, pady=10, sticky="e")
    return entry


num_rounds_entry = create_label_entry("Number of Rounds:", 0)
num_market_makers_entry = create_label_entry("Number of Market Makers:", 1)

use_real_market_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Use Real Market Price", variable=use_real_market_var).grid(row=2, columnspan=2, padx=10,
                                                                                       pady=10)

ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=3, columnspan=2, padx=10, pady=20)

root.mainloop()
