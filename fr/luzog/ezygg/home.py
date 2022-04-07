import threading
import tkinter as tk

from fr.luzog.ezygg.menu import Menu
from fr.luzog.ezygg.center import Center
from fr.luzog.ezygg.information import Information


class HomeFrame(tk.Frame):
    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang

        super().__init__(master, background=self.theme.home.bg, highlightthickness=self.theme.home.highlightthickness,
                         highlightbackground=self.theme.home.highlightbackground)
        self.home_label = tk.Label(self, text=self.lang.home.welcome + " " + (
            self.master.user.get_completename() if self.master.user.get_completename() is not None else self.master.user.get_username()) + " !",
                                   bg=self.theme.home.bg, fg=self.theme.home.fg, font=self.theme.home.f_welcome)
        self.home_label.pack(pady=10, side="top", anchor="center")
        self.menu = Menu(self, self.main, self.theme, self.lang)
        self.menu.show()
        self.center = Center(self, self.main, self.theme, self.lang)
        self.center.show()
        self.information = Information(self, self.main, self.theme, self.lang)
        self.information.show()

        # self.temp_geometry = self.winfo_geometry()
        self.bind("<Configure>", self.on_configure)

        def init():
            """
            Explanation: wait "asynchronously" (synchronously but in another Thread to load all components
            in a same time) 0.1sec and after, refresh the screen to remove unnecessary scrollbar.
            """
            t = threading.Thread()
            t.start()
            t.join(0.1)
            threading.Thread(target=self.on_configure).start()

        threading.Thread(target=init).start()

    def show(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=self.master.winfo_height(),
                   width=self.master.winfo_width())

    def update_place(self):
        self.place_configure(relx=0.5, rely=0.5, anchor=tk.CENTER, height=self.master.winfo_height(),
                             width=self.master.winfo_width())

    def on_configure(self, event=None):
        # def get_real_geometry(geometry: str):
        #     return (int(geometry.split("x")[0]) + int(geometry.split("x")[1].split("+")[0]),
        #             int(geometry.split("x")[1].split("+")[1]) + int(geometry.split("x")[1].split("+")[2]))

        # old, new = get_real_geometry(self.temp_geometry), get_real_geometry(self.winfo_geometry())

        self.update_place()
        self.menu.update_place()
        self.center.update_place()
        self.information.update_place()

        # self.temp_geometry = self.winfo_geometry()