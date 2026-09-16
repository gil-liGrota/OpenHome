import tkinter as tk
from sign_up import open_signup_screen
from log_in import open_login_screen
from PIL import Image, ImageTk

global user


def create_welcome_screen():
    root = tk.Tk()
    root.title("Open Home - Welcome")
    root.geometry("750x700")
    root.configure(bg="#9AF075")




    welcome_label = tk.Label(
        root,
        text="Welcome to - Open Home",
        font=("Arial", 20, "bold"),
        bg="#9AF075",
        fg="#1a365d"
    )
    welcome_label.pack(pady=10)

    subtitle_label = tk.Label(
        root,
        text="Please log in or sign up to continue",
        font=("Arial", 11),
        bg="#9AF075",
        fg="#4a5568"
    )
    subtitle_label.pack(pady=5)
    img = Image.open("openImg.png")
    resized_image = img.resize((200, 275))
    img = ImageTk.PhotoImage(resized_image)


    panel = tk.Label(root, image=img)
    panel.pack(fill="both")
    panel.configure(bg="#9AF075")





    tk.Frame(root, bg="#9AF075", height=40).pack()
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
        bg="#588F3F",
        fg="white",
        activebackground="#588F3F",
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
        bg="#588F3F",
        fg="white",
        activebackground="#588F3F",
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=on_signup
    )
    signup_btn.pack(pady=10)

    root.mainloop()