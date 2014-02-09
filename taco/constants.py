from socket import gethostname

APP_CODE_NAME = "Dirt Diver ZMQ"
#Cool Breeze,Betty Blue, Hammerhead, Dirt Diver, Whiplash, Whipporwill,Dog Patch 06,Red Cap
APP_NAME = "TacoNET"
APP_TAGLINE = []
APP_TAGLINE.append("It's blue and orange because I am a hack. --Scott")
APP_TAGLINE.append("Save it for beta. --Scott")
APP_TAGLINE.append("Laddergoatdotcom.com --Scott")
APP_TAGLINE.append("You're going to say THAT about Swifty? To ME of all people? AND WITH THAT TONE? --Scott")
APP_TAGLINE.append("Forget the search feature. Why would we spend time developing something nobody will use? --Scott")
APP_TAGLINE.append("No is an acceptable answer. --Scott")

APP_VERSION = 0.03
APP_STAGE = "Pre-Alpha"
APP_AUTHOR = ["Scott Powers"]

KB = 2 ** 10
MB = 2 ** 20
GB = 2 ** 30
TB = 2 ** 40

CHAT_LOG_MAXSIZE = 128

HOSTNAME = gethostname()
CHUNK_SIZE = 1024 * 16

JSON_SETTINGS_FILENAME = "settings.json"
CERT_STORE_DIR = "certstore/"

KEY_GENERATION_PREFIX = "taconet"

CLIENT_RECONNECT = 60

ROLLCALL_MIN = 2 
ROLLCALL_MAX = 5
ROLLCALL_TIMEOUT = ROLLCALL_MAX * 2

NET_GARBAGE = "G"
NET_REQUEST = "r"
NET_REPLY = "R"
NET_DATABLOCK = "D"

NET_REQUEST_ROLLCALL = "a"
NET_REPLY_ROLLCALL   = "A"

