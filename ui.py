
# import tkinter as tk
# from tkinter import ttk
# from fetch_data import get_all_bus_times, get_commuter_rail_schedule, parse_time_str
# from datetime import datetime
# import pytz

# # === CONFIG ===
# REFRESH_INTERVAL = 600_000  # 10 minutes in milliseconds

# # === COLORS ===
# GREEN = "\033[92m"
# YELLOW = "\033[93m"
# RESET = "\033[0m"

# # === TKINTER WINDOW ===
# root = tk.Tk()
# root.title("Lowell Departure Board")
# root.geometry("800x400")

# # Top frame for next connection
# top_frame = ttk.Frame(root, padding=10)
# top_frame.pack(fill=tk.X)
# next_connection_label = ttk.Label(top_frame, text="", font=("Helvetica", 16, "bold"))
# next_connection_label.pack()

# # Bottom frame for full schedules
# bottom_frame = ttk.Frame(root, padding=10)
# bottom_frame.pack(fill=tk.BOTH, expand=True)

# # Bus schedule
# bus_frame = ttk.Frame(bottom_frame)
# bus_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# bus_label = ttk.Label(bus_frame, text="🚌 Bus Schedule", font=("Helvetica", 14, "bold"))
# bus_label.pack(pady=5)
# bus_listbox = tk.Listbox(bus_frame, font=("Helvetica", 12))
# bus_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# # Train schedule
# train_frame = ttk.Frame(bottom_frame)
# train_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
# train_label = ttk.Label(train_frame, text="🚆 Train Schedule", font=("Helvetica", 14, "bold"))
# train_label.pack(pady=5)
# train_listbox = tk.Listbox(train_frame, font=("Helvetica", 12))
# train_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# # === UPDATE FUNCTION ===
# def update_board():
#     bus_listbox.delete(0, tk.END)
#     train_listbox.delete(0, tk.END)

#     eastern = pytz.timezone("America/New_York")
#     now = datetime.now(eastern)

#     bus_times = get_all_bus_times()
#     train_times = get_commuter_rail_schedule()

#     # Populate train list
#     for t in train_times:
#         train_listbox.insert(tk.END, t.strftime("%I:%M %p"))

#     # Populate bus list
#     for b in bus_times:
#         dt = parse_time_str(b["time"])
#         if dt >= now:
#             bus_listbox.insert(tk.END, b["time"])

#     # Determine next connection
#     next_conn = None
#     for b in bus_times:
#         bus_dt = parse_time_str(b["time"])
#         next_train = next((t for t in train_times if t > bus_dt), None)
#         if next_train:
#             next_conn = f"Next Connection: 🚌 {bus_dt.strftime('%I:%M %p')} → 🚆 {next_train.strftime('%I:%M %p')}"
#             break
#     next_connection_label.config(text=next_conn if next_conn else "No more connections today")

#     # Schedule next update
#     root.after(REFRESH_INTERVAL, update_board)

# # Initial update
# update_board()
# root.mainloop()

# ui.py
import tkinter as tk
from tkinter import ttk
from fetch_data import get_all_bus_times, get_commuter_rail_schedule, parse_time_str
from datetime import datetime
import pytz

# === CONFIG ===
REFRESH_INTERVAL = 600_000  # 10 minutes in milliseconds
COUNTDOWN_INTERVAL = 1_000  # 1 second

# === TKINTER WINDOW ===
root = tk.Tk()
root.title("Lowell Departure Board")
root.geometry("800x450")

# Top frame for next connection
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill=tk.X)

next_connection_label = ttk.Label(top_frame, text="", font=("Helvetica", 16, "bold"))
next_connection_label.pack()
countdown_label = ttk.Label(top_frame, text="", font=("Helvetica", 12))
countdown_label.pack()

# Bottom frame for full schedules
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(fill=tk.BOTH, expand=True)

# Bus schedule
bus_frame = ttk.Frame(bottom_frame)
bus_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
bus_label = ttk.Label(bus_frame, text="🚌 Bus Schedule", font=("Helvetica", 14, "bold"))
bus_label.pack(pady=5)
bus_listbox = tk.Listbox(bus_frame, font=("Helvetica", 12))
bus_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Train schedule
train_frame = ttk.Frame(bottom_frame)
train_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
train_label = ttk.Label(train_frame, text="🚆 Train Schedule", font=("Helvetica", 14, "bold"))
train_label.pack(pady=5)
train_listbox = tk.Listbox(train_frame, font=("Helvetica", 12))
train_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# === GLOBAL COUNTDOWN STATE ===
time_left = REFRESH_INTERVAL // 1000  # seconds

# === UPDATE FUNCTION ===
def update_board():
    global time_left
    bus_listbox.delete(0, tk.END)
    train_listbox.delete(0, tk.END)

    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)

    bus_times = get_all_bus_times()
    train_times = get_commuter_rail_schedule()

    # Populate train list
    for t in train_times:
        train_listbox.insert(tk.END, t.strftime("%I:%M %p"))

    # Populate bus list
    for b in bus_times:
        dt = parse_time_str(b["time"])
        if dt >= now:
            bus_listbox.insert(tk.END, b["time"])

    # Determine next connection and color-code
    next_conn_text = "No more connections today"
    next_conn_color = "black"

    for b in bus_times:
        bus_dt = parse_time_str(b["time"])
        if bus_dt < now:
            continue
        next_train = next((t for t in train_times if t > bus_dt), None)
        if next_train:
            diff = (next_train - bus_dt).total_seconds() / 60
            next_conn_text = f"Next Connection: 🚌 {bus_dt.strftime('%I:%M %p')} → 🚆 {next_train.strftime('%I:%M %p')} ({int(diff)} min apart)"
            if diff <= 40:
                next_conn_color = "green"
            elif 40 < diff <= 60:
                next_conn_color = "orange"
            else:
                next_conn_color = "red"
            break

    next_connection_label.config(text=next_conn_text, foreground=next_conn_color)

    # Reset countdown
    time_left = REFRESH_INTERVAL // 1000
    update_countdown()
    # Schedule next refresh
    root.after(REFRESH_INTERVAL, update_board)


def update_countdown():
    global time_left
    minutes, seconds = divmod(time_left, 60)
    countdown_label.config(text=f"Refreshing in {minutes:02}:{seconds:02}")
    if time_left > 0:
        time_left -= 1
        root.after(1000, update_countdown)

# Initial update
update_board()
root.mainloop()
