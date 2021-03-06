import ezyapi.mysql_connection as connect
from ezyapi.UUID import UUID


# Doesnt work. It make all returns to None. TODO ->> Fix that
# def user_not_null(func, username: str | UUID = None, password: str = None):
#     if username is not None and password is not None:
#         if User(username, password).exists():
#             return func
#
#     def wrapper(*args, **kwargs):
#         if args[0].exists():
#             func(*args, **kwargs)
#         else:
#             raise UserNotFoundException(args[0].uuid, args[0].password)
#
#     return wrapper


class UserNotFoundException(Exception):
    def __init__(self, username=None, password=None):
        if username is not None and password is not None:
            super().__init__(f"User '{username}' with password : '{password}' cannot be found.")
        elif username is not None:
            super().__init__(f"User '{username}' cannot be found.")
        elif password is not None:
            super().__init__(f"User with password : '{password}' cannot be found.")
        else:
            super().__init__("User cannot be found.")


class UserAlreadyExistsException(Exception):
    def __init__(self):
            super().__init__("User already exists.")


class User:
    @staticmethod
    def create_user(username: str, uuid: str | UUID = None, admin: bool = False, frozen: bool = False,
                    completename: str = None, mail: str = None, password: str = ""):
        if not uuid: uuid = UUID(username)
        if User(username).exists():
            raise UserAlreadyExistsException()
        else:
            connect.execute(f"""INSERT users(uuid, admin, frozen, username, completename, mail, password)
                                VALUES ("{str(uuid).lower()}", {1 if admin else 0}, {1 if frozen else 0},
                                "{username.lower()}", {"null" if completename is None or completename == " " else
                                ('"' + completename + '"')}, {'null' if mail is None else ('"' + str(mail).lower()
                                + '"')}, "{"" if password is None else str(password).lower()}")""")
            connect.commit()
        return User(username, password)

    def __init__(self, connection_id: str | UUID, password: str = ""):
        self.uuid: UUID = None
        self.password: str = None
        self.reconnect(connection_id, password)

    def exists(self) -> bool:
        connect.execute(f"""SELECT * FROM users WHERE uuid="{str(self.uuid).lower()}"
                            OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}\"""")
        return bool(len(connect.fetch()))

    def connected(self) -> bool:
        connect.execute(f"""SELECT * FROM users WHERE (uuid="{str(self.uuid).lower()}"
                            OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}")
                            AND password="{self.password}\"""")
        return bool(len(connect.fetch()))

    def reconnect(self, connection_id: str | UUID, password: str = ""):
        self.uuid, self.password = str(connection_id), str(password)
        if self.connected():
            connect.execute(f"""SELECT uuid FROM users WHERE (uuid="{str(self.uuid).lower()}"
                                OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}")
                                AND password="{self.password}\"""")
            self.uuid = UUID.parseUUID(connect.fetch(1)[0])

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_username(self) -> str:
        connect.execute(f"""SELECT username FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_username(self, username: str):
        connect.execute(f"""UPDATE users SET username = "{username}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_completename(self) -> str:
        connect.execute(f"""SELECT completename FROM users WHERE uuid="{self.uuid}\"""")
        f = connect.fetch(1)[0]
        return self.get_username() if f is None else f

    def set_completename(self, completename: str):
        connect.execute(f"""UPDATE users SET completename = "{completename}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_mail(self) -> str:
        connect.execute(f"""SELECT mail FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_mail(self, mail: str):
        connect.execute(f"""UPDATE users SET mail = "{mail}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_password(self) -> str:
        connect.execute(f"""SELECT password FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_password(self, password: str):
        connect.execute(f"""UPDATE users SET password = "{password}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_creation(self):
        connect.execute(f"""SELECT creation FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def is_admin(self) -> bool:
        connect.execute(f"""SELECT admin FROM users WHERE uuid="{self.uuid}\"""")
        return bool(connect.fetch(1)[0])

    def set_admin(self, admin: bool):
        connect.execute(f"""UPDATE users SET admin = {1 if bool(admin) else 0} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def is_frozen(self) -> bool:
        connect.execute(f"""SELECT frozen FROM users WHERE uuid="{self.uuid}\"""")
        return bool(connect.fetch(1)[0])

    def set_frozen(self, frozen: bool):
        connect.execute(f"""UPDATE users SET frozen = {1 if bool(frozen) else 0} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_lvl(self) -> int:
        connect.execute(f"""SELECT lvl FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_lvl(self, lvl: int):
        connect.execute(f"""UPDATE users SET lvl = {lvl} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def add_lvl(self, lvl: int):
        connect.execute(f"""UPDATE users SET lvl = {self.get_lvl() + lvl} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def remove_lvl(self, lvl: int):
        connect.execute(f"""UPDATE users SET lvl = {self.get_lvl() - lvl} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_exp(self) -> int:
        connect.execute(f"""SELECT exp FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_exp(self, exp: int):
        connect.execute(f"""UPDATE users SET exp = {exp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def add_exp(self, exp: int):
        connect.execute(f"""UPDATE users SET exp = {self.get_exp() + exp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def remove_exp(self, exp: int):
        connect.execute(f"""UPDATE users SET exp = {self.get_exp() - exp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_gp(self) -> int:
        connect.execute(f"""SELECT gp FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_gp(self, gp: int):
        connect.execute(f"""UPDATE users SET gp = {gp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def add_gp(self, gp: int):
        connect.execute(f"""UPDATE users SET gp = {self.get_gp() + gp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def remove_gp(self, gp: int):
        connect.execute(f"""UPDATE users SET gp = {self.get_gp() - gp} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_theme(self) -> int:
        connect.execute(f"""SELECT theme FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_theme(self, theme: int):
        connect.execute(f"""UPDATE users SET theme = {theme} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_played_games(self) -> int:
        connect.execute(f"""SELECT * FROM sets WHERE player="{self.uuid}\"""")
        return len(connect.fetch())

    def get_total_wins(self) -> int:
        connect.execute(f"""SELECT * FROM sets WHERE player="{self.uuid}\" AND won=1""")
        return len(connect.fetch())
