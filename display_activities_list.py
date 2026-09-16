import tkinter as tk
from tkinter import ttk, messagebox
import enter_screen
from host import Host
from guest import Guest
from add_activity import open_add_activity_screen
from manage_requests import open_manage_requests_screen
from db_config import db


def open_host_info_popup(host_name):
    doc = db.collection("hosts").document(host_name).get()
    if not doc.exists:
        messagebox.showerror("Error", f"Host '{host_name}' not found.")
        return

    data = doc.to_dict()
    is_vegan = "Yes" if data.get("is_vegan") else "No"
    is_vegetarian = "Yes" if data.get("is_vegetarian") else "No"
    is_religious = "Yes" if data.get("is_religious") else "No"
    bio = data.get("bio", "No bio provided.")

    info_text = (
        f"Host Name: {host_name}\n"
        f"Vegan: {is_vegan}\n"
        f"Vegetarian: {is_vegetarian}\n"
        f"Religious: {is_religious}\n"
        f"Bio: {bio}"
    )

    messagebox.showinfo(f"Host Profile", info_text)


def open_host_details_popup(host_name):
    doc = db.collection("hosts").document(host_name).get()
    if not doc.exists:
        messagebox.showerror("Error", "Host details not found.")
        return

    data = doc.to_dict()
    phone = data.get("phone", "N/A")
    address = data.get("address", "N/A")

    messagebox.showinfo(
        "Host Contact Details",
        f"Host Name: {host_name}\nPhone: {phone}\nAddress: {address}"
    )


def open_print_list_screen(items_list):
    window = tk.Tk()
    window.title("Open Home")
    window.geometry("580x520")
    window.configure(bg="#9AF075")

    header_frame = tk.Frame(window, bg="#9AF075")
    header_frame.pack(fill="x", padx=20, pady=10)

    title_label = tk.Label(
        header_frame,
        text="Open Activities",
        font=("Arial", 16, "bold"),
        bg="#9AF075",
        fg="#1a365d"
    )
    title_label.pack(side="left")

    container = tk.Frame(window, bg="#9AF075")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(container, bg="#9AF075", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#9AF075")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def register_guest_to_activity(activity_doc_id):
        if not hasattr(enter_screen, 'user') or not enter_screen.user:
            messagebox.showerror("Error", "No user logged in!")
            return

        if not activity_doc_id:
            messagebox.showerror("Error", "Activity ID is missing!")
            return

        guest_name = enter_screen.user.name
        doc_ref = db.collection("activities").document(activity_doc_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            pending_list = data.get("pending_guests", [])
            approved_list = data.get("approved_guests", [])
            rejected_list = data.get("rejected_guests", [])

            if guest_name in pending_list or guest_name in approved_list or guest_name in rejected_list:
                return

            pending_list.append(guest_name)
            doc_ref.update({"pending_guests": pending_list})

            # messagebox.showinfo("Success", "Request sent! Status: Pending")
            fetch_and_reload_all()

    def populate_list(current_items):
        for child in scrollable_frame.winfo_children():
            child.destroy()

        if not current_items:
            tk.Label(
                scrollable_frame,
                text="No activities available.",
                font=("Arial", 11, "italic"),
                bg="#9AF075",
                fg="#718096"
            ).pack(pady=20)
            return

        current_user_name = enter_screen.user.name if hasattr(enter_screen, 'user') and enter_screen.user else ""

        for item in current_items:
            card = tk.Frame(scrollable_frame, bg="#EDEBC2", bd=1, relief="solid", padx=15, pady=10)
            card.pack(fill="x", expand=True, pady=8)

            act_type = item.get("type of activity", "N/A")
            people = item.get("amount of people", "N/A")
            date = item.get("date", "N/A")
            host_name = item.get("host_name", "")

            doc_id = item.get("doc_id") or item.get("host_name") or ""

            pending_guests = item.get("pending_guests", [])
            approved_guests = item.get("approved_guests", [])
            rejected_guests = item.get("rejected_guests", [])

            details_text = f"Host: {host_name}\nType: {act_type}\nDate: {date}\nMax People: {people}"
            tk.Label(
                card,
                text=details_text,
                font=("Arial", 10),
                bg="#EDEBC2",
                justify="left"
            ).pack(side="left")

            buttons_frame = tk.Frame(card, bg="#EDEBC2")
            buttons_frame.pack(side="right", padx=5)

            if hasattr(enter_screen, 'user') and isinstance(enter_screen.user, Guest):
                if current_user_name in approved_guests:
                    join_btn = tk.Button(
                        buttons_frame,
                        text="Approved",
                        bg="#38a169",
                        fg="white",
                        font=("Arial", 9, "bold"),
                        bd=0,
                        cursor="hand2",
                        command=lambda h=host_name: open_host_details_popup(h)
                    )
                elif current_user_name in pending_guests:
                    join_btn = tk.Button(
                        buttons_frame,
                        text="Pending",
                        state="disabled",
                        bg="#a0aec0",
                        fg="white",
                        font=("Arial", 9, "bold"),
                        bd=0
                    )
                elif current_user_name in rejected_guests:
                    join_btn = tk.Button(
                        buttons_frame,
                        text="Rejected",
                        bg="#e53e3e",
                        fg="white",
                        font=("Arial", 9, "bold"),
                        bd=0,
                        cursor="hand2",
                        command=lambda: messagebox.showinfo(
                            "Request Status",
                            "Sorry, there was no match for this activity this time."
                        )
                    )
                else:
                    join_btn = tk.Button(
                        buttons_frame,
                        text="Join Activity",
                        bg="#319795",
                        fg="white",
                        font=("Arial", 9, "bold"),
                        bd=0,
                        cursor="hand2",
                        command=lambda target_id=doc_id: register_guest_to_activity(target_id)
                    )

                join_btn.pack(side="top", fill="x", pady=2)

                host_info_btn = tk.Button(
                    buttons_frame,
                    text="Host Info",
                    bg="#4a5568",
                    fg="white",
                    font=("Arial", 8, "bold"),
                    bd=0,
                    cursor="hand2",
                    command=lambda h=host_name: open_host_info_popup(h)
                )
                host_info_btn.pack(side="top", fill="x", pady=2)

            elif hasattr(enter_screen, 'user') and isinstance(enter_screen.user, Host):
                manage_btn = tk.Button(
                    buttons_frame,
                    text=f"Manage ({len(pending_guests)})",
                    bg="#2b6cb0",
                    fg="white",
                    font=("Arial", 9, "bold"),
                    bd=0,
                    cursor="hand2",
                    command=lambda target_id=doc_id: open_manage_requests_screen(
                        target_id,
                        refresh_callback=fetch_and_reload_all
                    )
                )
                manage_btn.pack(side="top", fill="x", pady=2)

    def fetch_and_reload_all():
        if hasattr(enter_screen, 'user') and isinstance(enter_screen.user, Guest):
            docs = db.collection("activities").stream()
            updated_list = []
            for doc in docs:
                data = doc.to_dict()
                data['doc_id'] = doc.id
                updated_list.append(data)
            populate_list(updated_list)

        elif hasattr(enter_screen, 'user') and isinstance(enter_screen.user, Host):
            docs = db.collection("activities").where("host_name", "==", enter_screen.user.name).stream()
            updated_list = []
            for doc in docs:
                data = doc.to_dict()
                data['doc_id'] = doc.id
                updated_list.append(data)
            populate_list(updated_list)

    fetch_and_reload_all()

    if hasattr(enter_screen, 'user') and isinstance(enter_screen.user, Host):
        plus_btn = tk.Button(
            header_frame,
            text="+",
            font=("Arial", 14, "bold"),
            bg="#319795",
            fg="white",
            width=3,
            bd=0,
            cursor="hand2",
            command=lambda: open_add_activity_screen(refresh_callback=fetch_and_reload_all)
        )
        plus_btn.pack(side="right")

    window.mainloop()