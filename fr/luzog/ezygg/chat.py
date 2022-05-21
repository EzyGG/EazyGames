import tkinter as tk
from enum import Enum
from threading import Thread, Event
from datetime import datetime as dt

from ezyapi.sessions import User
import ezyapi.mysql_connection as connect

from fr.luzog.ezygg.consts import Theme

# from dataclasses import dataclass
#
#
# @dataclass
# class Tag:
#     tag: str
#     bg: str
#     fg: str
#     font: tuple[str, int, str]


class Tags(Enum):
    NORMAL = "r"
    MENTION = "u"
    MENTION_SELF = "us"
    SENDER = "s"
    SENDER_SELF = "ss"
    DATETIME = "t"

    COLOR_SENDER = "cs"
    COLOR_SENDER_SELF = "css"
    COLOR_SENDER_ADMIN = "csa"
    COLOR_SENDER_SELF_ADMIN = "cssa"

    COLOR_BLACK = "cb"
    COLOR_WHITE = "cw"
    COLOR_DARK_GRAY = "cdga"
    COLOR_GRAY = "cga"
    COLOR_DARK_BLUE = "cdb"
    COLOR_BLUE = "cb"
    COLOR_DARK_GREEN = "cdgr"
    COLOR_GREEN = "cgr"
    COLOR_DARK_AQUA = "cda"
    COLOR_AQUA = "ca"
    COLOR_DARK_RED = "cdr"
    COLOR_RED = "cr"
    COLOR_DARK_PURPLE = "cdp"
    COLOR_PURPLE = "cp"
    COLOR_GOLD = "cgo"
    COLOR_YELLOW = "cy"

    FORMAT_BOLD = "fb"
    FORMAT_ITALIC = "fi"
    FORMAT_UNDERLINE = "fu"
    FORMAT_BOLD_ITALIC = "fbi"
    FORMAT_BOLD_UNDERLINE = "fbu"
    FORMAT_ITALIC_UNDERLINE = "fib"
    FORMAT_BOLD_ITALIC_UNDERLINE = "fbiu"


class ChatItem(tk.Frame):
    def __init__(self, master, theme: Theme, uid: int, sender: User, content: str, datetime: str,
                 ourself=False, admin=False, pady=2):
        self.theme = theme
        self.uid, self.sender, self.content, self.datetime = uid, sender, content, datetime
        self.ourself, self.admin, self.pady = ourself, admin, pady

        super().__init__(master, background=self.theme.chat.bg)

        self.header_frame = tk.Frame(self, bg=self.theme.chat.bg)
        self.header_frame.pack(fill="x")

        # PhotoImage...

        self.header_text = tk.Text(self.header_frame, bg=self.theme.chat.bg, fg=self.theme.chat.c_default,
                                   font=self.theme.chat.f_default, relief="flat", width=22, wrap=tk.WORD)
        self.init_tags(self.header_text)
        self.header_text.insert("end", str(self.sender.get_completename()),
                                (Tags.NORMAL.value, Tags.SENDER_SELF.value if self.ourself else Tags.SENDER.value,
                                 Tags.COLOR_SENDER_SELF_ADMIN.value if self.ourself and self.admin else
                                 Tags.COLOR_SENDER_ADMIN.value if self.admin else
                                 Tags.COLOR_SENDER_SELF.value if self.ourself else
                                 Tags.COLOR_SENDER.value))
        self.header_text.insert("end", "  ", Tags.NORMAL.value)
        self.header_text.insert("end", str(self.datetime), Tags.DATETIME.value)
        self.header_text.pack(side="left", fill="x")

        self.footer_text = tk.Text(self, bg=self.theme.chat.bg, fg=self.theme.chat.c_default,
                                   font=self.theme.chat.f_default, relief="flat", width=22, wrap=tk.WORD)
        self.init_tags(self.footer_text)
        self.footer_text.insert("end", str(content), Tags.NORMAL.value)
        self.format()
        self.footer_text.pack(fill="x")

        self.header_text.config(state="disable")
        self.footer_text.config(state="disable")

        self.bind_all("<Configure>", self.up2date, add="+")

    def destroy(self):
        self.unbind_all("<Configure>")
        super().destroy()

    def format(self):
        cont: str = self.footer_text.get("1.0", "end")
        self.footer_text.delete("1.0", "end")

        colors = [Tags.COLOR_WHITE]

        index, dont_insert = 0, 0
        while True:
            char = cont[index]
            has_next = len(cont) - 1 > index

            if not has_next:
                break

            if char == "§" and dont_insert:
                dont_insert -= 1
            elif char == "§" and not dont_insert:
                c = cont[index + 1]
                # cont = "".join(cont[:index] + cont[index + 2:])
                dont_insert += 2
                match c:
                    case "0": colors.append(Tags.COLOR_BLACK)
                    case "1": colors.append(Tags.COLOR_DARK_BLUE)
                    case "2": colors.append(Tags.COLOR_DARK_GREEN)
                    case "3": colors.append(Tags.COLOR_DARK_AQUA)
                    case "4": colors.append(Tags.COLOR_DARK_RED)
                    case "5": colors.append(Tags.COLOR_DARK_PURPLE)
                    case "6": colors.append(Tags.COLOR_GOLD)
                    case "7": colors.append(Tags.COLOR_GRAY)
                    case "8": colors.append(Tags.COLOR_DARK_GRAY)
                    case "9": colors.append(Tags.COLOR_BLUE)
                    case "a": colors.append(Tags.COLOR_GREEN)
                    case "b": colors.append(Tags.COLOR_AQUA)
                    case "c": colors.append(Tags.COLOR_RED)
                    case "d": colors.append(Tags.COLOR_PURPLE)
                    case "e": colors.append(Tags.COLOR_YELLOW)
                    case "f": colors.append(Tags.COLOR_WHITE)
                    case "l": colors.append(Tags.FORMAT_BOLD)
                    case "o": colors.append(Tags.FORMAT_ITALIC)
                    case "n": colors.append(Tags.FORMAT_UNDERLINE)
                    case "r": colors = [Tags.COLOR_WHITE]
                    case _: pass

                colors = list(set(colors))

                # Unpack All
                if Tags.FORMAT_BOLD_ITALIC_UNDERLINE in colors:
                    colors.append(Tags.FORMAT_BOLD)
                    colors.append(Tags.FORMAT_ITALIC)
                    colors.append(Tags.FORMAT_UNDERLINE)
                    colors.remove(Tags.FORMAT_BOLD_ITALIC_UNDERLINE)
                if Tags.FORMAT_ITALIC_UNDERLINE in colors:
                    colors.append(Tags.FORMAT_ITALIC)
                    colors.append(Tags.FORMAT_UNDERLINE)
                    colors.remove(Tags.FORMAT_ITALIC_UNDERLINE)
                if Tags.FORMAT_BOLD_UNDERLINE in colors:
                    colors.append(Tags.FORMAT_BOLD)
                    colors.append(Tags.FORMAT_UNDERLINE)
                    colors.remove(Tags.FORMAT_BOLD_UNDERLINE)
                if Tags.FORMAT_BOLD_ITALIC in colors:
                    colors.append(Tags.FORMAT_BOLD)
                    colors.append(Tags.FORMAT_ITALIC)
                    colors.remove(Tags.FORMAT_BOLD_ITALIC)

                # Reduce to keep only necessary
                colors = list(set(colors))

                # Pack properly
                if Tags.FORMAT_BOLD in colors and Tags.FORMAT_ITALIC in colors and Tags.FORMAT_UNDERLINE in colors:
                    colors.remove(Tags.FORMAT_BOLD)
                    colors.remove(Tags.FORMAT_ITALIC)
                    colors.remove(Tags.FORMAT_UNDERLINE)
                    colors.append(Tags.FORMAT_BOLD_ITALIC_UNDERLINE)
                elif Tags.FORMAT_ITALIC in colors and Tags.FORMAT_UNDERLINE in colors:
                    colors.remove(Tags.FORMAT_ITALIC)
                    colors.remove(Tags.FORMAT_UNDERLINE)
                    colors.append(Tags.FORMAT_ITALIC_UNDERLINE)
                elif Tags.FORMAT_BOLD in colors and Tags.FORMAT_UNDERLINE in colors:
                    colors.remove(Tags.FORMAT_BOLD)
                    colors.remove(Tags.FORMAT_UNDERLINE)
                    colors.append(Tags.FORMAT_BOLD_UNDERLINE)
                elif Tags.FORMAT_BOLD in colors and Tags.FORMAT_ITALIC in colors:
                    colors.remove(Tags.FORMAT_BOLD)
                    colors.remove(Tags.FORMAT_ITALIC)
                    colors.append(Tags.FORMAT_BOLD_ITALIC)

            if dont_insert:
                dont_insert -= 1
            else:
                self.footer_text.insert("end", cont[index], [Tags.NORMAL.value] + [t.value for t in colors])
            index += 1

    @staticmethod
    def reduced(content):
        """COMPLETELY USELESS SINCE I FOUND text.config(wrap="word")"""
        reduced = True
        cont = content.split("\n")
        br = 22
        for i, c in enumerate(cont[:]):
            if len(c) > br:
                idx = br
                while c[idx] != " ":
                    idx -= 1
                    if idx < 0:
                        continue
                if idx >= 0:
                    cont[i] = cont[i][:idx] + "\n" + cont[i][idx + 1:]
                    reduced = False
        return "\n".join(cont) if reduced else ChatItem.reduced("\n".join(cont))

    def show(self):
        self.pack(pady=self.pady, fill="x")
        self.up2date()
        self.update()

    def up2date(self, e=None):
        self.header_text.config(height=self.header_text.count("1.0", "end", "displaylines")[0])
        self.footer_text.config(height=self.footer_text.count("1.0", "end", "displaylines")[0])

    def init_tags(self, text: tk.Text):
        text.tag_configure(Tags.NORMAL.value, **self.theme.chat.NORMAL)
        text.tag_configure(Tags.SENDER.value, **self.theme.chat.SENDER)
        text.tag_configure(Tags.SENDER_SELF.value, **self.theme.chat.SENDER_SELF)
        text.tag_configure(Tags.DATETIME.value, **self.theme.chat.DATETIME)

        text.tag_configure(Tags.FORMAT_BOLD.value, **self.theme.chat.FORMAT_BOLD)
        text.tag_configure(Tags.FORMAT_ITALIC.value, **self.theme.chat.FORMAT_ITALIC)
        text.tag_configure(Tags.FORMAT_UNDERLINE.value, **self.theme.chat.FORMAT_UNDERLINE)
        text.tag_configure(Tags.FORMAT_BOLD_ITALIC.value, **self.theme.chat.FORMAT_BOLD_ITALIC)
        text.tag_configure(Tags.FORMAT_BOLD_UNDERLINE.value, **self.theme.chat.FORMAT_BOLD_UNDERLINE)
        text.tag_configure(Tags.FORMAT_ITALIC_UNDERLINE.value, **self.theme.chat.FORMAT_ITALIC_UNDERLINE)
        text.tag_configure(Tags.FORMAT_BOLD_ITALIC_UNDERLINE.value, **self.theme.chat.FORMAT_BOLD_ITALIC_UNDERLINE)

        text.tag_configure(Tags.COLOR_SENDER.value, **self.theme.chat.COLOR_SENDER)
        text.tag_configure(Tags.COLOR_SENDER_SELF.value, **self.theme.chat.COLOR_SENDER_SELF)
        text.tag_configure(Tags.COLOR_SENDER_ADMIN.value, **self.theme.chat.COLOR_SENDER_ADMIN)
        text.tag_configure(Tags.COLOR_SENDER_SELF_ADMIN.value, **self.theme.chat.COLOR_SENDER_SELF_ADMIN)

        text.tag_configure(Tags.COLOR_BLACK.value, **self.theme.chat.COLOR_BLACK)
        text.tag_configure(Tags.COLOR_WHITE.value, **self.theme.chat.COLOR_WHITE)
        text.tag_configure(Tags.COLOR_DARK_GRAY.value, **self.theme.chat.COLOR_DARK_GRAY)
        text.tag_configure(Tags.COLOR_GRAY.value, **self.theme.chat.COLOR_GRAY)
        text.tag_configure(Tags.COLOR_DARK_BLUE.value, **self.theme.chat.COLOR_DARK_BLUE)
        text.tag_configure(Tags.COLOR_BLUE.value, **self.theme.chat.COLOR_BLUE)
        text.tag_configure(Tags.COLOR_DARK_GREEN.value, **self.theme.chat.COLOR_DARK_GREEN)
        text.tag_configure(Tags.COLOR_GREEN.value, **self.theme.chat.COLOR_GREEN)
        text.tag_configure(Tags.COLOR_DARK_AQUA.value, **self.theme.chat.COLOR_DARK_AQUA)
        text.tag_configure(Tags.COLOR_AQUA.value, **self.theme.chat.COLOR_AQUA)
        text.tag_configure(Tags.COLOR_DARK_RED.value, **self.theme.chat.COLOR_DARK_RED)
        text.tag_configure(Tags.COLOR_RED.value, **self.theme.chat.COLOR_RED)
        text.tag_configure(Tags.COLOR_DARK_PURPLE.value, **self.theme.chat.COLOR_DARK_PURPLE)
        text.tag_configure(Tags.COLOR_PURPLE.value, **self.theme.chat.COLOR_PURPLE)
        text.tag_configure(Tags.COLOR_GOLD.value, **self.theme.chat.COLOR_GOLD)
        text.tag_configure(Tags.COLOR_YELLOW.value, **self.theme.chat.COLOR_YELLOW)


class ChatFrame(tk.Frame):
    def __init__(self, master, main, theme, lang, x=4, y=400, relx=0, rely=0):
        self.main, self.theme, self.lang = main, theme, lang
        self.place_x, self.place_y, self.place_relx, self.place_rely = x, y, relx, rely
        self.height, self.width = 0, 0
        self.__is_in = False

        super().__init__(master, background=self.theme.chat.bg)

        self.entry = tk.Text(self, bg=self.theme.chat.bg, fg=self.theme.chat.c_default, font=self.theme.chat.f_entry, height=2)
        self.entry.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(self, background=self.theme.chat.bg, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both")
        self.container = tk.Frame(self.canvas, bg=self.theme.chat.bg)
        self.canvas.create_window(0, 0, anchor="nw", window=tk.Frame(bg=self.theme.chat.bg))
        self.canvas.create_window(self.width / 2, 0, anchor="nw", window=self.container)

        self.spacing_frame = tk.Frame(self.container, bg=self.theme.chat.bg, height=100)
        self.spacing_frame.pack()

        self.limit = 10
        self.fetching_up = False
        self.chats: dict[int, ChatItem] = {}

        self.canvas.bind_all("<Configure>", self.update_place, add="+")
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel, add="+")
        self.canvas.bind("<Enter>", lambda e: self.is_in(True))
        self.canvas.bind("<Leave>", lambda e: self.is_in(False))
        self.entry.bind("<KeyPress-Return>", self.on_enter)
        self.entry.bind("<KeyRelease-Up>", self.on_up)

        self.refreshing = True
        self.refreshing_timeout = 1

        self.after(1000, self.update_place)

    def listener(self):
        if self.refreshing:
            self.chat_fetch(self.limit)
        if self.refreshing:
            self.after(self.refreshing_timeout, self.listener)

    def destroy(self):
        self.refreshing = False
        for item in list(self.chats.values()):
            item.destroy()
        self.canvas.unbind_all("<Configure>")
        super().destroy()

    def is_in(self, __set_is_in: bool | None = None) -> bool:
        if __set_is_in is not None:
            self.__is_in = __set_is_in
        return self.__is_in

    def on_mousewheel(self, event):
        if not self.fetching_up:
            if self.is_in():
                self.canvas.yview_scroll(int(-event.delta / 120), "units")
            if self.canvas.yview()[0] == 0.0:
                self.fetching_up = True
                self.limit += 10
                self.chat_fetch(limit=10, up=True)
                self.canvas.yview_scroll(5, "units")
                self.fetching_up = False

    def on_enter(self, e=None):
        content = self.entry.get("1.0", "end")[:-1]
        if content.replace(" ", "").replace("\t", "").replace("\0", "").replace("\n", "") == "":
            return
        last = self.chat_get_last_id()
        if last != max(list(self.chats.keys()) + [0]):
            self.chat_fetch()
            last = self.chat_get_last_id()
        self.chat_submit(ChatItem(self.container, self.theme, last + 1,
                                  self.main.user, content, str(dt.now().strftime(self.theme.chat.datetime_format)),
                                  True, self.main.user.is_admin()))
        self.after(50, lambda: self.entry.delete("1.0", "end"))

    def on_up(self, event):
        if self.entry.get("1.0", "end").replace(" ", "").replace("\t", "").replace("\0", "").replace("\n", ""):
            return
        c = self.chat_get_last_posted()
        if c:
            self.entry.delete("1.0", "end")
            self.entry.insert("1.0", c.content)

    def chat_get(self, uid: int) -> ChatItem | None:
        return self.chats.get(uid)

    def chat_get_last(self) -> ChatItem | None:
        return list(self.chats.values())[-1] if len(self.chats.items()) else None

    def chat_get_last_id(self) -> int:
        connect.close()
        connect.connexion()
        connect.execute("""SELECT max(id) FROM chat""")
        return connect.fetch(1)[0]

    def chat_get_last_posted(self) -> ChatItem | None:
        for c in list(self.chats.values())[::-1]:
            if c.ourself:
                return c
        return None

    def chat_delete(self, uid: int) -> ChatItem | None:
        chat = self.chats.get(uid)
        if chat:
            chat.forget()
            self.chats.pop(uid)
        return chat

    def chat_submit(self, *chats: ChatItem, commit: bool = True, up: bool = False):
        action = "SEND"
        yview = self.canvas.yview()[1]
        for chat in chats:
            if commit:
                cont = chat.content.replace('"', "\\\"")
                connect.execute(f"""INSERT INTO chat(id, action, user, content) VALUES ({chat.uid}, "{action}",
                                    "{chat.sender.get_uuid().getUUID()}", "{cont}")""")
                connect.commit()
            if up:
                self.chats = {chat.uid: chat} | self.chats
            else:
                self.chats[chat.uid] = chat
                chat.show()
        if yview >= 0.95:
            self.canvas.yview_scroll(99, "pages")

    def chat_fetch(self, limit: int = -2, up: bool = False):
        """
        Limit Param :
          > -2 == self.limit

          > -1 == infinite

          > 0 == no fetch

          > k == k
        """
        connect.close()
        connect.connexion()
        if up:
            changes = False
            connect.execute(f"""SELECT id, user, action, content, deleted, date FROM chat WHERE deleted = 0
                                AND id >= {min(list(self.chats.keys()) + [999999999999999]) - limit}
                                AND id < {min(list(self.chats.keys()) + [999999999999999])}""")
            for uid, user, action, content, deleted, date in connect.fetch()[::-1]:
                changes = True
                self.chat_submit(ChatItem(self.container, self.theme, uid,
                                          User(user), content, str(date.strftime(self.theme.chat.datetime_format)),
                                          self.main.user.get_uuid().getUUID() == user,
                                          True if not User(user).exists() else User(user).is_admin()),
                                 commit=False, up=True)
            if changes:
                for i, c in self.chats.items():
                    if c.winfo_ismapped():
                        c.forget()
                for i, c in self.chats.items():
                    c.show()
        else:
            connect.execute("""SELECT id, user, action, content, deleted, date FROM chat WHERE deleted = 1""")
            for uid, user, action, content, deleted, date in connect.fetch():
                if uid in list(self.chats.keys()):
                    self.chat_delete(uid)
            connect.execute(f"""SELECT id, user, action, content, deleted, date FROM chat WHERE deleted = 0 AND id >
                             {max(list(self.chats.keys()) + [self.chat_get_last_id() - limit if limit >= 0 else 0])}""")
            for uid, user, action, content, deleted, date in connect.fetch():
                self.chat_submit(ChatItem(self.container, self.theme, uid,
                                          User(user), content, str(date.strftime(self.theme.chat.datetime_format)),
                                          self.main.user.get_uuid().getUUID() == user,
                                          True if not User(user).exists() else User(user).is_admin()), commit=False)
        self.update()

    def geometry(self):
        self.height, self.width = 250, self.master.winfo_width() * 95 / 100
        return self.height, self.width

    def show(self):
        self.place()
        self.update_place()
        self.listener()

    def update_place(self, e=None):
        self.geometry()
        self.place_configure(x=self.place_x, y=self.place_y, relx=self.place_relx, rely=self.place_rely,
                             anchor="nw", height=self.height, width=self.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
