#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:57:58 2023

@author: lou
"""
import requests
import spotipy
from spotipy import util

client_id='CLIENT ID'
client_secret='CLIENT SECRET'
redirect_uri='http://localhost:8888/callback'

username = 'USERNAME'

scope_playlist = 'playlist-modify-public'
scope_user = 'user-library-read'
scope_playing = 'user-read-currently-playing'

AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

#Convert response to JSON
auth_response_data = auth_response.json()

#Save the access token
access_token = auth_response_data['access_token']

#Need to pass access token into header to send properly formed GET request to API server
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

token_playlist= util.prompt_for_user_token(username,scope_playlist,client_id,client_secret,redirect_uri) 
sp_playlist = spotipy.Spotify(auth=token_playlist)

data = 'setlists.txt'
with open(data) as f:
    lines = f.readlines()
ids = []

BASE_URL = 'https://api.spotify.com/v1/'
for line in lines:
    r = requests.get(BASE_URL + 'search?q='+line.replace(' ','%20')+'&type=track', headers=headers)
    r = r.json()
    try:
        tracks = r['tracks']['items']
        try:
            print(tracks[0]['name']+" by "+tracks[0]['artists'][0]['name']+" - "+tracks[0]['id'])
            ids.append(tracks[0]['id'])
        except IndexError:
            pass
    except KeyError:
        pass
    
l = len(ids)

new_playlist = sp_playlist.user_playlist_create(username,"Tiny Desk - ALL SONGS",public=True)
centaine = 99
while centaine<l:
    sp_playlist.user_playlist_add_tracks(username,playlist_id=new_playlist['id'],tracks= ids[centaine-99:centaine])
    centaine +=99
sp_playlist.user_playlist_add_tracks(username,playlist_id=new_playlist['id'],tracks= ids[centaine-99:l])
