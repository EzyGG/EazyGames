import os
import time
import tkinter as tk

import ezyapi.game_manager as manager
from ezyapi.sessions import User


class LogInFrame(tk.Frame):
    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang

        super().__init__(master, bg=self.theme.login.bg, highlightthickness=self.theme.login.highlightthickness,
                         highlightbackground=self.theme.login.highlightbackground)

        self.label = tk.Label(self, bg=self.theme.login.bg, fg=self.theme.login.fg, height=2, font=("", 30,), text=self.lang.login.label)
        self.label.pack(side="top", pady=30)

        self.user_frame = tk.Frame(self, bg=self.theme.login.bg)
        self.user_name_label = tk.Label(self.user_frame, bg=self.theme.login.bg, fg=self.theme.login.fg, text=self.lang.login.user_name_label)
        self.user_name_label.grid(row=0, column=0, padx=10, pady=20, sticky="e")
        self.user_name_entry = tk.Entry(self.user_frame, bg=self.theme.login.entry_bg, fg=self.theme.login.fg, width=35,
                                        font=("JetBrains Mono", 10))
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=20)
        self.user_pwd_label = tk.Label(self.user_frame, bg=self.theme.login.bg, fg=self.theme.login.fg, text=self.lang.login.user_pwd_label)
        self.user_pwd_label.grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.user_pwd_entry = tk.Entry(self.user_frame, bg=self.theme.login.entry_bg, fg=self.theme.login.fg, width=35, show="*",
                                       font=("JetBrains Mono", 10))
        self.user_pwd_entry.grid(row=1, column=1, padx=10, pady=20)
        self.user_frame.pack(side="top", pady=20)

        self.other_frame = tk.Label(self, bg=self.theme.login.bg)
        self.forgot_pwd_btn = tk.Button(self.other_frame, activebackground=self.theme.login.bg, bg=self.theme.login.bg, fg=self.theme.login.fg,
                                        bd=0, relief="solid", text=self.lang.login.forgot_pwd_btn,
                                        font=("", 10, "underline"), command=lambda: self.forgot_pwd_btn.config(
                text=self.lang.login.not_now))
        self.forgot_pwd_btn.pack(side="left", padx=10)
        self.register_btn = tk.Button(self.other_frame, activebackground=self.theme.login.bg, bg=self.theme.login.bg, fg=self.theme.login.fg,
                                      bd=0, relief="solid", text=self.lang.login.register_btn, font=("", 10, "underline"),
                                      command=self.register_btn)
        self.register_btn.pack(side="left", padx=10)
        self.other_frame.pack(side="top", pady=10)

        self.label = tk.Label(self, bg=self.theme.login.bg, fg=self.theme.login.fg, width=100)
        self.label.pack(side="top", pady=10)
        self.button = tk.Button(self, width=30, height=2, text=self.lang.login.button, activebackground=self.theme.login.bg,
                                bg=self.theme.login.bg, fg=self.theme.login.fg, bd=1, relief="solid", command=self.verify_user)
        self.button.pack(side="top", pady=20)

        self.main.bind("<Return>", lambda e: self.verify_user())

    def show(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)
        self.user_name_entry.focus_set()

    def verify_user(self):
        u = User(self.user_name_entry.get(), self.user_pwd_entry.get())
        self.label.configure(text=(self.lang.globals.connected_as + str(u.get_uuid())) if u.connected() else self.lang.globals.user_not_found,
                             fg="#00ff00" if u.connected() else "#ff0000", font=("", 10, "bold"))
        self.update()
        if u.connected():
            self.main.unbind("<Return>")
            self.main.user = u
            time.sleep(0.5)
            self.destroy()
            try:
                os.mkdir("rsrc/temp")
            except Exception:
                pass
            try:
                manager.import_resource(u.get_uuid(), "profile").save_by_erasing("rsrc/temp", name="profile")
            except Exception:
                pass

            from fr.luzog.ezygg.home import HomeFrame
            HomeFrame(self.main, self.main, self.theme, self.lang).show()

    def register_btn(self):
        self.main.unbind("<Return>")
        self.destroy()
        from fr.luzog.ezygg.register import RegisterFrame
        RegisterFrame(self.main, self.main, self.theme, self.lang).show()
