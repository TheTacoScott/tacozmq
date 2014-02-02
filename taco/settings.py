def Load_Settings():
    save_after = False
    with taco.globals.settings_lock:
        try:
            taco.globals.settings = json.loads(open(taco.constants.JSON_SETTINGS_FILENAME,'r').read())
            if not taco.globals.settings.has_key("Download Location"):
                taco.globals.settings["Download Location"] = "/tmp"
                save_after = True
            if not taco.globals.settings.has_key("Nickname"):
                taco.globals.settings["Nickname"] = "Your Nickname Here"
                save_after = True
            if not taco.globals.settings.has_key("Application Port"):
                taco.globals.settings["Application Port"] = 9001
                save_after = True
            if not taco.globals.settings.has_key("Application IP"):
                taco.globals.settings["Application IP"] = "0.0.0.0"
                save_after = True
            if not taco.globals.settings.has_key("Web Port"):
                taco.globals.settings["Web Port"] = 9002
                save_after = True
            if not taco.globals.settings.has_key("Web IP"):
                taco.globals.settings["Web IP"] = "127.0.0.1"
                save_after = True
            if not taco.globals.settings.has_key("External Port"):
                 taco.globals.settings["External Port"] = 9001
                 save_after = True
            if not taco.globals.settings.has_key("External IP"):
                taco.globals.settings["External IP"] = "127.0.0.1"
                save_after = True
            if not taco.globals.settings.has_key("Download Limit"):
                taco.globals.settings["Download Limit"] = 50
                save_after = True
            if not taco.globals.settings.has_key("Upload Limit"):
                taco.globals.settings["Upload Limit"] = 50
                save_after = True
            if not taco.globals.settings.has_key("Local UUID"):
                taco.globals.settings["Local UUID"] = unicode(str(uuid.uuid4()))
                save_after = True
            if not taco.globals.settings.has_key("Shares"):
                taco.globals.settings["Shares"] = []
                save_after = True
            if not taco.globals.settings.has_key("Peers"):
                taco.globals.settings["Peers"] = {}
                save_after = True
            with taco.globals.shares_lock:
                valid_list = True
                for index,value in enumerate(taco.globals.settings["Shares"]):
                    if type(value) == type(unicode("test")):
                        taco.globals.settings["Shares"][index] = [str(uuid.uuid4()),value]
                        save_after = True
                    elif type(value) == type([]) and len(value) == 2:
                        pass
                    else:
                        valid_list = False
                if valid_list:       
                    taco.globals.shares = taco.globals.settings["Shares"]
                else:
                    taco.globals.shares = []
                    save_after = True
            with taco.globals.peers_lock:
                for peer_uuid in taco.globals.settings["Peers"].keys():
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Enabled"):
                        taco.globals.settings["Peers"][peer_uuid]["Enabled"] = False
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Hostname"):
                        taco.globals.settings["Peers"][peer_uuid]["Hostname"] = "127.0.0.1"
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Port"):
                        taco.globals.settings["Peers"][peer_uuid]["Port"] = 9001
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Nickname Local"):
                        taco.globals.settings["Peers"][peer_uuid]["Nickname Local"] = ""
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Nickname Remote"):
                        taco.globals.settings["Peers"][peer_uuid]["Nickname Remote"] = peer_uuid
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Password Incoming"):
                        taco.globals.settings["Peers"][peer_uuid]["Password Incoming"] = ""
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Password Outgoing"):
                        taco.globals.settings["Peers"][peer_uuid]["Password Outgoing"] = ""
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Broadcast"):
                        taco.globals.settings["Peers"][peer_uuid]["Broadcast"] = True
                        save_after = True
                    if not taco.globals.settings["Peers"][peer_uuid].has_key("Dynamic"):
                        taco.globals.settings["Peers"][peer_uuid]["Dynamic"] = False
                        save_after = True
                    
                taco.globals.peers = taco.globals.settings["Peers"]
        except:
            taco.globals.SafePrint("Loading Settings Default")
            taco.globals.settings = {}
            taco.globals.settings["Network Password"] = "Some password here"
            taco.globals.settings["Download Location"] = "/tmp"
            taco.globals.settings["Nickname"] = "Your Nickname Here"
            taco.globals.settings["Application Port"] = 9001
            taco.globals.settings["Application IP"] = "0.0.0.0"
            taco.globals.settings["Web Port"] = 9002
            taco.globals.settings["Web IP"] = "127.0.0.1"
            taco.globals.settings["External Port"] = 9001
            taco.globals.settings["External IP"] = "127.0.0.1"
            taco.globals.settings["Download Limit"] = 50
            taco.globals.settings["Upload Limit"] = 50
            taco.globals.settings["Local UUID"] = unicode(str(uuid.uuid4()))
            with taco.globals.shares_lock:
                taco.globals.shares = []
            with taco.globals.peers_lock:
                taco.globals.peers = {}
            save_after = True
    taco.globals.SafePrint("*** Settings Loaded ***")
    if save_after:
        Save_Settings()
    #Print_Settings()

def Save_Settings():
    with taco.globals.settings_lock:
        with taco.globals.shares_lock:
            taco.globals.settings["Shares"] = taco.globals.shares
        with taco.globals.peers_lock:
            taco.globals.settings["Peers"] = taco.globals.peers

        open(taco.constants.JSON_SETTINGS_FILENAME,'w').write(json.dumps(taco.globals.settings,indent=4,sort_keys=True))
    taco.globals.SafePrint("*** Settings Saved ***")
    Load_Settings()
