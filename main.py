from pypresence import Presence
import json 
import requests
import time 
# make an application that shows what a player is playing on roblox to discord rich presence

def main():
    client_id = "1195220191051780106"  # Put your Client ID in here
    RPC = Presence(client_id)  # Initialize the Presence client
    RPC.connect() # Start the handshake loop

    # lets get the current playing game based on the userid provided from config.json
    with open('config.json') as f:
        data = json.load(f)
        userId = data['user_id']
    # enums for userPresencetypes given by presence.roblox.com
    userPresencetypes = {
        0: "Offline",
        1: "Online",
        2: "InGame",
        3: "InStudio",
}
    RobloxAPI = Roblox(userId)
    presence = RobloxAPI.getPresence()
    print(presence)


# class for Roblox API requests
class Roblox:
    def __init__(self, userId):
        self.userId = userId

    def getPresence(self):
        r = requests.post(f'https://presence.roblox.com/v1/presence/users', json={"userIds": [self.userId]})
        if r.status_code == 200:
            presence = r.json()
            return presence
        else:
            raise(f"Error getting presence {r.status_code}= {r.reason}")
    

def get_epoch_time():
    return int(time.time())


if __name__ == '__main__':
    main()