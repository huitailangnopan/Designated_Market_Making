import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
# Function to run the simulation with the gathered parameters
def run_simulation():
    try:
        num_rounds = int(num_rounds_entry.get()) if num_rounds_entry.get() else 100  # Default to 100 rounds
        num_market_makers = int(num_market_makers_entry.get()) if num_market_makers_entry.get() else 1  # Default to 10 market makers
        use_real_market = use_real_market_var.get()
        messagebox.showinfo("Simulation Parameters",
                            f"Number of Rounds: {num_rounds}\n"
                            f"Number of Market Makers: {num_market_makers}\n"
                            f"Use Real Market Price: {'Yes' if use_real_market else 'No'}")
        # Here, integrate the functionality to run the main simulation with these parameters
        command = ["python", "main.py", "--num_rounds", str(num_rounds), "--num_market_makers", str(num_market_makers)]
        print("use_real_market")
        if use_real_market:
            command.append("--use_real_market")
        subprocess.run(command)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for rounds and market makers.")

# Initialize the main GUI window
root = tk.Tk()
root.title("Simulation Configuration")

# Create and layout input fields for number of rounds
ttk.Label(root, text="Number of Rounds:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
num_rounds_entry = ttk.Entry(root)
num_rounds_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Create and layout input fields for number of market makers
ttk.Label(root, text="Number of Market Makers:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
num_market_makers_entry = ttk.Entry(root)
num_market_makers_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

# Create and layout a checkbox for using real market price
use_real_market_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Use Real Market Price", variable=use_real_market_var).grid(row=2, columnspan=2, padx=10, pady=10)

# Create and layout the submit button
ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=3, columnspan=2, padx=10, pady=20)

root.mainloop()
