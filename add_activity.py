import tkinter as tk
from tkinter import messagebox
from activity import Activity
import activity_constant
import enter_screen


def open_add_activity_screen(refresh_callback=None):
    add_window = tk.Toplevel()
    add_window.title("Add New Activity")
    add_window.geometry("350x420")
    add_window.configure(bg="#9AF075")

    tk.Label(
        add_window,
        text="Create New Activity",
        font=("Arial", 14, "bold"),
        bg="#9AF075",
        fg="#1a365d"
    ).pack(pady=15)

    tk.Label(add_window, text="Activity Type:", font=("Arial", 10, "bold"), bg="#9AF075").pack(anchor="w", padx=40)

    selected_activity = tk.StringVar(value=activity_constant.ACTIVITY_LIST[0])

    activity_dropdown = tk.OptionMenu(
        add_window,
        selected_activity,
        *activity_constant.ACTIVITY_LIST
    )
    activity_dropdown.config(font=("Arial", 10), width=22, bg="white", highlightthickness=0)
    activity_dropdown.pack(pady=5)

    tk.Label(add_window, text="Amount of People:", font=("Arial", 10, "bold"), bg="#9AF075").pack(anchor="w", padx=40,
                                                                                                  pady=(10, 0))
    amount_entry = tk.Entry(add_window, font=("Arial", 11), width=25)
    amount_entry.pack(pady=5)

    tk.Label(add_window, text="Date (e.g. 22/11/2026):", font=("Arial", 10, "bold"), bg="#9AF075").pack(anchor="w",
                                                                                                        padx=40,
                                                                                                        pady=(10, 0))
    date_entry = tk.Entry(add_window, font=("Arial", 11), width=25)
    date_entry.pack(pady=5)

    def save_activity():
        act_type = selected_activity.get()
        amount = amount_entry.get().strip()
        date = date_entry.get().strip()

        if act_type == "none":
            messagebox.showwarning("Warning", "Please select a valid activity type!")
            return

        if not amount or not date:
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return

        try:
            amount_num = int(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount of people must be a number!")
            return

        new_act = Activity(act_type, amount_num, date)

        if hasattr(enter_screen, 'user') and enter_screen.user:
            enter_screen.user.add_activity(new_act)
            add_window.destroy()

            if refresh_callback:
                refresh_callback()
        else:
            messagebox.showerror("Error", "No active host user found!")

    tk.Button(
        add_window,
        text="Save Activity",
        font=("Arial", 11, "bold"),
        bg="#588F3F",
        fg="white",
        width=15,
        bd=0,
        cursor="hand2",
        command=save_activity
    ).pack(pady=25)