import uuid
import taco.constants

default_settings_kv = {}
default_settings_kv["Download Location"] = "downloads/"
default_settings_kv["Nickname"] = "Your Nickname Here"
default_settings_kv["Application Port"] = 9001
default_settings_kv["Application IP"] = "0.0.0.0"
default_settings_kv["Web Port"] = 9002
default_settings_kv["Web IP"] = "127.0.0.1"
default_settings_kv["External Port"] = 9001
default_settings_kv["External IP"] = "127.0.0.1"
default_settings_kv["Download Limit"] = 50
default_settings_kv["Upload Limit"] = 50
default_settings_kv["Local UUID"] = unicode(str(uuid.uuid4()))
default_settings_kv["TacoNET Certificates Store"] = "certstore/"

default_peers_kv = {}
default_peers_kv["Enabled"] = False
default_peers_kv["Hostname"] = "127.0.0.1"
default_peers_kv["Port"] = "9001"
default_peers_kv["Nickname Local"] = "Local Nickname"
default_peers_kv["Nickname Remote"] = "Remote Nickname"
default_peers_kv["Broadcast"] = True
default_peers_kv["Dynamic"] = False
