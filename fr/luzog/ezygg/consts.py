from dataclasses import dataclass
from ezyapi.game_manager import GameVersion


VERSION = GameVersion("b1.3")


class Constants:
    @dataclass
    class Globals:
        title: str
        not_now: str
        connected_as: str
        user_not_found: str

    @dataclass
    class Login:
        label: str
        user_name_label: str
        user_pwd_label: str
        forgot_pwd_btn: str
        register_btn: str
        button: str

    @dataclass
    class Register:
        label: str
        user_name_label: str
        complete_last_name_label: str
        complete_first_name_label: str
        mail_label: str
        pwd_label: str
        vpwd_label: str
        login_label: str
        login_btn: str
        button: str
        error_username_expected: str
        error_username_too_short: str
        error_username_must_respect: str
        warn_username_case: str
        error_mail_invalid: str
        warn_password_too_simple: str
        error_password_dont_match: str
        errors: str
        warns: str
        error_user_already_exists: str

    @dataclass
    class Home:
        welcome: str

    @dataclass
    class Menu:
        title: str
        all_games: str
        tops: str
        reward: str
        shop: str
        not_now: str
        top5: str
        politics: str
        total_players: str

    @dataclass
    class Center:
        pass

    @dataclass
    class Information:
        completename: str
        identifier: str
        mail: str
        creation: str
        lvl: str
        exp: str
        gp: str
        sets: str
        more: str
        logout: str
        not_now: str

    @dataclass
    class GameDiv:
        reward: str
        nothing: str
        play: str
        more: str
        not_now: str


@dataclass
class Lang:
    name: str
    globals: Constants.Globals
    login: Constants.Login
    register: Constants.Register
    home: Constants.Home
    menu: Constants.Menu
    center: Constants.Center
    information: Constants.Information
    game_div: Constants.GameDiv

    @staticmethod
    def FR():
        return Lang(
            name="fr",
            globals=Constants.Globals(
                title="EzyGames",
                not_now="Pas disponible pour l'instant... :/",
                connected_as="Connecté en temps que ",
                user_not_found="Aucun joueur trouvé.",
            ),
            login=Constants.Login(
                label="Connexion",
                user_name_label="Nom d'utilisateur :",
                user_pwd_label="Mot de passe :",
                forgot_pwd_btn="Mot de passe oublié ?",
                register_btn="S'inscrire.",
                button="Se Connecter",
            ),
            register=Constants.Register(
                label="S'inscrire",
                user_name_label="Nom d'utilisateur (définitif) :",
                complete_last_name_label="Nom :",
                complete_first_name_label="Prenom :",
                mail_label="E-Mail :",
                pwd_label="Mot de passe (peut être vide) :",
                vpwd_label="Vérification du mot de passe :",
                login_label="Déjà membre ?",
                login_btn="Se Connecter.",
                button="S'inscrire",
                error_username_expected="Nom d'utilisateur attendu.",
                error_username_too_short="Nom d'utilisateur trop court.",
                error_username_must_respect="Le nom d'utilisateur doit respecter :",
                warn_username_case="Le nom d'utilisateur ne respecte pas la casse.",
                error_mail_invalid="Adresse mail valide attendue.",
                warn_password_too_simple="Le mot de passe est relativement simple.",
                error_password_dont_match="Les mots de passes de correspondent pas.",
                errors="Erreurs :",
                warns="Attention :",
                error_user_already_exists="Erreur : Le joueur existe déjà.",
            ),
            home=Constants.Home(
                welcome="Bienvenue",
            ),
            menu=Constants.Menu(
                title="Menu : (non fonctionnel)",
                all_games="Tous les jeux",
                tops="Tops des joueurs",
                reward="Récompenses",
                shop="Boutique",
                not_now="Plus Tard... :/",
                top5="Top 5 :",
                politics="© Politique EzyGG",
                total_players="Total des Joueurs :",
            ),
            center=Constants.Center(

            ),
            information=Constants.Information(
                completename="Nom Complet :",
                identifier="Identifiant :",
                mail="E-Mail :",
                creation="Création :",
                lvl="Niveau de Jeu (LVL) :",
                exp="Points d'Experience (EXP) :",
                gp="Points de Jeu (GP) :",
                sets="Parties Gagnées / Jouées :",
                more="Voir Plus",
                logout="Déconnexion",
                not_now="Plus Tard... :/",
            ),
            game_div=Constants.GameDiv(
                reward="Récompenses :",
                nothing="Aucune Récompense",
                play="Jouer !",
                more="Voir Plus",
                not_now="Plus Tard... :/",
            ),
        )


class Display:
    @dataclass
    class Globals:
        color_bg: str = "gray"
        color_bg2: str = "dim gray"
        color_bg3: str = "dark gray"
        color_lvl: str = "#00FFFF"
        color_exp: str = "#00FF00"
        color_gp: str = "#FFFF00"
        color_special: str = "#FF00FF"

    @dataclass
    class Main:
        bg: str = "gray"
        highlightthickness: int = 16
        highlightbackground: str = "dim gray"

    @dataclass
    class Login:
        fg: str = "black"
        bg: str = "dim gray"
        entry_bg: str = "gray"
        highlightthickness: int = 2
        highlightbackground: str = "black"

    @dataclass
    class Register:
        bg: str = "dim gray"
        entry_bg: str = "gray"
        highlightthickness: int = 2
        highlightbackground: str = "black"

        c_normal: str = "#000000"
        c_warn: str = "#ffa000"
        c_special: str = "#00a0ff"
        c_error: str = "#ff0000"

        f_normal: tuple[str, int, str] = ("TkDefaultFont", 9, "")
        f_modify: tuple[str, int, str] = ("TkDefaultFont", 9, "bold")
        f_underlined: tuple[str, int, str] = ("TkDefaultFont", 10, "underline")
        f_mono: tuple[str, int, str] = ("Consolas", 11, "")  # JetBrains Mono

        C_0: str = "#dedede"
        C_1: str = "#ff0000"
        C_2: str = "#ffa000"
        C_3: str = "#ffff00"
        C_4: str = "#00ff00"
        C_5: str = "#00bb00"
        C_6: str = "#00ffff"
        C_7: str = "#007fff"
        C_8: str = "#0000ff"
        C_9: str = "#ff00ff"
        C_10: str = "#000000"

    @dataclass
    class Home:
        fg: str = "black"
        bg: str = "gray"
        highlightthickness: int = 10
        highlightbackground: str = "dim gray"

        f_welcome: tuple[str, int, str] = ("JetBrains Mono", 14, "bold")

    @dataclass
    class Menu:
        fg_title: str = "black"
        fg_text: str = "black"
        fg_info: str = "black"
        fg_players: str = "black"
        bg: str = "dim gray"

        f_title: tuple[str, int, str] = ("", 8, "bold italic")
        f_top: tuple[str, int, str] = ("", 8, "italic")
        f_info: tuple[str, int, str] = ("", 7, "underline")

    @dataclass
    class Center:
        bg: str = "dark gray"

    @dataclass
    class Information:
        fg_label: str = "black"
        fg_text: str = "black"
        fg_btn: str = "black"
        bg: str = "dim gray"

        f_label: tuple[str, int, str] = ("", 8, "bold")

    @dataclass
    class GameDiv:
        fg_title: str = "black"
        fg_catchphrase: str = "black"
        fg_label: str = "black"
        fg_nothing: str = "black"
        fg_btn: str = "black"
        bg: str = "gray"
        bg_image: str = "dim gray"
        highlightthickness: int = 2
        highlightbackground: str = "dim gray"

        f_title: tuple[str, int, str] = ("", 12, "bold underline")
        f_label: tuple[str, int, str] = ("", 8, "underline")
        f_reward: tuple[str, int, str] = ("", 8, "")
        f_nothing: tuple[str, int, str] = ("", 8, "bold")
        f_btn: tuple[str, int, str] = ("", 8, "")


@dataclass
class Theme:
    name: str
    globals: Display.Globals
    main: Display.Main
    login: Display.Login
    register: Display.Register
    home: Display.Home
    menu: Display.Menu
    center: Display.Center
    information: Display.Information
    game_div: Display.GameDiv

    @staticmethod
    def original():
        return Theme(
            name="original",
            globals=Display.Globals(),
            main=Display.Main(),
            login=Display.Login(),
            register=Display.Register(),
            home=Display.Home(),
            menu=Display.Menu(),
            center=Display.Center(),
            information=Display.Information(),
            game_div=Display.GameDiv(),
        )

    @staticmethod
    def default():
        return Theme(
            name="default",
            globals=Display.Globals("skyblue2", "slategray1", "slategray1"),
            main=Display.Main(),
            login=Display.Login(),
            register=Display.Register(),
            home=Display.Home(),
            menu=Display.Menu(),
            center=Display.Center(),
            information=Display.Information(),
            game_div=Display.GameDiv(),
        )

    @staticmethod
    def dark():
        return Theme(
            name="dark",
            globals=Display.Globals(),
            main=Display.Main(),
            login=Display.Login(),
            register=Display.Register(),
            home=Display.Home(),
            menu=Display.Menu(),
            center=Display.Center(),
            information=Display.Information(),
            game_div=Display.GameDiv(),
        )

    @staticmethod
    def light():
        return Theme(
            name="light",
            globals=Display.Globals(),
            main=Display.Main(),
            login=Display.Login(),
            register=Display.Register(),
            home=Display.Home(),
            menu=Display.Menu(),
            center=Display.Center(),
            information=Display.Information(),
            game_div=Display.GameDiv(),
        )
