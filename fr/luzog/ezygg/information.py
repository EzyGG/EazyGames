import tkinter as tk
from PIL import Image as Image, ImageTk


class Information(tk.Frame):
    FACE_IMG_SIZE = (96, 96)

    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang

        super().__init__(master, background=self.theme.information.bg)
        self.spacing = 5

        tk.Frame(self, bg=self.theme.information.bg).pack(pady=35)

        try:
            self.img = Image.open("rsrc/temp/profile.png")
        except Exception:
            self.img = Image.open("/rsrc/default_face.png")
        _, _, width, height = self.img.getbbox()
        if width > self.FACE_IMG_SIZE[0] or height > self.FACE_IMG_SIZE[1]:
            if width - self.FACE_IMG_SIZE[0] > height - self.FACE_IMG_SIZE[1]:
                final_geometry = (self.FACE_IMG_SIZE[0], int((self.FACE_IMG_SIZE[0] / width) * height))
            else:
                final_geometry = (int((self.FACE_IMG_SIZE[1] / height) * width), self.FACE_IMG_SIZE[1])
            self.img = self.img.resize(final_geometry, Image.ANTIALIAS)
        _img = ImageTk.PhotoImage(self.img)
        self.face_img = tk.Label(self, bg=self.theme.information.bg, image=_img, height=self.FACE_IMG_SIZE[1],
                                 width=self.FACE_IMG_SIZE[0])
        self.face_img.image = _img
        self.face_img.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.complete_name_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                           font=self.theme.information.f_label, text=self.lang.information.completename)
        self.complete_name_info.pack(anchor="e")
        self.complete_name = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                                      text=self.main.user.get_completename())
        self.complete_name.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.user_name_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                       font=self.theme.information.f_label, text=self.lang.information.identifier)
        self.user_name_info.pack(anchor="e")
        self.user_name = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                                  text=self.main.user.get_username())
        self.user_name.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.mail_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                  font=self.theme.information.f_label, text=self.lang.information.mail)
        self.mail_info.pack(anchor="e")
        self.mail = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                             text=self.main.user.get_mail())
        self.mail.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.creation_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                      font=self.theme.information.f_label, text=self.lang.information.creation)
        self.creation_info.pack(anchor="e")
        self.creation = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                                 text=self.main.user.get_creation())
        self.creation.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        # self.uuid_info = tk.Label(self, bg=Center.COLOR_BG2, font=self.theme.information.f_label, text="UUID :")
        # self.uuid_info.pack(anchor="e")
        # self.uuid = tk.Label(self, bg=Center.COLOR_BG2, font=("", 7, "bold"), text=self.main.user.get_uuid())
        # self.uuid.pack(anchor="e")
        # tk.Frame(self, bg=Center.COLOR_BG2).pack(pady=self.spacing)

        tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label, text="---").pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.lvl_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                 font=self.theme.information.f_label, text=self.lang.information.lvl)
        self.lvl_info.pack(anchor="e")
        self.lvl = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                            text=self.main.user.get_lvl())
        self.lvl.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.exp_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                 font=self.theme.information.f_label, text=self.lang.information.exp)
        self.exp_info.pack(anchor="e")
        self.exp = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                            text=self.main.user.get_exp())
        self.exp.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.gp_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                font=self.theme.information.f_label, text=self.lang.information.gp)
        self.gp_info.pack(anchor="e")
        self.gp = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                           text=self.main.user.get_gp())
        self.gp.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.ratio_info = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label,
                                   font=self.theme.information.f_label, text=self.lang.information.sets)
        self.ratio_info.pack(anchor="e")
        self.ratio = tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_text,
                              text=str(self.main.user.get_total_wins())
                                                            + " / " + str(
            self.main.user.get_played_games()))
        self.ratio.pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        tk.Label(self, bg=self.theme.information.bg, fg=self.theme.information.fg_label, text="---").pack(anchor="e")
        tk.Frame(self, bg=self.theme.information.bg).pack(pady=self.spacing)

        self.settings_frame = tk.Frame(self, bg=self.theme.information.bg)
        self.settings_frame.pack(pady=self.spacing, side="bottom")
        self.more_button = tk.Button(self.settings_frame, activebackground=self.theme.information.bg,
                                     bg=self.theme.information.bg, fg=self.theme.information.fg_btn,
                                     bd=1, relief="solid", width=10, text=self.lang.information.more, command=lambda:
            self.more_button.configure(text=self.lang.information.not_now))
        self.more_button.pack(side="left")
        self.logout_button = tk.Button(self.settings_frame, activebackground=self.theme.information.bg,
                                       bg=self.theme.information.bg, fg=self.theme.information.fg_btn,
                                       bd=1, relief="solid", width=10, text=self.lang.information.logout,
                                       command=self.main.restart)
        self.logout_button.pack(side="right", padx=8)

    def show(self):
        self.place(relx=1, rely=1, anchor="se", height=self.main.winfo_height(),
                   width=self.main.winfo_width() * 17 / 100)

    def update_place(self):
        self.place_configure(relx=1, rely=1, anchor="se", height=self.main.winfo_height(),
                             width=self.main.winfo_width() * 17 / 100)
