import tkinter as tk
from sign_up import open_signup_screen
from log_in import open_login_screen

global user

def create_welcome_screen():
    root = tk.Tk()
    root.title("Open Home - Welcome")
    root.geometry("450x400")
    root.configure(bg="#f0f4f8")

    tk.Frame(root, bg="#f0f4f8", height=40).pack()

    welcome_label = tk.Label(
        root,
        text="Welcome to - Open Home",
        font=("Arial", 20, "bold"),
        bg="#f0f4f8",
        fg="#1a365d"
    )
    welcome_label.pack(pady=10)

    subtitle_label = tk.Label(
        root,
        text="Please log in or sign up to continue",
        font=("Arial", 11),
        bg="#f0f4f8",
        fg="#4a5568"
    )
    subtitle_label.pack(pady=5)

    def on_login():
        root.destroy()
        open_login_screen()

    def on_signup():
        root.destroy()
        open_signup_screen()

    login_btn = tk.Button(
        root,
        text="Log In",
        font=("Arial", 12, "bold"),
        bg="#2b6cb0",
        fg="white",
        activebackground="#2c5282",
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=on_login
    )
    login_btn.pack(pady=15)

    signup_btn = tk.Button(
        root,
        text="Sign Up",
        font=("Arial", 12, "bold"),
        bg="#319795",
        fg="white",
        activebackground="#2c7a7b",
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=on_signup
    )
    signup_btn.pack(pady=10)

    root.mainloop()