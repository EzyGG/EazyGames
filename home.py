import os
import time
import tkinter as tk
from sessions import User
import requests
from securized import ServerRessources


class Home(tk.Tk):
    COLOR_BG = "gray"
    COLOR_BG2 = "dim gray"
    COLOR_BG3 = "dark gray"

    def __init__(self):
        self.user: User = None

        super().__init__("EzyGames", "EzyGames")
        self.title("EzyGames")
        self.geometry("1080x720")  # 1080x720 1366x768
        self.resizable(False, False)
        self.configure(background=Home.COLOR_BG, highlightthickness=16)

        self.load_rsrc()

        try:
            self.iconbitmap("rsrc/icon.ico")
        except Exception:
            pass

        Home.ConnexionFrame(self).show()

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
        Home.dwl(ServerRessources.ICON, "icon.ico")
        Home.dwl(ServerRessources.IMAGE, "icon.png")
        Home.dwl(ServerRessources.DEFAULT_FACE, "default_face.png")

    def restart(self):
        self.stop()
        self.__init__()

    def start(self):
        self.mainloop()
        return self

    def stop(self):
        self.destroy()
        return self

    class Home(tk.Frame):
        def __init__(self, master):
            super().__init__(master, background=Home.COLOR_BG, highlightthickness=10,
                             highlightbackground=Home.COLOR_BG2)
            self.home_label = tk.Label(self, text="Bienvenue " + (
                self.master.user.get_completename() if self.master.user.get_completename() is not None else self.master.user.get_username()) + " !",
                                       bg=Home.COLOR_BG, font=("JetBrains Mono", 14, "bold"))
            self.home_label.pack(pady=10, side="top", anchor="center")
            self.menu = Home.Home.Menu(self)
            self.menu.show()
            self.main = Home.Home.Main(self)
            self.main.show()
            self.information = Home.Home.Information(self)
            self.information.show()

        def show(self):
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=self.master.winfo_height(),
                       width=self.master.winfo_width())

        class Menu(tk.Frame):
            def __init__(self, master):
                super().__init__(master, background=Home.COLOR_BG2)
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
                #  | Si ya de la place, Boutton "Quitter le Jeu"
                #  ---

            def show(self):
                self.place(relx=0, rely=1, anchor="sw", height=self.master.master.winfo_height(),
                           width=self.master.master.winfo_width() * 17 / 100)

        class Main(tk.Frame):
            def __init__(self, master):
                super().__init__(master, background=Home.COLOR_BG3)

            def show(self):
                self.place(relx=0.5, rely=1, anchor="s", height=self.master.master.winfo_height() * 90 / 100,
                           width=self.master.master.winfo_width() * 58 / 100)

        class Information(tk.Frame):
            def __init__(self, master):
                super().__init__(master, background=Home.COLOR_BG2)
                self.spacing = 5

                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=35)

                self.img = tk.PhotoImage(file="rsrc/default_face.png")
                self.img = self.img.subsample(int(self.img.width()/64), int(self.img.height()/64))
                self.face_img = tk.Label(self, bg=Home.COLOR_BG2, image=self.img, height=64, width=64)
                self.face_img.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.complete_name_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Nom Complet :")
                self.complete_name_info.pack(anchor="e")
                self.complete_name = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_completename())
                self.complete_name.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.user_name_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Identifiant :")
                self.user_name_info.pack(anchor="e")
                self.user_name = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_username())
                self.user_name.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.mail_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="E-Mail :")
                self.mail_info.pack(anchor="e")
                self.mail = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_mail())
                self.mail.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.creation_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Création :")
                self.creation_info.pack(anchor="e")
                self.creation = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_creation())
                self.creation.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.uuid_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="UUID :")
                self.uuid_info.pack(anchor="e")
                self.uuid = tk.Label(self, bg=Home.COLOR_BG2, font=("", 7,"bold"), text=self.master.master.user.get_uuid())
                self.uuid.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                tk.Label(self, bg=Home.COLOR_BG2, text="---").pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.lvl_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Niveau de Jeu (LVL) :")
                self.lvl_info.pack(anchor="e")
                self.lvl = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_lvl())
                self.lvl.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.exp_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Points d'Experience (EXP) :")
                self.exp_info.pack(anchor="e")
                self.exp = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_exp())
                self.exp.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.gp_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Points de Jeu (GP) :")
                self.gp_info.pack(anchor="e")
                self.gp = tk.Label(self, bg=Home.COLOR_BG2, text=self.master.master.user.get_points())
                self.gp.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.ratio_info = tk.Label(self, bg=Home.COLOR_BG2, font=("", 8,"bold"), text="Parties Gagnées / Jouées :")
                self.ratio_info.pack(anchor="e")
                self.ratio = tk.Label(self, bg=Home.COLOR_BG2, text=str(self.master.master.user.get_total_wins())
                                                                            + " / " + str(self.master.master.user.get_played_games()))
                self.ratio.pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                tk.Label(self, bg=Home.COLOR_BG2, text="---").pack(anchor="e")
                tk.Frame(self, bg=Home.COLOR_BG2).pack(pady=self.spacing)

                self.settings_frame = tk.Frame(self, bg=Home.COLOR_BG2)
                self.settings_frame.pack(pady=self.spacing)
                self.more_button = tk.Button(self.settings_frame, activebackground=Home.COLOR_BG2, bg=Home.COLOR_BG2,
                                             bd=1, relief="solid", width=10, text="Voir Plus", command=lambda:
                                             self.more_button.configure(text="Plus Tard... :/"))
                self.more_button.pack(side="left")
                self.logout_button = tk.Button(self.settings_frame, activebackground=Home.COLOR_BG2, bg=Home.COLOR_BG2,
                                               bd=1, relief="solid", width=10, text="Déconnexion",
                                               command=self.master.master.restart)
                self.logout_button.pack(side="right", padx=8)

            def show(self):
                self.place(relx=1, rely=1, anchor="se", height=self.master.master.winfo_height(),
                           width=self.master.master.winfo_width() * 17 / 100)

    class ConnexionFrame(tk.Frame):
        def __init__(self, master):
            super().__init__(master, bg=Home.COLOR_BG2, highlightthickness=2, highlightbackground="black")

            self.label = tk.Label(self, bg=Home.COLOR_BG2, height=2, font=("", 30,), text="Connexion")
            self.label.pack(side="top", pady=30)

            self.user_frame = tk.Frame(self, bg=Home.COLOR_BG2)
            self.user_name_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Username :")
            self.user_name_label.grid(row=0, column=0, padx=10, pady=20)
            self.user_name_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=35,
                                            font=("JetBrains Mono", 10))
            self.user_name_entry.grid(row=0, column=1, padx=10, pady=20)
            self.user_pwd_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Password :")
            self.user_pwd_label.grid(row=1, column=0, padx=10, pady=20)
            self.user_pwd_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=35, show="*",
                                           font=("JetBrains Mono", 10))
            self.user_pwd_entry.grid(row=1, column=1, padx=10, pady=20)
            self.user_frame.pack(side="top", pady=20)

            self.label = tk.Label(self, bg=Home.COLOR_BG2, width=100)
            self.label.pack(side="top", pady=20)
            self.button = tk.Button(self, width=30, height=2, text="Verifier",
                                    command=self.verify_user)
            self.button.pack(side="top", pady=20)

            self.master.bind("<Return>", lambda e: self.verify_user())

        def show(self):
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)
            self.user_name_entry.focus_set()

        def verify_user(self):
            u = User(self.user_name_entry.get(), self.user_pwd_entry.get())
            self.label.configure(text=("Connected as " + str(u.get_uuid())) if u.exists() else "User Not Found.",
                                 fg="#00ff00" if u.exists() else "#ff0000", font=("", 10, "bold"))
            self.update()
            if u.exists():
                self.master.unbind("<Return>")
                self.master.user = u
                time.sleep(0.5)
                self.destroy()
                Home.Home(self.master).show()
