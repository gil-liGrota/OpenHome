import tkinter as tk
from tkinter import messagebox
from db_config import db


def open_guest_info_popup(guest_name):
    doc = db.collection("guests").document(guest_name).get()
    if not doc.exists:
        messagebox.showerror("Error", f"Details for guest '{guest_name}' not found.")
        return

    data = doc.to_dict()
    name = guest_name
    phone = data.get("phone", "N/A")
    address = data.get("address", "N/A")
    allergies = data.get("allergies", "None")
    is_vegan = "Yes" if data.get("is_vegan") else "No"
    is_vegetarian = "Yes" if data.get("is_vegetarian") else "No"
    is_religious = "Yes" if data.get("is_religious") else "No"
    bio = data.get("bio", "No bio provided.")

    info_text = (
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Address: {address}\n"
        f"Allergies: {allergies}\n"
        f"Vegan: {is_vegan}\n"
        f"Vegetarian: {is_vegetarian}\n"
        f"Religious: {is_religious}\n"
        f"Bio: {bio}"
    )

    messagebox.showinfo(f"Guest Info", info_text)


def open_manage_requests_screen(activity_doc_id, refresh_callback=None):
    win = tk.Toplevel()
    win.title("Manage Activity Requests")
    win.geometry("480x520")
    win.configure(bg="#9AF075")

    tk.Label(
        win,
        text="Guests & Requests Status",
        font=("Arial", 14, "bold"),
        bg="#9AF075",
        fg="#1a365d"
    ).pack(pady=15)

    list_frame = tk.Frame(win, bg="#9AF075")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def load_requests():
        for child in list_frame.winfo_children():
            child.destroy()

        doc_ref = db.collection("activities").document(activity_doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            return

        data = doc.to_dict()
        pending_list = data.get("pending_guests", [])
        approved_list = data.get("approved_guests", [])

        if not pending_list and not approved_list:
            tk.Label(
                list_frame,
                text="No guests or pending requests yet.",
                font=("Arial", 10, "italic"),
                bg="#f0f4f8",
                fg="#718096"
            ).pack(pady=20)
            return

        for guest_name in pending_list:
            card = tk.Frame(list_frame, bg="white", bd=1, relief="solid", padx=10, pady=5)
            card.pack(fill="x", pady=5)

            name_btn = tk.Button(
                card,
                text=f"{guest_name} (Pending i)",
                font=("Arial", 10, "bold"),
                bg="white",
                bd=0,
                fg="#1a365d",
                cursor="hand2",
                command=lambda g=guest_name: open_guest_info_popup(g)
            )
            name_btn.pack(side="left")

            reject_btn = tk.Button(
                card,
                text="Reject",
                bg="#e53e3e",
                fg="white",
                font=("Arial", 9, "bold"),
                bd=0,
                cursor="hand2",
                command=lambda g=guest_name: handle_response(g, action="reject")
            )
            reject_btn.pack(side="right", padx=3)

            approve_btn = tk.Button(
                card,
                text="Approve",
                bg="#38a169",
                fg="white",
                font=("Arial", 9, "bold"),
                bd=0,
                cursor="hand2",
                command=lambda g=guest_name: handle_response(g, action="approve")
            )
            approve_btn.pack(side="right", padx=3)

        for guest_name in approved_list:
            card = tk.Frame(list_frame, bg="#e6fffa", bd=1, relief="solid", padx=10, pady=5)
            card.pack(fill="x", pady=5)

            name_btn = tk.Button(
                card,
                text=f"{guest_name} i",
                font=("Arial", 10, "bold"),
                bg="#e6fffa",
                bd=0,
                fg="#234e52",
                cursor="hand2",
                command=lambda g=guest_name: open_guest_info_popup(g)
            )
            name_btn.pack(side="left")

            tk.Label(card, text="Approved", font=("Arial", 9, "bold"), fg="#2f855a", bg="#e6fffa").pack(side="right", padx=5)

    def handle_response(guest_name, action):
        doc_ref = db.collection("activities").document(activity_doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            return

        data = doc.to_dict()
        pending_list = data.get("pending_guests", [])
        approved_list = data.get("approved_guests", [])
        rejected_list = data.get("rejected_guests", [])

        if guest_name in pending_list:
            pending_list.remove(guest_name)

        if action == "approve":
            if guest_name not in approved_list:
                approved_list.append(guest_name)
            # messagebox.showinfo("Success", f"{guest_name} approved!")
        elif action == "reject":
            if guest_name not in rejected_list:
                rejected_list.append(guest_name)
            # messagebox.showinfo("Notice", f"{guest_name} was set to Rejected.")

        doc_ref.update({
            "pending_guests": pending_list,
            "approved_guests": approved_list,
            "rejected_guests": rejected_list
        })

        load_requests()
        if refresh_callback:
            refresh_callback()

    load_requests()