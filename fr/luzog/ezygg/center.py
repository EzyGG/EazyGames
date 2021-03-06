import tkinter as tk

from ezyapi.UUID import UUID
import ezyapi.mysql_connection as connect

from fr.luzog.ezygg.game_div import GameDiv


class Center(tk.Frame):
    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang
        self.__is_in = False

        super().__init__(master, background=self.theme.center.bg)
        self.scroll = tk.Scrollbar(self, orient="vertical", width=20)
        self.scroll.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, background=self.theme.center.bg, bd=0, highlightthickness=0)
        self.container = tk.Frame(self.canvas, background=self.theme.center.bg)
        self.canvas.create_window((0, 0), window=self.container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.canvas.yview)
        self.canvas.pack(side="left", fill="both", expand=True)

        connect.execute("SELECT * FROM games")
        self.games = [GameDiv(self.container, self.main, self.theme, self.lang, UUID(id), name, catchphrase=catchphrase, exp=exp, gp=gp)
                      for id, name, accessible, creation, creator, exp, gp, other, catchphrase, desc
                      in connect.fetch()]

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel, add="+")
        self.canvas.bind("<Enter>", lambda e: self.is_in(True))
        self.canvas.bind("<Leave>", lambda e: self.is_in(False))

        self.update_place()

    def is_in(self, __set_is_in: bool | None = None) -> bool:
        if __set_is_in is not None:
            self.__is_in = __set_is_in
        return self.__is_in

    def on_mousewheel(self, event):
        if self.is_in():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def show(self):
        self.place(relx=0.5, rely=1, anchor="s", height=self.main.winfo_height() * 90 / 100,
                   width=self.main.winfo_width() * 58 / 100)

    def update_place(self):
        item_per_line = ((self.main.winfo_width() * 58 / 100) - 30) // GameDiv.TOTAL_WIDTH
        for g in self.games:
            g.forget()
        for i, g in enumerate(self.games):
            g.show(int(i // item_per_line), int(i % item_per_line))
        self.place_configure(relx=0.5, rely=1, anchor="s", height=self.main.winfo_height() * 90 / 100,
                             width=self.main.winfo_width() * 58 / 100)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.scroll.winfo_ismapped() and self.scroll.get() == (0.0, 1.0):
            self.scroll.forget()
        elif not self.scroll.winfo_ismapped() and self.scroll.get() != (0.0, 1.0):
            self.scroll.pack(side="right", fill="y")
