import tkinter as tk
from tkinter import ttk, messagebox
from guest import Guest
from host import Host
import enter_screen
from db_config import db
from display_activities_list import open_print_list_screen
from customtkinter import *

def get_doc_names(collection_name):
    docs = db.collection(collection_name).stream()
    return [doc.id for doc in docs]


def open_signup_screen():
    signup_window = tk.Tk()
    signup_window.title("Open Home")
    signup_window.geometry("500x650")
    signup_window.configure(bg="#f0f4f8")

    main_frame = tk.Frame(signup_window, bg="#9AF075")
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg="#9AF075", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#9AF075")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(fill="both", expand=True, padx=20)
    scrollbar.pack(fill="y")

    tk.Label(
        scrollable_frame,
        text="Create Your Account",
        font=("Arial", 18, "bold"),
        bg="#9AF075",
        fg="#1a365d"
    ).pack(pady=(20, 15))

    def create_entry_field(label_text):
        tk.Label(scrollable_frame, text=label_text, font=("Arial", 10, "bold"), bg="#9AF075", fg="#4a5568").pack(
            anchor="w", pady=(8, 2))
        entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=35)
        entry.pack(anchor="w", pady=(0, 5))
        return entry

    username_entry = create_entry_field("Username:")
    phone_entry = create_entry_field("Phone Number:")
    address_entry = create_entry_field("Address:")
    allergies_entry = create_entry_field("Allergies:")

    tk.Label(scrollable_frame, text="Preferences:", font=("Arial", 10, "bold"), bg="#9AF075", fg="#4a5568").pack(
        anchor="w", pady=(10, 2))

    is_vegetarian = tk.BooleanVar()
    is_vegan = tk.BooleanVar()
    is_religious = tk.BooleanVar()

    tk.Checkbutton(scrollable_frame, text="Vegetarian", variable=is_vegetarian, bg="#9AF075", font=("Arial", 10)).pack(
        anchor="w")
    tk.Checkbutton(scrollable_frame, text="Vegan", variable=is_vegan, bg="#9AF075", font=("Arial", 10)).pack(anchor="w")
    tk.Checkbutton(scrollable_frame, text="Religious", variable=is_religious, bg="#9AF075", font=("Arial", 10)).pack(
        anchor="w")

    tk.Label(scrollable_frame, text="Role:", font=("Arial", 10, "bold"), bg="#9AF075", fg="#4a5568").pack(anchor="w",
                                                                                                          pady=(12, 2))

    role_var = tk.StringVar(value="Guest")
    tk.Radiobutton(scrollable_frame, text="Guest", variable=role_var, value="Guest", bg="#9AF075",
                   font=("Arial", 10)).pack(anchor="w")
    tk.Radiobutton(scrollable_frame, text="Host", variable=role_var, value="Host", bg="#9AF075",
                   font=("Arial", 10)).pack(anchor="w")

    tk.Label(scrollable_frame, text="Bio:", font=("Arial", 10, "bold"), bg="#9AF075", fg="#4a5568").pack(anchor="w",
                                                                                                         pady=(12, 2))
    bio_text = tk.Text(scrollable_frame, font=("Arial", 10), width=35, height=4)
    bio_text.pack(anchor="w", pady=(0, 10))

    def submit_signup():
        name = username_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()
        allergies = allergies_entry.get().strip()
        vegan = is_vegan.get()
        vegetarian = is_vegetarian.get()
        religious = is_religious.get()
        selected_role = role_var.get()
        bio = bio_text.get("1.0", tk.END).strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Please enter both Username and Phone Number!")
            return

        existing_guests = get_doc_names("guests")
        existing_hosts = get_doc_names("hosts")

        if name in existing_guests or name in existing_hosts:
            messagebox.showerror("Username Taken", f"The username '{name}' is already taken. Please choose another one.")
            return

        if selected_role == "Guest":
            new_user = Guest(
                name=name,
                phone=phone,
                address=address,
                allergies=allergies if allergies != '' else "none",
                is_vegan=vegan,
                is_vegetarian=vegetarian,
                is_religious=religious,
                bio=bio
            )
            new_user.add_guest_to_db()

            enter_screen.user = new_user

            activities_docs = db.collection("activities").stream()
            activities_list = []
            for doc in activities_docs:
                act_data = doc.to_dict()
                act_data['doc_id'] = doc.id
                activities_list.append(act_data)

            # messagebox.showinfo("Success", f"{selected_role} registered successfully!")
            signup_window.destroy()

            open_print_list_screen(activities_list)

        elif selected_role == "Host":
            new_user = Host(
                name=name,
                phone=phone,
                address=address,
                is_vegan=vegan,
                is_vegetarian=vegetarian,
                is_religious=religious,
                bio=bio
            )
            new_user.add_host_to_db()

            enter_screen.user = new_user

            # messagebox.showinfo("Success", f"{selected_role} registered successfully!")
            signup_window.destroy()

            open_print_list_screen([])

    submit_btn = tk.Button(
        scrollable_frame,
        text="Register",
        font=("Arial", 11, "bold"),
        bg="#588F3F",
        fg="white",
        activebackground="#588F3F",
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=submit_signup
    )
    submit_btn.pack(pady=20)


    signup_window.mainloop()