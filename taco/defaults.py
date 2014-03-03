import uuid
import taco.constants

default_settings_kv = {}
default_settings_kv["Download Location"] = "downloads/"
default_settings_kv["Nickname"] = "Your Nickname Here"
default_settings_kv["Application Port"] = 5440
default_settings_kv["Application IP"] = "0.0.0.0"
default_settings_kv["Web Port"] = 5340
default_settings_kv["Web IP"] = "127.0.0.1"
default_settings_kv["Download Limit"] = 50
default_settings_kv["Upload Limit"] = 50
default_settings_kv["Local UUID"] = unicode(uuid.uuid4().hex)
default_settings_kv["TacoNET Certificates Store"] = "certstore/"

default_peers_kv = {}
default_peers_kv["enabled"] = False
default_peers_kv["hostname"] = "127.0.0.1"
default_peers_kv["port"] = "9001"
default_peers_kv["localnick"] = "Local Nickname"
default_peers_kv["dynamic"] = False
default_peers_kv["clientkey"] = ""
default_peers_kv["serverkey"] = ""
