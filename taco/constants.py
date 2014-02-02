from socket import gethostname
import struct
import re

APP_CODE_NAME = "Dirt Diver ZMQ"
#Cool Breeze,Betty Blue, Hammerhead, Dirt Diver, Whiplash, Whipporwill,Dog Patch 06,Red Cap
APP_NAME = "TacoNET"
APP_TAGLINE = ["Blue and Orange because I am a hack. --Scott","Save it for Beta. --Scott","Laddergoatdotcom.com --Scott","You're going to say THAT about Swifty? To ME of all people? AND WITH THAT TONE? --Scott","Forget the search feature. Why would we spend time developing something nobody will use? --Scott"]

APP_VERSION = 0.01
APP_STAGE = "Alpha"
APP_AUTHOR = ["Scott Powers"]

KB = 2 ** 10
MB = 2 ** 20
GB = 2 ** 30
TB = 2 ** 40

HOSTNAME = gethostname()
CHUNK_SIZE = 1024 * 16

ROLLCALL_MIN = 10
ROLLCALL_MAX = 20

KEEP_ALIVE_MIN = 15
KEEP_ALIVE_MAX = 25

CLIENT_COMMUNICATION_THRESHOLD = ROLLCALL_MAX + 10
CLIENT_RECONNECT_TIME = ROLLCALL_MIN * 10
CLIENT_FAILURE_COUNT = 5

MAX_NICKNAME_LENGTH = 64

MAX_CHAT_MESSAGE_LENGTH = 1024
MAX_CHAT_BACKLOG_SIZE = 128

FILESYSTEM_CACHE_TIME = 30.0

WEBSERVER_PORT = 8080
APPLICATION_PORT = 9119

JSON_SETTINGS_FILENAME = "settings.json"

