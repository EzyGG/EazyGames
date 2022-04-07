import os
import time
import requests
import threading
import tkinter as tk
from PIL import Image as Image, ImageTk

from ezyapi.UUID import UUID
import ezyapi.game_manager as manager
from securized import ServerRessources
import ezyapi.mysql_connection as connect
from sessions_master import User, UserAlreadyExistsException

from fr.luzog.ezygg.consts import Theme, Lang
from fr.luzog.ezygg.login import LogInFrame
# from fr.luzog.ezygg.home import HomeFrame
from fr.luzog.ezygg.register import RegisterFrame


class Main(tk.Tk):
    def __init__(self, theme: Theme = Theme.default(), lang: Lang = Lang.FR()):
        self.theme, self.lang = theme, lang
        self.user: User = None

        super().__init__(self.lang.globals.title, self.lang.globals.title)
        self.title(self.lang.globals.title)
        self.geometry("1080x720")  # 1080x720 1366x768
        self.resizable(True, True)
        self.configure(background=self.theme.main.bg, highlightthickness=self.theme.main.highlightthickness,
                       highlightbackground=self.theme.main.highlightbackground)

        self.load_rsrc()

        try:
            os.mkdir("games")
        except Exception:
            pass

        try:
            self.iconbitmap("rsrc/icon.ico")
        except Exception:
            pass

        if connect.connection is None:
            connect.connexion()

        LogInFrame(self, self, self.theme, self.lang).show()
        # lambda: print("HOME"),
        # lambda: RegisterFrame(self, self, self.theme, self.lang).show()  # lambda: HomeFrame(self).show()

    @staticmethod
    def dwl(url: str, name: str):
        req = requests.get(url)
        with open("rsrc/" + name, 'wb') as file:
            file.write(req.content)

    def load_rsrc(self):
        try:
            os.mkdir("rsrc")
        except Exception:
            pass
        # TODO -> Reestablish
        # self.dwl(ServerRessources.ICON, "icon.ico")
        # self.dwl(ServerRessources.IMAGE, "icon.png")
        # self.dwl(ServerRessources.DEFAULT_FACE, "default_face.png")

    def restart(self):
        self.stop()
        self.__init__()

    def start(self):
        self.mainloop()
        return self

    def stop(self):
        self.destroy()
        return self