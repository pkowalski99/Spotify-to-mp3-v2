from __future__ import unicode_literals
from http import client
from youtube_search import YoutubeSearch
from threading import Thread
import requests, sys, os, time, spotipy
import spotipy.oauth2 as oauth2
import pandas as pd
import yt_dlp as youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist':True,
    'keepvideo': False,
    'http-chunk-size': "10M",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}




def downloadPlaylist(playlist):
    threads = []
    for song in playlist:
        tempThread = Thread(target=downloadSong, args=(song,))
        threads.append(tempThread)
    for thread in threads:
        thread.start()
    print("Waiting")


def downloadSong(song):
    try:
        songUrl = YoutubeSearch(song, max_results=1).to_dict()
        songUrl = "https://www.youtube.com{}".format(songUrl[0]['url_suffix'])
    except:
        print(f"No valind url for song: {song}")
        pass
    finally:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(songUrl)

def validateUserCredentials(clientId, clientSecret, userName, playlistId):
    if clientId == "" or clientId == None or len(clientId) < 5: return False
    if clientSecret == "" or clientSecret == None or len(clientSecret) < 5: return False
    if userName == "" or userName == None or len(userName) < 5: return False
    if playlistId == "" or playlistId == None or len(playlistId) < 5: return False
    return True

       

def getPlaylist(spotify, username, playlistId):
    songsInPlaylist = []
    try:
        playlist = spotify.user_playlist(username, playlistId, fields='tracks,next,name')
    except:
        sys.exit("Something went wrong, probably wrong credentials")
    finally:
        playlist_name = playlist['name']
        tracks = playlist['tracks']
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    songsInPlaylist.append("{} - {}".format( track['artists'][0]['name'], track['name']))

                except:
                    pass
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break
        return songsInPlaylist


def main():
    os.system("CLS")
    while True:
        os.system("CLS")
        userName = input("Enter your user name")
        clientId = input("Enter your client id")
        clientSecret = input("Enter your client secret")
        playListId = input("Enter your playlist id")
        if validateUserCredentials(clientId, clientSecret,userName, playListId):
            break
        else:
            print("Enter correct informations!")
            continue
    auth_manager = oauth2.SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlist = getPlaylist(spotify, userName, playListId)
    downloadPlaylist(playlist)






if __name__ == "__main__":
    main()

