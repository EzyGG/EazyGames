import pyperclip
import tkinter as tk
from enum import Enum
from PIL import Image as Image, ImageTk

from ezyapi.sessions import User

from fr.luzog.ezygg.consts import Theme, Lang


class ContentType(Enum):
    NONE = 0
    LABEL = 1
    ENTRY_UNLOCKED = 2
    ENTRY_LOCKED = 3
    TEXT_UNLOCKED = 4
    TEXT_LOCKED = 5
    TEXT_1L_UNLOCKED = 6
    TEXT_1L_LOCKED = 7
    TEXT_3L_UNLOCKED = 8
    TEXT_3L_LOCKED = 9
    TEXT_8L_UNLOCKED = 10
    TEXT_8L_LOCKED = 11
    TEXT_12L_UNLOCKED = 12
    TEXT_12L_LOCKED = 13
    TEXT_16L_UNLOCKED = 14
    TEXT_16L_LOCKED = 15
    TEXT_20L_UNLOCKED = 16
    TEXT_20L_LOCKED = 17


class InfoItem(tk.Frame):
    def __init__(self, master, width: int, padx: int, pady: int, bg_global: str, bg_content: str,
                 label_text: str, label_color: str, label_font: tuple[str, int, str],
                 content_type: ContentType, content_text: str, content_color: str, content_font: tuple[str, int, str],
                 btn_text: str, btn_color: str, btn_font: tuple[str, int, str], btn_bd: int,
                 on_click, args: tuple | list = (), kwargs: dict = {}):
        self.width = width
        self.padx = padx
        self.pady = pady
        self.bg_global = bg_global
        self.bg_content = bg_content
        self.label_text = label_text
        self.label_color = label_color
        self.label_font = label_font
        self.content_type = content_type
        self.content_text = content_text
        self.content_color = content_color
        self.content_font = content_font
        self.btn_text = btn_text
        self.btn_color = btn_color
        self.btn_font = btn_font
        self.btn_bd = btn_bd
        self.on_click = on_click
        self.args = args
        self.kwargs = kwargs

        super().__init__(master, background=self.bg_global)

        # This frame is here, just to fix the width (expand doesn't work)
        tk.Frame(self, bg=self.bg_global, height=1, width=self.width - self.padx).pack()

        self.label = tk.Label(self, bg=self.bg_global, fg=self.label_color, font=self.label_font, text=self.label_text)
        self.label.pack(anchor="w", padx=10, pady=5)

        cont_params = {"bg": self.bg_content, "fg": self.content_color, "font": self.content_font}
        self.content: tk.Label | tk.Text | tk.Entry | None = None
        if self.content_type in [ContentType.LABEL]:
            self.content = tk.Label(self, **cont_params, text=self.content_text)
            self.content.pack(expand=True, fill="x", padx=10, pady=5)

        elif self.content_type in [ContentType.TEXT_UNLOCKED, ContentType.TEXT_LOCKED,
                                   ContentType.TEXT_1L_UNLOCKED, ContentType.TEXT_1L_LOCKED,
                                   ContentType.TEXT_3L_UNLOCKED, ContentType.TEXT_3L_LOCKED,
                                   ContentType.TEXT_8L_UNLOCKED, ContentType.TEXT_8L_LOCKED,
                                   ContentType.TEXT_12L_UNLOCKED, ContentType.TEXT_12L_LOCKED,
                                   ContentType.TEXT_16L_UNLOCKED, ContentType.TEXT_16L_LOCKED,
                                   ContentType.TEXT_20L_UNLOCKED, ContentType.TEXT_20L_LOCKED]:
            frame = tk.Frame(self, bg=bg_global)
            frame.pack(expand=True, fill="x", padx=10, pady=5)
            self.content = tk.Text(frame, **cont_params,
                                   height=1 if self.content_type in [ContentType.TEXT_1L_UNLOCKED,
                                                                     ContentType.TEXT_1L_LOCKED]
                                   else 3 if self.content_type in [ContentType.TEXT_3L_UNLOCKED,
                                                                   ContentType.TEXT_3L_LOCKED]
                                   else 8 if self.content_type in [ContentType.TEXT_8L_UNLOCKED,
                                                                   ContentType.TEXT_8L_LOCKED]
                                   else 12 if self.content_type in [ContentType.TEXT_12L_UNLOCKED,
                                                                    ContentType.TEXT_12L_LOCKED]
                                   else 16 if self.content_type in [ContentType.TEXT_16L_UNLOCKED,
                                                                    ContentType.TEXT_16L_LOCKED]
                                   else 20 if self.content_type in [ContentType.TEXT_20L_UNLOCKED,
                                                                    ContentType.TEXT_20L_LOCKED] else 5)
            self.scroll = tk.Scrollbar(frame, command=self.content.yview)
            self.content.configure(yscrollcommand=self.scroll.set)
            self.content.insert(tk.END, self.content_text)
            self.scroll.pack(side="right", fill="y")
            self.content.pack(fill="x")
            if self.content_type in [ContentType.TEXT_LOCKED, ContentType.TEXT_1L_LOCKED,
                                     ContentType.TEXT_3L_LOCKED, ContentType.TEXT_8L_LOCKED,
                                     ContentType.TEXT_12L_LOCKED, ContentType.TEXT_16L_LOCKED,
                                     ContentType.TEXT_20L_LOCKED]:
                self.content.configure(state="disabled", relief="flat")

        elif self.content_type in [ContentType.ENTRY_UNLOCKED, ContentType.ENTRY_LOCKED]:
            self.content = tk.Entry(self, **cont_params)
            self.content.insert(0, self.content_text)
            if self.content_type == ContentType.ENTRY_LOCKED:
                self.content.configure(state="disabled")
            self.content.bind("<Return>", lambda x: self.on_click(*self.args, **self.kwargs))
            self.content.pack(expand=True, fill="x", padx=10, pady=5)

        self.btn_frame = tk.Frame(self, bg=self.btn_color)
        self.btn_frame.pack(anchor="e", padx=10, pady=5)
        self.btn = tk.Button(self.btn_frame, activebackground=self.bg_global, bg=self.bg_global, fg=self.btn_color,
                             font=self.btn_font, text=self.btn_text, bd=0,
                             command=lambda: self.on_click(*self.args, **self.kwargs))
        self.btn.pack(ipadx=5, padx=self.btn_bd, pady=self.btn_bd)

    def show(self, **kwargs):
        self.pack(padx=0, **({"fill": "x", "expand": True, "pady": self.pady} | kwargs))
        self.master.after(100, lambda: self.scroll.forget()
                          if self.content_type in [ContentType.TEXT_LOCKED, ContentType.TEXT_1L_LOCKED,
                                                   ContentType.TEXT_3L_LOCKED, ContentType.TEXT_8L_LOCKED,
                                                   ContentType.TEXT_12L_LOCKED, ContentType.TEXT_16L_LOCKED,
                                                   ContentType.TEXT_20L_LOCKED]
                          and self.scroll.get() == (0.0, 1.0) else None)


class UserInfo(tk.Frame):
    def __init__(self, master, main, theme: Theme, lang: Lang, user: User, private: bool = True):
        self.main, self.theme, self.lang = main, theme, lang
        self.height, self.width = self.main.winfo_height() * 90 / 100, self.main.winfo_width() * 80 / 100
        self.user, self.private = user, private

        super().__init__(master, background=self.theme.menu.bg)
        self.scroll = tk.Scrollbar(self, orient="vertical", width=20)
        self.scroll.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, background=self.theme.center.bg, bd=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.container = tk.Frame(self.canvas, bg=self.theme.center.bg)
        self.canvas.create_window(0, 0, anchor="nw", window=tk.Frame(bg=self.theme.center.bg))
        self.canvas.create_window(self.width / 2, 0, anchor="n", window=self.container)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.canvas.yview)

        params = {"master": self.container,
                  "width": self.width, "padx": 50, "pady": 20, "bg_global": "gray", "bg_content": "gray",
                  "label_color": "black", "label_font": ("Arial", 10, "bold underline"),
                  "content_color": "black", "content_font": ("Consolas", 10, ""),
                  "btn_color": "black", "btn_font": ("Arial", 10, ""), "btn_bd": 1}

        def field_c(name, content, content_type=ContentType.TEXT_1L_LOCKED):
            return InfoItem(**params, label_text=f"{name} :", content_type=content_type,
                            content_text=str(content), btn_text="Copier",
                            on_click=pyperclip.copy, args=(str(content),))

        def field_m(name, content, private, on_click=None, args=(), kwargs={}):
            return InfoItem(**params, label_text=f"{name} :",
                            content_type=ContentType.TEXT_1L_LOCKED if private else ContentType.ENTRY_UNLOCKED,
                            content_text=str(content),
                            btn_text="Copier" if private else "Modifier",
                            on_click=pyperclip.copy if private else on_click,
                            args=(str(content),) if private and not args else args, kwargs=kwargs)

        self.information = [
            field_c("UUID", self.user.get_uuid()),
            field_c("Nom d'Utilisateur", self.user.get_username()),
            field_m("Nom Complet", self.user.get_completename(), self.private),
            field_m("E-Mail", self.user.get_mail(), self.private),
            field_m("Mot de Passe", ("*" * len(str(self.user.get_password()))) if self.private
                    else self.user.get_password(), self.private),
            field_c("Administrateur", ("Clé : " + ("*" * (len(str(self.user.get_uuid())) + 3)) if self.private
                                       else ("${" + str(self.user.get_uuid()) + "}"))
                    if self.user.is_admin() else "Non."),
            field_c("Création", self.user.get_creation()),
        ]
        for i in self.information: i.show()

        self.bind("<Configure>", self.update_place)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.after(100, self.update_place)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def show(self):
        self.place()
        self.update_place()

    def update_place(self, e=None):
        self.height, self.width = self.main.winfo_height() * 90 / 100, self.main.winfo_width() * 80 / 100
        self.place_configure(relx=0.5, rely=1, anchor="s", height=self.height, width=self.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.scroll.winfo_ismapped() and self.scroll.get() == (0.0, 1.0):
            self.scroll.forget()
        elif not self.scroll.winfo_ismapped() and self.scroll.get() != (0.0, 1.0):
            self.scroll.pack(side="right", fill="y")
