import os
import time
import tkinter as tk
from sessions import User, UserAlreadyExistsException
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
        self.configure(background=Home.COLOR_BG, highlightthickness=16, highlightbackground=Home.COLOR_BG2)

        self.load_rsrc()

        try:
            self.iconbitmap("rsrc/icon.ico")
        except Exception:
            pass

        Home.LogInFrame(self).show()

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

    class HomeFrame(tk.Frame):
        def __init__(self, master):
            super().__init__(master, background=Home.COLOR_BG, highlightthickness=10,
                             highlightbackground=Home.COLOR_BG2)
            self.home_label = tk.Label(self, text="Bienvenue " + (
                self.master.user.get_completename() if self.master.user.get_completename() is not None else self.master.user.get_username()) + " !",
                                       bg=Home.COLOR_BG, font=("JetBrains Mono", 14, "bold"))
            self.home_label.pack(pady=10, side="top", anchor="center")
            self.menu = Home.HomeFrame.Menu(self)
            self.menu.show()
            self.main = Home.HomeFrame.Main(self)
            self.main.show()
            self.information = Home.HomeFrame.Information(self)
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

    class LogInFrame(tk.Frame):
        def __init__(self, master):
            super().__init__(master, bg=Home.COLOR_BG2, highlightthickness=2, highlightbackground="black")

            self.label = tk.Label(self, bg=Home.COLOR_BG2, height=2, font=("", 30,), text="Connexion")
            self.label.pack(side="top", pady=30)

            self.user_frame = tk.Frame(self, bg=Home.COLOR_BG2)
            self.user_name_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Nom d'utilisateur :")
            self.user_name_label.grid(row=0, column=0, padx=10, pady=20, sticky="e")
            self.user_name_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=35,
                                            font=("JetBrains Mono", 10))
            self.user_name_entry.grid(row=0, column=1, padx=10, pady=20)
            self.user_pwd_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Mot de passe :")
            self.user_pwd_label.grid(row=1, column=0, padx=10, pady=20, sticky="e")
            self.user_pwd_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=35, show="*",
                                           font=("JetBrains Mono", 10))
            self.user_pwd_entry.grid(row=1, column=1, padx=10, pady=20)
            self.user_frame.pack(side="top", pady=20)

            self.other_frame = tk.Label(self, bg=Home.COLOR_BG2)
            self.forgot_pwd_btn = tk.Button(self.other_frame, activebackground=Home.COLOR_BG2, bg=Home.COLOR_BG2,
                                            bd=0, relief="solid", text="Mot de passe oublié ?",
                                            font=("", 10, "underline"), command=lambda: self.forgot_pwd_btn.config(text="Pas disponible pour l'instant... :/"))
            self.forgot_pwd_btn.pack(side="left", padx=10)
            self.register_btn = tk.Button(self.other_frame, activebackground=Home.COLOR_BG2, bg=Home.COLOR_BG2,
                                          bd=0, relief="solid", text="S'inscrire.", font=("", 10, "underline"),
                                          command=self.register_btn)
            self.register_btn.pack(side="left", padx=10)
            self.other_frame.pack(side="top", pady=10)

            self.label = tk.Label(self, bg=Home.COLOR_BG2, width=100)
            self.label.pack(side="top", pady=10)
            self.button = tk.Button(self, width=30, height=2, text="Se Connecter", activebackground=Home.COLOR_BG2,
                                    bg=Home.COLOR_BG2, bd=1, relief="solid", command=self.verify_user)
            self.button.pack(side="top", pady=20)

            self.master.bind("<Return>", lambda e: self.verify_user())

        def show(self):
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)
            self.user_name_entry.focus_set()

        def verify_user(self):
            u = User(self.user_name_entry.get(), self.user_pwd_entry.get())
            self.label.configure(text=("Connected as " + str(u.get_uuid())) if u.connected() else "User Not Found.",
                                 fg="#00ff00" if u.connected() else "#ff0000", font=("", 10, "bold"))
            self.update()
            if u.connected():
                self.master.unbind("<Return>")
                self.master.user = u
                time.sleep(0.5)
                self.destroy()
                Home.HomeFrame(self.master).show()

        def register_btn(self):
            self.master.unbind("<Return>")
            master = self.master
            self.destroy()
            Home.RegisterFrame(master).show()

    class RegisterFrame(tk.Frame):
        C_NORMAL = "#000000"
        C_WARN = "#ffa000"
        C_SPECIAL = "#00a0ff"
        C_ERROR = "#ff0000"

        F_NORMAL = ("TkDefaultFont", 9, "")
        F_MODIFY = ("TkDefaultFont", 9, "bold")

        C_0 = "#dedede"
        C_1 = "#ff0000"
        C_2 = "#ffa000"
        C_3 = "#ffff00"
        C_4 = "#00ff00"
        C_5 = "#00bb00"
        C_6 = "#00ffff"
        C_7 = "#007fff"
        C_8 = "#0000ff"
        C_9 = "#ff00ff"
        C_10 = "#000000"

        def __init__(self, master):
            super().__init__(master, bg=Home.COLOR_BG2, highlightthickness=2, highlightbackground="black")

            self.title = tk.Label(self, bg=Home.COLOR_BG2, height=1, font=("", 30,), text="S'inscrire")
            self.title.pack(side="top", pady=20)

            self.user_frame = tk.Frame(self, bg=Home.COLOR_BG2, height=300, width=650)

            self.user_name_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Nom d'utilisateur (définitif) :")
            self.user_name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            self.user_name_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=28, font=("JetBrains Mono", 10))
            self.user_name_entry.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

            tk.Frame(self.user_frame, bg=Home.COLOR_BG2).grid(row=1, column=0, columnspan=4, pady=10)

            self.complete_last_name_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Nom :")
            self.complete_last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.complete_last_name_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=20, font=("JetBrains Mono", 10))
            self.complete_last_name_entry.grid(row=2, column=1, padx=5, pady=5)

            self.complete_first_name_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Prénom :")
            self.complete_first_name_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
            self.complete_first_name_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=20, font=("JetBrains Mono", 10))
            self.complete_first_name_entry.grid(row=2, column=3, padx=5, pady=5)

            self.mail_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="E-Mail :")
            self.mail_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.mail_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=50, font=("JetBrains Mono", 10))
            self.mail_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

            tk.Frame(self.user_frame, bg=Home.COLOR_BG2).grid(row=4, column=0, columnspan=4, pady=10)

            self.lvl = tk.Frame(self.user_frame, bg=Home.COLOR_BG3, height=5, width=226)
            self.lvl.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

            self.pwd_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Mot de passe (peut être vide) :")
            self.pwd_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            self.pwd_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=28, font=("JetBrains Mono", 10), show="*")
            self.pwd_entry.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

            self.vpwd_label = tk.Label(self.user_frame, bg=Home.COLOR_BG2, text="Vérification du mot de passe :")
            self.vpwd_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            self.vpwd_entry = tk.Entry(self.user_frame, bg=Home.COLOR_BG, width=28, font=("JetBrains Mono", 10), show="*")
            self.vpwd_entry.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

            self.user_frame.pack(side="top", pady=25)

            self.other_frame = tk.Label(self, bg=Home.COLOR_BG2)
            self.login_label = tk.Label(self.other_frame, bg=Home.COLOR_BG2, text="Déjà membre ?")
            self.login_label.pack(side="left", padx=10)
            self.login_btn = tk.Button(self.other_frame, activebackground=Home.COLOR_BG2, bg=Home.COLOR_BG2,
                                          bd=0, relief="solid", text="Se Connecter.", font=("", 10, "underline"),
                                          command=self.login)
            self.login_btn.pack(side="left", padx=10)
            self.other_frame.pack(side="top", pady=10)

            self.label = tk.Label(self, bg=Home.COLOR_BG2, width=100)
            self.label.pack(side="top", pady=5)
            self.button = tk.Button(self, width=30, height=2, text="S'inscrire", activebackground=Home.COLOR_BG2,
                                    bg=Home.COLOR_BG2, bd=1, relief="solid", command=self.validate)
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
            return alphal ** 0.79 + alphau ** 0.79 + num ** 0.79 + spe ** 0.79 + other ** 0.79 - (0.999 if 0 < len(key) < 5 else 0)

        def show(self):
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=480, width=720)
            self.user_name_entry.focus_set()

        def login(self):
            self.master.unbind("<KeyPress>")
            self.master.unbind("<Return>")
            master = self.master
            self.destroy()
            Home.LogInFrame(master).show()

        def key_press(self, e=None):
            self.errors, self.warns = [], []

            if not self.user_name_entry.get():
                self.user_name_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                self.errors.append("Nom d'utilisateur attendu.")
            elif len(self.user_name_entry.get()) < 5:
                self.user_name_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                self.errors.append("Nom d'utilisateur trop court.")
            else:
                has_spe = False
                for c in self.user_name_entry.get().lower():
                    if c not in "abcdefghijklmnopqrstuvwxyz0123456789-._":
                        has_spe = True
                        break
                if has_spe:
                    self.user_name_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                    self.errors.append("Le nom d'utilisateur doit respecter : 'abcdefghijklmnopqrstuvwxyz0123456789-._'")
                elif self.user_name_entry.get() != self.user_name_entry.get().lower():
                    self.user_name_label.config(font=self.F_NORMAL, fg=self.C_WARN)
                    self.warns.append("Le nom d'utilisateur ne respecte pas la casse.")
                else:
                    self.user_name_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)

            if not self.complete_last_name_entry.get():
                self.complete_last_name_label.config(font=self.F_NORMAL, fg=self.C_NORMAL)
            else:
                self.complete_last_name_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)

            if not self.complete_first_name_entry.get():
                self.complete_first_name_label.config(font=self.F_NORMAL, fg=self.C_NORMAL)
            else:
                self.complete_first_name_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)

            if not self.mail_entry.get():
                self.mail_label.config(font=self.F_NORMAL, fg=self.C_NORMAL)
            elif self.mail_entry.get().count("@") == 1 and len(self.mail_entry.get().split("@")[0]) \
                    and len(self.mail_entry.get().split("@")[1]) >= 3 \
                    and self.mail_entry.get().split("@")[1].count(".") == 1:
                self.mail_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)
            else:
                self.mail_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                self.errors.append("Adresse mail valide attendue.")

            if not self.pwd_entry.get() and not self.vpwd_entry.get():
                self.pwd_label.config(font=self.F_NORMAL, fg=self.C_NORMAL)
                self.vpwd_label.config(font=self.F_NORMAL, fg=self.C_NORMAL)
            elif self.pwd_entry.get() == self.vpwd_entry.get():
                self.pwd_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)
                self.vpwd_label.config(font=self.F_NORMAL, fg=self.C_SPECIAL)
                if self.score(self.pwd_entry.get()) < 6:
                    self.pwd_label.config(font=self.F_NORMAL, fg=self.C_WARN)
                    self.warns.append("Le mot de passe est relativement simple.")
            else:
                self.pwd_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                self.vpwd_label.config(font=self.F_MODIFY, fg=self.C_ERROR)
                self.errors.append("Les mots de passes de correspondent pas.")

            if self.score(self.pwd_entry.get()) == 0:
                self.lvl.config(bg=self.C_0)
            elif self.score(self.pwd_entry.get()) < 4:
                self.lvl.config(bg=self.C_1)
            elif self.score(self.pwd_entry.get()) < 6:
                self.lvl.config(bg=self.C_2)
            elif self.score(self.pwd_entry.get()) < 7.85:
                self.lvl.config(bg=self.C_3)
            elif self.score(self.pwd_entry.get()) < 10:
                self.lvl.config(bg=self.C_4)
            elif self.score(self.pwd_entry.get()) < 12:
                self.lvl.config(bg=self.C_5)
            elif self.score(self.pwd_entry.get()) < 16:
                self.lvl.config(bg=self.C_6)
            elif self.score(self.pwd_entry.get()) < 20:
                self.lvl.config(bg=self.C_7)
            elif self.score(self.pwd_entry.get()) < 25:
                self.lvl.config(bg=self.C_8)
            elif self.score(self.pwd_entry.get()) < 30:
                self.lvl.config(bg=self.C_9)
            else:
                self.lvl.config(bg=self.C_10)

            if len(self.errors):
                self.label.config(font=self.F_MODIFY, fg=self.C_ERROR, text="Erreurs : " + " ; ".join(self.errors))
            elif len(self.warns):
                self.label.config(font=self.F_NORMAL, fg=self.C_WARN, text="Attention : " + " ; ".join(self.warns))
            else:
                self.label.config(font=self.F_NORMAL, fg=self.C_NORMAL, text="")

        def validate(self, e=None):
            if len(self.errors):
                return
            try:
                u = User.create_user(username=self.user_name_entry.get(), completename=(self.complete_first_name_entry.get()
                                     + " " + self.complete_last_name_entry.get()), mail=None if self.mail_entry.get() == ""
                                     else self.mail_entry.get(), password=self.pwd_entry.get())
            except UserAlreadyExistsException:
                self.label.config(font=self.F_MODIFY, fg=self.C_ERROR, text="Erreur : Le joueur existe déjà.")
                return
            self.label.configure(text=("Connected as " + str(u.get_uuid())) if u.connected() else "User Not Found.",
                                 fg="#00ff00" if u.connected() else "#ff0000", font=("", 10, "bold"))
            self.update()
            if u.connected():
                self.master.unbind("<KeyPress>")
                self.master.unbind("<Return>")
                self.master.user = u
                time.sleep(0.5)
                self.destroy()
                Home.HomeFrame(self.master).show()
