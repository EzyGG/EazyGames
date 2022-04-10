import os
import sys
import requests
import tkinter as tk

from securized import ServerRessources
import ezyapi.mysql_connection as connect
from sessions_master import User

from fr.luzog.ezygg.consts import Theme, Lang
from fr.luzog.ezygg.login import LogInFrame
from fr.luzog.ezygg.register import RegisterFrame


class Main(tk.Tk):
    def __init__(self, theme: Theme = Theme.default(), lang: Lang = Lang.FR()):
        self.theme, self.lang = theme, lang
        self.user: User | None = None

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

        # if len(args) >= 4 and "--password" in args and args.index("--password") != len(args) - 1:
        #     password = args[args.index("--password") + 1]
        #     args.pop(args.index("--password") + 1)
        #     args.pop(args.index("--password"))
        #
        #     if "--uuid" in args and args.index("--uuid") != len(args) - 1:
        #         id = args[args.index("--uuid") + 1]
        #         args.pop(args.index("--uuid") + 1)
        #         args.pop(args.index("--uuid"))
        #     elif "--username" in args and args.index("--username") != len(args) - 1:
        #         id = args[args.index("--username") + 1]
        #         args.pop(args.index("--username") + 1)
        #         args.pop(args.index("--username"))
        #     else:
        #         raise UserParameterExpected()
        #
        #     __user = sessions.User(id, password)
        #     if not __user.connected():
        #         raise sessions.UserNotFoundException()
        # else:
        #     raise UserParameterExpected()

        args = sys.argv[1:]

        def verif_kw(field, starts="--"):
            if len(args) >= 2 and (starts + field) in args and args.index(starts + field) != len(args) - 1\
                    and not args[args.index(starts + field) + 1].startswith(starts):
                v = args[args.index(starts + field) + 1]
                args.pop(args.index(starts + field) + 1)
                args.pop(args.index(starts + field))
                return v
            return None

        uid, name, pwd = verif_kw("uuid"), verif_kw("username"), verif_kw("password")
        uid, name, pwd = uid if uid else verif_kw("uid", starts="-"), name if name else verif_kw("usr", starts="-"),\
                         pwd if pwd else verif_kw("pwd", starts="-")

        complete_name = verif_kw("complete-name")
        if not complete_name: complete_name = verif_kw("cname", starts="-")

        first_name = verif_kw("first-name")
        if not first_name: first_name = verif_kw("fname", starts="-")
        if not first_name and complete_name: first_name = " ".join(complete_name.split(" ")[:-1]).title()

        last_name = verif_kw("last-name")
        if not last_name: last_name = verif_kw("lname", starts="-")
        if not last_name and complete_name: last_name = complete_name.split(" ")[-1].upper()

        mail = verif_kw("mail")
        if not mail: mail = verif_kw("mail", starts="-")

        def verif_a(field):
            if field in args:
                args.pop(args.index(field))
                return True
            return False

        no_chk = verif_a("--no-check") or verif_a("-nchk")
        register = verif_a("--register") or verif_a("-reg")

        if register:
            self.register = RegisterFrame(self, self, self.theme, self.lang)
            if name:
                self.register.user_name_entry.delete(0, "end")
                self.register.user_name_entry.insert(0, name.lower().replace(" ", "").replace("\n", ""))
            if first_name:
                self.register.complete_first_name_entry.delete(0, "end")
                self.register.complete_first_name_entry.insert(0, first_name)
            if last_name:
                self.register.complete_last_name_entry.delete(0, "end")
                self.register.complete_last_name_entry.insert(0, last_name)
            if mail:
                self.register.mail_entry.delete(0, "end")
                self.register.mail_entry.insert(0, mail)
            if pwd:
                self.register.pwd_entry.delete(0, "end")
                self.register.pwd_entry.insert(0, pwd)
                self.register.vpwd_entry.delete(0, "end")
                self.register.vpwd_entry.insert(0, pwd)
                self.register.key_press()
            self.register.show()
        else:
            self.login = LogInFrame(self, self, self.theme, self.lang)
            if uid or name:
                self.login.user_name_entry.delete(0, "end")
                self.login.user_name_entry.insert(0, uid if uid else name)
            if pwd:
                self.login.user_pwd_entry.delete(0, "end")
                self.login.user_pwd_entry.insert(0, pwd)
            self.login.show()
            if not no_chk:
                self.login.verify_user()

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
        self.dwl(ServerRessources.ICON, "icon.ico")
        self.dwl(ServerRessources.IMAGE, "icon.png")
        self.dwl(ServerRessources.DEFAULT_FACE, "default_face.png")

    def restart(self):
        self.stop()
        self.__init__()

    def start(self):
        self.mainloop()
        return self

    def stop(self):
        self.destroy()
        return self

    def clear_all(self):
        for c in self.winfo_children():
            c.destroy()
