import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import fastf1
import fastf1.plotting
import matplotlib as mpl
from tkinter.filedialog import asksaveasfilename
import random


fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# Tyre data (customizable per race)
tyre_options = {
    "C1–C2–C3": ["C1", "C2", "C3"],  # Monaco 2025 compounds
}


tyre_data = {
    'C1': {'min_life': 30, 'max_life': 40, 'lap_time_range': (78.0, 79.5), 'color': 'white'},
    'C2': {'min_life': 22, 'max_life': 32, 'lap_time_range': (76.5, 78.0), 'color': 'yellow'},
    'C3': {'min_life': 15, 'max_life': 25, 'lap_time_range': (75.0, 76.2), 'color': 'red'},
}


last_figure = None

def generate_strategy(num_stints, available_tyres):
    while True:
        chosen = [random.choice(available_tyres) for _ in range(num_stints)]
        if len(set(chosen)) >= 2:
            return chosen

def simulate_stint(tyre, num_laps):
    min_time, max_time = tyre_data[tyre]['lap_time_range']
    return [random.uniform(min_time, max_time) for _ in range(num_laps)]

def simulate_race(num_laps, pit_stop_time, num_pit_stops, available_tyres):
    num_stints = num_pit_stops + 1
    strategy = generate_strategy(num_stints, available_tyres)
    remaining_laps = num_laps
    lap_times = []
    stints = []
    start_lap = 1

    for i in range(num_stints):
        tyre = strategy[i]
        min_life = tyre_data[tyre]['min_life']
        max_life = tyre_data[tyre]['max_life']

        if i == num_stints - 1:
            stint_laps = remaining_laps
        else:
            try:
                max_valid = min(max_life, remaining_laps - sum(tyre_data[strategy[j]]['min_life'] for j in range(i+1, num_stints)))
            except IndexError:
                return None
            if max_valid < min_life:
                return None
            stint_laps = random.randint(min_life, max_valid)

        lap_times += simulate_stint(tyre, stint_laps)
        end_lap = start_lap + stint_laps - 1
        stints.append((tyre, start_lap, end_lap))
        start_lap += stint_laps
        remaining_laps -= stint_laps

    total_time = sum(lap_times) + pit_stop_time * num_pit_stops
    return total_time, stints

def run_simulation():
    try:
        num_laps = int(laps_entry.get())
        pit_stop_time = int(pit_entry.get())
        num_sim = int(sim_entry.get())
        num_pit_stops = int(pitstop_entry.get())
        selected_tyres = tyre_options[tyre_var.get()]
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers.")
        return

    for widget in output_frame.winfo_children():
        widget.destroy()

    results = []
    while len(results) < num_sim:
        output = simulate_race(num_laps, pit_stop_time, num_pit_stops, selected_tyres)
        if output:
            total_time, stints = output
            strat = '-'.join([s[0][0] for s in stints])  # S-M-H
            breakdown = ', '.join([f"{s[0][0]}({s[1]}–{s[2]})" for s in stints])
            results.append((strat, round(total_time, 1), breakdown, stints))

    top_results = sorted(results, key=lambda x: x[1])[:3]
    display_results_table(top_results)
    plot_strategy_timeline(top_results)

def display_results_table(results):
    label = tk.Label(output_frame, text="Simulation", font=("Helvetica", 12, "bold"))
    label.pack(pady=5)

    tree = ttk.Treeview(output_frame, columns=("Strategy", "Time", "Stint"), show='headings', height=5)
    tree.heading("Strategy", text="Strategy")
    tree.heading("Time", text="Total Time (s)")
    tree.heading("Stint", text="Stint Breakdown")
    for row in results:
        tree.insert("", "end", values=row[:3])
    tree.pack(pady=5)

    save_btn = tk.Button(output_frame, text="Save Graph as Image", command=save_graph_dialog)
    save_btn.pack(pady=5)

def plot_strategy_timeline(results):
    global last_figure
    fig, ax = plt.subplots(figsize=(10, 4))
    labels_used = set()

    for i, result in enumerate(results):
        stints = result[3]
        for stint in stints:
            tyre, start, end = stint
            label = tyre if tyre not in labels_used else ""
            ax.barh(y=i, width=end - start + 1, left=start, height=0.5,
                    color=tyre_data[tyre]['color'], edgecolor='black', label=label)
            labels_used.add(tyre)

    ax.set_xlabel("Lap")
    ax.set_ylabel("Top Strategies")
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["Strategy 1", "Strategy 2", "Strategy 3"])
    ax.set_title("Stint Timeline by Strategy")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')
    last_figure = fig
    plt.tight_layout()
    plt.show()

def save_graph_dialog():
    if last_figure:
        file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            last_figure.savefig(file_path)
            messagebox.showinfo("Success", f"Graph saved to:\n{file_path}")

# GUI setup
root = tk.Tk()
root.title("Tyre Strategy Simulator")
root.geometry("900x600")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Number of Laps:").grid(row=0, column=0, sticky="e")
laps_entry = tk.Entry(input_frame)
laps_entry.insert(0, "78")
laps_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Pit Stop Time Loss (s):").grid(row=1, column=0, sticky="e")
pit_entry = tk.Entry(input_frame)
pit_entry.insert(0, "22")
pit_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Number of Simulations:").grid(row=2, column=0, sticky="e")
sim_entry = tk.Entry(input_frame)
sim_entry.insert(0, "1000")
sim_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Number of Pit Stops:").grid(row=3, column=0, sticky="e")
pitstop_entry = tk.Entry(input_frame)
pitstop_entry.insert(0, "2")
pitstop_entry.grid(row=3, column=1)

tk.Label(input_frame, text="Tyre Compounds Available:").grid(row=4, column=0, sticky="e")
tyre_var = tk.StringVar(root)
tyre_var.set("Soft–Medium–Hard")
tyre_menu = ttk.OptionMenu(input_frame, tyre_var, *tyre_options.keys())
tyre_menu.grid(row=4, column=1)

tk.Button(
    input_frame,
    text="▶ Run Monte Carlo Simulation",
    command=run_simulation,
    bg="#28a745",
    fg="black",
    activebackground="#218838",
    font=("Helvetica", 11, "bold"),
    width=30
).grid(row=5, columnspan=2, pady=12)

output_frame = tk.Frame(root)
output_frame.pack(fill="both", expand=True)

root.mainloop()
