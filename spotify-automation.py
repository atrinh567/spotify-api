import requests
import json

from secrets import spotify_token, spotify_user_id

class CreatePlaylist:
    def __init__(self):
        self.spotify_token = spotify_token
        self.spotify_user_id = spotify_user_id
        self.playlist_id = self.create_playlist()

    def create_playlist(self):
        data = json.dumps({
            "name": "Playlist-test",
            "description": "Description",
            "public": False
        })
        headers = {
            "Content-Type": "Application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }

        if not self.check_if_duplicates(json.loads(data)["name"]):
            url = 'https://api.spotify.com/v1/users/{}/playlists'.format(spotify_user_id)
            req = requests.post(url, data=data, headers=headers)
            return req.json()["id"]
        else:
            print("Playlist name exists: {}".format(json.loads(data)["name"]))
            return self.find_playist_id(json.loads(data)["name"])

    def get_playlists(self):
        headers = {
            "Content-Type": "Application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }

        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(spotify_user_id)
        req = requests.get(url, headers=headers)

        playlists = json.loads(req.text)
        return playlists["items"]

    def check_if_duplicates(self, name):
        items = self.get_playlists()
        for i in items:
            if name == i["name"]:
                return True
        return False

    def find_playist_id(self, name):
        items = self.get_playlists()
        for i in items:
            if name == i["name"]:
                return i["id"]
        return "ID not found"

    def get_spotify_uri(self, track_name, artist_name):
        headers = {
            "Content-Type": "Application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
        
        url = "https://api.spotify.com/v1/search?q={}%2C{}&type=track%2Cartist&market=US&limit=1&offset=0".format(track_name, artist_name)

        req = requests.get(url, headers=headers)
        song = json.loads(req.text)
        return song["tracks"]["items"][0]["uri"]

    def add_song_to_playlist(self):
        songs = [
            {
                "name": "you and i",
                "artist": "michael buble"
            },
            {
                "name": "fly me to the moon",
                "artist": "frank sinatra"
            }
        ]

        headers = {
            "Content-Type": "Application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }

        for song in songs:
            url = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.playlist_id, self.get_spotify_uri(song["name"], song["artist"]))
            req = requests.post(url, headers=headers)
            print(req.json())

cp = CreatePlaylist()
cp.add_song_to_playlist()