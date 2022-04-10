import time
import tkinter as tk

from ezyapi.sessions import User, UserAlreadyExistsException


class RegisterFrame(tk.Frame):
    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang

        super().__init__(master, bg=self.theme.register.bg, highlightthickness=self.theme.register.highlightthickness,
                         highlightbackground=self.theme.register.highlightbackground)

        self.title = tk.Label(self, bg=self.theme.register.bg, fg=self.theme.register.c_normal, height=1, font=("", 30,), text=self.lang.register.label)
        self.title.pack(side="top", pady=20)

        self.user_frame = tk.Frame(self, bg=self.theme.register.bg, height=300, width=650)

        self.user_name_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.user_name_label)
        self.user_name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.user_name_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=28, font=self.theme.register.f_mono)
        self.user_name_entry.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

        tk.Frame(self.user_frame, bg=self.theme.register.bg).grid(row=1, column=0, columnspan=4, pady=10)

        self.complete_last_name_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.complete_last_name_label)
        self.complete_last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.complete_last_name_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=20,
                                                 font=self.theme.register.f_mono)
        self.complete_last_name_entry.grid(row=2, column=1, padx=5, pady=5)

        self.complete_first_name_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.complete_first_name_label)
        self.complete_first_name_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.complete_first_name_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=20,
                                                  font=self.theme.register.f_mono)
        self.complete_first_name_entry.grid(row=2, column=3, padx=5, pady=5)

        self.mail_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.mail_label)
        self.mail_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.mail_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=50, font=self.theme.register.f_mono)
        self.mail_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        tk.Frame(self.user_frame, bg=self.theme.register.bg).grid(row=4, column=0, columnspan=4, pady=10)

        self.lvl = tk.Frame(self.user_frame, height=5, width=226)
        self.lvl.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

        self.pwd_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.pwd_label)
        self.pwd_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.pwd_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=28, font=self.theme.register.f_mono, show="*")
        self.pwd_entry.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

        self.vpwd_label = tk.Label(self.user_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.vpwd_label)
        self.vpwd_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.vpwd_entry = tk.Entry(self.user_frame, bg=self.theme.register.entry_bg, fg=self.theme.register.c_normal, width=28, font=self.theme.register.f_mono, show="*")
        self.vpwd_entry.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

        self.user_frame.pack(side="top", pady=25)

        self.other_frame = tk.Label(self, bg=self.theme.register.bg)
        self.login_label = tk.Label(self.other_frame, bg=self.theme.register.bg, fg=self.theme.register.c_normal, text=self.lang.register.login_label)
        self.login_label.pack(side="left", padx=10)
        self.login_btn = tk.Button(self.other_frame, activebackground=self.theme.register.bg, bg=self.theme.register.bg, fg=self.theme.register.c_normal,
                                   bd=0, relief="solid", text=self.lang.register.login_btn, font=("", 10, "underline"),
                                   command=self.login)
        self.login_btn.pack(side="left", padx=10)
        self.other_frame.pack(side="top", pady=10)

        self.label = tk.Label(self, bg=self.theme.register.bg, fg=self.theme.register.c_normal, width=100)
        self.label.pack(side="top", pady=5)
        self.button = tk.Button(self, width=30, height=2, text=self.lang.register.button, activebackground=self.theme.register.bg,
                                bg=self.theme.register.bg, fg=self.theme.register.c_normal, bd=1, relief="solid", command=self.validate)
        self.button.pack(side="top", pady=5)

        self.master.bind("<Return>", self.validate)
        self.master.bind("<KeyPress>", self.key_press)

        self.errors, self.warns = [], []

        self.key_press()

    @staticmethod
    def score(key: str) -> float:
        alphal = 0
        alphau = 0
        num = 0
        spe = 0
        other = 0
        for c in key:
            if c in "abcdefghijklmnopqrstuvwxyz":
                alphal += 1
            elif c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                alphau += 1
            elif c in "1234567890":
                num += 1
            elif c in "&\"'(-_)=$*!:;,<>?./%£€+°#{[@]}":
                spe += 1
            else:
                other += 1
        return alphal ** 0.79 + alphau ** 0.79 + num ** 0.79 + spe ** 0.79 + other ** 0.79 - (
            0.999 if 0 < len(key) < 5 else 0)

    def show(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)
        self.user_name_entry.focus_set()

    def login(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Return>")
        self.destroy()

        from fr.luzog.ezygg.login import LogInFrame
        LogInFrame(self.main, self.main, self.theme, self.lang).show()

    def key_press(self, e=None):
        self.errors, self.warns = [], []

        if not self.user_name_entry.get():
            self.user_name_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
            self.errors.append(self.lang.register.error_username_expected)
        elif len(self.user_name_entry.get()) < 5:
            self.user_name_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
            self.errors.append(self.lang.register.error_username_too_short)
        else:
            has_spe = False
            for c in self.user_name_entry.get().lower():
                if c not in "abcdefghijklmnopqrstuvwxyz0123456789-._":
                    has_spe = True
                    break
            if has_spe:
                self.user_name_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
                self.errors.append(self.lang.register.error_username_must_respect + " 'abcdefghijklmnopqrstuvwxyz0123456789-._'")
            elif self.user_name_entry.get() != self.user_name_entry.get().lower():
                self.user_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_warn)
                self.warns.append(self.lang.register.warn_username_case)
            else:
                self.user_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)

        if not self.complete_last_name_entry.get():
            self.complete_last_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal)
        else:
            self.complete_last_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)

        if not self.complete_first_name_entry.get():
            self.complete_first_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal)
        else:
            self.complete_first_name_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)

        if not self.mail_entry.get():
            self.mail_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal)
        elif "GENERAL" and (self.mail_entry.get().count("@") == 1 and ".." not in self.mail_entry.get()) \
                and "LOCAL PART" \
                and (
                    6 <= len(self.mail_entry.get().split("@")[0]) <= 30
                    and not [True for c in self.mail_entry.get().split("@")[0].lower()
                             if c not in "abcdefghijklmnopqrstuvwxyz0123456789-."]
                    and self.mail_entry.get().split("@")[0][0] not in "-."
                    and self.mail_entry.get().split("@")[0][-1] not in "-."
                ) \
                and "DOMAIN PART" \
                and ((not "CLASSIC DOMAIN") or (
                    self.mail_entry.get().split("@")[1].count(".") == 1
                    and 1 <= len(self.mail_entry.get().split("@")[1].split(".")[0]) <= 67
                    and 1 <= len(self.mail_entry.get().split("@")[1].split(".")[1]) <= 63
                    and not [True for c in self.mail_entry.get().split("@")[1].lower()
                             if c not in "abcdefghijklmnopqrstuvwxyz0123456789-."]
                    and "-" not in [self.mail_entry.get().split("@")[1].split(".")[0][0],
                                    self.mail_entry.get().split("@")[1].split(".")[0][-1],
                                    self.mail_entry.get().split("@")[1].split(".")[1][0],
                                    self.mail_entry.get().split("@")[1].split(".")[1][-1]]
                ) or (not "IPv4") or (
                    self.mail_entry.get().split("@")[1].count(".") == 3
                    and self.mail_entry.get().split("@")[1].count("[") == 1
                    and self.mail_entry.get().split("@")[1].startswith("[")
                    and self.mail_entry.get().split("@")[1].count("]") == 1
                    and self.mail_entry.get().split("@")[1].endswith("]")
                    and not [True for c in self.mail_entry.get().split("@")[1].lower() if c not in "0123456789.[]"]
                    and len(self.mail_entry.get().split("@")[1][1:-1].split(".")[0])
                    and int(self.mail_entry.get().split("@")[1][1:-1].split(".")[0]) <= 255
                    and len(self.mail_entry.get().split("@")[1][1:-1].split(".")[1])
                    and int(self.mail_entry.get().split("@")[1][1:-1].split(".")[1]) <= 255
                    and len(self.mail_entry.get().split("@")[1][1:-1].split(".")[2])
                    and int(self.mail_entry.get().split("@")[1][1:-1].split(".")[2]) <= 255
                    and len(self.mail_entry.get().split("@")[1][1:-1].split(".")[3])
                    and int(self.mail_entry.get().split("@")[1][1:-1].split(".")[3]) <= 255
                ) or (not "IPv6") or (
                    self.mail_entry.get().split("@")[1].count(":") == 8
                    and self.mail_entry.get().split("@")[1].lower().count("[") == 1
                    and self.mail_entry.get().split("@")[1].lower().count("ipv6:") == 1
                    and self.mail_entry.get().split("@")[1].lower().startswith("[ipv6:")
                    and self.mail_entry.get().split("@")[1].count("]") == 1
                    and self.mail_entry.get().split("@")[1].endswith("]")
                    and not [True for c in self.mail_entry.get().split("@")[1][6:-1].lower()
                             if c not in "abcdef0123456789:"]
                    and not [True for i in self.mail_entry.get().split("@")[1][6:-1].lower().split(":")
                             if i and (int(i, 16) < 0 or int(i, 16) > 65535)]
                )):
            self.mail_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)
        else:
            self.mail_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
            self.errors.append(self.lang.register.error_mail_invalid)

        if not self.pwd_entry.get() and not self.vpwd_entry.get():
            self.pwd_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal)
            self.vpwd_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal)
        elif self.pwd_entry.get() == self.vpwd_entry.get():
            self.pwd_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)
            self.vpwd_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_special)
            if self.score(self.pwd_entry.get()) < 6:
                self.pwd_label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_warn)
                self.warns.append(self.lang.register.warn_password_too_simple)
        else:
            self.pwd_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
            self.vpwd_label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error)
            self.errors.append(self.lang.register.error_password_dont_match)

        if self.score(self.pwd_entry.get()) == 0:
            self.lvl.config(bg=self.theme.register.C_0)
        elif self.score(self.pwd_entry.get()) < 4:
            self.lvl.config(bg=self.theme.register.C_1)
        elif self.score(self.pwd_entry.get()) < 6:
            self.lvl.config(bg=self.theme.register.C_2)
        elif self.score(self.pwd_entry.get()) < 7.85:
            self.lvl.config(bg=self.theme.register.C_3)
        elif self.score(self.pwd_entry.get()) < 10:
            self.lvl.config(bg=self.theme.register.C_4)
        elif self.score(self.pwd_entry.get()) < 12:
            self.lvl.config(bg=self.theme.register.C_5)
        elif self.score(self.pwd_entry.get()) < 16:
            self.lvl.config(bg=self.theme.register.C_6)
        elif self.score(self.pwd_entry.get()) < 20:
            self.lvl.config(bg=self.theme.register.C_7)
        elif self.score(self.pwd_entry.get()) < 25:
            self.lvl.config(bg=self.theme.register.C_8)
        elif self.score(self.pwd_entry.get()) < 30:
            self.lvl.config(bg=self.theme.register.C_9)
        else:
            self.lvl.config(bg=self.theme.register.C_10)

        if len(self.errors):
            self.label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error, text=self.lang.register.errors + " " + " ; ".join(self.errors))
        elif len(self.warns):
            self.label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_warn, text=self.lang.register.warns + " " + " ; ".join(self.warns))
        else:
            self.label.config(font=self.theme.register.f_normal, fg=self.theme.register.c_normal, text="")

    def validate(self, e=None):
        if len(self.errors):
            return
        try:
            u = User.create_user(username=self.user_name_entry.get(), completename=(self.complete_first_name_entry.get()
                                                                                    + " " + self.complete_last_name_entry.get()),
                                 mail=None if self.mail_entry.get() == ""
                                 else self.mail_entry.get(), password=self.pwd_entry.get())
        except UserAlreadyExistsException:
            self.label.config(font=self.theme.register.f_modify, fg=self.theme.register.c_error, text=self.lang.register.error_user_already_exists)
            return
        self.label.configure(text=(self.lang.globals.connected_as + str(u.get_uuid())) if u.connected() else self.lang.globals.user_not_found,
                             fg="#00ff00" if u.connected() else "#ff0000", font=("", 10, "bold"))
        self.update()
        if u.connected():
            self.master.unbind("<KeyPress>")
            self.master.unbind("<Return>")
            self.master.user = u
            time.sleep(0.5)
            self.destroy()
            from fr.luzog.ezygg.home import HomeFrame
            HomeFrame(self.main, self.main, self.theme, self.lang).show()
