import time
import tkinter as tk
# import tkinter.filedialog as tk_file_dialog
from sessions import User


class Home(tk.Tk):
    def __init__(self):
        self.bg_color = "gray"
        self.bg2_color = "dim gray"

        super().__init__("EzyGames", "EzyGames")
        self.title("EzyGames")
        self.geometry("1080x720")
        self.iconbitmap("rsrc/icon.ico")
        self.configure(background="gray", highlightthickness=16)
        self.connexion()

    def home(self):
        pass

    def connexion(self):
        self.connection_frame = tk.Frame(self, bg=self.bg2_color, highlightthickness=2, highlightbackground="black")
        self.label = tk.Label(self.connection_frame, bg=self.bg2_color, height=2, font=("", 30,), text="Connexion")
        self.label.pack(side="top", pady=30)

        self.connection_user_frame = tk.Frame(self.connection_frame, bg=self.bg2_color)
        self.connection_user_name_label = tk.Label(self.connection_user_frame, bg=self.bg2_color, text="Username :")
        self.connection_user_name_label.grid(row=0, column=0, padx=10, pady=20)
        self.connection_user_name_entry = tk.Entry(self.connection_user_frame, bg=self.bg_color, width=35, font=("JetBrains Mono", 10))
        self.connection_user_name_entry.grid(row=0, column=1, padx=10, pady=20)
        self.connection_user_pwd_label = tk.Label(self.connection_user_frame, bg=self.bg2_color, text="Password :")
        self.connection_user_pwd_label.grid(row=1, column=0, padx=10, pady=20)
        self.connection_user_pwd_entry = tk.Entry(self.connection_user_frame, bg=self.bg_color, width=35, show="*", font=("JetBrains Mono", 10))
        self.connection_user_pwd_entry.grid(row=1, column=1, padx=10, pady=20)
        self.connection_user_frame.pack(side="top", pady=20)

        self.label = tk.Label(self.connection_frame, bg=self.bg2_color, width=100)
        self.label.pack(side="top", pady=20)
        self.button = tk.Button(self.connection_frame, width=30, height=2, text="Verifier", command=self.verify_user)
        self.button.pack(side="top", pady=20)

        self.bind("<KeyPress>", lambda e: self.verify_user() if e.char == "\r" else None)
        self.connection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)

    def verify_user(self):
        u = User(self.connection_user_name_entry.get(), self.connection_user_pwd_entry.get())
        self.label.configure(text=("Connected with " + str(u.get_uuid())) if u.exists() else "User Not Found.",
                             fg="#00ff00" if u.exists() else "#ff0000", font=("", 10, "bold"))
        self.update()
        if u.exists():
            self.unbind("<KeyPress>")
            time.sleep(1)
            self.connection_frame.destroy()
            self.home()

    def start(self):
        self.mainloop()
        return self

    def stop(self):
        self.destroy()
        return self
