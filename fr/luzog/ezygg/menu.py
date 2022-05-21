import webbrowser
import tkinter as tk
from PIL import Image as Image, ImageTk

from ezyapi.sessions import User
import ezyapi.mysql_connection as connect

from fr.luzog.ezygg.consts import VERSION
from fr.luzog.ezygg.user_info import UserInfo
from fr.luzog.ezygg.chat import ChatFrame


class Menu(tk.Frame):
    def __init__(self, master, main, theme, lang):
        self.main, self.theme, self.lang = main, theme, lang

        super().__init__(master, background=self.theme.menu.bg)
        # TODO -> Mettre ici plusieurs catégories
        #  ---
        #  | Partie Menu :
        #  | - Liste des jeux
        #  | - Récompenses
        #  | - Top des Joueurs
        #  | - Boutique
        #  ---
        #  | Partie Top:
        #  | - Juste les 3 où les 5 premiers avec le nb de points
        #  ---
        #  | Partie Amis en Lignes :
        #  | Affiche les gens connectés
        #  |  -> "Il y a ... Joueurs connectés :"
        #  |  -> *petit § avec la liste des gens connectés*
        #  ---
        #  | Si ya de la place:
        #  |  -> Version de l'app
        #  |  -> Boutton "Quitter le Jeu"
        #  ---

        # TODO -> For Now -> Commencer le menu + Update le webflow + Chercher la conso
        #  + Pr la semaine pro : Système de jeu FONCTIONNEL ! (fichiers .py / .exe, config[.yml .any .ezygg
        #   -> crypté pour ne pas changer les points du coté utilisateur], api pour les autres jeux
        #   OU ALORS les autres jeux == API !!!! breff à voir.)

        self.spacing = 5
        self.intent = 10

        tk.Frame(self, bg=self.theme.menu.bg).pack(pady=10)

        self.img = Image.open("rsrc/icon.png")
        self.img = self.img.resize((100, 100), Image.ANTIALIAS)
        _img = ImageTk.PhotoImage(self.img)
        self.face_img = tk.Label(self, bg=self.theme.menu.bg, image=_img, height=100, width=100)
        self.face_img.image = _img
        self.face_img.pack(anchor="w")
        tk.Frame(self, bg=self.theme.menu.bg).pack(pady=self.spacing * 2)

        # self.menu_title_lbl = tk.Label(self, bg=self.theme.menu.bg, fg=self.theme.menu.fg_title, font=self.theme.menu.f_title,
        #                                text=self.lang.menu.title)
        # self.menu_title_lbl.pack(anchor="w")
        # self.all_games_btn = tk.Button(self, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_text,
        #                                bd=0, relief="solid", text="- " + self.lang.menu.all_games,
        #                                command=lambda: self.all_games_btn.configure(text=" - " + self.lang.menu.not_now))
        # self.all_games_btn.pack(padx=self.intent, anchor="w")
        # self.tops_btn = tk.Button(self, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_text,
        #                           bd=0, relief="solid", text="- " + self.lang.menu.tops,
        #                           command=lambda: self.tops_btn.configure(text=" - " + self.lang.menu.not_now))
        # self.tops_btn.pack(padx=self.intent, anchor="w")
        # self.reward_btn = tk.Button(self, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_text,
        #                             bd=0, relief="solid", text="- " + self.lang.menu.reward,
        #                             command=lambda: self.reward_btn.configure(text=" - " + self.lang.menu.not_now))
        # self.reward_btn.pack(padx=self.intent, anchor="w")
        # self.shop_btn = tk.Button(self, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_text,
        #                           bd=0, relief="solid", text="- " + self.lang.menu.shop,
        #                           command=lambda: self.shop_btn.configure(text=" - " + self.lang.menu.not_now))
        # self.shop_btn.pack(padx=self.intent, anchor="w")
        # tk.Frame(self, bg=self.theme.menu.bg).pack(pady=self.spacing)

        self.menu_top_lbl = tk.Label(self, bg=self.theme.menu.bg, fg=self.theme.menu.fg_title, font=self.theme.menu.f_title,
                                     text=self.lang.menu.top5)
        self.menu_top_lbl.pack(anchor="w")
        self.top_5_widgets = []
        connect.execute(
            """SELECT uuid FROM users WHERE exp!=0 ORDER BY lvl DESC, exp DESC, gp DESC LIMIT 5""")
        top5 = connect.fetch()

        def u_info(usr):
            self.main.clear_all()
            self.chat.destroy()
            UserInfo(self.main, self.main, self.theme, self.lang, usr,
                     private=not self.main.user.is_admin() and usr.get_uuid() != self.main.user.get_uuid()).show()

        for i in range(5):
            if len(top5) > i:
                u = User(top5[i][0])
                text = str(i + 1) + ". " + u.get_completename() + " [" + str(u.get_exp()) + "]"
                usr = True
            else:
                text = str(i + 1) + ". ..."
                usr = False
            top = tk.Button(self, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_text,
                            bd=0, relief="solid", font=self.theme.menu.f_top,
                            text=text, command=(lambda u=u: u_info(u)) if usr else (lambda: None))
            top.pack(padx=0, anchor="w")
            self.top_5_widgets.append(top)
        tk.Frame(self, bg=self.theme.menu.bg).pack(pady=self.spacing)

        self.chat = ChatFrame(self, self.main, self.theme, self.lang)
        # Show later to avoid issues

        self.more_frame = tk.Frame(self, bg=self.theme.menu.bg)
        self.more_frame.pack(pady=self.spacing, side="bottom")
        self.rules_politics = tk.Button(self.more_frame, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_info,
                                        bd=0, relief="solid", font=self.theme.menu.f_info,
                                        text=self.lang.menu.politics,
                                        command=lambda: webbrowser.open(self.theme.globals.link_website))
        self.rules_politics.pack(side="left", padx=0)
        self.version_btn = tk.Button(self.more_frame, activebackground=self.theme.menu.bg, bg=self.theme.menu.bg, fg=self.theme.menu.fg_info,
                                       bd=0, relief="solid", font=self.theme.menu.f_info,
                                       text=VERSION.get_version(),
                                       command=lambda: webbrowser.open(self.theme.globals.link_github))
        self.version_btn.pack(side="left", padx=0)

        connect.execute("""SELECT * FROM users""")
        self.online_members = tk.Label(self, bg=self.theme.menu.bg, fg=self.theme.menu.fg_players,
                                       text=self.lang.menu.total_players + " " + str(len(connect.fetch()[0])))
        self.online_members.pack(pady=self.spacing, side="bottom", anchor="w")
        tk.Frame(self, bg=self.theme.menu.bg).pack(pady=self.spacing)

    def show(self):
        self.place(relx=0, rely=1, anchor="sw", height=self.main.winfo_height(),
                   width=self.main.winfo_width() * 17 / 100)
        self.chat.show()

    def update_place(self):
        self.place_configure(relx=0, rely=1, anchor="sw", height=self.main.winfo_height(),
                             width=self.main.winfo_width() * 17 / 100)
