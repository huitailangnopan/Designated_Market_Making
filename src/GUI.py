import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


def get_entry_value(entry, default):
    return int(entry.get()) if entry.get() else default


def run_simulation():
    """
    This function is used to run a simulation based on the parameters entered by the user in the GUI.
    It retrieves the values entered in the GUI, validates them, and then runs the simulation using these parameters.
    If the user has not entered a value for a parameter, a default value is used.
    The simulation is run by calling a separate Python script (main.py) using the subprocess module.
    If the user has entered an invalid value (i.e., a non-numeric value for a parameter that requires a number), an error message is displayed.
    """
    try:
        # Retrieve the number of rounds from the GUI, or use a default value of 100 if no value has been entered
        num_rounds = get_entry_value(num_rounds_entry, 100)
        # Retrieve the number of market makers from the GUI, or use a default value of 1 if no value has been entered
        num_market_makers = get_entry_value(num_market_makers_entry, 1)
        # Retrieve the value of the "Use Real Market Price" checkbox from the GUI
        use_real_market = use_real_market_var.get()

        # Display a message box showing the parameters that will be used for the simulation
        messagebox.showinfo("Simulation Parameters",
                            f"Number of Rounds: {num_rounds}\n"
                            f"Number of Market Makers: {num_market_makers}\n"
                            f"Use Real Market Price: {'Yes' if use_real_market else 'No'}")

        # Construct the command to run the simulation, including the parameters
        command = ["python", "main.py", "--num_rounds", str(num_rounds), "--num_market_makers", str(num_market_makers)]
        # If the "Use Real Market Price" checkbox is checked, add the corresponding option to the command
        if use_real_market:
            command.append("--use_real_market")
        # Run the simulation by calling the main.py script with the subprocess module
        subprocess.run(command)

    except ValueError:
        # If the user has entered an invalid value (i.e., a non-numeric value for a parameter that requires a number), display an error message
        messagebox.showerror("Error", "Please enter valid numbers for rounds and market makers.")


root = tk.Tk()
root.title("Simulation Configuration")


def create_label_entry(label_text, row):
    """
    This function creates a label and an entry field in the GUI.

    Parameters:
    label_text (str): The text to be displayed as the label.
    row (int): The row number where the label and entry field should be placed in the grid.

    Returns:
    entry: The entry field that was created.
    """
    # Create a label with the given text and place it in the specified row and column 0
    ttk.Label(root, text=label_text).grid(row=row, column=0, padx=10, pady=10, sticky="w")

    # Create an entry field and place it in the specified row and column 1
    entry = ttk.Entry(root)
    entry.grid(row=row, column=1, padx=10, pady=10, sticky="e")

    # Return the created entry field
    return entry


num_rounds_entry = create_label_entry("Number of Rounds:", 0)
num_market_makers_entry = create_label_entry("Number of Market Makers:", 1)

use_real_market_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Use Real Market Price", variable=use_real_market_var).grid(row=2, columnspan=2, padx=10,
                                                                                       pady=10)

ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=3, columnspan=2, padx=10, pady=20)

root.mainloop()
