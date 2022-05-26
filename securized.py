
class MySQL:
    HOST = "luzog.xyz"
    USER = "dev"
    PASSWORD = "root"
    DATABASE = "ezy"


class ServerRessources:
    ICON = "http://luzog.xyz:48833/icon.ico"
    IMAGE = "http://luzog.xyz:48833/icon.png"
    DEFAULT_FACE = "http://luzog.xyz:48833/resources/default_face.png"


class PyInstaller:
    # --splash "rsrc/icon.png"
    COMMAND = 'pyinstaller --onefile --noconsole --workpath "build/work" --distpath "builds" --name "1.0-SNAPSHOT-alpha2.0.1" "center.py"'
