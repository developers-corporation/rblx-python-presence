from pypresence import Presence
import json 
import requests
import time 
# make an application that shows what a player is playing on roblox to discord rich presence

def main():
    client_id = "1195220191051780106"  # Put your Client ID here
    RPC = Presence(client_id)  # Initialize the Presence client
    RPC.connect()  # Start the handshake loop

    # Load the token from config.json
    with open('./config.json') as f:
        data = json.load(f)
        cookieToken = data['token']

    RobloxAPI = Roblox()
    newToken = RobloxAPI.convertToken(cookieToken)
    RobloxAPI.setUserId(newToken)

    # Initialize variables to track previous presence type and start time
    prevPresenceType = None
    start_time = None

    while True:
        presence = RobloxAPI.getPresence(newToken)
        userPresenceType = presence['userPresences'][0]['userPresenceType']

        if prevPresenceType != userPresenceType:
            # Presence type has changed, reset start time
            start_time = get_epoch_time()
            prevPresenceType = userPresenceType

        # Get the necessary presence information based on the presence type
        if userPresenceType == 2:  # InGame
            universeId = presence['userPresences'][0]['universeId']
            gameName = RobloxAPI.getGameName(universeId)
            placeId = presence['userPresences'][0]['placeId']
            details = f"Playing {gameName}"
            state = "InGame"
            small_icon_url = RobloxAPI.getRobloxIcon()
            large_icon_url = RobloxAPI.getGameThumbnail(universeId)
        elif userPresenceType == 3:  # InStudio
            gameName = RobloxAPI.getGameName(None)
            details = f"Developing {gameName}"
            state = "InStudio"
            small_icon_url = RobloxAPI.getRobloxStudioIcon()
            large_icon_url = RobloxAPI.getGameThumbnail(None)
        else:
            # Skip the update if presence type is not InGame or InStudio
            continue

        RPC.update(
            details=details,
            state=state,
            large_image=large_icon_url,
            large_text=gameName,
            small_image=small_icon_url,
            small_text="Roblox",
            start=start_time,
            buttons=[
                {"label": "Play", "url": "https://www.roblox.com/games/" + str(placeId)},
                {"label": "Profile", "url": "https://www.roblox.com/users/" + str(RobloxAPI.userId) + "/profile"}
            ]
        )

        time.sleep(15)  # Update every 15 seconds
# class for Roblox API requests
class Roblox:
    def __init__(self):
       self.userId = None
       return
    
    def setUserId(self, token):
        # get the userId based on the token
        # provide the .ROBLOXSecurity cookie token in the request header -
        # accept: application/json
        # content-type: application/json
        # use users.roblox.com/v1/users/authenticated
        r = requests.get(f'https://users.roblox.com/v1/users/authenticated', headers={"Cookie": token, "accept": "application/json", "content-type": "application/json"})
        if r.status_code == 200:
            user = r.json()
            self.userId = user['id']
        else:
            print(f"Error getting userId {r.status_code}= {r.reason}")
            

    def getPresence(self, token):
        # provide the .ROBLOXSecurity cookie token and the user id in the request
        # header -
        # Cookie: .ROBLOSECURITY=token'
        # accept: application/json
        # content-type: application/json
        r = requests.post(f'https://presence.roblox.com/v1/presence/users', headers={"Cookie": token, "accept": "application/json", "content-type": "application/json"}, data=json.dumps({"userIds": [self.userId]}))
        if r.status_code == 200:
            presence = r.json()
            return presence
        else:
            print(f"Error getting presence {r.status_code}= {r.reason}")
            return 
        
    def convertToken(self, token):
        """
        converts the .ROBLOSECURITY cookie token to a format that can be used in the request
        params: token (str) - the ROBLOSECURITY cookie token
        returns: newToken (str) - the new ROBLSECURITY token
        """
        newToken = ".ROBLOSECURITY=" + token
        return newToken
    
    def getGameName(self, universeId):
        r = requests.get(f'https://games.roblox.com/v1/games?universeIds={universeId}')
        if r.status_code == 200:
            game = r.json()
            return game['data'][0]['name']
        else:
            print(f"Error getting game name {r.status_code}= {r.reason}")
            return 
        
    def getGameThumbnail(self, universeId):
        # get the game thumbnail from api
        r = requests.get(f'https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universeId}&size=768x432&format=Png&isCircular=false')
        if r.status_code == 200:
            game = r.json()
            return game['data'][0]['thumbnails'][0]['imageUrl']
        else:
            print(f"Error getting game thumbnail {r.status_code}= {r.reason}")
            return
        
    def getRobloxIcon(self):
        # get the roblox player icon from cdn
        return "https://cdn.glitch.global/972cbee0-d72e-4085-bc70-dcff2733fa78/roblox-player.png"
    
    def getRobloxStudioIcon(self):
        # get the roblox studio icon from cdn
        return "https://cdn.glitch.global/972cbee0-d72e-4085-bc70-dcff2733fa78/roblox-studio.png"


def get_epoch_time():
    # return as seconds
    return int(time.time())



if __name__ == '__main__':
    main()