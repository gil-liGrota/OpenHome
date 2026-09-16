import tkinter as tk
from tkinter import messagebox

from db_config import db
import enter_screen
from guest import Guest
from host import Host
from display_activities_list import open_print_list_screen


def get_doc_names(collection_name):
    docs = db.collection(collection_name).stream()
    return [doc.id for doc in docs]


def check_username(username, login_window):
    guest_names = get_doc_names("guests")
    host_names = get_doc_names("hosts")

    if username in guest_names:
        print(f"Found '{username}' in Guests!")
        user_guest_dict = db.collection("guests").document(username).get().to_dict() or {}

        allergies = user_guest_dict.get("allergies", "")
        enter_screen.user = Guest(
            username,
            user_guest_dict.get("phone", ""),
            user_guest_dict.get("address", ""),
            allergies,
            user_guest_dict.get("is_vegan", False),
            user_guest_dict.get("is_vegetarian", False),
            user_guest_dict.get("bio", ""),
            user_guest_dict.get("is_vegetarian", False)
        )

        login_window.destroy()
        activities_docs = db.collection("activities").stream()
        activities_list = [doc.to_dict() for doc in activities_docs]

        open_print_list_screen(activities_list)

    elif username in host_names:
        print(f"Found '{username}' in Hosts!")
        doc = db.collection("hosts").document(username).get()

        if doc.exists:
            host_data = doc.to_dict()
            activities = host_data.get("activity_list", [])

            enter_screen.user = Host(
                username,
                host_data.get("phone", ""),
                host_data.get("address", ""),
                host_data.get("is_vegan", False),
                host_data.get("is_vegetarian", False),
                host_data.get("bio", ""),
                host_data.get("is_vegetarian", False)
            )

            login_window.destroy()
            open_print_list_screen(activities)
    else:
        messagebox.showinfo("404", f"Username '{username}' does not exist.")


def open_login_screen():
    login_window = tk.Tk()
    login_window.title("Open Home")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f4f8")

    tk.Label(
        login_window,
        text="Log In",
        font=("Arial", 18, "bold"),
        bg="#f0f4f8",
        fg="#1a365d"
    ).pack(pady=(30, 20))

    tk.Label(
        login_window,
        text="Username:",
        font=("Arial", 10, "bold"),
        bg="#f0f4f8",
        fg="#4a5568"
    ).pack(anchor="w", padx=60, pady=(5, 2))

    username_entry = tk.Entry(login_window, font=("Arial", 11), width=28)
    username_entry.pack(pady=5)

    def on_submit():
        entered_name = username_entry.get().strip()
        check_username(entered_name, login_window)

    submit_btn = tk.Button(
        login_window,
        text="Submit",
        font=("Arial", 11, "bold"),
        bg="#2b6cb0",
        fg="white",
        activebackground="#2c5282",
        activeforeground="white",
        width=15,
        height=1,
        bd=0,
        cursor="hand2",
        command=on_submit
    )
    submit_btn.pack(pady=25)

    login_window.mainloop()