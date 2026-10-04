import tkinter as tk

import activity_constant
from activity_constant import BG_COLOR
from sign_up import open_signup_screen
from log_in import open_login_screen
from PIL import Image, ImageTk

global user


def create_welcome_screen():
    root = tk.Tk()
    root.title("Open Home - Welcome")
    root.geometry("450x400")
    root.configure(bg=activity_constant.BG_COLOR)




    welcome_label = tk.Label(
        root,
        text="Welcome to - Open Home",
        font=("Arial", 20, "bold"),
        bg=activity_constant.BG_COLOR,
        fg="#1a365d"
    )
    welcome_label.pack(pady=10)

    subtitle_label = tk.Label(
        root,
        text="Please log in or sign up to continue",
        font=("Arial", 11),
        bg=activity_constant.BG_COLOR,
        fg="#4a5568"
    )


    tk.Frame(root, bg=activity_constant.BG_COLOR, height=40).pack()
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
        bg=activity_constant.COLOR,
        fg="white",
        activebackground=activity_constant.COLOR,
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
        bg=activity_constant.COLOR,
        fg="white",
        activebackground=activity_constant.COLOR,
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=on_signup
    )
    signup_btn.pack(pady=10)

    root.mainloop()