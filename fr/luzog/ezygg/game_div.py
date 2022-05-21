import os
import tkinter as tk

from ezyapi.UUID import UUID
import ezyapi.game_manager as manager

from fr.luzog.ezygg.consts import Theme, Lang


class GameDiv(tk.Frame):
    TOTAL_WIDTH = 235
    TOTAL_HEIGHT = 335

    def __init__(self, master, main, theme: Theme, lang: Lang, uuid: UUID, name: str, catchphrase: str = None,
                 row: int = 0, column: int = 0, exp=0, gp=0, lvl=0, special=None):
        self.main, self.theme, self.lang = main, theme, lang

        # TODO -> Add <Enter> <Leave> Events (mouse hover effect)
        super().__init__(master, background=self.theme.game_div.bg, highlightthickness=self.theme.game_div.highlightthickness,
                         highlightbackground=self.theme.game_div.highlightbackground, width=220, height=320)
        self.uuid: UUID = uuid
        self.row, self.column = row, column
        self.name, self.catchphrase = name, catchphrase
        self.exp, self.gp, self.lvl, self.special = exp, gp, lvl, special

        self.pack_propagate(0)

        self.IMAGE_SIZE = (220, 160)

        self.img: tk.PhotoImage = None

        def find():
            t = None
            for f in os.listdir(f"games/{uuid}"):
                if "." in f and f.split(".")[0] == "thumbnail":
                    t = f.split(".")[1]
                    break
            if t is not None:
                self.img = tk.PhotoImage(file=f"games/{uuid}/thumbnail.{t}")

        try:
            os.mkdir(f"games/{uuid}")
        except Exception:
            pass

        try:
            find()
            if self.img is None:
                for r in manager.import_resources(uuid):
                    if r.specification == "thumbnail":
                        r.save_if_doesnt_exists(f"games/{uuid}", name="thumbnail")
                find()
        except FileNotFoundError:
            for r in manager.import_resources(uuid):
                if r.specification == "thumbnail":
                    r.save_if_doesnt_exists(f"games/{uuid}", name="thumbnail")
            find()

        if self.img:
            if self.img.width() > self.IMAGE_SIZE[0] or self.img.height() > self.IMAGE_SIZE[1]:
                if self.img.width() - self.IMAGE_SIZE[0] > self.img.height() - self.IMAGE_SIZE[1]:
                    final_geometry = (
                        self.IMAGE_SIZE[0], (self.IMAGE_SIZE[0] / self.img.width()) * self.img.height())
                else:
                    final_geometry = (
                        (self.IMAGE_SIZE[1] / self.img.height()) * self.img.width(), self.IMAGE_SIZE[1])
                self.img = self.img.subsample(round(self.img.width() / final_geometry[0]),
                                              round(self.img.height() / final_geometry[1]))
            self.image_label = tk.Label(self, bg=self.theme.game_div.bg_image, height=self.IMAGE_SIZE[1],
                                        width=self.IMAGE_SIZE[0], image=self.img)
            self.image_label.pack(anchor="center")
        else:
            tk.Frame(self, bg=self.theme.game_div.bg_image, height=self.IMAGE_SIZE[1], width=self.IMAGE_SIZE[0]).pack(
                anchor="center")

        self.title_label = tk.Label(self, bg=self.theme.game_div.bg, fg=self.theme.game_div.fg_title, text=str(name), font=self.theme.game_div.f_title,
                                    wraplengt=220)
        self.title_label.pack()

        self.catchphrase_label = tk.Label(self, bg=self.theme.game_div.bg, fg=self.theme.game_div.fg_catchphrase, text=str(catchphrase), wraplengt=220)
        self.catchphrase_label.pack()

        self.play_frame = tk.Frame(self, bg=self.theme.game_div.bg)
        self.play_button = tk.Button(self.play_frame, activebackground=self.theme.game_div.bg, bg=self.theme.game_div.bg, fg=self.theme.game_div.fg_btn,
                                     bd=1, relief="solid", width=10, text=self.lang.game_div.play, font=self.theme.game_div.f_btn,
                                     command=self.play)
        self.play_button.pack(padx=8)
        self.play_frame.pack(side="bottom")

        self.reward_frame2 = tk.Frame(self, bg=self.theme.game_div.bg)
        if lvl and gp:
            self.gp_label = tk.Label(self.reward_frame2, bg=self.theme.game_div.bg, font=self.theme.game_div.f_reward, text=f"+{gp} GP",
                                     fg=self.theme.globals.color_gp)
            self.gp_label.pack(side="left")
        if special:
            self.sp_label = tk.Label(self.reward_frame2, bg=self.theme.game_div.bg, font=self.theme.game_div.f_reward, text=f"{special}",
                                     fg=self.theme.globals.color_special)
            self.sp_label.pack(side="bottom")
        self.reward_frame2.pack(side="bottom")

        self.reward_frame1 = tk.Frame(self, bg=self.theme.game_div.bg)
        self.reward_label = tk.Label(self.reward_frame1, bg=self.theme.game_div.bg, fg=self.theme.game_div.fg_label, text=self.lang.game_div.reward,
                                     font=self.theme.game_div.f_label)
        self.reward_label.pack(side="left")
        if lvl:
            self.lvl_label = tk.Label(self.reward_frame1, bg=self.theme.game_div.bg, font=self.theme.game_div.f_reward, text=f"+{lvl} LVL",
                                      fg=self.theme.globals.color_lvl)
            self.lvl_label.pack(side="left")
        if exp:
            self.exp_label = tk.Label(self.reward_frame1, bg=self.theme.game_div.bg, font=self.theme.game_div.f_reward, text=f"+{exp} EXP",
                                      fg=self.theme.globals.color_exp)
            self.exp_label.pack(side="left")
        if not lvl and gp:
            self.gp_label = tk.Label(self.reward_frame1, bg=self.theme.game_div.bg, font=self.theme.game_div.f_reward, text=f"+{gp} GP",
                                     fg=self.theme.globals.color_gp)
            self.gp_label.pack(side="left")
        if not (lvl or special or exp or gp):
            self.nothing_label = tk.Label(self.reward_frame1, bg=self.theme.game_div.bg, fg=self.theme.game_div.fg_nothing, font=self.theme.game_div.f_nothing,
                                          text=self.lang.game_div.nothing)
            self.nothing_label.pack(side="left")
        self.reward_frame1.pack(side="bottom")

    def show(self, row: int = None, column: int = None):
        if row is not None: self.row = row
        if column is not None: self.column = column
        self.grid(padx=15, pady=15, row=self.row, column=self.column)

    def play(self):
        if not (self.uuid.getUUID() in os.listdir("games")
                and ("main.exe" in os.listdir("games\\" + self.uuid.getUUID())
                     or "center.py" in os.listdir("games\\" + self.uuid.getUUID()))):
            manager.import_resource(self.uuid, "game").save_by_erasing("games/" + self.uuid.getUUID())
        pwd = self.main.user.password.replace('"', '\\"')
        os.system(
            f"start /d {os.getcwd()}\\games\\{self.uuid.getUUID()} main --uuid \"{self.main.user.uuid.getUUID()}\" --password \"{pwd}\"")
        # TODO -> destroy() or not in options
        # self.master.master.master.master.master.destroy()