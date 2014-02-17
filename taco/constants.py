from socket import gethostname
import re
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

APP_VERSION = 0.04
APP_STAGE = "Pre-Alpha"
APP_AUTHOR = ["Scott Powers"]

KB = 2 ** 10
MB = 2 ** 20
GB = 2 ** 30
TB = 2 ** 40
MAX_NICKNAME_LENGTH = 48
MAX_CHAT_MESSAGE_LENGTH = 512
CHAT_LOG_MAXSIZE = 128

HOSTNAME = gethostname()
CHUNK_SIZE = 1024 * 16

JSON_SETTINGS_FILENAME = "settings.json"
CERT_STORE_DIR = "certstore/"

KEY_GENERATION_PREFIX = "taconet"

CLIENT_RECONNECT_MIN = 0
CLIENT_RECONNECT_MOD = 2
CLIENT_RECONNECT_MAX = 16

FILESYSTEM_CACHE_TIMEOUT = 120
FILESYSTEM_LISTING_TIMEOUT = 300
FILESYSTEM_CACHE_PURGE = 30
FILESYSTEM_WORKER_COUNT = 10
FILESYSTEM_RESULTS_SIZE = 16
FILESYSTEM_CHUNK_SIZE = KB * 16

ROLLCALL_MIN = 2 
ROLLCALL_MAX = 5
ROLLCALL_TIMEOUT = ROLLCALL_MAX * 2

NET_GARBAGE = "G"
NET_IDENT = "I"

NET_REQUEST = "r"
NET_REPLY = "R"
NET_DATABLOCK = "D"

NET_REQUEST_ROLLCALL = "a"
NET_REPLY_ROLLCALL   = "A"

NET_REQUEST_CERTS    = "b"
NET_REPLY_CERTS      = "B"

NET_REQUEST_CHAT     = "c"
NET_REPLY_CHAT       = "C"

NET_REQUEST_SHARE_LISTING = "d"
NET_REPLY_SHARE_LISTING = "D"

NET_REQUEST_SHARE_LISTING_RESULTS = "dd"
NET_REPLY_SHARE_LISTING_RESULTS = "DD"


RE_UUID_CHECKER = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
RE_NICKNAME_CHECKER = "^[\w\.\-\(\) ]{3,"+str(MAX_NICKNAME_LENGTH)+"}$"
RE_PORT_CHECKER = "^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$"
RE_HOST_CHECKER = "^(?:(?:(?:(?:[a-zA-Z0-9][-a-zA-Z0-9]{0,61})?[a-zA-Z0-9])[.])*(?:[a-zA-Z][-a-zA-Z0-9]{0,61}[a-zA-Z0-9]|[a-zA-Z])[.]?)$"
RE_CHAT_CHECKER = "^[!-~ ]{1,"+str(MAX_CHAT_MESSAGE_LENGTH)+"}$"
RE_IP_CHECKER = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

UUID_CHECKER = re.compile(RE_UUID_CHECKER,re.UNICODE)
NICKNAME_CHECKER = re.compile(RE_NICKNAME_CHECKER,re.UNICODE)
CHAT_CHECKER = re.compile(RE_CHAT_CHECKER,re.UNICODE)
SHARE_NAME_CHECKER = re.compile(u"^\w[\w \-\.]{1,126}\w$",re.UNICODE)
DIR_NAME_CHECKER = re.compile(u"^\w[\w \-\.]{1,126}\w$",re.UNICODE)
